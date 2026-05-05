import re
from difflib import SequenceMatcher

try:
    from query_processing.abbreviation_expansion import expand_abbreviations
except ImportError:
    def expand_abbreviations(text: str) -> str:
        return text


TOPIC_KEYWORDS = {
    "Game Engine Architecture": [
        "game", "games", "gaming", "video game", "video games",
        "game engine", "game engines", "engine architecture",
        "game architecture", "software architecture",
        "2d game", "3d game", "flappy bird",
        "gameplay", "game mechanics", "game design",
        "graphics", "rendering", "graphics engine", "rendering engine",
        "physics engine", "audio engine", "input system",
        "game subsystem", "world editor", "unity", "unreal",
        "godot", "cocos2dx", "urho3d", "architecture recovery",
        "subsystem", "subsystems", "coupling", "components",
        "maintainability", "software evolution"
    ],

    "Procedural Content Generation": [
        "procedural content generation", "pcg", "content generation",
        "procedural generation", "map generation", "level generation",
        "terrain generation", "heightmap", "heightmaps",
        "game map", "strategy game", "strategy games",
        "generative", "generator", "gan", "gans",
        "generative adversarial network",
        "generative adversarial networks",
        "random generation", "automatic generation",
        "game content", "synthetic content", "creative ai",
        "asset generation", "layout generation"
    ],

    "IoT Sensors and Actuators": [
        "iot", "internet of things", "sensor", "sensors",
        "actuator", "actuators", "smart device", "smart devices",
        "embedded system", "embedded systems",
        "wireless sensor", "wireless sensors",
        "sensor network", "sensor networks",
        "edge device", "edge devices", "edge computing",
        "fog computing", "microcontroller", "arduino",
        "raspberry pi", "mqtt", "rfid", "zigbee",
        "bluetooth", "low power", "smart home",
        "smart city", "cyber physical system",
        "cyber physical systems", "monitoring device",
        "environment sensor", "temperature sensor",
        "humidity sensor", "pressure sensor"
    ],

    "IoT Security and Privacy": [
        "iot security", "iot privacy", "security", "privacy",
        "cybersecurity", "network security", "data protection",
        "authentication", "authorization", "encryption",
        "secure communication", "secure protocol",
        "attack", "attacks", "threat", "threats",
        "vulnerability", "vulnerabilities", "malware",
        "intrusion detection", "anomaly detection",
        "device security", "firmware security",
        "privacy preserving", "access control",
        "botnet", "ddos", "risk", "trust",
        "secure iot", "privacy risk", "data leakage"
    ],

    "Green Computing": [
        "green computing", "sustainable computing",
        "energy efficient", "energy efficiency",
        "power consumption", "energy consumption",
        "carbon footprint", "carbon emissions",
        "sustainability", "sustainable", "green it",
        "data center energy", "energy aware",
        "low power", "power management",
        "renewable energy", "resource efficiency",
        "environmental impact", "eco friendly",
        "green cloud", "green software",
        "hardware efficiency", "energy optimization"
    ],

    "Environmental Monitoring Systems": [
        "environmental monitoring", "monitoring system",
        "monitoring systems", "environmental sensor",
        "environmental sensors", "pollution monitoring",
        "air quality", "water quality", "soil monitoring",
        "climate monitoring", "weather monitoring",
        "temperature monitoring", "humidity monitoring",
        "remote sensing", "sensor deployment",
        "environment data", "environmental data",
        "ecological monitoring", "smart agriculture",
        "disaster monitoring", "forest monitoring",
        "greenhouse monitoring", "real time monitoring"
    ],

    "History of the Internet and Web": [
        "internet", "web", "world wide web", "www",
        "history of the internet", "history of the web",
        "arpanet", "tcp", "ip", "tcp ip", "http",
        "html", "url", "browser", "web browser",
        "website", "webpage", "web page",
        "search engine", "email", "domain name",
        "dns", "web server", "client server",
        "hypertext", "tim berners lee",
        "internet protocol", "packet switching",
        "early internet", "web evolution",
        "social web", "web 1", "web 2", "web 3"
    ],

    "Open Source and Software Evolution": [
        "open source", "opensource", "software evolution",
        "software maintenance", "software repository",
        "github", "git", "version control",
        "commit", "commits", "pull request",
        "issue tracker", "bug report", "bug fix",
        "software project", "software development",
        "developer", "developers", "community",
        "collaboration", "license", "licensing",
        "free software", "fork", "forking",
        "code reuse", "code quality", "technical debt",
        "software ecosystem", "package manager",
        "dependency", "dependencies", "release",
        "software engineering"
    ],

    "AI Bias and Fairness": [
        "ai bias", "bias", "algorithmic bias",
        "fairness", "ai fairness", "machine learning fairness",
        "discrimination", "ethical ai", "ethics",
        "responsible ai", "bias detection",
        "bias mitigation", "fair machine learning",
        "model fairness", "dataset bias",
        "training data bias", "representational bias",
        "gender bias", "racial bias", "social bias",
        "equity", "accountability", "transparency",
        "explainability", "interpretability",
        "harm", "harms", "unfairness"
    ],

    "AI Governance and Responsible AI": [
        "ai governance", "responsible ai", "ai regulation",
        "ai policy", "ai ethics", "ethical ai",
        "ai safety", "ai accountability",
        "ai transparency", "ai auditing",
        "model governance", "risk management",
        "trustworthy ai", "human centered ai",
        "human centric ai", "ai compliance",
        "ai standards", "ai law", "ai oversight",
        "algorithmic accountability",
        "governance framework", "responsible innovation",
        "fairness", "privacy", "security",
        "explainability", "interpretability"
    ],

    "Digital Preservation Systems": [
        "digital preservation", "preservation system",
        "digital archive", "digital archives",
        "archiving", "archive", "archives",
        "long term preservation", "data preservation",
        "document preservation", "metadata",
        "digital library", "repository",
        "institutional repository", "file format",
        "format migration", "emulation",
        "digital curation", "records management",
        "information preservation", "web archive",
        "web archiving", "backup", "storage",
        "digital heritage", "accessibility",
        "preservation metadata"
    ],

    "General Artificial Intelligence and Machine Learning": [
        "artificial intelligence", "ai", "machine learning",
        "ml", "deep learning", "neural network",
        "neural networks", "reinforcement learning",
        "rl", "q learning", "deep q learning",
        "classification", "regression", "clustering",
        "prediction", "training", "inference",
        "model", "models", "dataset", "datasets",
        "algorithm", "algorithms", "optimization",
        "agent", "agents", "autonomous"
    ],

    "General Computer Science and Systems": [
        "computer science", "computing", "system",
        "systems", "architecture", "network",
        "networks", "database", "data",
        "software", "hardware", "programming",
        "application", "applications", "framework",
        "platform", "performance", "scalability",
        "distributed", "cloud", "edge", "security",
        "privacy", "algorithm", "model"
    ]
}


