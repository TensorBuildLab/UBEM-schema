# Tutorial 4: use Claude Code, a chat assistant or a hosted model

The paper evaluated only small local models. The tool works with any model that can follow a JSON Schema, and
with assistants that have no API at all.

## A. An assistant without an API (Claude Code, ChatGPT, or a person)

Use the `files` backend. The tool writes each request to a file instead of calling a model:

```bash
ubem-link describe examples/nyc/footprints_sample.csv --codebook examples/nyc/footprints_dictionary.json \
    --entry geo-nyc-footprints --model files:work/ --out out/
# -> "20 requests wait for answers in work/requests.jsonl"
ubem-link pending work/                  # writes work/prompts.md: instructions, input and answer schema per request
```

Each line of `work/requests.jsonl` holds `key`, `system` (instructions), `user` (the column) and `schema` (the
JSON Schema the answer must follow). Answer each by appending a line to `work/responses.jsonl`:

```json
{"key": "3f2c...", "response": {"concept": "building_height", "alternatives": [], "confidence": 0.9}}
```

Then run the same `describe` command again: answered requests are read, the conventions and checks are applied,
and the profile is written.

**With Claude Code**, open the repository and ask, for example: "Profile examples/nyc/footprints_sample.csv with
ubem-link using the files backend, answer the requests yourself following each schema, and show me the review
file." The skill in `.claude/skills/ubem-link-profile/SKILL.md` tells Claude Code how to do this: run
`describe`, answer `requests.jsonl` one request at a time without guessing values the documentation does not
support, rerun, then walk you through the review file.

## B. A hosted or local server with an OpenAI-compatible API

```bash
export OPENAI_BASE_URL=http://localhost:1234/v1       # LM Studio, vLLM or llama.cpp; omit for the OpenAI API
export OPENAI_API_KEY=...                             # only for hosted APIs; or put it in .env
ubem-link describe data.csv --codebook codebook.json --model openai:<model-name>
```

## C. Anthropic API

```bash
pip install -e ".[llm]"
# put ANTHROPIC_API_KEY=... in a .env file in the working directory (never on the command line)
ubem-link describe data.csv --codebook codebook.json --model anthropic:<model-id>
```

## Which to choose

Local models keep data on your machine and cost nothing per call; the paper's results are for them. Larger hosted
models are likely to map concepts better, which the paper did not test. Whatever the model, the conventions of the
dataset entry and the checks are applied the same way, and the review file is what a person should read.
