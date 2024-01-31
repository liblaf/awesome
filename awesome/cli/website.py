import logging
import pathlib
from collections.abc import Mapping, Sequence
from concurrent import futures
from typing import Annotated
from urllib import parse

import typer
import urltitle
import yaml


class Website:
    favicon: str
    title: str
    url: str

    def __init__(self, url: str) -> None:
        result: parse.SplitResult = parse.urlsplit(url=url)
        self.favicon = f"https://icons.bitwarden.net/{result.netloc}/icon.png"
        self.url = url
        self.title = url
        try:
            reader: urltitle.URLTitleReader = urltitle.URLTitleReader()
            self.title = reader.title(url=url)
            if self.title.startswith("(text/html; charset=utf-8)"):
                self.title = url
        except Exception as e:
            logging.error(e)


def main(
    data_path: Annotated[pathlib.Path, typer.Argument(exists=True, dir_okay=False)],
    *,
    title: Annotated[str, typer.Option()] = "Websites",
) -> None:
    lists: Mapping[str, Sequence[str]] = yaml.safe_load(data_path.read_text())
    with futures.ThreadPoolExecutor(max_workers=8) as executor:
        data: Mapping[str, Sequence[Website]] = {
            category: list(executor.map(Website, urls))
            for category, urls in lists.items()
        }
    print(
        f"""\
---
hide:
  - navigation
---
# {title}\
"""
    )
    for category, websites in data.items():
        print(f"## {category}")
        print('<div class="cards grid favicon links" markdown>')
        for website in websites:
            print(
                f"- [![Favicon]({website.favicon}) " f"{website.title}]({website.url})"
            )
        print("</div>")
