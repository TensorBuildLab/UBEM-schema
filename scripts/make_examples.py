"""Write the reviewed example profiles and the integration recipe for the New York City samples in examples/nyc.

The profiles are the reference (reviewed) profiles of the sample columns; tutorials compare a model's draft with
them, and the tests check that they validate and integrate.

    python scripts/make_examples.py
"""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
EX = ROOT / "examples" / "nyc"
REVIEWED = "reviewed reference profile (UBEM-Link examples)"


def var(name, concept=None, join_key=None, unit=None, mult=None, missing=None, datatype=None, **kw):
    v = {"name": name, "datatype": datatype}
    if concept:
        v["concept"] = concept
    if join_key:
        v["join_key"] = join_key
    if unit:
        v["unit"], v["unit_multiplier"] = unit, float(mult or 1)
    if missing:
        v["missing_codes"] = missing
    v.update(kw)
    v["profiled_by"] = REVIEWED
    return {k: x for k, x in v.items() if x is not None}


def entry(eid: str) -> dict:
    e = yaml.safe_load((ROOT / "catalog" / "datasets" / f"{eid}.yaml").read_text(encoding="utf-8"))
    return {k: v for k, v in e.items() if not k.startswith("_")}


NA = ["Not Available"]
PLACEHOLDER_BINS = ["1000000", "2000000", "3000000", "4000000", "5000000"]
profiles = {
    "ll84": ("chr-nyc-ll84", [
        var("property_id", concept="record_identifier", datatype="identifier"),
        var("property_name", datatype="string"),
        var("nyc_borough_block_and_lot", join_key="parcel_id", missing=NA, datatype="identifier"),
        var("nyc_building_identification", join_key="building_id", missing=NA + PLACEHOLDER_BINS, datatype="identifier"),
        var("address_1", join_key="address", datatype="string"),
        var("postal_code", join_key="postal_code", datatype="identifier"),
        var("largest_property_use_type", concept="building_use_type", missing=NA, datatype="categorical"),
        var("year_built", concept="year_of_construction", missing=NA, datatype="integer"),
        var("property_gfa_self_reported", concept="gross_floor_area", unit="unit:FT2", missing=NA, datatype="float"),
        var("property_gfa_calculated_1", concept="gross_floor_area", unit="unit:FT2", missing=NA, datatype="float"),
        var("site_energy_use_kbtu", concept="total_energy_consumption", unit="unit:KiloBTU_IT", missing=NA,
            aggregation="total_over_period", datatype="float"),
        var("electricity_use_grid_purchase_1", concept="electricity_consumption", unit="unit:KiloW-HR", missing=NA,
            aggregation="total_over_period", datatype="float"),
        var("natural_gas_use_kbtu", concept="natural_gas_consumption", unit="unit:KiloBTU_IT", missing=NA,
            aggregation="total_over_period", datatype="float"),
        var("natural_gas_use_therms_", concept="natural_gas_consumption", unit="unit:THM_US", missing=NA,
            aggregation="total_over_period", datatype="float"),
        var("site_eui_kbtu_ft", concept="energy_use_intensity", unit="unit:KiloBTU_IT-PER-FT2", missing=NA, datatype="float"),
        var("latitude", concept="geographic_coordinates", unit="unit:DEG", datatype="float"),
        var("longitude", concept="geographic_coordinates", unit="unit:DEG", datatype="float"),
    ]),
    "pluto": ("chr-nyc-pluto", [
        var("bbl", join_key="parcel_id", datatype="identifier"),
        var("borough", concept="administrative_region", datatype="categorical"),
        var("cd", concept="administrative_region", datatype="categorical"),
        var("bct2020", join_key="census_tract", datatype="identifier"),
        var("zipcode", join_key="postal_code", datatype="identifier"),
        var("bldgclass", concept="building_use_type", datatype="categorical"),
        var("landuse", concept="land_use", datatype="categorical"),
        var("yearbuilt", concept="year_of_construction", missing=["0"], datatype="integer"),
        var("numfloors", concept="floors_above_ground", datatype="float"),
        var("numbldgs", datatype="integer"),
        var("bldgarea", concept="gross_floor_area", unit="unit:FT2", missing=["0"], datatype="float"),
        var("resarea", unit="unit:FT2", missing=["0"], datatype="float"),
        var("comarea", unit="unit:FT2", missing=["0"], datatype="float"),
        var("latitude", concept="geographic_coordinates", unit="unit:DEG", datatype="float"),
        var("longitude", concept="geographic_coordinates", unit="unit:DEG", datatype="float"),
        var("version", datatype="string"),
    ]),
    "footprints": ("geo-nyc-footprints", [
        var("bin", join_key="building_id", missing=PLACEHOLDER_BINS, datatype="identifier"),
        var("base_bbl", join_key="parcel_id", datatype="identifier"),
        var("mappluto_bbl", join_key="parcel_id", datatype="identifier"),
        var("height_roof", concept="building_height", unit="unit:FT", missing=["0"], datatype="float"),
        var("ground_elevation", unit="unit:FT", missing=["0"], datatype="float"),
        var("construction_year", concept="year_of_construction", missing=["0"], datatype="integer"),
        var("feature_code", datatype="categorical"),
        var("shape_area", datatype="float", do_not_use=True),
        var("geom_source", datatype="categorical"),
        var("last_status_type", datatype="categorical"),
    ]),
}
for name, (eid, variables) in profiles.items():
    doc = entry(eid)
    doc["variables"] = variables
    (EX / f"{name}.reviewed.ubem.yaml").write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=110),
                                                   encoding="utf-8")
recipe = {
    "base": "ll84",
    "datasets": {"ll84": {"data": "ll84_sample.csv", "profile": "ll84.reviewed.ubem.yaml"},
                 "pluto": {"data": "pluto_sample.csv", "profile": "pluto.reviewed.ubem.yaml"},
                 "footprints": {"data": "footprints_sample.csv", "profile": "footprints.reviewed.ubem.yaml"},
                 "weather": {"epw": ["../../data/raw/nyc/weather/*.zip"]}},
    "needs": {"floor_area_m2": ["ll84", "gross_floor_area", "property_gfa_calculated_1"],
              "site_energy_kwh": ["ll84", "total_energy_consumption"],
              "gas_kwh": ["ll84", "natural_gas_consumption", "natural_gas_use_kbtu"],
              "use_type": ["ll84", "building_use_type"],
              "year_built": ["pluto", "year_of_construction"],
              "floors": ["pluto", "floors_above_ground"],
              "district": ["pluto", "administrative_region", "cd"],
              "roof_height_m": ["footprints", "building_height"]},
    "links": [{"from": "ll84", "to": "pluto", "key": "parcel_id", "multi": "first"},
              {"from": "ll84", "to": "footprints", "key": "building_id", "multi": "all",
               "aggregate": {"roof_height_m": "max"}},
              {"from": "ll84", "to": "weather", "nearest": True, "lat": "latitude", "lon": "longitude"}],
}
(EX / "recipe.yaml").write_text(yaml.safe_dump(recipe, sort_keys=False), encoding="utf-8")
print("wrote", sorted(p.name for p in EX.glob("*.yaml")))
