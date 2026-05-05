from llm_augmented.query_rewriting import rewrite_query
from llm_augmented.query_expansion import expand_query_llm
from llm_augmented.result_summarization import summarize_results
from llm_augmented.ranking_explanation import explain_ranking


def augment_query(
    query: str,
    use_rewrite: bool = True,
    use_expansion: bool = True,
) -> dict:
    original_query = query
    rewritten_query = query
    expanded_query = query
    expansion_terms = []

    if use_rewrite:
        rewritten_query = rewrite_query(original_query)

    if use_expansion:
        expanded_query, expansion_terms = expand_query_llm(rewritten_query)
    else:
        expanded_query = rewritten_query

    return {
        "original_query": original_query,
        "rewritten_query": rewritten_query,
        "expanded_query": expanded_query,
        "expansion_terms": expansion_terms,
    }


def summarize_top_results(query: str, results: list[dict]) -> str:
    return summarize_results(query, results)


def add_ranking_explanations(query: str, results: list[dict], limit: int = 10) -> list[dict]:
    explained_results = []

    for i, result in enumerate(results):
        result_copy = dict(result)

        if i < limit:
            result_copy["llm_explanation"] = explain_ranking(query, result)

        explained_results.append(result_copy)

    return explained_results