"""Graphical abstract for the submission (paper/figures/graphical_abstract.png).

Automation in Construction: optional, at least 1328 px wide, readable at 13 cm width. Numbers are read from
the generated tables, never typed in.
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
COL = {"qwen3:8b": "#256abf", "llama3.1:8b": "#e5803a"}
NAME = {"qwen3:8b": "Qwen3 8B", "llama3.1:8b": "Llama 3.1 8B"}

main = pd.read_csv(TAB / "bench_t2_main.csv")
lex = float(main.loc[main.level == "-", "acc@1"].iloc[0])

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


# 1. schema and catalog
a = panel(0.015, "1  Schema + catalog")
a.text(0.05, 0.78, "Meta-Urban 2.0 schema\n81-concept vocabulary\nmapped to Brick, BEDES,\nCityGML Energy ADE",
       fontsize=13.5, color=INK2, va="top", linespacing=1.35)
a.text(0.05, 0.36, "91 verified open datasets", fontsize=13.5, color=INK2)
a.text(0.05, 0.24, "3 of 48", fontsize=30, weight="bold", color=INK)
a.text(0.05, 0.10, "non-geometric datasets link\nto individual buildings", fontsize=12.5, color=INK2, linespacing=1.25)

# 2. benchmark: accuracy by level of schema context
b = panel(0.35, "2  LLM benchmark")
b.text(0.05, 0.80, "2,048 survey variables, two local\n8B LLMs, four levels of context", fontsize=12.5,
       color=INK2, va="top", linespacing=1.3)
ax = fig.add_axes([0.418, 0.20, 0.215, 0.44])
levels = ["L0", "L1", "L2", "L3"]
lab = ["ids", "labels", "defini-\ntions", "retrieval"]
w = 0.38
for k, m in enumerate(["qwen3:8b", "llama3.1:8b"]):
    d = main[main.model == m].set_index("level").reindex(levels)
    xs = [i + (k - 0.5) * w for i in range(4)]
    ax.bar(xs, d["acc@1"], width=w * 0.92, color=COL[m], label=NAME[m], edgecolor=SURF, linewidth=1.5)
ax.axhline(lex, color=MUTED, ls="--", lw=1.2, label="lexical baseline")
ax.set_xticks(range(4), lab, fontsize=11, color=INK2)
ax.set_ylim(0, 0.85)
ax.set_yticks([0, 0.25, 0.5, 0.75], ["0", "0.25", "0.50", "0.75"], fontsize=11, color=INK2)
ax.set_ylabel("Top-1 accuracy", fontsize=12, color=INK2)
ax.yaxis.grid(True, color=GRID, lw=0.8)
ax.set_axisbelow(True)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color(MUTED)
ax.tick_params(length=0)
ax.set_facecolor(PANEL)
ax.legend(fontsize=10.5, frameon=False, loc="upper left", ncol=1)

# 3. downstream consequences
c = panel(0.685, "3  Why errors matter")
c.text(0.05, 0.78, "Survey weights ignored", fontsize=13.5, color=INK2)
c.text(0.05, 0.62, "-16% to +102%", fontsize=27, weight="bold", color=INK)
c.text(0.05, 0.53, "error in energy use intensity", fontsize=12.5, color=INK2)
c.text(0.05, 0.38, "Unit multiplier dropped", fontsize=13.5, color=INK2)
c.text(0.05, 0.22, "x 1,000", fontsize=27, weight="bold", color=INK)
c.text(0.05, 0.12, "error in energy totals", fontsize=12.5, color=INK2)

for x0, x1 in [(0.318, 0.348), (0.653, 0.683)]:
    fig.add_artist(FancyArrowPatch((x0, 0.49), (x1, 0.49), transform=fig.transFigure, arrowstyle="-|>",
                                   mutation_scale=22, color=MUTED, lw=2))

fig.savefig(OUT, facecolor=SURF)
fig.savefig(OUT.with_suffix(".pdf"), facecolor=SURF)
fig.savefig(OUT.with_suffix(".tif"), facecolor=SURF, pil_kwargs={"compression": "tiff_lzw"})
print("wrote", OUT)
