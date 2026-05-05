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
