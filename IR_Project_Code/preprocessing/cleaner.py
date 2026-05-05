import re
import string


def clean_text(text: str) -> str:
    """
    Clean and normalize text by:
    - Converting to lowercase
    - Removing special characters and extra whitespace
    - Removing punctuation
    """
    if not text:
        return ""
    
    text = text.lower()
    
    text = re.sub(r'http\S+|www\S+', '', text)
    
    text = re.sub(r'\s+', ' ', text)
    
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    return text.strip()


def build_weighted_document(doc: dict) -> str:
    """
    Create a single weighted document text
    from multiple fields.
    """

    title = doc.get("clean_title", "")
    summary = doc.get("clean_summary", "")
    content = doc.get("clean_content", "")
    topic = doc.get("topic", "")

    weighted_text = (
        (title + " ") * 3 +
        (summary + " ") * 2 +
        (topic + " ") * 2 +
        content
    )

    return weighted_text.strip()