COMMON_FIXES = {
    "internetofthings": "internet of things",
    "iotsensors": "iot sensors",
    "iotsecurity": "iot security",
    "iotprivacy": "iot privacy",
    "greencomputing": "green computing",
    "environmentalmonitoring": "environmental monitoring",
    "historyoftheinternet": "history of the internet",
    "historyoftheweb": "history of the web",
    "opensource": "open source",
    "softwareevolution": "software evolution",
    "aibias": "ai bias",
    "aifairness": "ai fairness",
    "aigovernance": "ai governance",
    "responsibleai": "responsible ai",
    "digitalpreservation": "digital preservation",
    "gameengine": "game engine",
    "gameengines": "game engines",
    "gamearchitecture": "game architecture",
    "proceduralcontentgeneration": "procedural content generation",
    "contentgeneration": "content generation",
    "machinelearning": "machine learning",
    "deeplearning": "deep learning",
    "neuralnetwork": "neural network",
    "reinforcementlearning": "reinforcement learning",
    "computerscience": "computer science",
    "cybersecurity": "cybersecurity",
    "datascience": "data science",
    "worldwideweb": "world wide web",
    "tcpip": "tcp ip",
}


def normalize(text: str) -> str:
    if not text:
        return ""

    text = str(text).lower()
    text = text.replace("-", " ")
    text = text.replace("_", " ")
    text = text.replace("/", " ")
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def fix_spacing_and_typos(text: str) -> str:
    if not text:
        return ""

    text = str(text)
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
    text = normalize(text)

    compact = text.replace(" ", "")

    for wrong, correct in COMMON_FIXES.items():
        compact = compact.replace(wrong, correct.replace(" ", ""))

    text = compact

    for wrong, correct in COMMON_FIXES.items():
        text = text.replace(wrong, correct)

    return normalize(text)


