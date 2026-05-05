import pickle
import os
from rank_bm25 import BM25Okapi
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

from query_processing.normalization import normalize_query
from query_processing.spell_correction import correct_query, add_to_vocab
from query_processing.abbreviation_expansion import expand_abbreviations
from query_processing.topic_expansion import expand_query_with_topics
from query_processing.domain_check import is_query_in_domain
from query_processing.query_expansion import (
    get_synonyms,
    expand_with_synonyms,
    expand_with_related_terms,
    suggest_expanded_queries,
    apply_query_expansion
)

BM25_INDEX_PATH = os.path.join(os.path.dirname(__file__), "../data/processed/bm25_index.pkl")
TFIDF_MATRIX_PATH = os.path.join(os.path.dirname(__file__), "../data/processed/tfidf_matrix.pkl")
TFIDF_VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), "../data/processed/tfidf_vectorizer.pkl")
LM_STATS_PATH = os.path.join(os.path.dirname(__file__), "../data/processed/lm_stats.pkl")
DOC_MAPPING_PATH = os.path.join(os.path.dirname(__file__), "../data/processed/doc_mapping.pkl")

with open(DOC_MAPPING_PATH, "rb") as f:
    DOC_MAPPING = pickle.load(f)

all_words = []
for doc in DOC_MAPPING.values():
    content = doc.get("clean_content") or doc.get("content") or doc.get("clean_summary") or ""
    title = doc.get("clean_title") or doc.get("title") or ""
    
    if content:
        content_normalized = re.sub(r"[^\w\s]", " ", content)
        all_words.extend(content_normalized.split())
    if title:
        title_normalized = re.sub(r"[^\w\s]", " ", title)
        all_words.extend(title_normalized.split())

all_words = list(set(w for w in all_words if w.strip()))
add_to_vocab(all_words)

with open(BM25_INDEX_PATH, "rb") as f:
    BM25_INDEX = pickle.load(f)

with open(TFIDF_MATRIX_PATH, "rb") as f:
    TFIDF_MATRIX = pickle.load(f)

with open(TFIDF_VECTORIZER_PATH, "rb") as f:
    TFIDF_VECTORIZER = pickle.load(f)

with open(LM_STATS_PATH, "rb") as f:
    LM_STATS = pickle.load(f)


def get_query_expansion_suggestions(query, num_suggestions=3):
    """
    Get query expansion suggestions for the user.
    
    Args:
        query: Original query string
        num_suggestions: Number of suggestions to return
        
    Returns:
        List of expansion suggestions with details
    """
    if '"' in query:
        return []
    
    return suggest_expanded_queries(query, num_suggestions=num_suggestions)


def extract_phrase_query(query):
    """
    Extract exact phrases from straight or curly quotes.

    Example:
        machine "deep learning" models
    returns:
        ["deep learning"], "machine models"
    """
    if not query:
        return [], ""

    query = query.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")

    phrase_pattern = r'"([^"]+)"'
    phrases = re.findall(phrase_pattern, query)

    phrases = [normalize_for_phrase(p) for p in phrases if p.strip()]

    remaining = re.sub(phrase_pattern, " ", query)
    remaining = re.sub(r"\s+", " ", remaining).strip()

    return phrases, remaining


def normalize_for_phrase(text):
    """
    Normalize text for exact phrase comparison.
    """
    if not text:
        return ""

    text = str(text).lower()
    text = text.replace("-", " ")
    text = text.replace("_", " ")
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def document_text_for_phrase(doc):
    """
    Use every useful field for exact phrase matching.
    """
    return normalize_for_phrase(" ".join([
        str(doc.get("title", "")),
        str(doc.get("topic", "")),
        str(doc.get("clean_title", "")),
        str(doc.get("clean_summary", "")),
        str(doc.get("clean_content", "")),
        str(doc.get("combined_text", "")),
    ]))


def phrase_filter_and_boost(results, exact_phrases):
    """
    If the query contains quoted phrases, require every quoted phrase
    to appear exactly in the document text.

    This makes "game engine" behave as a real phrase query.
    """
    if not exact_phrases:
        return results

    filtered = []

    for result in results:
        text = normalize_for_phrase(" ".join([
            str(result.get("title", "")),
            str(result.get("topic", "")),
            str(result.get("snippet", "")),
            str(result.get("full_content", "")),
            str(result.get("combined_text", "")),
        ]))

        if all(phrase in text for phrase in exact_phrases):
            result["exact_match"] = True
            result["score"] = float(result["score"]) * 10
            filtered.append(result)

    filtered.sort(key=lambda x: x["score"], reverse=True)
    return filtered


def topic_boosting(results, detected_topics, boost_value=0.15):
    """
    Boost score for documents whose topic matches detected topic
    """
    boosted_results = []
    for r in results:
        score = r["score"]
        if r.get("topic") in detected_topics:
            score += score * boost_value
        boosted_results.append({**r, "score": score})
    boosted_results.sort(key=lambda x: x["score"], reverse=True)
    return boosted_results


