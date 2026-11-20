"""Read a dataset and its documentation into per-column descriptions that the profiler can use.

Data files: CSV, TSV, Excel, Parquet, JSON lines. Codebooks (documentation of the columns), detected
automatically:
    Socrata metadata JSON (NYC and many city portals: .../api/views/<id>.json)
    Frictionless Data Package or Table Schema JSON (datapackage.json, tableschema.json)
    CSV on the Web metadata JSON (*.csv-metadata.json)
    DDI-Codebook XML (survey archives)
    Markdown with a table whose header names the columns (for example city GIS metadata pages)
    Generic CSV or Excel codebooks, including EIA-style codebooks with a header row such as
        "Variable | Label | Values/Format codes" (the header row is searched for in the first 30 rows)
With no codebook, columns are described by their name and a summary of their values only.
"""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd


@dataclass
class Column:
    """What is known about one column before profiling."""

    name: str
    label: str = ""
    description: str = ""
    unit_text: str = ""            # unit as written in the documentation, if any
    codes_text: str = ""           # value codes as written in the documentation, verbatim
    code_list: list = field(default_factory=list)   # [[code, label], ...] when the documentation lists codes
    value_summary: str = ""        # summary of the values in the data
    value_min: float | None = None
    value_max: float | None = None
    n_values: int = 0
    n_missing: int = 0
    distinct_values: list = field(default_factory=list)  # up to 50 most frequent raw values

    def doc_text(self, max_words: int = 60) -> str:
        """Label and description, shortened, as shown to a model."""
        desc = " ".join(self.description.split()[:max_words])
        if self.label and desc and not desc.lower().startswith(self.label.lower()):
            return f"{self.label}. {desc}"
        return desc or self.label or self.name


# ------------------------------------------------------------------------------------------------ data
def read_table(path: str | Path, nrows: int | None = None) -> pd.DataFrame:
    """Read a data file with every value as text, so that codes like '007' or 'Not Available' are kept."""
    p = Path(path)
    suf = p.suffix.lower()
    if suf in (".xlsx", ".xls"):
        return pd.read_excel(p, dtype=str, nrows=nrows)
    if suf == ".parquet":
        df = pd.read_parquet(p)
        return (df.head(nrows) if nrows else df).astype(str).where(df.notna())
    if suf in (".jsonl", ".ndjson"):
        return pd.read_json(p, lines=True, dtype=str, nrows=nrows)
    sep = "\t" if suf in (".tsv", ".tab") else ","
    return pd.read_csv(p, dtype=str, nrows=nrows, sep=sep, low_memory=False, keep_default_na=False,
                       na_values=[""])


def summarize(s: pd.Series, k: int = 5) -> tuple[str, float | None, float | None, list]:
    """Short text summary of a column's values: numeric range and the most frequent non-numeric values."""
    num = pd.to_numeric(s, errors="coerce")
    text = s[num.isna() & s.notna()].value_counts().head(k)
    parts = [f'"{v}" ({n:,} records)' for v, n in text.items()]
    lo, hi = (float(num.min()), float(num.max())) if num.notna().any() else (None, None)
    if lo is not None:
        zeros = int((num == 0).sum())
        rng = f"numeric values from {lo:,.4g} to {hi:,.4g} (median {num.median():,.4g})"
        if zeros:
            rng += f", {zeros:,} zeros"
        parts.insert(0, rng)
    if s.isna().any():
        parts.append(f"{int(s.isna().sum()):,} empty")
    distinct = list(s.dropna().value_counts().head(50).index)
    return ("; ".join(parts) if parts else "(no values)"), lo, hi, distinct


# ------------------------------------------------------------------------------------------------ codebooks
def _from_socrata(js: dict) -> dict[str, Column]:
    out = {}
    for c in js.get("columns", []):
        if c.get("fieldName", "").startswith(":"):
            continue
        out[c["fieldName"]] = Column(c["fieldName"], label=c.get("name") or "", description=c.get("description") or "")
    return out


