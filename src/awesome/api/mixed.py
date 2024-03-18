import re

import pydantic

from awesome.api import github as _github
from awesome.api import website as _website
from awesome.api.github import Repository as Repository
from awesome.api.website import Website as Website


class Collection(pydantic.BaseModel):
    repos: list[Repository]
    websites: list[Website]


class Data(pydantic.BaseModel):
    data: dict[str, Collection]


async def get_collection(collection: list[str]) -> Collection:
    repos_input: list[str] = [s for s in collection if re.fullmatch(r"(\w+)/(\w+)", s)]
    repos: list[_github.Repository] = await _github.get_repos(repos_input)
    websites_input: list[str] = [s for s in collection if s.startswith("https://")]
    websites: list[_website.Website] = await _website.get_websites(websites_input)
    return Collection(websites=websites, repos=repos)


async def get_collections(
    collections: dict[str, list[str]],
) -> dict[str, Collection]:
    return {
        category: await get_collection(collection)
        for category, collection in collections.items()
    }
