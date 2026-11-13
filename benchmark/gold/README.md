# Gold labels and annotation protocol

## Task T3 (code and unit normalization): automatic gold

`meta_urban.codebooks` derives the T3 labels (weight flags, imputation flags and the variable they flag,
unit and multiplier, missing codes, code list) deterministically from the publishers' codebooks. They are exact
with respect to the codebook text. The rules are in the module docstring and are unit-tested in `tests/`.

## Task T2 (variable to concept): human gold, pre-filled by rules

`t2_draft_<dataset>.csv` holds a rule-based draft label for every variable (`meta_urban.gold_draft`). The
draft is **not** the gold standard. Results computed on draft labels are marked `gold_status = draft` and must
not be reported in the paper.

Protocol (to be run by the authors):

1. **Sample.** `benchmark/inputs/t2_eval_sample.csv`: 300 substantive variables (150 CBECS 2018, 150 RECS
   2020; imputation flags and replicate weights excluded because they are trivial), stratified by draft concept,
   seed 20261112. The sample is frozen: `bench items` keeps it unless called with `resample=True`.
2. **Annotate blind and independently.** `python -m meta_urban.gold_sheets make` writes
   `annotation/annotator_1.csv`, `annotation/annotator_2.csv` and `annotation/concepts.csv`. The sheets show
   the variable (name, label, section, question, codes) but **neither the draft label nor any model output**,
   so the gold is anchored on neither. Rule: `concept` is the most specific concept the variable measures, or
   `none`. Use `also_acceptable` (semicolon-separated ids) only when the variable genuinely fits another
   concept as well, for example a fuel-by-end-use indicator ("natural gas used for water heating") that is
   both an energy-source flag and a water-heating attribute. Annotators do not discuss items before merging.
3. **Agreement.** `python -m meta_urban.gold_sheets merge` reports Cohen's kappa, raw agreement and the share
   of draft labels each annotator changed, and writes `t2_gold_<dataset>.csv`. Agreed labels are adopted;
   disagreements are marked `needs_adjudication`.
4. **Adjudicate.** Resolve each flagged item in discussion and fill `adjudicated` (and `also_acceptable` if
   needed). Re-running `merge` keeps adjudicated rows.
5. **Score.** Gold is read at load time, so `python -m meta_urban.bench score` and
   `python -m meta_urban.bench_report` use the adjudicated labels without re-running any model. Strict
   accuracy uses `adjudicated`; lenient accuracy also accepts `also_acceptable`.
6. **Vocabulary changes.** If annotators agree a concept is missing, record it in `notes` and add it to the
   vocabulary in a new version; do not silently re-label.

Why blind: a check of the provisional runs found draft labels that are plainly wrong (high-intensity
discharge lighting drafted as energy use intensity because of the word "intensity"; an induction cooktop
drafted as a ventilation system). Annotators who see the draft tend to accept it.

## How the released T2 gold was made (2026-11-13)

Two qualified human annotators were not available, so steps 2 and 4 were run by LLM agents in fresh contexts
restricted to the annotation files (no web, no repository access, no draft labels, no model outputs):
annotator 1 Claude Opus 5.5, annotator 2 Claude Sonnet 5.5, adjudicator Claude Opus 5.5. Results: kappa 0.914,
raw agreement 0.920, 24 items adjudicated (`annotation/adjudication.csv` with rationales). Both annotators
changed the draft on 25.7% of items. The evaluated models (Qwen3, Llama 3.1) are from other developers. The
gold was not audited by a domain expert; instead, every result is rescored against four label sets
(`paper/tables/bench_t2_label_sensitivity.csv`). An expert can still audit the 50 sampled labels in
`annotation/human_audit.csv` (instructions in `annotation/AUDIT_INSTRUCTIONS.md`). Human annotations can
replace these files at any time; scoring reads the gold at run time.

## Task T1 (dataset profile extraction; not used in the paper)

Gold = the verified catalog entries in `catalog/datasets/`. Before T1 is run, an author spot-checks at least
20 entries against the publisher pages (fields marked null by the agents are the priority), and the
documentation snapshot used as model input is saved under `benchmark/inputs/t1_docs/<id>.txt` with its
retrieval date.
