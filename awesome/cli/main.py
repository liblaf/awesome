import os

import typer

import awesome.common.logging as my_logging
from awesome.cli import bangumi, github, website

app: typer.Typer = typer.Typer(name="awesome")
app.command(name="bangumi")(bangumi.main)
app.command(name="github")(github.main)
app.command(name="website")(website.main)
my_logging.init(level=os.getenv("LOG_LEVEL", "INFO"))
