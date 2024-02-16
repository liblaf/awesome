import datetime
from collections.abc import Mapping, Sequence

import pydantic

class _RateLimit(pydantic.BaseModel):
    class Rate(pydantic.BaseModel):
        limit: pydantic.NonNegativeInt
        used: pydantic.NonNegativeInt
        remaining: pydantic.NonNegativeInt
        reset: datetime.datetime
    resources: Mapping[str, Rate]
    rate: Rate

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
