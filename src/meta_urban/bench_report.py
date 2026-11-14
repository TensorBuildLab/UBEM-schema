"""Paper tables and figures from cached benchmark runs.

    python -m meta_urban.bench_report

Writes to paper/tables/ and paper/figures/:
    bench_t2_main.csv          T2 by model and context level (mappable items), with bootstrap 95% CIs
    bench_t2_tests.csv         paired exact McNemar tests between levels (repeat 0, temperature 0)
    bench_t2_l3_ceiling.csv    L3 accuracy split by whether the gold concept was among the retrieved candidates
    bench_t2_errors.csv        error types (exact, wrong concept in the same top-level group, false 'none', missed 'none', wrong)
    bench_t2_by_dataset.csv    Acc@1 by survey
    bench_t3_fields.csv        T3 field accuracy by model
    fig_t2_levels.png          Acc@1 by level and model, with baseline
    fig_t2_coverage.png        coverage-accuracy curve from vote share across repeats

All numbers carry the gold status of the labels they were scored against. Results on draft labels are
PROVISIONAL.
"""

from __future__ import annotations

import json
from math import comb

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from . import PAPER  # noqa: E402
from .analytics import GRID, INK2, MUTED, SURFACE, _style, save_fig  # noqa: E402
from .baselines import LexicalRetriever  # noqa: E402
from .bench import K_CANDIDATES, LEVELS, RES, _records, load_items, t3_items, t3_score  # noqa: E402
from .io import concept_index  # noqa: E402
from .llm import CACHE_DIR, parse_json  # noqa: E402
from .metrics import acc_at_k, macro_f1, majority, mrr, none_pr, run_agreement  # noqa: E402

TAB, FIG = PAPER / "tables", PAPER / "figures"
LEVEL_LABEL = {"L0": "L0 ids", "L1": "L1 +labels", "L2": "L2 full semantics", "L3": "L3 retrieve+rerank"}
MODEL_COLOR = {"ollama:qwen3:8b": "#256abf", "ollama:llama3.1:8b": "#e5803a"}
RNG = np.random.default_rng(20261113)


def models() -> list[str]:
    out = []
    for p in sorted(CACHE_DIR.glob("*.jsonl")):
        with open(p, encoding="utf-8") as fh:
            out.append(json.loads(fh.readline())["model"])
    return out


def short(model: str) -> str:
    return model.split(":", 1)[1]


def boot_ci(hits: np.ndarray, n: int = 2000) -> tuple[float, float]:
    idx = RNG.integers(0, len(hits), (n, len(hits)))
    m = hits[idx].mean(1)
    return float(np.quantile(m, 0.025)), float(np.quantile(m, 0.975))


def mcnemar_exact(a: np.ndarray, b: np.ndarray) -> tuple[int, int, float]:
    """Two-sided exact McNemar test on paired correctness vectors."""
    n01 = int(((~a) & b).sum())
    n10 = int((a & ~b).sum())
    n = n01 + n10
    if n == 0:
        return n01, n10, 1.0
    k = min(n01, n10)
    p = 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n
    return n01, n10, min(1.0, p)


def t2_frame(model: str) -> pd.DataFrame:
    """One row per (level, item, repeat) with prediction, ranked list and confidence."""
    df = _records(model)
    if df.empty:
        return df
    df = df[df.task == "T2"].copy()
    items = {(i["dataset"], i["name"]): i for i in load_items()}
    df = df[[(d, n) in items for d, n in zip(df.dataset, df.name)]].copy()
    df["gold"] = [items[(d, n)]["gold"] for d, n in zip(df.dataset, df.name)]
    df["gold_ok"] = [items[(d, n)]["gold_ok"] for d, n in zip(df.dataset, df.name)]
    js = df.response.map(parse_json)
    df["pred"] = js.map(lambda j: j.get("concept", "INVALID") if j else "INVALID")
    df["ranked"] = js.map(lambda j: [j.get("concept")] + [a for a in j.get("alternatives", []) if isinstance(a, str)]
                          if j else ["INVALID"])
    df["conf"] = js.map(lambda j: float(j.get("confidence", np.nan)) if j else np.nan)
    df["model"] = model
    return df


