import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Annotated, Optional

import typer
import yaml
from github import Github
from github.Repository import Repository

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
    in_place: Annotated[bool, typer.Option("-i", "--in-place")] = False,
    markdown: Annotated[
        Optional[Path],
        typer.Option(
            "-m",
            "--markdown",
            exists=False,
            file_okay=True,
            dir_okay=False,
            readable=False,
            writable=True,
        ),
    ] = None,
    token: Annotated[
        Optional[str], typer.Option("-t", "--token", envvar="GITHUB_TOKEN")
    ] = None,
) -> None:
    raw: dict[str, list[str]] = yaml.safe_load(stream=data.read_text())
    groups: dict[str, list[Repository]] = {}
    with ThreadPoolExecutor() as executor:
        gh: Github = Github(token)
        for group_name, repo_names in raw.items():
            repos: list[Repository] = list(
                executor.map(lambda repo_name: gh.get_repo(repo_name), repo_names)
            )
            repos.sort(key=lambda repo: repo.stargazers_count, reverse=True)
            raw[group_name] = [repo.full_name for repo in repos]
            groups[group_name] = repos

    if in_place:
        with data.open(mode="w") as stream:
            yaml.safe_dump(data=raw, stream=stream, **DUMP_OPTIONS)
    else:
        yaml.safe_dump(data=raw, stream=sys.stdout, **DUMP_OPTIONS)

    if markdown:
        markdown.write_text(format_article(groups=groups))
