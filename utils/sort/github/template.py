import string

import github.Repository

from ...utils import escape_markdown
from .constants import ITEM_TEMPLATE, SECTION_TEMPLATE


def format_item(repo: github.Repository.Repository) -> str:
    template = string.Template(ITEM_TEMPLATE)
    result = template.substitute(
        {
            "description": escape_markdown(repo.description or ""),
            "full_name": repo.full_name,
            "name": repo.name,
            "url": repo.html_url,
        }
    )
    return result


def format_section(name: str, repos: list[github.Repository.Repository]) -> str:
    template = string.Template(SECTION_TEMPLATE)
    items = "\n".join([format_item(repo=repo) for repo in repos])
    result = template.substitute({"name": name, "items": items})
    return result
