import asyncio
import datetime
import math
import os
from collections.abc import Iterable
from typing import Any

import aiocache
import githubkit
import pydantic
from githubkit import retry
from githubkit.versions.latest import models
from loguru import logger


@aiocache.cached()
async def get_repo_raw(full_name: str) -> models.FullRepository:
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
    return repository


@aiocache.cached()
async def get_commits(full_name: str) -> list[models.Commit]:
    _: Any
    token: str | None = os.getenv("GH_TOKEN")
    owner: str
    repo: str
    owner, _, repo = full_name.partition("/")
    async with githubkit.GitHub(
        token, auto_retry=retry.RetryRateLimit(max_retry=4)
    ) as gh:
        response: githubkit.Response[
            list[models.Commit]
        ] = await gh.rest.repos.async_list_commits(owner, repo)
    commits: list[models.Commit] = response.parsed_data
    return commits


@aiocache.cached()
async def get_participation(full_name: str) -> models.ParticipationStats:
    _: Any
    token: str | None = os.getenv("GH_TOKEN")
    owner: str
    repo: str
    owner, _, repo = full_name.partition("/")
    async with githubkit.GitHub(
        token, auto_retry=retry.RetryRateLimit(max_retry=4)
    ) as gh:
        response: githubkit.Response[
            models.ParticipationStats
        ] = await gh.rest.repos.async_get_participation_stats(owner, repo)
    participation: models.ParticipationStats = response.parsed_data
    return participation


class Repository(pydantic.BaseModel):
    activity_score: int | None = None
    description: str | None = None
    forks: pydantic.NonNegativeInt
    full_name: str
    html_url: pydantic.HttpUrl
    language: str | None = None
    name: str
    owner: str
    stars: pydantic.NonNegativeInt


async def get_updated_at(repo: models.FullRepository) -> datetime.datetime:
    commits: list[models.Commit] = await get_commits(repo.full_name)
    updated_at: datetime.datetime = repo.updated_at
    try:
        updated_at = datetime.datetime.fromisoformat(commits[0].commit.author.date)  # pyright: ignore
    except Exception as e:
        logger.error(e)
    finally:
        return updated_at


@logger.catch(default=None)
async def calc_score(repo: models.FullRepository) -> int:
    # initial score is 50 to give active repos with low GitHub KPIs (forks, watchers, stars) a better starting point
    score: float = 50

    # weighting: forks and watches count most, then stars, add some little score for open issues, too
    score += repo.forks_count * 5
    score += repo.subscribers_count
    score += repo.stargazers_count / 3
    score += repo.open_issues_count / 5

    # updated in last 3 months: adds a bonus multiplier between 0..1 to overall score (1 = updated today, 0 = updated more than 100 days ago)
    updated_at: datetime.datetime = await get_updated_at(repo)
    days_since_last_update: float = (
        datetime.datetime.now(datetime.UTC) - updated_at
    ).days
    score *= 1 + (100 - min(days_since_last_update, 100)) / 100

    # evaluate participation stats for the previous  3 months
    participation: models.ParticipationStats = await get_participation(repo.full_name)
    average_commits_per_week: float = sum(participation.all_[-13:]) / 13
    score *= 1 + min(max(average_commits_per_week - 3, 0), 7) / 7

    # boost calculation:
    # all repositories updated in the previous year will receive a boost of maximum 1000 declining by days since last update
    boost: float = 1000 - min(days_since_last_update, 365) * 2.74
    # gradually scale down boost according to repository creation date to mix with "real" engagement stats
    days_since_creation: float = (
        datetime.datetime.now(datetime.UTC) - repo.created_at
    ).days
    boost *= (365 - min(days_since_creation, 365)) / 365
    # add boost to score
    score += boost
    # give projects with a meaningful description a static boost of 50
    score += 50 if repo.description and len(repo.description) > 30 else 0
    # give projects with contribution guidelines (CONTRIBUTING.md) file a static boost of 100
    # iScore += (repo._InnerSourceMetadata.guidelines ? 100 : 0);
    # build in a logarithmic scale for very active projects (open ended but stabilizing around 5000)
    if score > 3000:
        score = 3000 + math.log(score) * 100
    # final score is a rounded value starting from 0 (subtract the initial value)
    score = round(score - 50)

    return score


async def get_repo(full_name: str) -> Repository:
    repository: models.FullRepository = await get_repo_raw(full_name)
    activity_score: int = await calc_score(repository)
    result: Repository = Repository(
        activity_score=activity_score,
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
        logger.warning("Moved: {} -> {}", full_name, result.full_name)
    return result


async def get_repos(repos: Iterable[str]) -> list[Repository]:
    return await asyncio.gather(*[get_repo(repo) for repo in repos])
