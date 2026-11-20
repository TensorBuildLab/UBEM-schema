"""Apply a UBEM-Link profile to its data: a deterministic normalization, with no model involved.

For every profiled column: missing codes become empty values, numeric values are converted to the canonical
unit of their quantity kind (QUDT factors from schema/vocab/units.yaml), and coded values can be replaced by
their labels. Columns marked do_not_use are dropped. The output keeps the original column names and adds a
second header row-free mapping file (column -> concept, unit) so that the result is self-describing.
"""

from __future__ import annotations

import pandas as pd

from .units import to_canonical

TEMP_DIFF = {"degree_days"}


def apply_profile(df: pd.DataFrame, variables: list[dict], decode: bool = False,
                  keep_unprofiled: bool = True) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Returns (normalized table, column dictionary with concept, canonical unit and conversion applied)."""
    out, rows = {}, []
    prof = {v["name"]: v for v in variables}
    for name in df.columns:
        v = prof.get(name)
        if v is None:
            if keep_unprofiled:
                out[name] = df[name]
            continue
        if v.get("do_not_use"):
            rows.append({"column": name, "status": "dropped (publisher says do not use)"})
            continue
        s = df[name]
        miss = [str(c) for c in v.get("missing_codes") or []]
        if miss:
            s = s.where(~s.astype(str).isin([m for m in miss if m != ""]))
        unit, mult = v.get("unit"), v.get("unit_multiplier") or 1
        status, cu = "kept", None
        if unit:
            x = pd.to_numeric(s, errors="coerce")
            conv, cu = to_canonical(x, unit, mult, difference=v.get("concept") in TEMP_DIFF)
            if conv is not None:
                s, status = conv, f"converted {unit} x{mult:g} to {cu}"
        elif decode and v.get("code_list"):
            lab = {str(c["code"]): c.get("label") for c in v["code_list"]}
            s = s.astype(str).map(lambda x: lab.get(x, x)).where(s.notna())
            status = "codes replaced by labels"
        out[name] = s
        rows.append({"column": name, "concept": v.get("concept") or (f"join:{v['join_key']}" if v.get("join_key") else None),
                     "unit": cu or unit, "status": status,
                     "missing_codes_removed": "; ".join(m if m else '""' for m in miss)})
    return pd.DataFrame(out, index=df.index), pd.DataFrame(rows)
