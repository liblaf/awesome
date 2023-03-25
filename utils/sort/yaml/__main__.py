from pathlib import Path

import typer
import yaml

from .. import sort

app = typer.Typer(name="yaml", invoke_without_command=True)


@app.callback()
def main(filepath: Path) -> None:
    data = yaml.load(filepath.read_text(), Loader=yaml.CLoader)
    data = sort(data)
    filepath.write_text(yaml.dump(data))


if __name__ == "__main__":
    app()
