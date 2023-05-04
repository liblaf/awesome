import typer


def main(name: str = typer.Option("world", "-n", "--name")) -> None:
    print(f"Hello, {name}!")
