from collections.abc import Iterable
from enum import StrEnum
from pathlib import Path
from typing import Annotated, Optional

import typer

from .data import crawler, yaml
from .format.latex import format_doc as format_latex
from .format.markdown import format_doc as format_markdown
from .format.scss import format_doc as format_scss


class Format(StrEnum):
    LATEX = "latex"
    MARKDOWN = "markdown"
    SCSS = "scss"


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
        Format,
        typer.Option(
            "-f",
            "--format",
            case_sensitive=False,
        ),
    ] = Format.MARKDOWN,
) -> None:
    palettes: Iterable[tuple[str, str, Iterable[tuple[str, int, int, int]]]]
    if data:
        palettes = yaml.get_palettes()
    else:
        palettes = crawler.get_palettes()
    match format:
        case Format.LATEX:
            print(format_latex(palettes))
        case Format.MARKDOWN:
            print(format_markdown(palettes))
        case Format.SCSS:
            print(format_scss(palettes))


if __name__ == "__main__":
    typer.run(main)
