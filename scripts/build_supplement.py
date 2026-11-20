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
        ("Four-source case (E8b): selection", "L2", "0", "1", "16 inputs"),
        ("Four-source case (E8b): normalization", "entry; card; scoped", "0", "1", "14 to 15 columns"),
        ("Mapping, Qwen3 14B", "L0, L1, L2D, L2, L3E", "0", "1", 300),
    ]
    t = pd.DataFrame(rows, columns=["Task", "Conditions", "Temperature", "Runs per item", "Items"])
    return ("## S1. Runs\n\nThe models (Qwen3 8B, Ollama tag qwen3:8b, digest 500a1f067a9f; Llama 3.1 8B, tag "
            "llama3.1:8b, digest 46e0c10c039e; Qwen3 14B, tag qwen3:14b, digest bdbd181c33f2, with partial CPU "
            "offload; all Q4_K_M quantization) were run through Ollama 0.40.16 on one "
            "NVIDIA GeForce RTX 3050 (8 GB), with an 8,192-token context, thinking disabled, seed equal to the "
            "run index, and output constrained by JSON Schema. Repeatability statistics use only the runs at "
            "T = 0.7.\n\n" + md(t))


def section_prompts() -> str:
    from ubem_link.bench import load_items, t3_items
    from ubem_link.city import norm_item, select_request
    from ubem_link.llm import t2_request, t3_request

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
    from ubem_link.city_integration import column_doc, entry
    from ubem_link.profiler import normalize_request, scoped_conventions

    col = column_doc("footprints", "height_roof")
    r = normalize_request(col, "nyc_footprints", scoped_conventions(entry("footprints"), col), "scoped")
    head, units = r["system"].split("UNIT LIST\n")
    unit_lines, conv = units.split("\n\nCONVENTIONS", 1)
    out.append("### Four-source case: the tool's normalization prompt (scoped conventions)\n\n```\n" + head
               + "UNIT LIST\n" + "\n".join(unit_lines.splitlines()[:6])
               + f"\n[... {len(unit_lines.splitlines()) - 6} more units ...]\n\nCONVENTIONS" + conv
               + "\n---\n" + r["user"] + "\n```\n")
    return "\n".join(out)


