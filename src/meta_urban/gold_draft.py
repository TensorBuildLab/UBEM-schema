"""Draft concept labels for benchmark task T2 (variable -> Meta-Urban concept).

These rules PRE-FILL annotation. They are not the gold standard. The gold standard is produced by two human
annotators who accept or correct every draft label (benchmark/gold/README.md); the paper reports how many draft
labels annotators changed. The rules use codebook structure (name prefixes, label prefixes, RECS sections) and
domain knowledge of the two surveys. They are deliberately kept out of the baselines: no baseline sees them.

Output: benchmark/gold/t2_draft_<dataset>.csv with columns
    dataset, name, label, section, draft_concept, rule, annotator_1, annotator_2, adjudicated, notes
"""

from __future__ import annotations

import re

import pandas as pd

from . import BENCH
from .codebooks import load_all
from .io import concept_index

I = re.I


def _txt(x) -> str:
    return x if isinstance(x, str) else ""


def _lab(r) -> str:
    return _txt(r["label"])


def _sec(r) -> str:
    return _txt(r.get("section"))


def has(pattern: str, field=_lab):
    rx = re.compile(pattern, I)
    return lambda r: bool(rx.search(field(r)))


def sec(*names: str):
    return lambda r: _sec(r) in names


def both(*preds):
    return lambda r: all(p(r) for p in preds)


def either(*preds):
    return lambda r: any(p(r) for p in preds)


def nothas(pattern: str):
    rx = re.compile(pattern, I)
    return lambda r: not rx.search(_lab(r))


ENERGY_UNITS = {"unit:BTU_IT", "unit:KiloW-HR", "unit:FT3", "unit:GAL_US"}
is_energy_qty = lambda r: r["unit"] in ENERGY_UNITS  # noqa: E731

FUEL = (r"electricity|natural gas|fuel oil\S*|propane|bottled gas\S*|district (?:steam|heat|hot water|chilled water)|"
        r"wood|coal|solar(?: thermal)?|kerosene|other energy source|other fuel|any energy")

CARRIER = [
    (re.compile(r"\bmajor fuels?\b|total (?:site )?energy|all fuels|TOTALBTU|total usage", I), "total_energy_consumption"),
    (re.compile(r"electric|kilowatt|\bKWH", I), "electricity_consumption"),
    (re.compile(r"natural gas|cubic feet|\bCUFEET", I), "natural_gas_consumption"),
]
END_USE = re.compile(
    r"heating|cooling|ventilat|water heat|lighting|cooking|refrigerat|office equipment|computing|dehumidif|"
    r"humidif|clothes|dish|freezer|television|\bTV|pool|hot tub|spa\b|well pump|microwave|ceiling fan|evaporative|"
    r"other uses|miscellaneous|electric vehicle|appliance|furnace fan|aquarium|charging|plug", I)

