# 2023 ChatGPT case-study outputs (legacy, kept for transparency)

These are the outputs reported in arXiv 2311.08535 (v1, 2023), produced with the ChatGPT-4 code-interpreter
plug-in (version of August 3, 2023) in single interactive sessions. They are kept unchanged so that the new
benchmark can be compared with them. They are not used as gold labels.

| File | What it is |
|---|---|
| `cbecs_target_schema_2023.csv` | The 2023 target schema rows for building characteristics |
| `cbecs_aligned_schema_2023.csv` | The 2023 "aligned schema" for CBECS 2018 |
| `cbecs_processed_examples/` | Example processed CBECS tables (unweighted) |
| `eia_mer_target_schema_2023.csv` | The 2023 target schema rows for macroscopic energy data |
| `eia_mer_processed/` | The 13 EIA Monthly Energy Review series split by ChatGPT |

Known problems found in 2026 (see `docs/diagnosis.md`, P2): coverage returned as raw codes
(`Regions: [3 4 1 2]`); survey weights dropped; "joint distribution list" left empty; the EIA timestamp format
given as `YYYY-MM-DD HH:MM:SS` for monthly data. The large `translated_data.csv` (53 MB) is not included.
