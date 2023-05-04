from pathlib import Path

import typer

from utils.utils.rich.run import run

from ..const import DEFAULT_NGINX_DIR


def main(
    domain: str = typer.Argument(...),
    nginx_dir: Path = typer.Option(
        DEFAULT_NGINX_DIR,
        "-d",
        "--nginx-dir",
        exists=True,
        file_okay=False,
        dir_okay=True,
    ),
) -> None:
    options: list[str] = ["--interactive", "--verbose"]
    args: list[str | Path] = [
        "sudo",
        "rm",
        *options,
        nginx_dir / "sites-enabled" / domain,
    ]
    run(args=args)