# Ordered rules: (rule id, predicate, concept). First match wins. "none" means no Meta-Urban concept applies.
RULES: list[tuple[str, callable, str]] = [
    ("flag", lambda r: r["is_imputation_flag"], "imputation_flag"),
    ("repwt", lambda r: r["is_replicate_weight"], "replicate_weight"),
    ("wt", lambda r: r["is_weight"], "survey_weight"),
    ("id", lambda r: r["name"] in {"PUBID", "DOEID"}, "record_identifier"),
    ("admin", sec("ADMIN"), "survey_reference_detail"),
    ("out_of_scope", either(sec("ENERGY ASSISTANCE"),
                            has(r"unable to use|energy assistance|who pays|conversion factor|payment|disconnect|"
                                r"bill(?:s|ing)? (?:paid|included)|included in rent")), "none"),
    ("climate", both(has(r"climate"), nothas(r"degree")), "climate_zone"),
    ("geo", either(lambda r: r["name"] in {"REGION", "CENDIV", "REGIONC", "DIVISION", "STATE_FIPS", "STATE_POSTAL",
                                           "STATE_NAME"}, has(r"census (?:region|division)|\bstate\b")),
     "administrative_region"),
    ("urban", has(r"urban|rural|metropolitan"), "urban_rural_indicator"),
    ("dd", has(r"degree.?days|\bHDD|\bCDD"), "degree_days"),
    ("weather", either(has(r"design temperature"), sec("WEATHER")), "dry_bulb_temperature"),
    # energy quantities
    ("expend", either(lambda r: r["unit"] == "iso4217:USD", has(r"expenditure|\bcost\b")), "energy_expenditure"),
    ("enduse", both(is_energy_qty, lambda r: bool(END_USE.search(_lab(r)))), "end_use_energy"),
    ("carrier", is_energy_qty, "_carrier"),
    ("eui", has(r"intensity|per square f"), "energy_use_intensity"),
    ("peak", has(r"\bpeak\b|demand charge|kW demand"), "peak_demand"),
    # fuel-use flags come before system rules ("Electricity used for space heating" is a fuel flag)
    ("fuelused", either(has(rf"^(?:derived variable: )?(?:{FUEL})\b.*\bused\b"), has(r"fuel used (?:by|for)|main .*fuel|"
                                                                                       r"fuel for|energy source")),
     "energy_sources_used"),
    # geometry
    ("sqftc", has(r"square footage category|size category"), "floor_area_category"),
    ("sqft", either(lambda r: r["unit"] == "unit:FT2", has(r"square footage|floorspace")), "gross_floor_area"),
    ("basement", has(r"basement|below ground|crawl ?space|attic"), "floors_below_ground"),
    ("floors", has(r"number of floors|stories|storeys"), "floors_above_ground"),
    ("ceil", has(r"ceiling height|floor.to.ceiling"), "floor_to_ceiling_height"),
    ("shape", has(r"building shape"), "building_shape"),
    ("rooftilt", has(r"roof tilt|roof shape|roof slope"), "roof_shape"),
    ("wwr", has(r"percent(?:age)? (?:of )?(?:exterior )?(?:wall )?(?:that is )?glass"), "window_to_wall_ratio"),
    # characteristics
    ("vintage", both(has(r"year (?:of )?construct|when .*built|year built|range when"),
                     nothas(r"equipment|appliance|refrigerator|freezer|furnace|heater|dryer|washer|conditioner|"
                            r"heat pump|computer|television")), "year_of_construction"),
    ("renov", has(r"renovat|retrofit|remodel|addition or annex|\bannex\b"), "renovation"),
    ("wall", has(r"wall (?:construction|material)|exterior wall|siding"), "wall_construction"),
    ("roofc", has(r"roof (?:construction|material)|cool roof|roof color|reflective roof|roofing"), "roof_construction"),
    ("window", both(has(r"\bwindows?\b|glazing|\bpanes?\b|tinted|reflective glass|skylight|glass door|type of glass|"
                        r"\bglass\b"), nothas(r"window (?:fan|air|unit)|or window fans?|window or wall|drive-?thru")), "window_properties"),
    ("insul", has(r"insulat|weatheriz|drafty|caulk|weather.?strip"), "insulation"),
    ("pba", has(r"principal building activity|building activity|type of housing unit|housing unit type|"
                r"type of complex|more specific"), "building_use_type"),
    ("units", has(r"number of (?:housing |apartment |dwelling )?units|units in (?:the )?building|apartments in"),
     "dwelling_units"),
    ("own", has(r"\bown(?:ed|er|ership|s)?\b|\brent|tenan|government|vacan|occupied by|franchise|\bchain\b|"
                r"percent occupancy|owner.occupied"), "ownership_tenure"),
    ("rooms", has(r"bedrooms|number of rooms|rooms\b|seat|beds\b|classroom|courtroom|bathroom|cafeteria|kitchen|"
                  r"food prep|restaurant|laundry|dry cleaning|data cent|server room|garage|parking|atrium|"
                  r"laborator|walk-in|dormitor|space used|floorspace used|vacant space|swimming pool area"),
     "rooms_and_spaces"),
    ("ctrl", has(r"energy management|building automation|\bBAS\b|smart thermostat|programmable|demand response|"
                 r"\bcontrols?\b|occupancy sensor|timer|smart (?:meter|speaker|plug)|setback|"
                 r"energy audit|benchmark"), "building_controls"),
    ("setpt", either(sec("THERMOSTAT"), has(r"thermostat setting|set ?point|temperature (?:inside|in home|when)")),
     "thermostat_setpoint"),
    ("gen", has(r"solar|photovoltaic|generat|cogenerat|battery|wind turbine|microturbine|fuel cell"),
     "onsite_generation"),
    ("dhw", either(has(r"water heat|hot water|tankless"), sec("WATER HEATING")), "water_heating_system"),
    ("cool", either(has(r"cool(?:ing)? (?:equipment|system)|air.condition|chiller|cooled|cooling|\bAC\b|A/C|"
                        r"evaporative|\bVRF\b|rooftop unit|packaged|split system|ceiling fan|whole house.*fan|"
                        r"dehumid|swamp|chilled water"), sec("AIR CONDITIONING")), "cooling_system"),
    ("heat", either(has(r"heat(?:ing)? (?:equipment|system)|furnace|boiler|heat pump|space heat|heated|heating|"
                        r"radiator|baseboard|fireplace|stove used for heat|reheat|steam distribution"),
                    sec("SPACE HEATING")), "heating_system"),
    ("vent", has(r"ventilat|economizer|variable air volume|\bVAV\b|\bDOAS\b|\bDCV\b|air handl|exhaust|"
                 r"fan coil|induction unit|duct"), "ventilation_system"),
    ("light", either(has(r"light|lamp|bulb|\bLED|fluorescent|halogen|incandescent|daylight"), sec("LIGHTING")),
     "lighting_system"),
    ("equip", either(has(r"computer|server|refrigerat|freezer|cooking|oven|stove|range\b|cooktop|microwave|"
                         r"television|\bTV|printer|copier|appliance|washer|dryer|dishwasher|elevator|escalator|"
                         r"vending|ice maker|laptop|tablet|game|internet|modem|router|pool|hot tub|\bspa\b|"
                         r"well pump|\bfans?\b|humidif|aquarium|electronic|devices?|monitors?|whiteboard|x-ray|"
                         r"accelerator|\bMRI\b|\bCT\b|scanner|machines?|\bEV\b|electric vehicle|equipment|"
                         r"coffee|toaster|grill|blender|charger|cell ?phone|register|point-of-sale"),
                     sec("APPLIANCES", "ELECTRONICS")), "plug_and_process_equipment"),
    # operation
    ("hours", has(r"hours|open (?:during|on|24)|weekend|days per week|schedule|open continuously"), "operating_hours"),
    ("occ", has(r"number of (?:employees|workers|people|household members|occupants)|employees|household members|"
                r"people (?:live|living)|number of (?:adults|children)"), "occupant_count"),
    ("demo", either(sec("HOUSEHOLD CHARACTERISTICS"),
                    has(r"income|age of (?:respondent|householder)|education|employ|race|ethnic|hispanic|"
                        r"sex of|gender|disabilit|medical device|telework|work from home")), "household_demographics"),
    ("usage", has(r"how often|frequency|times per|hours per day|per week|loads"), "equipment_usage_behavior"),
]


