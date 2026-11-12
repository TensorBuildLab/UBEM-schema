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
   seed 20261112.
2. **Annotate independently.** Two annotators with UBEM experience fill `annotator_1` and `annotator_2` in
   `t2_gold_<dataset>.csv` (copy of the draft file). Each sees the variable name, label, question text and
   code list and the concept vocabulary (`schema/vocab/ubem_concepts.yaml`). They may accept the draft or
   change it. Rule: choose the most specific concept the variable measures; `none` if no concept applies.
3. **Agreement.** Report Cohen's kappa between annotators (`meta_urban.metrics.cohen_kappa`) and the share of
   draft labels each annotator changed.
4. **Adjudicate.** Disagreements are resolved in discussion; the result goes into `adjudicated`.
5. **Vocabulary changes.** If annotators agree a concept is missing, record it in `notes` and add it to the
   vocabulary in a new version; do not silently re-label.

## Task T1 (dataset profile extraction)

Gold = the verified catalog entries in `catalog/datasets/`. Before T1 is run, an author spot-checks at least
20 entries against the publisher pages (fields marked null by the agents are the priority), and the
documentation snapshot used as model input is saved under `benchmark/inputs/t1_docs/<id>.txt` with its
retrieval date.
