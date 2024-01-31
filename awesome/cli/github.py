import asyncio
import datetime
import logging
import pathlib
from collections.abc import Mapping, Sequence
from typing import Annotated, Optional

import httpx
import pydantic
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
    delay: float = (
        rate_limit.rate.reset.timestamp() - datetime.datetime.now().timestamp()
    )
    logging.error(
        "Rate Limit Exceeded: Reset at %s after %s seconds",
        rate_limit.rate.reset,
        delay,
    )
    await asyncio.sleep(delay)
    raise tenacity.TryAgain()


@tenacity.retry(
    stop=stop.stop_after_attempt(4), wait=wait.wait_random_exponential(min=1)
)
async def get_commits(repo: str, token: Optional[str] = None) -> int:
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
        if response.status_code == 403:
            await handle_rate_limit(client=client)
        response.raise_for_status()
        json = response.json()
        return json["data"]["repository"]["object"]["history"]["totalCount"]


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
            logging.warning("Moved: %s -> %s", repo, result.full_name)
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
    for category, repos in data.items():
        repos: Sequence[Repository] = sorted(
            repos, key=lambda repo: repo.stargazers_count, reverse=True
        )
        print(f"## {category}")
        for repo in repos:
            output: str = f"- [{repo.name}]({repo.html_url})"
            output += f" (:star: {repo.stargazers_count:,}"
            output += f" | :octicons-commit-24: {repo.commits:,})"
            if repo.description:
                output += f" - {repo.description}"
            print(output)
