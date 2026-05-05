from query_processing.spell_correction import add_to_vocab

DOC_MAPPING = {}

def initialize_index(documents):
    """
    Initialize the document mapping and build vocabularies.
     Call this after loading all documents.
    """
    global DOC_MAPPING

    for i, doc in enumerate(documents):
        DOC_MAPPING[i] = {
            "doc_id": i,
            "title": doc["title"],
            "url": doc["url"],
            "topic": doc["topic"],
            "clean_title": doc["clean_title"],
            "clean_summary": doc["clean_summary"],
            "clean_content": doc["clean_content"]
        }

    all_words = []
    for doc in DOC_MAPPING.values():
        if doc.get("clean_content"):
            all_words.extend(doc["clean_content"].split())
        if doc.get("clean_title"):
            all_words.extend(doc["clean_title"].split())
        if doc.get("clean_summary"):
            all_words.extend(doc["clean_summary"].split())
    
    add_to_vocab(all_words)
    
    print(f"✅ Initialized index with {len(DOC_MAPPING)} documents")
    print(f"✅ Built vocabulary with {len(set(all_words))} unique words")

    return DOC_MAPPING