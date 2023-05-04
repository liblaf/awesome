import typer

from utils.utils import typer as typer_utils

from .github import main as cmd_github
from .website import main as cmd_website

app = typer.Typer(name="sort")


typer_utils.add_command(app=app, command=cmd_github, name="github")
typer_utils.add_command(app=app, command=cmd_website, name="website")
