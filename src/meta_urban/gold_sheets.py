"""Blind annotation sheets for T2 gold, and merging them into adjudication files.

    python -m meta_urban.gold_sheets make     # benchmark/gold/annotation/annotator_{1,2}.csv
    python -m meta_urban.gold_sheets merge    # kappa, draft-change rates, t2_gold_<dataset>.csv for adjudication

Annotators see the variable (name, label, section, question, codes) and the concept vocabulary, but neither
the rule-based draft label nor any model output, so the gold is not anchored on either. Each annotator fills
`concept` (one id or `none`) and, for genuinely ambiguous variables only, `also_acceptable` (other ids,
separated by semicolons).
"""

from __future__ import annotations

import sys

import pandas as pd

from . import BENCH
from .bench import load_items
from .io import leaf_concepts
from .metrics import cohen_kappa

ANN = BENCH / "gold" / "annotation"
COLS = ["dataset", "name", "label", "section", "question", "codes", "concept", "also_acceptable", "comment"]


def _codes(it: dict) -> str:
    cl = it.get("code_list") or []
    if cl:
        s = "; ".join(f"{c}={v}" for c, v in cl[:12])
        return s + ("; ..." if len(cl) > 12 else "")
    return str(it.get("codes_raw") or "")[:200]


def make() -> None:
    ANN.mkdir(parents=True, exist_ok=True)
    items = load_items()
    base = pd.DataFrame([{"dataset": i["dataset"], "name": i["name"], "label": i.get("label") or "",
                          "section": i.get("section") or "", "question": i.get("question") or "",
                          "codes": _codes(i), "concept": "", "also_acceptable": "", "comment": ""} for i in items])
    for k in (1, 2):
        p = ANN / f"annotator_{k}.csv"
        if p.exists():
            print(f"{p} exists; not overwritten")
            continue
        base[COLS].to_csv(p, index=False, encoding="utf-8-sig")
        print(f"wrote {p} ({len(base)} variables)")
    vocab = pd.DataFrame([{"id": c["id"], "label": c.get("pref_label", ""), "broader": c.get("broader", ""),
                           "definition": c.get("definition", "")} for c in leaf_concepts()])
    vocab.to_csv(ANN / "concepts.csv", index=False, encoding="utf-8-sig")


def merge() -> None:
    a = pd.read_csv(ANN / "annotator_1.csv", dtype=str).fillna("")
    b = pd.read_csv(ANN / "annotator_2.csv", dtype=str).fillna("")
    m = a.merge(b, on=["dataset", "name"], suffixes=("_1", "_2"))
    done = m[(m.concept_1 != "") & (m.concept_2 != "")]
    valid = {c["id"] for c in leaf_concepts()} | {"none"}
    bad = sorted({x for x in pd.concat([done.concept_1, done.concept_2]) if x not in valid})
    if bad:
        print("Unknown concept ids (fix before merging):", bad)
        return
    items = {(i["dataset"], i["name"]): i for i in load_items()}
    draft = [items[(d, n)]["gold"] for d, n in zip(done.dataset, done.name)]
    print(f"annotated by both: {len(done)} of {len(m)}")
    print(f"Cohen's kappa: {cohen_kappa(list(done.concept_1), list(done.concept_2)):.3f}")
    print(f"raw agreement: {(done.concept_1 == done.concept_2).mean():.3f}")
    for k in ("1", "2"):
        print(f"annotator {k} differs from draft: {(done[f'concept_{k}'] != pd.Series(draft, index=done.index)).mean():.3f}")
    for ds, g in done.groupby("dataset"):
        out = BENCH / "gold" / f"t2_gold_{ds}.csv"
        prev = pd.read_csv(out, dtype=str).fillna("").set_index("name") if out.exists() else None
        rows = []
        for r in g.itertuples():
            agree = r.concept_1 == r.concept_2
            alts = sorted({x.strip() for x in (r.also_acceptable_1 + ";" + r.also_acceptable_2).split(";") if x.strip()}
                          - {r.concept_1} if agree else set())
            keep = prev is not None and r.name in prev.index and prev.at[r.name, "adjudicated"] != ""
            rows.append({"dataset": ds, "name": r.name, "label": r.label_1,
                         "annotator_1": r.concept_1, "annotator_2": r.concept_2,
                         "also_1": r.also_acceptable_1, "also_2": r.also_acceptable_2,
                         # agreed labels are adopted; disagreements stay empty until adjudicated in discussion
                         "adjudicated": prev.at[r.name, "adjudicated"] if keep else (r.concept_1 if agree else ""),
                         "also_acceptable": prev.at[r.name, "also_acceptable"] if keep else ";".join(alts),
                         "needs_adjudication": "" if (agree or keep) else "yes",
                         "notes": prev.at[r.name, "notes"] if keep else ""})
        pd.DataFrame(rows).to_csv(out, index=False, encoding="utf-8")
        print(f"wrote {out}: {sum(x['needs_adjudication'] == 'yes' for x in rows)} items need adjudication")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "make"
    {"make": make, "merge": merge}[cmd]()
