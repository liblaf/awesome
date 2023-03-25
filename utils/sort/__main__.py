import typer

from .github.__main__ import app as app_github
from .yaml.__main__ import app as app_yaml

app = typer.Typer(name="sort")
app.add_typer(app_yaml)
app.add_typer(app_github)


if __name__ == "__main__":
    app()
