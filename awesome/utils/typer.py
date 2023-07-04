from typing import Callable, Optional

import typer


def add_command(
    app: typer.Typer, command: Callable, name: Optional[str] = None
) -> None:
    if isinstance(command, typer.Typer):
        app.add_typer(command, name=name)
    else:
        app.command(name=name)(command)
