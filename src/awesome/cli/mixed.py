import asyncio
import sys

import yaml

from awesome.api import mixed as _mixed


async def _main() -> None:
    collections_input: dict[str, list[str]] = yaml.safe_load(sys.stdin)
    collections: dict[str, _mixed.Collection] = await _mixed.get_collections(
        collections_input
    )
    data = _mixed.Data(data=collections)
    print(data.model_dump_json(by_alias=True))


def main() -> None:
    asyncio.run(_main())
