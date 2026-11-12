"""Benchmark driver.

    python -m meta_urban.bench items                       # build benchmark items + annotation sample
    python -m meta_urban.bench baselines                   # lexical (and optional embedding) baselines on T2
    python -m meta_urban.bench t2 --model anthropic:<id> --levels L0 L1 L2 L3 --repeats 5
    python -m meta_urban.bench t3 --model local:<id> --repeats 3
    python -m meta_urban.bench report                      # tables from all cached runs

Gold labels: T2 uses `adjudicated` from benchmark/gold/t2_gold_<dataset>.csv when present, otherwise the draft
labels; every output records which (`gold_status`). Results computed on draft labels are PROVISIONAL and must not
be reported in the paper.
"""

from __future__ import annotations

import argparse
import json
import sys

import numpy as np
import pandas as pd

from . import BENCH
from .baselines import LexicalRetriever
from .codebooks import load_all
from .llm import _load_cache, complete, parse_json, t2_prompt, t3_prompt
from .metrics import acc_at_k, macro_f1, majority, mrr, none_pr, run_agreement

ITEMS = BENCH / "inputs" / "t2_t3_items.jsonl"
SAMPLE = BENCH / "inputs" / "t2_eval_sample.csv"
RES = BENCH / "results"
SEED = 20261112


# ------------------------------------------------------------------------------------------------- items
def gold_table() -> pd.DataFrame:
    parts = []
    for ds in ["cbecs2018", "recs2020"]:
        g = BENCH / "gold" / f"t2_gold_{ds}.csv"
        d = BENCH / "gold" / f"t2_draft_{ds}.csv"
        if g.exists():
            t = pd.read_csv(g, dtype=str).fillna("")
            t["gold"] = np.where(t["adjudicated"] != "", t["adjudicated"], t["draft_concept"])
            t["gold_status"] = np.where(t["adjudicated"] != "", "adjudicated", "draft")
        else:
            t = pd.read_csv(d, dtype=str).fillna("")
            t["gold"], t["gold_status"] = t["draft_concept"], "draft"
        parts.append(t[["dataset", "name", "gold", "gold_status"]])
    return pd.concat(parts, ignore_index=True)


def build_items(per_dataset: int = 150) -> pd.DataFrame:
    cb = load_all()
    g = gold_table()
    df = cb.merge(g, on=["dataset", "name"], how="left")
    ITEMS.parent.mkdir(parents=True, exist_ok=True)
    with open(ITEMS, "w", encoding="utf-8") as fh:
        for rec in df.to_dict("records"):
            rec = {k: (None if isinstance(v, float) and np.isnan(v) else v) for k, v in rec.items()}
            fh.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")
    # evaluation sample for T2: substantive variables only (no imputation flags, no replicate weights),
    # stratified by draft concept so that rare concepts are represented, fixed seed.
    sub = df[~df.is_imputation_flag & ~df.is_replicate_weight].copy()
    rng = np.random.default_rng(SEED)
    picks = []
    for ds, part in sub.groupby("dataset"):
        # proportional allocation with a floor of 1 per concept
        groups = part.groupby("gold")
        alloc = {k: max(1, round(per_dataset * len(v) / len(part))) for k, v in groups}
        while sum(alloc.values()) > per_dataset:
            big = max(alloc, key=alloc.get)
            alloc[big] -= 1
        for k, v in groups:
            n = min(alloc[k], len(v))
            picks.append(v.iloc[rng.choice(len(v), n, replace=False)])
    sample = pd.concat(picks)[["dataset", "name", "label", "section", "gold", "gold_status"]]
    sample = sample.sort_values(["dataset", "name"]).reset_index(drop=True)
    sample.to_csv(SAMPLE, index=False, encoding="utf-8")
    return sample


