import string
import urllib.parse

import urltitle

from .constants import ITEM_TEMPLATE, SECTION_TEMPLATE
from .utils import escape_markdown


def format_item(url: dict) -> str:
    netloc: str = urllib.parse.urlparse(url["url"]).netloc
    if "favicon" not in url:
        url["favicon"] = f"https://proposed-rose-aardwolf.faviconkit.com/{netloc}/128"
    if "title" not in url:
        try:
            reader: urltitle.URLTitleReader = urltitle.URLTitleReader()
            url["title"] = reader.title(url["url"])
        except:
            url["title"] = url["url"]
    template = string.Template(ITEM_TEMPLATE)
    result = template.substitute(
        {
            "favicon": url["favicon"],
            "netloc": netloc,
            "title": escape_markdown(url["title"]),
            "url": url["url"],
        }
    )
    return result


def format_section(name: str, urls: list[dict]) -> str:
    template = string.Template(SECTION_TEMPLATE)
    items = "\n".join([format_item(url) for url in urls])
    result = template.substitute({"name": name, "items": items})
    return result
