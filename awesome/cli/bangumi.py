import asyncio
from collections import defaultdict
from typing import TYPE_CHECKING, Annotated

import typer

from awesome.api import bangumi as _bangumi

if TYPE_CHECKING:
    from collections.abc import MutableMapping, MutableSequence, Sequence


def main(
    title: Annotated[str, typer.Option()] = "ACG",
    user: Annotated[str, typer.Option()] = "liblaf",
) -> None:
    collections: Sequence[_bangumi.UserSubjectCollection] = asyncio.run(
        _bangumi.get_user_collection(user=user)
    )
    data: MutableMapping[
        _bangumi.Rate, MutableSequence[_bangumi.UserSubjectCollection]
    ] = defaultdict(list)
    for collection in collections:
        data[collection.rate].append(collection)
    print(
        f"""\
---
hide:
  - navigation
---
# {title}
!!! note
    本列表仅代表个人观感\
""",
        end="",
    )
    print('    <div class="legends">')
    for type_ in _bangumi.CollectionType:
        print(
            f'        <div class="{type_.name}" markdown> {type_.emoji} {type_.name} </div>'  # noqa: E501
        )
    print("    </div>")
    for rate, collections in sorted(data.items(), reverse=True):
        collections_sorted: list[_bangumi.UserSubjectCollection] = sorted(
            collections, key=lambda x: x.subject.date, reverse=True
        )
        print(
            f"""\
## {rate.name} {rate.value}
<div class="cards grid gallery links" markdown>\
"""
        )
        for collection in collections_sorted:
            name: str = collection.subject.name_cn or collection.subject.name
            if collection.type_ != _bangumi.CollectionType.看过:
                name = f"{collection.type_.emoji} {name}"
            print(collection.markdown)
        print("</div>")
