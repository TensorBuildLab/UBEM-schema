"""Turn a dataset and its codebook into an AI-ready UBEM-Link profile, with a local or hosted language model.

For each column the profiler
  1. maps it to a UBEM-Link concept or join-key type. A retriever ranks the concept cards (dense embeddings
     through Ollama, falling back to TF-IDF), and the model chooses among the ten best under constrained output.
     This is the setting that kept accuracy at a fifth of the tokens in the paper (E5);
  2. builds its normalization profile (datatype, unit, multiplier, missing codes, code list, weight and flag
     roles) under constrained output, from the column's documentation, a summary of its values, and only those
     dataset conventions whose machine-readable scope covers the column;
  3. applies those conventions deterministically: a convention's unit, multiplier and missing codes overwrite
     the model's answer, and every disagreement is recorded for review. The paper found that conventions given
     to a model as prose were applied beyond their scope;
  4. runs the profile checks and the concept checks, and ranks columns for human review.

The unit list offered to the model is the full UBEM-Link unit vocabulary, including units in which sources
publish (kBtu, therm, ft), because in the paper a closed list without them made both models write kBtu as kWh.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from .checks import NON_SUBSTANTIVE
from .io import concept_index, leaf_concepts, schema_enums
from .llm import ROLE, complete, parse_json
from .readers import Column
from .units import CONCEPT_KINDS, kind, to_canonical, unit_choices, unit_menu, unit_words

DATATYPES = ["integer", "float", "string", "categorical", "boolean", "datetime", "geometry", "identifier"]
AGGREGATIONS = ["static", "instantaneous", "total_over_period", "average_over_period", "count", "share", "none"]
# Plausible ranges of values in canonical units, used to catch unit errors that survive the other checks
PLAUSIBLE = {"building_height": (0, 650), "floors_above_ground": (0, 200), "floors_below_ground": (0, 20),
             "year_of_construction": (1500, 2035), "gross_floor_area": (1, 2.0e7),
             "energy_use_intensity": (0, 5000), "dry_bulb_temperature": (-70, 60),
             "relative_humidity": (0, 100), "window_to_wall_ratio": (0, 100)}


@dataclass
class Settings:
    model: str = "ollama:qwen3:8b"
    retrieval: str = "dense"          # dense | lexical | all
    k: int = 10
    conventions: str = "scoped"       # scoped (tool default) | card (all conventions as prose) | none
    apply_conventions: bool = True    # overwrite the model's answer with a matching convention's values
    cache_dir: str | Path | None = None


# ------------------------------------------------------------------------------------------------ conventions
def convention_matches(conv: dict, name: str, label: str = "") -> bool:
    """True if the convention's machine-readable scope covers the column."""
    names = conv.get("applies_to_variables") or []
    if name in names or name.lower() in {n.lower() for n in names}:
        return True
    pat = conv.get("applies_to_pattern")
    if pat:
        return bool(re.search(pat, name, re.I) or (label and re.search(pat, label, re.I)))
    return False


def scoped_conventions(entry: dict | None, col: Column) -> list[dict]:
    return [c for c in (entry or {}).get("conventions") or [] if convention_matches(c, col.name, col.label)]


def _convention_text(convs: list[dict]) -> str:
    out = []
    for c in convs:
        ex = f" Example: {c['example']}" if c.get("example") else ""
        out.append(f"- {c.get('applies_to', 'all variables')}: {c['rule']}{ex}")
    return "\n".join(out)


# ------------------------------------------------------------------------------------------------ prompts
def _join_key_cards() -> list[tuple[str, str]]:
    from .io import SCHEMA_YAML
    import yaml

    pv = yaml.safe_load(open(SCHEMA_YAML, encoding="utf-8"))["enums"]["JoinKey"]["permissible_values"]
    return [(f"join:{k}", f"join:{k}: {k.replace('_', ' ')}. {(v or {}).get('description', '')}") for k, v in pv.items()]


def _concept_card(c: dict) -> str:
    extra = [f"broader={c['broader']}" if c.get("broader") else "", f"describes={c['entity']}" if c.get("entity") else "",
             f"unit={c['canonical_unit']}" if c.get("canonical_unit") else "",
             ("also called: " + ", ".join(c["alt_labels"][:6])) if c.get("alt_labels") else ""]
    return f"{c['id']}: {c['pref_label']}. {c['definition']} [{'; '.join(e for e in extra if e)}]"


