import asyncio
import os
from collections.abc import Iterable
from typing import Any

import githubkit
import pydantic
from githubkit import retry


class Language(pydantic.BaseModel):
    color: str
    name: str


class Repo(pydantic.BaseModel):
    forkCount: int
    name: str
    nameWithOwner: str
    owner: str
    primaryLanguage: Language | None = None
    shortDescriptionHTML: str
    stargazerCount: int
    url: str


QUERY: str = """\
query ($owner: String!, $name: String!) {
    repository(owner: $owner, name: $name) {
        forkCount
        name
        nameWithOwner
        owner {
            login
        }
        primaryLanguage {
            name
            color
        }
        shortDescriptionHTML
        stargazerCount
        url
    }
}
"""


class Response(pydantic.BaseModel):
    class Repository(pydantic.BaseModel):
        forkCount: int
        name: str
        nameWithOwner: str

        class Owner(pydantic.BaseModel):
            login: str

        owner: Owner
        primaryLanguage: Language | None = None
        shortDescriptionHTML: str
        stargazerCount: int
        url: str

    repository: Repository


async def fetch_github(client: githubkit.GitHub, nameWithOwner: str) -> Repo:
    _: Any
    owner: str
    name: str
    owner, _, name = nameWithOwner.partition("/")
    response = Response(
        **await client.async_graphql(
            query=QUERY, variables={"owner": owner, "name": name}
        )
    )
    repository: Response.Repository = response.repository
    return Repo(
        forkCount=repository.forkCount,
        name=repository.name,
        nameWithOwner=repository.nameWithOwner,
        owner=repository.owner.login,
        primaryLanguage=repository.primaryLanguage,
        shortDescriptionHTML=repository.shortDescriptionHTML,
        stargazerCount=repository.stargazerCount,
        url=repository.url,
    )


async def fetch_github_list(nameWithOwner: Iterable[str]) -> list[Repo]:
    token: str | None = os.getenv("GH_TOKEN")
    async with githubkit.GitHub(
        token, auto_retry=retry.RetryRateLimit(max_retry=4)
    ) as client:
        return await asyncio.gather(
            *[fetch_github(client, name) for name in nameWithOwner]
        )
