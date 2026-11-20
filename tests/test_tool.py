"""Tests of the ubem-link tool: readers, units, conventions, the files backend, apply and integrate."""

import json
from pathlib import Path

import pandas as pd
import pytest
import yaml

from ubem_link import ROOT
from ubem_link.apply import apply_profile
from ubem_link.cli import main as cli
from ubem_link.integrate import run_recipe, split_keys
from ubem_link.profiler import convention_matches, scoped_conventions
from ubem_link.readers import Column, describe_columns, read_codebook, read_table
from ubem_link.units import to_canonical, unit_choices
from ubem_link.validate import validate_profile

EX = ROOT / "examples" / "nyc"


def test_units_convert_publisher_units():
    assert to_canonical(1000.0, "unit:KiloBTU_IT", 1)[0] == pytest.approx(293.0710702)
    assert to_canonical(1000.0, "unit:BTU_IT", 1000)[0] == pytest.approx(293.0710702)
    assert to_canonical(212.0, "unit:DEG_F", 1)[0] == pytest.approx(100.0)
    assert to_canonical(10.0, "unit:DEG_F", 1, difference=True)[0] == pytest.approx(10 / 1.8)
    assert to_canonical(100.0, "unit:FT", 1) == (pytest.approx(30.48), "unit:M")
    assert "unit:THM_US" in unit_choices() and "none" in unit_choices()


def test_readers_detect_codebook_formats(tmp_path):
    soc = read_codebook(EX / "footprints_dictionary.json")
    assert "height_roof" in soc
    md = read_codebook(EX / "footprints_metadata.md")
    assert "feet" in md["HEIGHT_ROOF"].description
    cb = tmp_path / "codebook.csv"
    cb.write_text("Variable,Label,Units,Values\nTEMPHOME,Thermostat when home,deg F,50-90; -2=Not applicable\n"
                  "KWH,Annual electricity,kWh,0-200000\n", encoding="utf-8")
    g = read_codebook(cb)
    assert g["TEMPHOME"].unit_text == "deg F" and "Not applicable" in g["TEMPHOME"].codes_text
    df = read_table(EX / "footprints_sample.csv")
    cols = describe_columns(df, md)
    h = next(c for c in cols if c.name == "height_roof")
    assert "feet" in h.description and h.value_min is not None


def test_convention_scope_is_machine_readable():
    e = yaml.safe_load((ROOT / "catalog" / "datasets" / "geo-nyc-footprints.yaml").read_text(encoding="utf-8"))
    h = scoped_conventions(e, Column("height_roof"))
    assert any(c.get("unit") == "unit:FT" for c in h)
    assert not scoped_conventions(e, Column("feature_code"))
    assert convention_matches({"applies_to_pattern": "kbtu(?!.*ft)"}, "site_energy_use_kbtu")
    assert not convention_matches({"applies_to_pattern": "kbtu(?!.*ft)"}, "site_eui_kbtu_ft")


def _answer(req: dict) -> dict:
    """A deterministic stand-in for a model: wrong on purpose for height (metres), so that the convention must fix it."""
    props = req["schema"]["properties"]
    if "concept" in props:
        ids = props["concept"]["enum"]
        pick = "building_height" if "height_roof" in req["user"] and "building_height" in ids else "none"
        return {"concept": pick, "alternatives": [], "confidence": 0.9}
    unit = "unit:M" if "height_roof" in req["user"] else "none"
    return {"datatype": "float", "unit": unit, "unit_multiplier": 1, "missing_codes": [], "codes": [],
            "is_weight": False, "is_replicate_weight": False, "is_imputation_flag": False, "flags_variable": "none",
            "aggregation": "static"}


def test_files_backend_round_trip_and_conventions(tmp_path):
    work, out = tmp_path / "work", tmp_path / "out"
    args = ["describe", str(EX / "footprints_sample.csv"), "--codebook", str(EX / "footprints_dictionary.json"),
            "--entry", "geo-nyc-footprints", "--retrieval", "lexical", "--only", "height_roof", "feature_code",
            "--model", f"files:{work}", "--cache", str(tmp_path / "cache"), "--out", str(out)]
    assert cli(args) == 3  # requests queued for an assistant
    reqs = [json.loads(x) for x in (work / "requests.jsonl").read_text(encoding="utf-8").splitlines()]
    assert len(reqs) == 4
    with open(work / "responses.jsonl", "w", encoding="utf-8") as fh:
        for r in reqs:
            fh.write(json.dumps({"key": r["key"], "response": _answer(r)}) + "\n")
    assert cli(["pending", str(work)]) == 0
    assert cli(args) == 0
    doc = yaml.safe_load((out / "geo-nyc-footprints.ubem.yaml").read_text(encoding="utf-8"))
    assert validate_profile(doc) == []
    h = next(v for v in doc["variables"] if v["name"] == "height_roof")
    assert h["unit"] == "unit:FT" and "0" in h["missing_codes"]            # the convention overrode the answer
    assert any("convention set unit" in f for f in h["review_flags"])     # and the disagreement is flagged
    review = pd.read_csv(out / "geo-nyc-footprints.review.csv")
    assert list(review.columns)[:3] == ["name", "concept", "unit"]


def test_apply_and_integrate_examples(tmp_path):
    prof = yaml.safe_load((EX / "footprints.reviewed.ubem.yaml").read_text(encoding="utf-8"))
    df = read_table(EX / "footprints_sample.csv")
    out, rep = apply_profile(df, prof["variables"])
    assert "shape_area" not in out  # publisher says do not use
    h = pd.to_numeric(df.height_roof, errors="coerce")
    assert out.height_roof.max() == pytest.approx(h.max() * 0.3048)
    assert split_keys(pd.Series(["3059154; 3059153", "1000000", "Not Available"]), "all", {"1000000", "Not Available"}) \
        .tolist() == [["3059154", "3059153"], [], []]
    recipe = yaml.safe_load((EX / "recipe.yaml").read_text(encoding="utf-8"))
    if not list((EX / "../../data/raw/nyc/weather").glob("*.zip")):
        recipe["datasets"].pop("weather")
        recipe["links"] = [lk for lk in recipe["links"] if not lk.get("nearest")]
    table, report = run_recipe(recipe, EX)
    assert len(table) == 40 and report.linked.iloc[0] >= 35
    assert table["footprints.roof_height_m"].median() < 100  # metres, not feet


def test_reviewed_example_profiles_validate():
    for p in EX.glob("*.reviewed.ubem.yaml"):
        assert validate_profile(yaml.safe_load(p.read_text(encoding="utf-8"))) == [], p.name
