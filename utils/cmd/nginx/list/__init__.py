from pathlib import Path

import typer

from utils.utils.rich.run import run

from ..const import DEFAULT_NGINX_DIR


def main(
    nginx_dir: Path = typer.Option(
        DEFAULT_NGINX_DIR,
        "-d",
        "--nginx-dir",
        exists=True,
        file_okay=False,
        dir_okay=True,
    ),
) -> None:
    options: list[str] = ["--classify", "--human-readable", "-l"]
    run(args=["ls", *options, nginx_dir / "sites-available"])
    run(args=["ls", *options, nginx_dir / "sites-enabled"])
