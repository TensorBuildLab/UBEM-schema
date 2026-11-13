"""LLM runners and prompts for the alignment benchmark.

Providers (credentials come from the environment, never from this repository):
    anthropic:<model>   Anthropic SDK (ANTHROPIC_API_KEY or an `ant auth login` profile). Claude 5.5 models
                        reject non-default sampling parameters, so repeats use default sampling; effort is set
                        to "low" (classification-style task) and recorded with every call.
    ollama:<model>      Local Ollama server, native /api/chat (OLLAMA_HOST, default http://localhost:11434).
                        num_ctx is set explicitly so long vocabularies are never silently truncated.
    openai:<model>      OpenAI SDK (OPENAI_API_KEY); kept for completeness.

Design for fairness and cost:
  * The task instructions and the target vocabulary form the SYSTEM prompt, identical across items of one
    condition, so Anthropic prompt caching and Ollama's KV-cache prefix reuse both apply. The variable (or
    codebook entry) is the only per-call USER content.
  * Every provider receives the same JSON schema as a structured-output constraint.
  * Every call is cached in benchmark/results/cache/<model>.jsonl with its metadata (task, level, item,
    repeat), raw response, token usage and latency, so results can be re-scored without re-running.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import time
from pathlib import Path

import requests

from . import BENCH
from .io import leaf_concepts

CACHE_DIR = BENCH / "results" / "cache"


def _load_dotenv() -> None:
    """Read KEY=VALUE lines from the repository's .env (git-ignored) into the environment, without printing."""
    env = BENCH.parent / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


_load_dotenv()
ROLE = ("You are an expert in urban building energy modeling (UBEM) and in building energy survey data. "
        "Answer with one JSON object that follows the required schema.")


# ======================================================================================== T2 prompts
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


def t2_request(item: dict, level: str, candidates: list[str] | None = None) -> dict:
    """Return {system, user, schema} for task T2 at a given context level.

    L0 ids only; L1 ids + labels; L2 full semantics; L3 = L2 restricted to retrieved candidates.
    For L3 the system prompt varies per item (no prefix caching); that cost is reported.
    """
    concepts = leaf_concepts()
    block_level = level
    if level == "L3":
        keep = set(candidates or [])
        concepts = [c for c in concepts if c["id"] in keep]
        block_level = "L2"
    ids = [c["id"] for c in concepts] + ["none"]
    system = (
        f"{ROLE}\n\nTask: map one survey variable to the single most specific concept in the target vocabulary "
        "that the variable measures or records. Answer \"none\" if no concept applies.\n\n"
        f"TARGET VOCABULARY\n{_concept_block(block_level, concepts)}\n\n"
        'Output: {"concept": <id or "none">, "alternatives": [<up to two other ids, best first>], '
        '"confidence": <0 to 1>}'
    )
    schema = {
        "type": "object",
        "properties": {
            "concept": {"type": "string", "enum": ids},
            "alternatives": {"type": "array", "items": {"type": "string", "enum": ids}},
            "confidence": {"type": "number"},
        },
        "required": ["concept", "alternatives", "confidence"],
        "additionalProperties": False,
    }
    return {"system": system, "user": f"VARIABLE\n{_variable_block(item)}", "schema": schema}


# ======================================================================================== T3 prompts
UNIT_CHOICES = ["unit:BTU_IT", "unit:KiloW-HR", "unit:FT3", "unit:GAL_US", "iso4217:USD", "unit:FT2", "unit:DEG_F",
                "unit:HR", "none"]

T3_SYSTEM = (
    f"{ROLE}\n\nTask: read the codebook entry of one survey variable and normalize it. Fields:\n"
    "is_weight: true if it is a sampling or analysis weight (final or replicate).\n"
    "is_replicate_weight: true if it is a replicate weight.\n"
    "is_imputation_flag: true if it flags imputation of another variable.\n"
    "flags_variable: the variable name it flags, or \"none\".\n"
    f"unit: one of {UNIT_CHOICES} for numeric quantities; \"none\" for categorical or unitless variables.\n"
    "unit_multiplier: factor applied to raw values before the unit applies (1000 for 'thousand Btu', 100 for "
    "'hundred cubic feet', otherwise 1); 0 if there is no unit.\n"
    "missing_codes: codes meaning not applicable, withheld, refused, don't know or missing; use \"\" for a blank "
    "(\"Missing=...\").\n"
    "codes: every categorical code as [code, label]; [] if the variable is not categorical."
)
T3_SCHEMA = {
    "type": "object",
    "properties": {
        "is_weight": {"type": "boolean"},
        "is_replicate_weight": {"type": "boolean"},
        "is_imputation_flag": {"type": "boolean"},
        "flags_variable": {"type": "string"},
        "unit": {"type": "string", "enum": UNIT_CHOICES},
        "unit_multiplier": {"type": "number"},
        "missing_codes": {"type": "array", "items": {"type": "string"}},
        "codes": {"type": "array", "items": {"type": "array", "items": {"type": "string"}}},
    },
    "required": ["is_weight", "is_replicate_weight", "is_imputation_flag", "flags_variable", "unit",
                 "unit_multiplier", "missing_codes", "codes"],
    "additionalProperties": False,
}


