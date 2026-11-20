# Tutorial 1: profile a dataset with a local model

Goal: describe New York City's building footprints, a dataset whose portal dictionary leaves most columns
undocumented, and see what the tool does with the publisher's separate metadata page. About 10 minutes.

## 1. Install

```bash
git clone https://github.com/TensorBuildLab/UBEM-schema && cd UBEM-schema
pip install -e .
ollama pull qwen3:8b && ollama pull nomic-embed-text     # https://ollama.com; about 5.5 GB in total
```

## 2. Look at the data

`examples/nyc/footprints_sample.csv` holds 39 footprints of benchmarked buildings. The portal's dictionary
(`footprints_dictionary.json`) describes `bin` and `base_bbl` but says nothing about `height_roof`,
`construction_year` or units. The publisher's metadata page (`footprints_metadata.md`, from
github.com/CityOfNewYork/nyc-geo-metadata) says that heights are in feet above ground, that zero means "not
available", and that `shape_area` must not be used.

## 3. Profile it, first with the portal dictionary only

```bash
ubem-link describe examples/nyc/footprints_sample.csv \
    --codebook examples/nyc/footprints_dictionary.json \
    --dataset-id nyc-footprints-draft --conventions none --out out/
```

Open `out/nyc-footprints-draft.review.csv`. Columns are ordered by how much they need a person's attention. Check
`height_roof`: with no documentation of its unit, a small model has to guess from values between 18 and 459 (feet, which the dictionary does not say).

## 4. Profile it with the metadata page and the catalog entry

```bash
ubem-link describe examples/nyc/footprints_sample.csv \
    --codebook examples/nyc/footprints_dictionary.json examples/nyc/footprints_metadata.md \
    --entry geo-nyc-footprints --out out/
```

The entry `catalog/datasets/geo-nyc-footprints.yaml` states the publisher's conventions with machine-readable
scopes, for example:

```yaml
- convention_type: unit
  applies_to_variables: [height_roof, ground_elevation]
  rule: Heights and elevations are in feet; the roof height is measured above the ground elevation.
  unit: unit:FT
- convention_type: do_not_use
  applies_to_variables: [shape_area, shape_length]
  rule: Do not use; these values are generated in Web Mercator, which does not preserve area or length.
```

The tool shows `height_roof` only the conventions that concern it, and writes `unit: unit:FT` whatever the model
answered; if the model disagreed, the review file says so. `shape_area` is marked `do_not_use`. (It is 1.74 times
the true footprint area at New York's latitude.)

## 5. Validate, compare with the reviewed profile, apply

```bash
ubem-link validate out/geo-nyc-footprints.ubem.yaml
diff <(grep -A3 "name: height_roof" out/geo-nyc-footprints.ubem.yaml) \
     <(grep -A3 "name: height_roof" examples/nyc/footprints.reviewed.ubem.yaml)
ubem-link apply examples/nyc/footprints.reviewed.ubem.yaml examples/nyc/footprints_sample.csv -o out/footprints_si.csv
```

`footprints_si.csv` has heights in metres, zeros removed and `shape_area` dropped;
`footprints_si.columns.csv` lists what was done to each column.

## What to take away

The model is useful for the many routine columns; the facts that decide whether results are right (units,
missing codes, fields not to use) come from the publisher's documentation, are recorded once in the dataset entry
with a scope, and are applied by the tool. The review file tells you where to look.
