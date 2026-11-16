"""Profile checks, version 2: consistency rules for an AI-built variable profile (unit, multiplier, missing codes).

Version 1 (ubem_link.endtoend.profile_check) was written on the 11 variables of the national pipeline (E7).
Applied unchanged to all normalization outputs of the benchmark it over-fired (rules_heldout in
ubem_link.revision_stats): "Inapplicable" was not recognized as a non-substantive code label, categorical
variables whose label mentions a unit (a square-footage range) were flagged, and abbreviations such as ccf and
kBtu were not recognized as multipliers. Version 2 fixes these three causes. It was written after inspecting the
benchmark outputs, so its benchmark performance is in-sample; it was committed before any profile of the
New York City data (E8) was generated, so E8 is a held-out test of both versions.

What the rules need: the codebook entry (label, code list, valid range) and the schema's unit vocabulary.
They are implemented in Python, not generated from the LinkML source; the generated JSON Schema and SHACL check
structure (types, required fields, closed enumerations), which constrained decoding already guarantees.
"""

from __future__ import annotations

import re

UNIT_WORDS = {"unit:BTU_IT": ("btu",), "unit:KiloW-HR": ("kwh", "kilowatt"), "unit:FT2": ("square f", "sq ft", "sqft", "ft2", "ft²"),
              "unit:FT3": ("cubic f", "ccf", "mcf"), "unit:GAL_US": ("gallon",), "iso4217:USD": ("dollar", "$")}
NON_SUBSTANTIVE = ("withheld", "not applicable", "inapplicable", "don't know", "dont know", "refused", "missing",
                   "not ascertained", "skipped", "not available", "no answer", "suppressed")


def expected_multiplier(label: str, unit: str) -> float:
    """Multiplier implied by the label's qualifiers for the given base unit."""
    s = label.lower()
    if unit == "unit:BTU_IT":
        if re.search(r"\bmmbtu\b|million btu", s):
            return 1e6
        if re.search(r"\btherms?\b", s):
            return 1e5
        if re.search(r"\bkbtu\b|thous\w* btu|thousand british", s):
            return 1e3
    if unit == "unit:FT3":
        if re.search(r"\bccf\b|hundred cubic", s):
            return 100.0
        if re.search(r"\bmcf\b|thous\w* cubic", s):
            return 1e3
    if re.search(r"\bthous", s):
        return 1e3
    if re.search(r"\bhundred", s):
        return 100.0
    return 1.0


def check(item: dict, prof: dict) -> list[str]:
    label = item.get("label") or ""
    low = label.lower()
    codes = {str(c): str(lab).lower() for c, lab in (item.get("code_list") or [])}
    out = []
    u = prof.get("unit") or "none"
    if codes and len(codes) > 2 and u != "none":
        out.append("unit given for a categorical variable")
    if not codes or len(codes) <= 2:  # continuous (a 'Missing=...' line may appear as a one-entry code list)
        named = [k for k, words in UNIT_WORDS.items() if any(w in low for w in words)]
        if named and u not in named:
            out.append("unit disagrees with label")
        if u != "none" and float(prof.get("unit_multiplier") or 1) != expected_multiplier(label, u):
            out.append("multiplier disagrees with label")
    lo, hi = item.get("value_min"), item.get("value_max")
    for c in prof.get("missing_codes") or []:
        c = str(c)
        if c == "":
            continue
        if c in codes:
            if not any(w in codes[c] for w in NON_SUBSTANTIVE):
                out.append(f"missing code {c!r} is a substantive category")
            continue
        try:
            x = float(c)
        except ValueError:
            if not any(w in c.lower() for w in NON_SUBSTANTIVE):
                out.append(f"missing code {c!r} is neither a listed code nor a missing-value label")
            continue
        if lo is not None and hi is not None and lo <= x <= hi:
            out.append(f"missing code {c!r} inside the valid range")
    return out
