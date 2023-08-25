from string import Template

from github.Repository import Repository

FRONTMATTER: str = r"""
---
title: Awesome GitHub
---
"""

ITEM_TEMPLATE: Template = Template(
    r"| [${name}](${url}) | ![GitHub Repo Stars](https://img.shields.io/github/stars/${full_name}) ![GitHub Commit Activity](https://img.shields.io/github/commit-activity/y/${full_name}) | ${description} |"
)

SECTION_TEMPLATE: Template = Template(
    r"""
## ${name}

| Name | Statistics | Description |
| ---- | ---------- | ----------- |
${items}
"""
)


def format_item(repo: Repository) -> str:
    return ITEM_TEMPLATE.substitute(
        {
            "description": repo.description or "",
            "full_name": repo.full_name,
            "name": repo.name,
            "url": repo.html_url,
        }
    )


def format_section(name: str, repos: list[Repository]) -> str:
    items: str = "\n".join(map(format_item, repos))
    return SECTION_TEMPLATE.substitute({"name": name, "items": items})


def format_article(groups: dict[str, list[Repository]]) -> str:
    sections: list[str] = [
        format_section(name, groups[name]) for name in sorted(groups.keys())
    ]
    return "\n".join([FRONTMATTER, "\n".join(sections)])