def column_item(col: Column, dataset: str) -> dict:
    """The column as a benchmark-style item (used by the retrievers)."""
    return {"dataset": dataset, "name": col.name, "label": col.doc_text(40), "code_list": col.code_list}


def column_block(col: Column, dataset: str, max_codes: int = 12) -> str:
    parts = [f"dataset: {dataset}", f"column name: {col.name}"]
    if col.label:
        parts.append(f"label: {col.label}")
    if col.description:
        parts.append(f"description: {' '.join(col.description.split()[:80])}")
    if col.unit_text:
        parts.append(f"unit (documented): {col.unit_text}")
    if col.code_list:
        shown = "; ".join(f"{c}={lab}" for c, lab in col.code_list[:max_codes])
        parts.append(f"codes (documented): {shown}{' ...' if len(col.code_list) > max_codes else ''}")
    elif col.codes_text:
        parts.append(f"values/codes (documented, verbatim): {col.codes_text[:600]}")
    parts.append(f"values in the data: {col.value_summary}")
    return "\n".join(parts)


def map_request(col: Column, dataset: str, candidates: list[str]) -> dict:
    idx = {c["id"]: c for c in leaf_concepts()}
    cards = "\n".join(_concept_card(idx[c]) for c in candidates if c in idx)
    keys = _join_key_cards()
    ids = [c for c in candidates if c in idx] + [k for k, _ in keys] + ["none"]
    system = (f"{ROLE}\n\nTask: map one column of a dataset to the single most specific concept of the target "
              "vocabulary that the column measures or records. If the column is an identifier or code through "
              "which records can be linked to other datasets, answer the matching join key type instead. Answer "
              "\"none\" if nothing applies.\n\n"
              f"TARGET VOCABULARY\n{cards}\n\nJOIN KEY TYPES\n" + "\n".join(t for _, t in keys) +
              '\n\nOutput: {"concept": <id or "none">, "alternatives": [<up to two other ids>], "confidence": <0 to 1>}')
    ctype = {"type": "string", "enum": ids}
    schema = {"type": "object", "properties": {"concept": ctype, "alternatives": {"type": "array", "items": ctype},
                                               "confidence": {"type": "number"}},
              "required": ["concept", "alternatives", "confidence"], "additionalProperties": False}
    return {"system": system, "user": f"COLUMN\n{column_block(col, dataset)}", "schema": schema}


NORM_SYSTEM = (
    f"{ROLE}\n\nTask: read the documentation of one column of a dataset and a summary of its values, and state "
    "how its values must be read. Fields:\n"
    f"datatype: one of {DATATYPES}.\n"
    "unit: the unit of numeric quantities, chosen from the UNIT LIST exactly as the source publishes it (kBtu is "
    "unit:KiloBTU_IT, therms are unit:THM_US, feet are unit:FT); \"none\" for categorical, identifier, text or "
    "unitless columns and for counts and calendar years.\n"
    "unit_multiplier: 1 unless the documentation says values are in thousands, hundreds or millions of the unit "
    "(for example \"in thousands of dollars\": unit:CCY_USD with multiplier 1000).\n"
    "missing_codes: values that mean missing, unknown, not applicable or withheld (use \"\" for an empty value). "
    "Do not list a value that is a valid observation.\n"
    "codes: every categorical code as [code, label]; [] if the column is not categorical.\n"
    "is_weight, is_replicate_weight: true for sampling or analysis weights.\n"
    "is_imputation_flag and flags_variable: true and the column it flags, if it records whether another column "
    "was imputed; otherwise false and \"none\".\n"
    f"aggregation: one of {AGGREGATIONS}.\n\nUNIT LIST\n"
)


