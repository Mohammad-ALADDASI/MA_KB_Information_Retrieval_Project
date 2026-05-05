import csv
import json
import os
from cleaner import clean_text
from field_weighting import build_weighted_document

# Put your CSV here:
# data/raw/input.csv
INPUT_PATH = "data/raw/input.csv"
OUTPUT_PATH = "data/processed/corpus_clean.json"
SUMMARY_WORDS = 80


def first_non_empty(row, *field_names):
    """Return the first non-empty value from possible CSV/JSON field names."""
    for name in field_names:
        value = row.get(name, "")
        if value is not None and str(value).strip() != "":
            return str(value)
    return ""


def make_summary(clean_content, max_words=SUMMARY_WORDS):
    """Create a short summary from cleaned content."""
    return " ".join(clean_content.split()[:max_words])


def normalize_doc(raw_doc, idx):
    """
    Convert a raw CSV/JSON row into the format expected by the search system.

    Your CSV columns:
    source, theme, title, text, url, length_type, doc_id, word_count
    """
    title = first_non_empty(raw_doc, "title")
    url = first_non_empty(raw_doc, "url")
    topic = first_non_empty(raw_doc, "topic", "theme")
    content = first_non_empty(raw_doc, "content", "text")
    summary = first_non_empty(raw_doc, "summary")

    clean_content = clean_text(content)
    clean_summary = clean_text(summary) if summary else make_summary(clean_content)

    raw_doc_id = first_non_empty(raw_doc, "doc_id")
    try:
        doc_id = int(raw_doc_id) if raw_doc_id != "" else idx
    except ValueError:
        doc_id = idx

    clean_doc = {
        "doc_id": doc_id,
        "title": title,
        "url": url,
        "topic": topic,
        "clean_title": clean_text(title),
        "clean_summary": clean_summary,
        "clean_content": clean_content,
    }

    clean_doc["combined_text"] = build_weighted_document(clean_doc)
    return clean_doc


def load_raw_docs(input_path):
    ext = os.path.splitext(input_path)[1].lower()

    if ext == ".csv":
        with open(input_path, "r", encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))

    if ext == ".json":
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else [data]

    raise ValueError("Input file must be .csv or .json")


def build_corpus():
    raw_docs = load_raw_docs(INPUT_PATH)
    processed_docs = [normalize_doc(doc, idx) for idx, doc in enumerate(raw_docs)]

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(processed_docs, f, ensure_ascii=False, indent=2)

    print(f"Processed {len(processed_docs)} documents.")
    print(f"Saved cleaned corpus to {OUTPUT_PATH}")


if __name__ == "__main__":
    build_corpus()
