import os
import logging
import threading
import webbrowser
from flask import Flask, Response, request, jsonify, send_from_directory

logging.getLogger("werkzeug").setLevel(logging.ERROR)

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
    static_folder=os.path.join(os.path.dirname(__file__), "templates"),
)

_engine    = None
_data_path = None


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
        result_set    = _engine.process_query(query)
        stemmed_terms = _engine.get_stemmed_terms(query)
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
    filepath = os.path.join(_data_path, f"speech_{safe_id}.txt")

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
    count = 0
    if _data_path and os.path.isdir(_data_path):
        count = sum(1 for f in os.listdir(_data_path) if f.endswith(".txt"))
    return jsonify(doc_count=count)


def run_gui(engine, data_path="data/Trump Speechs", host="127.0.0.1", port=5050):
    global _engine, _data_path
    _engine    = engine
    _data_path = data_path

    url = f"http://{host}:{port}"
    print(f"\n  Boolean IR System  →  {url}\n")
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    app.run(host=host, port=port, debug=False, use_reloader=False)