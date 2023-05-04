import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from string import Template

import urltitle
import urltitle.config

from utils.utils import markdown as markdown_utils

FAVICON_KIT_API: str = "https://proposed-rose-aardwolf.faviconkit.com"
FAVICON_SIZE: int = 256


FRONTMATTER: str = r"""
---
title: Awesome Websites
category:
  - Awesome
tag:
  - Website
---
"""


ITEM_TEMPLATE: Template = Template(
    r'| <img src="${favicon}" alt="${netloc}" width="32" /> | [${title}](${url}) |'
)

SECTION_TEMPLATE: Template = Template(
    r"""
## ${name}

| Favicon | Title |
| :-----: | ----- |
${items}
"""
)


def format_item(website: dict[str, str]) -> str:
    url = website["url"]

    netloc: str = urllib.parse.urlparse(url=url).netloc
    website["netloc"] = netloc

    if "favicon" not in website:
        website["favicon"] = f"{FAVICON_KIT_API}/{netloc}/{FAVICON_SIZE}"

    if "title" not in website:
        reader: urltitle.URLTitleReader = urltitle.URLTitleReader()
        title: str = reader.title(url)
        website["title"] = title

    return ITEM_TEMPLATE.substitute(
        {
            "favicon": website["favicon"],
            "netloc": website["netloc"],
            "title": markdown_utils.escape(website["title"]),
            "url": website["url"],
        }
    )


def format_section(name: str, websites: list[dict[str, str]]) -> str:
    with ThreadPoolExecutor() as executor:
        items: str = "\n".join(executor.map(format_item, websites))
    return SECTION_TEMPLATE.substitute({"name": name, "items": items})


def format_article(groups: dict[str, list[dict[str, str]]]) -> str:
    sections: list[str] = [
        format_section(name, groups[name]) for name in sorted(groups.keys())
    ]
    return "\n".join([FRONTMATTER, "\n".join(sections)])
