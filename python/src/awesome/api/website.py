import asyncio
from collections.abc import Iterable
from urllib import parse

import bs4
import fake_useragent
import httpx
import pydantic
from loguru import logger

UA = fake_useragent.UserAgent()


class Website(pydantic.BaseModel):
    url: pydantic.HttpUrl
    title: str | None = None
    image: pydantic.HttpUrl | None = None
    description: str | None = None

    @pydantic.computed_field
    @property
    def favicon(self) -> str:
        result: parse.ParseResult = parse.urlparse(str(self.url))
        return f"https://icons.bitwarden.net/{result.netloc}/icon.png"


def _get_title(soup: bs4.BeautifulSoup) -> str | None:
    tag: bs4.Tag | bs4.NavigableString | None = soup.find(name="title")
    if tag:
        return tag.get_text(strip=True)
    tag = soup.find(name="meta", property="og:title")
    if isinstance(tag, bs4.Tag) and isinstance(content := tag.get("content"), str):
        return content
    tag = soup.find(name="meta", attrs={"name": "twitter:title"})
    if isinstance(tag, bs4.Tag) and isinstance(content := tag.get("content"), str):
        return content
    return None


def _get_image(soup: bs4.BeautifulSoup) -> str | None:
    tag: bs4.Tag | bs4.NavigableString | None = soup.find(
        name="meta", property="og:image"
    )
    if (
        isinstance(tag, bs4.Tag)
        and isinstance(content := tag.get("content"), str)
        and content
    ):
        return content
    tag = soup.find(name="meta", attrs={"name": "twitter:image"})
    if (
        isinstance(tag, bs4.Tag)
        and isinstance(content := tag.get("content"), str)
        and content
    ):
        return content
    return None


def _get_description(soup: bs4.BeautifulSoup) -> str | None:
    tag: bs4.Tag | bs4.NavigableString | None = soup.find(
        name="meta", property="og:description"
    )
    if (
        isinstance(tag, bs4.Tag)
        and isinstance(content := tag.get("content"), str)
        and content
    ):
        return content
    tag = soup.find(name="meta", attrs={"name": "twitter:description"})
    if (
        isinstance(tag, bs4.Tag)
        and isinstance(content := tag.get("content"), str)
        and content
    ):
        return content
    return None


async def fetch_website(client: httpx.AsyncClient, url: str) -> Website:
    try:
        response: httpx.Response = await client.get(url)
        response = response.raise_for_status()
        soup: bs4.BeautifulSoup = bs4.BeautifulSoup(
            response.text, features="html.parser"
        )
        image: str | None = _get_image(soup)
        if image and not image.startswith("http"):
            image = parse.urljoin(url, image)
        if image:
            response = await client.get(image)
            if not response.is_success:
                image = None
        return Website(
            url=url,  # pyright: ignore
            title=_get_title(soup),
            image=image,  # pyright: ignore
            description=_get_description(soup),
        )
    except Exception as e:
        logger.error(e)
        return Website(url=url)  # pyright: ignore


async def fetch_website_list(urls: Iterable[str]) -> list[Website]:
    async with httpx.AsyncClient(
        headers={"User-Agent": UA.chrome},  # pyright: ignore
        follow_redirects=True,
    ) as client:
        return await asyncio.gather(*[fetch_website(client, url) for url in urls])
