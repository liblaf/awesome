import asyncio
import datetime
import pathlib
from collections.abc import Mapping, Sequence
from typing import Annotated

import httpx
import loguru
import pydantic
import tenacity
import typer
import yaml
from tenacity import stop, wait


class Index(pydantic.BaseModel):
    id: int
    title: str


class Subject(pydantic.BaseModel):
    class Images(pydantic.BaseModel):
        common: str
        grid: str
        large: str
        medium: str
        small: str

    class Rating(pydantic.BaseModel):
        score: float

    date: datetime.date
    id: int
    images: Images
    name_cn: str
    name: str
    rating: Rating
    summary: str


class GetIndexSubjectsResponse(pydantic.BaseModel):
    class Subject(pydantic.BaseModel):
        id: int

    data: Sequence[Subject]
    limit: int
    offset: int
    total: int


@tenacity.retry(stop=stop.stop_after_attempt(4), wait=wait.wait_random_exponential())
async def get_subject(id: int) -> Subject:
    async with httpx.AsyncClient() as client:
        response: httpx.Response = await client.get(
            f"https://api.bgm.tv/v0/subjects/{id}"
        )
        response.raise_for_status()
        result: Subject = Subject(**response.json())
        assert result.id == id
        return result


@tenacity.retry(stop=stop.stop_after_attempt(4), wait=wait.wait_random_exponential())
async def get_index(id: int) -> Index:
    async with httpx.AsyncClient() as client:
        response: httpx.Response = await client.get(
            f"https://api.bgm.tv/v0/indices/{id}"
        )
        response.raise_for_status()
        result: Index = Index(**response.json())
        assert result.id == id
        return result


@tenacity.retry(stop=stop.stop_after_attempt(4), wait=wait.wait_random_exponential())
async def get_index_subjects(id: int) -> Sequence[Subject]:
    async with httpx.AsyncClient() as client:
        response: httpx.Response = await client.get(
            f"https://api.bgm.tv/v0/indices/{id}/subjects"
        )
        response.raise_for_status()
        response_body: GetIndexSubjectsResponse = GetIndexSubjectsResponse(
            **response.json()
        )
        if response_body.limit < response_body.total:
            loguru.logger.warning(
                "Limit ({}) < Total ({})", response_body.limit, response_body.total
            )
        return await asyncio.gather(
            *[get_subject(id=subject.id) for subject in response_body.data]
        )


async def get_all(ids: Sequence[int]) -> Mapping[str, Sequence[Subject]]:
    return {
        (await get_index(id=id)).title: await get_index_subjects(id=id) for id in ids
    }


def main(
    data_path: Annotated[pathlib.Path, typer.Argument(exists=True, dir_okay=False)],
    *,
    title: Annotated[str, typer.Option()] = "ACG",
) -> None:
    lists: Sequence[int] = yaml.safe_load(data_path.read_text())
    data: Mapping[str, Sequence[Subject]] = asyncio.run(get_all(ids=lists))
    print(f"# {title}")
    for category, subjects in data.items():
        print(
            f"""
## {category}

<div class="cards grid links" markdown>
"""
        )
        for subject in subjects:
            print(
                f"""- <a href="https://bgm.tv/subject/{subject.id}">
    <figure>
      <img alt="{subject.name_cn or subject.name}" src="{subject.images.grid}" />
      <figcaption>
        <span> {subject.name_cn or subject.name} </span> <br />
        <span class="acg-info"> {subject.date} / {subject.rating.score} </span>
      </figcaption>
    </figure>
  </a>"""
            )
        print()
        print("</div>")
