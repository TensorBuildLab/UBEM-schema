"""Statistics added in response to the reviewers (paper Sections 5-7 and the supplement).

    python -m meta_urban.revision_stats

Writes to paper/tables/:
    stats_conditions.csv      per model x condition: strict and lenient acc@1, cluster-bootstrap 95% interval
                              (resampling gold concepts), per-survey accuracy, macro (per-concept) accuracy,
                              design-weighted accuracy (inverse sampling fractions of the concept strata), and how
                              the 5 variables with no applicable concept were answered
    stats_tests.csv           every paired comparison used in the paper, under each of four label sets, with exact
                              McNemar p and Holm-adjusted p (family: all comparisons x both models, per label set)
    stats_repeatability.csv   run-to-run variation among the temperature-0.7 repeats only
    stats_leakage.csv         accuracy on variables whose label does / does not contain a synonym or label of their
                              gold concept
    stats_e6_relations.csv    documentation transplant by SKOS relation of the transplanted term
    stats_e4_verification.csv quantity-kind checks on mappings, strict and lenient error basis
    stats_e7_confusion.csv    profile checks against consequential / harmless / exact profiles (E7)
    stats_e7_errors.csv       every E7 profile that changed an indicator
    stats_rules_heldout.csv   the frozen E7 rules applied to all code/unit normalization outputs of the benchmark,
                              excluding the 11 variables the rules were written on
All mapping statistics use temperature-0 outputs (repeat 0) unless stated.
"""

from __future__ import annotations

import csv
import re

import numpy as np
import pandas as pd

from . import BENCH, PAPER
from .bench import _records, load_items, parse_json, t3_items
from .bench_report import (concept_index, item_table, label_sources, mcnemar_exact, models, schema_check, short,
                           t2_frame)
from .io import leaf_concepts

TAB = PAPER / "tables"
RNG = np.random.default_rng(20261115)
CONDITIONS = ["L0", "L1", "L2D", "L2", "L2N", "O0", "O2D", "L2U", "L3", "XBR", "XBE", "XEA"]
COMPARISONS = [  # (condition, versus, experiment, question)
    ("L1", "L0", "E1", "labels over identifiers"),
    ("L2D", "L1", "E1", "definitions over labels"),
    ("L2", "L2D", "E1", "group, entity, unit and synonyms over definitions"),
    ("L2N", "L1", "E1", "group, entity, unit and synonyms over labels (no definitions)"),
    ("L2", "L2N", "E1", "definitions over the rest of the card"),
    ("O2D", "O0", "E1", "definitions with opaque codes"),
    ("L0", "O0", "E1", "meaningful identifiers over opaque codes"),
    ("L2U", "L2", "E2", "open versus closed output"),
    ("L3", "L2", "E5", "ten retrieved cards versus all cards"),
    ("XBR", "L0", "E6", "Brick documentation over identifiers"),
    ("XBE", "L0", "E6", "BEDES documentation over identifiers"),
    ("XEA", "L0", "E6", "Energy ADE documentation over identifiers"),
    ("XBR", "L2", "E6", "Brick documentation versus Meta-Urban cards"),
    ("XBE", "L2", "E6", "BEDES documentation versus Meta-Urban cards"),
    ("XEA", "L2", "E6", "Energy ADE documentation versus Meta-Urban cards"),
]


def holm(p: list[float]) -> list[float]:
    p = np.asarray(p, float)
    order = np.argsort(p)
    adj = np.empty_like(p)
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (len(p) - rank) * p[i]))
        adj[i] = running
    return list(adj)


def cluster_boot(hit: np.ndarray, cluster: np.ndarray, n: int = 2000) -> tuple[float, float]:
    """95% interval resampling whole clusters (gold concepts), so correlated variables are not counted as
    independent evidence."""
    ids = np.unique(cluster)
    groups = [hit[cluster == c] for c in ids]
    sums = np.array([g.sum() for g in groups])
    ns = np.array([len(g) for g in groups])
    draws = RNG.integers(0, len(ids), (n, len(ids)))
    acc = sums[draws].sum(1) / ns[draws].sum(1)
    return float(np.quantile(acc, 0.025)), float(np.quantile(acc, 0.975))


