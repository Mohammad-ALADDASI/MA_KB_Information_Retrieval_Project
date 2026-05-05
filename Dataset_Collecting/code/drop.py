import pandas as pd

df=pd.read_csv("output\heterogeneous_corpus.csv")
df = df[df["theme"] != "Palestinian Digital Heritage"]
df.to_csv("output/heterogeneous_corpus_clean.csv", index=False)