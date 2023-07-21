from collections.abc import Iterable
from pathlib import Path
from typing import Annotated, Optional

import click
import typer

from .data import crawler, yaml
from .format.latex import format_doc as format_latex
from .format.markdown import format_doc as format_markdown
from .format.scss import format_doc as format_scss


def main(
    data: Annotated[
        Optional[Path],
        typer.Option(
            "-d",
            "--data",
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
        ),
    ] = None,
    format: Annotated[
        str,
        typer.Option(
            "-f",
            "--format",
            click_type=click.Choice(
                choices=["markdown", "latex", "scss"], case_sensitive=False
            ),
            case_sensitive=False,
        ),
    ] = "markdown",
) -> None:
    palettes: Iterable[tuple[str, str, Iterable[tuple[str, int, int, int]]]]
    if data:
        palettes = yaml.get_palettes()
    else:
        palettes = crawler.get_palettes()
    match format:
        case "markdown":
            print(format_markdown(palettes))
        case "latex":
            print(format_latex(palettes))
        case "scss":
            print(format_scss(palettes))


if __name__ == "__main__":
    typer.run(main)
