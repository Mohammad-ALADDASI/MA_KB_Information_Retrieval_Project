from llm_augmented.openai_client import call_llm


def explain_ranking(query: str, document: dict) -> str:
    prompt = f"""
Explain briefly why this document may have been retrieved for the query.

Query:
{query}

Document:
Title: {document.get("title", "")}
Topic: {document.get("topic", "")}
Snippet: {document.get("snippet", "")}

Rules:
- Use 1 to 2 sentences.
- Mention keyword or semantic overlap.
- Do not claim the document is definitely relevant.
"""

    return call_llm(prompt)