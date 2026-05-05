import json
import pickle
from collections import Counter

CORPUS_PATH = "data/processed/corpus_clean.json"
LM_STATS_PATH = "data/processed/lm_stats.pkl"
DOC_MAPPING_PATH = "data/processed/doc_mapping.pkl"


def build_complete_doc_mapping(corpus):
    doc_mapping = {}

    for row_index, doc in enumerate(corpus):
        doc_mapping[row_index] = {
            "original_doc_id": doc.get("doc_id", row_index),
            "title": doc.get("title", ""),
            "url": doc.get("url", ""),
            "topic": doc.get("topic", ""),
            "clean_title": doc.get("clean_title", ""),
            "clean_summary": doc.get("clean_summary", ""),
            "clean_content": doc.get("clean_content", ""),
            "combined_text": doc.get("combined_text", "")
        }

    return doc_mapping


def build_lm_index():
    with open(CORPUS_PATH, "r", encoding="utf-8") as f:
        corpus = json.load(f)

    doc_word_counts = {}
    doc_lengths = {}
    collection_counts = Counter()
    total_terms = 0

    for row_index, doc in enumerate(corpus):
        tokens = doc.get("combined_text", "").split()

        if not tokens:
            tokens = ["__empty__"]

        counter = Counter(tokens)

        doc_word_counts[row_index] = counter
        doc_lengths[row_index] = len(tokens)

        collection_counts.update(counter)
        total_terms += len(tokens)

    if total_terms == 0:
        total_terms = 1

    lm_stats = {
        "doc_word_counts": doc_word_counts,
        "doc_lengths": doc_lengths,
        "collection_counts": collection_counts,
        "total_terms": total_terms
    }

    with open(LM_STATS_PATH, "wb") as f:
        pickle.dump(lm_stats, f)

    doc_mapping = build_complete_doc_mapping(corpus)

    with open(DOC_MAPPING_PATH, "wb") as f:
        pickle.dump(doc_mapping, f)

    print(f"✅ Language Model statistics built for {len(corpus)} documents.")
    print(f"✅ Total collection terms: {total_terms}")
    print(f"✅ Vocabulary size: {len(collection_counts)}")
    print(f"✅ Document mapping saved for {len(doc_mapping)} documents.")


if __name__ == "__main__":
    build_lm_index()