"""
Simplified search interface
"""
from retrieval.retrieve import retrieve_bm25, retrieve_lm, retrieve_tfidf
from query_processing.spell_correction import get_correction_suggestions


def search(query, model="bm25", top_n=10):
    """
    Main search function with automatic spell check suggestions.
    
    Args:
        query: User query
        model: Retrieval model ("bm25", "tfidf", or "lm")
        top_n: Number of results to return
        
    Returns:
        Dictionary with query, suggestions, and results
    """
    if model == "bm25":
        results = retrieve_bm25(query, top_n)
    elif model == "tfidf":
        results = retrieve_tfidf(query, top_n)
    else:
        results = retrieve_lm(query, top_n)

    suggestion = None
    if not results or (len(results) > 0 and results[0].get("score", 0) < 0.05):
        suggestions = get_correction_suggestions(query, max_suggestions=1)
        if suggestions:
            suggestion = suggestions[0][0]  

    return {
        "query": query,
        "suggestion": suggestion,
        "results": results
    }