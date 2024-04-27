import asyncio
from typing import Annotated

import typer

from awesome.api import bgm as _bgm


async def async_main(user: str) -> None:
    collections: list[_bgm.UserSubjectCollection] = await _bgm.fetch_user_collection(
        user
    )
    data = _bgm.Data(data=collections)
    print(data.model_dump_json(by_alias=True))


def main(user: Annotated[str, typer.Argument()] = "liblaf") -> None:
    asyncio.run(async_main(user))
