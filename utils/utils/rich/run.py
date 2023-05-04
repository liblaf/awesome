import shlex
import subprocess
from pathlib import Path
from typing import Optional, Sequence

from .logging import log, style


def run(args: Sequence[str | Path], input: Optional[bytes] = None) -> None:
    command: str = shlex.join(map(str, args))
    log(command, style=style.INFO, prefix="RUN")
    completed: subprocess.CompletedProcess = subprocess.run(args=args, input=input)
    if completed.returncode != 0:
        log(command, style=style.FAIL, prefix=f"FAIL {completed.returncode}")
        completed.check_returncode()
    log(command, style=style.SUCCESS, prefix="SUCCESS")
