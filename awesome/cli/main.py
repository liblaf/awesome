import typer

from awesome import log
from awesome.cli import bangumi, mixed

log.init()
app: typer.Typer = typer.Typer(name="awesome")
app.command(name="bangumi")(bangumi.main)
app.command(name="mixed")(mixed.main)
