from typing import Annotated

from awesome.api import bangumi as bangumi

def main(
    title: Annotated[str, None] = "ACG", user: Annotated[str, None] = "liblaf"
) -> None: ...
