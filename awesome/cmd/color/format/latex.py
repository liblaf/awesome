from collections.abc import Iterable
from string import Template

from awesome.cmd.color.utils.color import contrast_ratio, relative_luminance

COLOR_TEMPLATE: Template = Template(
    r"\definecolor{${text}}{RGB}{${r}, ${g}, ${b}} % contrast (white): ${contrast_white}, contrast (black): ${contrast_black}"
)

DOC_TEMPLATE: Template = Template(
    r"""
\RequirePackage{xcolor}

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
            "r": r,
            "g": g,
            "b": b,
            "contrast_black": f"{contrast_black:.2f}",
            "contrast_white": f"{contrast_white:.2f}",
            "text": text,
        }
    ).strip()


def format_palette(
    title: str, description: str, colors: Iterable[tuple[str, int, int, int]]
) -> str:
    return "\n".join(format_color(text, r, g, b) for text, r, g, b in colors).strip()


def format_doc(
    palettes: Iterable[tuple[str, str, Iterable[tuple[str, int, int, int]]]]
) -> str:
    return DOC_TEMPLATE.substitute(
        {
            "palettes": "\n\n".join(
                format_palette(*palette) for palette in palettes
            ).strip()
        }
    ).strip()
