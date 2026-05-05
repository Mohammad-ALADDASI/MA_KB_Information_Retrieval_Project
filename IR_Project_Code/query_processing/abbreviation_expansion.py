"""
Abbreviation Expansion Module
Expands common abbreviations in AI/ML/CS domain
"""

import re

# Comprehensive abbreviation mappings
ABBREVIATIONS = {
    # AI & ML
    "ai": "artificial intelligence",
    "ml": "machine learning",
    "dl": "deep learning",
    "nn": "neural network",
    "cnn": "convolutional neural network",
    "rnn": "recurrent neural network",
    "lstm": "long short term memory",
    "gru": "gated recurrent unit",
    "gan": "generative adversarial network",
    "vae": "variational autoencoder",
    "rl": "reinforcement learning",
    "drl": "deep reinforcement learning",
    "dqn": "deep q network",
    
    # NLP
    "nlp": "natural language processing",
    "bert": "bidirectional encoder representations from transformers",
    "gpt": "generative pre-trained transformer",
    "ner": "named entity recognition",
    "pos": "part of speech",
    "lm": "language model",
    "tts": "text to speech",
    "asr": "automatic speech recognition",
    "mt": "machine translation",
    "nmt": "neural machine translation",
    
    # Computer Vision
    "cv": "computer vision",
    "ocr": "optical character recognition",
    "yolo": "you only look once",
    "rcnn": "region based convolutional neural network",
    "ssd": "single shot detector",
    "fcn": "fully convolutional network",
    "unet": "u-net",
    
    # Data Science
    "ds": "data science",
    "da": "data analysis",
    "eda": "exploratory data analysis",
    "etl": "extract transform load",
    "knn": "k nearest neighbors",
    "svm": "support vector machine",
    "dt": "decision tree",
    "rf": "random forest",
    "gbm": "gradient boosting machine",
    "xgb": "extreme gradient boosting",
    "pca": "principal component analysis",
    "ica": "independent component analysis",
    "lda": "latent dirichlet allocation",
    "svd": "singular value decomposition",
    
    # Optimization & Training
    "sgd": "stochastic gradient descent",
    "adam": "adaptive moment estimation",
    "rmsprop": "root mean square propagation",
    "mse": "mean squared error",
    "mae": "mean absolute error",
    "rmse": "root mean squared error",
    "auc": "area under curve",
    "roc": "receiver operating characteristic",
    "map": "mean average precision",
    
    # Big Data & Cloud
    "aws": "amazon web services",
    "gcp": "google cloud platform",
    "api": "application programming interface",
    "rest": "representational state transfer",
    "sql": "structured query language",
    "nosql": "not only sql",
    "hdfs": "hadoop distributed file system",
    "mapreduce": "map reduce",
    
    # Security & Network
    "ssl": "secure sockets layer",
    "tls": "transport layer security",
    "vpn": "virtual private network",
    "ids": "intrusion detection system",
    "ips": "intrusion prevention system",
    "ddos": "distributed denial of service",
    
    # IoT & Hardware
    "iot": "internet of things",
    "gpu": "graphics processing unit",
    "cpu": "central processing unit",
    "tpu": "tensor processing unit",
    "fpga": "field programmable gate array",
    "asic": "application specific integrated circuit",
    
    # Metrics & Measures
    "f1": "f1 score",
    "ap": "average precision",
    "iou": "intersection over union",
    "fps": "frames per second",
    "flops": "floating point operations per second",
    
    # Standards & Formats
    "json": "javascript object notation",
    "xml": "extensible markup language",
    "yaml": "yaml ain't markup language",
    "csv": "comma separated values",
    "html": "hypertext markup language",
    "http": "hypertext transfer protocol",
    "https": "hypertext transfer protocol secure",
    "ftp": "file transfer protocol",
    
    # Blockchain & Crypto
    "btc": "bitcoin",
    "eth": "ethereum",
    "nft": "non fungible token",
    "dao": "decentralized autonomous organization",
    "defi": "decentralized finance",
    
    # Additional
    "ui": "user interface",
    "ux": "user experience",
    "ci": "continuous integration",
    "cd": "continuous deployment",
    "devops": "development operations",
    "mlops": "machine learning operations",
    "saas": "software as a service",
    "paas": "platform as a service",
    "iaas": "infrastructure as a service",
}


def expand_abbreviations(query: str) -> str:
    """
    Expand abbreviations in query while preserving original terms.
    Example: "ml algorithms" -> "ml machine learning algorithms"
    
    Args:
        query: Input query string
        
    Returns:
        Query with abbreviations expanded (both forms included)
    """
    if not query:
        return ""
    
    query_lower = query.lower()
    tokens = query_lower.split()
    
    expanded_terms = []
    
    for token in tokens:
        clean_token = re.sub(r'[^\w]', '', token)
        
        if clean_token in ABBREVIATIONS:
            expansion = ABBREVIATIONS[clean_token]
            expanded_terms.append(f"{clean_token} {expansion}")
        else:
            expanded_terms.append(clean_token)
    
    return " ".join(expanded_terms)


def get_expansion(abbreviation: str) -> str:
    """
    Get the expansion for a single abbreviation.
    
    Args:
        abbreviation: The abbreviation to expand
        
    Returns:
        Expanded form or original if not found
    """
    abbr_lower = abbreviation.lower().strip()
    return ABBREVIATIONS.get(abbr_lower, abbreviation)


def detect_abbreviations(query: str) -> dict:
    """
    Detect all abbreviations in a query.
    
    Args:
        query: Input query string
        
    Returns:
        Dictionary mapping found abbreviations to their expansions
    """
    query_lower = query.lower()
    tokens = query_lower.split()
    
    detected = {}
    for token in tokens:
        clean_token = re.sub(r'[^\w]', '', token)
        if clean_token in ABBREVIATIONS:
            detected[clean_token] = ABBREVIATIONS[clean_token]
    
    return detected


if __name__ == "__main__":
    test_queries = [
        "ml classification",
        "cnn for cv",
        "nlp with bert and gpt",
        "rl algorithms",
        "ai and ml techniques"
    ]
    
    print("=" * 60)
    print("ABBREVIATION EXPANSION TESTS")
    print("=" * 60)
    
    for query in test_queries:
        expanded = expand_abbreviations(query)
        detected = detect_abbreviations(query)
        
        print(f"\nOriginal: {query}")
        print(f"Expanded: {expanded}")
        if detected:
            print(f"Detected: {detected}")