"""Unit vocabulary of UBEM-Link (schema/vocab/units.yaml): the closed list offered to models, and conversion of
values to the canonical unit of each quantity kind."""

from __future__ import annotations

from functools import lru_cache

import yaml

from . import ROOT

UNITS_YAML = ROOT / "schema" / "vocab" / "units.yaml"
ALIASES = {"iso4217:USD": "unit:CCY_USD"}  # unit spelling used in the benchmark prompts


@lru_cache
def vocabulary() -> dict:
    return yaml.safe_load(UNITS_YAML.read_text(encoding="utf-8"))


def units() -> dict[str, dict]:
    return vocabulary()["units"]


def unit_choices() -> list[str]:
    """Closed unit list for constrained output (every unit of the vocabulary, plus 'none')."""
    return list(units()) + ["none"]


def unit_menu() -> str:
    """One line per unit for a prompt: id, label and quantity kind."""
    return "\n".join(f"{u}: {d['label']} [{d['kind']}]" for u, d in units().items())


def kind(unit: str | None) -> str | None:
    u = units().get(ALIASES.get(unit, unit) if unit else unit)
    return u["kind"] if u else None


def canonical(kind_name: str) -> str | None:
    return vocabulary()["canonical"].get(kind_name)


def to_canonical(values, unit: str | None, multiplier: float | None = 1.0, difference: bool = False):
    """Convert raw values (scalar, numpy array or pandas Series) to the canonical unit of the unit's kind.
    Returns (converted values, canonical unit); (None, None) when the unit is unknown or 'none'."""
    if not unit or unit == "none":
        return None, None
    d = units().get(ALIASES.get(unit, unit))
    if d is None:
        return None, None
    m = float(multiplier or 1.0)
    if difference and "difference_factor" in d:
        return values * m * d["difference_factor"], canonical(d["kind"])
    return values * m * d["factor"] + d.get("offset", 0.0), canonical(d["kind"])


def unit_words() -> dict[str, tuple[str, ...]]:
    return {u: tuple(d.get("words") or ()) for u, d in units().items()}


CONCEPT_KINDS = {
    # quantity kinds of the concept vocabulary (QUDT) -> unit kinds of this vocabulary
    "quantitykind:Energy": {"energy"}, "quantitykind:Area": {"area"}, "quantitykind:Length": {"length"},
    "quantitykind:Temperature": {"temperature"}, "quantitykind:Power": {"power"},
    "quantitykind:Irradiance": {"irradiance"}, "quantitykind:Velocity": {"speed"},
    "quantitykind:Pressure": {"pressure"}, "quantitykind:Currency": {"money"},
    "quantitykind:DimensionlessRatio": {"ratio"}, "quantitykind:Time": {"time"},
    "quantitykind:Angle": {"angle"}, "quantitykind:Volume": {"volume"},
}
