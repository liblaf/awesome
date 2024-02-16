from collections.abc import Iterable, Sequence

import pydantic

class Website(pydantic.BaseModel):
    url: pydantic.HttpUrl
    favicon: pydantic.HttpUrl
    title: str
    @property
    def markdown(self) -> str: ...

async def get_websites(urls: Iterable[str]) -> Sequence[Website]: ...
