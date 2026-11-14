"""Tables and figures for the schema-design experiments E1-E6 (paper Section 6).

    python -m meta_urban.design_report

Writes paper/tables/bench_design_conditions.csv, bench_design_tests.csv, bench_t3_conventions.csv and
paper/figures/fig_design_conditions.png, fig_standards.png. Every number is computed from the cached model
outputs at temperature 0 (repeat 0) against the adjudicated gold.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from .analytics import GRID, INK2, MUTED, SURFACE, _style, save_fig  # noqa: E402
from .bench import t3_items, t3_score  # noqa: E402
from .bench_report import FIG, MODEL_COLOR, TAB, boot_ci, item_table, mcnemar_exact, models, short, t2_frame  # noqa: E402
from .io import leaf_concepts  # noqa: E402

CONDITIONS = [  # (level, label, experiment)
    ("L0", "ids only", "E1"), ("L1", "ids + labels", "E1"), ("L2D", "+ definitions", "E1"),
    ("L2", "full concept cards", "E1"), ("L2U", "cards, open output", "E2"), ("L3", "retrieved cards", "E5"),
    ("XBR", "Brick documentation", "E6"), ("XBE", "BEDES documentation", "E6"),
    ("XEA", "Energy ADE documentation", "E6")]
NAME = {"qwen3:8b": "Qwen3 8B", "llama3.1:8b": "Llama 3.1 8B"}


def _frames():
    return {m: f for m in models() if not (f := t2_frame(m)).empty}


def conditions_table(frames) -> tuple[pd.DataFrame, pd.DataFrame]:
    ids = {c["id"] for c in leaf_concepts()} | {"none"}
    rows, tests = [], []
    for model, df in frames.items():
        tabs = {}
        for lv, lab, exp in CONDITIONS:
            if lv not in set(df.level):
                continue
            it = item_table(df, lv)
            tabs[lv] = it
            m = it[it.gold != "none"]
            h = (m.pred0 == m.gold).values
            lo, hi = boot_ci(h)
            g = df[(df.level == lv) & (df.repeat == 0)]
            rows.append({"model": short(model), "level": lv, "condition": lab, "experiment": exp, "n": len(m),
                         "acc@1": h.mean(), "lo": lo, "hi": hi,
                         "lenient": float(np.mean([p in ok for p, ok in zip(m.pred0, m.gold_ok)])),
                         "out_of_vocabulary_pct": 100 * float(np.mean([p not in ids for p in it.pred0])),
                         "input_tokens": float(g.input_tokens.mean())})
        base = {"L2": tabs.get("L2"), "L0": tabs.get("L0")}
        for lv in tabs:
            for ref in ("L0", "L2"):
                if lv == ref or base[ref] is None:
                    continue
                a, b = base[ref], tabs[lv].loc[base[ref].index]
                mask = (a.gold != "none").values
                ha, hb = (a.pred0 == a.gold).values[mask], (b.pred0 == b.gold).values[mask]
                n01, n10, p = mcnemar_exact(ha, hb)
                tests.append({"model": short(model), "condition": lv, "versus": ref, "delta": hb.mean() - ha.mean(),
                              "gained": n01, "lost": n10, "p_exact": p})
    return pd.DataFrame(rows), pd.DataFrame(tests)


def transplant_subset_table(frames) -> pd.DataFrame:
    """E6 restricted to variables whose gold concept the other standard actually documents."""
    from .standards import transplant_docs

    rows = []
    for model, df in frames.items():
        if not {"L2", "L0"} <= set(df.level):
            continue
        l2, l0 = item_table(df, "L2"), item_table(df, "L0")
        l0 = l0.loc[l2.index]
        for lv, std in (("XBR", "brick"), ("XBE", "bedes"), ("XEA", "energy_ade")):
            if lv not in set(df.level):
                continue
            docs = transplant_docs(std)
            x = item_table(df, lv).loc[l2.index]
            mask = ((l2.gold != "none") & l2.gold.isin(docs.keys())).values
            hx, h2, h0 = ((t.pred0 == t.gold).values[mask] for t in (x, l2, l0))
            _, _, p = mcnemar_exact(h2, hx)
            rows.append({"model": short(model), "standard": std, "concepts_documented": len(docs),
                         "with_definition": sum(". " in v for v in docs.values()), "n_variables": int(mask.sum()),
                         "acc_standard_docs": hx.mean(), "acc_meta_urban_cards": h2.mean(), "acc_ids_only": h0.mean(),
                         "p_standard_vs_meta_urban": p})
    return pd.DataFrame(rows)


def conventions_table() -> pd.DataFrame:
    """Normalization at temperature 0 with (T3P) and without (T3) the dataset card."""
    items = {(i["dataset"], i["name"]): i for i in t3_items()}
    rows = []
    for model in models():
        for task, lab in (("T3", "codebook entry only"), ("T3P", "with dataset card")):
            s3 = t3_score(model, task)
            if s3.empty:
                continue
            s3 = s3[s3.repeat == 0]
            it = [items[(d, n)] for d, n in zip(s3.dataset, s3.name)]
            g = lambda f: np.array([bool(i.get(f)) for i in it])  # noqa: E731
            flag = g("is_imputation_flag")
            unit = np.array([i.get("unit") is not None for i in it])
            scaled = np.array([(i.get("unit_multiplier") or 1) != 1 for i in it])
            r = {"model": short(model), "context": lab, "calls": len(s3), "valid": s3.valid.mean()}
            for f, nm in (("is_weight", "weight"), ("is_replicate_weight", "replicate weight"),
                          ("is_imputation_flag", "imputation flag")):
                pos = g(f)
                r[f"{nm} recall"] = s3.loc[pos, f"ok_{f}"].mean()
                r[f"{nm} false alarm"] = 1 - s3.loc[~pos, f"ok_{f}"].mean()
            for ds in ("cbecs2018", "recs2020"):
                m = flag & (s3.dataset == ds).values
                r[f"flagged variable {ds}"] = s3.loc[m, "ok_flags_variable"].mean()
            r["unit"] = s3.loc[unit, "ok_unit"].mean()
            r["multiplier (scaled units)"] = s3.loc[scaled, "ok_unit_multiplier"].mean()
            r["missing codes exact"] = s3.ok_missing_codes.mean()
            r["missing codes lenient"] = s3.ok_missing_codes_lenient.mean()
            for ds in ("cbecs2018", "recs2020"):
                m = (s3.dataset == ds).values
                r[f"missing codes exact {ds}"] = s3.loc[m, "ok_missing_codes"].mean()
            r["code list Jaccard"] = s3.codes_jaccard.mean()
            rows.append(r)
    return pd.DataFrame(rows)


def fig_conditions(tab: pd.DataFrame, path) -> None:
    order = [c for c in CONDITIONS if c[0] in set(tab.level) and not c[0].startswith("X")]
    fig, ax = plt.subplots(figsize=(7.2, 3.3), dpi=200)
    ms = [m for m in ("qwen3:8b", "llama3.1:8b") if m in set(tab.model)]
    w = 0.38
    x = np.arange(len(order))
    for k, m in enumerate(ms):
        d = tab[tab.model == m].set_index("level").reindex([c[0] for c in order])
        xs = x + (k - 0.5) * w
        ax.bar(xs, d["acc@1"], width=w * 0.92, color=MODEL_COLOR[f"ollama:{m}"], label=NAME[m], edgecolor=SURFACE)
        ax.errorbar(xs, d["acc@1"], yerr=[d["acc@1"] - d["lo"], d["hi"] - d["acc@1"]], fmt="none", ecolor=INK2,
                    elinewidth=0.8, capsize=2)
        for xi, v, h in zip(xs, d["acc@1"], d["hi"]):
            ax.text(xi, h + 0.012, f"{v:.2f}", ha="center", fontsize=6.2, color=INK2)
    seps = [i - 0.5 for i in range(1, len(order)) if order[i][2] != order[i - 1][2]]
    for s_ in seps:
        ax.axvline(s_, color=GRID, lw=1)
    for exp in dict.fromkeys(c[2] for c in order):
        xs_ = [i for i, c in enumerate(order) if c[2] == exp]
        ax.text(np.mean(xs_), 0.94, exp, ha="center", fontsize=7.5, color=MUTED, weight="bold")
    ax.set_xticks(x, [c[1].replace(" + ", "\n+ ").replace("cards, ", "cards,\n") for c in order], fontsize=7)
    ax.set_ylim(0, 1)
    ax.set_ylabel("Top-1 accuracy", fontsize=8, color=INK2)
    ax.yaxis.grid(True, color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    _style(ax)
    ax.legend(fontsize=7, frameon=False, loc="upper left", bbox_to_anchor=(0.0, 0.92))
    fig.tight_layout()
    save_fig(fig, path)
    plt.close(fig)


SRC_COLOR = {"ids": "#c9c7bf", "std": "#3a9a8f", "mu": "#1f3f73"}
MODEL_MARK = {"qwen3:8b": ("o", INK2, "Qwen3 8B"), "llama3.1:8b": ("^", SURFACE, "Llama 3.1 8B")}


def _bars_with_models(ax, x, vals_by_model, colors):
    """Bar = mean of the two models; one marker per model on top of it."""
    ms = list(vals_by_model)
    mean = np.mean([vals_by_model[m] for m in ms], axis=0)
    ax.bar(x, mean, width=0.72, color=colors, edgecolor=SURFACE, linewidth=1.5)
    for k, m in enumerate(ms):
        mk, fc, _ = MODEL_MARK[m]
        ax.scatter(x + (k - 0.5) * 0.22, vals_by_model[m], marker=mk, s=16, facecolor=fc, edgecolor=INK2,
                   linewidth=0.7, zorder=3)
    for xi, v, c in zip(x, mean, colors):
        ax.text(xi, 0.025, f"{v:.2f}", ha="center", fontsize=6.2, weight="bold",
                color=INK2 if c == SRC_COLOR["ids"] else SURFACE)


def fig_standards(tab: pd.DataFrame, sub: pd.DataFrame, path) -> None:
    from .standards import transplant_docs

    n = len(leaf_concepts())
    ms = [m for m in ("qwen3:8b", "llama3.1:8b") if m in set(tab.model)]
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.4, 3.2), dpi=200, gridspec_kw={"width_ratios": [5, 6.4]})
    # (a) all mappable variables
    order = [("L0", "ids only", "ids"), ("XEA", "Energy\nADE", "std"), ("XBR", "Brick", "std"),
             ("XBE", "BEDES", "std"), ("L2", "Meta-\nUrban", "mu")]
    std_of = {"XEA": "energy_ade", "XBR": "brick", "XBE": "bedes"}
    vals = {m: tab[tab.model == m].set_index("level").reindex([o[0] for o in order])["acc@1"].values for m in ms}
    x = np.arange(len(order))
    _bars_with_models(a, x, vals, [SRC_COLOR[o[2]] for o in order])
    labs = []
    for lv, lab, _ in order:
        cov = "" if lv == "L0" else f"\n({100 * (len(transplant_docs(std_of[lv])) if lv in std_of else n) / n:.0f}%)"
        labs.append(lab + cov)
    a.set_xticks(x, labs, fontsize=6.5)
    a.set_title("(a) All 295 mappable variables", fontsize=8, color=INK2, loc="left")
    # (b) only variables whose gold concept the standard documents
    stds = [("brick", "Brick"), ("bedes", "BEDES"), ("energy_ade", "Energy ADE")]
    cols = [("acc_ids_only", "ids"), ("acc_standard_docs", "std"), ("acc_meta_urban_cards", "mu")]
    xs, colors, labels, centers = [], [], [], []
    vals_b = {m: [] for m in ms}
    pos = 0.0
    for std, lab in stds:
        r = {m: sub[(sub.model == m) & (sub.standard == std)].iloc[0] for m in ms}
        grp = []
        for c, key in cols:
            xs.append(pos)
            grp.append(pos)
            colors.append(SRC_COLOR[key])
            for m in ms:
                vals_b[m].append(r[m][c])
            pos += 0.8
        r0 = r[ms[0]]
        centers.append(np.mean(grp))
        labels.append(f"{lab}\n{int(r0.n_variables)} variables\n{int(r0.with_definition)} of "
                      f"{int(r0.concepts_documented)} matched\nterms defined")
        pos += 0.7
    _bars_with_models(b, np.array(xs), {m: np.array(v) for m, v in vals_b.items()}, colors)
    b.set_xticks(centers, labels, fontsize=6.5)
    b.set_title("(b) Variables whose concept the standard documents", fontsize=8, color=INK2, loc="left")
    for ax in (a, b):
        ax.set_ylim(0, 0.8)
        ax.yaxis.grid(True, color=GRID, lw=0.6)
        ax.set_axisbelow(True)
        ax.tick_params(axis="x", length=0)
        _style(ax)
    a.set_ylabel("Top-1 accuracy", fontsize=8, color=INK2)
    b.set_yticklabels([])
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch

    handles = [Patch(color=SRC_COLOR["ids"], label="ids only"),
               Patch(color=SRC_COLOR["std"], label="documentation of the other standard"),
               Patch(color=SRC_COLOR["mu"], label="Meta-Urban concept cards")]
    handles += [Line2D([], [], marker=MODEL_MARK[m][0], ls="", markerfacecolor=MODEL_MARK[m][1],
                       markeredgecolor=INK2, markersize=4.5, label=MODEL_MARK[m][2]) for m in ms]
    fig.legend(handles=handles, loc="upper center", ncol=5, fontsize=6.5, frameon=False, bbox_to_anchor=(0.5, 1.0),
               handlelength=1.2, columnspacing=1.1)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    save_fig(fig, path)
    plt.close(fig)


def main() -> int:
    frames = _frames()
    tab, tests = conditions_table(frames)
    conv = conventions_table()
    tab.to_csv(TAB / "bench_design_conditions.csv", index=False)
    tests.to_csv(TAB / "bench_design_tests.csv", index=False)
    conv.to_csv(TAB / "bench_t3_conventions.csv", index=False)
    sub = transplant_subset_table(frames)
    sub.to_csv(TAB / "bench_design_transplant_subset.csv", index=False)
    print(sub.round(3).to_string(index=False))
    fig_standards(tab, sub, FIG / "fig_standards.png")
    fig_conditions(tab, FIG / "fig_design_conditions.png")
    print(tab.round(3).to_string(index=False))
    print(tests.round(4).to_string(index=False))
    print(conv.round(3).T.to_string())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
