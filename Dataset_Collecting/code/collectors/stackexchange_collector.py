import re
import time
from stackapi import StackAPI

from utils import make_record, is_valid_record, clean_text


TAG_KEYWORDS = {
    "Green Computing": ["energy", "performance", "optimization", "power-management"],
    "Environmental Monitoring Systems": ["iot", "sensors", "arduino", "raspberry-pi"],
    "History of the Internet and Web": ["internet", "http", "web", "networking"],
    "Open Source and Software Evolution": ["git", "github", "open-source", "version-control"],
    "AI Bias and Fairness": ["machine-learning", "ai", "nlp", "data-science"],
    "AI Governance and Responsible AI": ["ai", "machine-learning", "ethics", "governance"],
    "Digital Preservation Systems": ["metadata", "database", "archiving", "xml"],
    "Palestinian Digital Heritage": ["ocr", "nlp", "unicode", "digitization"],
}


def html_to_text(html: str) -> str:
    """
    Light HTML cleanup for Stack Exchange post bodies.
    """
    text = clean_text(html)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def fetch_stackexchange_documents(theme: str, queries: list[str], max_results: int = 8) -> list[dict]:
    """
    Collect Stack Overflow / Stack Exchange questions with bodies.
    Each question body is treated as one document.
    """
    records = []
    seen_urls = set()

    site = StackAPI("stackoverflow")
    site.page_size = 20
    site.max_pages = 1

    candidate_tags = TAG_KEYWORDS.get(theme, [])

    # fall back to query-derived single-word hints if needed
    if not candidate_tags:
        for q in queries:
            for token in q.lower().split():
                token = token.strip(",.-_")
                if len(token) > 2:
                    candidate_tags.append(token)

    for tag in candidate_tags:
        if len(records) >= max_results:
            break

        print(f"[StackExchange] Theme='{theme}' | Tag='{tag}'")

        try:
            response = site.fetch(
                "questions",
                tagged=tag,
                sort="votes",
                filter="withbody",
            )

            for item in response.get("items", []):
                if len(records) >= max_results:
                    break

                url = (item.get("link") or "").strip()
                if not url or url in seen_urls:
                    continue

                title = (item.get("title") or "").strip()
                body = html_to_text(item.get("body", ""))

                # combine title + body for a more useful retrieval document
                text = f"{title}\n\n{body}".strip()

                record = make_record(
                    source="StackExchange",
                    theme=theme,
                    title=title,
                    text=text,
                    url=url,
                )

                if is_valid_record(record, min_words=40, max_words=8000):
                    records.append(record)
                    seen_urls.add(url)

            time.sleep(0.6)

        except Exception as e:
            print(f"[StackExchange] Error for tag '{tag}': {e}")

    return records