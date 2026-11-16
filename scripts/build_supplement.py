"""Build the supplementary material (paper/supplement.md -> paper/build/supplementary_material.docx).

    python scripts/build_supplement.py

Every table is read from paper/tables/ or generated from the code, so the supplement cannot drift from the
results. The supplement contains no author-identifying information (double-anonymized review).
"""
import json
import subprocess
from pathlib import Path

import pandas as pd
import pypandoc

ROOT = Path(__file__).resolve().parents[1]
PAPER, TAB = ROOT / "paper", ROOT / "paper" / "tables"


def md(df: pd.DataFrame, fmt: dict | None = None) -> str:
    fmt = fmt or {}
    cols = list(df.columns)
    lines = ["| " + " | ".join(str(c) for c in cols) + " |", "|" + "---|" * len(cols)]
    for r in df.itertuples(index=False):
        cells = []
        for c, v in zip(cols, r):
            if isinstance(v, float):
                v = fmt.get(c, "{:.3f}").format(v) if pd.notna(v) else ""
            cells.append(str(v).replace("|", "/").replace("\n", " "))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def section_runs() -> str:
    rows = [
        ("Mapping (T2)", "L0, L1, L2, L3", "0 and 0.7", "1 at T = 0, 4 at T = 0.7", 300),
        ("Mapping (T2)", "L2D, L2U, L2N, O0, O2D, XBR, XBE, XEA", "0", "1", 300),
        ("Normalization (T3)", "codebook entry only", "0 and 0.7", "1 at T = 0, 2 at T = 0.7", 390),
        ("Normalization (T3P)", "with the dataset card", "0", "1", 390),
        ("National pipeline (E7)", "entry only; with card", "0 and 0.7", "as T3/T3P", 11),
        ("City case (E8): selection", "L0, L2", "0", "1", "6 concepts"),
        ("City case (E8): normalization", "entry only; with card", "0", "1", "4 to 5 columns"),
    ]
    t = pd.DataFrame(rows, columns=["Task", "Conditions", "Temperature", "Runs per item", "Items"])
    return ("## S1. Runs\n\nBoth models (Qwen3 8B, Ollama tag qwen3:8b, digest 500a1f067a9f; Llama 3.1 8B, tag "
            "llama3.1:8b, digest 46e0c10c039e; both Q4_K_M quantization) were run through Ollama 0.40.16 on one "
            "NVIDIA GeForce RTX 3050 (8 GB), with an 8,192-token context, thinking disabled, seed equal to the "
            "run index, and output constrained by JSON Schema. Repeatability statistics use only the runs at "
            "T = 0.7.\n\n" + md(t))


def section_prompts() -> str:
    from meta_urban.bench import load_items, t3_items
    from meta_urban.city import norm_item, select_request
    from meta_urban.llm import t2_request, t3_request

    it = next(i for i in load_items() if i["name"] == "SQFT")
    t3 = next(i for i in t3_items() if i["name"] == "MFBTU")
    out = ["## S2. Prompts\n\nThe system prompt carries the task and the schema artifacts; the user message carries "
           "the variable. Long vocabulary blocks are shortened here to their first lines; the full prompts of "
           "every call are in the released cache.\n"]
    for lv in ("L0", "L2D", "L2", "O2D", "XBE"):
        r = t2_request(it, lv)
        head, block = r["system"].split("TARGET VOCABULARY\n")
        vocab, tail = block.split("\n\nOutput:")
        out.append(f"### Mapping, condition {lv}\n\n```\n{head}TARGET VOCABULARY\n" + "\n".join(vocab.splitlines()[:4])
                   + f"\n[... {len(vocab.splitlines()) - 4} more lines ...]\n\nOutput:{tail}\n---\n{r['user']}\n```\n")
    for prof in (False, True):
        r = t3_request(t3, profile=prof)
        sys = r["system"] if not prof else r["system"][:1600] + "\n[... dataset card continues ...]"
        out.append(f"### Normalization, {'with' if prof else 'without'} the dataset card\n\n```\n{sys}\n---\n{r['user']}\n```\n")
    r = select_request("ll84", "gross_floor_area", "compute annual energy use intensity per unit floor area", "L2")
    head, cols = r["system"].split("DATASET COLUMNS (field: display name)\n")
    out.append("### City case, column selection (L2)\n\n```\n" + head + "DATASET COLUMNS (field: display name)\n"
               + "\n".join(cols.splitlines()[:5]) + "\n[... 260 more columns ...]\n---\n" + r["user"] + "\n```\n")
    n = norm_item("site_energy_use_kbtu")
    out.append("### City case, normalization input\n\n```\n" + t3_request(n)["user"] + "\n```\n")
    return "\n".join(out)


