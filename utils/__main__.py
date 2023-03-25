import typer

from .hello.__main__ import app as app_hello
from .sort.__main__ import app as app_sort

app = typer.Typer(name="utils.py")
app.add_typer(app_hello)
app.add_typer(app_sort)


if __name__ == "__main__":
    app()