def section_vocabulary() -> str:
    import csv

    from ubem_link.io import leaf_concepts

    links = {}
    with open(ROOT / "schema" / "vocab" / "mappings_2026-11-13.csv", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            links.setdefault(r["concept_id"], []).append(f"{r['standard']}:{r['relation']}")
    rows = [{"id": c["id"], "group": c.get("broader"), "definition": c["definition"],
             "unit": c.get("canonical_unit") or "", "links (standard:relation)": "; ".join(links.get(c["id"], []))}
            for c in leaf_concepts()]
    return ("## S4. Concept vocabulary\n\nThe 73 mapping targets with their definitions, canonical units and links "
            "to Brick 1.4.4, BEDES 2.5 and the CityGML Energy ADE 1.0. Each linked term was checked to exist in the "
            "release files; the relation type was assigned with AI assistance and has not been audited by an "
            "independent expert.\n\n" + md(pd.DataFrame(rows)))


def section_rules() -> str:
    import inspect

    from ubem_link import checks, endtoend

    return ("## S5. Profile checks\n\nVersion 1 was written on the 11 variables of the national pipeline (E7). "
            "Version 2 was written after applying version 1 to all normalization outputs of the benchmark, and "
            "committed before any profile of the New York City data was generated, but in the same commit as the LL84 "
            "catalog entry; three of its terms ('Not Available', kBtu, ft²) occur in LL84 and in neither survey, and "
            "S20 also reports version 2 without them. Both are Python functions; "
            "they use the codebook entry and the schema's unit vocabulary and are not generated from the LinkML "
            "source.\n\n### Version 1\n\n```python\n" + inspect.getsource(endtoend.profile_check)
            + "```\n\n### Version 2\n\n```python\n" + inspect.getsource(checks.expected_multiplier)
            + "\n" + inspect.getsource(checks.check) + "```\n")


def section_tables() -> str:
    out = []
    spec = [
        ("S6. Mapping accuracy by condition: intervals, surveys, concepts, design weights and abstention",
         "stats_conditions.csv", "Cluster intervals resample gold concepts. Design-weighted accuracy weights each "
         "variable by the inverse sampling fraction of its stratum (survey x rule-based draft concept)."),
        ("S7. Paired comparisons under four label sets", "stats_tests.csv",
         "Exact McNemar tests; Holm adjustment over all comparisons and both models within each label set."),
        ("S8. Run-to-run variation (temperature 0.7 runs only)", "stats_repeatability.csv", ""),
        ("S9. Accuracy with and without lexical overlap between the variable label and the gold concept",
         "stats_leakage.csv", "Overlap: the label contains the concept's label or one of its synonyms."),
        ("S10. Documentation transplant by SKOS relation of the transplanted term", "stats_e6_relations.csv", ""),
        ("S11. Quantity-kind checks on mappings (E4), strict and lenient error basis", "stats_e4_verification.csv", ""),
        ("S12. Profile checks on the national pipeline profiles (E7)", "stats_e7_confusion.csv", ""),
        ("S13. Every E7 profile that changed a national indicator", "stats_e7_errors.csv", ""),
        ("S14. Profile checks on all benchmark normalization outputs", "stats_rules_heldout.csv",
         "Excludes the 11 variables the version 1 rules were written on. Version 2 results on these data are "
         "in-sample."),
        ("S15. National indicators: reference values and design-based standard errors", "endtoend_reference_se.csv",
         "Replicate-weight variance as specified by EIA: CBECS 2018, 151 jackknife replicates with coefficient 1; "
         "RECS 2020, 60 jackknife replicates with coefficient 59/60."),
        ("S16. National indicators from AI-built profiles at all temperatures", "endtoend_quantities.csv", ""),
        ("S17. Top-code sensitivity (CBECS 2018 floors)", "downstream_topcode_sensitivity.csv", ""),
        ("S18. Effect of single normalization errors on CBECS 2018 quantities", "downstream_d3_sensitivity.csv", ""),
        ("S19. City case: columns selected by the models", "city_selection.csv",
         "The tax-lot key is described by the JoinKey value parcel_id. Correct columns per role are listed in "
         "ubem_link.city.ROLES; for floor area, the variants with and without parking are accepted."),
        ("S20. City case: AI-built profiles and profile checks",
         ["city_profiles.csv", "city_checks_heldout.csv"],
         "Second table: every distinct profile of the city runs. Error: a wrong conversion to SI units, a unit "
         "given to a column that has none in the vocabulary (an intensity), or a numeric missing code that occurs "
         "in the data. Rows with source 'post hoc units' come from the exploratory variant whose unit vocabulary "
         "also offers kBtu and therms, which version 2 of the checks does not know; they are not part of the "
         "held-out evaluation."),
        ("S21. City case: pipeline results, decomposition and the first run",
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


def section_category_profiles() -> str:
    import importlib.util

    spec = importlib.util.spec_from_file_location("make_docs", ROOT / "scripts" / "make_docs.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    body = mod.category_profiles().split("\n", 4)[-1]
    prov = pd.read_csv(ROOT / "catalog" / "category_profiles_provenance.csv")
    n_doc = int((prov.evidence == "documentation").sum())
    n_entry = int((prov.evidence == "entry_only").sum())
    return ("## S3. Category profiles\n\nEvery field of the seven category profiles, generated from the schema. "
            "The category profiles of the catalog were drafted by agents from the verified entries: "
            f"{n_entry} from the entry text alone, {n_doc} also against a publisher page, and the New York City "
            "PLUTO and footprint entries from the publishers' metadata; fields that could not be established were "
            "left empty (provenance per entry in the repository).\n\n" + body.replace("## ", "### "))


def section_city4() -> str:
    out = ["## S22. Four-source city integration (E8b)\n\nLL84 benchmarking, PLUTO tax lots, building "
           "footprints (polygons and roof heights) and TMYx weather files of four stations. Columns chosen by each "
           "model (definitions given, L2) and the profiles built with the tool's normalization prompt under four "
           "context conditions: entry (portal description and values only), card (all dataset conventions as "
           "prose), scoped (only the conventions whose machine-readable scope covers the column) and tool (scoped, "
           "with the conventions' stated values applied by the tool). Status compares a profile with the "
           "reference: error (a wrong conversion to SI units, a missing code of the reference not declared while "
           "it occurs in the data, or a frequent valid value declared missing), harmless deviation, or exact.\n"]
    for f, title in (("city4_reference.csv", "Reference pipeline"), ("city4_weather_stations.csv", "Weather stations"),
                     ("city4_selection.csv", "Columns selected"), ("city4_profiles.csv", "Profiles of the reference columns"),
                     ("city4_indicators.csv", "Indicators of the integrated table")):
        q = TAB / f
        if q.exists():
            d = pd.read_csv(q)
            out.append(f"### {title}\n\n" + md(d) + "\n")
    return "\n".join(out)


def section_larger_model() -> str:
    q = TAB / "stats_conditions.csv"
    if not q.exists():
        return ""
    d = pd.read_csv(q)
    if "model" not in d or not d.model.astype(str).str.contains("14b").any():
        return ""
    keep = d[d.model.astype(str).str.contains("qwen3")]
    return ("## S23. Model size: Qwen3 8B and Qwen3 14B\n\nCore mapping conditions for the two Qwen3 models at "
            "T = 0 (Qwen3 14B with partial CPU offload on the same 8 GB GPU).\n\n" + md(keep) + "\n")


def section_catalog() -> str:
    d = pd.read_csv(TAB / "catalog_linkage_by_dataset.csv").drop(columns=["Unnamed: 0"], errors="ignore")
    return ("## S24. Catalog\n\nEvery dataset with its primary UBEM role, finest public spatial granularity and "
            "best linkage to buildings. Linkage classes: shared_identifier (a field holding the same building or "
            "parcel identifier as a footprint or parcel dataset of the same jurisdiction); building_location "
            "(coordinates or addresses of individual buildings); area_code (only an area such as a census unit, "
            "postal code or climate zone); attribute_only (records of individual buildings described only by "
            "attributes, with no location); none (no usable key).\n\n" + md(d))


def section_reproducibility() -> str:
    rows = [
        ("Fig. 1, Section 2.3, S24", "ubem_link.analytics", "catalog_*.csv"),
        ("Figs. 2 to 4", "ubem_link.schema_figures", "figure files"),
        ("Table 4", "ubem_link.standards", "ai_readiness_audit.csv"),
        ("Table 5, Figs. 5 and 6, S23", "ubem_link.design_report, ubem_link.revision_stats",
         "bench_design_conditions.csv, stats_conditions.csv"),
        ("Table 6", "ubem_link.design_report", "bench_t3_conventions.csv"),
        ("Fig. 7", "ubem_link.bench_report", "bench_t2_coverage.csv"),
        ("Table 7, Fig. 8, S15 to S18", "ubem_link.endtoend, ubem_link.downstream", "endtoend_*.csv, downstream_*.csv"),
        ("Table 8, Fig. 9, S19 to S21", "ubem_link.city", "city_*.csv"),
        ("Table 9, S22", "ubem_link.city_integration", "city4_*.csv"),
        ("S6 to S14", "ubem_link.revision_stats", "stats_*.csv"),
        ("S3", "scripts/make_docs.py (category profiles)", "docs/category-profiles.md"),
    ]
    return ("## S25. Reproducibility map\n\nEach table and figure is produced by one module of the released package "
            "(`python -m <module>`), from cached model outputs, without new model calls.\n\n"
            + md(pd.DataFrame(rows, columns=["Item", "Module", "Output"])))


def main() -> None:
    parts = ["---\ntitle: \"Supplementary material\"\n---\n",
             "UBEM-Link: an AI-ready semantic schema for integrating open data in urban building energy modeling\n",
             section_runs(), section_prompts(), section_category_profiles(), section_vocabulary(),
             section_rules(), section_tables(), section_city4(), section_larger_model(), section_catalog(),
             section_reproducibility()]
    src = PAPER / "supplement.md"
    src.write_text("\n\n".join(parts), encoding="utf-8")
    out = PAPER / "build" / "supplementary_material.docx"
    subprocess.run([pypandoc.get_pandoc_path(), str(src), "-o", str(out)], check=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
