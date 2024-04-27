import pydantic

from awesome.api import github as _github
from awesome.api import website as _website


class Item(pydantic.BaseModel):
    github: str | None = None
    website: pydantic.HttpUrl | None = None


class Data(pydantic.BaseModel):
    github: dict[str, _github.Repo] = {}
    website: dict[pydantic.HttpUrl, _website.Website] = {}


async def fetch_items(input: list[Item]) -> Data:
    github_list: list[_github.Repo] = await _github.fetch_github_list(
        set(item.github for item in input if item.github)
    )
    website_list: list[_website.Website] = await _website.fetch_website_list(
        set(str(item.website) for item in input if item.website)
    )
    return Data(
        github={repo.nameWithOwner: repo for repo in github_list},
        website={website.url: website for website in website_list},
    )