def normalize_request(col: Column, dataset: str, conventions: list[dict], mode: str) -> dict:
    system = NORM_SYSTEM + unit_menu()
    if conventions and mode != "none":
        head = ("CONVENTIONS OF THIS DATASET THAT APPLY TO THIS COLUMN" if mode == "scoped" else
                "DATASET CONVENTIONS (apply to many columns; individual entries do not repeat them)")
        system += f"\n\n{head}\n{_convention_text(conventions)}"
    schema = {"type": "object", "properties": {
        "datatype": {"type": "string", "enum": DATATYPES},
        "unit": {"type": "string", "enum": unit_choices()},
        "unit_multiplier": {"type": "number"},
        "missing_codes": {"type": "array", "items": {"type": "string"}},
        "codes": {"type": "array", "items": {"type": "array", "items": {"type": "string"}}},
        "is_weight": {"type": "boolean"}, "is_replicate_weight": {"type": "boolean"},
        "is_imputation_flag": {"type": "boolean"}, "flags_variable": {"type": "string"},
        "aggregation": {"type": "string", "enum": AGGREGATIONS}},
        "required": ["datatype", "unit", "unit_multiplier", "missing_codes", "codes", "is_weight",
                     "is_replicate_weight", "is_imputation_flag", "flags_variable", "aggregation"],
        "additionalProperties": False}
    return {"system": system, "user": f"COLUMN\n{column_block(col, dataset)}", "schema": schema}


def select_request(columns: list[Column], target: str, purpose: str) -> dict:
    """Choose the column that holds a concept or join key (the step a pipeline needs)."""
    if target.startswith("join:"):
        text = dict(_join_key_cards())[target]
    else:
        text = _concept_card(concept_index()[target])
    block = "\n".join(f"{c.name}: {c.label or c.doc_text(12)}" for c in columns)
    system = (f"{ROLE}\n\nTask: a data pipeline needs the column of a dataset that holds a given concept. Choose the "
              "single best column, or \"none\" if no column holds it.\n\n"
              f"DATASET COLUMNS (name: label)\n{block}\n\n"
              'Output: {"column": <name or "none">, "confidence": <0 to 1>}')
    schema = {"type": "object", "properties": {"column": {"type": "string", "enum": [c.name for c in columns] + ["none"]},
                                               "confidence": {"type": "number"}},
              "required": ["column", "confidence"], "additionalProperties": False}
    return {"system": system, "user": f"CONCEPT\n{text}\n\nPURPOSE\n{purpose}", "schema": schema}


# ------------------------------------------------------------------------------------------------ checks
def _missing_like(text: str) -> bool:
    t = text.lower()
    return any(w in t for w in NON_SUBSTANTIVE) or bool(re.search(r"\bunknown\b|\bn/?a\b|\bnull\b", t))


def profile_checks(col: Column, prof: dict, concept: str | None, convs: list[dict]) -> list[str]:
    """Checks of a variable profile that need no gold: documentation, data, concept and conventions."""
    out = []
    doc = f"{col.name} {col.label} {col.description} {col.unit_text}".lower()
    u, m = prof.get("unit") or "none", float(prof.get("unit_multiplier") or 1)
    named = [k for k, words in unit_words().items() if any(w.strip() and w in doc for w in words)]
    stated = [c for c in convs if c.get("unit")]
    if u != "none" and named and u not in named and not stated:
        out.append(f"unit {u} is not named in the documentation (named: {', '.join(named[:3])})")
    if u == "none" and named and col.value_min is not None and not stated and len(col.code_list) <= 2:
        out.append(f"no unit, but the documentation names {named[0]}")
    if re.search(r"\bthousands?\b|\bhundreds?\b|\bmillions?\b", doc) and m == 1 and u != "none" and \
            not re.search(r"kbtu|mmbtu|ccf|mcf|thousand btu|million btu", doc):
        out.append("documentation mentions a scale word but the multiplier is 1")
    vals = {str(v) for v in col.distinct_values}
    codes = {str(c): str(lab) for c, lab in col.code_list}
    for c in prof.get("missing_codes") or []:
        c = str(c)
        if c == "":
            continue
        if c in codes and not _missing_like(codes[c]):
            out.append(f"missing code {c!r} is a documented category ({codes[c]})")
        elif c not in codes and not _missing_like(c):
            try:
                float(c)
            except ValueError:
                out.append(f"missing code {c!r} is not a missing-value label")
                continue
            if not any(c in x.get("missing_codes", []) for x in convs) and not _missing_like(doc):
                out.append(f"numeric missing code {c!r} is not documented as missing")
    for v in col.distinct_values[:20]:
        if isinstance(v, str) and _missing_like(v) and v not in (prof.get("missing_codes") or []):
            out.append(f"value {v!r} looks like a missing code but is not listed")
            break
    if concept and not concept.startswith("join:") and concept != "none":
        c = concept_index().get(concept, {})
        qk = c.get("quantity_kind")
        allowed = CONCEPT_KINDS.get(qk)
        if allowed and u != "none" and kind(u) not in allowed:
            out.append(f"unit {u} ({kind(u)}) does not fit the concept's quantity kind {qk}")
        if c.get("canonical_unit") and u == "none" and col.value_min is not None and concept in PLAUSIBLE \
                and concept not in ("floors_above_ground", "floors_below_ground", "year_of_construction"):
            out.append(f"no unit for a concept measured in {c['canonical_unit']}")
        if concept in PLAUSIBLE and col.value_min is not None:
            lo, hi = PLAUSIBLE[concept]
            q = np.array([col.value_min, col.value_max], dtype=float)
            if u != "none":
                q, _ = to_canonical(q, u, m)
            if q is not None and (q[1] > hi * 10 or q[0] < lo - abs(hi)):
                out.append(f"values outside the plausible range for {concept} after conversion")
    for c in convs:
        if c.get("convention_type") == "do_not_use":
            out.append(f"publisher says do not use: {c['rule'][:80]}")
    return out


