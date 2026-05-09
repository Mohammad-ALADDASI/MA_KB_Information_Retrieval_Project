# 🔍 Heterogeneous Information Retrieval System

This video presents our Information Retrieval (IR) system developed using BM25, TF-IDF, and Language Models (LM), enhanced with Large Language Model (LLM) augmentation techniques such as query rewriting, query expansion, result summarization, and ranking explanation. The project demonstrates preprocessing, indexing, retrieval, evaluation, and a Flask-based user interface with support for keyword, natural language, ambiguous, and phrase queries. The system was evaluated using Precision@10, Recall@10, and MAP@10 to compare the effectiveness of classical retrieval methods and LLM-enhanced retrieval approaches. 

Timeline:
00:00 - 00:20 → Introduction
00:20 - 00:55 → Project Overview & Dataset
00:55 - 01:35 → Code Structure Explanation
01:35 - 02:10 → Retrieval Models (BM25, TF-IDF, LM)
02:10 - 02:45 → Interface Features & LLM Options
02:45 - 03:10 → Keyword Query Demo
03:10 - 03:35 → Natural Language Query Demo
03:35 - 03:55 → Ambiguous Query Demo
03:55 - 04:15 → Phrase Query Demo
04:15 - 04:40 → LLM-Augmented Query Demo
04:40 - 05:00 → Evaluation Results & Conclusion
![Demo Video ]([https://youtu.be/UDegcQr1-iA])(https://youtu.be/0NNBWFSb85w))

## 📌 Project Overview

This project implements a **complete Information Retrieval (IR) system pipeline** under realistic conditions. It is divided into three milestones:

1. **Data Collection & Analysis**
2. **Retrieval System & Experimental Evaluation**
3. **LLM-Augmented Retrieval**

The goal is to simulate real-world search environments by combining **heterogeneous data sources**, implementing **multiple retrieval models**, and enhancing them with **Large Language Models (LLMs)**.

---

# 📂 Project Structure

```bash
project/
├── data/
│   ├── raw/
│   │   └── heterogeneous_corpus.csv
│   └── processed/
│       ├── corpus_clean.json
│       ├── bm25_index.pkl
│       ├── tfidf_index.pkl
│       ├── lm_stats.pkl
│       └── doc_mapping.pkl
│
├── src/
│   ├── retrieval/
│   │   ├── bm25.py
│   │   ├── tfidf.py
│   │   ├── lm.py
│   │   └── retrieve.py
│   │
│   ├── preprocessing/
│   │   ├── clean_text.py
│   │   ├── build_corpus.py
│   │   └── tokenizer.py
│   │
│   ├── query_processing/
│   │   ├── domain_check.py
│   │   ├── spell_correction.py
│   │   ├── abbreviation_expansion.py
│   │   └── query_expansion.py
│   │
│   ├── evaluation/
│   │   └── run_experiments.py
│   │
│   └── llm/
│       ├── query_rewriting.py
│       └── query_expansion_llm.py
│
├── gui/
│   ├── app.py
│   ├── templates/
│   │   ├── base.html
│   │   └── index.html
│   │   └── static/
│
├── queries/
│   └── evaluation_queries.json
│
├── analysis/
│   ├── vocabulary_stats.csv
│   ├── stopword_stats.csv
│   └── lexical_overlap.csv
│
├── reports/
│   └── final_report.pdf
│
├── rebuild_indexes.py
├── requirements.txt
└── README.md
```

---

# 🧩 Milestone 1: Data Collection & Analysis (8 Points)

## 📊 Dataset Description

A **heterogeneous corpus of 500 documents** was constructed from multiple sources to simulate real-world retrieval scenarios.

### ✅ Requirements Satisfied

* ✔ At least **500 documents**
* ✔ At least **4 content types**
* ✔ At least **8 technical themes**
* ✔ Includes:

  * Short (<300 words)
  * Medium
  * Long (>2000 words)
* ✔ Each document contains:

  * Title
  * Text
  * URL

---

## 🌐 Data Sources

* arXiv (research paper abstracts)
* Wikipedia (encyclopedic articles)
* GitHub (README files)
* StackExchange (Q&A discussions)
* Web Articles (technical blogs & institutional content)

---

## 🧠 Themes Covered

* AI Bias and Fairness
* AI Governance and Responsible AI
* Open Source and Software Evolution
* Green Computing
* Environmental Monitoring Systems
* Digital Preservation Systems
* History of the Internet and Web
* IoT Security and Privacy
* IoT Sensors and Actuators
* Game Engine Architecture
* Procedural Content Generation

---

## 📈 Dataset Analysis

The dataset was analyzed before preprocessing to compute:

* Document distribution by:

  * Source
  * Theme
  * Length
* Average document length (overall + per topic)
* Vocabulary statistics:

  * Token ratio per topic
  * Stopword percentage per topic
  * Lexical overlap between topics

📄 See: `reports/milestone1_report.pdf`

---

# ⚙️ Milestone 2: Retrieval System & Experimental Framework (12 Points)

## 🖥️ System Features

A **GUI-based search system** was developed with:

* 🔎 Search box
* 📊 Retrieval model selector (dropdown)
* 📄 Top-10 ranked results:

  * Title
  * URL
  * Snippet (~200 characters)
  * Ranking score

---

## 🔍 Retrieval Models Implemented

* Vector Space Model (TF-IDF)
* BM25
* Embedding-based retrieval (semantic search)

---

## 🧠 Query Handling Features

* ✔ Spelling Correction
* ✔ Abbreviation Expansion (e.g., AI → Artificial Intelligence)
* ✔ Case Insensitivity
* ✔ Phrase Matching ("exact phrases")

---

## 🧪 Experimental Setup

### Query Design (20 Queries)

| Type                 | Count |
| -------------------- | ----- |
| Keyword Queries      | 5     |
| Natural Language     | 5     |
| Ambiguous Queries    | 5     |
| Noisy / Typo Queries | 5     |

Each query includes:

* Justification of difficulty
* Ground-truth relevant documents (≥20)

---

## 📏 Evaluation Metrics

* Precision@10
* Recall
* Mean Average Precision (MAP)

### 📊 Analysis Includes:

* Model comparison per topic
* Performance comparison across query types
* At least **one failure case per model**

📄 See: `reports/milestone2_report.pdf`

🎥 Demo Video (≤5 min): Included in submission

---

# 🤖 Milestone 3: LLM-Augmented Retrieval (10 Points)

## 🚀 Enhancements Using LLMs

Two LLM-based strategies were implemented:

### 1. Query Rewriting

* Reformulates user queries into clearer, structured versions

### 2. Query Expansion

* Adds related terms and synonyms to improve recall

---

## 🔍 Optional Enhancements (if implemented)

* Result Summarization
* Ranking Explanation

---

## 📊 Evaluation

A qualitative analysis was conducted to assess LLM impact:

### ✔ Cases where LLM improved:

* Better semantic understanding
* Improved recall for vague queries

### ❌ Cases where LLM hurt:

* Over-expansion introducing noise
* Query drift affecting precision

📄 See: `reports/milestone3_report.pdf`

---

# 🧪 Analysis Outputs

Located in `/analysis/`:

* `vocabulary_stats.csv`
* `stopword_stats.csv`
* `lexical_overlap.csv`

These provide insights into:

* Linguistic diversity
* Stopword usage
* Cross-topic similarity

---

# ▶️ How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the GUI

```bash
python gui/app.py
```

### 3. Run retrieval experiments

```bash
python src/evaluation/run_experiments.py
```

---

# 🎯 Intended Use

This project is designed for:

* Information Retrieval research
* NLP experimentation
* Search system evaluation
* Educational purposes

---

# ⚖️ License & Ethics

* All data collected from publicly accessible sources
* Only textual content and URLs stored
* Users should refer to original sources for attribution

---

# 👩‍💻 Authors

This project was developed as part of a university course:

**Information Retrieval and Text Analysis**

---

# 📅 Deadlines

| Milestone          | Deadline     |
| ------------------ | ------------ |
| Milestone 1        | 21/3/2026    |
| Milestone 2        | 25/4/2026    |
| Milestone 3        | 9/5/2026     |
| Project Discussion | 10–21/5/2026 |

---