def t3_request(item: dict) -> dict:
    user = (f"dataset: {item['dataset']}\nvariable name: {item['name']}\nlabel: {item.get('label')}\n"
            f"values/format codes (verbatim):\n{item.get('codes_raw') or '(none)'}")
    return {"system": T3_SYSTEM, "user": user, "schema": T3_SCHEMA}


# ======================================================================================== providers
def _key(model: str, req: dict, settings: dict, repeat: int) -> str:
    blob = json.dumps([model, req["system"], req["user"], req["schema"], settings, repeat], sort_keys=True)
    return hashlib.sha256(blob.encode()).hexdigest()[:24]


def cache_path(model: str) -> Path:
    return CACHE_DIR / (re.sub(r"[^A-Za-z0-9._-]", "_", model) + ".jsonl")


def load_cache(model: str) -> dict:
    p = cache_path(model)
    out = {}
    if p.exists():
        with open(p, encoding="utf-8") as fh:
            for line in fh:
                rec = json.loads(line)
                out[rec["key"]] = rec
    return out


def default_settings(model: str, repeat: int) -> dict:
    provider = model.split(":", 1)[0]
    if provider == "anthropic":
        return {"effort": "low", "max_tokens": 4000}
    if provider == "ollama":
        # temperature 0 for the point estimate (repeat 0), 0.7 with a fixed seed for the repeats
        return {"temperature": 0.0 if repeat == 0 else 0.7, "seed": repeat, "num_ctx": 8192, "think": False}
    return {"temperature": 0.0 if repeat == 0 else 0.7, "max_tokens": 1000}


def _call(model: str, req: dict, settings: dict) -> tuple[str, dict]:
    provider, _, name = model.partition(":")
    if provider == "anthropic":
        import anthropic

        client = anthropic.Anthropic()
        msg = client.messages.create(
            model=name,
            max_tokens=settings["max_tokens"],
            system=[{"type": "text", "text": req["system"], "cache_control": {"type": "ephemeral"}}],
            messages=[{"role": "user", "content": req["user"]}],
            output_config={"effort": settings["effort"],
                           "format": {"type": "json_schema", "schema": req["schema"]}},
        )
        if msg.stop_reason == "refusal":
            return "", {"stop_reason": "refusal", "model_version": msg.model}
        text = next((b.text for b in msg.content if b.type == "text"), "")
        u = msg.usage
        return text, {"input_tokens": u.input_tokens, "output_tokens": u.output_tokens,
                      "cache_read_input_tokens": getattr(u, "cache_read_input_tokens", None),
                      "cache_creation_input_tokens": getattr(u, "cache_creation_input_tokens", None),
                      "stop_reason": msg.stop_reason, "model_version": msg.model}
    if provider == "ollama":
        host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        body = {"model": name, "stream": False, "format": req["schema"], "keep_alive": "30m",
                "think": settings.get("think", False),
                "messages": [{"role": "system", "content": req["system"]}, {"role": "user", "content": req["user"]}],
                "options": {k: settings[k] for k in ("temperature", "seed", "num_ctx") if k in settings}}
        r = requests.post(f"{host}/api/chat", json=body, timeout=600)
        r.raise_for_status()
        js = r.json()
        return js["message"]["content"], {"input_tokens": js.get("prompt_eval_count"),
                                          "output_tokens": js.get("eval_count"),
                                          "model_version": js.get("model"), "stop_reason": js.get("done_reason")}
    if provider == "mock":  # plumbing test only: answers the first allowed value of every field
        props = req["schema"]["properties"]
        out = {}
        for k, v in props.items():
            if "enum" in v:
                out[k] = v["enum"][0]
            else:
                out[k] = {"boolean": False, "number": 0.5, "string": "none", "array": []}[v["type"]]
        return json.dumps(out), {"input_tokens": approx_tokens(req["system"] + req["user"]), "output_tokens": 20}
    if provider == "openai":
        from openai import OpenAI

        r = OpenAI().chat.completions.create(
            model=name, temperature=settings["temperature"], max_tokens=settings["max_tokens"],
            response_format={"type": "json_schema", "json_schema": {"name": "answer", "schema": req["schema"]}},
            messages=[{"role": "system", "content": req["system"]}, {"role": "user", "content": req["user"]}])
        return r.choices[0].message.content, {"input_tokens": r.usage.prompt_tokens,
                                              "output_tokens": r.usage.completion_tokens, "model_version": r.model}
    raise ValueError(f"unknown provider in {model!r}")


def complete(model: str, req: dict, meta: dict, repeat: int = 0, cache: dict | None = None) -> dict:
    cache = cache if cache is not None else load_cache(model)
    settings = default_settings(model, repeat)
    k = _key(model, req, settings, repeat)
    if k in cache:
        return cache[k]
    err = None
    for attempt in range(4):
        try:
            t0 = time.time()
            text, usage = _call(model, req, settings)
            break
        except Exception as exc:  # noqa: BLE001  network or rate limit: back off, then give up loudly
            err = exc
            time.sleep(5 * 2 ** attempt)
    else:
        raise RuntimeError(f"{model} failed after retries: {err}")
    rec = {"key": k, "model": model, "repeat": repeat, "settings": settings, **meta,
           "response": text, "latency_s": round(time.time() - t0, 2), **usage}
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with open(cache_path(model), "a", encoding="utf-8") as fh:
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


def approx_tokens(text: str) -> int:
    """Rough size estimate (4 characters per token) for planning only; real counts come from the APIs."""
    return len(text) // 4
