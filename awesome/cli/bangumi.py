import asyncio
from collections import defaultdict
from collections.abc import MutableMapping, MutableSequence, Sequence
from typing import Annotated

import typer

from awesome.api import bangumi


def main(
    title: Annotated[str, typer.Option()] = "ACG",
    user: Annotated[str, typer.Option()] = "liblaf",
) -> None:
    collections: Sequence[bangumi.UserSubjectCollection] = asyncio.run(
        bangumi.get_user_collection(user=user)
    )
    data: MutableMapping[
        bangumi.Rate, MutableSequence[bangumi.UserSubjectCollection]
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
    for type_ in bangumi.CollectionType:
        print(
            f'        <div class="{type_.name}" markdown> {type_.emoji} {type_.name} </div>'  # noqa: E501
        )
    print("    </div>")
    for rate, collections in sorted(data.items(), reverse=True):
        collections = sorted(collections, key=lambda x: x.subject.date, reverse=True)
        print(
            f"""\
## {rate.name} {rate.value}
<div class="cards grid gallery links" markdown>\
"""
        )
        for collection in collections:
            name: str = collection.subject.name_cn or collection.subject.name
            if collection.type_ != bangumi.CollectionType.看过:
                name = f"{collection.type_.emoji} {name}"
            print(
                f"""\
- <a class="{collection.type_.name}" href="https://bgm.tv/subject/{collection.subject.id}" title="{collection.type_.name}">
    <figure>
      <img src="{collection.subject.images.large}" />
      <figcaption>
        <span markdown> {name} </span> <br />
        <small>
          {collection.subject.date} / {collection.subject.score}
        </small>
      </figcaption>
    </figure>
  </a>\
"""  # noqa: E501
            )
        print("</div>")
