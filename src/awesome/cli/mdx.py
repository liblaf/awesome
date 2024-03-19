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

import Repos from "@site/src/components/Repos";
"""
    )
    for collection in collections.keys():
        print(
            f"""
## {collection}

<Repos name="{collection}" />
"""
        )


def main(title: Annotated[str, typer.Argument()]) -> None:
    asyncio.run(_main(title=title))
