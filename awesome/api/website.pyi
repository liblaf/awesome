from collections.abc import Iterable, Sequence

import pydantic
from _typeshed import Incomplete

ua: Incomplete

class Website(pydantic.BaseModel):
    url: pydantic.HttpUrl
    favicon: pydantic.HttpUrl
    title: str
    @property
    def markdown(self) -> str: ...

async def get_website(url: str) -> Website: ...
async def get_websites(urls: Iterable[str]) -> Sequence[Website]: ...
