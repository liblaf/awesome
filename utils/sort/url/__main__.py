from pathlib import Path

import typer
import yaml

from .constants import FRONTMATTER
from .sort import sort_urls
from .template import format_section

app = typer.Typer(name="url", invoke_without_command=True)


@app.callback()
def main(filepath: Path = typer.Argument(None)) -> None:
    """
    Examples:
        $ utils.py sort github data/github.yaml > docs/awesome-github.md
    """
    data: dict = yaml.safe_load(stream=filepath.read_text())
    print(FRONTMATTER)
    for key, value in data.items():
        urls: list[dict] = sort_urls(urls=value)
        print(format_section(name=key, urls=urls))
