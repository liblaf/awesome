import typer

from .github.__main__ import app as app_github
from .json.__main__ import app as app_json
from .url.__main__ import app as app_url
from .yaml.__main__ import app as app_yaml

app = typer.Typer(name="sort")
app.add_typer(app_github)
app.add_typer(app_json)
app.add_typer(app_url)
app.add_typer(app_yaml)


if __name__ == "__main__":
    app()
