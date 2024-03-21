import asyncio
import os
from collections.abc import Iterable
from typing import Any

import githubkit
import pydantic
import tenacity
from githubkit import retry
from githubkit.versions.latest import models
from loguru import logger


class Repository(pydantic.BaseModel):
    description: str | None
    forks: pydantic.NonNegativeInt
    full_name: str
    html_url: pydantic.HttpUrl
    language: str | None
    name: str
    owner: str
    stars: pydantic.NonNegativeInt


@tenacity.retry(
    stop=tenacity.stop_after_attempt(4), wait=tenacity.wait_random_exponential(min=1)
)
async def get_repo(full_name: str) -> Repository:
    _: Any
    token: str | None = os.getenv("GH_TOKEN")
    owner: str
    repo: str
    owner, _, repo = full_name.partition("/")
    async with githubkit.GitHub(
        token, auto_retry=retry.RetryRateLimit(max_retry=4)
    ) as gh:
        response: githubkit.Response[
            models.FullRepository
        ] = await gh.rest.repos.async_get(owner, repo)
        repository: models.FullRepository = response.parsed_data
        result: Repository = Repository(
            description=repository.description,
            forks=repository.forks_count,
            full_name=full_name,
            html_url=repository.html_url,  # pyright: ignore
            language=repository.language,
            name=repository.name,
            owner=repository.owner.login,
            stars=repository.stargazers_count,
        )
        if result.full_name != full_name:
            logger.warning("Moved: {} -> {}", repo, result.full_name)
        return result


async def get_repos(repos: Iterable[str]) -> list[Repository]:
    return await asyncio.gather(*[get_repo(repo) for repo in repos])
