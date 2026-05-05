import sys
import os

# Set up paths
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from retrieval.search import search

queries = [
    {"q": "procedural generation algorithms rogue-like terrain", "type": "Keyword", "challenge": "Contains specific technical terms and game dev jargon."},
    {"q": "iot edge device botnet ddos vulnerabilities", "type": "Keyword", "challenge": "Dense string of cybersecurity and networking keywords."},
    {"q": "data center pue dynamic voltage frequency scaling", "type": "Keyword", "challenge": "Highly specialized hardware and energy efficiency terminology."},
    {"q": "format obsolescence checksum integrity digital archives", "type": "Keyword", "challenge": "Niche archival and digital preservation concepts."},
    {"q": "algorithmic redlining facial recognition demographic parity", "type": "Keyword", "challenge": "Interdisciplinary concepts spanning AI ethics and sociology."},
    {"q": "What are the performance advantages of using an Entity Component System over object-oriented programming in game engines?", "type": "Natural Language", "challenge": "Long query with complex syntactic structure and comparative semantics."},
    {"q": "How did the transition from ARPANET to TCP/IP in 1983 change global network infrastructure?", "type": "Natural Language", "challenge": "Contains historical entities, dates, and requires relational understanding."},
    {"q": "What are the key differences between the EU AI Act and the US approach to artificial intelligence regulation?", "type": "Natural Language", "challenge": "Asks for a comparison between geopolitical entities and policy frameworks."},
    {"q": "How can remote satellite sensing be used to track the rate of Amazon rainforest deforestation?", "type": "Natural Language", "challenge": "Cross-domain query combining aerospace tech with environmental science."},
    {"q": "Why do many large open-source projects fail after the original creator steps down?", "type": "Natural Language", "challenge": "Subjective question requiring semantic understanding of community dynamics."},
    {"q": "engine performance", "type": "Ambiguous", "challenge": "Could refer to game engines, search engines, or physical car engines."},
    {"q": "node power", "type": "Ambiguous", "challenge": "Could mean computational graph nodes, network nodes, or hardware cluster power."},
    {"q": "web", "type": "Ambiguous", "challenge": "Extremely broad term; could refer to the WWW, spider webs, or data structures."},
    {"q": "fork", "type": "Ambiguous", "challenge": "Could refer to a GitHub fork, a Unix process fork, or a physical tool."},
    {"q": "auditing models", "type": "Ambiguous", "challenge": "Could be financial auditing models or AI fairness/bias auditing models."},
    {"q": "procedrual genration algorithsm for terrain", "type": "Noisy/Typo-heavy", "challenge": "Multiple spelling errors in key domain terms."},
    {"q": "ai biass and machne learnig farness", "type": "Noisy/Typo-heavy", "challenge": "Heavy typos in common machine learning terms."},
    {"q": "enviroment monitorng snsors water quality", "type": "Noisy/Typo-heavy", "challenge": "Dropped letters and misspelled keywords."},
    {"q": "histiry of tim berners lee wrold wide wbe", "type": "Noisy/Typo-heavy", "challenge": "Misspelled entities and core internet terms."},
    {"q": "how to presrve old digtal files from obsolecense", "type": "Noisy/Typo-heavy", "challenge": "Typo-heavy natural language query."}
]

def get_ground_truth(query):
    # To define a realistic ground truth, we pull top results from all 3 models and pool them.
    # We take the top 100 from each and pick the top 20 most frequent/highest ranked overall.
    models = ["bm25", "tfidf", "lm"]
    pool = {}
    for m in models:
        results = search(query, model=m, top_n=50)["results"]
        for rank, r in enumerate(results):
            if "doc_id" not in r or r["doc_id"] == -1: continue # Error or out of domain
            did = r["doc_id"]
            if did not in pool:
                pool[did] = {"score": 0, "title": r.get("title", "")}
            # Give points based on rank
            pool[did]["score"] += (50 - rank)
            
    # Sort by score and take top 20
    sorted_docs = sorted(pool.items(), key=lambda x: x[1]["score"], reverse=True)
    gt_ids = [d[0] for d in sorted_docs[:20]]
    return set(gt_ids), [pool[i]["title"] for i in gt_ids]

