from difflib import get_close_matches
import re
from collections import Counter
from query_processing.abbreviation_expansion import ABBREVIATIONS

CUSTOM_VOCAB = set()
WORD_FREQUENCY = Counter()

def add_to_vocab(words):
    """
    Add words from corpus to vocabulary with frequency tracking
    """
    global CUSTOM_VOCAB, WORD_FREQUENCY
    
    if isinstance(words, str):
        word_list = words.lower().split()
    else:
        word_list = [str(word).lower() for word in words if word]
    
    CUSTOM_VOCAB.update(word_list)
    
    WORD_FREQUENCY.update(word_list)


def edit_distance(s1, s2):
    """
    Calculate Levenshtein distance between two strings
    """
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    
    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        new_distances = [i2 + 1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                new_distances.append(distances[i1])
            else:
                new_distances.append(1 + min((distances[i1], distances[i1 + 1], new_distances[-1])))
        distances = new_distances
    
    return distances[-1]


def split_compound_word(word):
    """
    Try to split a compound word into valid vocabulary words
    """
    word_lower = word.lower()
    
    if len(word_lower) < 6:
        return None
    
    best_match = None
    best_score = 0
    
    for i in range(3, len(word_lower) - 2):
        first_part = word_lower[:i]
        second_part = word_lower[i:]
        
        if first_part in CUSTOM_VOCAB and second_part in CUSTOM_VOCAB:
            score = WORD_FREQUENCY.get(first_part, 0) + WORD_FREQUENCY.get(second_part, 0)
            if score > best_score:
                best_score = score
                best_match = f"{first_part} {second_part}"
    
    return best_match


def handle_common_typos(word):
    """
    Handle common typing mistakes
    """
    deduplicated = re.sub(r'(.)\1{2,}', r'\1\1', word)
    if deduplicated in CUSTOM_VOCAB:
        return deduplicated
    
    deduplicated = re.sub(r'(.)\1+', r'\1', word)
    if deduplicated in CUSTOM_VOCAB:
        return deduplicated
    
    return None


def correct_word(word):
    """
    Correct a single word using multiple strategies
    Returns: (corrected_word, confidence_score)
    """
    word_lower = word.lower()
    
    if word_lower in ABBREVIATIONS:
        return word_lower, 1.0
    
    if word_lower in CUSTOM_VOCAB:
        return word_lower, 1.0
    
    typo_fix = handle_common_typos(word_lower)
    if typo_fix:
        return typo_fix, 0.95
    
    split_result = split_compound_word(word_lower)
    if split_result:
        return split_result, 0.90
    
    if len(word_lower) <= 2:
        return word_lower, 0.0
    elif len(word_lower) <= 3:
        matches = get_close_matches(word_lower, CUSTOM_VOCAB, n=5, cutoff=0.85)
    elif len(word_lower) <= 5:
        matches = get_close_matches(word_lower, CUSTOM_VOCAB, n=5, cutoff=0.75)
    elif len(word_lower) <= 8:
        matches = get_close_matches(word_lower, CUSTOM_VOCAB, n=5, cutoff=0.70)
    else:
        matches = get_close_matches(word_lower, CUSTOM_VOCAB, n=5, cutoff=0.65)
    
    if matches:
        best_match = None
        best_score = 0
        
        for match in matches:
            freq_score = WORD_FREQUENCY.get(match, 0)
            distance = edit_distance(word_lower, match)
            max_distance = max(len(word_lower), len(match))
            similarity = 1.0 - (distance / max_distance)
            
            combined_score = (similarity * 0.7) + (min(freq_score / 100, 1.0) * 0.3)
            
            if combined_score > best_score:
                best_score = combined_score
                best_match = match
        
        if best_match:
            distance = edit_distance(word_lower, best_match)
            max_distance = max(len(word_lower), len(best_match))
            confidence = 1.0 - (distance / max_distance)
            
            return best_match, confidence
    
    return word_lower, 0.0


def correct_query(query: str, min_confidence=0.70):
    """
    Correct spelling mistakes in query with confidence threshold
    
    Args:
        query: Input query string
        min_confidence: Minimum confidence to apply correction (default 0.70 for better corrections)
    
    Returns:
        Corrected query string
    """
    query_lower = query.lower().strip()
    
    if not query_lower:
        return ""
    
    tokens = query_lower.split()
    corrected_tokens = []
    
    for token in tokens:
        clean_token = re.sub(r'[^\w]', '', token)
        
        if not clean_token:
            continue
        
        if clean_token in ABBREVIATIONS:
            corrected_tokens.append(clean_token)
            continue
        
        corrected_word, confidence = correct_word(clean_token)
        
        if confidence >= min_confidence:
            corrected_tokens.append(corrected_word)
        elif clean_token not in CUSTOM_VOCAB and confidence > 0.6:
            corrected_tokens.append(corrected_word)
        else:
            corrected_tokens.append(clean_token)
    
    return " ".join(corrected_tokens)


def get_correction_suggestions(query, max_suggestions=3):
    """
    Get multiple correction suggestions for a query
    Returns: List of (corrected_query, confidence) tuples
    """
    tokens = query.lower().split()
    suggestions = []
    all_corrections = {}
    
    for i, token in enumerate(tokens):
        clean_token = re.sub(r'[^\w]', '', token)
        
        if clean_token in ABBREVIATIONS:
            continue
        
        corrected, confidence = correct_word(clean_token)
        
        if corrected != clean_token and confidence > 0.65:
            all_corrections[i] = (corrected, confidence)
    
    if all_corrections:
        new_tokens = tokens.copy()
        total_confidence = 0
        
        for idx, (corrected, conf) in all_corrections.items():
            new_tokens[idx] = corrected
            total_confidence += conf
        
        avg_confidence = total_confidence / len(all_corrections)
        suggested_query = " ".join(new_tokens)
        
        suggestions.append((suggested_query, avg_confidence))
    
    return suggestions[:max_suggestions]