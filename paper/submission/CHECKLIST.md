# Submission checklist: *Energy* (Elsevier)

The official Guide for Authors page (sciencedirect.com/journal/energy/publish/guide-for-authors) blocks
automated access. The limits below marked "secondary source" come from a third-party summary and **must be
confirmed against the official guide** before submission. Rebuild every file in this folder with
`python scripts/graphical_abstract.py` and `python scripts/build_docx.py`.

## Files to upload

| Item | File | Status |
|---|---|---|
| Manuscript | `manuscript.docx` | Editable Word, single column, no underline, continuous line numbers from the title page, page numbers |
| Highlights | `highlights.docx` | 5 bullets, 71-83 characters each (limit 85) |
| Graphical abstract | `graphical_abstract.tif` (or `.pdf`) | 2656 x 1000 px, landscape, readable at 13 cm; numbers read from the generated tables |
| Figures | `Figure_1` to `Figure_8` (`.pdf` vector, `.png` 600 dpi) | One file per figure, numbered in order of appearance |
| Cover letter | `cover_letter.docx` | Addressed to *Energy* |

## Manuscript content

| Requirement | Status |
|---|---|
| Research article length: at most 8,000 words including tables, excluding abstract and references (secondary source) | Within the limit (counted by `build_docx.py`, printed at build) |
| Abstract at most 200 words (secondary source) | 199 words |
| Keywords | 7 |
| Nomenclature (expected for this journal, secondary source) | Table after the keywords |
| Title concise, no undefined abbreviations | Done |
| Authors, affiliations (organization, city, postal code, country), corresponding email | Done |
| Numbered sections; abstract and nomenclature unnumbered | Done |
| Tables editable, numbered in order of citation | 9 tables, generated from `paper/tables/` |
| Figures cited, captioned, AI-assisted creation disclosed in captions | Figs. 1-8 |
| SI units | EUI in kWh/m2, floor area in m2, energy in kWh/MWh; source units (Btu, ft2) only when quoting the surveys |
| CRediT statement | Done |
| Declaration of competing interest | Present |
| Funding | **Fill** |
| Acknowledgments | **Fill** |
| Data availability | Done (public GitHub repository) |
| Declaration of generative AI in manuscript preparation | Present, before the references |
| References numbered in order of citation; DOIs; web references with access dates; [dataset] marks | Done |
| American English | Done |
| Prior preprint disclosed | Cover letter (arXiv:2311.08535) |

## At submission

- Article type: Research article (full length article).
- Author order identical to the title page.
- Suggested reviewers: optional, placeholder in the cover letter.
