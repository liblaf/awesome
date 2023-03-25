import string

import github.Repository

from .constants import ITEM_TEMPLATE, SECTION_TEMPLATE


def format_item(repo: github.Repository.Repository) -> str:
    template = string.Template(ITEM_TEMPLATE)
    result = template.substitute(
        {
            "description": repo.description,
            "full_name": repo.full_name,
            "name": repo.name,
            "url": repo.url,
        }
    )
    return result


def format_section(name: str, repos: list[github.Repository.Repository]) -> str:
    template = string.Template(SECTION_TEMPLATE)
    items = "\n".join([format_item(repo=repo) for repo in repos])
    name = name.replace("-", " ").title()
    result = template.substitute({"name": name, "repos": items})
    return result