# ------------------------------------------------------------------------------------------------ profiler
class Profiler:
    def __init__(self, settings: Settings | None = None, entry: dict | None = None, dataset: str | None = None):
        self.s = settings or Settings()
        self.entry = entry or {}
        self.dataset = dataset or self.entry.get("id") or "dataset"
        self._retriever = None
        self.log: list[dict] = []
        self.pending = 0

    # retrieval -------------------------------------------------------------------------------------
    def _rank(self, cols: list[Column]) -> list[list[str]]:
        ids = [c["id"] for c in leaf_concepts()]
        if self.s.retrieval == "all":
            return [ids for _ in cols]
        items = [column_item(c, self.dataset) for c in cols]
        if self._retriever is None:
            from .baselines import LexicalRetriever, OllamaEmbeddingRetriever

            try:
                self._retriever = OllamaEmbeddingRetriever() if self.s.retrieval == "dense" else LexicalRetriever()
            except Exception:  # noqa: BLE001  no Ollama server or no embedding model: lexical fallback
                self._retriever = LexicalRetriever()
        try:
            return self._retriever.rank(items, k=self.s.k)
        except Exception:  # noqa: BLE001
            from .baselines import LexicalRetriever

            self._retriever = LexicalRetriever()
            return self._retriever.rank(items, k=self.s.k)

    def _call(self, req: dict, meta: dict) -> dict:
        r = complete(self.s.model, req, {"dataset": self.dataset, **meta}, 0, cache_dir=self.s.cache_dir)
        return parse_json(r.get("response", "")) or {}

    # steps -----------------------------------------------------------------------------------------
    def map_concept(self, col: Column, candidates: list[str]) -> dict:
        js = self._call(map_request(col, self.dataset, candidates), {"task": "tool-map", "name": col.name})
        return {"concept": js.get("concept", "none"), "alternatives": js.get("alternatives") or [],
                "confidence": js.get("confidence")}

    def normalize(self, col: Column) -> tuple[dict, dict, list[dict]]:
        """Returns (model answer, final profile after conventions, conventions applied)."""
        convs = scoped_conventions(self.entry, col)
        shown = convs if self.s.conventions == "scoped" else (self.entry.get("conventions") or [])
        req = normalize_request(col, self.dataset, shown, self.s.conventions)
        task = {"scoped": "tool-norm", "card": "tool-norm-card", "none": "tool-norm-none"}[self.s.conventions]
        raw = self._call(req, {"task": task, "name": col.name})
        prof = {k: raw.get(k) for k in ("datatype", "unit", "unit_multiplier", "missing_codes", "codes", "is_weight",
                                         "is_replicate_weight", "is_imputation_flag", "flags_variable", "aggregation")}
        prof["unit"] = prof.get("unit") or "none"
        prof["unit_multiplier"] = prof.get("unit_multiplier") or (1 if prof["unit"] != "none" else 0)
        prof["missing_codes"] = [str(x) for x in prof.get("missing_codes") or []]
        final = json.loads(json.dumps(prof))
        notes = []
        if self.s.apply_conventions:
            for c in convs:
                for code in c.get("missing_codes") or []:
                    if str(code) not in final["missing_codes"]:
                        final["missing_codes"].append(str(code))
                if c.get("unit"):
                    if (final["unit"], float(final["unit_multiplier"] or 1)) != (c["unit"], float(c.get("unit_multiplier") or 1)):
                        notes.append(f"convention set unit {c['unit']} x{c.get('unit_multiplier') or 1} "
                                     f"(model: {final['unit']} x{final['unit_multiplier']})")
                    final["unit"], final["unit_multiplier"] = c["unit"], c.get("unit_multiplier") or 1
                if c.get("convention_type") == "do_not_use":
                    final["do_not_use"] = True
        final["convention_notes"] = notes
        return prof, final, convs

    def profile(self, cols: list[Column], only: list[str] | None = None) -> list[dict]:
        cols = [c for c in cols if not only or c.name in only]
        ranked = self._rank(cols)
        out = []
        from .llm import PendingResponses

        self.pending = 0
        for col, cands in zip(cols, ranked):
            try:
                mp = self.map_concept(col, cands)
            except PendingResponses:
                mp = None
                self.pending += 1
            try:
                raw, final, convs = self.normalize(col)
            except PendingResponses:
                self.pending += 1
                continue
            if mp is None:
                continue
            flags = profile_checks(col, final, mp["concept"], convs) + final.pop("convention_notes")
            conf = mp["confidence"]
            if conf is not None and conf < 0.6:
                flags.append(f"low mapping confidence ({conf:.2f})")
            var = {"name": col.name, "label": col.label or None, "description": col.description or None,
                   "datatype": final.get("datatype"), "concept": None, "join_key": None,
                   "unit": None if final["unit"] == "none" else final["unit"],
                   "unit_multiplier": None if final["unit"] == "none" else float(final["unit_multiplier"] or 1),
                   "aggregation": None if final.get("aggregation") in (None, "none") else final["aggregation"],
                   "missing_codes": final["missing_codes"] or None,
                   "code_list": [{"code": str(c[0]), "label": str(c[1])} for c in (final.get("codes") or []) if len(c) >= 2] or None,
                   "is_weight": bool(final.get("is_weight")) or None,
                   "is_replicate_weight": bool(final.get("is_replicate_weight")) or None,
                   "is_imputation_flag": bool(final.get("is_imputation_flag")) or None,
                   "flags_variable": None if final.get("flags_variable") in (None, "", "none") else final["flags_variable"],
                   "do_not_use": final.get("do_not_use") or None,
                   "profiled_by": f"{self.s.model} (unreviewed)", "confidence": conf,
                   "review_flags": flags or None}
            if mp["concept"].startswith("join:"):
                var["join_key"] = mp["concept"].split(":", 1)[1]
            elif mp["concept"] != "none":
                var["concept"] = mp["concept"]
            self.log.append({"name": col.name, "candidates": cands, "mapping": mp, "model_profile": raw,
                             "conventions": [c.get("applies_to") for c in convs]})
            out.append({k: v for k, v in var.items() if v is not None})
        return out


def review_table(variables: list[dict]):
    """Columns ordered for human review: most flags and lowest confidence first."""
    import pandas as pd

    rows = [{"name": v["name"], "concept": v.get("concept") or (f"join:{v['join_key']}" if v.get("join_key") else "none"),
             "unit": v.get("unit", "none"), "multiplier": v.get("unit_multiplier"),
             "missing_codes": "; ".join(v.get("missing_codes") or []), "confidence": v.get("confidence"),
             "n_flags": len(v.get("review_flags") or []), "flags": " | ".join(v.get("review_flags") or []),
             "accept": "", "correction": ""} for v in variables]
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    df["_c"] = df.confidence.fillna(0.5)
    return df.sort_values(["n_flags", "_c"], ascending=[False, True]).drop(columns="_c")


def known_enums() -> dict[str, list[str]]:
    return schema_enums()
