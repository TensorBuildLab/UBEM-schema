"""Parse EIA survey codebooks (CBECS 2018, RECS 2020) into a common variable table.

Output columns:
    dataset, name, label, section, vtype, codes_raw,
    code_list (list of [code, label]), value_min, value_max, missing_codes (list),
    unit, unit_multiplier, is_weight, is_replicate_weight, is_imputation_flag, flags_variable

The derived columns are the gold labels for benchmark task T3 (code and unit normalization). They are derived
deterministically from the publisher's codebook text with the documented rules below, so they are exact with
respect to the codebook, not to the world: if the codebook text is wrong, the gold is wrong in the same way.
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from . import DATA_RAW

DASH = "[–—�-]"          # en dash, em dash, replacement char, hyphen
NUM = r"-?[\d,]+(?:\.\d+)?"
MISSING_PAT = re.compile(r"not applicable|inapplicable|withheld|don.?t know|refused|missing|suppressed", re.I)

# unit phrases found in codebook labels -> (QUDT/ISO unit, multiplier)
UNIT_RULES: list[tuple[re.Pattern, str, float]] = [
    (re.compile(r"\(thous(?:and)? Btu\)|in thousand Btu", re.I), "unit:BTU_IT", 1000.0),
    (re.compile(r"\(kWh\)|in kilowatt-?hours", re.I), "unit:KiloW-HR", 1.0),
    (re.compile(r"\(ccf\)|in hundred cubic feet", re.I), "unit:FT3", 100.0),
    (re.compile(r"\(gallons\)|in gallons", re.I), "unit:GAL_US", 1.0),
    (re.compile(r"\(\$\)|in dollars", re.I), "iso4217:USD", 1.0),
    (re.compile(r"square f(?:ee|oo)t(?:age)?(?! category)(?! range)", re.I), "unit:FT2", 1.0),
    (re.compile(r"base 65", re.I), "unit:DEG_F", 1.0),
    (re.compile(r"hours (?:open )?per week|hours per week", re.I), "unit:HR", 1.0),
]
TEMP_PAT = re.compile(r"thermostat setting|temperature (?:in|setting)|temperature when", re.I)


def _to_num(s: str) -> float | None:
    try:
        return float(s.replace(",", ""))
    except ValueError:
        return None


def parse_codes(text: str, style: str) -> tuple[list[list[str]], float | None, float | None, list[str]]:
    """Return (code_list, min, max, missing_codes) from a codebook 'values' cell.

    style 'eq'    : CBECS lines like '1=Northeast', '1,001 - 2,100,000', 'Missing=Not applicable'
    style 'space' : RECS lines like '1 Mobile home', '50 - 90', '-2 Not applicable'
    """
    codes: list[list[str]] = []
    missing: list[str] = []
    vmin = vmax = None
    if not isinstance(text, str):
        return codes, vmin, vmax, missing
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        rng = re.fullmatch(rf"({NUM})\s*{DASH}\s*({NUM})", line)
        if rng:
            a, b = _to_num(rng.group(1)), _to_num(rng.group(2))
            vmin = a if vmin is None else min(vmin, a)
            vmax = b if vmax is None else max(vmax, b)
            continue
        if style == "eq":
            m = re.fullmatch(r"([^=]+?)\s*=\s*(.+)", line)
        else:
            m = re.fullmatch(rf"({NUM})\s+(.+)", line)
        if m:
            code, label = m.group(1).strip(), m.group(2).strip()
            codes.append([code, label])
            if MISSING_PAT.search(label):
                missing.append("" if code.lower() == "missing" else code)
        elif style == "space" and not re.search(r"!A\d", line):
            codes.append([line, line])        # RECS character codes such as 'Midwest'
    return codes, vmin, vmax, missing


def unit_of(label: str, codes: list, vmin, vmax) -> tuple[str | None, float | None]:
    if codes and not (vmin is not None or vmax is not None):
        return None, None                      # purely categorical
    if re.search(r"category|range", label, re.I):
        return None, None
    for pat, unit, mult in UNIT_RULES:
        if pat.search(label):
            return unit, mult
    if TEMP_PAT.search(label) and vmin is not None and 40 <= vmin and (vmax or 0) <= 100:
        return "unit:DEG_F", 1.0
    return None, None


def load_cbecs2018(path: Path | str = DATA_RAW / "cbecs2018_codebook.xlsx") -> pd.DataFrame:
    cb = pd.read_excel(path, header=1)
    cb.columns = ["order", "name", "vtype", "label", "codes_raw", "question"]
    cb = cb.dropna(subset=["name"])
    names = set(cb["name"])
    rows = []
    for r in cb.itertuples():
        label = str(r.label).strip()
        codes, vmin, vmax, missing = parse_codes(r.codes_raw, "eq")
        is_flag = label.lower().startswith("imputation flag")
        flags_var = None
        if is_flag:
            cand = r.name[1:] if r.name.startswith("Z") else None
            flags_var = cand if cand in names else None
        unit, mult = (None, None) if is_flag else unit_of(label, codes, vmin, vmax)
        rows.append(dict(
            dataset="cbecs2018", name=r.name, label=label, section=None, question=_s(r.question),
            vtype=str(r.vtype).strip().lower(), codes_raw=_s(r.codes_raw), code_list=codes,
            value_min=vmin, value_max=vmax, missing_codes=missing, unit=unit, unit_multiplier=mult,
            is_weight=bool(re.fullmatch(r"FINALWT\d*", r.name)),
            is_replicate_weight=bool(re.fullmatch(r"FINALWT\d+", r.name)),
            is_imputation_flag=is_flag, flags_variable=flags_var,
        ))
    return pd.DataFrame(rows)


def load_recs2020(path: Path | str = DATA_RAW / "recs2020_codebook_v7.xlsx") -> pd.DataFrame:
    cb = pd.read_excel(path, header=1)
    cb.columns = ["name", "vtype", "label", "codes_raw", "section"]
    cb = cb.dropna(subset=["name"])
    names = set(cb["name"])
    rows = []
    for r in cb.itertuples():
        label = str(r.label).strip()
        codes, vmin, vmax, missing = parse_codes(r.codes_raw, "space")
        m = re.match(r"imputation (?:indicator|flag) for (\w+)?", label, re.I)
        is_flag = bool(m)
        flags_var = (m.group(1) if m and m.group(1) in names else
                     (r.name[1:] if m and r.name.startswith("Z") and r.name[1:] in names else None))
        unit, mult = (None, None) if is_flag else unit_of(label, codes, vmin, vmax)
        rows.append(dict(
            dataset="recs2020", name=r.name, label=label, section=_s(r.section), question=None,
            vtype=str(r.vtype).strip().lower(), codes_raw=_s(r.codes_raw), code_list=codes,
            value_min=vmin, value_max=vmax, missing_codes=missing, unit=unit, unit_multiplier=mult,
            is_weight=bool(re.fullmatch(r"NWEIGHT\d*", r.name)),
            is_replicate_weight=bool(re.fullmatch(r"NWEIGHT\d+", r.name)),
            is_imputation_flag=is_flag, flags_variable=flags_var,
        ))
    return pd.DataFrame(rows)


def _s(x):
    return None if (x is None or (isinstance(x, float) and pd.isna(x))) else str(x)


def load_all() -> pd.DataFrame:
    return pd.concat([load_cbecs2018(), load_recs2020()], ignore_index=True)


if __name__ == "__main__":
    df = load_all()
    print(df.groupby("dataset").agg(
        n=("name", "size"), coded=("code_list", lambda s: sum(bool(x) for x in s)),
        with_unit=("unit", lambda s: s.notna().sum()), weights=("is_weight", "sum"),
        flags=("is_imputation_flag", "sum"), flag_linked=("flags_variable", lambda s: s.notna().sum()),
    ))
