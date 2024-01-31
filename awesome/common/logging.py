import logging

from rich import console
from rich import logging as rich_logging


def init(level: int | str = logging.NOTSET) -> None:
    handler: rich_logging.RichHandler = rich_logging.RichHandler(
        level=level, console=console.Console(stderr=True)
    )
    logging.basicConfig(
        format="%(message)s", datefmt="[%X]", handlers=[handler], level=level
    )
