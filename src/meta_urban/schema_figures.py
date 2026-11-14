"""Figures that present the schema itself (paper Section 4).

    python -m meta_urban.schema_figures

fig_architecture      one LinkML source, domain knowledge in, two audiences out (people and AI systems)
fig_class_diagram     classes, key fields and relations of Meta-Urban 2.0
fig_worked_example    CBECS 2018 described with the schema: dataset card, three variable profiles, concept cards
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import yaml  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

from . import PAPER, SCHEMA_YAML  # noqa: E402
from .analytics import save_fig  # noqa: E402
from .io import concept_index, leaf_concepts, load_concepts  # noqa: E402

FIG = PAPER / "figures"
INK, INK2, MUTED, LINE = "#0b0b0b", "#52514e", "#898781", "#c9c8c1"
DOMAIN, SOURCE, HUMAN, AIC = "#f4f4f1", "#e6eefb", "#f4f4f1", "#dcebdc"
BLUE, GREEN = "#256abf", "#2f7d32"
plt.rcParams.update({"font.family": "DejaVu Sans"})


def box(ax, x, y, w, h, title, lines=(), fc=DOMAIN, ec=LINE, tsize=8.6, lsize=7.2, tcolor=INK, lw=1.0):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.012", fc=fc, ec=ec, lw=lw))
    ax.text(x + 0.012, y + h - 0.018, title, fontsize=tsize, weight="bold", color=tcolor, va="top")
    for i, t in enumerate(lines):
        ax.text(x + 0.014, y + h - 0.058 - i * 0.034, t, fontsize=lsize, color=INK2, va="top")


def arrow(ax, p0, p1, color=MUTED, lw=1.3, style="-|>", ls="-"):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=11, color=color, lw=lw, linestyle=ls,
                                 shrinkA=0, shrinkB=0))


def canvas(w=7.2, h=4.4):
    fig = plt.figure(figsize=(w, h), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    return fig, ax


# ------------------------------------------------------------------------------------------ architecture
def fig_architecture(path):
    fig, ax = canvas(7.2, 3.7)
    L = 0.046  # line height in axes units
    T, S = 7.4, 6.3  # title and line font sizes

    def col(x, w, y_top, blocks, gap=0.03):
        """Stack boxes top-down; each block = (title, lines, fc, ec, tcolor). Returns box centers."""
        centers = []
        y = y_top
        for title, lines, fc, ec, tc in blocks:
            h = 0.075 + L * len(lines)
            ax.add_patch(FancyBboxPatch((x, y - h), w, h, boxstyle="round,pad=0,rounding_size=0.012", fc=fc, ec=ec,
                                        lw=1.0))
            ax.text(x + 0.01, y - 0.016, title, fontsize=T, weight="bold", color=tc, va="top")
            for i, t in enumerate(lines):
                ax.text(x + 0.012, y - 0.062 - i * L, t, fontsize=S, color=INK2, va="top")
            centers.append((x, y - h / 2, w, y - h))
            y -= h + gap
        return centers

    heads = [(0.01, "Domain knowledge"), (0.225, "One source (LinkML)"), (0.505, "Compiled artifacts"),
             (0.79, "Enables")]
    for x, t in heads:
        ax.text(x, 0.985, t, fontsize=7.8, weight="bold", color=INK, va="top")
    top = 0.925
    src = col(0.01, 0.195, top, [("Sources", ["UBEM workflow roles", "survey methodology:", "  weights, imputation,",
                                              "  top-codes", "CityGML, Energy ADE,", "  BEDES, Brick",
                                              "DCAT 3, SKOS, QUDT,", "  CSVW", "codebooks and", "  user guides"],
                                   DOMAIN, LINE, INK)])
    mid = col(0.225, 0.26, top, [
        ("Dataset level", ["DCAT 3 profile; six facets:", "role, statistical nature,", "granularity, time step,",
                           "access, join keys; weights,", "conventions, verification"], SOURCE, BLUE, BLUE),
        ("Variable level", ["CSVW profile: concept,", "QUDT unit and multiplier,", "codes, missing codes,",
                            "weight and imputation flags"], SOURCE, BLUE, BLUE),
        ("Concept vocabulary", ["81 SKOS concepts, each defined;", "168 verified links to Brick,",
                                "BEDES, Energy ADE"], SOURCE, BLUE, BLUE)], gap=0.025)
    right = col(0.505, 0.265, top, [
        ("For people", ["YAML schema and catalog,", "documentation, OWL ontology"], HUMAN, LINE, INK),
        ("For AI systems", ["schema card (~4k tokens)", "concept cards (~60 tokens each)",
                            "dataset cards with conventions", "JSON Schema: constrained output",
                            "SHACL: checks on AI output"], AIC, GREEN, GREEN)])
    use = col(0.79, 0.2, top, [
        ("People", ["find, judge and join", "datasets; audit AI"], HUMAN, LINE, INK),
        ("AI systems", ["profile datasets", "map variables", "normalize codes", "  and units",
                        "check own answers"], AIC, GREEN, GREEN)])
    sx = src[0][0] + 0.195
    for (x, yc, w, yb) in mid:
        arrow(ax, (sx + 0.003, yc), (x - 0.003, yc))
    mx = mid[0][0] + 0.26
    arrow(ax, (mx + 0.003, mid[0][1]), (0.502, right[0][1]))
    arrow(ax, (mx + 0.003, mid[1][1]), (0.502, right[1][1]), color=GREEN)
    arrow(ax, (mx + 0.003, mid[2][1]), (0.502, right[1][1] - 0.04), color=GREEN)
    for a_, b_, c in ((right[0], use[0], MUTED), (right[1], use[1], GREEN)):
        arrow(ax, (0.505 + 0.265 + 0.003, a_[1]), (0.787, b_[1]), color=c)
    yb = min(use[1][3], right[1][3]) - 0.035
    arrow(ax, (0.89, use[1][3] - 0.005), (0.89, yb), color=GREEN, style="-")
    arrow(ax, (0.89, yb), (0.64, yb), color=GREEN, style="-")
    arrow(ax, (0.64, yb), (0.64, right[1][3] - 0.004), color=GREEN)
    ax.text(0.765, yb - 0.012, "AI output checked against the same schema", fontsize=6, color=GREEN, ha="center",
            va="top")
    save_fig(fig, path)
    plt.close(fig)


# ------------------------------------------------------------------------------------------ class diagram
def _cls(ax, x, y, w, name, fields, fc=SOURCE, ec=BLUE, fs=5.5):
    h = 0.048 + 0.03 * len(fields)
    ax.add_patch(FancyBboxPatch((x, y - h), w, h, boxstyle="round,pad=0,rounding_size=0.008", fc=fc, ec=ec, lw=1.0))
    ax.add_patch(FancyBboxPatch((x, y - 0.042), w, 0.042, boxstyle="round,pad=0,rounding_size=0.008", fc=ec, ec=ec))
    ax.text(x + w / 2, y - 0.021, name, fontsize=7, weight="bold", color="white", ha="center", va="center")
    for i, f in enumerate(fields):
        ax.text(x + 0.007, y - 0.058 - 0.03 * i, f, fontsize=fs, color=INK2, va="center", family="DejaVu Sans Mono")
    return (x, y - h, w, h)


def fig_class_diagram(path):
    fig, ax = canvas(7.2, 4.5)
    cat = _cls(ax, 0.01, 0.97, 0.16, "Catalog", ["datasets*", "concepts*"])
    ds = _cls(ax, 0.215, 0.97, 0.32, "DatasetProfile (dcat:Dataset)", [
        "id, title, publisher, license, doi", "access_level: AccessLevel", "ubem_roles: UBEMRole*",
        "statistical_nature: StatisticalNature", "spatial_granularity: SpatialGranularity",
        "temporal_resolution: ISO 8601 duration", "join_keys: JoinKey*",
        "sampling_weights  (required if survey)", "verified: date, by, sources_checked"])
    dist = _cls(ax, 0.585, 0.97, 0.19, "Distribution", ["format, access_url", "api, registration"])
    conv = _cls(ax, 0.585, 0.80, 0.19, "Convention", ["applies_to", "rule", "example"], fc="#eef6ee", ec=GREEN)
    var = _cls(ax, 0.215, 0.58, 0.32, "VariableProfile (csvw:Column)", [
        "name, label, description, datatype", "concept: UBEMConcept", "mapping_relation: SKOS relation",
        "unit (QUDT), unit_multiplier", "aggregation, entity", "missing_codes",
        "is_weight, is_replicate_weight", "is_imputation_flag, flags_variable"])
    code = _cls(ax, 0.01, 0.43, 0.16, "CodeEntry", ["code", "meaning"])
    con = _cls(ax, 0.585, 0.58, 0.23, "UBEMConcept (skos:Concept)", [
        "id, pref_label, definition", "broader: UBEMConcept", "entity, quantity_kind", "canonical_unit (QUDT)",
        "alt_labels", "exact/close/broad/narrow/", "  related_match"])
    ext = _cls(ax, 0.86, 0.58, 0.13, "External", ["Brick 1.4", "BEDES 2.5", "Energy ADE", "CityGML, EPW"],
               fc=DOMAIN, ec=MUTED)
    _cls(ax, 0.585, 0.29, 0.405, "Enumerations (every value defined)", [
        "UBEMRole (7)        StatisticalNature (12)", "SpatialGranularity (17, ranked)   JoinKey (24)",
        "AccessLevel (5)     Aggregation (6)    EntityType (12)"], fc=DOMAIN, ec=MUTED)

    def mid_r(b):
        return (b[0] + b[2], b[1] + b[3] / 2)

    def mid_l(b):
        return (b[0], b[1] + b[3] / 2)

    def lab(p0, p1, t, c=MUTED, dy=0.014):
        ax.text((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2 + dy, t, fontsize=5.6, color=c, ha="center")

    p0, p1 = (cat[0] + cat[2], cat[1] + cat[3] / 2), (ds[0], cat[1] + cat[3] / 2)
    arrow(ax, p0, p1, lw=1.0); lab(p0, p1, "1..*")
    p0, p1 = (ds[0] + ds[2], dist[1] + dist[3] / 2), mid_l(dist)
    arrow(ax, p0, p1, lw=1.0); lab(p0, p1, "1..*")
    p0, p1 = (ds[0] + ds[2], conv[1] + conv[3] / 2), mid_l(conv)
    arrow(ax, p0, p1, color=GREEN, lw=1.0); lab(p0, p1, "0..*", GREEN)
    p0, p1 = (ds[0] + ds[2] / 2, ds[1]), (ds[0] + ds[2] / 2, var[1] + var[3])
    arrow(ax, p0, p1, lw=1.0); ax.text(p0[0] + 0.01, (p0[1] + p1[1]) / 2, "variables 0..*", fontsize=5.6, color=MUTED, va="center")
    p0, p1 = mid_l(var), mid_r(code)
    p0 = (var[0], code[1] + code[3] / 2)
    arrow(ax, p0, p1, lw=1.0); lab(p0, p1, "0..*")
    p0, p1 = (var[0] + var[2], con[1] + con[3] - 0.09), (con[0], con[1] + con[3] - 0.09)
    arrow(ax, p0, p1, lw=1.0); lab(p0, p1, "concept")
    p0, p1 = (con[0] + con[2], ext[1] + ext[3] / 2), mid_l(ext)
    arrow(ax, p0, p1, lw=1.0); lab(p0, p1, "match", dy=0.012)
    ax.text(0.215, 0.115, "* list.  Every class, field and enumeration value carries a definition; the same source\n"
            "compiles to JSON Schema (structured output), SHACL (validation) and OWL.", fontsize=6.2, color=INK2,
            va="top")
    save_fig(fig, path)
    plt.close(fig)


# ------------------------------------------------------------------------------------------ worked example
def fig_worked_example(path):
    fig, ax = canvas(7.2, 3.9)
    mono = dict(family="DejaVu Sans Mono", fontsize=6.1, color=INK, va="top")
    ax.text(0.01, 0.985, "a  Dataset card (excerpt)", fontsize=8.2, weight="bold", va="top")
    ax.add_patch(FancyBboxPatch((0.01, 0.415), 0.47, 0.53, boxstyle="round,pad=0,rounding_size=0.01", fc=SOURCE, ec=BLUE))
    ds = ("id: chr-cbecs-2018\n"
          "title: 2018 Commercial Buildings Energy\n"
          "       Consumption Survey (CBECS)\n"
          "ubem_roles: [building_characteristics,\n"
          "             calibration_validation]\n"
          "statistical_nature: sample_survey_weighted\n"
          "spatial_granularity: census_region_division\n"
          "join_keys: [census_region_division,\n"
          "            building_type]\n"
          "sampling_weights: FINALWT, FINALWT1-151\n"
          "conventions:\n"
          "- applies_to: names starting with Z\n"
          "  rule: Z<NAME> flags imputation of <NAME>;\n"
          "        0 reported, 1 imputed, 9 inapplicable\n"
          "- rule: 994/995 are top-codes, not numbers\n"
          "- rule: energy in thousand Btu (x1,000)")
    ax.text(0.022, 0.93, ds, **mono, linespacing=1.32)
    ax.text(0.51, 0.985, "b  Variable profiles", fontsize=8.2, weight="bold", va="top")
    vars_ = [("MFBTU  'Annual major fuels consumption (thous Btu)'",
              "concept: total_energy_consumption (exact)\nunit: unit:BTU_IT  multiplier: 1000\naggregation: total_over_period"),
             ("NFLOOR  'Number of floors'",
              "concept: floors_above_ground (close)\nmissing/top-codes: 994 = 10-14, 995 = 15+\naggregation: count"),
             ("ZMONUSE  'Imputation flag: Months in use'",
              "is_imputation_flag: true\nflags_variable: MONUSE\nconcept: imputation_flag (exact)")]
    y = 0.945
    for head, body in vars_:
        ax.add_patch(FancyBboxPatch((0.51, y - 0.16), 0.48, 0.16, boxstyle="round,pad=0,rounding_size=0.01",
                                    fc="white", ec=LINE))
        ax.text(0.52, y - 0.012, head, family="DejaVu Sans Mono", fontsize=6.1, weight="bold", va="top")
        ax.text(0.52, y - 0.05, body, **mono, linespacing=1.3)
        y -= 0.1775
    ax.text(0.01, 0.39, "c  Concept card seen by an AI system (one per concept, ~60 tokens)", fontsize=8.2,
            weight="bold", va="top")
    ax.add_patch(FancyBboxPatch((0.01, 0.135), 0.98, 0.22, boxstyle="round,pad=0,rounding_size=0.01", fc="#eef6ee", ec=GREEN))
    idx = concept_index()
    from .ai_docs import concept_card, concept_card_text
    import textwrap
    txt = "\n".join(textwrap.fill(concept_card_text(concept_card(idx[c], idx)), 128)
                    for c in ("total_energy_consumption", "floors_above_ground", "imputation_flag"))
    ax.text(0.022, 0.335, txt, **mono, linespacing=1.32)
    ax.set_ylim(0.125, 1)
    fig.set_size_inches(7.2, 3.9 * 0.875)
    save_fig(fig, path)
    plt.close(fig)


# ------------------------------------------------------------------------------------------ vocabulary
def fig_vocabulary(path):
    concepts = load_concepts()
    groups = [c for c in concepts if not c.get("broader")]
    leaves = leaf_concepts()
    fig, ax = canvas(7.2, 4.2)
    ncol = 4
    w, gap = 0.235, 0.012
    per = {g["id"]: [c for c in leaves if c.get("broader") == g["id"]] for g in groups}
    order = sorted(groups, key=lambda g: -len(per[g["id"]]))
    cols = [[] for _ in range(ncol)]
    heights = [0.0] * ncol
    for g in order:
        k = heights.index(min(heights))
        cols[k].append(g)
        heights[k] += 0.06 + 0.026 * len(per[g["id"]])
    for k, col in enumerate(cols):
        y = 0.985
        x = 0.01 + k * (w + gap)
        for g in col:
            items = per[g["id"]]
            h = 0.05 + 0.026 * len(items)
            ax.add_patch(FancyBboxPatch((x, y - h), w, h, boxstyle="round,pad=0,rounding_size=0.008", fc=SOURCE, ec=BLUE))
            ax.text(x + 0.008, y - 0.012, f"{g['pref_label']} ({len(items)})", fontsize=7.2, weight="bold",
                    color=BLUE, va="top")
            for i, c in enumerate(items):
                n = sum(len(c.get(m) or []) for m in ("exact_match", "close_match", "broad_match", "narrow_match",
                                                      "related_match"))
                ax.text(x + 0.012, y - 0.045 - 0.026 * i, c["pref_label"], fontsize=5.9, color=INK2, va="top")
                if n:
                    ax.text(x + w - 0.008, y - 0.045 - 0.026 * i, "•" * min(n, 5), fontsize=5.9, color=GREEN,
                            va="top", ha="right")
            y -= h + 0.012
    save_fig(fig, path)
    plt.close(fig)


def main() -> int:
    fig_architecture(FIG / "fig_architecture.png")
    fig_class_diagram(FIG / "fig_class_diagram.png")
    fig_worked_example(FIG / "fig_worked_example.png")
    print("wrote schema figures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
