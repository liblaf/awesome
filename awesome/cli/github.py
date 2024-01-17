import asyncio
import datetime
import os
import pathlib
from collections.abc import Mapping, Sequence
from typing import Annotated, Optional

import httpx
import loguru
import pandas as pd
import pydantic
import slugify
import tenacity
import typer
import yaml
from tenacity import stop, wait


class Repository(pydantic.BaseModel):
    commits: int = -1
    description: Optional[str]
    full_name: str
    html_url: str
    name: str
    stargazers_count: int


class RateLimit(pydantic.BaseModel):
    class Rate(pydantic.BaseModel):
        limit: int
        used: int
        remaining: int
        reset: datetime.datetime

    rate: Rate


async def handle_rate_limit(client: httpx.AsyncClient) -> None:
    response: httpx.Response = await client.get("https://api.github.com/rate_limit")
    response.raise_for_status()
    rate_limit: RateLimit = RateLimit(**response.json())
    loguru.logger.error(
        "Rate Limit Exceeded: Reset at {} after {} seconds",
        rate_limit.rate.reset,
        rate_limit.rate.reset.timestamp() - datetime.datetime.now().timestamp(),
    )
    await asyncio.sleep(
        rate_limit.rate.reset.timestamp() - datetime.datetime.now().timestamp()
    )
    raise tenacity.TryAgain()


@tenacity.retry(
    stop=stop.stop_after_attempt(32), wait=wait.wait_random_exponential(min=1)
)
async def get_commits(repo: str, token: Optional[str] = None) -> int:
    async with httpx.AsyncClient(
        headers={"Authorization": f"Bearer {token}"} if token else None,
        follow_redirects=True,
    ) as client:
        response: httpx.Response = await client.get(
            f"https://api.github.com/repos/{repo}/stats/commit_activity"
        )
        if response.status_code == 403:
            await handle_rate_limit(client=client)
        response.raise_for_status()
        if response.status_code == 202:
            raise tenacity.TryAgain()
        return sum(week["total"] for week in response.json())


@tenacity.retry(
    stop=stop.stop_after_attempt(4), wait=wait.wait_random_exponential(min=1)
)
async def get_repo(repo: str, token: Optional[str] = None) -> Repository:
    async with httpx.AsyncClient(
        headers={"Authorization": f"Bearer {token}"} if token else None,
        follow_redirects=True,
    ) as client:
        response: httpx.Response = await client.get(
            f"https://api.github.com/repos/{repo}"
        )
        if response.status_code == 403:
            await handle_rate_limit(client=client)
        response.raise_for_status()
        result: Repository = Repository(
            **response.json(), commits=await get_commits(repo=repo, token=token)
        )
        if result.full_name != repo:
            loguru.logger.warning("Moved: {} -> {}", repo, result.full_name)
        return result


async def get_repos(
    data: Mapping[str, Sequence[str]], token: Optional[str] = None
) -> Mapping[str, Sequence[Repository]]:
    return {
        category: await asyncio.gather(
            *[get_repo(repo=repo, token=token) for repo in repos]
        )
        for category, repos in data.items()
    }


def main(
    data_path: Annotated[pathlib.Path, typer.Argument(exists=True, dir_okay=False)],
    output_dir: Annotated[pathlib.Path, typer.Argument(exists=False, file_okay=False)],
    *,
    title: Annotated[str, typer.Option()] = "GitHub",
    token: Annotated[
        Optional[str], typer.Option(envvar=["GH_TOKEN", "GITHUB_TOKEN"])
    ] = None,
) -> None:
    lists: Mapping[str, Sequence[str]] = yaml.safe_load(data_path.read_text())
    data: Mapping[str, Sequence[Repository]] = asyncio.run(
        get_repos(data=lists, token=token)
    )
    os.makedirs(output_dir, exist_ok=True)
    print(
        f"""# {title}

!!! note

    Commits are counted from the last year only."""
    )
    for category, repos in data.items():
        data_frame: pd.DataFrame = pd.DataFrame.from_records(
            data=[
                (
                    f"[{repo.name}]({repo.html_url})",
                    repo.stargazers_count,
                    repo.commits,
                    repo.description or " ",
                )
                for repo in repos
            ],
            columns=["Name", "Stars", "Commits", "Description"],
        )
        data_frame.sort_values(by="Stars", ascending=False, inplace=True)
        output_path: pathlib.Path = output_dir / f"{slugify.slugify(category)}.csv"
        data_frame.to_csv(output_path, index=False)
        print(
            f"""
## {category}

{{{{ read_csv("{output_path}", intfmt=",") }}}}"""
        )
