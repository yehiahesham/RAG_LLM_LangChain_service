from collections import Counter
from math import sqrt
from typing import List, Tuple


def tokenize(text: str) -> List[str]:
    return [t for t in "".join([c.lower() if c.isalnum() else " " for c in text]).split() if t]


def vectorize(tokens: List[str]) -> Counter:
    return Counter(tokens)


def cosine(a: Counter, b: Counter) -> float:
    common = set(a.keys()) & set(b.keys())
    dot = sum(a[t]*b[t] for t in common)
    na = sqrt(sum(v*v for v in a.values()))
    nb = sqrt(sum(v*v for v in b.values()))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na*nb)


class SimpleVectorStore:
    def __init__(self):
        self.docs: List[str] = []
        self.vecs: List[Counter] = []

    def build_index(self, docs: List[str]):
        self.docs = docs
        self.vecs = [vectorize(tokenize(d)) for d in docs]

    def similarity_search(self, query: str, k: int = 5) -> List[Tuple[str, float]]:
        qv = vectorize(tokenize(query))
        sims = [(doc, cosine(qv, dv)) for doc, dv in zip(self.docs, self.vecs)]
        sims.sort(key=lambda x: x[1], reverse=True)
        return sims[:k]