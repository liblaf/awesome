import asyncio
import json
import sys

from awesome import log as _log
from awesome.api import item as _item


async def async_main() -> None:
    items: list[_item.Item] = []
    for line in sys.stdin:
        line: str = line.strip()
        if not line:
            continue
        item = _item.Item(**json.loads(line))
        items.append(item)
    data: _item.Data = await _item.fetch_items(items)
    print(data.model_dump_json())


def main() -> None:
    _log.init()
    asyncio.run(async_main())
