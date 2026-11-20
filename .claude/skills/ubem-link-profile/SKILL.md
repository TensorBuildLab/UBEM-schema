---
name: ubem-link-profile
description: Profile a building or urban energy dataset with the ubem-link tool, answering the model requests yourself through the files backend, then walk the user through the review file. Use when someone asks to make a dataset AI-ready, profile or describe a dataset's columns, map columns to UBEM-Link concepts, find units or missing codes, or prepare data for urban building energy modeling with this repository.
---

# Profile a dataset with ubem-link (Claude Code as the model)

The `ubem-link` tool profiles each column of a dataset: concept or join key, unit, multiplier, missing codes, code
list, weight or flag roles. With `--model files:<dir>` it writes its requests to files instead of calling a model,
and you answer them.

## Steps

1. Find the data file and every piece of documentation the user has (portal dictionary JSON, codebook CSV/XLSX,
   metadata page, user guide). Ask for documentation if there is none; profiling from values alone is weak.
2. If the dataset is in the catalog (`ubem-link catalog --text <words>`), use its entry with `--entry <id>`; its
   conventions are applied by the tool. Otherwise consider drafting conventions from the user guide
   (`ubem-link conventions guide.txt -o conventions.yaml`), and show the user the proposals before using them.
3. Run:
   ```bash
   ubem-link describe DATA --codebook DOCS... [--entry ID] --model files:work/ --out out/
   ubem-link pending work/
   ```
4. Answer every request in `work/requests.jsonl`. For each line: read `system` (the instructions) and `user`
   (the column), and append one line to `work/responses.jsonl`:
   `{"key": "<key>", "response": <JSON object that follows schema exactly>}`.
   - Use only values allowed by the schema's enums.
   - Base units and missing codes on the documentation and the value summary. If the documentation does not state
     a unit, do not invent one; choose the unit the values support and give a low confidence in the mapping answer.
   - Never list a value as a missing code if it is a valid observation (zero energy use is a valid value unless
     the documentation says otherwise).
5. Rerun the same `describe` command. It reads your answers, applies the dataset conventions (which overwrite your
   unit and missing codes where they state them, and flag the disagreement) and runs the checks.
6. Open `out/<id>.review.csv` and go through it with the user, top rows first. Explain each flag in one line.
   Do not mark a profile as reviewed yourself: `profiled_by` stays `(unreviewed)` until the user confirms.
7. `ubem-link validate out/<id>.ubem.yaml`, then, if the user wants SI data,
   `ubem-link apply out/<id>.ubem.yaml DATA -o out/<id>_si.csv`.

## Notes

- To use a local model instead, replace `files:work/` with `ollama:qwen3:8b` (requires Ollama).
- Never put API keys on the command line or in files you create; the tool reads them from the environment or `.env`.