def evaluate(query_obj):
    q = query_obj["q"]
    gt_ids, gt_titles = get_ground_truth(q)
    
    metrics = {}
    models = ["bm25", "tfidf", "lm"]
    failure_cases = {}
    all_retrieved_docs = {}
    
    for m in models:
        results = search(q, model=m, top_n=10)["results"]
        retrieved_ids = [r.get("doc_id", -1) for r in results if r.get("doc_id", -1) != -1]
        
        # Store retrieved docs for output
        docs_info = []
        for rank, r in enumerate(results):
            did = r.get("doc_id", -1)
            is_rel = did in gt_ids
            rel_marker = "[REL]" if is_rel else "[NOT]"
            score = r.get("score", 0)
            docs_info.append(f"      {rank+1}. {rel_marker} (Score: {score:.4f}) {r.get('title', 'Unknown')}")
        all_retrieved_docs[m] = docs_info
        
        # Precision@10
        relevant_retrieved = [did for did in retrieved_ids if did in gt_ids]
        p10 = len(relevant_retrieved) / 10.0
        
        # Recall@10
        recall = len(relevant_retrieved) / max(1, len(gt_ids))
        
        # MAP@10
        ap = 0.0
        rel_count = 0
        for i, did in enumerate(retrieved_ids):
            if did in gt_ids:
                rel_count += 1
                ap += rel_count / (i + 1.0)
        ap /= max(1, len(gt_ids))
        
        metrics[m] = {"P@10": p10, "Recall@10": recall, "AP@10": ap}
        
        # Failure case: find a retrieved doc that is NOT relevant
        failure = "None"
        for r in results:
            if r.get("doc_id", -1) not in gt_ids and r.get("doc_id", -1) != -1:
                failure = f"'{r.get('title', 'Unknown')}' was retrieved but is not in the relevant set."
                break
        if failure == "None" and len(retrieved_ids) < 10:
            failure = "Model failed to retrieve enough relevant documents."
        elif failure == "None":
            failure = "No obvious failure in top 10 (all relevant)."
        failure_cases[m] = failure
        
    return gt_titles, metrics, failure_cases, all_retrieved_docs

with open("evaluation_results.txt", "w", encoding="utf-8") as f:
    f.write("IR System Evaluation Report\n")
    f.write("===========================\n\n")
    
    for i, qobj in enumerate(queries):
        print(f"Evaluating query {i+1}/20...")
        f.write(f"Query {i+1}: {qobj['q']}\n")
        f.write(f"Type: {qobj['type']}\n")
        f.write(f"Challenge Justification: {qobj['challenge']}\n")
        
        gt_titles, metrics, failures, retrieved_docs = evaluate(qobj)
        
        f.write(f"Relevant Document Set (n={len(gt_titles)}): \n")
        for title in gt_titles[:5]: # Print first 5 to save space
            f.write(f"  - {title}\n")
        if len(gt_titles) > 5:
            f.write(f"  - ... and {len(gt_titles) - 5} more.\n")
            
        f.write("\nMetrics & Retrieved Documents:\n")
        for m, mets in metrics.items():
            f.write(f"  Model: {m.upper()}\n")
            f.write(f"    Precision@10: {mets['P@10']:.2f}\n")
            f.write(f"    Recall@10:    {mets['Recall@10']:.2f}\n")
            f.write(f"    MAP@10:       {mets['AP@10']:.2f}\n")
            f.write(f"    Failure Case: {failures[m]}\n")
            f.write(f"    Retrieved Top 10:\n")
            if retrieved_docs[m]:
                for doc_str in retrieved_docs[m]:
                    f.write(f"{doc_str}\n")
            else:
                f.write("      No documents retrieved.\n")
            
        f.write("-" * 50 + "\n\n")

print("Evaluation complete. Results saved to evaluation_results.txt")
