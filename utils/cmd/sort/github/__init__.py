import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Optional

import typer
import yaml
from github import Github
from github.Repository import Repository

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
    token: Optional[str] = typer.Option(None, "--token", "-t", envvar="GITHUB_TOKEN"),
) -> None:
    data: dict[str, list[str]] = yaml.safe_load(stream=data_filepath.read_text())
    groups: dict[str, list[Repository]] = {}
    with ThreadPoolExecutor() as executor:
        gh: Github = Github(token)
        for group_name, repo_names in data.items():
            repos: list[Repository] = list(
                executor.map(lambda repo_name: gh.get_repo(repo_name), repo_names)
            )
            repos.sort(key=lambda repo: repo.stargazers_count, reverse=True)
            data[group_name] = [repo.full_name for repo in repos]
            groups[group_name] = repos

    if in_place:
        with data_filepath.open(mode="w") as stream:
            yaml.safe_dump(data=data, stream=stream, **DUMP_OPTIONS)
    else:
        yaml.safe_dump(data=data, stream=sys.stdout, **DUMP_OPTIONS)

    if markdown:
        markdown.write_text(format_article(groups=groups))
