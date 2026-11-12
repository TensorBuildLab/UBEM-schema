"""Metrics for the alignment benchmark."""

from __future__ import annotations

from collections import Counter
from itertools import combinations

import numpy as np
import pandas as pd


def acc_at_k(ranked: list[list[str]], gold: list[str], k: int) -> float:
    hits = [g in r[:k] for r, g in zip(ranked, gold)]
    return float(np.mean(hits)) if hits else float("nan")


def mrr(ranked: list[list[str]], gold: list[str]) -> float:
    vals = []
    for r, g in zip(ranked, gold):
        vals.append(1.0 / (r.index(g) + 1) if g in r else 0.0)
    return float(np.mean(vals)) if vals else float("nan")


def macro_f1(pred: list[str], gold: list[str]) -> float:
    labels = sorted(set(gold) | set(pred))
    f1s = []
    for lab in labels:
        tp = sum(p == lab and g == lab for p, g in zip(pred, gold))
        fp = sum(p == lab and g != lab for p, g in zip(pred, gold))
        fn = sum(p != lab and g == lab for p, g in zip(pred, gold))
        if tp + fp + fn == 0:
            continue
        prec = tp / (tp + fp) if tp + fp else 0.0
        rec = tp / (tp + fn) if tp + fn else 0.0
        f1s.append(2 * prec * rec / (prec + rec) if prec + rec else 0.0)
    return float(np.mean(f1s)) if f1s else float("nan")


def none_pr(pred: list[str], gold: list[str]) -> tuple[float, float]:
    """Precision and recall of the 'none' (no concept applies) decision."""
    tp = sum(p == "none" and g == "none" for p, g in zip(pred, gold))
    fp = sum(p == "none" and g != "none" for p, g in zip(pred, gold))
    fn = sum(p != "none" and g == "none" for p, g in zip(pred, gold))
    return (tp / (tp + fp) if tp + fp else float("nan"), tp / (tp + fn) if tp + fn else float("nan"))


def run_agreement(runs: list[list[str]]) -> dict:
    """Self-consistency across repeated runs of the same condition.

    runs: R lists (one per repeat), each with one prediction per item.
    Returns the mean pairwise agreement and the share of items where all runs agree.
    """
    if len(runs) < 2:
        return {"pairwise_agreement": float("nan"), "unanimous_share": float("nan")}
    arr = np.array(runs)
    pair = [np.mean(arr[i] == arr[j]) for i, j in combinations(range(len(runs)), 2)]
    unanimous = np.mean([len(set(arr[:, k])) == 1 for k in range(arr.shape[1])])
    return {"pairwise_agreement": float(np.mean(pair)), "unanimous_share": float(unanimous)}


def majority(votes: list[str]) -> tuple[str, float]:
    c = Counter(votes)
    label, n = c.most_common(1)[0]
    return label, n / len(votes)


def coverage_accuracy(conf: list[float], correct: list[bool], steps: int = 11) -> pd.DataFrame:
    """Accuracy of automatically accepted mappings when only items with confidence >= t are accepted."""
    rows = []
    conf_a, corr_a = np.array(conf), np.array(correct)
    for t in np.linspace(0, 1, steps):
        m = conf_a >= t
        rows.append({"threshold": t, "coverage": float(m.mean()),
                     "accuracy": float(corr_a[m].mean()) if m.any() else float("nan")})
    return pd.DataFrame(rows)


def cohen_kappa(a: list[str], b: list[str]) -> float:
    labels = sorted(set(a) | set(b))
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[l] * cb[l] for l in labels) / (n * n)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0
