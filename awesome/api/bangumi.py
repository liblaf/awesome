import datetime
import enum
from collections.abc import Mapping, Sequence
from typing import LiteralString

import httpx
import pydantic
import tenacity
from tenacity import stop, wait

# https://bangumi.github.io/api/
_USER_AGENT: str = "liblaf/awesome (https://github.com/liblaf/awesome)"


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


class CollectionType(enum.IntEnum):
    想看 = 1
    看过 = 2
    在看 = 3
    搁置 = 4
    抛弃 = 5

    @property
    def emoji(self) -> str:
        return _COLLECTIONS[self]


_COLLECTIONS: Mapping[CollectionType, LiteralString] = {
    CollectionType.想看: ":star:",
    CollectionType.看过: ":thumbsup:",
    CollectionType.在看: ":material-play:",
    CollectionType.搁置: ":material-archive:",
    CollectionType.抛弃: ":material-trash-can:",
}


class UserSubjectCollection(pydantic.BaseModel):
    subject_id: pydantic.PositiveInt
    rate: Rate
    type_: CollectionType = pydantic.Field(alias="type")

    class SlimSubject(pydantic.BaseModel):
        id: pydantic.PositiveInt
        name: str
        name_cn: str
        date: datetime.date

        class Images(pydantic.BaseModel):
            large: pydantic.HttpUrl
            common: pydantic.HttpUrl
            medium: pydantic.HttpUrl
            small: pydantic.HttpUrl
            grid: pydantic.HttpUrl

        images: Images
        score: pydantic.PositiveFloat

    subject: SlimSubject


class _PagedUserCollection(pydantic.BaseModel):
    total: int
    limit: int
    offset: int
    data: Sequence[UserSubjectCollection]


@tenacity.retry(
    stop=stop.stop_after_attempt(4), wait=wait.wait_random_exponential(min=1)
)
async def _get_user_collection_paged(
    user: str, offset: int = 0
) -> _PagedUserCollection:
    async with httpx.AsyncClient(
        headers={"User-Agent": _USER_AGENT} if _USER_AGENT else None
    ) as client:
        response: httpx.Response = await client.get(
            f"https://api.bgm.tv/v0/users/{user}/collections", params={"offset": offset}
        )
        response = response.raise_for_status()
        response_body: _PagedUserCollection = _PagedUserCollection(**response.json())
        return response_body


@tenacity.retry(
    stop=stop.stop_after_attempt(4), wait=wait.wait_random_exponential(min=1)
)
async def get_user_collection(
    user: str,
) -> Sequence[UserSubjectCollection]:
    data: Sequence[UserSubjectCollection] = []
    while True:
        response_body: _PagedUserCollection = await _get_user_collection_paged(
            user=user, offset=len(data)
        )
        data.extend(response_body.data)
        if len(data) >= response_body.total:
            break
    return data
