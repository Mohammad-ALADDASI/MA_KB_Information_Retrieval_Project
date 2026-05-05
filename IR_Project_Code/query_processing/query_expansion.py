"""
Query Expansion Module
Provides synonym expansion and related term suggestions
"""

from query_processing.abbreviation_expansion import expand_abbreviations, detect_abbreviations

SYNONYMS = {
    "algorithm": ["method", "approach", "technique", "procedure"],
    "model": ["architecture", "framework", "system"],
    "network": ["net", "architecture"],
    "learning": ["training", "optimization"],
    "classification": ["categorization", "labeling"],
    "detection": ["recognition", "identification"],
    "analysis": ["evaluation", "assessment", "examination"],
    "processing": ["computation", "handling"],
    "data": ["information", "dataset"],
    "performance": ["efficiency", "accuracy", "effectiveness"],
    "feature": ["attribute", "characteristic", "property"],
    "prediction": ["forecasting", "estimation"],
    "optimization": ["improvement", "enhancement"],
    "clustering": ["grouping", "segmentation"],
    "regression": ["prediction", "estimation"],
}

RELATED_TERMS = {
    "neural network": ["deep learning", "backpropagation", "activation function", "layers"],
    "machine learning": ["supervised learning", "unsupervised learning", "training", "model"],
    "deep learning": ["neural network", "cnn", "rnn", "transformer"],
    "computer vision": ["image processing", "object detection", "image recognition"],
    "nlp": ["natural language processing", "text mining", "language model"],
    "classification": ["supervised learning", "labels", "categories"],
    "clustering": ["unsupervised learning", "grouping", "k-means"],
    "cnn": ["convolutional neural network", "computer vision", "image processing"],
    "rnn": ["recurrent neural network", "sequence", "lstm"],
    "transformer": ["attention", "bert", "gpt"],
}


def get_synonyms(word):
    """
    Get synonyms for a word.
    
    Args:
        word: Input word
        
    Returns:
        List of synonyms
    """
    word_lower = word.lower().strip()
    return SYNONYMS.get(word_lower, [])


def get_related_terms(phrase):
    """
    Get related terms for a phrase.
    
    Args:
        phrase: Input phrase
        
    Returns:
        List of related terms
    """
    phrase_lower = phrase.lower().strip()
    return RELATED_TERMS.get(phrase_lower, [])


def expand_with_synonyms(query):
    """
    Expand query with synonyms of key terms.
    
    Args:
        query: Input query
        
    Returns:
        Expanded query string
    """
    tokens = query.lower().split()
    expanded_tokens = []
    
    for token in tokens:
        expanded_tokens.append(token)
        synonyms = get_synonyms(token)
        if synonyms:
            # Add top 2 synonyms
            expanded_tokens.extend(synonyms[:2])
    
    return " ".join(expanded_tokens)


def expand_with_related_terms(query):
    """
    Expand query with related domain terms.
    
    Args:
        query: Input query
        
    Returns:
        Expanded query string
    """
    query_lower = query.lower()
    expanded = query
    
    for phrase, related in RELATED_TERMS.items():
        if phrase in query_lower:
            # Add top 3 related terms
            expanded += " " + " ".join(related[:3])
            break
    
    return expanded


def suggest_expanded_queries(query, num_suggestions=3):
    """
    Suggest multiple expanded query variations.
    
    Args:
        query: Original query
        num_suggestions: Number of suggestions to generate
        
    Returns:
        List of suggested queries with metadata
    """
    suggestions = []
    
    synonym_expanded = expand_with_synonyms(query)
    if synonym_expanded != query:
        suggestions.append({
            "query": synonym_expanded,
            "type": "synonym_expansion",
            "description": "Query expanded with synonyms"
        })
    
    related_expanded = expand_with_related_terms(query)
    if related_expanded != query:
        suggestions.append({
            "query": related_expanded,
            "type": "related_terms",
            "description": "Query expanded with related terms"
        })
    
    detected_abbr = detect_abbreviations(query)
    if detected_abbr:
        abbr_expanded = expand_abbreviations(query)
        combined = expand_with_related_terms(abbr_expanded)
        suggestions.append({
            "query": combined,
            "type": "abbreviation_and_related",
            "description": "Abbreviations expanded with related terms"
        })
    
    return suggestions[:num_suggestions]


def apply_query_expansion(query, strategy="balanced"):
    """
    Apply query expansion based on strategy.
    
    Args:
        query: Input query
        strategy: "conservative", "balanced", or "aggressive"
        
    Returns:
        Expanded query
    """
    if strategy == "conservative":
        return expand_abbreviations(query)
    
    elif strategy == "balanced":
        expanded = expand_abbreviations(query)
        return expand_with_related_terms(expanded)
    
    elif strategy == "aggressive":
        expanded = expand_abbreviations(query)
        expanded = expand_with_synonyms(expanded)
        return expand_with_related_terms(expanded)
    
    return query


if __name__ == "__main__":
    test_queries = [
        "ml classification",
        "cnn for image detection",
        "nlp model",
    ]
    
    print("=" * 60)
    print("QUERY EXPANSION TESTS")
    print("=" * 60)
    
    for query in test_queries:
        print(f"\nOriginal: {query}")
        print(f"Synonyms: {expand_with_synonyms(query)}")
        print(f"Related: {expand_with_related_terms(query)}")
        print(f"Suggestions:")
        for suggestion in suggest_expanded_queries(query):
            print(f"  - {suggestion['type']}: {suggestion['query'][:80]}...")