def design_weights() -> dict:
    """Inverse sampling fraction of each item's stratum (dataset x rule-based draft concept) in the frame of
    substantive variables (imputation flags and replicate weights excluded), as drawn in bench.build_items."""
    frame = []
    for ds in ("cbecs2018", "recs2020"):
        t = pd.read_csv(BENCH / "gold" / f"t2_draft_{ds}.csv", dtype=str).fillna("")
        frame.append(t.assign(dataset=ds)[["dataset", "name", "draft_concept"]])
    frame = pd.concat(frame)
    allit = {(i["dataset"], i["name"]): i for i in load_items(sample_only=False)}
    frame = frame[[not (allit[(d, n)]["is_imputation_flag"] or allit[(d, n)]["is_replicate_weight"])
                   for d, n in zip(frame.dataset, frame.name)]]
    sample = {(i["dataset"], i["name"]) for i in load_items()}
    frame["in_sample"] = [(d, n) in sample for d, n in zip(frame.dataset, frame.name)]
    N = frame.groupby(["dataset", "draft_concept"]).size()
    n = frame[frame.in_sample].groupby(["dataset", "draft_concept"]).size()
    w = (N / n).to_dict()
    s = frame[frame.in_sample]
    return {(d, nm): w[(d, c)] for d, nm, c in zip(s.dataset, s.name, s.draft_concept)}


def conditions_table(frames, tabs) -> pd.DataFrame:
    w = design_weights()
    rows = []
    for model, t in tabs.items():
        for lv in CONDITIONS:
            if lv not in t:
                continue
            it = t[lv]
            m = it[it.gold != "none"]
            hit = (m.pred0 == m.gold).values
            lo, hi = cluster_boot(hit, m.gold.values)
            per_concept = m.assign(h=hit).groupby("gold").h.mean()
            ww = np.array([w[k] for k in m.index])
            none = it[it.gold == "none"]
            rows.append({"model": short(model), "condition": lv, "n": len(m), "acc@1": hit.mean(),
                         "cluster_lo": lo, "cluster_hi": hi,
                         "lenient": float(np.mean([p in ok for p, ok in zip(m.pred0, m.gold_ok)])),
                         "acc_cbecs": hit[m.index.get_level_values(0) == "cbecs2018"].mean(),
                         "acc_recs": hit[m.index.get_level_values(0) == "recs2020"].mean(),
                         "macro_per_concept": per_concept.mean(), "concepts": len(per_concept),
                         "design_weighted": float((ww * hit).sum() / ww.sum()),
                         "none_items": len(none), "none_answered_none": int((none.pred0 == "none").sum()),
                         "false_none_on_mappable": int((m.pred0 == "none").sum())})
    return pd.DataFrame(rows)


def tests_table(tabs) -> pd.DataFrame:
    rows = []
    for src, lab in label_sources().items():
        block = []
        for model, t in tabs.items():
            for a, b, exp, q in COMPARISONS:
                if a not in t or b not in t:
                    continue
                common = t[a].index.intersection(t[b].index)
                ta, tb = t[a].loc[common], t[b].loc[common]
                idx = [k for k in common if lab[k][0] != "none"]
                ha = np.array([ta.at[k, "pred0"] == lab[k][0] for k in idx])
                hb = np.array([tb.at[k, "pred0"] == lab[k][0] for k in idx])
                n01, n10, p = mcnemar_exact(hb, ha)
                block.append({"label_set": src, "model": short(model), "experiment": exp, "condition": a,
                              "versus": b, "question": q, "n": len(idx), "acc_condition": ha.mean(),
                              "acc_versus": hb.mean(), "delta": ha.mean() - hb.mean(), "gained": n01, "lost": n10,
                              "p_exact": p})
        adj = holm([r["p_exact"] for r in block])
        for r, pa in zip(block, adj):
            r["p_holm"] = pa
        rows += block
    return pd.DataFrame(rows)


def repeatability(frames) -> pd.DataFrame:
    rows = []
    for model, df in frames.items():
        for lv in ("L0", "L1", "L2", "L3"):
            g = df[(df.level == lv)]
            piv = g.pivot_table(index=["dataset", "name"], columns="repeat", values="pred", aggfunc="first").dropna()
            gold = g.drop_duplicates(["dataset", "name"]).set_index(["dataset", "name"]).gold.loc[piv.index]
            mask = (gold != "none").values
            hot = [c for c in piv.columns if c >= 1]
            acc_hot = [float((piv[c] == gold).values[mask].mean()) for c in hot]
            agree = [float((piv[a] == piv[b]).mean()) for i, a in enumerate(hot) for b in hot[i + 1:]]
            rows.append({"model": short(model), "condition": lv, "runs_T0.7": len(hot),
                         "acc_T0": float((piv[0] == gold).values[mask].mean()),
                         "acc_T0.7_mean": float(np.mean(acc_hot)), "acc_T0.7_sd": float(np.std(acc_hot, ddof=1)),
                         "pairwise_agreement_T0.7_min": min(agree), "pairwise_agreement_T0.7_max": max(agree)})
    return pd.DataFrame(rows)


