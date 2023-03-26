import json
from pathlib import Path

import typer

from .. import sort

app = typer.Typer(name="json", invoke_without_command=True)


@app.callback()
def main(filepath: Path) -> None:
    data = json.loads(filepath.read_text())
    data = sort(data)
    filepath.write_text(json.dumps(data, sort_keys=True))


if __name__ == "__main__":
    app()
