import os
import pathlib
from collections.abc import Mapping, Sequence
from concurrent import futures
from typing import Annotated
from urllib import parse

import loguru
import pandas as pd
import slugify
import typer
import urltitle
import yaml


class Website:
    favicon: str
    title: str
    url: str

    def __init__(self, url: str) -> None:
        result: parse.SplitResult = parse.urlsplit(url=url)
        self.favicon = (
            f"https://melodic-scarlet-wolverine.faviconkit.com/{result.netloc}/256"
        )
        self.url = url
        self.title = url
        try:
            reader: urltitle.URLTitleReader = urltitle.URLTitleReader()
            self.title = reader.title(url=url)
        except Exception as e:
            loguru.logger.error(e)


def main(
    data_path: Annotated[pathlib.Path, typer.Argument(exists=True, dir_okay=False)],
    output_dir: Annotated[pathlib.Path, typer.Argument(exists=False, file_okay=False)],
    *,
    title: Annotated[str, typer.Option()] = "Websites",
) -> None:
    lists: Mapping[str, Sequence[str]] = yaml.safe_load(data_path.read_text())
    with futures.ThreadPoolExecutor(max_workers=8) as executor:
        data: Mapping[str, Sequence[Website]] = {
            category: list(executor.map(Website, urls))
            for category, urls in lists.items()
        }
    os.makedirs(output_dir, exist_ok=True)
    print(f"# {title}")
    for category, websites in data.items():
        data_frame: pd.DataFrame = pd.DataFrame.from_records(
            data=[
                (
                    f"[![Favicon]({website.favicon})]({website.url})",
                    f"[{website.title}]({website.url})",
                )
                for website in websites
            ],
            columns=["Favicon", "Title"],
        )
        output_path: pathlib.Path = output_dir / f"{slugify.slugify(category)}.csv"
        data_frame.to_csv(output_path, index=False)
        print(
            f"""
## {category}

{{{{ read_csv("{output_path}", intfmt=",") }}}}"""
        )
