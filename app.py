import os
from flask import Flask, Response, request, jsonify, send_from_directory
from indexer import Indexer
from query_engine import QueryEngine
from nltk.stem import PorterStemmer

DATA_PATH = "data/Trump Speechs"
STOPWORDS  = "Stopword-List.txt"

indexer = Indexer(DATA_PATH, STOPWORDS)
indexer.build_indexes()

engine = QueryEngine(
    indexer.inverted_index,
    indexer.positional_index,
    indexer.documents,
    PorterStemmer()
)

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
    static_folder=os.path.join(os.path.dirname(__file__), "templates"),
)

@app.route("/")
def index():
    return send_from_directory(app.template_folder, "index.html")

@app.route("/favicon.ico")
def favicon():
    svg = (
        b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
        b'<rect width="32" height="32" rx="4" fill="#f5f0e8"/>'
        b'<rect x="4" y="4" width="11" height="11" rx="2" fill="#1a1a1a"/>'
        b'<rect x="17" y="4" width="11" height="11" rx="2" fill="#1a1a1a" opacity=".35"/>'
        b'<rect x="4" y="17" width="11" height="11" rx="2" fill="#1a1a1a" opacity=".35"/>'
        b'<rect x="17" y="17" width="11" height="11" rx="2" fill="#1a1a1a"/>'
        b'</svg>'
    )
    return Response(svg, mimetype="image/svg+xml")

@app.route("/search", methods=["POST"])
def search():
    data  = request.get_json(force=True)
    query = data.get("query", "").strip()
    if not query:
        return jsonify(results=[], stemmed=[])
    try:
        result_set    = engine.process_query(query)
        stemmed_terms = engine.get_stemmed_terms(query)
        results = sorted(
            result_set,
            key=lambda x: int(x) if x.isdigit() else float("inf")
        ) if result_set else []
    except Exception as e:
        return jsonify(error=str(e), results=[], stemmed=[]), 500
    return jsonify(results=results, stemmed=stemmed_terms)

@app.route("/preview/<doc_id>")
def preview(doc_id):
    safe_id  = "".join(c for c in doc_id if c.isdigit())
    filepath = os.path.join(DATA_PATH, f"speech_{safe_id}.txt")
    if not os.path.isfile(filepath):
        return jsonify(content="File not found."), 404
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        return jsonify(content=content)
    except Exception as e:
        return jsonify(content=f"Error: {e}"), 500

@app.route("/info")
def info():
    count = sum(1 for f in os.listdir(DATA_PATH) if f.endswith(".txt")) if os.path.isdir(DATA_PATH) else 0
    return jsonify(doc_count=count)