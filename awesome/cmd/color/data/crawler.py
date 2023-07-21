import re
from collections.abc import Iterable
from pathlib import Path
from typing import Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.remote.webelement import WebElement

RGBA_PATTERN: str = r"rgba\((?P<r>\d+), (?P<g>\d+), (?P<b>\d+), (?P<a>\d+)\)"


def get_color(color_item: WebElement) -> tuple[str, int, int, int]:
    text: str = color_item.find_element(
        by=By.CLASS_NAME, value="main-color-text"
    ).text.strip()
    value: str = color_item.value_of_css_property("background-color").strip()
    match_results: Optional[re.Match] = re.match(pattern=RGBA_PATTERN, string=value)
    assert match_results
    r, g, b = match_results.group("r", "g", "b")
    return text, int(r), int(g), int(b)


def get_colors(
    color_items: Iterable[WebElement],
) -> Iterable[tuple[str, int, int, int]]:
    yield from map(get_color, color_items)


def get_palette(
    color_palette: WebElement,
) -> tuple[str, str, Iterable[tuple[str, int, int, int]]]:
    title: str = color_palette.find_element(
        by=By.CLASS_NAME, value="color-title"
    ).text.strip()
    description: str = color_palette.find_element(
        by=By.CLASS_NAME, value="color-description"
    ).text.strip()
    title = title.removesuffix(description).strip()
    color_items: list[WebElement] = color_palette.find_elements(
        by=By.CLASS_NAME, value="main-color-item"
    )
    return title, description, get_colors(color_items)


def get_palettes(
    binary_location: Path = Path("/usr/bin/microsoft-edge-stable"),
    executable_path: Path = Path.cwd() / "bin" / "msedgedriver",
) -> Iterable[tuple[str, str, Iterable[tuple[str, int, int, int]]]]:
    options: Options = Options()
    options.binary_location = str(binary_location)
    options.headless = True
    service: Service = Service(executable_path=str(executable_path))
    with webdriver.Edge(options=options, service=service) as driver:
        driver.get(url="https://ant.design/docs/spec/colors/")
        color_palettes: list[WebElement] = driver.find_elements(
            by=By.CLASS_NAME, value="color-palette"
        )
        yield from map(get_palette, color_palettes)
