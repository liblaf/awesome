FRONTMATTER: str = r"""
---
title: Awesome GitHub
category:
  - Awesome
tag:
  - GitHub
---
"""


ITEM_TEMPLATE: str = r"| [${name}](${url}) | ![GitHub Repo stars](https://img.shields.io/github/stars/${full_name}) ![GitHub commit activity](https://img.shields.io/github/commit-activity/y/${full_name}) | ${description} |"


SECTION_TEMPLATE: str = r"""
## ${name}

| Name | Statistics | Description |
| ---- | ---------- | ----------- |
${items}
"""
