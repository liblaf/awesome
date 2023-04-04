import typing
from pathlib import Path

import github.Repository
import typer
import yaml

from .constants import FRONTMATTER
from .sort import sort_repositories
from .template import format_section

app = typer.Typer(name="github", invoke_without_command=True)


@app.callback()
def main(
    filepath: Path = typer.Argument(None),
    token: typing.Optional[str] = typer.Option(None, "-t", "--token"),
) -> None:
    """
    Examples:
        $ utils.py sort github data/github.yaml > docs/awesome-github.md
    """
    data: dict = yaml.safe_load(stream=filepath.read_text())
    print(FRONTMATTER)
    for key, value in data.items():
        repos: list[github.Repository.Repository] = sort_repositories(
            repositories=value, token=token
        )
        print(format_section(name=key, repos=repos))
