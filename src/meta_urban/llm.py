"""LLM runners and prompts for the alignment benchmark.

Providers (keys come from the environment, never from this repository):
    anthropic:<model>          ANTHROPIC_API_KEY
    openai:<model>             OPENAI_API_KEY
    local:<model>              any OpenAI-compatible server (Ollama, vLLM, llama.cpp); base URL from
                               META_URBAN_LOCAL_BASE_URL (default http://localhost:11434/v1)

Every call is cached in benchmark/results/cache/<provider>__<model>.jsonl keyed by a hash of
(model, prompt, temperature, repeat), so reruns are free and the raw outputs are part of the record.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import time
from pathlib import Path

from . import BENCH
from .io import leaf_concepts

CACHE_DIR = BENCH / "results" / "cache"

SYSTEM = ("You are an expert in urban building energy modeling (UBEM) and building energy survey data. "
          "Answer only with one JSON object, no prose.")


# ----------------------------------------------------------------------------------------------- prompts (T2)
def _concept_block(level: str, concepts: list[dict]) -> str:
    if level == "L0":
        return "\n".join(c["id"] for c in concepts)
    if level == "L1":
        return "\n".join(f"{c['id']}: {c['pref_label']}" for c in concepts)
    lines = []
    for c in concepts:
        extra = []
        if c.get("broader"):
            extra.append(f"broader={c['broader']}")
        if c.get("entity"):
            extra.append(f"describes={c['entity']}")
        if c.get("canonical_unit"):
            extra.append(f"unit={c['canonical_unit']}")
        if c.get("alt_labels"):
            extra.append("also called: " + ", ".join(c["alt_labels"][:6]))
        lines.append(f"{c['id']}: {c['pref_label']}. {c['definition']} [{'; '.join(extra)}]")
    return "\n".join(lines)


def _variable_block(item: dict, max_codes: int = 8) -> str:
    parts = [f"dataset: {item['dataset']}", f"variable name: {item['name']}", f"label: {item.get('label')}"]
    if item.get("section"):
        parts.append(f"questionnaire section: {item['section']}")
    codes = item.get("code_list") or []
    if codes:
        shown = "; ".join(f"{c}={l}" for c, l in codes[:max_codes])
        more = f" (+{len(codes) - max_codes} more)" if len(codes) > max_codes else ""
        parts.append(f"codes: {shown}{more}")
    return "\n".join(parts)


def t2_prompt(item: dict, level: str, candidates: list[str] | None = None) -> str:
    concepts = leaf_concepts()
    if level == "L3":
        keep = set(candidates or [])
        concepts = [c for c in concepts if c["id"] in keep]
        level_for_block = "L2"
    else:
        level_for_block = level
    return (
        "Map the survey variable below to the single most specific concept in the target vocabulary that the "
        "variable measures or records. If no concept applies, answer \"none\".\n\n"
        f"TARGET VOCABULARY (id: description)\n{_concept_block(level_for_block, concepts)}\n\n"
        f"VARIABLE\n{_variable_block(item)}\n\n"
        'Return JSON: {"concept": "<id or none>", "alternatives": ["<second id>", "<third id>"], '
        '"confidence": <number 0-1>}'
    )


# ----------------------------------------------------------------------------------------------- prompts (T3)
UNIT_CHOICES = ["unit:BTU_IT", "unit:KiloW-HR", "unit:FT3", "unit:GAL_US", "iso4217:USD", "unit:FT2", "unit:DEG_F",
                "unit:HR", "null"]


def t3_prompt(item: dict) -> str:
    return (
        "Read the codebook entry of a survey variable and normalize it.\n\n"
        f"dataset: {item['dataset']}\nvariable name: {item['name']}\nlabel: {item.get('label')}\n"
        f"values/format codes (verbatim):\n{item.get('codes_raw') or '(none)'}\n\n"
        "Return JSON with keys:\n"
        ' "is_weight": true if this is a sampling/analysis weight (final or replicate),\n'
        ' "is_replicate_weight": true if it is a replicate weight,\n'
        ' "is_imputation_flag": true if it flags imputation of another variable,\n'
        ' "flags_variable": name of the variable it flags, or null,\n'
        f' "unit": one of {UNIT_CHOICES} for numeric quantities (null for categorical or unitless),\n'
        ' "unit_multiplier": factor to apply before the unit (e.g. 1000 for "thousand Btu"), or null,\n'
        ' "missing_codes": list of codes that mean not applicable / withheld / missing ("" for blank),\n'
        ' "codes": list of [code, label] pairs for categorical codes, [] if none'
    )


# ----------------------------------------------------------------------------------------------- providers
def _key(model: str, prompt: str, temperature: float, repeat: int) -> str:
    return hashlib.sha256(json.dumps([model, prompt, temperature, repeat]).encode()).hexdigest()[:24]


def _cache_path(model: str) -> Path:
    return CACHE_DIR / (re.sub(r"[^A-Za-z0-9._-]", "_", model) + ".jsonl")


def _load_cache(model: str) -> dict:
    p = _cache_path(model)
    if not p.exists():
        return {}
    out = {}
    with open(p, encoding="utf-8") as fh:
        for line in fh:
            rec = json.loads(line)
            out[rec["key"]] = rec
    return out


def _call(model: str, prompt: str, temperature: float, max_tokens: int = 400) -> tuple[str, dict]:
    provider, _, name = model.partition(":")
    if provider == "anthropic":
        import anthropic

        client = anthropic.Anthropic()
        msg = client.messages.create(model=name, max_tokens=max_tokens, temperature=temperature, system=SYSTEM,
                                     messages=[{"role": "user", "content": prompt}])
        text = "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")
        return text, {"input_tokens": msg.usage.input_tokens, "output_tokens": msg.usage.output_tokens,
                      "model_version": msg.model}
    if provider in {"openai", "local"}:
        from openai import OpenAI

        client = OpenAI() if provider == "openai" else OpenAI(
            base_url=os.environ.get("META_URBAN_LOCAL_BASE_URL", "http://localhost:11434/v1"), api_key="local")
        r = client.chat.completions.create(model=name, temperature=temperature, max_tokens=max_tokens,
                                           messages=[{"role": "system", "content": SYSTEM},
                                                     {"role": "user", "content": prompt}])
        u = r.usage
        return r.choices[0].message.content, {"input_tokens": getattr(u, "prompt_tokens", None),
                                              "output_tokens": getattr(u, "completion_tokens", None),
                                              "model_version": r.model}
    raise ValueError(f"unknown provider in {model!r}")


def complete(model: str, prompt: str, temperature: float = 0.0, repeat: int = 0, cache: dict | None = None) -> dict:
    cache = cache if cache is not None else _load_cache(model)
    k = _key(model, prompt, temperature, repeat)
    if k in cache:
        return cache[k]
    for attempt in range(4):
        try:
            t0 = time.time()
            text, usage = _call(model, prompt, temperature)
            break
        except Exception as exc:  # noqa: BLE001  (network / rate limit): back off and retry
            if attempt == 3:
                raise
            time.sleep(2 ** attempt * 5)
            last = exc  # noqa: F841
    rec = {"key": k, "model": model, "temperature": temperature, "repeat": repeat, "prompt_sha": k,
           "response": text, "latency_s": round(time.time() - t0, 2), **usage}
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with open(_cache_path(model), "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    cache[k] = rec
    return rec


def parse_json(text: str) -> dict | None:
    if not text:
        return None
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
