from llm_augmented.openai_client import call_llm
from llm_augmented.config import MAX_EXPANSION_TERMS


def expand_query_llm(query: str) -> tuple[str, list[str]]:
    prompt = f"""
Generate related search terms and synonyms for this information retrieval query.

Rules:
- Return only comma-separated terms.
- Maximum {MAX_EXPANSION_TERMS} terms.
- Do not include explanations.
- Avoid unrelated terms.

Query:
{query}
"""

    output = call_llm(prompt)

    terms = [
        term.strip().lower()
        for term in output.split(",")
        if term.strip()
    ]

    terms = list(dict.fromkeys(terms))[:MAX_EXPANSION_TERMS]

    expanded_query = query + " " + " ".join(terms)

    return expanded_query, terms