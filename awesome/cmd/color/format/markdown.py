from collections.abc import Iterable
from string import Template

from awesome.cmd.color.utils.color import contrast_ratio, relative_luminance

COLOR_TEMPLATE: Template = Template(
    r"| | `${text}` | `${hex}` | `${contrast_white}` | `${contrast_black}` |"
)

STYLE_TEMPLATE: Template = Template(
    r"""
.${text} tbody tr:nth-child(${i}) {
  background: ${color};
}
"""
)

PALETTE_TEMPLATE: Template = Template(
    r"""
### ${title} (${description})

<style>
  ${styles}
</style>

<div class="${text}" markdown>

| &#8193; | Color | Hex | Contrast (White) | Contrast (Black) |
| :-----: | :---: | :-: | :--------------: | :--------------: |
${colors}

</div>
"""
)

DOC_TEMPLATE: Template = Template(
    r"""
---
title: Awesome Colors
icon: palette
category:
  - Demo
  - Design
tag:
  - Color
  - Palette
  - Style
  - Theme
---

## Color Palettes[^1]

[^1]: [Colors - Ant Design](https://ant.design/docs/spec/colors/)

${palettes}
"""
)


def format_color(text: str, r: int, g: int, b: int) -> str:
    l_black: float = relative_luminance(0, 0, 0)
    l_white: float = relative_luminance(255, 255, 255)
    l: float = relative_luminance(r, g, b)
    contrast_black: float = contrast_ratio(l, l_black)
    contrast_white: float = contrast_ratio(l, l_white)
    return COLOR_TEMPLATE.substitute(
        {
            "contrast_black": f"{contrast_black:.2f}",
            "contrast_white": f"{contrast_white:.2f}",
            "hex": f"#{r:02x}{g:02x}{b:02x}",
            "text": text,
        }
    ).strip()


def format_style(text: str, r: int, g: int, b: int) -> str:
    return STYLE_TEMPLATE.substitute(
        {
            "text": text.split("-")[0],
            "i": int(text.split("-")[1]),
            "color": f"#{r:02x}{g:02x}{b:02x}",
        }
    ).strip()


def format_palette(
    title: str, description: str, colors: Iterable[tuple[str, int, int, int]]
) -> str:
    colors = list(colors)
    return PALETTE_TEMPLATE.substitute(
        {
            "colors": "\n".join(
                format_color(text, r, g, b) for text, r, g, b in colors
            ),
            "description": description,
            "styles": "\n".join(
                format_style(text, r, g, b) for text, r, g, b in colors
            ),
            "text": colors[0][0].split("-")[0],
            "title": title,
        }
    ).strip()


def format_doc(
    palettes: Iterable[tuple[str, str, Iterable[tuple[str, int, int, int]]]]
) -> str:
    return DOC_TEMPLATE.substitute(
        {"palettes": "\n\n".join(format_palette(*palette) for palette in palettes)}
    ).strip()
