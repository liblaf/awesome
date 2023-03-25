import tldextract


def sort_urls(urls: list[dict]) -> list[dict]:
    return sorted(urls, key=lambda u: tldextract.extract(u["url"]).registered_domain)