def leakage(tabs) -> pd.DataFrame:
    idx = {c["id"]: c for c in leaf_concepts()}
    items = {(i["dataset"], i["name"]): i for i in load_items()}

    def overlaps(k) -> bool:
        it = items[k]
        c = idx.get(it["gold"])
        if c is None:
            return False
        text = " " + re.sub(r"[^a-z0-9]+", " ", (it.get("label") or "").lower()) + " "
        phrases = [c["pref_label"]] + list(c.get("alt_labels") or [])
        return any(f" {re.sub(r'[^a-z0-9]+', ' ', p.lower()).strip()} " in text for p in phrases if p)

    rows = []
    for model, t in tabs.items():
        for lv in CONDITIONS:
            if lv not in t:
                continue
            m = t[lv][t[lv].gold != "none"]
            ov = np.array([overlaps(k) for k in m.index])
            hit = (m.pred0 == m.gold).values
            rows.append({"model": short(model), "condition": lv, "n_overlap": int(ov.sum()),
                         "n_no_overlap": int((~ov).sum()), "acc_overlap": hit[ov].mean(),
                         "acc_no_overlap": hit[~ov].mean()})
    return pd.DataFrame(rows)


def e6_relations(tabs) -> pd.DataFrame:
    from .standards import MAPPINGS, RELATION_ORDER, transplant_docs

    best = {}
    with open(MAPPINGS, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            k = (r["standard"], r["concept_id"])
            rank = RELATION_ORDER.index(r["relation"])
            if k not in best or rank < best[k][0]:
                best[k] = (rank, r["relation"])
    rows = []
    for model, t in tabs.items():
        for lv, std in (("XBR", "brick"), ("XBE", "bedes"), ("XEA", "energy_ade")):
            if lv not in t:
                continue
            docs = transplant_docs(std)
            base = t["L2"]
            for grp, rels in (("exact or close match", {"exactMatch", "closeMatch"}),
                              ("broad, narrow or related match", {"broadMatch", "narrowMatch", "relatedMatch"})):
                common = base.index.intersection(t[lv].index).intersection(t["L0"].index)
                keep = [k for k in common if base.at[k, "gold"] in docs
                        and best.get((std, base.at[k, "gold"]), (0, ""))[1].split(":")[-1] in rels]
                if not keep:
                    continue
                acc = {c: float(np.mean([t[c].at[k, "pred0"] == t[c].at[k, "gold"] for k in keep]))
                       for c in (lv, "L2", "L0")}
                rows.append({"model": short(model), "standard": std, "relation": grp, "n_variables": len(keep),
                             "concepts": len({base.at[k, 'gold'] for k in keep}), "acc_standard_docs": acc[lv],
                             "acc_meta_urban_cards": acc["L2"], "acc_ids_only": acc["L0"]})
    return pd.DataFrame(rows)


def e4_verification(tabs) -> pd.DataFrame:
    idx = concept_index()
    items = {(i["dataset"], i["name"]): i for i in t3_items()}
    rows = []
    for model, t in tabs.items():
        it = t["L2"]
        flag = np.array([schema_check(p, items[k], idx) for k, p in zip(it.index, it.pred0)])
        for basis in ("strict, 295 mappable variables", "lenient, all 300 variables"):
            if basis.startswith("strict"):
                mask = (it.gold != "none").values
                ok = (it.pred0 == it.gold).values
            else:
                mask = np.ones(len(it), bool)
                ok = np.array([p in g for p, g in zip(it.pred0, it.gold_ok)])
            f, o = flag[mask], ok[mask]
            rows.append({"model": short(model), "basis": basis, "wrong": int((~o).sum()),
                         "wrong_flagged": int((f & ~o).sum()), "recall_pct": 100 * (f & ~o).sum() / max(1, (~o).sum()),
                         "correct": int(o.sum()), "correct_flagged": int((f & o).sum()),
                         "false_alarm_pct": 100 * (f & o).sum() / max(1, o.sum()),
                         "precision_pct": 100 * (f & ~o).sum() / max(1, f.sum())})
    return pd.DataFrame(rows)


def e7_tables() -> tuple[pd.DataFrame, pd.DataFrame]:
    import json as _json

    from .checks import check as check_v2
    from .endtoend import _items

    e = pd.read_csv(TAB / "endtoend_profile_errors.csv")
    items = _items()
    e["flagged"] = e["flags"].fillna("") != ""
    e["flagged_v2"] = [bool(check_v2(items[(d, v)], _json.loads(p.replace("'", '"').replace("False", "false")
                                                                .replace("True", "true"))))
                       for d, v, p in zip(e.dataset, e.variable, e.ai_profile)]
    e["deviates"] = e["fields_wrong"].fillna("") != ""
    e["class"] = np.where(e.consequential, "changes an indicator",
                          np.where(e.deviates, "deviates, no effect on indicators", "identical to gold"))
    e["temperature"] = np.where(e.condition.str.contains("T=0.7"), 0.7, 0.0)
    conf = e.groupby(["temperature", "class"]).agg(profiles=("flagged", "size"), flagged_v1=("flagged", "sum"),
                                                   flagged_v2=("flagged_v2", "sum")).reset_index()
    tot = e.groupby("class").agg(profiles=("flagged", "size"), flagged_v1=("flagged", "sum"),
                                 flagged_v2=("flagged_v2", "sum")).reset_index()
    conf = pd.concat([conf, tot.assign(temperature="all")])
    errs = e[e.consequential][["model", "condition", "dataset", "variable", "fields_wrong", "max_effect_pct", "flags",
                               "ai_profile"]]
    return conf, errs


def rules_heldout() -> pd.DataFrame:
    """Frozen E7 rules on every normalization output of the benchmark (T3 and T3P, all runs), excluding the 11
    variables of the E7 pipeline on which the rules were written."""
    from .checks import check as check_v2
    from .endtoend import PIPE, profile_check

    e7 = {(ds, n) for ds, names in PIPE.items() for n in names}
    items = {(i["dataset"], i["name"]): i for i in t3_items()}
    rows = []
    for model in models():
        df = _records(model)
        df = df[df.task.isin(["T3", "T3P"])]
        for r in df.itertuples():
            k = (r.dataset, r.name)
            if k not in items or k in e7:
                continue
            it = items[k]
            js = parse_json(r.response) or {}
            prof = {"unit": js.get("unit") or "none", "unit_multiplier": js.get("unit_multiplier") or 0,
                    "missing_codes": [str(c) for c in (js.get("missing_codes") or [])]}
            gu = it.get("unit") or "none"
            unit_err = prof["unit"] != gu
            mult_err = gu != "none" and float(prof["unit_multiplier"] or 1) != float(it.get("unit_multiplier") or 1)
            gm = sorted(str(c) for c in (it.get("missing_codes") or []) if str(c) != "")
            pm = sorted(c for c in prof["missing_codes"] if c != "")
            for version, fn in (("v1 (frozen, held-out)", profile_check), ("v2 (revised, in-sample)", check_v2)):
                rows.append({"rules": version, "model": short(model), "task": r.task,
                             "temperature": 0.0 if r.repeat == 0 else 0.7,
                             "unit_or_multiplier_error": unit_err or mult_err, "missing_code_error": gm != pm,
                             "flagged": bool(fn(it, prof))})
    d = pd.DataFrame(rows)
    out = []
    for (version, model, temp), g in d.groupby(["rules", "model", "temperature"]):
        um = g[g.unit_or_multiplier_error]
        mc = g[g.missing_code_error & ~g.unit_or_multiplier_error]
        ok = g[~g.missing_code_error & ~g.unit_or_multiplier_error]
        out.append({"rules": version, "model": model, "temperature": temp, "profiles": len(g),
                    "unit_or_multiplier_errors": len(um), "flagged_pct_of_those": 100 * um.flagged.mean() if len(um) else np.nan,
                    "missing_code_errors_only": len(mc), "flagged_pct_of_missing_code_errors": 100 * mc.flagged.mean() if len(mc) else np.nan,
                    "correct_profiles": len(ok), "false_alarm_pct": 100 * ok.flagged.mean() if len(ok) else np.nan})
    return pd.DataFrame(out)


def main() -> int:
    frames = {m: f for m in models() if not (f := t2_frame(m)).empty}
    tabs = {m: {lv: item_table(df, lv) for lv in CONDITIONS if lv in set(df.level)} for m, df in frames.items()}
    out = {
        "stats_conditions": conditions_table(frames, tabs),
        "stats_tests": tests_table(tabs),
        "stats_repeatability": repeatability(frames),
        "stats_leakage": leakage(tabs),
        "stats_e6_relations": e6_relations(tabs),
        "stats_e4_verification": e4_verification(tabs),
        "stats_rules_heldout": rules_heldout(),
    }
    out["stats_e7_confusion"], out["stats_e7_errors"] = e7_tables()
    pd.set_option("display.width", 220)
    for name, d in out.items():
        d.to_csv(TAB / f"{name}.csv", index=False)
        show = d if name != "stats_tests" else d[d.label_set == "adjudicated gold"]
        print(f"\n== {name} ==\n{show.drop(columns=[c for c in ('ai_profile',) if c in show]).round(3).to_string(index=False)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
