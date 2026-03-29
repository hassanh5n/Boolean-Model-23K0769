from indexer import Indexer
from query_engine import QueryEngine
from gui import run_gui
from nltk.stem import PorterStemmer

DATA_PATH = "data/Trump Speechs"
STOPWORDS = "Stopword-List.txt"

indexer = Indexer(DATA_PATH, STOPWORDS)

print("Building indexes...")
indexer.build_indexes()
indexer.save_indexes()

engine = QueryEngine(
    indexer.inverted_index,
    indexer.positional_index,
    indexer.documents,
    PorterStemmer()
)

def load_queries(file):
    queries = []
    with open(file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("{"):
                continue
            queries.append(line)
    return queries

queries = load_queries("Querry List.txt")
for q in queries:
    result = engine.process_query(q)
    print(f"Query: {q}")
    print(f"Result: {result}")
    print("-" * 40)

run_gui(engine, data_path=DATA_PATH)