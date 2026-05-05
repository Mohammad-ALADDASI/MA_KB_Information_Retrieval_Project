# Heterogeneous Technical Corpus Dataset

## Overview

This dataset is a heterogeneous technical corpus constructed for an Information Retrieval and Text Analysis assignment.

The corpus simulates real-world retrieval environments by combining documents from multiple technical sources and diverse thematic domains. It includes documents of varying lengths and formats collected from research repositories, encyclopedic platforms, software repositories, technical Q&A forums, and web articles.

The dataset supports tasks such as:

* Information retrieval experiments
* Topic modeling and analysis
* Text mining and NLP tasks
* Lexical similarity and overlap analysis
* Cross-domain comparison of technical content

---

# Dataset Statistics

Total Documents: **500** 

## Document Sources

| Source        | Documents |
| ------------- | --------- |
| arXiv         | 275       |
| GitHub        | 102       |
| WebArticle    | 56        |
| Wikipedia     | 34        |
| StackExchange | 33        |

## Document Length Distribution

| Length Category | Documents |
| --------------- | --------- |
| Short           | 351       |
| Medium          | 100       |
| Long            | 49        |

Average Document Length: **1183 words**

---

# Themes Covered

The dataset contains **11 technical themes**:

| Theme                              | Documents |
| ---------------------------------- | --------- |
| Procedural content generation      | 63        |
| Game engine architecture           | 62        |
| IoT sensors and actuators          | 62        |
| IoT security and privacy           | 62        |
| AI Bias and Fairness               | 38        |
| Open Source and Software Evolution | 37        |
| Environmental Monitoring Systems   | 36        |
| AI Governance and Responsible AI   | 36        |
| Green Computing                    | 35        |
| History of the Internet and Web    | 35        |
| Digital Preservation Systems       | 34        |

---

# Dataset Structure

The dataset is stored as a CSV file:

```
output/heterogeneous_corpus.csv
```

Each row corresponds to a single document.

Dataset schema:

| Field       | Description                          |
| ----------- | ------------------------------------ |
| source      | Source type of the document          |
| theme       | Assigned thematic category           |
| title       | Title of the document                |
| text        | Extracted textual content            |
| url         | Original source link                 |
| length_type | Short / Medium / Long classification |
| doc_id      | Unique document identifier           |
| word_count  | Number of words in the document      |

---

# Vocabulary Statistics

The dataset exhibits varying lexical richness across themes.

| Theme                              | Token Ratio |
| ---------------------------------- | ----------- |
| Game engine architecture           | 0.316       |
| Environmental Monitoring Systems   | 0.291       |
| Procedural content generation      | 0.279       |
| IoT security and privacy           | 0.271       |
| IoT sensors and actuators          | 0.270       |
| Digital Preservation Systems       | 0.232       |
| Green Computing                    | 0.236       |
| AI Governance and Responsible AI   | 0.216       |
| AI Bias and Fairness               | 0.213       |
| History of the Internet and Web    | 0.205       |
| Open Source and Software Evolution | 0.179       |

These values indicate differences in vocabulary diversity and domain-specific terminology usage.

---

# Stopword Statistics

Stopword usage remains relatively consistent across themes, typically ranging between **24% and 30%** of total tokens.

This reflects a balance between technical terminology and natural language structure across documents.

---

# Lexical Overlap

Lexical overlap between themes ranges approximately between **18% and 26%**, indicating:

* Moderate shared vocabulary across domains
* Distinct domain-specific terminology
* Clear thematic separation suitable for retrieval experiments

Higher overlap is observed between related domains such as:

* AI Bias and AI Governance
* Open Source and Internet History
* Green Computing and AI-related topics

---

# Document Sources

Documents were collected from multiple publicly accessible technical resources:

### arXiv

Research paper abstracts covering AI, computing systems, and technical domains.

### Wikipedia

Structured encyclopedic articles on historical and technical topics.

### GitHub

README files and documentation from open-source repositories.

### StackExchange

Technical discussions and problem-solving threads.

### Web Articles

Institutional blogs and technical articles from educational and research platforms.

---

# Data Collection Pipeline

The dataset was generated using an automated Python-based pipeline.

Project structure:

```
corpus_builder/
├── build_dataset.py
├── analyze_dataset.py
├── config.py
├── utils.py
├── collectors/
│   ├── arxiv_collector.py
│   ├── wikipedia_collector.py
│   ├── github_collector.py
│   ├── stackexchange_collector.py
│   └── web_collector.py
```

Collection methods:

* API-based retrieval (arXiv, Wikipedia, GitHub, StackExchange)
* Web scraping using:

  * requests
  * BeautifulSoup
  * Trafilatura

Each source document is treated as a single corpus entry.

---

# Data Processing

### Deduplication

Duplicate documents removed using URL and metadata matching.

### Validation

Documents with missing or insufficient textual content were filtered out.

### Normalization

All documents standardized into a consistent schema.

---

# Analysis Files

The dataset includes additional analytical outputs:

```
vocabulary_stats.csv
stopword_stats.csv
lexical_overlap.csv
```

These provide:

* Vocabulary diversity per theme
* Stopword distribution
* Cross-theme lexical similarity

---

# Intended Use

This dataset is intended for:

* Information retrieval experiments
* NLP and text analysis tasks
* Thematic clustering
* Lexical diversity studies
* Cross-domain analysis

It demonstrates how heterogeneous corpora can be constructed from multiple technical sources.

---

# License and Ethical Use

All data was collected from publicly accessible sources.

Only textual content and source URLs are included.
Users should refer to original sources for licensing and attribution.

---

# Authors

Dataset constructed as part of a university assignment in:

**Information Retrieval and Text Analysis**

Built using an automated Python data collection and analysis pipeline.
