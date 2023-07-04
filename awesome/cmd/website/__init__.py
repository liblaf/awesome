import sys
from pathlib import Path
from typing import Annotated, Optional

import typer
import yaml
from tldextract import tldextract

from awesome.const.yaml import DUMP_OPTIONS

from .template import format_article


def main(
    data: Annotated[
        Path,
        typer.Argument(
            ...,
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            writable=False,
        ),
    ],
    in_place: Annotated[bool, typer.Option("--in-place", "-i")] = False,
    markdown: Annotated[
        Optional[Path],
        typer.Option(
            "--markdown",
            "-m",
            exists=False,
            file_okay=True,
            dir_okay=False,
            readable=False,
            writable=True,
        ),
    ] = None,
) -> None:
    groups: dict[str, list[dict[str, str]]] = yaml.safe_load(stream=data.read_text())

    for group_name in groups.keys():
        groups[group_name].sort(
            key=lambda website: tldextract.extract(website["url"]).registered_domain
        )

    if in_place:
        with data.open(mode="w") as stream:
            yaml.safe_dump(data=groups, stream=stream, **DUMP_OPTIONS)
    else:
        yaml.safe_dump(data=groups, stream=sys.stdout, **DUMP_OPTIONS)

    if markdown:
        markdown.write_text(format_article(groups=groups))
