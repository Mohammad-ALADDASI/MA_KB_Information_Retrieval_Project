import json
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

CORPUS_PATH = "data/processed/corpus_clean.json"
TFIDF_MATRIX_PATH = "data/processed/tfidf_matrix.pkl"
VECTORIZER_PATH = "data/processed/tfidf_vectorizer.pkl"
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


def build_tfidf_index():
    with open(CORPUS_PATH, "r", encoding="utf-8") as f:
        corpus = json.load(f)

    docs_text = [doc["combined_text"] for doc in corpus]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(docs_text)

    with open(TFIDF_MATRIX_PATH, "wb") as f:
        pickle.dump(tfidf_matrix, f)
    with open(VECTORIZER_PATH, "wb") as f:
        pickle.dump(vectorizer, f)

    doc_mapping = build_complete_doc_mapping(corpus)
    with open(DOC_MAPPING_PATH, "wb") as f:
        pickle.dump(doc_mapping, f)

    print(f"✅ TF-IDF index built for {len(corpus)} documents.")
    print(f"✅ Document mapping saved with {len(doc_mapping[0].keys())} fields per document")


if __name__ == "__main__":
    build_tfidf_index()