def _from_table_schema(fields: list[dict], missing: list | None = None) -> dict[str, Column]:
    out = {}
    for f in fields:
        col = Column(f["name"], label=f.get("title") or "", description=f.get("description") or "")
        enum = (f.get("constraints") or {}).get("enum")
        if enum:
            col.codes_text = "; ".join(map(str, enum))
        if f.get("unit"):
            col.unit_text = str(f["unit"])
        miss = f.get("missingValues") or missing
        if miss:
            col.codes_text = (col.codes_text + "; " if col.codes_text else "") + f"missing values: {miss}"
        out[f["name"]] = col
    return out


def _from_csvw(js: dict) -> dict[str, Column]:
    cols = (js.get("tableSchema") or (js.get("tables") or [{}])[0].get("tableSchema") or {}).get("columns", [])
    out = {}
    for c in cols:
        titles = c.get("titles")
        title = titles[0] if isinstance(titles, list) else (titles or "")
        out[c["name"]] = Column(c["name"], label=str(title), description=str(c.get("dc:description") or ""))
    return out


def _from_ddi(path: Path) -> dict[str, Column]:
    root = ET.parse(path).getroot()
    strip = lambda t: t.split("}")[-1]  # noqa: E731
    out = {}
    for var in root.iter():
        if strip(var.tag) != "var":
            continue
        name = var.get("name")
        col = Column(name)
        codes = []
        for ch in var:
            tag = strip(ch.tag)
            if tag == "labl":
                col.label = (ch.text or "").strip()
            elif tag in ("txt", "qstn"):
                col.description += " " + " ".join("".join(ch.itertext()).split())
            elif tag == "catgry":
                val = next((x.text for x in ch if strip(x.tag) == "catValu"), None)
                lab = next((x.text for x in ch if strip(x.tag) == "labl"), "")
                if val is not None:
                    codes.append([val.strip(), (lab or "").strip()])
        col.code_list = codes
        col.codes_text = "; ".join(f"{c}={lab}" for c, lab in codes)
        out[name] = col
    return out


def _from_markdown(text: str) -> dict[str, Column]:
    """Parse the first Markdown table whose header has a name-like column."""
    out = {}
    lines = [ln for ln in text.splitlines() if ln.strip().startswith("|")]
    i = 0
    while i < len(lines) - 1:
        head = [h.strip().lower() for h in lines[i].strip().strip("|").split("|")]
        if re.fullmatch(r"[\s|:-]+", lines[i + 1]) and any(re.search(r"name|field|column|variable|attribute", h) for h in head):
            ni = next(k for k, h in enumerate(head) if re.search(r"name|field|column|variable|attribute", h))
            di = next((k for k, h in enumerate(head) if re.search(r"descr|definition|meaning", h)), None)
            for row in lines[i + 2:]:
                cells = [c.strip() for c in row.strip().strip("|").split("|")]
                if len(cells) <= ni:
                    break
                desc = " ".join(cells[k] for k in range(len(cells)) if k != ni)
                if di is not None and di < len(cells):
                    desc = cells[di] + " " + " ".join(cells[k] for k in range(len(cells)) if k not in (ni, di))
                desc = re.sub(r"<br\s*/?>", " ", desc)
                for nm in re.split(r"\s*<br>\s*|\s+", cells[ni]):
                    if nm:
                        out[nm] = Column(nm, description=" ".join(desc.split()))
            break
        i += 1
    return out


HEADER_WORDS = {
    "name": r"^(variable|var|field|column|name|variable name|field name|column name|item|attribute)$",
    "label": r"^(label|title|variable label|display name|short description)$",
    "description": r"(description|definition|question|meaning|notes?)",
    "unit": r"^(units?|unit of measure|uom)$",
    "codes": r"(values|codes|format|categories|response|value labels|allowed)",
}


