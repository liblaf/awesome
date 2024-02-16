import asyncio
import pathlib
from typing import Annotated, Any, Mapping, Optional, Sequence

import pydantic
import typer
import yaml

from awesome.api import github as _github
from awesome.api import website as _website
from awesome.typing import check_type as _check_type


class _CollectionRaw:
    websites: Sequence[str]
    repos: Sequence[str]

    def __init__(self, value: Any) -> None:
        if v := _check_type(value, Mapping[str, Sequence[str]]):
            self.websites = v.get("websites", [])
            self.repos = v.get("repos", [])
        elif v := _check_type(value, Sequence[str]):
            self.websites = []
            self.repos = []
            for s in v:
                if s.startswith("https://"):
                    self.websites.append(s)
                else:
                    self.repos.append(s)
        else:
            raise NotImplementedError()


class _Collection(pydantic.BaseModel):
    websites: Sequence[_website.Website]
    repos: Sequence[_github.Repository]


async def _get_collection(
    collection: _CollectionRaw, token: str | None = None
) -> _Collection:
    websites: Sequence[_website.Website] = await _website.get_websites(
        map(str, collection.websites)
    )
    repos: Sequence[_github.Repository] = await _github.get_repos(
        collection.repos, token=token
    )
    return _Collection(websites=websites, repos=repos)


async def _get_collections(
    collections: Mapping[str, _CollectionRaw], token: str | None = None
) -> Mapping[str, _Collection]:
    return {
        category: await _get_collection(collection, token=token)
        for category, collection in collections.items()
    }


def main(
    data_file: Annotated[pathlib.Path, typer.Argument(exists=True, dir_okay=False)],
    *,
    title: Annotated[str, typer.Option()] = "GitHub",
    token: Annotated[
        Optional[str], typer.Option(envvar=["GH_TOKEN", "GITHUB_TOKEN"])
    ] = None,
) -> None:
    data: Mapping[str, Any] = yaml.safe_load(data_file.read_text())
    data = {k: _CollectionRaw(v) for k, v in data.items()}
    collections: Mapping[str, _Collection] = asyncio.run(
        _get_collections(data, token=token)
    )
    print(
        f"""\
---
hide:
  - navigation
---
# {title}
!!! note
    Commits are counted from the last year only.\
"""
    )
    for category, collection in collections.items():
        print(f"## {category}")
        if collection.websites:
            print('<div class="cards grid favicon links" markdown>')
            for website_ in collection.websites:
                print(website_.markdown)
            print("</div>")
        if collection.repos:
            for repo in collection.repos:
                print(repo.markdown)
