import sys
from pathlib import Path
from typing import Optional

import typer
import yaml
from tldextract import tldextract

from utils.const.yaml import DUMP_OPTIONS

from .template import format_article


def main(
    data_filepath: Path = typer.Argument(
        ..., exists=True, file_okay=True, dir_okay=False, readable=True, writable=False
    ),
    in_place: bool = typer.Option(False, "-i", "--in-place"),
    markdown: Optional[Path] = typer.Option(
        None,
        "-m",
        "--markdown",
        exists=False,
        file_okay=True,
        dir_okay=False,
        readable=False,
        writable=True,
    ),
) -> None:
    groups: dict[str, list[dict[str, str]]] = yaml.safe_load(
        stream=data_filepath.read_text()
    )

    for group_name in groups.keys():
        groups[group_name].sort(
            key=lambda website: tldextract.extract(website["url"]).registered_domain
        )

    if in_place:
        with data_filepath.open(mode="w") as stream:
            yaml.safe_dump(data=groups, stream=stream, **DUMP_OPTIONS)
    else:
        yaml.safe_dump(data=groups, stream=sys.stdout, **DUMP_OPTIONS)

    if markdown:
        markdown.write_text(format_article(groups=groups))
