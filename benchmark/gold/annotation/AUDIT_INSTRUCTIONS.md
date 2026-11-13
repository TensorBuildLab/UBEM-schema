# Auditing 50 gold labels (about 30 minutes)

The file `human_audit.csv` (opens in Excel) lists 50 randomly chosen variables from the CBECS 2018 and RECS 2020
codebooks. Each has been assigned a concept from the Meta-Urban vocabulary. We need a building-energy expert to
say whether the assignment is reasonable.

For each row, read:

- `label`, `question`, `codes`: what the survey variable is.
- `gold` and `gold_meaning`: the concept it was assigned and that concept's definition.
- `also_acceptable_meaning`: other concepts accepted for ambiguous variables (may be empty).

Then fill:

- `verdict`: `agree` if the gold concept (or one of the accepted alternatives) is a reasonable description of
  what the variable measures; `disagree` otherwise.
- `correction`: only if you disagree, the concept you would choose (any id from `concepts.csv`, or `none`).
- `comment`: optional.

Rule of thumb: the concept should be the most specific one that describes what the variable measures.
"Is natural gas used for water heating?" is about the energy source used (with water heating as an accepted
alternative); "Electricity used for space heating, in kWh" is end-use energy; "Main heating equipment type" is
the space heating system. You do not need to check spelling, coding or the other columns.

When done, return the file (or save it in place) and run:

```bash
python -m meta_urban.gold_sheets audit_report
```
