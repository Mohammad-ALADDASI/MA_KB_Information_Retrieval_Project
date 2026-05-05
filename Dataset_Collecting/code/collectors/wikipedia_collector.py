import time
import requests
import wikipediaapi

from config import USER_AGENT
from utils import make_record, is_valid_record


WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"


def search_wikipedia_titles(query: str, limit: int = 10) -> list[str]:
    """
    Use the MediaWiki search API to find candidate page titles.
    This is better than calling wiki.page(query) directly because it can
    return multiple relevant pages for one query phrase.
    """
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srlimit": limit,
        "format": "json",
    }

    headers = {
        "User-Agent": USER_AGENT
    }

    try:
        response = requests.get(
            WIKIPEDIA_API_URL,
            params=params,
            headers=headers,
            timeout=20
        )
        response.raise_for_status()
        data = response.json()

        results = data.get("query", {}).get("search", [])
        return [item["title"] for item in results if "title" in item]

    except Exception as e:
        print(f"[Wikipedia] Search error for query '{query}': {e}")
        return []


def fetch_wikipedia_documents(theme: str, queries: list[str], max_results: int = 4) -> list[dict]:
    """
    Collect Wikipedia articles for a given theme.
    Wikipedia pages are useful for medium/long documents.
    """
    records = []
    seen_urls = set()
    seen_titles = set()

    wiki = wikipediaapi.Wikipedia(
        user_agent=USER_AGENT,
        language="en"
    )

    for query in queries:
        if len(records) >= max_results:
            break

        print(f"[Wikipedia] Theme='{theme}' | Query='{query}'")
        candidate_titles = search_wikipedia_titles(query, limit=8)

        for title in candidate_titles:
            if len(records) >= max_results:
                break

            if title.lower() in seen_titles:
                continue

            try:
                page = wiki.page(title)

                if not page.exists():
                    continue

                text = (page.text or "").strip()
                url = (page.fullurl or "").strip()
                page_title = (page.title or "").strip()

                record = make_record(
                    source="Wikipedia",
                    theme=theme,
                    title=page_title,
                    text=text,
                    url=url,
                )

                if is_valid_record(record, min_words=150, max_words=20000):
                    if record["url"] not in seen_urls:
                        records.append(record)
                        seen_urls.add(record["url"])
                        seen_titles.add(page_title.lower())

                time.sleep(0.5)

            except Exception as e:
                print(f"[Wikipedia] Error on page '{title}': {e}")

    return records