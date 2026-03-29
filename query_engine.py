class QueryEngine:
    def __init__(self, inverted_index, positional_index, documents, stemmer):
        self.inverted_index = inverted_index
        self.positional_index = positional_index
        self.documents = documents
        self.stemmer = stemmer

    def stem(self, word):
        return self.stemmer.stem(word)

    def AND(self, a, b):
        return a & b

    def OR(self, a, b):
        return a | b

    def NOT(self, a):
        return set(self.documents.keys()) - a

    def proximity(self, t1, t2, k):
        result = set()

        if t1 not in self.positional_index or t2 not in self.positional_index:
            return result

        common_docs = set(self.positional_index[t1]) & set(self.positional_index[t2])

        for doc in common_docs:
            pos1 = self.positional_index[t1][doc]
            pos2 = self.positional_index[t2][doc]

            i, j = 0, 0
            while i < len(pos1) and j < len(pos2):
                if abs(pos1[i] - pos2[j]) <= k:
                    result.add(doc)
                    break
                elif pos1[i] < pos2[j]:
                    i += 1
                else:
                    j += 1

        return result

    def evaluate(self, query):
        query = query.strip()

        if query.startswith("(") and query.endswith(")"):
            return self.evaluate(query[1:-1])

        if " or " in query:
            parts = query.split(" or ")
            result = set()
            for part in parts:
                result |= self.evaluate(part)
            return result

        if " and " in query:
            parts = query.split(" and ")
            result = self.evaluate(parts[0])
            for part in parts[1:]:
                result &= self.evaluate(part)
            return result

        if query.startswith("not "):
            term = self.stem(query.replace("not ", "").strip())
            return self.NOT(self.inverted_index.get(term, set()))

        tokens = query.split()
        result = None
        for token in tokens:
            if token in ["and", "or", "not"]:
                continue

            stemmed = self.stem(token)
            postings = self.inverted_index.get(stemmed, set())

            if result is None:
                result = postings
            else:
                result &= postings

        return result if result else set()

    def process_query(self, query):
        query = query.lower()

        if "/" in query:
            tokens = query.split()

            terms = []
            k = None

            for token in tokens:
                if token.startswith("/"):
                    k = int(token.replace("/", ""))
                elif token not in ["and", "or", "not"]:
                    terms.append(self.stem(token))

            if len(terms) >= 2 and k is not None:
                return self.proximity(terms[0], terms[1], k)
        
        print("QUERY TOKENS:", query.split())
        print("STEMMED:", [self.stem(t) for t in query.split()])

        if "and" not in query and "or" not in query and "/" not in query:
            words = query.split()
            result = None

            for word in words:
                postings = self.inverted_index.get(self.stem(word), set())
                if result is None:
                    result = postings
                else:
                    result &= postings

            return result if result else set()

        return self.evaluate(query)