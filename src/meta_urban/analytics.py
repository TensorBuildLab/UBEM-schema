"""RQ1 and RQ2: computed landscape indicators and competency questions over the catalog.

    python -m meta_urban.analytics      # writes paper/tables/*.csv, paper/tables/competency.md, paper/figures/*.png
"""

from __future__ import annotations

from collections import Counter

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from . import PAPER  # noqa: E402
from .io import load_catalog, schema_enums  # noqa: E402

ROLES = ["boundary_conditions", "geometry_inventory", "building_characteristics", "operation_use",
         "calibration_validation", "reference_simulation", "context_coupling"]
ROLE_LABEL = {"boundary_conditions": "Boundary conditions", "geometry_inventory": "Geometry & inventory",
              "building_characteristics": "Building characteristics", "operation_use": "Operation & use",
              "calibration_validation": "Calibration & validation", "reference_simulation": "Reference simulation",
              "context_coupling": "Context & coupling"}
TIERS = {
    "Building / station": {"point_station", "building", "parcel"},
    "Fine grid / small area": {"grid_cell_fine", "census_block_group", "census_tract", "postal_code"},
    "Coarse grid / county / city": {"grid_cell_coarse", "county", "city", "utility_service_territory"},
    "State / region / nation": {"state_province", "climate_zone", "census_region_division", "nation"},
    "None / unknown": {"none", "unknown"},
}
TIER_OF = {g: t for t, gs in TIERS.items() for g in gs}
ACCESS_ORDER = ["open_download", "open_api", "registration_required", "request_or_agreement", "restricted_commercial"]
FINE_KEYS = {"lat_lon", "geometry", "address", "parcel_id", "building_id", "ubid"}
OPEN = {"open_download", "open_api", "registration_required"}

# reference palette (dataviz skill, references/palette.md): sequential blue ramp, ink and grid tokens
BLUE = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
INK, INK2, MUTED, GRID, SURFACE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#ffffff"


def frame() -> pd.DataFrame:
    rows = []
    for e in load_catalog():
        roles = e.get("ubem_roles") or []
        cov = (e.get("spatial_coverage") or {}).get("countries") or []
        rows.append({
            "id": e["id"], "primary_role": roles[0] if roles else None, "roles": roles,
            "granularity": e.get("spatial_granularity"), "tier": TIER_OF.get(e.get("spatial_granularity"), "None / unknown"),
            "nature": e.get("statistical_nature"), "access": e.get("access_level"),
            "license_known": bool(e.get("license")) and "unknown" not in str(e.get("license")).lower(),
            "pid": bool(e.get("doi") or e.get("persistent_identifier")),
            "descriptor_paper": bool(e.get("reference_paper_doi")),
            "join_keys": e.get("join_keys") or [], "scope": e.get("geographic_scope"),
            "us_only": cov == ["US"], "global": "GLOBAL" in cov,
            "temporal_resolution": e.get("temporal_resolution"),
        })
    return pd.DataFrame(rows)


