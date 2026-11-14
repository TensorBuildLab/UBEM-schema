# Submission checklist (v0.3)

Proposed journal: *Engineering Applications of Artificial Intelligence* (Elsevier, subscription route), pending
the authors' confirmation. The files follow Elsevier's common requirements, which this folder already met for
Automation in Construction. **Before submitting, check the items marked "confirm" against the chosen
journal's own Guide for Authors.** Rebuild every file in this folder with `python scripts/graphical_abstract.py`
and `python scripts/build_docx.py`.

## Files to upload

| Item | File | Status |
|---|---|---|
| Manuscript | `manuscript.docx` | Editable Word, single column, no underline, continuous line numbers from the title page, page numbers |
| Highlights | `highlights.docx` | 5 bullets, each at most 84 characters (Elsevier limit 85) |
| Graphical abstract | `graphical_abstract.tif` (or `.pdf`) | 2656 x 1000 px, landscape, readable at 13 cm; plotted from the generated tables |
| Figures | `Figure_1` to `Figure_8` (`.pdf` vector, `.png` 600 dpi) | One file per figure, numbered in order of appearance |
| Cover letter | `cover_letter.docx` | Addressed to EAAI; states the AI contribution and the application separately |
| Response to comments | `Liang Zhang working folder/response_to_comments.md` | Internal: how each comment on v0.2 was addressed |

## Manuscript content

| Requirement | Status |
|---|---|
| Title concise, no undefined abbreviations | Done ("AI" spelled out in the title) |
| Authors, affiliations (organization, city, postal code, country), corresponding email | Done |
| Abstract | 241 words; **confirm** the journal's limit (AiC's was 150; most Elsevier AI journals allow 250-300) |
| Keywords | 7 |
| Numbered sections; abstract unnumbered | Done |
| Tables | 8, editable, numbered in order, generated from `paper/tables/` |
| Figures cited, captioned, AI-assisted creation disclosed in captions | Done for Figs. 1-8 |
| CRediT statement | Done |
| Declaration of competing interest | Present |
| Funding | **Fill** |
| Acknowledgments | **Fill** |
| Data availability | Done (public GitHub repository) |
| Declaration of generative AI in manuscript preparation | Present, before the references |
| References numbered in order of citation; DOIs; web references with access dates; [dataset] marks | Done (94 references) |
| American English | Done |
| Prior preprint disclosed | Cover letter (arXiv:2311.08535) |

## At submission

- Article type: Research paper.
- Author order identical to the title page.
- Suggested reviewers: optional, in the cover letter placeholder.
