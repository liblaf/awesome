FRONTMATTER: str = r"""
---
title: Awesome Websites
---
"""


ITEM_TEMPLATE: str = (
    r'| <img src="${favicon}" alt="${netloc}" width="48" /> | [${title}](${url}) |'
)


SECTION_TEMPLATE: str = r"""
## ${name}

| Favicon | Title |
| :-----: | ----- |
${items}
"""
