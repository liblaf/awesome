import asyncio
import datetime
import os
from collections.abc import Iterable

import httpx
import pydantic
import tenacity
from loguru import logger


class RateLimit(pydantic.BaseModel):
    class Rate(pydantic.BaseModel):
        limit: pydantic.NonNegativeInt
        used: pydantic.NonNegativeInt
        remaining: pydantic.NonNegativeInt
        reset: datetime.datetime

    resources: dict[str, Rate]
    rate: Rate


async def handle_rate_limit(client: httpx.AsyncClient) -> None:
    response: httpx.Response = await client.get("https://api.github.com/rate_limit")
    response.raise_for_status()
    rate_limit: RateLimit = RateLimit(**response.json())
    resources: dict[str, RateLimit.Rate] = {
        **rate_limit.resources,
        "rest": rate_limit.rate,
    }
    name: str
    reset: RateLimit.Rate
    name, reset = max(
        [(name, reset) for name, reset in resources.items() if reset.remaining == 0],
        key=lambda item: item[1].reset,
    )
    delay: datetime.timedelta = reset.reset - datetime.datetime.now(datetime.UTC)
    logger.error("Rate limit exceeded: {}, reset in {}", name, delay)
    await asyncio.sleep(delay.total_seconds())
    raise tenacity.TryAgain


class Repository(pydantic.BaseModel):
    description: str | None
    full_name: str
    html_url: pydantic.HttpUrl
    name: str
    stargazers_count: pydantic.NonNegativeInt


@tenacity.retry(
    stop=tenacity.stop_after_attempt(4), wait=tenacity.wait_random_exponential(min=1)
)
async def get_repo(repo: str) -> Repository:
    token: str | None = os.getenv("GH_TOKEN")
    async with httpx.AsyncClient(
        headers={"Authorization": f"Bearer {token}"} if token else None,
        follow_redirects=True,
    ) as client:
        response: httpx.Response = await client.get(
            f"https://api.github.com/repos/{repo}"
        )
        if response.status_code == httpx.codes.FORBIDDEN:
            await handle_rate_limit(client=client)
        response.raise_for_status()
        result: Repository = Repository(**response.json())
        if result.full_name != repo:
            logger.warning("Moved: {} -> {}", repo, result.full_name)
        return result


async def get_repos(repos: Iterable[str]) -> list[Repository]:
    return await asyncio.gather(*[get_repo(repo) for repo in repos])