def load_items(sample_only: bool = True) -> list[dict]:
    with open(ITEMS, encoding="utf-8") as fh:
        items = [json.loads(l) for l in fh]
    if sample_only:
        keep = set(map(tuple, pd.read_csv(SAMPLE)[["dataset", "name"]].values))
        items = [i for i in items if (i["dataset"], i["name"]) in keep]
    return items


# ------------------------------------------------------------------------------------------------- T2
def t2_baselines(embedding: bool = False) -> pd.DataFrame:
    items = load_items()
    gold = [i["gold"] for i in items]
    rows = []
    retrievers = {"B1_lexical_tfidf": LexicalRetriever()}
    if embedding:
        from .baselines import EmbeddingRetriever
        retrievers["B2_embedding_minilm"] = EmbeddingRetriever()
    pos = [k for k, g in enumerate(gold) if g != "none"]
    for name, ret in retrievers.items():
        ranked = ret.rank(items)
        rp, gp = [ranked[k] for k in pos], [gold[k] for k in pos]
        S = ret.scores(items)
        top = S.max(1)
        tau = 0.0  # forced choice; a 'none' threshold would need tuning data we do not have
        pred = [r[0] if t > tau else "none" for r, t in zip(ranked, top)]
        rows.append({
            "method": name, "n_items": len(items), "n_mappable": len(pos),
            "acc@1": acc_at_k(rp, gp, 1), "acc@3": acc_at_k(rp, gp, 3), "acc@5": acc_at_k(rp, gp, 5),
            "recall@10": acc_at_k(rp, gp, 10), "mrr": mrr(rp, gp),
            "macro_f1_all": macro_f1(pred, gold),
            "gold_status": ",".join(sorted({i["gold_status"] for i in items})),
        })
    out = pd.DataFrame(rows)
    RES.mkdir(parents=True, exist_ok=True)
    out.to_csv(RES / "t2_baselines.csv", index=False)
    return out


def t2_llm(model: str, levels: list[str], repeats: int, temperature: float, limit: int | None, k: int = 10):
    items = load_items()[:limit] if limit else load_items()
    cands = LexicalRetriever().rank(items, k=k)
    cache = _load_cache(model)
    for level in levels:
        for rep in range(repeats):
            for it, cand in zip(items, cands):
                prompt = t2_prompt(it, level, cand if level == "L3" else None)
                complete(model, prompt, temperature=temperature, repeat=rep, cache=cache)
            print(f"{model} {level} repeat {rep} done ({len(items)} items)", flush=True)


def t2_score(model: str, levels: list[str], repeats: int, temperature: float, limit: int | None, k: int = 10):
    items = load_items()[:limit] if limit else load_items()
    gold = [i["gold"] for i in items]
    cands = LexicalRetriever().rank(items, k=k)
    cache = _load_cache(model)
    rows = []
    for level in levels:
        runs, ranked_runs = [], []
        for rep in range(repeats):
            preds, ranks = [], []
            for it, cand in zip(items, cands):
                key_prompt = t2_prompt(it, level, cand if level == "L3" else None)
                from .llm import _key
                rec = cache.get(_key(model, key_prompt, temperature, rep))
                js = parse_json(rec["response"]) if rec else None
                p = (js or {}).get("concept", "PARSE_ERROR") if js else ("MISSING" if rec is None else "PARSE_ERROR")
                preds.append(p)
                ranks.append([p, *[a for a in (js or {}).get("alternatives", []) if isinstance(a, str)]])
            runs.append(preds)
            ranked_runs.append(ranks)
        maj = [majority([r[k] for r in runs])[0] for k in range(len(items))]
        pos = [k for k, g in enumerate(gold) if g != "none"]
        per_rep_acc = [np.mean([runs[r][k] == gold[k] for k in range(len(items))]) for r in range(repeats)]
        npr = none_pr(maj, gold)
        rows.append({
            "model": model, "level": level, "repeats": repeats, "n_items": len(items),
            "acc@1_mean": float(np.mean(per_rep_acc)), "acc@1_sd": float(np.std(per_rep_acc, ddof=1)) if repeats > 1 else 0.0,
            "acc@1_majority": float(np.mean([m == g for m, g in zip(maj, gold)])),
            "acc@3_rep0_mappable": acc_at_k([ranked_runs[0][k] for k in pos], [gold[k] for k in pos], 3),
            "macro_f1_majority": macro_f1(maj, gold),
            "none_precision": npr[0], "none_recall": npr[1],
            "invalid_rate": float(np.mean([p in {"PARSE_ERROR", "MISSING"} for r in runs for p in r])),
            **run_agreement(runs),
        })
    return pd.DataFrame(rows)


