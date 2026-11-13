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
import time

import numpy as np
import pandas as pd

from . import BENCH
from .baselines import LexicalRetriever
from .codebooks import load_all
from .llm import approx_tokens, complete, load_cache, parse_json, t2_request, t3_request
from .metrics import acc_at_k, macro_f1, majority, mrr, none_pr, run_agreement

ITEMS = BENCH / "inputs" / "t2_t3_items.jsonl"
SAMPLE = BENCH / "inputs" / "t2_eval_sample.csv"
T3_EXTRA = BENCH / "inputs" / "t3_extra_sample.csv"
RES = BENCH / "results"
SEED = 20261112


# ------------------------------------------------------------------------------------------------- items
def gold_table() -> pd.DataFrame:
    """Current T2 gold: adjudicated labels where present, otherwise the rule-based draft.

    `also_acceptable` (semicolon-separated concept ids) records other concepts the adjudicators accept for an
    ambiguous variable; lenient accuracy counts them as correct.
    """
    parts = []
    for ds in ["cbecs2018", "recs2020"]:
        g = BENCH / "gold" / f"t2_gold_{ds}.csv"
        d = BENCH / "gold" / f"t2_draft_{ds}.csv"
        t = pd.read_csv(d, dtype=str).fillna("")
        t["gold"], t["gold_status"], t["also_acceptable"] = t["draft_concept"], "draft", ""
        if g.exists():
            a = pd.read_csv(g, dtype=str).fillna("").set_index(["dataset", "name"])
            t = t.set_index(["dataset", "name"])
            adj = a["adjudicated"].reindex(t.index).fillna("")
            t.loc[adj != "", "gold"] = adj[adj != ""]
            t.loc[adj != "", "gold_status"] = "adjudicated"
            if "also_acceptable" in a:
                t["also_acceptable"] = a["also_acceptable"].reindex(t.index).fillna("")
            t = t.reset_index()
        t["gold_ok"] = [[x] + [y.strip() for y in str(alt).split(";") if y.strip()]
                        for x, alt in zip(t["gold"], t["also_acceptable"])]
        parts.append(t[["dataset", "name", "gold", "gold_status", "gold_ok"]])
    return pd.concat(parts, ignore_index=True)


def build_items(per_dataset: int = 150, resample: bool = False) -> pd.DataFrame:
    """Write all codebook items and, on first use only, draw the 300-variable evaluation sample.

    The sample is frozen once drawn (it is stratified on the draft labels): later runs keep it, so that
    adjudicated gold and new model runs refer to the same variables. Pass resample=True to redraw it.
    """
    cb = load_all()
    g = gold_table().drop(columns="gold_ok")
    df = cb.merge(g, on=["dataset", "name"], how="left")
    ITEMS.parent.mkdir(parents=True, exist_ok=True)
    with open(ITEMS, "w", encoding="utf-8") as fh:
        for rec in df.to_dict("records"):
            rec = {k: (None if isinstance(v, float) and np.isnan(v) else v) for k, v in rec.items()}
            fh.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")
    if SAMPLE.exists() and not resample:
        return pd.read_csv(SAMPLE)
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
    # gold is read at load time, so adjudicated labels apply without rebuilding items or re-running models
    g = gold_table().set_index(["dataset", "name"])
    for i in items:
        k = (i["dataset"], i["name"])
        if k in g.index:
            i["gold"], i["gold_status"], i["gold_ok"] = g.at[k, "gold"], g.at[k, "gold_status"], g.at[k, "gold_ok"]
        else:
            i["gold_ok"] = [i["gold"]]
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


LEVELS = ["L0", "L1", "L2", "L3"]
K_CANDIDATES = 10


def _t2_jobs(levels, repeats, limit):
    items = load_items()[:limit] if limit else load_items()
    cands = LexicalRetriever().rank(items, k=K_CANDIDATES)
    jobs = []
    for level in levels:
        for rep in range(repeats):
            for it, cand in zip(items, cands):
                req = t2_request(it, level, cand if level == "L3" else None)
                meta = {"task": "T2", "level": level, "dataset": it["dataset"], "name": it["name"]}
                jobs.append((req, meta, rep))
    return jobs


def t3_items() -> list[dict]:
    """T3 items: the 300-variable sample plus a fixed supplement of the record-level variables it excludes.

    The T2 sample has no imputation flags or replicate weights, so on its own it would measure flag and weight
    detection only on negatives. The supplement adds 30 imputation flags and 15 replicate weights per survey
    and any final weights not already sampled (seed 20261113), drawn once and frozen in t3_extra_sample.csv.
    """
    base = load_items()
    for i in base:
        i["subset"] = "sample"
    allit = load_items(sample_only=False)
    insample = {(i["dataset"], i["name"]) for i in base}
    if not T3_EXTRA.exists():
        rng = np.random.default_rng(20261113)
        picks = []
        for ds in ["cbecs2018", "recs2020"]:
            for pred, n in [(lambda i: i["is_imputation_flag"], 30), (lambda i: i["is_replicate_weight"], 15),
                            (lambda i: i["is_weight"] and not i["is_replicate_weight"], 5)]:
                pool = [i for i in allit if i["dataset"] == ds and pred(i) and (i["dataset"], i["name"]) not in insample]
                picks += [pool[k] for k in sorted(rng.choice(len(pool), min(n, len(pool)), replace=False))]
        pd.DataFrame([{"dataset": i["dataset"], "name": i["name"]} for i in picks]).to_csv(T3_EXTRA, index=False)
    keep = set(map(tuple, pd.read_csv(T3_EXTRA)[["dataset", "name"]].values))
    extra = [dict(i, subset="supplement") for i in allit if (i["dataset"], i["name"]) in keep]
    return base + extra