def keyword_match(query: str, keyword: str) -> bool:
    query = normalize(query)
    keyword = normalize(keyword)

    if not query or not keyword:
        return False

    if " " in keyword:
        return keyword in query

    return re.search(rf"\b{re.escape(keyword)}\b", query) is not None


def fuzzy_match(query: str, keywords: list[str], threshold: float = 0.82) -> bool:
    query = normalize(query)
    words = query.split()

    for keyword in keywords:
        keyword_norm = normalize(keyword)

        if keyword_match(query, keyword_norm):
            return True

        if len(keyword_norm.split()) > 1:
            ratio = SequenceMatcher(None, query, keyword_norm).ratio()
            if ratio >= threshold:
                return True

        if len(keyword_norm) >= 5:
            for word in words:
                if len(word) >= 5:
                    ratio = SequenceMatcher(None, word, keyword_norm).ratio()
                    if ratio >= threshold:
                        return True

    return False


def detect_topics(query: str) -> list[str]:
    if not query:
        return []

    expanded_query = expand_abbreviations(query)
    fixed_query = fix_spacing_and_typos(expanded_query)

    detected = []

    for topic, keywords in TOPIC_KEYWORDS.items():
        exact_found = any(keyword_match(fixed_query, kw) for kw in keywords)

        if exact_found:
            detected.append(topic)
            continue

        fuzzy_found = fuzzy_match(fixed_query, keywords)

        if fuzzy_found:
            detected.append(topic)

    return sorted(set(detected))


def expand_query_with_topics(query: str) -> tuple[str, list[str]]:
    detected_topics = detect_topics(query)

    expansion_terms = []
    for topic in detected_topics:
        expansion_terms.extend(TOPIC_KEYWORDS.get(topic, []))

    expansion_terms = sorted(set(expansion_terms))

    if expansion_terms:
        expanded_query = f"{query} {' '.join(expansion_terms)}"
    else:
        expanded_query = query

    return expanded_query, detected_topics


def is_query_in_domain(query: str) -> bool:
    """
    IMPORTANT:
    This intentionally returns True for every non-empty query.

    Reason:
    The retrieval system should not reject searches just because
    the domain keyword list missed a word. The keyword list is used
    for topic detection and query expansion only.
    """
    return bool(query and query.strip())


def get_domain_confidence(query: str) -> float:
    detected_topics = detect_topics(query)

    if not query or not query.strip():
        return 0.0

    if not detected_topics:
        return 0.25

    confidence = len(detected_topics) / max(len(TOPIC_KEYWORDS), 1)
    return min(max(confidence, 0.35), 1.0)


def get_all_domain_keywords() -> list[str]:
    all_keywords = []

    for keywords in TOPIC_KEYWORDS.values():
        all_keywords.extend(keywords)

    return sorted(set(all_keywords))


def explain_domain_match(query: str) -> dict:
    detected_topics = detect_topics(query)

    return {
        "query": query,
        "normalized_query": fix_spacing_and_typos(expand_abbreviations(query)),
        "in_domain": is_query_in_domain(query),
        "confidence": get_domain_confidence(query),
        "detected_topics": detected_topics,
    }