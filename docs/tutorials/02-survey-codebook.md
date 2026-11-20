# Tutorial 2: survey microdata, weights, flags and conventions

Goal: profile part of the 2020 Residential Energy Consumption Survey (RECS), where the hard parts are not the
units but the survey design: a final weight, 60 replicate weights, imputation flags, and codes such as -2 for
"not applicable". About 15 minutes.

## 1. Get the data

```bash
python scripts/download_data.py        # CBECS 2018, RECS 2020 and their codebooks into data/raw/ (SHA-256 checked)
```

## 2. Profile a few columns with the EIA codebook

The EIA codebook is an Excel file; the tool finds its header row ("Variable", "Description and Labels",
"Response Codes") by itself.

```bash
ubem-link describe data/raw/recs2020_public_v7.csv \
    --codebook data/raw/recs2020_codebook_v7.xlsx --entry chr-recs-2020 \
    --only DOEID NWEIGHT NWEIGHT1 TEMPHOME ZTEMPHOME KWH BTUNG TYPEHUQ YEARMADERANGE \
    --rows 2000 --out out/
```

`--entry chr-recs-2020` brings in the catalog entry, whose conventions state, among others, that imputation
flags are named `Z` + the variable they flag and that `-2` means "not applicable".

## 3. Read the review file

`out/chr-recs-2020.review.csv` lists, worst first, what to check. Things to look for:

- `NWEIGHT` should be `is_weight: true`, `NWEIGHT1` also `is_replicate_weight: true`. A weight is not an
  observation: summing households without it gives 18,496 instead of 123.5 million.
- `ZTEMPHOME` should be `is_imputation_flag: true` with `flags_variable: TEMPHOME`. The naming rule is stated only in the
  user guide, which is why it is a convention of the entry.
- `TEMPHOME` should list `-2` as a missing code and have unit `unit:DEG_F`.
- `KWH` has unit `unit:KiloW-HR`; `BTUNG` is in thousand Btu (`unit:KiloBTU_IT`).

## 4. Apply the profile

```bash
ubem-link apply out/chr-recs-2020.ubem.yaml data/raw/recs2020_public_v7.csv -o out/recs_si.csv
```

Temperatures are converted to °C, energy to kWh, and `-2` codes become empty values. The weights are kept as
columns: estimates must use them (see `src/ubem_link/endtoend.py` for weighted estimates with replicate-weight
standard errors).

## 5. Propose conventions from a user guide

If a dataset has no catalog entry yet, the tool can draft its conventions from the documentation:

```bash
ubem-link conventions user_guide.txt -o out/conventions.yaml
```

Each proposal carries the sentence of the guide it rests on (proposals whose quote does not occur in the text are
dropped) and a scope. Confirm each one before you copy it into the entry's `conventions:`.