def _t3_jobs(repeats, limit):
    items = t3_items()[:limit] if limit else t3_items()
    return [(t3_request(it), {"task": "T3", "dataset": it["dataset"], "name": it["name"]}, rep)
            for rep in range(repeats) for it in items]


def run_jobs(model: str, jobs: list, workers: int = 1) -> None:
    cache = load_cache(model)
    t0, done = time.time(), 0

    def tick():
        if done % 50 == 0:
            print(f"{model}: {done}/{len(jobs)} ({time.time() - t0:.0f}s)", flush=True)

    if workers <= 1:
        for req, meta, rep in jobs:
            complete(model, req, meta, rep, cache)
            done += 1
            tick()
        return
    from concurrent.futures import ThreadPoolExecutor, as_completed

    with ThreadPoolExecutor(workers) as ex:
        futs = [ex.submit(complete, model, req, meta, rep, cache) for req, meta, rep in jobs]
        for f in as_completed(futs):
            f.result()
            done += 1
            tick()


def plan(repeats: int, limit: int | None) -> pd.DataFrame:
    parts = []
    for task, jobs in [("T2", _t2_jobs(LEVELS, repeats, limit)), ("T3", _t3_jobs(min(repeats, 3), limit))]:
        df = pd.DataFrame([{"task": task, "level": m.get("level", "-"), "sys": approx_tokens(r["system"]),
                            "user": approx_tokens(r["user"])} for r, m, _ in jobs])
        g = df.groupby(["task", "level"]).agg(calls=("sys", "size"), system_tokens_each=("sys", "mean"),
                                              user_tokens_each=("user", "mean"))
        g["input_tokens_total_M"] = g.calls * (g.system_tokens_each + g.user_tokens_each) / 1e6
        parts.append(g)
    return pd.concat(parts).round(3)


def _records(model: str) -> pd.DataFrame:
    recs = list(load_cache(model).values())
    return pd.DataFrame(recs) if recs else pd.DataFrame()


def t2_score(model: str) -> pd.DataFrame:
    df = _records(model)
    if df.empty or "task" not in df:
        return pd.DataFrame()
    df = df[df.task == "T2"].copy()
    items = load_items()
    gold = {(i["dataset"], i["name"]): i["gold"] for i in items}
    df = df[[(d, n) in gold for d, n in zip(df.dataset, df.name)]].copy()
    df["gold"] = [gold[(d, n)] for d, n in zip(df.dataset, df.name)]
    parsed = df.response.map(parse_json)
    df["pred"] = parsed.map(lambda j: j.get("concept", "INVALID") if j else "INVALID")
    df["ranked"] = parsed.map(lambda j: ([j.get("concept")] + [a for a in j.get("alternatives", []) if isinstance(a, str)])
                              if j else ["INVALID"])
    rows = []
    for level, g in df.groupby("level"):
        piv = g.pivot_table(index=["dataset", "name"], columns="repeat", values="pred", aggfunc="first").dropna()
        if piv.empty:
            continue
        gl = [gold[k] for k in piv.index]
        runs = [list(piv[c]) for c in piv.columns]
        maj = [majority(list(row))[0] for row in piv.itertuples(index=False)]
        acc_reps = [float(np.mean([p == q for p, q in zip(run, gl)])) for run in runs]
        g0 = g[g.repeat == piv.columns[0]].drop_duplicates(["dataset", "name"]).set_index(["dataset", "name"]).loc[piv.index]
        mappable = [k for k, x in enumerate(gl) if x != "none"]
        npr = none_pr(maj, gl)
        tin = g.input_tokens.fillna(0).sum()
        cread = g["cache_read_input_tokens"].fillna(0).sum() if "cache_read_input_tokens" in g else 0.0
        rows.append({
            "model": model, "level": level, "n_items": len(piv), "repeats": len(runs),
            "acc@1_rep0": acc_reps[0], "acc@1_mean": float(np.mean(acc_reps)),
            "acc@1_sd": float(np.std(acc_reps, ddof=1)) if len(runs) > 1 else 0.0,
            "acc@1_majority": float(np.mean([m == x for m, x in zip(maj, gl)])),
            "acc@3_rep0": acc_at_k([g0.ranked.iloc[k] for k in mappable], [gl[k] for k in mappable], 3),
            "mrr_rep0": mrr([g0.ranked.iloc[k] for k in mappable], [gl[k] for k in mappable]),
            "macro_f1_majority": macro_f1(maj, gl),
            "none_precision": npr[0], "none_recall": npr[1],
            "invalid_rate": float((g.pred == "INVALID").mean()),
            **run_agreement(runs),
            "mean_latency_s": float(g.latency_s.mean()),
            "input_tokens_per_call": float((tin + cread) / len(g)),
            "cache_read_share": float(cread / max(1.0, tin + cread)),
            "gold_status": ",".join(sorted({i["gold_status"] for i in items})),
        })
    return pd.DataFrame(rows)