def _from_generic_table(df: pd.DataFrame) -> dict[str, Column]:
    """Find the header row (first 30 rows) whose cells name a column role, then read one Column per row."""
    rows = [df.columns.astype(str).tolist()] + df.head(30).astype(str).values.tolist()
    for k, row in enumerate(rows):
        roles = {}
        for j, cell in enumerate(row):
            c = " ".join(str(cell).lower().replace("\n", " ").split())
            for role, pat in HEADER_WORDS.items():
                if role not in roles and re.search(pat, c):
                    roles[role] = j
                    break
        if "name" in roles and len(roles) >= 2:
            body = df.iloc[k:] if k else df
            out = {}
            for vals in body.astype(str).values.tolist():
                get = lambda r: (vals[roles[r]] if r in roles and roles[r] < len(vals) else "")  # noqa: E731
                nm = get("name").strip()
                if not nm or nm.lower() in ("nan", "none") or re.search(HEADER_WORDS["name"], nm.lower()):
                    continue
                clean = lambda x: "" if x.strip().lower() == "nan" else x.strip()  # noqa: E731
                out[nm] = Column(nm, label=clean(get("label")), description=clean(get("description")),
                                 unit_text=clean(get("unit")), codes_text=clean(get("codes")))
            return out
    raise ValueError("no header row with a variable-name column found in the codebook")


def read_codebook(path: str | Path) -> dict[str, Column]:
    """Read a codebook in any supported format; returns column name -> Column."""
    p = Path(path)
    suf = p.suffix.lower()
    if suf == ".json":
        js = json.loads(p.read_text(encoding="utf-8"))
        if "columns" in js and any("fieldName" in c for c in js["columns"]):
            return _from_socrata(js)
        if "resources" in js:  # data package: first tabular resource
            res = js["resources"][0]
            sch = res.get("schema") or {}
            return _from_table_schema(sch.get("fields", []), sch.get("missingValues"))
        if "fields" in js:
            return _from_table_schema(js["fields"], js.get("missingValues"))
        if "tableSchema" in js or "tables" in js:
            return _from_csvw(js)
        raise ValueError(f"unrecognized JSON codebook: {p}")
    if suf == ".xml":
        return _from_ddi(p)
    if suf in (".md", ".markdown"):
        return _from_markdown(p.read_text(encoding="utf-8"))
    if suf in (".xlsx", ".xls"):
        sheets = pd.read_excel(p, sheet_name=None, dtype=str, header=None)
        best = {}
        for df in sheets.values():
            try:
                got = _from_generic_table(df)
            except ValueError:
                continue
            if len(got) > len(best):
                best = got
        if not best:
            raise ValueError(f"no codebook table found in {p}")
        return best
    return _from_generic_table(pd.read_csv(p, dtype=str, header=None, keep_default_na=False))


def merge_codebooks(*books: dict[str, Column]) -> dict[str, Column]:
    """Combine several documentation sources (for example a portal dictionary and a metadata page); fields of
    later sources fill what earlier ones leave empty, and descriptions are appended."""
    out: dict[str, Column] = {}
    for b in books:
        for k, c in b.items():
            key = next((o for o in out if o.lower() == k.lower()), k)
            if key not in out:
                out[key] = c
                continue
            o = out[key]
            o.label = o.label or c.label
            if c.description and c.description not in o.description:
                o.description = (o.description + " " + c.description).strip()
            o.unit_text = o.unit_text or c.unit_text
            o.codes_text = o.codes_text or c.codes_text
            o.code_list = o.code_list or c.code_list
    return out


def describe_columns(df: pd.DataFrame, codebook: dict[str, Column] | None = None) -> list[Column]:
    """One Column per data column: documentation from the codebook (matched case-insensitively) plus a value
    summary from the data."""
    book = {k.lower(): v for k, v in (codebook or {}).items()}
    out = []
    for name in df.columns:
        doc = book.get(str(name).lower())
        col = Column(str(name)) if doc is None else Column(**{**doc.__dict__, "name": str(name)})
        s = df[name]
        col.value_summary, col.value_min, col.value_max, col.distinct_values = summarize(s)
        col.n_values, col.n_missing = int(s.notna().sum()), int(s.isna().sum())
        out.append(col)
    return out
