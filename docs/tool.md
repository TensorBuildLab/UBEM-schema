# The ubem-link tool

`ubem-link` turns a dataset you have not seen before, and whatever documentation it comes with, into a UBEM-Link
profile: one record per column stating what it measures, in which unit, which values mean "missing", whether it
is a weight, a flag or a key, and how sure the model was. A person reviews the flagged columns; the profile is
then applied to the data without any model, and several profiled datasets can be joined into one table.

```bash
pip install -e .                       # from a clone of the repository
ollama pull qwen3:8b                   # a local model (about 5 GB); nomic-embed-text for retrieval
ollama pull nomic-embed-text
ubem-link describe data.csv --codebook codebook.xlsx --entry my-entry.yaml --out profiles/
```

## Commands

| Command | What it does |
|---|---|
| `describe DATA --codebook ... --entry ...` | Profile every column; write `<id>.ubem.yaml`, `<id>.review.csv`, `<id>.card.md`, `<id>.log.jsonl` |
| `conventions DOCS.txt -o conventions.yaml` | Propose dataset conventions from a user guide, each with a quote and a machine-readable scope |
| `validate PROFILE.yaml` | Check a profile against the JSON Schema and rules; list open review flags |
| `apply PROFILE.yaml DATA -o OUT.csv` | Remove missing codes, convert units to SI, drop do-not-use columns (no model) |
| `integrate RECIPE.yaml -o OUT.csv` | Join profiled datasets by keys and nearest weather station; report linkage |
| `select DATA --target CONCEPT --purpose TEXT` | Ask which column holds a concept a pipeline needs |
| `catalog --role ... --key ... --granularity ...` | Search the catalog |
| `cards --out DIR` | Export the AI documentation layer for any assistant |
| `pending DIR` | List requests waiting for an assistant (files backend) |

## Codebooks it reads

Socrata data dictionaries (`.../api/views/<id>.json`, used by many city portals), Frictionless Data Packages and
Table Schemas, CSV on the Web metadata, DDI-Codebook XML, Markdown metadata pages with an attribute table, and
generic CSV or Excel codebooks, including the EIA codebooks of CBECS and RECS (the header row is detected). Several
sources can be given at once (`--codebook dictionary.json metadata.md`); their descriptions are merged. Without a
codebook, columns are described by their names and a summary of their values.

## How a column is profiled, and why

Each step follows a result of the paper's experiments with two small local models.

1. **Concept mapping with retrieval.** A dense retriever (nomic-embed-text through Ollama; TF-IDF if no server
   is running) picks the ten most similar concept cards, and the model chooses among them or among the join-key
   types, with its answer constrained to those ids. Ten retrieved cards kept mapping accuracy at a fifth of the
   tokens of the full vocabulary, and a closed list rules out invented concepts at no accuracy cost.
2. **Normalization with the source's own units.** The model chooses the unit from the full UBEM-Link unit list,
   which includes the units in which sources publish (kBtu, therm, foot). When the list lacked kBtu, both models
   in the paper wrote kBtu as kilowatt-hours, a 215% error in New York City's energy use intensity.
3. **Scoped conventions, applied by the tool.** A dataset entry may state conventions (`"Not Available"` means
   missing; heights are in feet; a field must not be used). Only the conventions whose machine-readable scope
   (`applies_to_variables` or `applies_to_pattern`) covers a column are shown to the model, and their stated
   unit, multiplier and missing codes overwrite the model's answer. In the paper, conventions given as prose for
   the whole dataset were also applied to columns they did not concern.
4. **Checks and a review queue.** Every profile is checked against its documentation (a unit named there, scale
   words), its data (missing codes that are frequent valid values, values that look like missing codes but are
   not listed), its concept (unit of the wrong quantity kind, values out of a plausible range after conversion)
   and its conventions. Flags and low confidence put a column at the top of `<id>.review.csv`. In the paper the
   checks caught most consequential errors but also flagged correct profiles, so they decide what a person
   looks at first, not what is correct.

## Models

| `--model` | Runs | Notes |
|---|---|---|
| `ollama:qwen3:8b` (default) | locally through Ollama | the model of the paper; runs on an 8 GB GPU |
| `ollama:<any>` | locally | for example `ollama:qwen3:14b` (needs about 10 GB) |
| `openai:<name>` | any OpenAI-compatible server | set `OPENAI_BASE_URL` for LM Studio, vLLM or llama.cpp (local), or `OPENAI_API_KEY` for a hosted API |
| `anthropic:<name>` | Anthropic API | set `ANTHROPIC_API_KEY`; install `pip install -e ".[llm]"` |
| `files:<dir>` | no API | requests are written to files that an assistant such as Claude Code answers; see [tutorial 4](tutorials/04-assistants-and-apis.md) |

Keys are read from the environment or a `.env` file in the working directory, never from the command line.
Every answer is cached (`--cache`, default `.ubem_link_cache/`), so a rerun costs nothing and a profile can be
regenerated exactly.

## What the tool does not do

It does not decide that a profile is correct. The review file lists what to check; `profiled_by` in each variable
says `(unreviewed)` until a person changes it. Concept mapping by small models was right for about three in five
survey variables in the paper's benchmark, so the concept column of a draft profile in particular needs review.