def item_table(df: pd.DataFrame, level: str) -> pd.DataFrame:
    """Per-item view for one level: repeat-0 prediction, majority vote and vote share."""
    g = df[df.level == level]
    piv = g.pivot_table(index=["dataset", "name"], columns="repeat", values="pred", aggfunc="first").dropna()
    r0 = g[g.repeat == 0].drop_duplicates(["dataset", "name"]).set_index(["dataset", "name"]).loc[piv.index]
    out = pd.DataFrame(index=piv.index)
    out["gold"] = r0.gold
    out["gold_ok"] = r0.gold_ok
    out["pred0"] = r0.pred
    out["ranked0"] = r0.ranked
    out["conf0"] = r0.conf
    votes = [majority(list(row)) for row in piv.itertuples(index=False)]
    out["maj"] = [v[0] for v in votes]
    out["share"] = [v[1] for v in votes]
    out["runs"] = [list(row) for row in piv.itertuples(index=False)]
    return out


def gold_status() -> str:
    return ",".join(sorted({i["gold_status"] for i in load_items()}))


# ------------------------------------------------------------------------------------------------ tables
def t2_main(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    items = load_items()
    lex = LexicalRetriever().rank(items, k=K_CANDIDATES)
    gold = [i["gold"] for i in items]
    pos = [k for k, g in enumerate(gold) if g != "none"]
    hits = np.array([lex[k][0] == gold[k] for k in pos])
    lo, hi = boot_ci(hits)
    oks = [i["gold_ok"] for i in items]
    rows.append({"model": "lexical TF-IDF", "level": "-", "n_mappable": len(pos), "acc@1": hits.mean(),
                 "acc@1_lenient": float(np.mean([lex[k][0] in oks[k] for k in pos])),
                 "acc@1_lo": lo, "acc@1_hi": hi, "acc@1_mean5": np.nan, "acc@1_sd5": np.nan,
                 "acc@3": acc_at_k([lex[k] for k in pos], [gold[k] for k in pos], 3),
                 "mrr": mrr([lex[k] for k in pos], [gold[k] for k in pos]),
                 "macro_f1_all": macro_f1([r[0] for r in lex], gold), "none_recall": 0.0,
                 "pairwise_agreement": 1.0, "input_tokens_per_call": 0.0})
    for model, df in frames.items():
        for level in LEVELS:
            if level not in set(df.level):
                continue
            it = item_table(df, level)
            m = it[it.gold != "none"]
            h = (m.pred0 == m.gold).values
            lo, hi = boot_ci(h)
            reps = [np.mean([r[k] == gld for gld, r in zip(m.gold, m.runs)]) for k in range(len(m.runs.iloc[0]))]
            rows.append({
                "model": short(model), "level": level, "n_mappable": len(m), "acc@1": h.mean(),
                "acc@1_lenient": np.mean([p in ok for p, ok in zip(m.pred0, m.gold_ok)]),
                "acc@1_lo": lo, "acc@1_hi": hi, "acc@1_mean5": np.mean(reps), "acc@1_sd5": np.std(reps, ddof=1),
                "acc@3": acc_at_k(list(m.ranked0), list(m.gold), 3), "mrr": mrr(list(m.ranked0), list(m.gold)),
                "macro_f1_all": macro_f1(list(it.pred0), list(it.gold)),
                "none_recall": none_pr(list(it.pred0), list(it.gold))[1],
                "pairwise_agreement": run_agreement([list(c) for c in zip(*it.runs)])["pairwise_agreement"],
                "input_tokens_per_call": df[df.level == level].input_tokens.mean(),
            })
    out = pd.DataFrame(rows)
    out["gold_status"] = gold_status()
    return out


def t2_tests(frames) -> pd.DataFrame:
    rows = []
    pairs = [("L0", "L1"), ("L1", "L2"), ("L0", "L2"), ("L2", "L3")]
    for model, df in frames.items():
        tabs = {lv: item_table(df, lv) for lv in LEVELS if lv in set(df.level)}
        for a, b in pairs:
            if a not in tabs or b not in tabs:
                continue
            ta, tb = tabs[a], tabs[b].loc[tabs[a].index]
            mask = (ta.gold != "none").values
            ha = (ta.pred0 == ta.gold).values[mask]
            hb = (tb.pred0 == tb.gold).values[mask]
            n01, n10, p = mcnemar_exact(ha, hb)
            rows.append({"model": short(model), "a": a, "b": b, "acc_a": ha.mean(), "acc_b": hb.mean(),
                         "delta": hb.mean() - ha.mean(), "b_only_correct": n01, "a_only_correct": n10, "p_exact": p})
    # between models at the same level
    ms = list(frames)
    if len(ms) == 2:
        for lv in LEVELS:
            try:
                ta, tb = item_table(frames[ms[0]], lv), item_table(frames[ms[1]], lv)
            except KeyError:
                continue
            idx = ta.index.intersection(tb.index)
            ta, tb = ta.loc[idx], tb.loc[idx]
            mask = (ta.gold != "none").values
            ha, hb = (ta.pred0 == ta.gold).values[mask], (tb.pred0 == tb.gold).values[mask]
            n01, n10, p = mcnemar_exact(ha, hb)
            rows.append({"model": f"{short(ms[0])} vs {short(ms[1])}", "a": lv, "b": lv, "acc_a": ha.mean(),
                         "acc_b": hb.mean(), "delta": hb.mean() - ha.mean(), "b_only_correct": n01,
                         "a_only_correct": n10, "p_exact": p})
    return pd.DataFrame(rows)


def t2_l3_ceiling(frames) -> pd.DataFrame:
    items = load_items()
    cands = LexicalRetriever().rank(items, k=K_CANDIDATES)
    incand = {(i["dataset"], i["name"]): i["gold"] in c for i, c in zip(items, cands)}
    rows = []
    for model, df in frames.items():
        for lv in ("L2", "L3"):
            if lv not in set(df.level):
                continue
            it = item_table(df, lv)
            it = it[it.gold != "none"]
            flag = np.array([incand[k] for k in it.index])
            hit = (it.pred0 == it.gold).values
            rows.append({"model": short(model), "level": lv, "gold_in_candidates_n": int(flag.sum()),
                         "acc_if_in_candidates": hit[flag].mean(), "gold_not_in_candidates_n": int((~flag).sum()),
                         "acc_if_not_in_candidates": hit[~flag].mean()})
    return pd.DataFrame(rows)


def _error_type(pred: str, gold: str, idx: dict) -> str:
    if pred == gold:
        return "exact"
    if pred == "INVALID":
        return "invalid"
    if gold == "none":
        return "missed_none"
    if pred == "none":
        return "false_none"
    return "same_group" if _group(pred, idx) == _group(gold, idx) else "other_group"


def _group(c: str, idx: dict) -> str | None:
    """Top-level grouping concept (weather, geometry, characteristics, systems, energy, ...)."""
    seen = set()
    while c in idx and idx[c].get("broader") and c not in seen:
        seen.add(c)
        c = idx[c]["broader"]
    return c


def t2_errors(frames) -> pd.DataFrame:
    idx = concept_index()
    rows = []
    for model, df in frames.items():
        for lv in LEVELS:
            if lv not in set(df.level):
                continue
            it = item_table(df, lv)
            et = pd.Series([_error_type(p, g, idx) for p, g in zip(it.pred0, it.gold)])
            row = {"model": short(model), "level": lv, "n": len(it)}
            row.update(et.value_counts(normalize=True).reindex(
                ["exact", "same_group", "other_group", "false_none", "missed_none", "invalid"]).fillna(0).to_dict())
            rows.append(row)
    return pd.DataFrame(rows)


def t2_by_dataset(frames) -> pd.DataFrame:
    rows = []
    for model, df in frames.items():
        for lv in LEVELS:
            if lv not in set(df.level):
                continue
            it = item_table(df, lv).reset_index()
            it = it[it.gold != "none"]
            for ds, g in it.groupby("dataset"):
                rows.append({"model": short(model), "level": lv, "dataset": ds, "n": len(g),
                             "acc@1": (g.pred0 == g.gold).mean()})
    return pd.DataFrame(rows).pivot_table(index=["model", "level"], columns="dataset", values="acc@1").reset_index()


def t3_fields() -> pd.DataFrame:
    """T3 accuracy by field, each computed on the items where the field is informative.

    Detection fields are split into recall on positives (mostly the supplement of flags and weights) and the
    false-positive rate on the 300-variable sample; units on items that have a unit; multipliers on items whose
    unit is scaled (thousand Btu, hundred cubic feet).
    """
    items = {(i["dataset"], i["name"]): i for i in t3_items()}
    rows = []
    for model in models():
        s3 = t3_score(model)
        if s3.empty:
            continue
        it = [items[(d, n)] for d, n in zip(s3.dataset, s3.name)]
        g = lambda f: np.array([bool(i.get(f)) for i in it])  # noqa: E731
        row = {"model": short(model), "n_calls": len(s3), "valid": s3.valid.mean()}
        for f in ("is_weight", "is_replicate_weight", "is_imputation_flag"):
            pos = g(f)
            row[f"{f}_recall"] = s3.loc[pos, f"ok_{f}"].mean() if pos.any() else np.nan
            row[f"{f}_n_pos"] = int(pos.sum())
            row[f"{f}_fp_rate"] = 1 - s3.loc[~pos, f"ok_{f}"].mean()
        flag = g("is_imputation_flag")
        row["flags_variable_acc"] = s3.loc[flag, "ok_flags_variable"].mean() if flag.any() else np.nan
        for ds in ("cbecs2018", "recs2020"):  # CBECS labels describe the variable; RECS labels name it
            m = flag & (s3.dataset == ds).values
            row[f"flags_variable_acc_{ds}"] = s3.loc[m, "ok_flags_variable"].mean() if m.any() else np.nan
        has_unit = np.array([i.get("unit") is not None for i in it])
        row["unit_acc"] = s3.loc[has_unit, "ok_unit"].mean()
        row["unit_n"] = int(has_unit.sum())
        row["spurious_unit_rate"] = 1 - s3.loc[~has_unit, "ok_unit"].mean()
        scaled = np.array([(i.get("unit_multiplier") or 1) != 1 for i in it])
        row["multiplier_acc_scaled"] = s3.loc[scaled, "ok_unit_multiplier"].mean() if scaled.any() else np.nan
        row["multiplier_n_scaled"] = int(scaled.sum())
        row["multiplier_acc_all_units"] = s3.loc[has_unit, "ok_unit_multiplier"].mean()
        row["missing_codes_exact"] = s3.ok_missing_codes.mean()
        row["missing_codes_lenient"] = s3.ok_missing_codes_lenient.mean()
        row["codes_jaccard"] = s3.codes_jaccard.mean()
        rows.append(row)
    return pd.DataFrame(rows)


# ------------------------------------------------------------------------------------------------ figures
def fig_levels(main: pd.DataFrame, path) -> None:
    fig, ax = plt.subplots(figsize=(7.0, 3.4), dpi=200)
    llm = main[main.level != "-"]
    ms = list(dict.fromkeys(llm.model))
    w = 0.8 / max(1, len(ms))
    x = np.arange(len(LEVELS))
    for k, m in enumerate(ms):
        d = llm[llm.model == m].set_index("level").reindex(LEVELS)
        col = MODEL_COLOR.get(f"ollama:{m}", "#3987e5")
        xs = x - 0.4 + w * (k + 0.5)
        ax.bar(xs, d["acc@1"], width=w * 0.9, color=col, label=m, edgecolor=SURFACE)
        ax.errorbar(xs, d["acc@1"], yerr=[d["acc@1"] - d["acc@1_lo"], d["acc@1_hi"] - d["acc@1"]],
                    fmt="none", ecolor=INK2, elinewidth=0.8, capsize=2)
        for xi, v in zip(xs, d["acc@1"]):
            pass
        for xi, v, h in zip(xs, d["acc@1"], d["acc@1_hi"]):
            ax.text(xi, h + 0.015, f"{v:.2f}", ha="center", fontsize=6.5, color=INK2)
    base = main[main.level == "-"]["acc@1"].iloc[0]
    ax.axhline(base, color=MUTED, linestyle="--", linewidth=0.9, label=f"lexical baseline ({base:.2f})")
    ax.set_xticks(x, [LEVEL_LABEL[lv] for lv in LEVELS], fontsize=7.5)
    ax.set_ylim(0, 1)
    ax.set_ylabel("Top-1 accuracy (mappable items)", fontsize=8, color=INK2)
    ax.yaxis.grid(True, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    _style(ax)
    ax.legend(fontsize=7, frameon=False, loc="upper left")
    fig.tight_layout()
    save_fig(fig, path)
    plt.close(fig)


def fig_coverage(frames, path, level: str = "L2") -> pd.DataFrame:
    """Coverage-accuracy trade-off when only some mappings are accepted automatically and the rest go to a human.

    Signals: the model's own confidence (threshold sweep), unanimity of its five repeats, and agreement across
    context levels (L2 = L3) and across models (all runs at L2 and L3 agree).
    """
    fig, ax = plt.subplots(figsize=(5.6, 3.6), dpi=200)
    rows = []
    tabs = {m: {lv: item_table(df, lv) for lv in ("L2", "L3") if lv in set(df.level)} for m, df in frames.items()}
    idx = None
    for m in tabs:
        idx = tabs[m][level].index if idx is None else idx.intersection(tabs[m][level].index)

    def add(model, signal, mask, ok, param=np.nan):
        rows.append({"model": model, "level": level, "signal": signal, "param": param,
                     "coverage": float(mask.mean()), "accuracy": float(ok[mask].mean()) if mask.any() else np.nan})

    for model, t in tabs.items():
        it = t[level].loc[idx]
        ok = (it.pred0 == it.gold).values
        col = MODEL_COLOR.get(model, "#3987e5")
        pts = []
        for th in [0.0, 0.5, 0.7, 0.8, 0.85, 0.9, 0.95]:
            mask = (it.conf0.fillna(0) >= th).values
            if mask.any():
                add(short(model), "confidence", mask, ok, th)
                pts.append((mask.mean(), ok[mask].mean()))
        ax.plot(*zip(*pts), marker="o", markersize=3, linewidth=1.3, color=col, label=f"{short(model)}: own confidence")
        mask = (it.share == 1.0).values
        add(short(model), "repeats_unanimous", mask, ok)
        ax.scatter(mask.mean(), ok[mask].mean(), marker="s", s=22, color=col, zorder=3)
        if "L3" in t:
            mask = (it.pred0.values == t["L3"].loc[idx].pred0.values)
            add(short(model), "L2_equals_L3", mask, ok)
            ax.scatter(mask.mean(), ok[mask].mean(), marker="^", s=26, color=col, zorder=3)
    ms = list(tabs)
    if len(ms) >= 2:
        base = tabs[ms[0]][level].loc[idx]
        ok = (base.pred0 == base.gold).values
        preds = [tabs[m][lv].loc[idx].pred0.values for m in ms for lv in tabs[m]]
        mask = np.all([p == preds[0] for p in preds], axis=0)
        add("all", "all_models_and_levels_agree", mask, ok)
        ax.scatter(mask.mean(), ok[mask].mean(), marker="D", s=26, color=INK2, zorder=3)
    from matplotlib.lines import Line2D
    handles, _ = ax.get_legend_handles_labels()
    handles += [Line2D([], [], marker="s", linestyle="", color=MUTED, label="five repeats unanimous"),
                Line2D([], [], marker="^", linestyle="", color=MUTED, label="L2 and L3 agree"),
                Line2D([], [], marker="D", linestyle="", color=INK2, label="both models, L2 and L3 agree")]
    ax.legend(handles=handles, fontsize=6.5, frameon=False, loc="lower left")
    ax.set_xlabel("Share of variables mapped automatically", fontsize=8, color=INK2)
    ax.set_ylabel("Accuracy of automatic mappings", fontsize=8, color=INK2)
    ax.set_xlim(0, 1.02)
    ax.set_ylim(0, 1.02)
    ax.grid(True, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    _style(ax)
    fig.tight_layout()
    save_fig(fig, path)
    plt.close(fig)
    return pd.DataFrame(rows)


UNIT_DIM = {"unit:BTU_IT": "Energy", "unit:KiloW-HR": "Energy", "unit:FT3": "Energy", "unit:GAL_US": "Energy",
            "iso4217:USD": "Currency", "unit:FT2": "Area", "unit:DEG_F": "Temperature", "unit:HR": "Time"}
UNIT_BEARING = {"Energy", "Currency", "Area", "Temperature", "Power", "Irradiance", "Pressure", "Speed", "Length"}


def concept_dim(c: dict) -> str | None:
    if c.get("canonical_unit") == "unit:CCY_USD":
        return "Currency"
    if c.get("canonical_unit") == "unit:KiloW-HR-PER-M2":
        return "EnergyIntensity"
    q = c.get("quantity_kind")
    return q.split(":")[1] if q else None


def schema_check(concept: str, item: dict, idx: dict) -> bool:
    """True if the schema's unit/quantity rules reject mapping `item` to `concept` (a verifiable inconsistency).

    The variable's unit comes from its profile (codebook-derived); the concept's dimension from its quantity
    kind or canonical unit. Rejected: a unit-bearing variable mapped to a categorical concept or to a concept of
    another dimension, and a categorical variable without a unit mapped to a unit-bearing quantity."""
    if concept in ("none", "INVALID") or concept not in idx:
        return False
    vdim = UNIT_DIM.get(item.get("unit"))
    cdim = concept_dim(idx[concept])
    if vdim:
        return cdim is None or (cdim != vdim and not (cdim == "Count" and vdim == "Time"))
    return bool(item.get("code_list")) and cdim in UNIT_BEARING


def t2_verification(frames) -> pd.DataFrame:
    """How many wrong mappings the schema's own constraints catch, and at what false-alarm cost."""
    idx = concept_index()
    items = {(i["dataset"], i["name"]): i for i in t3_items()}
    rows = []
    for model, df in frames.items():
        for lv in LEVELS:
            if lv not in set(df.level):
                continue
            it = item_table(df, lv)
            flag = np.array([schema_check(p, items[k], idx) for k, p in zip(it.index, it.pred0)])
            ok = np.array([p in g for p, g in zip(it.pred0, it.gold_ok)])
            rows.append({"model": short(model), "level": lv, "n": len(it), "wrong": int((~ok).sum()),
                         "wrong_flagged": int((flag & ~ok).sum()),
                         "wrong_flagged_pct": 100 * (flag & ~ok).sum() / max(1, (~ok).sum()),
                         "correct_flagged_pct": 100 * (flag & ok).sum() / max(1, ok.sum()),
                         "accuracy_after_review": float((ok | flag).mean()) if False else float(ok.mean())})
    return pd.DataFrame(rows)


def label_sources() -> dict[str, dict]:
    """Alternative label sets for a sensitivity analysis: (dataset, name) -> (label, acceptable labels)."""
    from . import BENCH

    ann = BENCH / "gold" / "annotation"
    src = {}
    items = load_items()
    src["adjudicated gold"] = {(i["dataset"], i["name"]): (i["gold"], set(i["gold_ok"])) for i in items}
    for k in (1, 2):
        t = pd.read_csv(ann / f"annotator_{k}.csv", dtype=str).fillna("")
        src[f"annotator {k} alone"] = {
            (d, n): (c, {c} | {x.strip() for x in a.split(";") if x.strip()})
            for d, n, c, a in zip(t.dataset, t.name, t.concept, t.also_acceptable)}
    draft = {}
    for ds in ("cbecs2018", "recs2020"):
        t = pd.read_csv(BENCH / "gold" / f"t2_draft_{ds}.csv", dtype=str).fillna("")
        draft.update({(ds, n): (c, {c}) for n, c in zip(t.name, t.draft_concept)})
    src["rule-based draft (keyword rules)"] = {k: draft[k] for k in src["adjudicated gold"]}
    return src


def t2_label_sensitivity(frames) -> pd.DataFrame:
    """Do the T2 conclusions hold whichever label set is used? Strict and lenient Acc@1 at repeat 0, and exact
    McNemar p for the two contrasts the paper relies on (L0 vs L2, L2 vs L3)."""
    rows = []
    tabs = {m: {lv: item_table(df, lv) for lv in LEVELS if lv in set(df.level)} for m, df in frames.items()}
    for src_name, lab in label_sources().items():
        for model, t in tabs.items():
            idx = [k for k in t["L0"].index if lab[k][0] != "none"]
            hit = {lv: np.array([t[lv].at[k, "pred0"] == lab[k][0] for k in idx]) for lv in t}
            len_ = {lv: np.mean([t[lv].at[k, "pred0"] in lab[k][1] for k in idx]) for lv in t}
            row = {"labels": src_name, "model": short(model), "n": len(idx)}
            for lv in LEVELS:
                row[f"acc_{lv}"] = hit[lv].mean()
                row[f"lenient_{lv}"] = len_[lv]
            row["p_L0_vs_L2"] = mcnemar_exact(hit["L0"], hit["L2"])[2]
            row["p_L2_vs_L3"] = mcnemar_exact(hit["L2"], hit["L3"])[2]
            rows.append(row)
    return pd.DataFrame(rows)


def main() -> int:
    frames = {m: t2_frame(m) for m in models()}
    frames = {m: f for m, f in frames.items() if not f.empty}
    TAB.mkdir(parents=True, exist_ok=True)
    out = {
        "bench_t2_main": t2_main(frames),
        "bench_t2_tests": t2_tests(frames),
        "bench_t2_l3_ceiling": t2_l3_ceiling(frames),
        "bench_t2_errors": t2_errors(frames),
        "bench_t2_by_dataset": t2_by_dataset(frames),
        "bench_t3_fields": t3_fields(),
        "bench_t2_label_sensitivity": t2_label_sensitivity(frames),
        "bench_t2_verification": t2_verification(frames),
    }
    fig_levels(out["bench_t2_main"], FIG / "fig_t2_levels.png")
    out["bench_t2_coverage"] = fig_coverage(frames, FIG / "fig_t2_coverage.png")
    for name, df in out.items():
        df.to_csv(TAB / f"{name}.csv", index=False)
        print(f"\n== {name} ==\n{df.round(3).to_string(index=False)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
