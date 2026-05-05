import re

def normalize_query(query: str) -> str:
    """
    Normalize user query:
    - Lowercase
    - Strip extra whitespace
    - Remove unwanted symbols (keep words and spaces)
    """
    if not query:
        return ""
    
    query = query.lower()
    query = re.sub(r"[^\w\s]", " ", query)  
    query = re.sub(r"\s+", " ", query)      
    return query.strip()
