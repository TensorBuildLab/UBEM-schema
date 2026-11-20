"""Generate the reference pages of the documentation from the schema, so they cannot drift from it.

    python scripts/make_docs.py            # docs/category-profiles.md, docs/vocabulary.md, docs/catalog.md
    gen-doc schema/ubem_link.yaml -d docs/reference     # LinkML's per-class, per-slot and per-enum pages
"""

from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
S = yaml.safe_load((ROOT / "schema" / "ubem_link.yaml").read_text(encoding="utf-8"))
DOCS = ROOT / "docs"
ROLE_OF = {"WeatherProfile": "boundary_conditions", "GeometryProfile": "geometry_inventory",
           "OperationProfile": "operation_use", "CharacteristicsProfile": "building_characteristics",
           "EnergyProfile": "calibration_validation", "SimulationProfile": "reference_simulation",
           "ContextProfile": "context_coupling"}


def one(text) -> str:
    return " ".join(str(text or "").split())


def slot_row(name: str, required: set) -> str:
    d = S["slots"].get(name) or {}
    rng = d.get("range", "string")
    vals = ""
    if rng in S["enums"]:
        vals = ", ".join(f"`{v}`" for v in S["enums"][rng]["permissible_values"])
    req = "required" if name in required else ""
    lst = "list" if d.get("multivalued") else ""
    return f"| `{name}` | {', '.join(x for x in (req, lst) if x) or ''} | {one(d.get('description'))} | {vals} |"


def category_profiles() -> str:
    out = ["# Category profiles", "",
           "Generated from `schema/ubem_link.yaml` by `scripts/make_docs.py`; do not edit by hand.", "",
           one(S["classes"]["CategoryProfile"]["description"]), "",
           "Every category profile also has `provides_concepts` (ids of UBEM-Link concepts the dataset provides) and "
           "`metadata_standards` (standards the publisher already uses).", ""]
    for cname, role in ROLE_OF.items():
        c = S["classes"][cname]
        req = {k for k, v in (c.get("slot_usage") or {}).items() if (v or {}).get("required")}
        slot_name = cname[0].lower() + cname[1:].replace("Profile", "_profile").replace("_profile", "") + "_profile"
        out += [f"## {cname}", "", f"Key in a dataset profile: `{slot_name}`; UBEM role: `{role}`.", "",
                one(c.get("description")), "", "| Field | | Meaning | Allowed values |", "|---|---|---|---|"]
        out += [slot_row(s, req) for s in c.get("slots", [])]
        out.append("")
    return "\n".join(out)


def vocabulary() -> str:
    v = yaml.safe_load((ROOT / "schema" / "vocab" / "ubem_concepts.yaml").read_text(encoding="utf-8"))
    cs = v["concepts"] if isinstance(v, dict) else v
    groups = {c["id"]: c for c in cs if c["id"] in {x.get("broader") for x in cs}}
    out = ["# Concept vocabulary", "", "Generated from `schema/vocab/ubem_concepts.yaml`; do not edit by hand.", ""]
    for gid, g in groups.items():
        out += [f"## {g['pref_label']} (`{gid}`)", "", one(g.get("definition")), "",
                "| Concept | Definition | Canonical unit | Links |", "|---|---|---|---|"]
        for c in cs:
            if c.get("broader") != gid:
                continue
            n = sum(len(c.get(k) or []) for k in ("exact_match", "close_match", "broad_match", "narrow_match", "related_match"))
            out.append(f"| `{c['id']}` {c['pref_label']} | {one(c['definition'])} | {c.get('canonical_unit') or ''} | {n or ''} |")
        out.append("")
    return "\n".join(out)


def catalog() -> str:
    entries = [yaml.safe_load(p.read_text(encoding="utf-8")) for p in sorted((ROOT / "catalog" / "datasets").glob("*.yaml"))]
    role = Counter(e["ubem_roles"][0] for e in entries)
    out = ["# Catalog of open UBEM datasets", "", "Generated from `catalog/datasets/`; do not edit by hand. Search it "
           "with `ubem-link catalog --role ... --key ... --granularity ...`.", "",
           "| Primary role | Datasets |", "|---|---|"] + [f"| `{k}` | {v} |" for k, v in role.most_common()] + [""]
    out += ["| Id | Dataset | Roles | Finest granularity | Join keys |", "|---|---|---|---|---|"]
    for e in entries:
        out.append(f"| `{e['id']}` | {e.get('short_name') or e['title']} | {', '.join(e['ubem_roles'])} | "
                   f"{e.get('spatial_granularity')} | {', '.join(e.get('join_keys') or [])} |")
    return "\n".join(out) + "\n"


DOCS.mkdir(exist_ok=True)
(DOCS / "category-profiles.md").write_text(category_profiles() + "\n", encoding="utf-8")
(DOCS / "vocabulary.md").write_text(vocabulary() + "\n", encoding="utf-8")
(DOCS / "catalog.md").write_text(catalog(), encoding="utf-8")
print("wrote docs/category-profiles.md, docs/vocabulary.md, docs/catalog.md")
