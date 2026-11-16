# Submission checklist: *Computers, Environment and Urban Systems* (Elsevier)

CEUS is a hybrid journal: publication is free on the subscription route, and open access is optional (MPDL
open-access record for Elsevier 0198-9715). History: desk-rejected by *Energy* on 2026-11-15 (scope), without
reviews. This version (v4) was revised after three independent AI reviews; the response is in the authors'
working folder.

The official Guide for Authors page blocks automated access, so journal-specific limits (word count, abstract
length) **must be confirmed against the guide** before submission. Rebuild every file in this folder with
`python scripts/graphical_abstract.py`, `python scripts/build_docx.py` (prints the word counts) and
`python scripts/build_supplement.py`.

## Files to upload

| Item | File | Status |
|---|---|---|
| Manuscript, anonymized | `manuscript_without_author_info.docx` | No author block, acknowledgement, data availability, AI declaration or repository link; document properties cleared |
| Title page | authors' working folder, `title page.docx` | Authors, affiliations, CRediT, competing interests, acknowledgement, data availability, AI declaration |
| Highlights | `highlights.docx` | 5 bullets, 63–81 characters (Elsevier limit 85) |
| Graphical abstract | `graphical_abstract.tif` (or `.pdf`) | 2656 x 1000 px; both models, city panel, no false-alarm claim |
| Figures | `Figure_1` to `Figure_9` (`.pdf` vector, `.png` 600 dpi) | One file per figure; Fig. 9 is the New York City map |
| Supplementary material | `paper/build/supplementary_material.docx` | S1–S22, anonymized |
| Cover letter | `cover_letter.docx` | Addressed to CEUS |

## Manuscript content

| Requirement | Status |
|---|---|
| Abstract | 200 words; **confirm** the limit |
| Main text and tables | About 8,000 words (6,823 main text including headings and captions, 1,200 in tables); **confirm** the limit |
| Keywords | 6 |
| Use of AI in the research | Section 5.5 (Methods) |
| Declaration of generative AI and AI-assisted technologies | On the title page (anonymized review) |
| References numbered in order of citation, DOIs, [dataset] marks | Done |
| Prior preprint (arXiv:2311.08535) | **Decision pending** (see the response document): cite in the third person, rename, or keep as is |

## Classifications or keywords in the submission system

Choose those closest to urban data and computing: urban energy, building stock, GIS and spatial data
infrastructure, semantic interoperability, artificial intelligence and machine learning.
