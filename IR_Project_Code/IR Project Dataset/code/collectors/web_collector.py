import time
from typing import Iterable
from urllib.parse import urlparse

import requests
import trafilatura
from bs4 import BeautifulSoup

from utils import make_record, is_valid_record


DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}


def extract_title_from_html(html: str) -> str:
    try:
        soup = BeautifulSoup(html, "html.parser")
        if soup.title and soup.title.string:
            return soup.title.string.strip()
    except Exception:
        pass
    return ""


def fetch_page_with_requests(url: str, timeout: int = 20) -> tuple[str, str]:
    """
    Fetch raw HTML with requests and extract a fallback title.
    Returns (title, html).
    """
    response = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
    response.raise_for_status()
    response.encoding = response.apparent_encoding

    html = response.text
    title = extract_title_from_html(html)
    return title, html


def extract_main_text_from_html(html: str, url: str | None = None) -> str:
    """
    Use trafilatura for main-content extraction.
    """
    text = trafilatura.extract(
        html,
        url=url,
        include_comments=False,
        include_tables=False,
        favor_precision=True,
        deduplicate=True,
    )
    return (text or "").strip()


def fetch_web_document(url: str) -> dict | None:
    """
    Fetch one webpage and turn it into a normalized corpus record candidate.
    Theme is assigned by the caller.
    """
    try:
        title, html = fetch_page_with_requests(url)
        text = extract_main_text_from_html(html, url=url)

        if not text:
            return None

        return {
            "title": title or urlparse(url).path.strip("/") or "Untitled Web Document",
            "text": text,
            "url": url,
        }

    except Exception as e:
        print(f"[Web] Error fetching '{url}': {e}")
        return None


def fetch_web_documents(theme: str, urls: Iterable[str], max_results: int = 8) -> list[dict]:
    """
    Collect web articles from a curated URL list.
    One URL = one document.
    """
    records = []
    seen_urls = set()

    for url in urls:
        if len(records) >= max_results:
            break

        normalized_url = url.strip()
        if not normalized_url or normalized_url in seen_urls:
            continue

        print(f"[Web] Theme='{theme}' | URL='{normalized_url}'")

        page = fetch_web_document(normalized_url)
        if not page:
            continue

        record = make_record(
            source="WebArticle",
            theme=theme,
            title=page["title"],
            text=page["text"],
            url=page["url"],
        )

        if is_valid_record(record, min_words=120, max_words=30000):
            records.append(record)
            seen_urls.add(normalized_url)

        time.sleep(0.8)

    return records