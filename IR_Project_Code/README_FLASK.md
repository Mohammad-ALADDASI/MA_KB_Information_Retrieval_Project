# Flask IR System

This is a conversion of the original Streamlit IR project to a Flask web application.

## Project Structure
- `app.py`: Main Flask application.
- `templates/`: HTML templates for the web interface.
- `retrieval/`: Core retrieval logic (BM25, TF-IDF, LM).
- `query_processing/`: Query enhancement features (Spell correction, expansion, etc.).
- `data/`: Processed indexes and document mappings.

## Installation
1. Install the required dependencies:
   ```bash
   pip install flask scikit-learn rank-bm25 numpy
   ```

2. Run the application:
   ```bash
   python app.py
   ```

3. Open your browser and navigate to `http://localhost:5000`.

## Features
- **Multiple Models**: Choose between BM25, TF-IDF, and Language Model.
- **Query Enhancement**: Includes spell correction, abbreviation expansion, and synonym expansion.
- **Exact Phrase Search**: Support for "quoted" phrases with ranking boosts.
- **Domain Detection**: Checks if the query is within the AI/Data Science domain.
