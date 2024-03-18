import datetime
import enum

import httpx
import pydantic
import tenacity

# https://bangumi.github.io/api/
USER_AGENT: str = "liblaf/awesome (https://github.com/liblaf/awesome)"


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


class PagedUserCollection(pydantic.BaseModel):
    total: int
    limit: int
    offset: int
    data: list[UserSubjectCollection]


class Data(pydantic.BaseModel):
    data: list[UserSubjectCollection]


@tenacity.retry(
    stop=tenacity.stop_after_attempt(4), wait=tenacity.wait_random_exponential(min=1)
)
async def get_user_collection_paged(user: str, offset: int = 0) -> PagedUserCollection:
    async with httpx.AsyncClient(
        headers={"User-Agent": USER_AGENT} if USER_AGENT else None
    ) as client:
        response: httpx.Response = await client.get(
            f"https://api.bgm.tv/v0/users/{user}/collections", params={"offset": offset}
        )
        response = response.raise_for_status()
        response_body: PagedUserCollection = PagedUserCollection(**response.json())
        return response_body


async def get_user_collection(user: str) -> list[UserSubjectCollection]:
    data: list[UserSubjectCollection] = []
    while True:
        response_body: PagedUserCollection = await get_user_collection_paged(
            user=user, offset=len(data)
        )
        data.extend(response_body.data)
        if len(data) >= response_body.total:
            break
    return data