def draft_label(row: dict) -> tuple[str, str]:
    for rid, pred, concept in RULES:
        if pred(row):
            if concept == "_carrier":
                text = _lab(row) + " " + row["name"]
                for pat, cid in CARRIER:
                    if pat.search(text):
                        return cid, rid
                return "other_fuel_consumption", rid
            return concept, rid
    return "none", "none"


def build() -> pd.DataFrame:
    df = load_all()
    known = set(concept_index())
    out = []
    for row in df.to_dict("records"):
        cid, rid = draft_label(row)
        assert cid == "none" or cid in known, cid
        out.append(dict(dataset=row["dataset"], name=row["name"], label=row["label"], section=row["section"],
                        draft_concept=cid, rule=rid, annotator_1="", annotator_2="", adjudicated="", notes=""))
    res = pd.DataFrame(out)
    (BENCH / "gold").mkdir(parents=True, exist_ok=True)
    for ds, part in res.groupby("dataset"):
        part.to_csv(BENCH / "gold" / f"t2_draft_{ds}.csv", index=False, encoding="utf-8")
    return res


if __name__ == "__main__":
    res = build()
    print(res.groupby(["dataset"]).draft_concept.apply(lambda s: (s != "none").mean()).rename("share_mapped"))
    print(res.draft_concept.value_counts().to_string())
