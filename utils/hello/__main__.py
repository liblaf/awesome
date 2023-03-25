import typer

app = typer.Typer(name="hello", invoke_without_command=True)


@app.callback()
def main(name: str = typer.Argument("world")) -> None:
    print(f"Hello, {name}!")
