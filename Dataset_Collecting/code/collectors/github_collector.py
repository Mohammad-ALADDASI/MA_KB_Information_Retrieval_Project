import os
import time
from github import Github

from utils import make_record, is_valid_record


def _get_github_client():
    token = os.getenv("GITHUB_TOKEN", "").strip()
    if token:
        return Github(token)
    return Github()  # unauthenticated fallback, but more limited


def fetch_github_documents(theme: str, queries: list[str], max_results: int = 8) -> list[dict]:
    """
    Collect GitHub README files related to a theme.
    Each README is treated as one document.

    Parameters
    ----------
    theme : str
        Dataset theme label.
    queries : list[str]
        Query phrases used to search repositories.
    max_results : int
        Maximum number of valid README documents to return.

    Returns
    -------
    list[dict]
        Normalized dataset records.
    """
    records = []
    seen_repo_urls = set()
    seen_names = set()

    g = _get_github_client()

    for query in queries:
        if len(records) >= max_results:
            break

        print(f"[GitHub] Theme='{theme}' | Query='{query}'")

        try:
            repos = g.search_repositories(query=query, sort="stars", order="desc")

            for repo in repos:
                if len(records) >= max_results:
                    break

                repo_url = (repo.html_url or "").strip()
                repo_name = (repo.full_name or "").strip().lower()

                if not repo_url or repo_url in seen_repo_urls or repo_name in seen_names:
                    continue

                try:
                    readme = repo.get_readme()
                    content = readme.decoded_content.decode("utf-8", errors="ignore").strip()

                    title = f"{repo.full_name} README"

                    record = make_record(
                        source="GitHub",
                        theme=theme,
                        title=title,
                        text=content,
                        url=repo_url,
                    )

                    if is_valid_record(record, min_words=80, max_words=30000):
                        records.append(record)
                        seen_repo_urls.add(repo_url)
                        seen_names.add(repo_name)

                    time.sleep(0.4)

                except Exception:
                    continue

        except Exception as e:
            print(f"[GitHub] Search error for query '{query}': {e}")

    return records