def section_vocabulary() -> str:
    import csv

    from meta_urban.io import leaf_concepts

    links = {}
    with open(ROOT / "schema" / "vocab" / "mappings_2026-11-13.csv", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            links.setdefault(r["concept_id"], []).append(f"{r['standard']}:{r['relation']}")
    rows = [{"id": c["id"], "group": c.get("broader"), "definition": c["definition"],
             "unit": c.get("canonical_unit") or "", "links (standard:relation)": "; ".join(links.get(c["id"], []))}
            for c in leaf_concepts()]
    return ("## S3. Concept vocabulary\n\nThe 73 mapping targets with their definitions, canonical units and links "
            "to Brick 1.4.4, BEDES 2.5 and the CityGML Energy ADE 1.0. Each linked term was checked to exist in the "
            "release files; the relation type was assigned with AI assistance and has not been audited by an "
            "independent expert.\n\n" + md(pd.DataFrame(rows)))


def section_rules() -> str:
    import inspect

    from meta_urban import checks, endtoend

    return ("## S4. Profile checks\n\nVersion 1 was written on the 11 variables of the national pipeline (E7). "
            "Version 2 was written after applying version 1 to all normalization outputs of the benchmark, and "
            "committed before any profile of the New York City data was generated, but in the same commit as the LL84 "
            "catalog entry; three of its terms ('Not Available', kBtu, ft²) occur in LL84 and in neither survey, and "
            "S19 also reports version 2 without them. Both are Python functions; "
            "they use the codebook entry and the schema's unit vocabulary and are not generated from the LinkML "
            "source.\n\n### Version 1\n\n```python\n" + inspect.getsource(endtoend.profile_check)
            + "```\n\n### Version 2\n\n```python\n" + inspect.getsource(checks.expected_multiplier)
            + "\n" + inspect.getsource(checks.check) + "```\n")


def section_tables() -> str:
    out = []
    spec = [
        ("S5. Mapping accuracy by condition: intervals, surveys, concepts, design weights and abstention",
         "stats_conditions.csv", "Cluster intervals resample gold concepts. Design-weighted accuracy weights each "
         "variable by the inverse sampling fraction of its stratum (survey x rule-based draft concept)."),
        ("S6. Paired comparisons under four label sets", "stats_tests.csv",
         "Exact McNemar tests; Holm adjustment over all comparisons and both models within each label set."),
        ("S7. Run-to-run variation (temperature 0.7 runs only)", "stats_repeatability.csv", ""),
        ("S8. Accuracy with and without lexical overlap between the variable label and the gold concept",
         "stats_leakage.csv", "Overlap: the label contains the concept's label or one of its synonyms."),
        ("S9. Documentation transplant by SKOS relation of the transplanted term", "stats_e6_relations.csv", ""),
        ("S10. Quantity-kind checks on mappings (E4), strict and lenient error basis", "stats_e4_verification.csv", ""),
        ("S11. Profile checks on the national pipeline profiles (E7)", "stats_e7_confusion.csv", ""),
        ("S12. Every E7 profile that changed a national indicator", "stats_e7_errors.csv", ""),
        ("S13. Profile checks on all benchmark normalization outputs", "stats_rules_heldout.csv",
         "Excludes the 11 variables the version 1 rules were written on. Version 2 results on these data are "
         "in-sample."),
        ("S14. National indicators: reference values and design-based standard errors", "endtoend_reference_se.csv",
         "Replicate-weight variance as specified by EIA: CBECS 2018, 151 jackknife replicates with coefficient 1; "
         "RECS 2020, 60 jackknife replicates with coefficient 59/60."),
        ("S15. National indicators from AI-built profiles at all temperatures", "endtoend_quantities.csv", ""),
        ("S16. Top-code sensitivity (CBECS 2018 floors)", "downstream_topcode_sensitivity.csv", ""),
        ("S17. Effect of single normalization errors on CBECS 2018 quantities", "downstream_d3_sensitivity.csv", ""),
        ("S18. City case: columns selected by the models", "city_selection.csv",
         "The tax-lot key is described by the JoinKey value parcel_id. Correct columns per role are listed in "
         "meta_urban.city.ROLES; for floor area, the variants with and without parking are accepted."),
        ("S19. City case: AI-built profiles and profile checks",
         ["city_profiles.csv", "city_checks_heldout.csv"],
         "Second table: every distinct profile of the city runs. Error: a wrong conversion to SI units, a unit "
         "given to a column that has none in the vocabulary (an intensity), or a numeric missing code that occurs "
         "in the data. Rows with source 'post hoc units' come from the exploratory variant whose unit vocabulary "
         "also offers kBtu and therms, which version 2 of the checks does not know; they are not part of the "
         "held-out evaluation."),
        ("S20. City case: pipeline results, decomposition and the first run",
         ["city_summary.csv", "city_decomposition.csv", "city_v1_record_identifier/city_summary.csv",
          "city_v1_record_identifier/city_selection.csv"],
         "First table: model columns and model profiles. Second: model columns with gold profiles (selection "
         "only), reference columns with model profiles (normalization only), and the post hoc unit variant. "
         "Third and fourth: the first run, in which the tax-lot key was described by the concept "
         "record_identifier ('Identifier of a record, building, meter, station or respondent within the "
         "dataset'); with that definition both models chose the internal Property ID and no property was joined."),
    ]
    for title, files, note in spec:
        files = [files] if isinstance(files, str) else files
        blocks = []
        for f in files:
            p = TAB / f
            if not p.exists():
                continue
            d = pd.read_csv(p)
            for c in ("profile", "ai_profile", "profiles"):
                if c in d:
                    d[c] = d[c].astype(str).str.slice(0, 120)
            blocks.append(md(d))
        if blocks:
            out.append(f"## {title}\n\n{note}\n\n" + "\n\n".join(blocks) + "\n")
    return "\n".join(out)


def section_catalog() -> str:
    d = pd.read_csv(TAB / "catalog_linkage_by_dataset.csv").drop(columns=["Unnamed: 0"], errors="ignore")
    return ("## S21. Catalog\n\nEvery dataset with its primary UBEM role, finest public spatial granularity and "
            "best linkage to buildings. Linkage classes: shared_identifier (a field holding the same building or "
            "parcel identifier as a footprint or parcel dataset of the same jurisdiction); building_location "
            "(coordinates or addresses of individual buildings); area_code (only an area such as a census unit, "
            "postal code or climate zone); attribute_only (records of individual buildings described only by "
            "attributes, with no location); none (no usable key).\n\n" + md(d))


def section_reproducibility() -> str:
    rows = [
        ("Table 5", "meta_urban.standards", "ai_readiness_audit.csv"),
        ("Table 6, Fig. 5, Fig. 6", "meta_urban.design_report", "bench_design_conditions.csv, bench_design_tests.csv"),
        ("Table 7", "meta_urban.design_report", "bench_t3_conventions.csv"),
        ("Fig. 7", "meta_urban.bench_report", "bench_t2_coverage.csv"),
        ("Table 8, Fig. 8, S14 to S17", "meta_urban.endtoend, meta_urban.downstream", "endtoend_*.csv, downstream_*.csv"),
        ("Table 9, Fig. 9, S18 to S20", "meta_urban.city", "city_*.csv"),
        ("S5 to S13", "meta_urban.revision_stats", "stats_*.csv"),
        ("Fig. 4, S21", "meta_urban.analytics", "catalog_*.csv"),
        ("Figs. 1 to 3", "meta_urban.schema_figures", "figure files"),
    ]
    return ("## S22. Reproducibility map\n\nEach table and figure is produced by one module of the released package "
            "(`python -m <module>`), from cached model outputs, without new model calls.\n\n"
            + md(pd.DataFrame(rows, columns=["Item", "Module", "Output"])))


def main() -> None:
    parts = ["---\ntitle: \"Supplementary material\"\n---\n",
             "Meta-Urban: an AI-ready semantic schema for integrating open data in urban building energy modeling\n",
             section_runs(), section_prompts(), section_vocabulary(), section_rules(), section_tables(),
             section_catalog(), section_reproducibility()]
    src = PAPER / "supplement.md"
    src.write_text("\n\n".join(parts), encoding="utf-8")
    out = PAPER / "build" / "supplementary_material.docx"
    subprocess.run([pypandoc.get_pandoc_path(), str(src), "-o", str(out)], check=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
