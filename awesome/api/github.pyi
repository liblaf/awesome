import datetime
from collections.abc import Mapping, Sequence

import httpx
import pydantic

class RateLimit(pydantic.BaseModel):
    class Rate(pydantic.BaseModel):
        limit: pydantic.NonNegativeInt
        used: pydantic.NonNegativeInt
        remaining: pydantic.NonNegativeInt
        reset: datetime.datetime
    resources: Mapping[str, Rate]
    rate: Rate

async def handle_rate_limit(client: httpx.AsyncClient) -> None: ...
async def get_commits(repo: str, token: str | None = None) -> int:
    """https://github.com/badges/shields/blob/master/services/github/github-commit-activity.service.js"""

class Repository(pydantic.BaseModel):
    commits: pydantic.NonNegativeInt | None
    description: str | None
    full_name: str
    html_url: pydantic.HttpUrl
    name: str
    stargazers_count: pydantic.NonNegativeInt
    @property
    def markdown(self) -> str: ...

async def get_repo(repo: str, token: str | None = None) -> Repository: ...
async def get_repos(
    repos: Sequence[str], token: str | None = None
) -> Sequence[Repository]: ...
