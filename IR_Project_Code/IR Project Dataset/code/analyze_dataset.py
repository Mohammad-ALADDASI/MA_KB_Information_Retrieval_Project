from pathlib import Path

import pandas as pd

from config import OUTPUT_FILE


def safe_divide(a: float, b: float) -> float:
    return a / b if b else 0.0


def load_dataset(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"Dataset not found: {csv_path}")
    return pd.read_csv(csv_path, encoding="utf-8-sig")


def print_basic_info(df: pd.DataFrame) -> None:
    print("\n=== BASIC INFO ===")
    print(f"Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")

    if "source" in df.columns:
        print("\nSource distribution:")
        print(df["source"].value_counts())

    if "theme" in df.columns:
        print("\nTheme distribution:")
        print(df["theme"].value_counts())

    if "length_type" in df.columns:
        print("\nLength distribution:")
        print(df["length_type"].value_counts())


def print_length_stats(df: pd.DataFrame) -> None:
    if "word_count" not in df.columns:
        print("\nNo word_count column found.")
        return

    print("\n=== LENGTH STATS ===")
    print(f"Average document length: {df['word_count'].mean():.2f} words")

    if "theme" in df.columns:
        print("\nAverage document length per topic:")
        print(df.groupby("theme")["word_count"].mean().sort_values(ascending=False))


def build_vocabulary_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Lightweight vocabulary stats:
    - total tokens
    - unique tokens
    - token ratio = unique / total
    """
    rows = []

    for theme, group in df.groupby("theme"):
        all_text = " ".join(group["text"].fillna("").astype(str)).lower()
        tokens = [tok for tok in all_text.split() if tok.strip()]

        total_tokens = len(tokens)
        unique_tokens = len(set(tokens))
        token_ratio = safe_divide(unique_tokens, total_tokens)

        rows.append({
            "theme": theme,
            "total_tokens": total_tokens,
            "unique_tokens": unique_tokens,
            "token_ratio": token_ratio,
        })

    return pd.DataFrame(rows).sort_values("theme")


def build_stopword_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Placeholder stopword stats using a small built-in list.
    Later we can improve this with NLTK or spaCy if you want.
    """
    stopwords_basic = {
        "the", "a", "an", "and", "or", "but", "if", "then", "than", "of", "on", "in",
        "to", "for", "with", "by", "at", "from", "as", "is", "are", "was", "were",
        "be", "been", "being", "this", "that", "these", "those", "it", "its"
    }

    rows = []

    for theme, group in df.groupby("theme"):
        all_text = " ".join(group["text"].fillna("").astype(str)).lower()
        tokens = [tok.strip(".,!?;:()[]{}\"'") for tok in all_text.split()]
        tokens = [tok for tok in tokens if tok]

        total_tokens = len(tokens)
        stopword_tokens = sum(1 for tok in tokens if tok in stopwords_basic)
        stopword_pct = safe_divide(stopword_tokens, total_tokens) * 100

        rows.append({
            "theme": theme,
            "total_tokens": total_tokens,
            "stopword_tokens": stopword_tokens,
            "stopword_percentage": stopword_pct,
        })

    return pd.DataFrame(rows).sort_values("theme")


def build_lexical_overlap(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes lexical overlap between topics:
    overlap(A,B) = |V(A) ∩ V(B)| / |V(A) ∪ V(B)| * 100
    """
    theme_vocab = {}

    for theme, group in df.groupby("theme"):
        all_text = " ".join(group["text"].fillna("").astype(str)).lower()
        vocab = set(tok.strip(".,!?;:()[]{}\"'") for tok in all_text.split())
        vocab = {tok for tok in vocab if tok}
        theme_vocab[theme] = vocab

    themes = sorted(theme_vocab.keys())
    matrix = []

    for theme_a in themes:
        row = {"theme": theme_a}
        vocab_a = theme_vocab[theme_a]

        for theme_b in themes:
            vocab_b = theme_vocab[theme_b]
            union = vocab_a | vocab_b
            inter = vocab_a & vocab_b
            overlap = safe_divide(len(inter), len(union)) * 100
            row[theme_b] = overlap

        matrix.append(row)

    return pd.DataFrame(matrix)


def main() -> None:
    df = load_dataset(OUTPUT_FILE)

    print_basic_info(df)
    print_length_stats(df)

    vocab_stats = build_vocabulary_stats(df)
    stopword_stats = build_stopword_stats(df)
    overlap_df = build_lexical_overlap(df)

    print("\n=== VOCABULARY STATS ===")
    print(vocab_stats.to_string(index=False))

    print("\n=== STOPWORD STATS ===")
    print(stopword_stats.to_string(index=False))

    print("\n=== LEXICAL OVERLAP (%) ===")
    print(overlap_df.to_string(index=False))

    # Save analysis tables
    analysis_dir = OUTPUT_FILE.parent
    vocab_stats.to_csv(analysis_dir / "vocabulary_stats.csv", index=False, encoding="utf-8-sig")
    stopword_stats.to_csv(analysis_dir / "stopword_stats.csv", index=False, encoding="utf-8-sig")
    overlap_df.to_csv(analysis_dir / "lexical_overlap.csv", index=False, encoding="utf-8-sig")

    print(f"\nSaved analysis tables to: {analysis_dir}")


if __name__ == "__main__":
    main()