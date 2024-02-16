import datetime
import enum
from collections.abc import Sequence

import pydantic

class Rate(enum.IntEnum):
    未定: int
    不忍直视: int
    很差: int
    差: int
    较差: int
    不过不失: int
    还行: int
    推荐: int
    力荐: int
    神作: int
    超神作: int

class CollectionType(enum.IntEnum):
    想看: int
    看过: int
    在看: int
    搁置: int
    抛弃: int
    @property
    def emoji(self) -> str: ...

class UserSubjectCollection(pydantic.BaseModel):
    subject_id: pydantic.PositiveInt
    rate: Rate
    type_: CollectionType
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

async def get_user_collection(user: str) -> Sequence[UserSubjectCollection]: ...
