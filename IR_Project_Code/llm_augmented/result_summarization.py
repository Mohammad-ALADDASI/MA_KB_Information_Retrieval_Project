from llm_augmented.openai_client import call_llm


def summarize_results(query: str, results: list[dict]) -> str:
    if not results:
        return "No results were retrieved."

    docs_text = []

    for i, doc in enumerate(results[:10], start=1):
        docs_text.append(
            f"""
Document {i}
Title: {doc.get("title", "")}
Topic: {doc.get("topic", "")}
Snippet: {doc.get("snippet", "")}
"""
        )

    prompt = f"""
Summarize the Top-10 retrieval results for the query below.

Query:
{query}

Results:
{chr(10).join(docs_text)}

Rules:
- Write 3 to 5 sentences.
- Mention the main shared themes.
- Do not invent information.
"""

    return call_llm(prompt)