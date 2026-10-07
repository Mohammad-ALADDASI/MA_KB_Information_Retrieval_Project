# 🔍 Heterogeneous Information Retrieval System

> A complete Information Retrieval system combining **BM25**, **TF-IDF**, and **Language Model retrieval** with query processing, dataset analysis, experimental evaluation, and optional **LLM-augmented search**.

This project was developed as part of a university **Information Retrieval and Text Analysis** course. It explores the complete lifecycle of a search system: collecting a heterogeneous corpus, preprocessing and indexing documents, processing user queries, ranking results with multiple retrieval models, evaluating retrieval effectiveness, and enhancing search using Large Language Models.

The system includes a **Flask-based web interface** supporting keyword queries, natural-language queries, ambiguous queries, typo-heavy queries, and exact phrase search.

---

## 🌟 Project Highlights

- 📚 **500-document heterogeneous corpus**
- 🌐 Content collected from multiple public technical sources
- 🔎 **BM25**, **TF-IDF**, and **Language Model** retrieval
- ✍️ Spelling correction
- 🔤 Abbreviation expansion
- 🧠 Query expansion and query normalization
- 💬 Natural-language query support
- `"..."` Exact phrase search
- 🎯 Domain-aware query handling
- 🤖 Optional **LLM query rewriting**
- ➕ Optional **LLM query expansion**
- 📝 Optional result summarization
- 💡 Optional ranking explanations
- 📊 Precision@10, Recall@10, and MAP@10 evaluation
- 🌍 Flask web interface
- 📈 Dataset analysis and Word2Vec experiments

---

## 🎥 Demo & Documentation

