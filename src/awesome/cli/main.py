import typer

from awesome import log as _log
from awesome.cli import bgm as _bgm
from awesome.cli import mdx as _mdx
from awesome.cli import mixed as _mixed

app = typer.Typer(name="awesome")
app.command("bgm")(_bgm.main)
app.command("mdx")(_mdx.main)
app.command("mixed")(_mixed.main)


def main() -> None:
    _log.init()
    app()


if __name__ == "__main__":
    main()
