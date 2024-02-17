import asyncio
from collections.abc import Iterable, Sequence
from urllib import parse
from venv import logger

import bs4
import fake_useragent  # type: ignore
import httpx
import pydantic
import typeguard

ua = fake_useragent.UserAgent()


class Website(pydantic.BaseModel):
    url: pydantic.HttpUrl
    title: str | None = None
    image: pydantic.HttpUrl | None = None
    description: str | None = None

    @property
    def favicon(self) -> str:
        result: parse.ParseResult = parse.urlparse(str(self.url))
        return f"https://icons.bitwarden.net/{result.netloc}/icon.png"

    @property
    def markdown(self) -> str:
        result: str = f'<li><a href="{self.url}" markdown>'
        result += f'<img alt="Favicon" class="favicon" src="{self.favicon}" />'
        if self.title:
            result += self.title
        else:
            result += str(self.url)
        if self.image:
            result += f'<img class="og" src="{self.image}" />'
        if self.description:
            if not self.image:
                result += "<hr/>"
            result += f"<p>{self.description}</p>"
        result += "</a></li>"
        return result


@typeguard.typechecked()
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


@typeguard.typechecked()
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


@typeguard.typechecked()
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


@typeguard.typechecked()
async def get_website(url: str) -> Website:
    try:
        async with httpx.AsyncClient(
            headers={"User-Agent": ua.random},  # pyright: ignore
            follow_redirects=True,
        ) as client:
            response: httpx.Response = await client.get(url)
            response = response.raise_for_status()
            soup: bs4.BeautifulSoup = bs4.BeautifulSoup(response.text)
            image: str | None = _get_image(soup)
            if image and not image.startswith("http"):
                image = parse.urljoin(url, image)
            return Website(
                url=url,
                title=_get_title(soup),
                image=image,
                description=_get_description(soup),
            )
    except Exception as e:
        logger.error(e)
        return Website(url=url)


async def get_websites(urls: Iterable[str]) -> Sequence[Website]:
    return await asyncio.gather(*[get_website(url) for url in urls])
