import asyncio
from collections.abc import Iterable, Sequence
from urllib import parse
from venv import logger

import bs4
import fake_useragent  # type: ignore
import httpx
import pydantic
import tenacity

ua = fake_useragent.UserAgent()


class Website(pydantic.BaseModel):
    url: pydantic.HttpUrl
    favicon: pydantic.HttpUrl
    title: str

    @property
    def markdown(self) -> str:
        return f"- [![Favicon]({self.favicon}) {self.title}]({self.url})"


def _favicon(url: str) -> str:
    result: parse.ParseResult = parse.urlparse(url)
    return f"https://icons.bitwarden.net/{result.netloc}/icon.png"


@tenacity.retry(
    stop=tenacity.stop_after_attempt(4), wait=tenacity.wait_random_exponential(min=1)
)
async def _title(url: str) -> str:
    try:
        async with httpx.AsyncClient(
            headers={
                "User-Agent": ua.random  # type: ignore
            },
            follow_redirects=True,
        ) as client:
            response: httpx.Response = await client.get(url)
            response = response.raise_for_status()
            soup: bs4.BeautifulSoup = bs4.BeautifulSoup(response.text, "html.parser")
            tag: bs4.Tag | bs4.NavigableString | None = soup.find(name="title")
            if not tag:
                return url
            return tag.get_text(strip=True)
    except Exception as e:
        logger.error(e)
        return url


async def get_website(url: str) -> Website:
    return Website(
        url=url,  # type: ignore
        favicon=_favicon(url),  # type: ignore
        title=await _title(url),
    )


async def get_websites(urls: Iterable[str]) -> Sequence[Website]:
    return await asyncio.gather(*[get_website(url) for url in urls])
