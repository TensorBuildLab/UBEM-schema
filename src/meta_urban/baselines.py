"""Non-LLM baselines for task T2 (variable -> concept) and the candidate retriever used by condition L3.

B1 lexical: TF-IDF over word unigrams/bigrams plus character 3-5 grams. A variable is represented by its name
(split on case and underscores) and its label; a concept by its preferred label, alternative labels and
definition. Concepts are ranked by cosine similarity.

B2 embedding (optional, needs `pip install meta-urban[embed]`): sentence-transformers model, same texts.
"""

from __future__ import annotations

import re

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion

from .io import leaf_concepts


def variable_text(item: dict) -> str:
    name = re.sub(r"[_\d]+", " ", item["name"])
    return f"{name} {item.get('label') or ''}".strip()


def concept_text(c: dict) -> str:
    return " ; ".join([c["pref_label"], *c.get("alt_labels", []), c["definition"]])


class LexicalRetriever:
    def __init__(self, concepts: list[dict] | None = None):
        self.concepts = concepts or leaf_concepts()
        self.ids = [c["id"] for c in self.concepts]
        self.vec = FeatureUnion([
            ("word", TfidfVectorizer(analyzer="word", ngram_range=(1, 2), sublinear_tf=True, lowercase=True)),
            ("char", TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), sublinear_tf=True, lowercase=True)),
        ])
        self.C = self.vec.fit_transform([concept_text(c) for c in self.concepts])

    def scores(self, items: list[dict]) -> np.ndarray:
        from sklearn.preprocessing import normalize

        X = normalize(self.vec.transform([variable_text(i) for i in items]))
        return np.asarray((X @ normalize(self.C).T).toarray())

    def rank(self, items: list[dict], k: int | None = None) -> list[list[str]]:
        S = self.scores(items)
        order = np.argsort(-S, axis=1)
        k = k or len(self.ids)
        return [[self.ids[j] for j in row[:k]] for row in order]


class EmbeddingRetriever(LexicalRetriever):
    def __init__(self, model: str = "sentence-transformers/all-MiniLM-L6-v2", concepts: list[dict] | None = None):
        from sentence_transformers import SentenceTransformer  # optional dependency

        self.concepts = concepts or leaf_concepts()
        self.ids = [c["id"] for c in self.concepts]
        self.model = SentenceTransformer(model)
        self.C = self.model.encode([concept_text(c) for c in self.concepts], normalize_embeddings=True)

    def scores(self, items: list[dict]) -> np.ndarray:
        X = self.model.encode([variable_text(i) for i in items], normalize_embeddings=True)
        return X @ self.C.T