# ------------------------------------------------------------------------------------------------- T3
T3_FIELDS = ["is_weight", "is_replicate_weight", "is_imputation_flag", "flags_variable", "unit", "unit_multiplier",
             "missing_codes"]


def _norm(field, v):
    if field in {"unit", "flags_variable"}:
        return None if v in (None, "", "null", "None", "none") else str(v)
    if field == "unit_multiplier":
        try:
            v = float(v)
        except (TypeError, ValueError):
            return None
        return None if v == 0.0 else v
    if field == "missing_codes":
        return sorted(str(x) for x in (v or []))
    return bool(v)


def t3_score(model: str) -> pd.DataFrame:
    df = _records(model)
    if df.empty or "task" not in df:
        return pd.DataFrame()
    df = df[df.task == "T3"]
    items = {(i["dataset"], i["name"]): i for i in t3_items()}
    rows = []
    for r in df.itertuples():
        it = items.get((r.dataset, r.name))
        if it is None:
            continue
        js = parse_json(r.response) or {}
        row = {"model": model, "repeat": r.repeat, "dataset": r.dataset, "name": r.name, "subset": it["subset"],
               "valid": bool(js)}
        for f in T3_FIELDS:
            if f == "unit_multiplier" and it.get("unit") is None:
                row[f"ok_{f}"] = np.nan  # a multiplier is only meaningful when the variable has a unit
                continue
            row[f"ok_{f}"] = _norm(f, js.get(f)) == _norm(f, it.get(f))
        # lenient variant: ignore the blank-code convention ("" for 'Missing=...') on both sides
        strip = lambda v: sorted(str(x) for x in (v or []) if str(x) != "")  # noqa: E731
        row["ok_missing_codes_lenient"] = strip(js.get("missing_codes")) == strip(it.get("missing_codes"))
        gc = {str(c) for c, _ in (it.get("code_list") or [])}
        pc = {str(c[0]) for c in js.get("codes", []) if isinstance(c, (list, tuple)) and c}
        row["codes_jaccard"] = len(gc & pc) / len(gc | pc) if (gc | pc) else 1.0
        rows.append(row)
    return pd.DataFrame(rows)


def score_all() -> None:
    from .llm import CACHE_DIR

    t2, t3 = [], []
    for p in sorted(CACHE_DIR.glob("*.jsonl")):
        with open(p, encoding="utf-8") as fh:
            model = json.loads(fh.readline())["model"]
        s2 = t2_score(model)
        if not s2.empty:
            t2.append(s2)
        s3 = t3_score(model)
        if not s3.empty:
            agg = s3.filter(like="ok_").mean().to_dict() | {"codes_jaccard": s3.codes_jaccard.mean(),
                                                           "valid": s3.valid.mean(), "n": len(s3)}
            t3.append(pd.DataFrame([{"model": model, **agg}]))
    RES.mkdir(parents=True, exist_ok=True)
    if t2:
        T2 = pd.concat(t2)
        T2.to_csv(RES / "t2_llm_summary.csv", index=False)
        print(T2.round(3).to_string(index=False))
    if t3:
        T3 = pd.concat(t3)
        T3.to_csv(RES / "t3_llm_summary.csv", index=False)
        print(T3.round(3).to_string(index=False))


# ------------------------------------------------------------------------------------------------- CLI
def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["items", "baselines", "plan", "t2", "t3", "score"])
    ap.add_argument("--model")
    ap.add_argument("--levels", nargs="+", default=LEVELS)
    ap.add_argument("--repeats", type=int, default=5)
    ap.add_argument("--limit", type=int)
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--embedding", action="store_true")
    a = ap.parse_args(argv)
    if a.cmd == "items":
        s = build_items()
        print(s.groupby("dataset").size(), "\n", s.gold.value_counts().head(15))
    elif a.cmd == "baselines":
        print(t2_baselines(a.embedding).round(3).to_string(index=False))
    elif a.cmd == "plan":
        print(plan(a.repeats, a.limit).to_string())
    elif a.cmd == "t2":
        run_jobs(a.model, _t2_jobs(a.levels, a.repeats, a.limit), a.workers)
        print(t2_score(a.model).round(3).to_string(index=False))
    elif a.cmd == "t3":
        run_jobs(a.model, _t3_jobs(a.repeats, a.limit), a.workers)
        s3 = t3_score(a.model)
        print(s3.filter(like="ok_").mean().round(3).to_string(), "\ncodes_jaccard", round(s3.codes_jaccard.mean(), 3))
    elif a.cmd == "score":
        score_all()
    return 0


if __name__ == "__main__":
    sys.exit(main())
