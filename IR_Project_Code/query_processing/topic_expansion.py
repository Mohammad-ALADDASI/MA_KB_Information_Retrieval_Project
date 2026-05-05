import re
from difflib import SequenceMatcher

TOPIC_KEYWORDS = {
    "Artificial Intelligence": ["artificial intelligence", "ai", "intelligent systems", "neural networks", "neural network", "deep learning", "deep learn", "expert system", "knowledge graph"],
    "Machine Learning": ["machine learning", "ml", "supervised learning", "unsupervised learning", "learning algorithm", "model training", "classification", "regression", "clustering"],
    "Computer Vision": ["computer vision", "image recognition", "object detection", "image processing", "visual recognition", "video analysis", "computer sight"],
    "Natural Language Processing": ["natural language processing", "nlp", "text mining", "language models", "text classification", "sentiment analysis", "speech recognition", "machine translation"],
    "Data Science": ["data science", "data analysis", "data analytics", "statistical analysis", "predictive modeling", "big data analytics"],
    "Big Data": ["big data", "hadoop", "spark", "distributed computing", "data warehouse", "massive data", "large scale data", "petabyte", "exabyte"],
    "Cloud Computing": ["cloud computing", "cloud storage", "aws", "azure", "google cloud", "saas", "paas", "iaas", "serverless", "containerization", "docker", "kubernetes"],
    "Bioinformatics": ["bioinformatics", "genomics", "protein", "dna", "gene sequencing", "molecular biology", "biological data", "computational biology", "sequence analysis"],
    "Data Mining": ["data mining", "pattern discovery", "knowledge discovery", "association rules", "clustering", "classification algorithm", "anomaly detection"],
    "Cybersecurity": ["cybersecurity", "security", "encryption", "penetration testing", "malware detection", "network security", "data protection", "vulnerability", "threat detection", "information security"],
    "Internet of Things": ["internet of things", "iot", "smart devices", "sensor networks", "wireless sensor", "embedded systems", "iot platform", "connected devices"],
    "Blockchain Technology": ["blockchain", "cryptocurrency", "bitcoin", "ethereum", "distributed ledger", "smart contracts", "consensus algorithm", "decentralized", "ledger technology"]
}

def normalize(text: str) -> str:
    """Normalize text by removing extra spaces and converting to lowercase"""
    return re.sub(r"\s+", " ", text.lower().strip())

def fix_spacing_and_typos(text: str) -> str:
    """
    Fix common spacing issues and compound words
    e.g., 'LanguageProcessing' -> 'language processing'
    """
    text = text.lower()
    
    # Fix camelCase and PascalCase by inserting spaces
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    text = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', text)
    
    replacements = {
        'languageprocessing': 'language processing',
        'imagerecognition': 'image recognition',
        'deeplearning': 'deep learning',
        'neuralnetwork': 'neural network',
        'datamining': 'data mining',
        'dataanalysis': 'data analysis',
        'datascienc': 'data science',
        'machinelearning': 'machine learning',
        'artificalintelligenc': 'artificial intelligence',
        'computervision': 'computer vision',
        'textclassification': 'text classification',
        'sentimentanalysis': 'sentiment analysis',
        'bigdata': 'big data',
        'cloudcomputing': 'cloud computing',
        'cloudstora': 'cloud storage',
        'googlecloud': 'google cloud',
        'bioinformatic': 'bioinformatics',
        'proteinstructure': 'protein structure',
        'genesequencing': 'gene sequencing',
        'molecularbiology': 'molecular biology',
        'penetrationtest': 'penetration testing',
        'malwaredetection': 'malware detection',
        'networksecurity': 'network security',
        'dataprotection': 'data protection',
        'threatdetection': 'threat detection',
        'informationsecurity': 'information security',
        'internetofthings': 'internet of things',
        'smartdevices': 'smart devices',
        'sensornetwork': 'sensor networks',
        'embeddedsystem': 'embedded systems',
        'cryptocurrency': 'cryptocurrency',
        'distributedledger': 'distributed ledger',
        'smartcontract': 'smart contracts',
        'consensusalgorithm': 'consensus algorithm',
        'decentralized': 'decentralized',
    }
    
    for compound, expanded in replacements.items():
        text = text.replace(compound, expanded)
    
    text = re.sub(r"\s+", " ", text.strip())
    return text

def fuzzy_match(text: str, keywords: list, threshold: float = 0.75) -> bool:
    """
    Check if text fuzzy matches any keyword with threshold
    """
    text_normalized = normalize(text)
    for keyword in keywords:
        if keyword in text_normalized:
            return True
        
        ratio = SequenceMatcher(None, text_normalized, keyword).ratio()
        if ratio >= threshold:
            return True
        
        for word in text_normalized.split():
            if SequenceMatcher(None, word, keyword).ratio() >= 0.8:
                return True
    
    return False

def detect_topics(query: str):
    """
    Detect which corpus topics are relevant to the query
    Handles spelling mistakes, missing spaces, and typos
    """
    query_fixed = fix_spacing_and_typos(query)
    query_norm = normalize(query_fixed)
    
    detected = []
    for topic, keywords in TOPIC_KEYWORDS.items():
        for kw in keywords:
            if kw in query_norm:
                detected.append(topic)
                break
        
        if topic not in detected:
            if fuzzy_match(query_fixed, keywords, threshold=0.75):
                detected.append(topic)

    return list(set(detected))  

def expand_query_with_topics(query: str):
    """
    Expand query using detected topic terms
    """
    detected_topics = detect_topics(query)

    expanded_terms = []
    for topic in detected_topics:
        expanded_terms.extend(TOPIC_KEYWORDS.get(topic, []))

    expanded_terms = list(set(expanded_terms))

    if expanded_terms:
        expanded_query = query + " " + " ".join(expanded_terms)
    else:
        expanded_query = query

    return expanded_query, detected_topics
