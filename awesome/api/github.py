import asyncio
import datetime
from collections.abc import Mapping, Sequence

import httpx
import pydantic
import tenacity
from loguru import logger


class _RateLimit(pydantic.BaseModel):
    class Rate(pydantic.BaseModel):
        limit: pydantic.NonNegativeInt
        used: pydantic.NonNegativeInt
        remaining: pydantic.NonNegativeInt
        reset: datetime.datetime

    resources: Mapping[str, Rate]
    rate: Rate


async def _handle_rate_limit(client: httpx.AsyncClient) -> None:
    response: httpx.Response = await client.get("https://api.github.com/rate_limit")
    response.raise_for_status()
    rate_limit: _RateLimit = _RateLimit(**response.json())
    resources: dict[str, _RateLimit.Rate] = {
        **rate_limit.resources,
        "rest": rate_limit.rate,
    }
    name: str
    reset: _RateLimit.Rate
    name, reset = max(
        [(name, reset) for name, reset in resources.items() if reset.remaining == 0],
        key=lambda item: item[1].reset,
    )
    delay: datetime.timedelta = reset.reset - datetime.datetime.now()
    logger.error("Rate limit exceeded: %s, reset in %s", name, delay.total_seconds())
    await asyncio.sleep(delay.total_seconds())
    raise tenacity.TryAgain()


@tenacity.retry(
    stop=tenacity.stop_after_attempt(4), wait=tenacity.wait_random_exponential(min=1)
)
async def _get_commits(repo: str, token: str | None = None) -> int:
    """https://github.com/badges/shields/blob/master/services/github/github-commit-activity.service.js"""
    async with httpx.AsyncClient(
        headers={"Authorization": f"Bearer {token}"} if token else None,
        follow_redirects=True,
    ) as client:
        user: str
        user, _, repo = repo.partition("/")
        since: datetime.datetime = datetime.datetime.now()
        since = since.replace(year=since.year - 1)
        response: httpx.Response = await client.post(
            "https://api.github.com/graphql",
            json={
                "query": """\
query (
    $user: String!
    $repo: String!
    $branch: String!
    $since: GitTimestamp
) {
    repository(owner: $user, name: $repo) {
        object(expression: $branch) {
            ... on Commit {
                history(since: $since) {
                    totalCount
                }
            }
        }
    }
}\
""",
                "variables": {
                    "user": user,
                    "repo": repo,
                    "branch": "HEAD",
                    "since": since.isoformat(),
                },
            },
        )
        if response.status_code == httpx.codes.FORBIDDEN:
            await _handle_rate_limit(client=client)
        response.raise_for_status()
        json = response.json()
        return json["data"]["repository"]["object"]["history"]["totalCount"]


class Repository(pydantic.BaseModel):
    commits: pydantic.NonNegativeInt | None
    description: str | None
    full_name: str
    html_url: pydantic.HttpUrl
    name: str
    stargazers_count: pydantic.NonNegativeInt

    @property
    def markdown(self) -> str:
        result: str = f"- [{self.name}]({self.html_url})"
        result += f" (:star: {self.stargazers_count:,}"
        result += f" | :octicons-commit-24: {self.commits:,})"
        if self.description:
            result += f" - {self.description}"
        return result


@tenacity.retry(
    stop=tenacity.stop_after_attempt(4), wait=tenacity.wait_random_exponential(min=1)
)
async def get_repo(repo: str, token: str | None = None) -> Repository:
    async with httpx.AsyncClient(
        headers={"Authorization": f"Bearer {token}"} if token else None,
        follow_redirects=True,
    ) as client:
        response: httpx.Response = await client.get(
            f"https://api.github.com/repos/{repo}"
        )
        if response.status_code == 403:
            await _handle_rate_limit(client=client)
        response.raise_for_status()
        result: Repository = Repository(
            **response.json(), commits=await _get_commits(repo=repo, token=token)
        )
        if result.full_name != repo:
            logger.warning("Moved: %s -> %s", repo, result.full_name)
        return result


async def get_repos(
    repos: Sequence[str], token: str | None = None
) -> Sequence[Repository]:
    return await asyncio.gather(*[get_repo(repo, token=token) for repo in repos])
