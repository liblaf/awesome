import typer

from utils.utils import typer as typer_utils

from .add import main as cmd_add
from .disable import main as cmd_disable
from .enable import main as cmd_enable
from .list import main as cmd_list

app = typer.Typer(name="nginx")


typer_utils.add_command(app=app, command=cmd_add, name="add")
typer_utils.add_command(app=app, command=cmd_disable, name="disable")
typer_utils.add_command(app=app, command=cmd_enable, name="enable")
typer_utils.add_command(app=app, command=cmd_list, name="list")