def indicators(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    out = {}
    out["role_by_tier"] = pd.crosstab(df.primary_role, df.tier).reindex(index=ROLES, columns=list(TIERS), fill_value=0)
    out["role_by_access"] = pd.crosstab(df.primary_role, df.access).reindex(index=ROLES, columns=ACCESS_ORDER, fill_value=0)
    out["role_by_nature"] = pd.crosstab(df.primary_role, df.nature).reindex(index=ROLES, fill_value=0)
    g = df.groupby("primary_role")
    out["role_summary"] = pd.DataFrame({
        "n": g.size(),
        "open_share": g.access.apply(lambda s: s.isin(OPEN).mean()),
        "license_stated_share": g.license_known.mean(),
        "pid_share": g.pid.mean(),
        "descriptor_paper_share": g.descriptor_paper.mean(),
        "fine_key_share": g.join_keys.apply(lambda s: np.mean([bool(FINE_KEYS & set(k)) for k in s])),
        "us_only_share": g.us_only.mean(),
        "global_share": g["global"].mean(),
    }).reindex(ROLES)
    keys = Counter(k for ks in df.join_keys for k in ks)
    out["join_key_counts"] = pd.DataFrame(keys.most_common(), columns=["join_key", "n_datasets"])
    df = df.assign(linkage=df.apply(linkage_class, axis=1))
    out["linkability"] = pd.crosstab(df.primary_role, df.linkage).reindex(index=ROLES, columns=LINKAGE, fill_value=0)
    out["linkage_by_dataset"] = df[["id", "primary_role", "granularity", "linkage"]]
    return out


LINKAGE = ["shared_identifier", "building_location", "area_code", "attribute_only", "none"]
SHARED_IDS = {"ubid", "parcel_id", "address"}
AREA_KEYS = {"census_block_group", "census_tract", "postal_code", "fips_county", "fips_state", "census_region_division",
             "nuts_region", "small_statistical_area", "utility_id", "balancing_authority", "grid_cell", "country_iso",
             "climate_zone_ashrae", "climate_zone_iecc"}


def linkage_class(row) -> str:
    """How a dataset's records can be linked to individual buildings (footprints) in another dataset.

    shared_identifier: an identifier that exists outside the dataset (UBID, cadastral parcel id, address);
    building_location: building-precise coordinates or geometry (spatial join), at building/parcel granularity;
    area_code: only area-level codes or grid cells (records can be allocated to areas, not to buildings);
    attribute_only: only attributes such as building type or vintage (statistical matching only);
    none: no usable key. A dataset-internal `building_id` is not a cross-dataset key and is ignored.
    """
    keys = set(row["join_keys"])
    if keys & SHARED_IDS:
        return "shared_identifier"
    if keys & {"lat_lon", "geometry"} and row["granularity"] in {"building", "parcel"}:
        return "building_location"
    if keys & AREA_KEYS or keys & {"lat_lon"}:
        return "area_code"
    if keys & {"building_type", "vintage"}:
        return "attribute_only"
    return "none"


def competency(df: pd.DataFrame) -> str:
    cat = {e["id"]: e for e in load_catalog()}
    lines = ["# Competency questions answered from the catalog", "",
             "Each question is executed by `meta_urban.analytics.competency()` over the YAML catalog.", ""]

    def q(title, ids, note=""):
        lines.append(f"**{title}**  ")
        lines.append((", ".join(sorted(ids)) if ids else "(none)") + (f"  \n_{note}_" if note else ""))
        lines.append("")

    hourly = {"PT1H", "PT30M", "PT15M", "PT10M", "PT5M", "PT1M"}
    q("CQ1. Which open weather datasets give hourly or finer data for the United States at station or <= 1 km resolution?",
      [i for i, e in cat.items() if "boundary_conditions" in (e.get("ubem_roles") or []) and e.get("access_level") in OPEN
       and e.get("temporal_resolution") in hourly and e.get("spatial_granularity") in {"point_station", "grid_cell_fine", "building"}
       and set((e.get("spatial_coverage") or {}).get("countries") or []) & {"US", "GLOBAL"}])
    q("CQ2. Which open geometry datasets give building-level polygons with height for the United States?",
      [i for i, e in cat.items() if "geometry_inventory" in (e.get("ubem_roles") or []) and e.get("access_level") in OPEN
       and e.get("spatial_granularity") == "building"
       and set((e.get("spatial_coverage") or {}).get("countries") or []) & {"US", "GLOBAL"}
       and "height" in " ".join(map(str, e.get("content_types") or [])).lower()])
    q("CQ3. Which datasets are weighted samples, and which weights must be used?",
      [f"{i} ({str(e.get('sampling_weights'))[:60]}...)" for i, e in cat.items() if e.get("statistical_nature") == "sample_survey_weighted"])
    q("CQ4. Which open datasets report measured energy at building or meter level?",
      [i for i, e in cat.items() if "calibration_validation" in (e.get("ubem_roles") or []) and e.get("access_level") in OPEN
       and e.get("statistical_nature") == "measured_monitoring" and e.get("spatial_granularity") in {"building", "point_station", "none", "unknown"}])
    q("CQ5. Which building-characteristics datasets can be joined to a geometry dataset at building level?",
      [i for i, e in cat.items() if "building_characteristics" in (e.get("ubem_roles") or []) and FINE_KEYS & set(e.get("join_keys") or [])],
      "Building-level keys: " + ", ".join(sorted(FINE_KEYS)))
    q("CQ6. Which datasets lack an explicit license?",
      [i for i, e in cat.items() if not e.get("license")])
    return "\n".join(lines)


def save_fig(fig, path) -> None:
    """Save a figure as a 600-dpi PNG and a vector PDF (journal artwork requirements)."""
    from pathlib import Path as _P

    fig.savefig(path, facecolor=SURFACE, dpi=600)
    fig.savefig(_P(path).with_suffix(".pdf"), facecolor=SURFACE)


def _style(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(MUTED)
    ax.tick_params(colors=INK2, labelsize=8)


def fig_heatmap(m: pd.DataFrame, path):
    fig, ax = plt.subplots(figsize=(7.0, 3.6), dpi=200)
    vals = m.values
    vmax = max(1, vals.max())
    cmap = matplotlib.colors.ListedColormap(["#f4f4f1"] + BLUE[1:])
    bounds = [-0.5, 0.5] + list(np.linspace(1.5, vmax + 0.5, len(BLUE) - 1))
    norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)
    ax.imshow(vals, cmap=cmap, norm=norm, aspect="auto")
    for i in range(vals.shape[0]):
        for j in range(vals.shape[1]):
            v = vals[i, j]
            ax.text(j, i, str(v), ha="center", va="center", fontsize=8,
                    color="#ffffff" if v >= vmax * 0.55 else INK)
    ax.set_xticks(range(vals.shape[1]), [c.replace(" / ", " /\n") for c in m.columns], fontsize=7.5)
    ax.set_yticks(range(vals.shape[0]), [ROLE_LABEL[r] for r in m.index], fontsize=8)
    ax.set_xticks(np.arange(-.5, vals.shape[1]), minor=True)
    ax.set_yticks(np.arange(-.5, vals.shape[0]), minor=True)
    ax.grid(which="minor", color=SURFACE, linewidth=2)
    ax.tick_params(which="both", length=0, colors=INK2)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xlabel("Finest spatial granularity released publicly", fontsize=8, color=INK2)
    fig.tight_layout()
    save_fig(fig, path)
    plt.close(fig)


def fig_access(m: pd.DataFrame, path):
    fig, ax = plt.subplots(figsize=(7.0, 3.2), dpi=200)
    shades = ["#184f95", "#3987e5", "#86b6ef", "#b9b8b0", "#6e6d68"]  # open (blue) -> closed (gray)
    left = np.zeros(len(m))
    for col, c in zip(m.columns, shades):
        v = m[col].values
        ax.barh(range(len(m)), v, left=left, color=c, edgecolor=SURFACE, linewidth=1.5, height=0.62,
                label=col.replace("_", " "))
        left += v
    ax.set_yticks(range(len(m)), [ROLE_LABEL[r] for r in m.index], fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("Number of datasets in catalog", fontsize=8, color=INK2)
    ax.xaxis.grid(True, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    _style(ax)
    ax.legend(ncol=5, fontsize=6.5, frameon=False, loc="lower center", bbox_to_anchor=(0.4, 1.0))
    fig.tight_layout()
    save_fig(fig, path)
    plt.close(fig)


def fig_weights(path):
    d2 = pd.read_csv(PAPER / "tables" / "downstream_d2_weights_by_pba.csv")
    d2 = d2[d2.share_of_buildings_weighted_pct >= 0.5].sort_values("err_unweighted_agg_pct")
    fig, ax = plt.subplots(figsize=(7.0, 3.8), dpi=200)
    y = np.arange(len(d2))
    ax.barh(y, d2.err_unweighted_agg_pct, color=np.where(d2.err_unweighted_agg_pct >= 0, "#3987e5", "#e34948"),
            height=0.62, edgecolor=SURFACE)
    ax.axvline(0, color=MUTED, linewidth=0.8)
    ax.set_yticks(y, d2.pba, fontsize=7.5)
    lo, hi = d2.err_unweighted_agg_pct.min(), d2.err_unweighted_agg_pct.max()
    ax.set_xlim(min(lo, 0) - 12, hi + 14)
    for yi, v in zip(y, d2.err_unweighted_agg_pct):
        ax.text(v + (1.5 if v >= 0 else -1.5), yi, f"{v:+.0f}%", va="center", ha="left" if v >= 0 else "right",
                fontsize=6.5, color=INK2)
    ax.set_xlabel("Error in floor-area-weighted EUI when survey weights are ignored (%)", fontsize=8, color=INK2)
    ax.xaxis.grid(True, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    _style(ax)
    fig.tight_layout()
    save_fig(fig, path)
    plt.close(fig)


def main() -> None:
    df = frame()
    tdir, fdir = PAPER / "tables", PAPER / "figures"
    tdir.mkdir(parents=True, exist_ok=True)
    fdir.mkdir(parents=True, exist_ok=True)
    ind = indicators(df)
    for k, v in ind.items():
        v.to_csv(tdir / f"catalog_{k}.csv")
    (tdir / "competency.md").write_text(competency(df), encoding="utf-8")
    fig_heatmap(ind["role_by_tier"], fdir / "fig_role_by_granularity.png")
    fig_access(ind["role_by_access"], fdir / "fig_role_by_access.png")
    if (tdir / "downstream_d2_weights_by_pba.csv").exists():
        fig_weights(fdir / "fig_weights_eui_error.png")
    pd.set_option("display.width", 200)
    print(f"{len(df)} datasets")
    for k in ["role_by_tier", "role_by_access", "role_summary", "linkability"]:
        print(f"\n== {k}\n", ind[k].round(2).to_string())
    print("\n== join keys\n", ind["join_key_counts"].head(12).to_string(index=False))


if __name__ == "__main__":
    main()
