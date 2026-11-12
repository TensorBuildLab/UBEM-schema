# Why the 2023 manuscript kept failing, and what has to change

Manuscript: *Taxonomy, Semantic Data Schema, and Schema Alignment for Open Data in Urban Building Energy
Modeling* (Zhang, Chen, Zou; arXiv 2311.08535). Submitted to Applied Energy, Sustainable Cities and Society,
Building and Environment, Building Research & Information, Urban Informatics and Energy and Buildings
(2023–2025). Only the Urban Informatics round left written reviews in the project folder (two reviewers: one
major, one minor). This note reads those reviews together with the manuscript itself. Review comments are
paraphrased, not quoted, because peer reviews are confidential.

## 1. The verdict in one paragraph

The paper makes three claims, and none of them is supported by evidence a reviewer can check. The review is
not systematic (no search protocol, no inclusion criteria, U.S.-centric, many web pages instead of papers, and
it admits it "will not exhaust" sources). The "semantic data schema" is a two-column table of field names and
example values: it has no classes, no relations, no identifiers, no units model, no link to existing standards,
and no machine-readable release. The LLM case study is three datasets run once in one ChatGPT session in
August 2023, with no ground truth, no metric, no baseline and no repeat, and its central inference ("the LLM
succeeded, so the schema is machine-readable and human-interpretable") does not follow, because the same LLM
would have succeeded with any reasonable list of field names. Editors at energy journals see a review that is
thinner than Malhotra et al. (2022) and Goy et al. (2020), a schema that is weaker than CityGML Energy ADE or
BEDES, and an LLM demo that is anecdotal. That is a desk-reject or a reject after review, at every venue.

## 2. Specific problems, ranked by how much they hurt

### P1. The central inference is a non-sequitur (fatal)
The abstract and conclusion say the accurate LLM results "indicate the machine-readability and
human-interpretability of the developed semantic data schema." Success of a strong LLM on three easy inputs
says nothing about the schema unless it is compared with alternatives (no schema, a flat field list, an
existing standard). Reviewer 2 (Urban Informatics) asked exactly this: the case studies show feasibility of
alignment, not the advantage of the schema, and the uncertainty of LLMs is not addressed.

### P2. The "accurate" results are not accurate (fatal once a reviewer looks)
The project folder holds the outputs. Checks against the raw files:
- CBECS: "Effective coverage" was returned as `Regions: [3 4 1 2], Census divisions: [5 9 7 2 8 3 6 1 4]`,
  i.e., raw codes, not decoded, unordered. That is not an aligned value.
- CBECS: "Sample or Probability = Sample" and the processed tables drop the survey weights (`FINALWT` and 151
  jackknife replicate weights). CBECS rows are a weighted probability sample; using them as a distribution
  without weights is a methodological error a building-stock modeler (e.g., an NREL ComStock reviewer) will
  catch immediately.
- CBECS: "Joint distribution list = []" although every microdata record is, by construction, a joint sample
  of all characteristics. The field definition itself is confused.
- EIA MER: "Timestamp format YYYY-MM-DD HH:MM:SS" for monthly data, "Interpolation: Unknown", and
  "Name of dataset = U.S. Energy Information Administration" (the publisher, not the dataset).
- RECS: Fig. 7 and Fig. 8 show only a partial list "for demonstration."
- The LLM was "ChatGPT-4 code interpreter, August 3, 2023": a closed, retired product. Nothing can be re-run.

### P3. The schema is not semantic (major; Reviewer 1 Q9)
Reviewer 1 asked for a definition of "semantic data schema" and for the spatial, temporal and semantic
relations it encodes. Table 1 has none. The taxonomy has seven categories but Table 1 defines six (the
"comprehensive data lake" has no schema), and the same fields (name, timestamp format, constant interval,
interval, interpolation, coverage) are repeated per category instead of being defined once. Fields mix dataset-level metadata (name, coverage) and
variable-level semantics (weather variable list) without saying which is which. There are no units, no code
lists, no identifiers, no cardinalities, no join keys (Chen et al. 2019 already identified missing common keys
as the main barrier), and no mapping to BEDES, Brick, CityGML Energy ADE, DCAT or schema.org.

### P4. The taxonomy mixes orthogonal dimensions (major)
The seven categories combine three different axes: content (weather, geometry, occupant behavior,
characteristics), spatial granularity ("macroscopic" vs. "microscopic" energy data) and distribution channel
("comprehensive data lake"). A data lake is not a data type; the Building Data Genome Project appears both as
microscopic energy data and as a data lake. The taxonomy is not compared with Malhotra et al. (2022), who
already published a taxonomic review of UBEM information, or with Goy et al. (2020) and Chen et al. (2019).
Reviewer 1 also asked that limitations and gaps be stated per category instead of hidden in a summary.

### P5. The review is not a review (major)
No search strings, databases, dates or PRISMA-style counts; "we will not review open data at the local level";
mostly U.S. federal sources; many URLs instead of citations (both Urban Informatics reviewers raised this);
GIS/remote-sensing literature missing (Reviewer 1 named OSM and Scientific Data footprint datasets). The
"well-developed vs. underdeveloped" summary (Sect. 2.8) is an opinion with no indicator behind it.

### P6. Outdated (major, and worse every year)
Since 2023: ComStock/ResStock End-Use Load Profiles and annual releases on OEDI, Model America,
Buildings-900K, Overture Maps, Microsoft Global ML footprints with heights, Google Open Buildings 2.5D,
EUBUCCO, 3D-GloBFP, GlobalBuildingAtlas, CBECS 2018 consumption release, RECS 2020. On the method side:
open-weight LLMs, structured-output APIs, and an LLM schema-matching literature with benchmarks (Valentine,
ReMatch, Magneto, Jellyfish) that sets the evaluation bar. The co-authors' own SQLMorpher (IEEE BigData 2023)
and DataMorpher (ICDE 2025) are not cited.

### P7. Presentation (minor but cumulative)
Bold body text, long promotional sentences ("heralds a new era"), section numbering errors ("Section 3.3.1"
does not exist; "Section 5" for conclusions that are Section 4), typos ("Water Underground" for Weather
Underground; "AHSRAE"; "Targe schema"), web-page references, reference format not adapted to the journal.
Same title and abstract were resubmitted to six journals with minimal change.

### P8. Assets that are under-used
- Three expert surveys (NREL modelers) in the folder name concrete missing data: building-level end-use
  commercial data with metadata, residential setpoints from connected thermostats, insulation/window data by
  region, geographic crosswalks (tract to ZIP+4), annual technology baselines, AMI access. They support the gap
  analysis, but n = 3 and the survey was run for an internal proposal, so it cannot be presented as a study.
  Use it, if at all, as acknowledged expert input, and check consent before quoting anyone.
- The co-authors' tools (SQLMorpher/DataMorpher/TreeMorpher by Jia Zou's group) are natural baselines.

## 3. What a publishable version must show

1. A clear, testable research question, not three loosely connected deliverables.
2. A schema that is a real, versioned, machine-actionable artifact (classes, slots, enums, units, IRIs,
   mappings to existing standards), released with validators.
3. A reproducible evidence base: a catalog of open datasets coded with the schema, so the gap analysis is
   computed rather than asserted.
4. An evaluation that can fail: ground truth, metrics, baselines, ablations (with vs. without the schema's
   semantics), repeats, open-weight models that anyone can re-run, and an error analysis.
5. A downstream check that alignment errors matter (or do not) for a UBEM quantity.
6. Everything in the GitHub repository, with the paper's numbers regenerated by scripts.

See `docs/redesign.md` for the plan that does this.
