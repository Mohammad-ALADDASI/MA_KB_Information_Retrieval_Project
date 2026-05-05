from collections import Counter
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from config import OUTPUT_FILE, THEMES, SOURCE_LIMITS, MIN_WORDS, MAX_WORDS
from collectors.arxiv_collector import fetch_arxiv_documents
from collectors.wikipedia_collector import fetch_wikipedia_documents
from collectors.github_collector import fetch_github_documents
from collectors.stackexchange_collector import fetch_stackexchange_documents
from collectors.web_collector import fetch_web_documents


WEB_URLS = {
   
    "AI Governance and Responsible AI": [

    "https://www.unesco.org/en/artificial-intelligence/recommendation-ethics",
    "https://www.unesco.org/en/articles/recommendation-ethics-artificial-intelligence",
    "https://www.unesco.org/en/artificial-intelligence/recommendation-ethics/cases",
    "https://unesdoc.unesco.org/ark:/48223/pf0000380455",
    "https://www.oecd.ai/en/ai-principles",
    "https://www.oecd.ai/en/dashboards/overview",
    "https://ai.google/responsibilities/",
    "https://ai.google/responsibilities/safety/",
    "https://ai.google/responsibilities/accountability/",
    "https://ai.google/responsibilities/privacy-security/",
    "https://www.brookings.edu/topic/artificial-intelligence/",
    "https://www.weforum.org/reports/ai-governance-alliance/",
    "https://hai.stanford.edu/news",
    "https://www.unesco.org/en/artificial-intelligence",
    "https://www.oecd.org/going-digital/ai/principles/"
    ],

    "Environmental Monitoring Systems": [
        "https://www.earthdata.nasa.gov/learn/earth-observation-data-basics",
        "https://www.earthdata.nasa.gov/topics/climate-indicators",
        "https://www.earthdata.nasa.gov/data/projects/eis",
        "https://science.nasa.gov/earth/earth-observatory/",
        "https://www.usgs.gov/special-topics/water-science-school/science/water-quality-monitoring",
        "https://www.epa.gov/measurements-modeling/environmental-monitoring"
    ],

    "Green Computing": [
        "https://www.ibm.com/topics/green-computing",
        "https://aws.amazon.com/sustainability/",
        "https://azure.microsoft.com/en-us/explore/global-infrastructure/sustainability/",
        "https://www.iea.org/reports/digitalisation-and-energy",
        "https://www.nrel.gov/computing/"
    ]
}

WEB_URLS_AI_Bias = [
   "https://research.google/pubs/pub43146/",
    "https://research.google/pubs/fairness-and-machine-learning/",
    "https://pair.withgoogle.com/explorables/fairness/",
    "https://fairmlbook.org/",
    "https://fairlearn.org/main/user_guide/fairness_in_machine_learning.html",
    "https://www.microsoft.com/en-us/research/project/fairness-accountability-transparency-and-ethics-in-ai/",
    "https://www.ibm.com/topics/ai-bias",
    "https://developers.google.com/machine-learning/fairness-overview",
    "https://developers.google.com/machine-learning/fairness-metrics",
    "https://developers.google.com/machine-learning/crash-course/fairness"
    ]
WEB_URLS["AI Bias and Fairness"] = WEB_URLS_AI_Bias
def normalize_text(value: str) -> str:
    return " ".join((value or "").strip().lower().split())


def load_existing_dataset() -> list[dict]:
    """
    Load the existing CSV if it already exists.
    """
    output_path = Path(OUTPUT_FILE)

    if not output_path.exists():
        print("[build_dataset] No existing dataset found. Starting fresh.")
        return []

    try:
        df = pd.read_csv(output_path, encoding="utf-8-sig")
        records = df.fillna("").to_dict(orient="records")
        print(f"[build_dataset] Loaded existing dataset: {len(records)} records")
        return records
    except Exception as e:
        print(f"[build_dataset] Failed to read existing dataset: {e}")
        return []


def build_existing_keys(records: list[dict]) -> tuple[set[str], set[tuple[str, str]]]:
    """
    Build lookup sets from existing dataset so we only keep new documents.
    """
    existing_urls = set()
    existing_source_title = set()

    for record in records:
        url = normalize_text(record.get("url", ""))
        source = normalize_text(record.get("source", ""))
        title = normalize_text(record.get("title", ""))

        if url:
            existing_urls.add(url)
        if source and title:
            existing_source_title.add((source, title))

    return existing_urls, existing_source_title


def filter_out_existing(
    new_records: list[dict],
    existing_urls: set[str],
    existing_source_title: set[tuple[str, str]],
) -> list[dict]:
    """
    Remove anything already present in the current output CSV.
    """
    filtered = []

    for record in new_records:
        url = normalize_text(record.get("url", ""))
        source = normalize_text(record.get("source", ""))
        title = normalize_text(record.get("title", ""))

        if url and url in existing_urls:
            continue
        if source and title and (source, title) in existing_source_title:
            continue

        filtered.append(record)

        if url:
            existing_urls.add(url)
        if source and title:
            existing_source_title.add((source, title))

    return filtered


