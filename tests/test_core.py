from pathlib import Path

import pytest

from meta_urban import DATA_RAW
from meta_urban.codebooks import parse_codes, unit_of
from meta_urban.gold_draft import draft_label
from meta_urban.io import concept_index, load_concepts
from meta_urban.metrics import acc_at_k, cohen_kappa, mrr, run_agreement
from meta_urban.validate import validate


def test_catalog_validates():
    assert validate() == []


def test_concepts_well_formed():
    idx = concept_index()
    for c in load_concepts():
        assert c["definition"] and c["pref_label"]
        if c.get("broader"):
            assert c["broader"] in idx, c["id"]


def test_parse_codes_eq_and_space():
    codes, lo, hi, miss = parse_codes("1=Cold\n2=Cool\n7=Withheld for confidentiality", "eq")
    assert codes[0] == ["1", "Cold"] and miss == ["7"] and lo is None
    codes, lo, hi, miss = parse_codes("50 - 90\n-2 Not applicable", "space")
    assert (lo, hi) == (50.0, 90.0) and miss == ["-2"]
    codes, lo, hi, miss = parse_codes("124 – 802,588,047\nMissing=Not applicable", "eq")
    assert hi == 802588047.0 and miss == [""]


def test_units():
    assert unit_of("Annual major fuels consumption (thous Btu)", [], 1, 2) == ("unit:BTU_IT", 1000.0)
    assert unit_of("Total electricity use, in kilowatt-hours, 2020", [], 1, 2) == ("unit:KiloW-HR", 1.0)
    assert unit_of("Square footage category", [["2", "x"]], None, None) == (None, None)


def test_draft_rules_examples():
    base = dict(is_imputation_flag=False, is_replicate_weight=False, is_weight=False, unit=None, section=None,
                question=None)
    assert draft_label({**base, "name": "PBA", "label": "Principal building activity"})[0] == "building_use_type"
    assert draft_label({**base, "name": "ELHT1", "label": "Electricity used for main heating"})[0] == "energy_sources_used"
    assert draft_label({**base, "name": "MFBTU", "label": "Annual major fuels consumption (thous Btu)",
                        "unit": "unit:BTU_IT"})[0] == "total_energy_consumption"


def test_metrics():
    assert acc_at_k([["a", "b"], ["c", "a"]], ["a", "a"], 1) == 0.5
    assert mrr([["a", "b"], ["c", "a"]], ["a", "a"]) == 0.75
    assert run_agreement([["a", "b"], ["a", "c"]])["pairwise_agreement"] == 0.5
    assert cohen_kappa(["a", "b", "a"], ["a", "b", "a"]) == 1.0


@pytest.mark.skipif(not (DATA_RAW / "cbecs2018_final_public.csv").exists(), reason="run scripts/download_data.py")
def test_weighted_totals_match_eia():
    from meta_urban.downstream import d1_reference, load_cbecs

    df, _ = load_cbecs()
    d1 = d1_reference(df)
    assert (d1.rel_diff_pct.abs() < 0.1).all()


def test_mcnemar_and_gold_ok():
    import numpy as np

    from meta_urban.bench import load_items
    from meta_urban.bench_report import mcnemar_exact

    a = np.array([True] * 10 + [False] * 10)
    b = np.array([True] * 10 + [True] * 8 + [False] * 2)
    n01, n10, p = mcnemar_exact(a, b)
    assert (n01, n10) == (8, 0) and abs(p - 2 / 2 ** 8) < 1e-12
    items = load_items()
    assert len(items) == 300 and all(i["gold"] in i["gold_ok"] for i in items)


def test_endtoend_profile_checks():
    from meta_urban.endtoend import _items, gold_profile, profile_check

    items = _items()
    assert all(not profile_check(it, gold_profile(it)) for it in items.values())
    el = items[("cbecs2018", "ELBTU")]
    bad = dict(gold_profile(el), unit_multiplier=1_000_000)
    assert "multiplier disagrees with label" in profile_check(el, bad)
    gas = items[("recs2020", "BTUNG")]
    assert profile_check(gas, dict(gold_profile(gas), missing_codes=["0"]))
