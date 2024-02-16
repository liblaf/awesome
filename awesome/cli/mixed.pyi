import pathlib
from typing import Annotated, Any, Sequence

import pydantic

from awesome.api import github as _github
from awesome.api import website as _website

class _CollectionRaw:
    websites: Sequence[str]
    repos: Sequence[str]
    def __init__(self, value: Any) -> None: ...

class _Collection(pydantic.BaseModel):
    websites: Sequence[_website.Website]
    repos: Sequence[_github.Repository]

def main(
    data_file: Annotated[pathlib.Path, None],
    *,
    title: Annotated[str, None] = "GitHub",
    token: Annotated[str | None, None] = None,
) -> None: ...
