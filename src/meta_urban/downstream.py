"""RQ4: do alignment and statistical-design errors change UBEM quantities?

Uses CBECS 2018 public-use microdata. Three analyses:

D1  Reference pipeline (what a correct alignment implies): weighted building count, floorspace and major-fuel
    consumption, checked against EIA published Tables B1 and C1.
D2  Ignoring the survey design (what the 2023 case study did): unweighted counts and record-mean EUI by
    principal building activity (PBA), compared with weighted aggregate EUI.
D3  Sensitivity of UBEM quantities to each code/unit normalization error type of task T3 (unit multiplier
    dropped, top-codes read as values, missing codes kept as values, imputation flag read as data).
    These are deterministic error injections; actual LLM error rates from T3 are combined with them in the paper.

    python -m meta_urban.downstream
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from . import DATA_RAW, PAPER
from .codebooks import load_cbecs2018

KBTU_TO_KWH = 1 / 3.412141633  # 1 kBtu = 0.29307 kWh
FT2_TO_M2 = 0.09290304


def load_cbecs() -> tuple[pd.DataFrame, dict]:
    df = pd.read_csv(DATA_RAW / "cbecs2018_final_public.csv", low_memory=False)
    cb = load_cbecs2018().set_index("name")
    pba = dict(cb.loc["PBA", "code_list"])
    return df, {int(k): v for k, v in pba.items()}


def published_totals() -> dict:
    b1 = pd.read_excel(DATA_RAW / "cbecs2018_table_b1.xlsx", header=None)
    c1 = pd.read_excel(DATA_RAW / "cbecs2018_table_c1.xlsx", header=None)
    rb = b1[b1[0].astype(str).str.strip() == "All buildings"].iloc[0]
    rc = c1[c1[0].astype(str).str.strip() == "All buildings"].iloc[0]
    return {"buildings_thousand": float(rb[1]), "floorspace_million_ft2": float(rb[2]),
            "major_fuels_trillion_btu": float(rc[3])}


def d1_reference(df: pd.DataFrame) -> pd.DataFrame:
    w = df["FINALWT"]
    est = {"buildings_thousand": w.sum() / 1e3,
           "floorspace_million_ft2": (w * df["SQFT"]).sum() / 1e6,
           "major_fuels_trillion_btu": (w * df["MFBTU"].fillna(0)).sum() / 1e9}  # MFBTU is thousand Btu
    pub = published_totals()
    rows = [{"quantity": k, "weighted_estimate": est[k], "eia_published": pub[k],
             "rel_diff_pct": 100 * (est[k] - pub[k]) / pub[k],
             "unweighted_naive": {"buildings_thousand": len(df) / 1e3,
                                  "floorspace_million_ft2": df["SQFT"].sum() / 1e6,
                                  "major_fuels_trillion_btu": df["MFBTU"].fillna(0).sum() / 1e9}[k]}
            for k in est]
    return pd.DataFrame(rows)


def d2_weights(df: pd.DataFrame, pba_names: dict) -> pd.DataFrame:
    d = df[df["MFBTU"].notna() & (df["SQFT"] > 0)].copy()
    d["eui_kwh_m2"] = d["MFBTU"] * KBTU_TO_KWH / (d["SQFT"] * FT2_TO_M2)
    w = d["FINALWT"]
    tot_w = df["FINALWT"].sum()
    rows = []
    for code, g in d.groupby("PBA"):
        gw = g["FINALWT"]
        agg_w = (gw * g["MFBTU"]).sum() * KBTU_TO_KWH / ((gw * g["SQFT"]).sum() * FT2_TO_M2)
        rows.append({
            "pba": pba_names.get(int(code), str(code)), "records": len(g),
            "share_of_records_pct": 100 * len(g) / len(d),
            "share_of_buildings_weighted_pct": 100 * df.loc[df.PBA == code, "FINALWT"].sum() / tot_w,
            "eui_weighted_aggregate": agg_w,
            "eui_unweighted_record_mean": g["eui_kwh_m2"].mean(),
            "eui_unweighted_aggregate": g["MFBTU"].sum() * KBTU_TO_KWH / (g["SQFT"].sum() * FT2_TO_M2),
        })
    out = pd.DataFrame(rows)
    out["err_record_mean_pct"] = 100 * (out.eui_unweighted_record_mean - out.eui_weighted_aggregate) / out.eui_weighted_aggregate
    out["err_unweighted_agg_pct"] = 100 * (out.eui_unweighted_aggregate - out.eui_weighted_aggregate) / out.eui_weighted_aggregate
    return out.sort_values("share_of_buildings_weighted_pct", ascending=False)


def d3_sensitivity(df: pd.DataFrame) -> pd.DataFrame:
    w = df["FINALWT"]
    rows = []

    def add(error, quantity, correct, wrong):
        rows.append({"t3_error_type": error, "quantity": quantity, "correct": correct, "with_error": wrong,
                     "rel_error_pct": 100 * (wrong - correct) / correct})

    # 1) unit multiplier dropped: MFBTU (thousand Btu) read as Btu -> national kWh/m2 off by 1000x
    eui = (w * df.MFBTU.fillna(0)).sum() * KBTU_TO_KWH / ((w * df.SQFT).sum() * FT2_TO_M2)
    add("unit multiplier dropped (thousand Btu read as Btu)", "national EUI [kWh/m2]", eui, eui / 1000)
    # 2) wrong unit: thousand Btu read as kWh
    add("wrong unit (thousand Btu read as kWh)", "national EUI [kWh/m2]", eui, eui * 3.412141633)
    # 3) floorspace read as m2 instead of ft2
    fs = (w * df.SQFT).sum() * FT2_TO_M2 / 1e6
    add("ft2 read as m2", "total floorspace [million m2]", fs, fs / FT2_TO_M2)
    # 4) top-codes read as values: NFLOOR 994 (10-14) and 995 (15+) used as numbers
    nf_ok = df.NFLOOR.replace({994: 12, 995: 15})  # midpoint / lower bound, documented assumption
    add("top-codes read as values (NFLOOR 994/995)", "weighted mean floors", (w * nf_ok).sum() / w.sum(),
        (w * df.NFLOOR).sum() / w.sum())
    # 5) missing/withheld code kept as a category value: PUBCLIM 7 = withheld
    pc_ok = df.PUBCLIM.where(df.PUBCLIM != 7)
    share_hot_ok = (w * (pc_ok == 5)).sum() / w[pc_ok.notna()].sum()
    share_hot_bad = (w * (df.PUBCLIM == 5)).sum() / w.sum()
    add("withheld code kept as data (PUBCLIM 7)", "share of buildings in hot/very hot zone", share_hot_ok, share_hot_bad)
    # 6) weights ignored entirely (the 2023 case study)
    add("survey weights ignored", "number of buildings [thousand]", w.sum() / 1e3, len(df) / 1e3)
    return pd.DataFrame(rows)


def main() -> None:
    df, pba = load_cbecs()
    out = PAPER / "tables"
    out.mkdir(parents=True, exist_ok=True)
    d1 = d1_reference(df)
    d2 = d2_weights(df, pba)
    d3 = d3_sensitivity(df)
    d1.to_csv(out / "downstream_d1_reference.csv", index=False)
    d2.to_csv(out / "downstream_d2_weights_by_pba.csv", index=False)
    d3.to_csv(out / "downstream_d3_sensitivity.csv", index=False)
    pd.set_option("display.width", 200)
    print(d1.round(2).to_string(index=False), "\n")
    print(d2.round(1).to_string(index=False), "\n")
    print(d3.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
