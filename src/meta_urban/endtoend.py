"""E7: from AI-built variable profiles to UBEM quantities (paper Section 7).

A small UBEM input pipeline reads only the variable profiles (weight, unit, multiplier, missing codes) and
computes national building-stock quantities from the CBECS 2018 and RECS 2020 microdata. The profiles come
either from the gold codebook normalization (reference) or from a language model's normalization of the
codebook entry, with or without the dataset card. Any difference in the result is caused by the AI-built
profile alone.

    python -m meta_urban.endtoend            # runs the few missing model calls (cached), writes tables
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from . import DATA_RAW, PAPER
from .bench import load_items, parse_json
from .llm import complete, load_cache, t3_request

PIPE = {"cbecs2018": ["FINALWT", "SQFT", "MFBTU", "ELBTU", "NGBTU", "PUBCLIM"],
        "recs2020": ["NWEIGHT", "TOTSQFT_EN", "TOTALBTU", "BTUEL", "BTUNG"]}
MODELS = ["ollama:qwen3:8b", "ollama:llama3.1:8b"]
TO_KWH = {"unit:BTU_IT": 1 / 3412.141633, "unit:KiloW-HR": 1.0, "unit:FT3": 1037 / 3412.141633}  # gas heat content
TO_M2 = {"unit:FT2": 0.09290304}
FILES = {"cbecs2018": "cbecs2018_final_public.csv", "recs2020": "recs2020_public_v7.csv"}


def _items() -> dict:
    allit = {(i["dataset"], i["name"]): i for i in load_items(sample_only=False)}
    return {k: allit[k] for ds, names in PIPE.items() for k in [(ds, n) for n in names]}


def gold_profile(item: dict) -> dict:
    return {"is_weight": bool(item["is_weight"]), "unit": item.get("unit") or "none",
            "unit_multiplier": item.get("unit_multiplier") or 0, "missing_codes": item.get("missing_codes") or []}


def ai_profiles(model: str, profile: bool, repeat: int) -> dict:
    cache = load_cache(model)
    out = {}
    for (ds, name), it in _items().items():
        meta = {"task": "T3P" if profile else "T3", "dataset": ds, "name": name}
        rec = complete(model, t3_request(it, profile=profile), meta, repeat, cache)
        js = parse_json(rec["response"]) or {}
        out[(ds, name)] = {"is_weight": bool(js.get("is_weight")), "unit": js.get("unit") or "none",
                           "unit_multiplier": js.get("unit_multiplier") or 0,
                           "missing_codes": [str(c) for c in (js.get("missing_codes") or [])]}
    return out


def _clean(s: pd.Series, prof: dict) -> pd.Series:
    codes = {c for c in prof["missing_codes"] if c != ""}
    if not codes:
        return s
    as_str = s.map(lambda v: "" if pd.isna(v) else (str(int(v)) if float(v).is_integer() else str(v)))
    return s.where(~as_str.isin(codes))


def _factor(prof: dict, table: dict) -> float:
    """Raw value -> target unit; NaN if the profile gives no usable unit (the quantity cannot be computed)."""
    f = table.get(prof["unit"])
    if f is None:
        return np.nan
    m = prof["unit_multiplier"] or 1
    return f * float(m)


def quantities(ds: str, prof: dict, df: pd.DataFrame) -> dict:
    p = {n: prof[(ds, n)] for n in PIPE[ds]}
    wname = "FINALWT" if ds == "cbecs2018" else "NWEIGHT"
    w = df[wname] if p[wname]["is_weight"] else pd.Series(1.0, index=df.index)
    area_n = "SQFT" if ds == "cbecs2018" else "TOTSQFT_EN"
    area = _clean(df[area_n], p[area_n]) * _factor(p[area_n], TO_M2)

    def energy(n):  # kWh per record
        return _clean(df[n], p[n]) * _factor(p[n], TO_KWH)

    q = {}
    if ds == "cbecs2018":
        tot_area = (w * area).sum()
        q["Buildings (thousand)"] = w.sum() / 1e3
        q["Floor area (million m2)"] = tot_area / 1e6
        for n, lab in (("MFBTU", "major fuels"), ("ELBTU", "electricity"), ("NGBTU", "natural gas")):
            q[f"EUI, {lab} (kWh/m2)"] = (w * energy(n)).sum(min_count=1) / tot_area
        pc = _clean(df["PUBCLIM"], p["PUBCLIM"])
        q["Share in hot or very hot zone (%)"] = 100 * (w * (pc == 5)).sum() / w[pc.notna()].sum()
    else:
        hh = w.sum()
        q["Households (million)"] = hh / 1e6
        for n, lab in (("TOTALBTU", "site energy"), ("BTUEL", "electricity"), ("BTUNG", "natural gas")):
            e = energy(n)
            q[f"{lab.capitalize()} per household (MWh)"] = (w * e).sum(min_count=1) / w[e.notna()].sum() / 1e3
        q["Site EUI (kWh/m2)"] = (w * energy("TOTALBTU")).sum(min_count=1) / (w * area).sum()
    return {k: (np.nan if v is None or not np.isfinite(v) else v) for k, v in q.items()}


UNIT_WORDS = {"unit:BTU_IT": ("btu",), "unit:KiloW-HR": ("kwh", "kilowatt"), "unit:FT2": ("square f", "sq ft", "sqft"),
              "unit:FT3": ("cubic f", "ccf"), "unit:GAL_US": ("gallon",), "iso4217:USD": ("dollar", "$")}


def profile_check(item: dict, prof: dict) -> list[str]:
    """Consistency rules a schema-aware validator can apply to an AI-built variable profile, using only the
    codebook entry (never the gold): the unit agrees with the unit word in the label, the multiplier agrees with
    a 'thousand'/'hundred' qualifier and is a power of ten, a missing code is a blank or a listed code with a
    non-substantive label, and a missing code of a continuous variable lies outside its valid range."""
    label = (item.get("label") or "").lower()
    out = []
    u = prof["unit"]
    named = [k for k, words in UNIT_WORDS.items() if any(w in label for w in words)]
    if named and u not in named:
        out.append("unit disagrees with label")
    if u != "none":
        m = float(prof["unit_multiplier"] or 1)
        want = 1000.0 if "thous" in label else 100.0 if "hundred" in label else 1.0
        if m != want:
            out.append("multiplier disagrees with label")
    codes = {str(c): str(lab).lower() for c, lab in (item.get("code_list") or [])}
    lo, hi = item.get("value_min"), item.get("value_max")
    for c in prof["missing_codes"]:
        if c == "":
            continue
        if codes:
            if c not in codes:
                out.append(f"missing code {c!r} not in code list")
            elif not any(w in codes[c] for w in ("withheld", "not applicable", "don't know", "refused", "missing",
                                                   "not ascertained", "skipped")):
                out.append(f"missing code {c!r} is a substantive category")
        else:
            try:
                x = float(c)
            except ValueError:
                out.append(f"missing code {c!r} is not a code")
                continue
            if lo is not None and hi is not None and lo <= x <= hi:
                out.append(f"missing code {c!r} inside the valid range")
    return out


def run() -> tuple[pd.DataFrame, pd.DataFrame]:
    data = {ds: pd.read_csv(DATA_RAW / f, low_memory=False) for ds, f in FILES.items()}
    gold = {k: gold_profile(it) for k, it in _items().items()}
    ref = {ds: quantities(ds, gold, data[ds]) for ds in PIPE}
    conds = [("codebook entry only", False, 0), ("with dataset card", True, 0),
             ("codebook entry only, T=0.7 run 1", False, 1), ("codebook entry only, T=0.7 run 2", False, 2)]
    items = _items()
    assert not any(profile_check(items[k], gold[k]) for k in gold), "gold profiles must pass the checks"
    rows, errs = [], []
    for model in MODELS:
        for lab, profile, rep in conds:
            prof = ai_profiles(model, profile, rep)
            for k in gold:
                g, a = gold[k], prof[k]
                bad = [f for f in ("is_weight", "unit") if g[f] != a[f]]
                if g["unit"] != "none" and float(g["unit_multiplier"] or 1) != float(a["unit_multiplier"] or 1):
                    bad.append("unit_multiplier")
                if sorted(c for c in g["missing_codes"] if c) != sorted(c for c in a["missing_codes"] if c):
                    bad.append("missing_codes")
                # consequence of this variable's AI profile alone: largest change of any quantity
                one = {**gold, k: a}
                q1 = quantities(k[0], one, data[k[0]])
                eff = max((abs(100 * (q1[n] - r) / r) if np.isfinite(q1[n]) else np.inf)
                          for n, r in ref[k[0]].items())
                errs.append({"model": model.split(":", 1)[1], "condition": lab, "dataset": k[0], "variable": k[1],
                             "fields_wrong": "; ".join(bad), "max_effect_pct": eff,
                             "consequential": eff > 0.5, "flags": "; ".join(profile_check(items[k], a)),
                             "ai_profile": str(a)})
            for ds in PIPE:
                q = quantities(ds, prof, data[ds])
                for name, r in ref[ds].items():
                    v = q[name]
                    rows.append({"model": model.split(":", 1)[1], "condition": lab, "dataset": ds, "quantity": name,
                                 "reference": r, "ai_pipeline": v,
                                 "rel_error_pct": np.nan if np.isnan(v) else 100 * (v - r) / r})
    return pd.DataFrame(rows), pd.DataFrame(errs)


def main() -> int:
    res, errs = run()
    out = PAPER / "tables"
    res.to_csv(out / "endtoend_quantities.csv", index=False)
    errs.to_csv(out / "endtoend_profile_errors.csv", index=False)
    pd.set_option("display.width", 220)
    piv = res.pivot_table(index=["dataset", "quantity"], columns=["model", "condition"], values="rel_error_pct", sort=False,
                          dropna=True)
    print(res.drop_duplicates(["dataset", "quantity"])[["dataset", "quantity", "reference"]].round(2).to_string())
    print(piv.round(1).to_string())
    errs["flagged"] = errs["flags"].fillna("") != ""
    errs["wrong"] = errs.fields_wrong.fillna("") != ""
    summ = errs.groupby(["model", "condition"]).agg(
        profiles=("variable", "size"), wrong=("wrong", "sum"), consequential=("consequential", "sum"),
        consequential_flagged=("consequential", lambda s: int((s & errs.loc[s.index, "flagged"]).sum())),
        correct_flagged=("wrong", lambda s: int((~s & errs.loc[s.index, "flagged"]).sum()))).reset_index()
    summ.to_csv(out / "endtoend_summary.csv", index=False)
    print(summ.to_string())
    print(errs[errs.wrong | errs.flagged].drop(columns="ai_profile").to_string())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
