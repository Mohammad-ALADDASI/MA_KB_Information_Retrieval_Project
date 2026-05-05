"""Rebuild the full search corpus and indexes from data/raw/input.csv."""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

commands = [
    [sys.executable, "preprocessing/build_corpus.py"],
    [sys.executable, "indexing/build_bm25.py"],
    [sys.executable, "indexing/build_tfidf.py"],
    [sys.executable, "indexing/build_lm.py"],
]

for cmd in commands:
    print("\n$", " ".join(cmd))
    subprocess.run(cmd, cwd=ROOT, check=True)

print("\nDone. Now run: python app.py")
