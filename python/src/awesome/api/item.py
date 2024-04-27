import pydantic

from awesome.api import github as _github


class Item(pydantic.BaseModel):
    github: str | None = None


class Data(pydantic.BaseModel):
    github: dict[str, _github.Repo] = {}


async def fetch_items(input: list[Item]) -> Data:
    github_list: list[_github.Repo] = await _github.fetch_github_list(
        set(item.github for item in input if item.github)
    )
    return Data(github={repo.nameWithOwner: repo for repo in github_list})
