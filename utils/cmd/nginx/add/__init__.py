from pathlib import Path

import typer

from utils.utils.rich.run import run

from ..const import DEFAULT_NGINX_DIR
from ..enable import main as cmd_enable
from .template import NGINX_CONFIG_TEMPLATE


def main(
    domain: str = typer.Argument(...),
    port: int = typer.Option(8000),
    nginx_dir: Path = typer.Option(
        DEFAULT_NGINX_DIR, exists=True, file_okay=False, dir_okay=True
    ),
) -> None:
    config: str = NGINX_CONFIG_TEMPLATE.substitute({"domain": domain, "port": port})
    run(
        args=["sudo", "tee", nginx_dir / "sites-available" / domain],
        input=bytes(config, encoding="utf-8"),
    )
    cmd_enable(domain=domain, nginx_dir=nginx_dir)
    run(args=["sudo", "certbot", "--nginx", "-d", domain])
    run(args=["sudo", "nginx", "-s", "reload"])