| Resource | Link |
| --- | --- |
| 🎬 Demo Video | [Watch on YouTube](https://youtu.be/0NNBWFSb85w) |
| 📄 Project Documentation | [Open Google Docs](https://docs.google.com/document/d/1ynFGdEQevTd2_o-QfKIdhNidFLw2Gw7kzWafodaqPSA/edit?usp=sharing) |

### Demo Timeline

| Time | Section |
| --- | --- |
| 00:00 – 00:20 | Introduction |
| 00:20 – 00:55 | Project Overview & Dataset |
| 00:55 – 01:35 | Code Structure Explanation |
| 01:35 – 02:10 | Retrieval Models: BM25, TF-IDF, LM |
| 02:10 – 02:45 | Interface Features & LLM Options |
| 02:45 – 03:10 | Keyword Query Demo |
| 03:10 – 03:35 | Natural Language Query Demo |
| 03:35 – 03:55 | Ambiguous Query Demo |
| 03:55 – 04:15 | Phrase Query Demo |
| 04:15 – 04:40 | LLM-Augmented Query Demo |
| 04:40 – 05:00 | Evaluation Results & Conclusion |

---

# 📌 Project Overview

The project implements a complete **Information Retrieval pipeline under realistic conditions**.

Development was divided into three major milestones:

1. **Data Collection & Analysis**
2. **Retrieval System & Experimental Evaluation**
3. **LLM-Augmented Retrieval**

The goal is to simulate a real-world search environment by combining heterogeneous data sources, classical retrieval algorithms, query-processing techniques, experimental evaluation, and modern LLM-assisted retrieval.

---

# 🏗️ Repository Structure

The repository is organized into two main parts:

```text
MA_KB_Information_Retrieval_Project/
│
├── Dataset_Collecting/
│   ├── code/
│   │   ├── collectors/
│   │   ├── output/
│   │   ├── analyze_dataset.py
│   │   ├── build_dataset.py
│   │   ├── config.py
│   │   └── requirements.txt
│   │
│   └── csv_dataset/
│
├── IR_Project_Code/
│   ├── app.py
│   │
│   ├── data/
│   │   ├── raw/
│   │   └── processed/
│   │
│   ├── preprocessing/
│   ├── query_processing/
│   ├── retrieval/
│   ├── llm_augmented/
│   │
│   ├── templates/
│   ├── static/
│   │
│   ├── results/
│   │   ├── dataset_analysis/
│   │   └── word2vec/
│   │
│   ├── rebuild_indexes.py
│   ├── evaluation_results.txt
│   └── requirements.txt
│
├── .gitignore
└── README.md
```

### Main Components

| Component | Purpose |
| --- | --- |
| `Dataset_Collecting/` | Dataset collection, validation, analysis, and corpus construction |
| `IR_Project_Code/app.py` | Main Flask web application |
| `preprocessing/` | Cleaning and corpus preparation |
| `query_processing/` | Query normalization, spell correction, abbreviation expansion, and related processing |
| `retrieval/` | BM25, TF-IDF, and Language Model retrieval logic |
| `llm_augmented/` | LLM-based query rewriting, expansion, summarization, and explanation |
| `data/processed/` | Generated indexes and processed document data |
| `results/` | Dataset analysis and Word2Vec outputs |
| `evaluation_results.txt` | Experimental retrieval evaluation results |

---

# 🧩 Milestone 1 — Data Collection & Analysis

## 📊 Dataset Description

A heterogeneous corpus of **500 documents** was constructed to simulate a realistic information retrieval environment.

### Requirements Satisfied

- ✅ At least **500 documents**
- ✅ Multiple content types
- ✅ Multiple technical themes
- ✅ Short documents under 300 words
- ✅ Medium-length documents
- ✅ Long documents over 2,000 words
- ✅ Each document contains:
  - Title
  - Text
  - Source URL
  - Source type
  - Theme
  - Word count
  - Document identifier

---

## 🌐 Data Sources

Documents were collected from a mixture of publicly accessible technical sources:

- **arXiv** — research papers and technical abstracts
- **Wikipedia** — encyclopedic technical articles
- **GitHub** — README files and project documentation
- **StackExchange** — technical questions and discussions
- **Web Articles** — institutional, technical, and educational web content

This combination creates a more realistic retrieval environment than a single-source corpus.

---

## 🧠 Themes Covered

The corpus contains technical content across areas including:

- AI Bias and Fairness
- AI Governance and Responsible AI
- Open Source and Software Evolution
- Green Computing
- Environmental Monitoring Systems
- Digital Preservation Systems
- History of the Internet and Web
- IoT Security and Privacy
- IoT Sensors and Actuators
- Game Engine Architecture
- Procedural Content Generation

Earlier stages of dataset development also explored **Palestinian Digital Heritage** as a corpus theme.

---

## 📈 Dataset Analysis

The dataset was analyzed before retrieval preprocessing.

Analysis includes:

- Document distribution by source
- Document distribution by theme
- Document length distribution
- Average document length
- Average document length per topic
- Vocabulary statistics
- Stopword percentages
- Lexical overlap between topics
- Frequent-word analysis
- Word2Vec-based semantic exploration
- PCA and t-SNE visualization of word embeddings

Generated analysis files can be found under:

```text
Dataset_Collecting/code/output/
```

and:

```text
IR_Project_Code/results/dataset_analysis/
```

---

# ⚙️ Milestone 2 — Retrieval System & Experimental Framework

The second stage of the project implements the search engine itself.

## 🔍 Retrieval Models

Three retrieval approaches are available.

### 1. BM25

BM25 is a probabilistic ranking model that scores documents according to query-term occurrence while accounting for document length and term frequency saturation.

It is particularly effective for traditional keyword search.

### 2. TF-IDF

The TF-IDF retrieval model represents documents and queries using weighted term vectors and measures their similarity.

It provides a strong classical vector-space baseline.

### 3. Language Model Retrieval

The Language Model approach estimates the likelihood of a query being generated from each document's language model.

This provides a probabilistic alternative to BM25 and TF-IDF.

---

# 🧠 Query Processing

The system includes several mechanisms for improving raw user queries before retrieval.

## ✍️ Spelling Correction

Typo-heavy input can be corrected before retrieval.

Example:

```text
ai biass and machne learnig farness
```

can be transformed toward a cleaner representation involving:

```text
AI bias and machine learning fairness
```

---

## 🔤 Abbreviation Expansion

Technical abbreviations can be expanded to improve retrieval coverage.

Examples include concepts such as:

```text
AI → Artificial Intelligence
IoT → Internet of Things
NLP → Natural Language Processing
```

---

## 🔎 Exact Phrase Search

Quoted text can be treated as an exact phrase.

Example:

```text
"artificial intelligence"
```

Exact phrase matches can receive additional ranking importance compared with documents containing the individual terms independently.

---

## 🔡 Case Normalization

Search is designed to work consistently regardless of capitalization differences.

For example:

```text
Artificial Intelligence
```

and:

```text
artificial intelligence
```

are processed consistently.

---

## 🌐 Domain Awareness

The system includes query-domain checking to estimate whether a query belongs to the technical areas represented by the corpus.

This reduces meaningless retrieval for completely unrelated searches.

---

# 🖥️ Flask Web Interface

The project includes a web interface built using **Flask**.

The interface allows users to:

- Enter a search query
- Select a retrieval model
- Configure the number of returned results
- View ranked documents
- View ranking scores
- View snippets with highlighted search terms
- Receive spelling suggestions
- Use query-expansion features
- Enable LLM augmentation
- Request LLM-generated summaries
- Request ranking explanations

Each search result can include:

- Document title
- Source URL
- Relevant snippet
- Retrieval score
- Exact-match information
- Optional LLM ranking explanation

---

# 📊 Experimental Evaluation

The system was evaluated with a set of **20 test queries** representing different search conditions.

## Query Types

| Query Type | Count |
| --- | ---: |
| Keyword | 5 |
| Natural Language | 5 |
| Ambiguous | 5 |
| Noisy / Typo-heavy | 5 |
| **Total** | **20** |

Each query was associated with a relevant-document set used to evaluate the retrieval models.

---

## 📏 Evaluation Metrics

### Precision@10

Measures how many of the first 10 retrieved documents are relevant.

### Recall@10

Measures how much of the known relevant-document set appears within the first 10 retrieved results.

### MAP@10

Mean Average Precision evaluates both relevance and the positions at which relevant documents appear.

---

## 📑 Evaluation Output

Detailed experimental results are available in:

```text
IR_Project_Code/evaluation_results.txt
```

The report compares:

- BM25
- TF-IDF
- Language Model retrieval

and includes:

- Precision@10
- Recall@10
- MAP@10
- Retrieved top-10 documents
- Failure cases
- Query-type comparisons

---

# 🤖 Milestone 3 — LLM-Augmented Retrieval

The final stage explores how Large Language Models can complement traditional retrieval systems.

LLMs are **not used as a replacement for the search engine**. Instead, they are used as an optional augmentation layer around the classical retrieval pipeline.

---

## ✏️ Query Rewriting

The LLM can rewrite a user's query into a clearer formulation before retrieval.

For example, an ambiguous or conversational query can be reformulated into terminology that better represents the user's information need.

---

## ➕ Query Expansion

The LLM can add semantically related concepts and terminology to a query.

This can improve recall when the original query does not contain the terminology used in relevant documents.

However, excessive expansion may also introduce irrelevant concepts and cause **query drift**.

---

## 📝 Result Summarization

The system can optionally generate a summary based on top-ranked retrieval results.

This provides users with a quick overview of the information contained in the retrieved documents.

---

## 💡 Ranking Explanation

An optional LLM component can generate human-readable explanations describing why particular results may be relevant to the user's query.

---

## 📊 Qualitative LLM Analysis

The project examines both positive and negative effects of LLM augmentation.

### Cases where LLM augmentation can help

- Better interpretation of natural-language queries
- Improved handling of vague search requests
- Better semantic coverage
- Additional related terminology
- Improved recall

### Cases where LLM augmentation can hurt

- Query drift
- Over-expansion
- Introduction of unrelated concepts
- Reduced precision
- Additional latency
- Dependency on an external model

This illustrates an important principle of modern retrieval systems:

> LLM augmentation should complement retrieval rather than automatically replace established retrieval models.

---

# 🚀 Running the Project

## 1. Clone the Repository

```bash
git clone https://github.com/Mohammad-ALADDASI/MA_KB_Information_Retrieval_Project.git
cd MA_KB_Information_Retrieval_Project
```

---

## 2. Enter the Application Directory

```bash
cd IR_Project_Code
```

---

## 3. Create a Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

Depending on which parts of the project you run, additional libraries used by the dataset-analysis and LLM components may also be required.

---

## 5. Configure Optional LLM Features

LLM functionality expects the OpenAI API key to be supplied using an environment variable.

Create a local `.env` file if needed:

```env
OPENAI_API_KEY=your_api_key_here
```

A GitHub API token can also optionally be supplied when running GitHub-based dataset collection:

```env
GITHUB_TOKEN=your_github_token_here
```

> ⚠️ Never commit actual API keys, access tokens, passwords, or other credentials to this repository.

`.env` and `.env.*` files are intentionally excluded from version control.

---

## 6. Rebuild Search Indexes if Required

```bash
python rebuild_indexes.py
```

Pre-generated processed data may already be included in the project, but rebuilding the indexes ensures they correspond to the local corpus.

---

## 7. Start the Flask Application

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

in your browser.

> The Flask development server is intended for local development and demonstrations. A production deployment should use an appropriate production WSGI server and should not expose Flask debug mode publicly.

---

# 📦 Rebuilding the Dataset

Dataset collection code is located under:

```text
Dataset_Collecting/code/
```

Install its dependencies:

```bash
cd Dataset_Collecting/code
pip install -r requirements.txt
```

The dataset collection pipeline includes separate collectors for:

```text
collectors/
├── arxiv_collector.py
├── github_collector.py
├── stackexchange_collector.py
├── web_collector.py
└── wikipedia_collector.py
```

The pipeline performs:

1. Document collection
2. Text extraction
3. Normalization
4. Validation
5. Deduplication
6. Topic assignment
7. Length calculation
8. Dataset export
9. Corpus analysis

---

# 🧪 Example Searches

The project is designed to support multiple kinds of queries.

### Keyword Query

```text
iot edge device botnet ddos vulnerabilities
```

### Natural-Language Query

```text
How can artificial intelligence systems reduce algorithmic bias?
```

### Exact Phrase Query

```text
"history of the internet"
```

### Ambiguous Query

```text
fairness
```

### Typo-Heavy Query

```text
enviroment monitorng snsors water quality
```

These different query styles help test the robustness of preprocessing and ranking techniques.

---

# 🔬 Technologies Used

## Core

- Python
- Flask
- Pandas
- NumPy
- scikit-learn

## Information Retrieval

- BM25
- TF-IDF
- Probabilistic Language Models
- Query normalization
- Query expansion
- Exact phrase matching

## NLP & Analysis

- Text preprocessing
- Tokenization
- Vocabulary analysis
- Word2Vec
- PCA
- t-SNE

## Data Collection

- arXiv
- Wikipedia APIs
- GitHub API
- StackExchange
- Requests
- BeautifulSoup
- Trafilatura

## LLM Integration

- OpenAI API
- Query rewriting
- Query expansion
- Search-result summarization
- Ranking explanation

---

# 📈 Research Questions Explored

The project provides a practical environment for exploring questions such as:

- How does BM25 compare with TF-IDF on a heterogeneous technical corpus?
- How does probabilistic Language Model retrieval compare with classical vector-space retrieval?
- How much does spelling correction improve typo-heavy searches?
- Does query expansion improve recall?
- When does query expansion cause query drift?
- How do retrieval models behave across different topic domains?
- How does query type affect retrieval performance?
- Can LLM rewriting improve vague or conversational queries?
- When does LLM augmentation improve search quality?
- When does LLM augmentation decrease precision?

---

# 🧠 What This Project Demonstrates

Beyond implementing individual algorithms, the project demonstrates how the components of a search system interact:

```text
User Query
    │
    ▼
Query Validation
    │
    ▼
Normalization
    │
    ├── Spell Correction
    ├── Abbreviation Expansion
    ├── Query Expansion
    └── Optional LLM Rewriting
    │
    ▼
Retrieval Engine
    │
    ├── BM25
    ├── TF-IDF
    └── Language Model
    │
    ▼
Ranked Results
    │
    ├── Highlighting
    ├── Optional LLM Summary
    └── Optional Ranking Explanation
    │
    ▼
Flask Web Interface
```

This makes the repository useful as both an academic project and a practical reference implementation for experimenting with modern information retrieval techniques.

---

# 🔐 Security & Privacy

This repository is intended to be public.

Secrets and credentials should therefore always remain outside version control.

### Do not commit

- `.env` files
- OpenAI API keys
- GitHub access tokens
- Passwords
- Private keys
- Authentication cookies
- Debugger credentials
- Private application logs

Environment variables should be used for credentials instead.

Example:

```python
import os

api_key = os.getenv("OPENAI_API_KEY")
```

The repository's `.gitignore` should exclude local environment files, Python cache files, notebook checkpoints, and logs.

Recommended entries include:

```gitignore
.env
.env.*
*.log

__pycache__/
*.py[cod]

.ipynb_checkpoints/
```

---

# 🧹 Repository Hygiene

Generated Python bytecode and local development artifacts are not necessary for reproducing the project.

For a clean public repository, files such as the following should normally remain excluded from version control:

```text
__pycache__/
*.pyc
.ipynb_checkpoints/
*.log
```

Large generated indexes or trained models may also be moved to release assets or regenerated locally when repository size becomes a concern.

---

# ⚖️ Dataset, Attribution & Responsible Use

The corpus was constructed from publicly accessible sources for **educational and research purposes**.

Source material may remain subject to the copyright, licenses, attribution requirements, and terms of service of its original publishers.

The presence of material on a publicly accessible website does not necessarily mean that it can be redistributed without restriction.

Users of this project should therefore:

- Refer to the original source URLs
- Respect source-specific licenses
- Preserve attribution where required
- Review applicable terms before redistributing collected content
- Use the corpus primarily for research and educational experimentation

The repository does not claim ownership of third-party source material.

---

# 🎯 Intended Use

This project is intended for:

- Information Retrieval research
- NLP experimentation
- Search-engine prototyping
- Ranking-model comparison
- Query-processing experiments
- LLM-assisted retrieval experiments
- Educational demonstrations
- University coursework
- Reproducible retrieval experiments

---

# 🚧 Limitations

Like any experimental retrieval system, this project has limitations.

- The corpus contains only 500 documents and is not representative of the entire web.
- Relevance judgments used for evaluation may contain subjective decisions.
- Classical retrieval models depend heavily on vocabulary overlap.
- LLM augmentation can introduce query drift.
- LLM-based features require access to an external model.
- LLM output may vary between requests.
- The Flask application is designed primarily for local demonstration rather than production deployment.
- Results should be interpreted as experimental findings rather than general benchmarks for all information retrieval systems.

---

# 🔮 Possible Future Improvements

Possible extensions include:

- Dense embedding retrieval
- Sentence-transformer embeddings
- Hybrid BM25 + vector search
- Cross-encoder reranking
- Reciprocal Rank Fusion
- Retrieval-Augmented Generation
- Larger evaluation datasets
- More rigorous relevance annotation
- NDCG and MRR evaluation
- Search analytics
- Query history
- REST API support
- Containerized deployment with Docker
- Automated tests
- Continuous integration
- Improved experiment reproducibility
- Larger multilingual corpora

---

# 🎓 Academic Context

This project was developed as part of a university course:

**Information Retrieval and Text Analysis**

The implementation was divided into three milestones.

| Milestone | Deadline |
| --- | --- |
| Milestone 1 — Data Collection & Analysis | 21/03/2026 |
| Milestone 2 — Retrieval & Evaluation | 25/04/2026 |
| Milestone 3 — LLM-Augmented Retrieval | 09/05/2026 |
| Project Discussion | 10–21/05/2026 |

---

# 📚 Project Milestones at a Glance

### Milestone 1

**Data Collection & Analysis**

- Build heterogeneous corpus
- Validate document diversity
- Analyze document lengths
- Analyze vocabulary
- Measure lexical overlap
- Explore corpus semantics

### Milestone 2

**Retrieval & Evaluation**

- Build BM25 retrieval
- Build TF-IDF retrieval
- Build Language Model retrieval
- Implement query preprocessing
- Build Flask interface
- Create evaluation queries
- Measure Precision, Recall, and MAP
- Analyze model failures

### Milestone 3

**LLM-Augmented Retrieval**

- Query rewriting
- Query expansion
- Result summarization
- Ranking explanations
- Qualitative analysis of LLM impact

---

# 🤝 Contributions

This is primarily an academic and research project, but suggestions, discussions, and improvements are welcome.

If you would like to experiment with the project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test the retrieval behavior
5. Submit a pull request with a clear description of the improvement

Potential contribution areas include retrieval algorithms, evaluation, query processing, documentation, UI improvements, and dataset tooling.

---

# ⭐ Support the Project

If you find this project useful for learning about **Information Retrieval, NLP, search engines, or LLM-enhanced retrieval**, consider starring the repository.

A ⭐ helps make the project easier for other students and developers interested in information retrieval to discover.

---

# 📬 Repository

**GitHub:**  
[MA_KB_Information_Retrieval_Project](https://github.com/Mohammad-ALADDASI/MA_KB_Information_Retrieval_Project)

---

## Final Note

This project brings together classical Information Retrieval and modern LLM-based techniques in one experimental system.

Rather than treating LLMs as a replacement for search, the project explores how traditional ranking algorithms, query processing, corpus analysis, evaluation, and language models can work together to build a more capable retrieval pipeline.

**BM25 + TF-IDF + Language Models + Query Processing + LLM Augmentation + Evaluation = a complete experimental Information Retrieval system.**