# ------------------------------------------------------------------------------------------------- T3
T3_FIELDS = ["is_weight", "is_replicate_weight", "is_imputation_flag", "flags_variable", "unit", "unit_multiplier",
             "missing_codes"]


def t3_gold(item: dict) -> dict:
    return {k: item.get(k) for k in T3_FIELDS} | {"codes": item.get("code_list") or []}


def _norm(field, v):
    if field in {"unit", "flags_variable"}:
        return None if v in (None, "", "null", "None") else str(v)
    if field == "unit_multiplier":
        return None if v in (None, "", "null") else float(v)
    if field == "missing_codes":
        return sorted(str(x) for x in (v or []))
    return bool(v)


def t3_run_and_score(model: str, repeats: int, temperature: float, limit: int | None) -> pd.DataFrame:
    items = load_items()[:limit] if limit else load_items()
    cache = _load_cache(model)
    rows = []
    for rep in range(repeats):
        for it in items:
            rec = complete(model, t3_prompt(it), temperature=temperature, repeat=rep, cache=cache)
            js = parse_json(rec["response"]) or {}
            g = t3_gold(it)
            row = {"model": model, "repeat": rep, "dataset": it["dataset"], "name": it["name"]}
            for f in T3_FIELDS:
                row[f"ok_{f}"] = _norm(f, js.get(f)) == _norm(f, g[f])
            gc = {str(c) for c, _ in g["codes"]}
            pc = {str(c[0]) for c in js.get("codes", []) if isinstance(c, (list, tuple)) and c}
            row["codes_jaccard"] = len(gc & pc) / len(gc | pc) if (gc | pc) else 1.0
            rows.append(row)
    out = pd.DataFrame(rows)
    out.to_csv(RES / f"t3_{model.replace(':', '__')}.csv", index=False)
    return out


# ------------------------------------------------------------------------------------------------- CLI
def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["items", "baselines", "t2", "t3"])
    ap.add_argument("--model")
    ap.add_argument("--levels", nargs="+", default=["L0", "L1", "L2", "L3"])
    ap.add_argument("--repeats", type=int, default=5)
    ap.add_argument("--temperature", type=float, default=0.7)
    ap.add_argument("--limit", type=int)
    ap.add_argument("--embedding", action="store_true")
    a = ap.parse_args(argv)
    if a.cmd == "items":
        s = build_items()
        print(s.groupby("dataset").size(), "\n", s.gold.value_counts().head(15))
    elif a.cmd == "baselines":
        print(t2_baselines(a.embedding).round(3).to_string(index=False))
    elif a.cmd == "t2":
        t2_llm(a.model, a.levels, a.repeats, a.temperature, a.limit)
        res = t2_score(a.model, a.levels, a.repeats, a.temperature, a.limit)
        res.to_csv(RES / f"t2_{a.model.replace(':', '__')}.csv", index=False)
        print(res.round(3).to_string(index=False))
    elif a.cmd == "t3":
        res = t3_run_and_score(a.model, a.repeats, a.temperature, a.limit)
        print(res.filter(like="ok_").mean().round(3).to_string(), "\ncodes_jaccard", round(res.codes_jaccard.mean(), 3))
    return 0


if __name__ == "__main__":
    sys.exit(main())