def deduplicate_records(records: list[dict]) -> list[dict]:
    """
    Remove duplicates primarily by URL, then by (source, lower-title).
    """
    deduped = []
    seen_urls = set()
    seen_source_title = set()

    for record in records:
        url = normalize_text(record.get("url", ""))
        title = normalize_text(record.get("title", ""))
        source = normalize_text(record.get("source", ""))

        source_title_key = (source, title)

        if url and url in seen_urls:
            continue
        if source_title_key in seen_source_title:
            continue

        deduped.append(record)

        if url:
            seen_urls.add(url)
        seen_source_title.add(source_title_key)

    return deduped


def validate_records(records: list[dict]) -> list[dict]:
    """
    Final pass validation using config-level limits.
    """
    valid = []
    for record in records:
        wc = int(record.get("word_count", 0))
        if not record.get("title"):
            continue
        if not record.get("text"):
            continue
        if not record.get("url"):
            continue
        if wc < MIN_WORDS or wc > MAX_WORDS:
            continue
        valid.append(record)
    return valid


def print_summary(records: list[dict], title: str = "DATASET SUMMARY") -> None:
    print(f"\n=== {title} ===")
    print(f"Total documents: {len(records)}")

    source_counts = Counter(r["source"] for r in records)
    theme_counts = Counter(r["theme"] for r in records)
    length_counts = Counter(r["length_type"] for r in records)

    print("\nBy source:")
    for source, count in source_counts.items():
        print(f"  {source}: {count}")

    print("\nBy theme:")
    for theme, count in theme_counts.items():
        print(f"  {theme}: {count}")

    print("\nBy length:")
    for label, count in length_counts.items():
        print(f"  {label}: {count}")


def collect_for_theme(theme: str, queries: list[str]) -> list[dict]:
    theme_records = []

    print(f"\n==============================")
    print(f"Collecting theme: {theme}")
    print(f"==============================")

    try:
        theme_records.extend(
            fetch_arxiv_documents(
                theme=theme,
                queries=queries,
                max_results=SOURCE_LIMITS["arxiv"],
            )
        )
    except Exception as e:
        print(f"[build_dataset] arXiv failed for theme '{theme}': {e}")

    try:
        theme_records.extend(
            fetch_wikipedia_documents(
                theme=theme,
                queries=queries,
                max_results=SOURCE_LIMITS["wikipedia"],
            )
        )
    except Exception as e:
        print(f"[build_dataset] Wikipedia failed for theme '{theme}': {e}")

    try:
        theme_records.extend(
            fetch_github_documents(
                theme=theme,
                queries=queries,
                max_results=SOURCE_LIMITS["github"],
            )
        )
    except Exception as e:
        print(f"[build_dataset] GitHub failed for theme '{theme}': {e}")

    try:
        theme_records.extend(
            fetch_stackexchange_documents(
                theme=theme,
                queries=queries,
                max_results=SOURCE_LIMITS["stackexchange"],
            )
        )
    except Exception as e:
        print(f"[build_dataset] StackExchange failed for theme '{theme}': {e}")

    try:
        theme_records.extend(
            fetch_web_documents(
                theme=theme,
                urls=WEB_URLS.get(theme, []),
                max_results=SOURCE_LIMITS["web"],
            )
        )
    except Exception as e:
        print(f"[build_dataset] Web collector failed for theme '{theme}': {e}")

    return theme_records


def save_dataset(records: list[dict]) -> None:
    df = pd.DataFrame(records)

    column_order = [
        "doc_id",
        "source",
        "theme",
        "title",
        "text",
        "url",
        "word_count",
        "length_type",
    ]

    existing_columns = [col for col in column_order if col in df.columns]
    df = df[existing_columns]

    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
    print(f"\nSaved dataset to: {OUTPUT_FILE}")


def main() -> None:
    load_dotenv()

    existing_records = load_existing_dataset()
    existing_urls, existing_source_title = build_existing_keys(existing_records)

    if existing_records:
        print_summary(existing_records, title="EXISTING DATASET")

    all_new_records = []

    target_theme = "AI Bias and Fairness"

    theme_records = collect_for_theme(
        target_theme,
        THEMES[target_theme]
    )
    all_new_records.extend(theme_records)

    print(f"\nCollected raw new records: {len(all_new_records)}")

    all_new_records = deduplicate_records(all_new_records)
    print(f"After deduplication (new batch only): {len(all_new_records)}")

    all_new_records = validate_records(all_new_records)
    print(f"After validation (new batch only): {len(all_new_records)}")

    all_new_records = filter_out_existing(
        all_new_records,
        existing_urls,
        existing_source_title,
    )
    print(f"After removing records already in existing CSV: {len(all_new_records)}")

    final_records = existing_records + all_new_records

    print_summary(all_new_records, title="NEW RECORDS ADDED")
    print_summary(final_records, title="FINAL MERGED DATASET")

    save_dataset(final_records)


if __name__ == "__main__":
    main()