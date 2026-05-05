import json
import pickle
from rank_bm25 import BM25Okapi

CORPUS_PATH = "data/processed/corpus_clean.json"
INDEX_PATH = "data/processed/bm25_index.pkl"
DOC_MAPPING_PATH = "data/processed/doc_mapping.pkl"


def build_complete_doc_mapping(corpus):
    doc_mapping = {}

    for row_index, doc in enumerate(corpus):
        doc_mapping[row_index] = {
            "original_doc_id": doc.get("doc_id", row_index),
            "title": doc["title"],
            "url": doc["url"],
            "topic": doc["topic"],
            "clean_title": doc.get("clean_title", ""),
            "clean_summary": doc.get("clean_summary", ""),
            "clean_content": doc.get("clean_content", ""),
            "combined_text": doc.get("combined_text", "")
        }

    return doc_mapping


def build_bm25_index():
    with open(CORPUS_PATH, "r", encoding="utf-8") as f:
        corpus = json.load(f)

    tokenized_corpus = [doc["combined_text"].split() for doc in corpus]

    bm25 = BM25Okapi(tokenized_corpus)

    with open(INDEX_PATH, "wb") as f:
        pickle.dump(bm25, f)

    doc_mapping = build_complete_doc_mapping(corpus)
    with open(DOC_MAPPING_PATH, "wb") as f:
        pickle.dump(doc_mapping, f)

    print(f" BM25 index built and saved for {len(corpus)} documents.")
    print(f" Document mapping saved with {len(doc_mapping[0].keys())} fields per document")


if __name__ == "__main__":
    build_bm25_index()