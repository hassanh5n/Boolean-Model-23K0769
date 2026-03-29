import re
from nltk.stem import PorterStemmer

class Preprocessor:
    def __init__(self, stopwords_file):
        self.stopwords = self.load_stopwords(stopwords_file)
        self.stemmer = PorterStemmer()

    def load_stopwords(self, file):
        with open(file, 'r') as f:
            return set(word.strip() for word in f)

    def preprocess(self, text):
        text = text.lower()

        tokens = re.findall(r'\b[a-z]+\b', text)

        tokens = [t for t in tokens if t not in self.stopwords]

        tokens = [self.stemmer.stem(t) for t in tokens]

        return tokens