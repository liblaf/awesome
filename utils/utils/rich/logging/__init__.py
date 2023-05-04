from typing import Any, Optional

import rich
from rich.console import Console
from rich.style import Style


def log(
    *objects: Any, style: Optional[str | Style] = None, prefix: Optional[str] = None
) -> None:
    console: Console = rich.get_console()
    if prefix:
        objects = (f"[reverse] {prefix} [/]", *objects)
    console.log(*objects, style=style)
