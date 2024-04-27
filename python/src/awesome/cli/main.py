import typer

from awesome import log as _log
from awesome.cli import bgm as _bgm
from awesome.cli import item as _item

app = typer.Typer(name="awesome")
app.command(name="item")(_item.main)
app.command(name="bgm")(_bgm.main)


def main() -> None:
    _log.init()
    app()
