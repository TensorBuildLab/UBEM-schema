"""ubem-link: make open building and urban energy data AI-ready with the UBEM-Link schema.

    ubem-link describe DATA [--codebook FILE ...] [--entry ENTRY] [--model MODEL] [--out DIR]
        Profile every column of a dataset: concept or join key, unit, multiplier, missing codes, code list,
        weights and flags. Writes <id>.ubem.yaml (UBEM-Link DatasetProfile), <id>.review.csv (columns to check,
        worst first), <id>.card.md (dataset card for any AI assistant) and <id>.log.jsonl (model answers).
    ubem-link conventions DOCS.txt [--model MODEL] -o conventions.yaml
        Propose dataset conventions (missing codes, units, flags, keys) from a user guide, with machine-readable
        scopes, for a person to confirm and add to the entry.
    ubem-link validate PROFILE.yaml
        Validate a profile against the UBEM-Link JSON Schema and rules; list the open review flags.
    ubem-link apply PROFILE.yaml DATA -o OUT.csv [--decode]
        Normalize the data with the profile: missing codes removed, units converted to SI, no model involved.
    ubem-link integrate RECIPE.yaml -o OUT.csv
        Join profiled datasets (keys, nearest weather station) into one table and report linkage.
    ubem-link select DATA --target CONCEPT|join:KEY --purpose TEXT [--codebook FILE]
        Ask the model which column holds a concept that a pipeline needs.
    ubem-link catalog [--role ROLE] [--key KEY] [--granularity G] [--text WORDS]
        Search the UBEM-Link catalog of open datasets.
    ubem-link cards [--out DIR]
        Export the AI documentation layer (schema card, concept cards, dataset cards) for use in any assistant.
    ubem-link pending DIR
        With --model files:DIR, list the requests waiting for an assistant's answers and write DIR/prompts.md.

Models: ollama:<name> (default ollama:qwen3:8b, local), openai:<name> (any OpenAI-compatible server; set
OPENAI_BASE_URL for LM Studio, vLLM or llama.cpp, OPENAI_API_KEY for hosted APIs), anthropic:<name>
(ANTHROPIC_API_KEY), or files:<dir> (no API: an assistant such as Claude Code answers the requests in files).
Keys are read from the environment or a .env file, never from the command line.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

from . import CATALOG_DIR
from .io import load_catalog


def _entry(arg: str | None, data_path: Path) -> dict:
    if not arg:
        return {"id": data_path.stem.lower().replace(" ", "-"), "title": data_path.stem}
    p = Path(arg)
    if p.exists():
        return yaml.safe_load(p.read_text(encoding="utf-8"))
    hit = next((e for e in load_catalog() if e["id"] == arg), None)
    if hit is None:
        raise SystemExit(f"no file and no catalog entry named {arg!r}")
    return hit


def _codebook(paths: list[str] | None):
    from .readers import merge_codebooks, read_codebook

    return merge_codebooks(*[read_codebook(p) for p in paths]) if paths else {}


def _dump(obj, path: Path) -> None:
    path.write_text(yaml.safe_dump(obj, sort_keys=False, allow_unicode=True, width=110), encoding="utf-8")


def cmd_describe(a) -> int:
    from .ai_docs import dataset_card
    from .profiler import Profiler, Settings, review_table
    from .readers import describe_columns, read_table

    data = Path(a.data)
    df = read_table(data, nrows=a.rows)
    cols = describe_columns(df, _codebook(a.codebook))
    entry = _entry(a.entry, data)
    if a.dataset_id:
        entry["id"] = a.dataset_id
    s = Settings(model=a.model, retrieval=a.retrieval, k=a.k, conventions=a.conventions,
                 apply_conventions=not a.no_apply_conventions, cache_dir=a.cache)
    prof = Profiler(s, entry, entry["id"])
    variables = prof.profile(cols, only=a.only)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    if prof.pending:
        print(f"{prof.pending} requests wait for answers in {a.model.split(':', 1)[1]}/requests.jsonl.\n"
              f"Answer them (see `ubem-link pending {a.model.split(':', 1)[1]}`), then run this command again.")
        return 3
    profile = {k: v for k, v in entry.items() if k != "variables" and not k.startswith("_")}
    profile["variables"] = variables
    _dump(profile, out / f"{entry['id']}.ubem.yaml")
    review_table(variables).to_csv(out / f"{entry['id']}.review.csv", index=False)
    (out / f"{entry['id']}.card.md").write_text(dataset_card(profile) + "\n", encoding="utf-8")
    with open(out / f"{entry['id']}.log.jsonl", "w", encoding="utf-8") as fh:
        for r in prof.log:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    flagged = sum(1 for v in variables if v.get("review_flags"))
    print(f"profiled {len(variables)} columns with {a.model}; {flagged} flagged for review "
          f"-> {out / (entry['id'] + '.ubem.yaml')}, {entry['id']}.review.csv")
    return 0


def cmd_conventions(a) -> int:
    from .conventions import extract_conventions

    text = Path(a.docs).read_text(encoding="utf-8", errors="replace")
    convs = extract_conventions(text, a.model, cache_dir=a.cache)
    _dump({"conventions": convs}, Path(a.output))
    print(f"{len(convs)} proposed conventions -> {a.output} (confirm each against the documentation before use)")
    return 0


def cmd_validate(a) -> int:
    from .validate import validate_profile

    doc = yaml.safe_load(Path(a.profile).read_text(encoding="utf-8"))
    errors = validate_profile(doc)
    for e in errors:
        print("ERROR", e)
    flags = [(v["name"], f) for v in doc.get("variables") or [] for f in v.get("review_flags") or []]
    for name, f in flags:
        print("REVIEW", name, "-", f)
    print(f"{len(errors)} schema errors; {len(flags)} open review flags in {len(doc.get('variables') or [])} variables")
    return 1 if errors else 0


def cmd_apply(a) -> int:
    from .apply import apply_profile
    from .readers import read_table

    doc = yaml.safe_load(Path(a.profile).read_text(encoding="utf-8"))
    out, report = apply_profile(read_table(a.data), doc.get("variables") or [], decode=a.decode)
    out.to_csv(a.output, index=False)
    report.to_csv(Path(a.output).with_suffix(".columns.csv"), index=False)
    print(f"wrote {a.output} ({len(out):,} rows) and the column report {Path(a.output).with_suffix('.columns.csv').name}")
    return 0


def cmd_integrate(a) -> int:
    from .integrate import run_recipe

    recipe = yaml.safe_load(Path(a.recipe).read_text(encoding="utf-8"))
    table, report = run_recipe(recipe, Path(a.recipe).parent)
    table.to_csv(a.output, index=False)
    report.to_csv(Path(a.output).with_suffix(".links.csv"), index=False)
    print(report.to_string(index=False))
    return 0


def cmd_select(a) -> int:
    from .llm import complete, parse_json
    from .profiler import select_request
    from .readers import describe_columns, read_table

    cols = describe_columns(read_table(a.data, nrows=a.rows), _codebook(a.codebook))
    r = complete(a.model, select_request(cols, a.target, a.purpose), {"task": "tool-select", "name": a.target}, 0,
                 cache_dir=a.cache)
    print(json.dumps(parse_json(r["response"]) or {}, indent=1))
    return 0


def cmd_catalog(a) -> int:
    hits = []
    for e in load_catalog():
        if a.role and a.role not in (e.get("ubem_roles") or []):
            continue
        if a.key and a.key not in (e.get("join_keys") or []):
            continue
        if a.granularity and e.get("spatial_granularity") != a.granularity:
            continue
        if a.text and not all(w.lower() in json.dumps(e).lower() for w in a.text):
            continue
        hits.append(e)
    for e in hits:
        print(f"{e['id']:<34} {e.get('spatial_granularity', ''):<16} {', '.join(e.get('join_keys') or [])[:40]:<42} "
              f"{e.get('short_name') or e.get('title')}")
    print(f"{len(hits)} datasets")
    return 0


def cmd_cards(a) -> int:
    from . import ai_docs

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "schema_card.md").write_text(ai_docs.schema_card(), encoding="utf-8")
    cards = [ai_docs.concept_card_text(ai_docs.concept_card(c)) for c in ai_docs.leaf_concepts()]
    (out / "concept_cards.md").write_text("\n".join(cards) + "\n", encoding="utf-8")
    print(f"wrote {out}/schema_card.md and concept_cards.md ({len(cards)} concepts)")
    return 0


def cmd_pending(a) -> int:
    d = Path(a.dir)
    reqs = [json.loads(x) for x in (d / "requests.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()] \
        if (d / "requests.jsonl").exists() else []
    done = set()
    if (d / "responses.jsonl").exists():
        done = {json.loads(x)["key"] for x in (d / "responses.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()}
    todo = [r for r in reqs if r["key"] not in done]
    lines = ["# Requests waiting for answers", "",
             "Answer each request by appending one line to responses.jsonl:",
             '`{"key": "<key>", "response": <a JSON object that follows the schema>}`', ""]
    for r in todo:
        lines += [f"## {r['key']} ({r.get('task')}: {r.get('name')})", "", "### Instructions", "", r["system"], "",
                  "### Input", "", r["user"], "", "### Answer schema", "", "```json", json.dumps(r["schema"]), "```", ""]
    (d / "prompts.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(todo)} of {len(reqs)} requests wait for answers; instructions in {d / 'prompts.md'}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="ubem-link", description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def model_args(p):
        p.add_argument("--model", default="ollama:qwen3:8b")
        p.add_argument("--cache", default=".ubem_link_cache", help="directory of cached model answers")

    p = sub.add_parser("describe")
    p.add_argument("data")
    p.add_argument("--codebook", nargs="+")
    p.add_argument("--entry", help="dataset profile YAML or catalog id with the dataset-level facts and conventions")
    p.add_argument("--dataset-id")
    p.add_argument("--retrieval", choices=["dense", "lexical", "all"], default="dense")
    p.add_argument("--k", type=int, default=10)
    p.add_argument("--conventions", choices=["scoped", "card", "none"], default="scoped")
    p.add_argument("--no-apply-conventions", action="store_true")
    p.add_argument("--only", nargs="+", help="profile only these columns")
    p.add_argument("--rows", type=int, help="read only the first N rows for the value summaries")
    p.add_argument("--out", default="ubem_link_out")
    model_args(p)
    p.set_defaults(fn=cmd_describe)

    p = sub.add_parser("conventions")
    p.add_argument("docs")
    p.add_argument("-o", "--output", default="conventions.yaml")
    model_args(p)
    p.set_defaults(fn=cmd_conventions)

    p = sub.add_parser("validate")
    p.add_argument("profile")
    p.set_defaults(fn=cmd_validate)

    p = sub.add_parser("apply")
    p.add_argument("profile")
    p.add_argument("data")
    p.add_argument("-o", "--output", required=True)
    p.add_argument("--decode", action="store_true", help="replace codes by their labels")
    p.set_defaults(fn=cmd_apply)

    p = sub.add_parser("integrate")
    p.add_argument("recipe")
    p.add_argument("-o", "--output", required=True)
    p.set_defaults(fn=cmd_integrate)

    p = sub.add_parser("select")
    p.add_argument("data")
    p.add_argument("--target", required=True, help="concept id or join:<key type>")
    p.add_argument("--purpose", required=True)
    p.add_argument("--codebook", nargs="+")
    p.add_argument("--rows", type=int, default=5000)
    model_args(p)
    p.set_defaults(fn=cmd_select)

    p = sub.add_parser("catalog")
    p.add_argument("--role")
    p.add_argument("--key")
    p.add_argument("--granularity")
    p.add_argument("--text", nargs="+")
    p.set_defaults(fn=cmd_catalog)

    p = sub.add_parser("cards")
    p.add_argument("--out", default="ubem_link_cards")
    p.set_defaults(fn=cmd_cards)

    p = sub.add_parser("pending")
    p.add_argument("dir")
    p.set_defaults(fn=cmd_pending)

    a = ap.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())


__all__ = ["main", "CATALOG_DIR"]
