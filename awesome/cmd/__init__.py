import typer

from awesome.utils import typer as typer_utils

from .color import main as cmd_color
from .github import main as cmd_github
from .website import main as cmd_website

app = typer.Typer(name="awesome")

typer_utils.add_command(app=app, command=cmd_color, name="color")
typer_utils.add_command(app=app, command=cmd_github, name="github")
typer_utils.add_command(app=app, command=cmd_website, name="website")
