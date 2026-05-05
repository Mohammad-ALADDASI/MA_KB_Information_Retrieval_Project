from llm_augmented.openai_client import call_llm


def rewrite_query(query: str) -> str:
    prompt = f"""
Rewrite the following search query into a clearer and more structured information retrieval query.

Rules:
- Preserve the original meaning.
- Do not add unrelated concepts.
- Keep it short.
- Return only the rewritten query.

Original query:
{query}
"""

    rewritten = call_llm(prompt)

    return rewritten.strip() if rewritten else query