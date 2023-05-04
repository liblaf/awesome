import typer

from utils.utils import typer as typer_utils

from .hello import main as cmd_hello
from .nginx import app as cmd_nginx
from .sort import app as cmd_sort

app = typer.Typer(name="utils")


typer_utils.add_command(app=app, command=cmd_hello, name="hello")
typer_utils.add_command(app=app, command=cmd_nginx, name="nginx")
typer_utils.add_command(app=app, command=cmd_sort, name="sort")
