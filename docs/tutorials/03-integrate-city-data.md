# Tutorial 3: integrate benchmarking, tax lots, footprints and weather

Goal: build the input table of a physics-based UBEM for New York City buildings from four open sources, one per
data category: energy benchmarking (LL84), tax lots (PLUTO), building footprints, and typical-year weather files.
This is the integration of the paper's city case, on a 40-building sample. About 10 minutes.

## 1. The sources and their keys

| Dataset | Category | Keys | Pitfalls recorded in its entry |
|---|---|---|---|
| LL84 benchmarking 2023 | microscopic energy | BBL (tax lot), BIN (building) | units only in field names (kBtu, kWh, therms, ft²); "Not Available"; several BBLs or BINs in one field |
| PLUTO | building characteristics | BBL; latitude and longitude | `yearbuilt = 0` means unknown; one record per lot |
| Building footprints | building stock geometry | BIN; polygon | heights in feet; 0 means unknown; placeholder BINs 1000000 ... 5000000; `shape_area` in Web Mercator |
| TMYx weather, 4 stations | weather | station coordinates | EPW timestamps are interval-ending, local standard time |

## 2. Profiles

Profile each tabular source as in tutorial 1 (or use the reviewed profiles in `examples/nyc/*.reviewed.ubem.yaml`).
The profiles say which column holds which key (`join_key: parcel_id`, `join_key: building_id`) and which codes
are placeholders.

## 3. The recipe

`examples/nyc/recipe.yaml`:

```yaml
base: ll84
datasets:
  ll84:       {data: ll84_sample.csv, profile: ll84.reviewed.ubem.yaml}
  pluto:      {data: pluto_sample.csv, profile: pluto.reviewed.ubem.yaml}
  footprints: {data: footprints_sample.csv, profile: footprints.reviewed.ubem.yaml}
  weather:    {epw: ["../../data/raw/nyc/weather/*.zip"]}
needs:                                   # output column: [dataset, concept, optional column]
  floor_area_m2:   [ll84, gross_floor_area, property_gfa_calculated_1]
  site_energy_kwh: [ll84, total_energy_consumption]
  year_built:      [pluto, year_of_construction]
  floors:          [pluto, floors_above_ground]
  roof_height_m:   [footprints, building_height]
links:
  - {from: ll84, to: pluto, key: parcel_id, multi: first}
  - {from: ll84, to: footprints, key: building_id, multi: all, aggregate: {roof_height_m: max}}
  - {from: ll84, to: weather, nearest: true, lat: latitude, lon: longitude}
```

Get the weather files first: `python scripts/download_nyc.py --only weather`.

## 4. Run it

```bash
cd examples/nyc
ubem-link integrate recipe.yaml -o ../../out/nyc_ubem_inputs.csv
```

```
                                                               link  records  linked  linked_pct
         ll84 -> pluto (parcel_id: nyc_borough_block_and_lot = bbl)       40      39        97.5
ll84 -> footprints (building_id: nyc_building_identification = bin)       40      39        97.5
                                  ll84 -> weather (nearest station)       40      38        95.0
```

The output has one row per property with floor area in m², energy in kWh, construction year, floors, roof height
in metres, the nearest station's EPW file and its heating and cooling degree days.

## 5. Check the integration

Two quantities from different sources must agree if the join and the units are right:

- roof height divided by the number of floors should be about 3 to 4 m (feet read as metres give about 11 m);
- LL84 floor area divided by footprint area times floors should be about 1.

On the full city data the reference integration gives 3.5 m per floor and a ratio of 1.04 (paper, Section 7).
Such cross-source checks catch errors that no single dataset reveals.
