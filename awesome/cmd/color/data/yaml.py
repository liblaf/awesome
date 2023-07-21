from collections.abc import Iterable
from pathlib import Path
from typing import Any

import yaml


def hex_to_rgb(hex: int) -> tuple[int, int, int]:
    return hex // 65536, (hex // 256) % 256, hex % 256


def get_colors(color: str, hexes: Iterable[int]) -> Iterable[tuple[str, int, int, int]]:
    for i, hex in enumerate(hexes):
        yield f"{color}-{i + 1}", *hex_to_rgb(hex)


def get_palette(
    color: str, data: dict[str, Any]
) -> tuple[str, str, Iterable[tuple[str, int, int, int]]]:
    name: str = data["name"]
    description: str = data["description"]
    return name, description, get_colors(color, data["hex"])


def get_palettes(
    filepath: Path = Path.cwd() / "data" / "colors.yaml",
) -> Iterable[tuple[str, str, Iterable[tuple[str, int, int, int]]]]:
    data: dict[str, Any] = yaml.safe_load(filepath.read_text())
    for key, value in data.items():
        yield get_palette(key, value)
