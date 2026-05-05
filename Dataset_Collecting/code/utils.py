import re
import hashlib
from html import unescape

STOPWORDS_BASIC = {
    "the", "a", "an", "and", "or", "but", "if", "then", "than", "of", "on", "in",
    "to", "for", "with", "by", "at", "from", "as", "is", "are", "was", "were",
    "be", "been", "being", "this", "that", "these", "those", "it", "its"
}


def clean_text(text: str) -> str:
    if not text:
        return ""

    text = unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def word_count(text: str) -> int:
    return len(text.split()) if text else 0


def get_length_label(count: int) -> str:
    if count < 300:
        return "Short"
    if count > 2000:
        return "Long"
    return "Medium"


def normalize_url(url: str) -> str:
    if not url:
        return ""
    return url.split("#")[0].strip()


def build_doc_id(source: str, theme: str, title: str, url: str) -> str:
    raw = f"{source}|{theme}|{title}|{url}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest()


def make_record(source: str, theme: str, title: str, text: str, url: str) -> dict:
    title = clean_text(title)
    text = clean_text(text)
    url = normalize_url(url)

    count = word_count(text)

    return {
        "doc_id": build_doc_id(source, theme, title, url),
        "source": source,
        "theme": theme,
        "title": title,
        "text": text,
        "url": url,
        "word_count": count,
        "length_type": get_length_label(count),
    }


def is_valid_record(record: dict, min_words: int = 80, max_words: int = 15000) -> bool:
    if not record["title"] or not record["text"] or not record["url"]:
        return False
    if record["word_count"] < min_words:
        return False
    if record["word_count"] > max_words:
        return False
    return True