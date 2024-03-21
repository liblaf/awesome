import asyncio
import sys
from typing import Annotated

import typer
import yaml


async def _main(title: str) -> None:
    collections: dict[str, list[str]] = yaml.safe_load(sys.stdin)
    print(
        f"""\
---
title: {title}
---

import AwesomeList from "@site/src/components/AwesomeList";
"""
    )
    for collection in collections.keys():
        print(
            f"""
## {collection}

<AwesomeList name="{collection}" />
"""
        )


def main(title: Annotated[str, typer.Argument()]) -> None:
    asyncio.run(_main(title=title))
