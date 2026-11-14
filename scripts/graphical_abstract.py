"""Graphical abstract for the submission (paper/figures/graphical_abstract.png, .pdf, .tif).

At least 1328 px wide and readable at 13 cm width. Numbers are read from the generated tables, never typed in.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
TAB, OUT = ROOT / "paper" / "tables", ROOT / "paper" / "figures" / "graphical_abstract.png"
INK, INK2, MUTED, GRID, SURF, PANEL = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#ffffff", "#f4f4f1"
COL = {"ids": "#c9c7bf", "std": "#3a9a8f", "mu": "#1f3f73"}

cond = pd.read_csv(TAB / "bench_design_conditions.csv")
conv = pd.read_csv(TAB / "bench_t3_conventions.csv")
mean = cond.groupby("level")["acc@1"].mean()
oov = cond.loc[cond.level == "L2U", "out_of_vocabulary_pct"].mean()
flag0 = conv.loc[conv.context == "codebook entry only", "flagged variable cbecs2018"].mean()
flag1 = conv.loc[conv.context == "with dataset card", "flagged variable cbecs2018"].mean()

fig = plt.figure(figsize=(13.28, 5.0), dpi=200)  # 2656 x 1000 px
fig.patch.set_facecolor(SURF)


def panel(x, title):
    ax = fig.add_axes([x, 0.06, 0.30, 0.86])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.add_patch(FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0,rounding_size=0.04", fc=PANEL, ec="none"))
    ax.text(0.05, 0.93, title, fontsize=17, weight="bold", color=INK, va="top")
    return ax


# 1. the schema: one source, two audiences
a = panel(0.015, "1  AI-ready schema")
a.add_patch(FancyBboxPatch((0.22, 0.60), 0.56, 0.14, boxstyle="round,pad=0.01,rounding_size=0.02", fc=COL["mu"],
                           ec="none"))
a.text(0.50, 0.67, "Meta-Urban\none LinkML source", ha="center", va="center", fontsize=12, color=SURF,
       weight="bold", linespacing=1.2)
for x, head, body in ((0.05, "for people", "documentation\nOWL ontology\nlinks to Brick,\nBEDES, Energy ADE"),
                      (0.53, "for AI", "concept cards\ndataset cards\nJSON Schema\nSHACL checks")):
    a.add_patch(FancyBboxPatch((x, 0.13), 0.42, 0.33, boxstyle="round,pad=0.01,rounding_size=0.02", fc=SURF,
                               ec=GRID, lw=1.2))
    a.text(x + 0.21, 0.42, head, ha="center", va="top", fontsize=12.5, weight="bold", color=INK)
    a.text(x + 0.21, 0.335, body, ha="center", va="top", fontsize=11, color=INK2, linespacing=1.3)
    a.annotate("", xy=(x + 0.21, 0.47), xytext=(0.50, 0.59),
               arrowprops={"arrowstyle": "-|>", "color": MUTED, "lw": 1.6, "mutation_scale": 14})
a.text(0.05, 0.80, "6 design principles, each tested", fontsize=12, color=INK2)
a.text(0.50, 0.05, "AI output checked against the same schema", ha="center", fontsize=10.5, color=INK2,
       style="italic")

# 2. what helps a model: definitions
b = panel(0.35, "2  Definitions are the core")
b.text(0.05, 0.82, "Mapping survey variables to concepts,\ntwo local 8B models (mean)", fontsize=11.5,
       color=INK2, va="top", linespacing=1.3)
ax = fig.add_axes([0.392, 0.17, 0.245, 0.47])
order = [("L0", "ids", "ids"), ("L1", "labels", "ids"), ("L2D", "+ defini-\ntions", "mu"),
         ("L2", "full\ncards", "mu"), ("STD", "other\nstandards", "std")]
vals = [mean[["XBR", "XBE", "XEA"]].mean() if lv == "STD" else mean[lv] for lv, _, _ in order]
ax.bar(range(len(order)), vals, width=0.72, color=[COL[o[2]] for o in order], edgecolor=SURF, linewidth=1.5)
for i, v in enumerate(vals):
    ax.text(i, v + 0.015, f"{v:.2f}", ha="center", fontsize=10.5, color=INK2)
ax.set_xticks(range(len(order)), [o[1] for o in order], fontsize=10, color=INK2)
ax.set_ylim(0, 0.7)
ax.set_yticks([0, 0.2, 0.4, 0.6], ["0", "0.2", "0.4", "0.6"], fontsize=10.5, color=INK2)
ax.set_ylabel("Top-1 accuracy", fontsize=11.5, color=INK2)
ax.yaxis.grid(True, color=GRID, lw=0.8)
ax.set_axisbelow(True)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color(MUTED)
ax.tick_params(length=0)
ax.set_facecolor(PANEL)

# 3. conventions and closed vocabulary
c = panel(0.685, "3  Conventions and checks")
c.text(0.05, 0.79, "Imputation flags linked to their variable", fontsize=12.5, color=INK2)
c.text(0.05, 0.64, f"{100 * flag0:.0f}% → {100 * flag1:.0f}%", fontsize=27, weight="bold", color=INK)
c.text(0.05, 0.56, "when the schema states the convention", fontsize=11.5, color=INK2)
c.text(0.05, 0.40, "Invented concept identifiers", fontsize=12.5, color=INK2)
c.text(0.05, 0.25, f"{oov:.1f}% → 0%", fontsize=27, weight="bold", color=INK)
c.text(0.05, 0.215, "with a closed vocabulary (JSON Schema),\nat no cost in accuracy", fontsize=11.5, color=INK2,
       va="top", linespacing=1.25)

for x0, x1 in [(0.318, 0.348), (0.653, 0.683)]:
    fig.add_artist(FancyArrowPatch((x0, 0.49), (x1, 0.49), transform=fig.transFigure, arrowstyle="-|>",
                                   mutation_scale=22, color=MUTED, lw=2))

fig.savefig(OUT, facecolor=SURF)
fig.savefig(OUT.with_suffix(".pdf"), facecolor=SURF)
fig.savefig(OUT.with_suffix(".tif"), facecolor=SURF, pil_kwargs={"compression": "tiff_lzw"})
print("wrote", OUT)
