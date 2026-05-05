import time
import arxiv

from utils import make_record, is_valid_record


def fetch_arxiv_documents(theme: str, queries: list[str], max_results: int = 12) -> list[dict]:
    """
    Collect arXiv paper abstracts for a given theme.
    Each abstract is treated as one short document.

    Parameters
    ----------
    theme : str
        The normalized theme name used in your dataset.
    queries : list[str]
        Query phrases related to the theme.
    max_results : int
        Maximum number of valid documents to return.

    Returns
    -------
    list[dict]
        List of normalized dataset records.
    """
    records = []
    seen_urls = set()

    client = arxiv.Client(
        page_size=25,
        delay_seconds=3,
        num_retries=3,
    )

    for query in queries:
        if len(records) >= max_results:
            break

        print(f"[arXiv] Theme='{theme}' | Query='{query}'")

        search = arxiv.Search(
            query=query,
            max_results=25,
            sort_by=arxiv.SortCriterion.Relevance,
        )

        try:
            for result in client.results(search):
                url = (result.entry_id or "").strip()
                if not url or url in seen_urls:
                    continue

                title = (result.title or "").replace("\n", " ").strip()
                summary = (result.summary or "").replace("\n", " ").strip()

                record = make_record(
                    source="arXiv",
                    theme=theme,
                    title=title,
                    text=summary,
                    url=url,
                )

                if is_valid_record(record, min_words=40, max_words=2000):
                    records.append(record)
                    seen_urls.add(url)

                if len(records) >= max_results:
                    break

            time.sleep(1)

        except Exception as e:
            print(f"[arXiv] Error for query '{query}': {e}")

    return records