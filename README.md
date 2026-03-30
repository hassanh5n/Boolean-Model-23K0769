# Boolean Information Retrieval Model

A Boolean Information Retrieval system built over a corpus of Trump speeches. Supports standard Boolean operators (`AND`, `OR`, `NOT`) and proximity search, with a Flask web interface deployed on Vercel.

**Live Demo:** [boolean-model-23-k0769.vercel.app](https://boolean-model-23-k0769.vercel.app)

---

## Features

- **Inverted Index** — maps stemmed terms to the documents they appear in
- **Positional Index** — stores word positions per document to enable proximity queries
- **Boolean Queries** — supports `AND`, `OR`, `NOT` operators with grouping via parentheses
- **Proximity Search** — find documents where two terms appear within *k* words of each other
- **Porter Stemmer** — terms are stemmed at index and query time for consistent matching
- **Document Preview** — click any result to read the full speech inline

---

## Query Syntax

| Query | Description |
|---|---|
| `america great` | Implicit AND — documents containing both terms |
| `america AND great` | Explicit AND |
| `america OR china` | Documents containing either term |
| `NOT china` | Documents that do not contain the term |
| `america AND NOT china` | Combined operators |
| `america great /3` | Proximity — terms within 3 words of each other |

> Queries are case-insensitive. Stop words are filtered and terms are auto-stemmed.

---

## Project Structure

```
├── app.py              # Flask app — routes for search, preview, and info
├── indexer.py          # Builds inverted and positional indexes from corpus
├── query_engine.py     # Parses and evaluates Boolean + proximity queries
├── preprocessor.py     # Tokenization, stopword removal, stemming
├── main.py             # CLI entry point
├── gui.py              # Local Tkinter GUI (optional)
├── templates/
│   └── index.html      # Frontend UI
├── data/
│   └── Trump Speechs/  # Corpus — plain text speech files
├── indexes/            # Persisted index files
├── Stopword-List.txt   # Custom stopword list
├── vercel.json         # Vercel deployment config
└── requirements.txt    # Python dependencies
```

---

## Local Setup

**Prerequisites:** Python 3.9+

```bash
git clone https://github.com/hassanh5n/Boolean-IR-Model.git
cd Boolean-IR-Model
pip install -r requirements.txt
python app.py
```

Then open `http://localhost:5000` in your browser.

---

## Deployment

The app is deployed as a Python serverless function on Vercel via `@vercel/python`. The `vercel.json` routes all traffic through `app.py`.

```json
{
  "version": 2,
  "builds": [{ "src": "app.py", "use": "@vercel/python" }],
  "routes": [{ "src": "/(.*)", "dest": "app.py" }]
}
```

---

## Tech Stack

- **Backend:** Python, Flask
- **NLP:** NLTK (Porter Stemmer)
- **Frontend:** HTML/CSS/JS
- **Deployment:** Vercel

---

## Course

Information Retrieval — FAST NUCES  
Student ID: 23K-0769
