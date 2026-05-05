import sys
import os
import time
import re
from flask import Flask, render_template, request
import markdown
# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from retrieval.retrieve import retrieve_bm25, retrieve_tfidf, retrieve_lm, get_query_expansion_suggestions
from query_processing.spell_correction import get_correction_suggestions, correct_query
from query_processing.domain_check import is_query_in_domain, get_domain_confidence

from llm_augmented import (
    augment_query,
    summarize_top_results,
    add_ranking_explanations,
)
app = Flask(__name__)

def highlight_keywords(text, query_for_highlight):
    """Highlight query keywords and exact phrases in text"""
    highlighted = text
    
    phrase_pattern = r'"([^"]+)"'
    phrases = re.findall(phrase_pattern, query_for_highlight)
    
    for phrase in phrases:
        phrase_clean = phrase.strip()
        if phrase_clean:
            pattern = re.compile(f'({re.escape(phrase_clean)})', re.IGNORECASE)
            highlighted = pattern.sub(r'<span class="highlight" style="background-color: #ffeb3b; font-weight: bold;">\1</span>', highlighted)
    
    keywords = [w.strip('"') for w in query_for_highlight.lower().split() if len(w.strip('"')) > 2 and '"' not in w]
    
    for keyword in keywords:
        pattern = re.compile(f'({re.escape(keyword)})', re.IGNORECASE)
        highlighted = pattern.sub(r'<span class="highlight">\1</span>', highlighted)
    
    return highlighted
def render_markdown(text):
    if not text:
        return ""
    return markdown.markdown(
        text,
        extensions=["extra", "nl2br", "sane_lists"]
    )

@app.route("/")
def index():
    query = request.args.get("q", "")
    model_option = request.args.get("model", "BM25")
    top_n = int(request.args.get("top_n", 10))

    use_llm = request.args.get("use_llm") == "on"
    use_summary = request.args.get("summary") == "on"
    use_explanations = request.args.get("explain") == "on"

    llm_info = None
    llm_summary = None
    llm_summary_html = None
    llm_error = None

    if not query:
        return render_template(
            "index.html",
            query="",
            model=model_option,
            top_n=top_n,
            use_llm=use_llm,
            use_summary=use_summary,
            use_explanations=use_explanations,
            llm_info=llm_info,
            llm_summary=llm_summary,
            llm_summary_html=llm_summary_html,
            llm_error=llm_error,
        )

    start_time = time.time()

    domain_confidence = get_domain_confidence(query)
    in_domain = is_query_in_domain(query)

    if not in_domain:
        return render_template(
            "index.html",
            query=query,
            error=True,
            domain_confidence=domain_confidence,
            model=model_option,
            top_n=top_n,
            use_llm=use_llm,
            use_summary=use_summary,
            use_explanations=use_explanations,
            llm_info=llm_info,
            llm_summary=llm_summary,
            llm_summary_html=llm_summary_html,
            llm_error=llm_error,
        )

    has_quotes = '"' in query or "“" in query or "”" in query

    if has_quotes:
        corrected_query = query
        query_was_corrected = False
    else:
        corrected_query = correct_query(query, min_confidence=0.70)
        query_was_corrected = corrected_query.lower().strip() != query.lower().strip()

    suggestion = None
    display_corrected = None

    if query_was_corrected:
        query_to_use = corrected_query
        display_corrected = corrected_query
    else:
        query_to_use = query
        suggestions = get_correction_suggestions(query, max_suggestions=1)

        if suggestions:
            suggested_query, confidence = suggestions[0]
            if suggested_query.lower() != query.lower() and confidence > 0.70:
                suggestion = (suggested_query, confidence)

    try:
        if use_llm and query_to_use.strip():
            llm_info = augment_query(
                query_to_use,
                use_rewrite=True,
                use_expansion=True,
            )
            query_to_use = llm_info["expanded_query"]
    except Exception as e:
        llm_error = f"LLM query augmentation failed: {str(e)}"

    expansions = []
    if not has_quotes:
        expansions = get_query_expansion_suggestions(query_to_use, num_suggestions=2)

    if model_option == "BM25":
        results = retrieve_bm25(query_to_use, top_n=top_n)
    elif model_option == "TF-IDF":
        results = retrieve_tfidf(query_to_use, top_n=top_n)
    else:
        results = retrieve_lm(query_to_use, top_n=top_n)

    try:
        if use_summary and results:
            llm_summary = summarize_top_results(query_to_use, results)
            llm_summary_html = render_markdown(llm_summary)
    except Exception as e:
        llm_error = f"LLM summarization failed: {str(e)}"

    try:
        if use_explanations and results:
            results = add_ranking_explanations(query_to_use, results, limit=10)

            for res in results:
                if res.get("llm_explanation"):
                    res["llm_explanation_html"] = render_markdown(
                        res["llm_explanation"]
                    )
    except Exception as e:
        llm_error = f"LLM ranking explanation failed: {str(e)}"

    search_time = time.time() - start_time
    exact_match_count = sum(1 for r in results if r.get("exact_match", False))

    for res in results:
        res["highlighted_snippet"] = highlight_keywords(
            res.get("snippet", ""),
            query_to_use,
        )

    return render_template(
        "index.html",
        query=query,
        query_to_use=query_to_use,
        corrected_query=display_corrected,
        suggestion=suggestion,
        model=model_option,
        top_n=top_n,
        results=results,
        search_time=search_time,
        domain_confidence=domain_confidence,
        has_quotes=has_quotes,
        expansions=expansions,
        exact_match_count=exact_match_count,
        use_llm=use_llm,
        use_summary=use_summary,
        use_explanations=use_explanations,
        llm_info=llm_info,
        llm_summary=llm_summary,
        llm_summary_html=llm_summary_html,
        llm_error=llm_error,
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