def preprocess_query(query, skip_expansion=False):
    """
    Full query preprocessing pipeline.
    
    Args:
        query: Raw user query (ALREADY spell-corrected by app.py)
        skip_expansion: If True, skip abbreviation/topic expansion (for exact phrase queries)
    
    Returns:
        (final_query, detected_topics, exact_phrases)
    """
    exact_phrases, remaining_query = extract_phrase_query(query)
    
    query_to_process = remaining_query if remaining_query else query
    
    processed = normalize_query(query_to_process)
    
    if not skip_expansion and not exact_phrases:
        expanded_query = expand_abbreviations(processed)
    else:
        expanded_query = processed
    
    
    if not skip_expansion and not exact_phrases:
        final_query, detected_topics = expand_query_with_topics(expanded_query)
    else:
        final_query = expanded_query
        detected_topics = []
    
    return final_query, detected_topics, exact_phrases

def handle_out_of_domain_query(query):
    """
    Return informative message for out-of-domain queries
    """
    return [{
        "doc_id": -1,
        "title": "Query Outside Domain",
        "url": "",
        "snippet": f"Your query '{query}' appears to be outside our knowledge base domain. "
                   "This system specializes in AI, Machine Learning, Computer Vision, "
                   "Natural Language Processing, and Data Science topics. "
                   "Please try queries related to these areas.",
        "score": 0,
        "out_of_domain": True
    }]


def retrieve_bm25(query, top_n=10):
    """
    BM25 retrieval with full query processing.
    
    Args:
        query: Original user query (may contain quotes for phrases)
        top_n: Number of results to return
    """
    if not is_query_in_domain(query):
        return handle_out_of_domain_query(query)
    
    expanded_query, detected_topics, exact_phrases = preprocess_query(query)
    
    query_tokens = expanded_query.split()
    scores = BM25_INDEX.get_scores(query_tokens)
    
    results = []
    for doc_id, score in enumerate(scores):
        if score > 0:
            doc = DOC_MAPPING[doc_id]
            results.append({
                "doc_id": doc.get("original_doc_id", doc_id),
                "score": score,
                "title": doc["title"],
                "url": doc["url"],
                "topic": doc["topic"],
                "snippet": doc["clean_summary"][:200],
                "full_content": doc.get("clean_content", ""),
                "exact_match": False
            })
    
    if not results:
        return [{
            "title": "No relevant results",
            "url": "",
            "snippet": "No documents match your query. Try different keywords.",
            "score": 0
        }]
    
    results = topic_boosting(results, detected_topics)
    results = phrase_filter_and_boost(results, exact_phrases)  
    
    return results[:top_n]



def retrieve_tfidf(query, top_n=10):
    """
    TF-IDF retrieval with full query processing.
    """
    if not is_query_in_domain(query):
        return handle_out_of_domain_query(query)
    
    expanded_query, detected_topics, exact_phrases = preprocess_query(query)
    
    query_vec = TFIDF_VECTORIZER.transform([expanded_query])
    scores = cosine_similarity(query_vec, TFIDF_MATRIX).flatten()
    
    results = []
    for doc_id, score in enumerate(scores):
        if score > 0:
            doc = DOC_MAPPING[doc_id]
            results.append({
                "doc_id": doc.get("original_doc_id", doc_id),
                "score": float(score),
                "title": doc["title"],
                "url": doc["url"],
                "topic": doc["topic"],
                "snippet": doc["clean_summary"][:200],
                "full_content": doc.get("clean_content", ""),
                "exact_match": False
            })
    
    if not results:
        return [{
            "title": "No relevant results",
            "url": "",
            "snippet": "No documents match your query. Try different keywords.",
            "score": 0
        }]
    
    results = topic_boosting(results, detected_topics)
    results = phrase_filter_and_boost(results, exact_phrases)  # Pass original query!
    
    return results[:top_n]


def retrieve_lm(query, top_n=10, mu=2000):
    """
    Language Model retrieval with Dirichlet smoothing.
    """
    if not is_query_in_domain(query):
        return handle_out_of_domain_query(query)
    
    expanded_query, detected_topics, exact_phrases = preprocess_query(query)
    query_tokens = expanded_query.split()
    
    collection_counts = LM_STATS["collection_counts"]
    total_terms = LM_STATS["total_terms"]
    doc_word_counts = LM_STATS["doc_word_counts"]
    doc_lengths = LM_STATS["doc_lengths"]
    
    results = []
    for doc_id in doc_word_counts:
        score = 0.0
        doc_len = doc_lengths[doc_id]
        counter = doc_word_counts[doc_id]
        
        for token in query_tokens:
            tf = counter.get(token, 0)
            cf = collection_counts.get(token, 0)
            p_td = (tf + mu * (cf / total_terms)) / (doc_len + mu)
            score += np.log(p_td + 1e-12)
        
        doc = DOC_MAPPING[doc_id]
        results.append({
            "doc_id": doc.get("original_doc_id", doc_id),
            "score": score,
            "title": doc["title"],
            "url": doc["url"],
            "topic": doc["topic"],
            "snippet": doc["clean_summary"][:200],
            "full_content": doc.get("clean_content", ""),
            "exact_match": False
        })
    
    results.sort(key=lambda x: x["score"], reverse=True)
    
    if results and len(set(r["score"] for r in results[:5])) == 1:
        return [{
            "title": "No relevant results",
            "url": "",
            "snippet": "No documents match your query. Try different keywords.",
            "score": 0
        }]
    
    results = topic_boosting(results, detected_topics)
    results = phrase_filter_and_boost(results, exact_phrases)  
    
    return results[:top_n]