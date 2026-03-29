import os
import json
from collections import defaultdict
from preprocessor import Preprocessor

class Indexer:
    def __init__(self, data_path, stopwords_file):
        self.data_path = data_path
        self.preprocessor = Preprocessor(stopwords_file)

        self.inverted_index = defaultdict(set)
        self.positional_index = defaultdict(lambda: defaultdict(list))
        self.documents = {}

    def build_indexes(self):
        for file in os.listdir(self.data_path):
            if not file.endswith(".txt"):
                continue

            doc_id = file.replace("speech_", "").replace(".txt", "")

            with open(os.path.join(self.data_path, file), 'r', encoding='utf-8') as f:
                text = f.read()

            tokens = self.preprocessor.preprocess(text)
            self.documents[doc_id] = text

            for pos, token in enumerate(tokens):
                self.inverted_index[token].add(doc_id)
                self.positional_index[token][doc_id].append(pos)

    def save_indexes(self):
        os.makedirs("indexes", exist_ok=True)

        inv = {k: list(v) for k, v in self.inverted_index.items()}
        pos = {k: {d: v for d, v in docs.items()} for k, docs in self.positional_index.items()}

        with open("indexes/inverted.json", "w") as f:
            json.dump(inv, f)

        with open("indexes/positional.json", "w") as f:
            json.dump(pos, f)

    def load_indexes(self):
        with open("indexes/inverted.json", "r") as f:
            inv = json.load(f)
            self.inverted_index = {k: set(v) for k, v in inv.items()}

        with open("indexes/positional.json", "r") as f:
            self.positional_index = json.load(f)