from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "heterogeneous_corpus.csv"

# 8 technical themes derived from your 4 umbrella areas
THEMES = {
    "Green Computing": [
        "green computing",
        "energy efficient computing",
        "sustainable software",
        "low-power systems"
    ],
    "Environmental Monitoring Systems": [
        "environmental monitoring technology",
        "climate data platforms",
        "smart environmental sensors",
        "sustainability monitoring systems"
    ],
    "History of the Internet and Web": [
        "history of the internet",
        "history of the world wide web",
        "web evolution",
        "internet architecture history"
    ],
    "Open Source and Software Evolution": [
        "history of open source software",
        "software evolution",
        "open source ecosystems",
        "version control history"
    ],
    "AI Bias and Fairness": [
        "AI bias",
        "fair machine learning",
        "algorithmic fairness",
        "bias in artificial intelligence"
    ],
    "AI Governance and Responsible AI": [
        "responsible AI",
        "AI governance",
        "AI accountability",
        "AI transparency"
    ],
    "Digital Preservation Systems": [
        "digital preservation systems",
        "digital archives technology",
        "metadata preservation",
        "cultural heritage digitization"
    ],
    "Palestinian Digital Heritage": [
        "Palestinian digital archives",
        "Palestinian cultural heritage digitization",
        "digital preservation of Palestinian history",
        "Palestinian archive technology"
    ],
}

SOURCE_LIMITS = {
    "arxiv": 12,
    "wikipedia": 4,
    "github": 8,
    "stackexchange": 8,
    "web": 8,
}

MIN_WORDS = 80
MAX_WORDS = 15000

USER_AGENT = "HeterogeneousCorpusBuilder/1.0"