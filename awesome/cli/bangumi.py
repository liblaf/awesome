import asyncio
import datetime
import enum
from collections import defaultdict
from collections.abc import Mapping, MutableMapping, MutableSequence, Sequence
from typing import Annotated, Optional

import httpx
import pydantic
import tenacity
import typer
from tenacity import stop, wait

USER_AGENT: Optional[str] = "liblaf/awesome (https://github.com/liblaf/awesome)"


class CollectionType(enum.IntEnum):
    想看 = 1
    看过 = 2
    在看 = 3
    搁置 = 4
    抛弃 = 5

    def __str__(self) -> str:
        return self.name

    @property
    def emoji(self) -> str:
        return COLLECTIONS[self]


COLLECTIONS: Mapping[CollectionType, str] = {
    CollectionType.想看: ":star:",
    CollectionType.看过: ":thumbsup:",
    CollectionType.在看: ":material-play:",
    CollectionType.搁置: ":material-archive:",
    CollectionType.抛弃: ":material-trash-can:",
}


class Rate(enum.IntEnum):
    未定 = 0
    不忍直视 = 1
    很差 = 2
    差 = 3
    较差 = 4
    不过不失 = 5
    还行 = 6
    推荐 = 7
    力荐 = 8
    神作 = 9
    超神作 = 10

    def __str__(self) -> str:
        return self.name


class UserSubjectCollection(pydantic.BaseModel):
    subject_id: int
    rate: Rate
    type_: CollectionType = pydantic.Field(alias="type")

    class SlimSubject(pydantic.BaseModel):
        id: int
        name: str
        name_cn: str
        date: datetime.date

        class Images(pydantic.BaseModel):
            large: str
            common: str
            medium: str
            small: str
            grid: str

        images: Images
        score: float

    subject: SlimSubject


class PagedUserCollection(pydantic.BaseModel):
    total: int
    limit: int
    offset: int
    data: Sequence[UserSubjectCollection]


@tenacity.retry(
    stop=stop.stop_after_attempt(4), wait=wait.wait_random_exponential(min=1)
)
async def get_user_collection_paged(user: str, offset: int = 0) -> PagedUserCollection:
    async with httpx.AsyncClient(
        headers={"User-Agent": USER_AGENT} if USER_AGENT else None
    ) as client:
        response: httpx.Response = await client.get(
            f"https://api.bgm.tv/v0/users/{user}/collections", params={"offset": offset}
        )
        response.raise_for_status()
        response_body: PagedUserCollection = PagedUserCollection(**response.json())
        return response_body


@tenacity.retry(
    stop=stop.stop_after_attempt(4), wait=wait.wait_random_exponential(min=1)
)
async def get_user_collection(
    user: str,
) -> Sequence[UserSubjectCollection]:
    data: Sequence[UserSubjectCollection] = []
    while True:
        response_body: PagedUserCollection = await get_user_collection_paged(
            user=user, offset=len(data)
        )
        data.extend(response_body.data)
        if len(data) >= response_body.total:
            break
    return data


def main(
    title: Annotated[str, typer.Option()] = "ACG",
    user: Annotated[str, typer.Option()] = "liblaf",
) -> None:
    collections: Sequence[UserSubjectCollection] = asyncio.run(
        get_user_collection(user=user)
    )
    data: MutableMapping[Rate, MutableSequence[UserSubjectCollection]] = defaultdict(
        list
    )
    for collection in collections:
        data[collection.rate].append(collection)
    print(
        f"""\
---
hide:
  - navigation
---
# {title}
!!! note
    本列表仅代表个人观感\
""",
        end="",
    )
    print('   <div class="legends">')
    for type_ in CollectionType:
        print(f'        <div class="{type_}" markdown> {type_.emoji} {type_} </div>')
    print("    </div>")
    for rate, collections in sorted(data.items(), reverse=True):
        collections = sorted(collections, key=lambda x: x.subject.date, reverse=True)
        print(
            f"""\
## {rate} {rate.value}
<div class="cards grid gallery links" markdown>\
"""
        )
        for collection in collections:
            name: str = collection.subject.name_cn or collection.subject.name
            if collection.type_ != CollectionType.看过:
                name = f"{collection.type_.emoji} {name}"
            print(
                f"""\
- <a class="{collection.type_}" href="https://bgm.tv/subject/{collection.subject.id}" title="{collection.type_}">
    <figure>
      <img src="{collection.subject.images.large}" />
      <figcaption>
        <span markdown> {name} </span> <br />
        <small>
          {collection.subject.date} / {collection.subject.score}
        </small>
      </figcaption>
    </figure>
  </a>\
"""  # noqa: E501
            )
        print("</div>")
