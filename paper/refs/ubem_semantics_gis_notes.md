# Notes for ubem_semantics_gis.bib

Checked on 2026-11-12. "verified" means one of the following:
- the DOI resolved at `api.crossref.org/works/<doi>` and the title, authors, year and venue match the bib entry;
- for standards, W3C, OGC, ETSI and web resources, the official URL was fetched;
- for arXiv items, the arXiv API record was read.

Entries: 98 verified (84 with a Crossref-resolved DOI; 14 standards, websites or preprints checked at their official URL or on arXiv) and 5 UNVERIFIED or corrected items, listed at the end: 3 could not be verified (no record or not yet published) and 2 corrections.

Each line below gives the key, the status, and what the item contributes to a paper on (i) a faceted taxonomy of UBEM open data, (ii) a machine-actionable metadata schema, and (iii) an LLM schema-alignment benchmark.

---

## Most likely novelty threats (read first)

1. **zhang2023taxonomy** (arXiv 2311.08535, Zhang, Chen and Zou): **HIGHEST THREAT. This is your own preprint, so the overlap is with yourself.**
   - It already proposes three things:
     - a taxonomy of UBEM open-data types;
     - a semantic data schema for each category;
     - an LLM case study that processes three open datasets with that schema.
   - The journal paper must cite it explicitly and state what is new:
     - a faceted taxonomy rather than a single-axis category list;
     - a formal, validatable schema (e.g., LinkML, DCAT or schema.org mappings);
     - a quantitative alignment benchmark rather than a three-dataset demonstration.
   - Check the journal's policy on prior arXiv posting.
2. **malhotra2022information** (Building and Environment 208:108552): **HIGH.**
   - It is a "taxonomic review" of UBEM information modelling. It classifies input data formats, simulation tools, outputs and validation. It reports that about 95% of the studies it analysed were not reproducible and that interoperability is weak.
   - How it differs: its taxonomy classifies literature and workflow components. It does not describe datasets with facets, defines no machine-actionable metadata schema, and has no alignment benchmark.
   - Use it as the closest prior "taxonomy" and as motivation (reproducibility and interoperability gaps).
3. **wang2022data** (Building and Environment 217:109056) and **bishop2024review** (Clean Energy and Sustainability 2(4):10016): **HIGH to MEDIUM.**
   - Wang et al. classify UBEM inputs into geometric, non-geometric, weather and validation/calibration data, and assess their availability and cost.
   - Bishop et al. catalogue urban energy modelling data across seven domains: climate, geographic, building, transport, demographics, energy networks/consumption, and distributed energy resources. For each domain they list formats, sources, acquisition and bridging methods.
   - How they differ: both are one-level categorisations meant for people to read. Neither defines controlled vocabularies, required or optional metadata fields, validation rules, or a test of automated alignment. Bishop et al. themselves name "lack of coordination and standardisation" as the main barrier, which supports your motivation.
4. **agugiaro2018energy**, **nouvel2015development** and **agugiaro2025proposal / agugiaro2026further** (CityGML Energy ADE): **MEDIUM-HIGH.**
   - The Energy ADE is the existing standardised data model for UBEM inputs and outputs, and it is being revised toward version 3.0 in 2025-2026.
   - How it differs: it models building and energy objects at the instance level and is bound to CityGML geometry. It does not describe datasets for discovery or provenance at the level of DCAT or schema.org, and it does not cover non-CityGML open data (tabular benchmarking disclosures, meter data, weather files, stock-model outputs).
   - Your schema should map to the Energy ADE, not compete with it.
5. **allan2020linked** (eSim 2020, UES ontology) and **ma2024ontology** (Sustainable Cities and Society 106:105394): **MEDIUM.**
   - Allan et al. propose a linked-data Urban Energy Simulation ontology. It gives a standardised vocabulary for heterogeneous UBEM data and targets data availability, accuracy and traceability, inside the CESAR-P platform.
   - Ma et al. propose a Building Template Ontology and an Urban Building Ontology to fuse multi-domain data for UBEM.
   - How they differ: both are ontologies tied to one tool or workflow and describe simulation inputs. Neither offers a cross-source faceted taxonomy of open datasets, a reusable metadata profile, or an LLM alignment benchmark.

Runners-up:
- **jin2023review**: a catalogue and review of more than 190 open city-level building energy datasets; this is a dataset inventory with no schema.
- **lee2025metadata**: a metadata schema (a Brick extension) for virtual building models in digital twins, implemented in GPT-based applications. It operates at building and operations scale, not on UBEM open data.
- **pan2022semantic**: schema matching of building-energy data with pre-trained language models and active learning. It overlaps the alignment benchmark; the LLM/schema-matching agent should cover it.
- **choi2024gpt**: GPT-UBEM, an LLM used inside a data-driven UBEM.
- **colverd2026national**: the NEBULA national UBEM dataset, with documented sources and licences.

---

## A. UBEM reviews and data-focused UBEM papers

- `reinhart2016urban`: verified. Foundational UBEM review that frames the data-input, simulation and validation pipeline and names input-data acquisition as a core challenge.
- `ferrando2020urban`: verified. Reviews bottom-up physics-based UBEM tools, which defines the consumers (and their input formats) that a UBEM metadata schema must serve.
- `johari2020urban`: verified. State-of-the-art review of UBEM methods and future prospects, including data needs and limitations.
- `sola2018simulation`: verified. Note that the requested "Sola et al. 2020, simulation tools for UBEM review" is actually Energies 2018, 11(12):3269; it reviews tools for building urban-scale energy models.
- `sola2020multidomain`: verified. The 2020 Sola et al. review (Sustainable Cities and Society 54:101872) of multi-domain urban-scale energy modelling tools; probably the "2020" paper you intended.
- `ali2021review`: verified. Qualitative and quantitative review of UBEM approaches, methods and tools.
- `hong2020ten`: verified. "Ten questions" paper that names data availability, quality and standardisation as key UBEM challenges.
- `kamel2022systematic`: verified. Systematic review that explicitly tabulates UBEM tools and data sources.
- `goy2020data`: verified. Assesses how data availability shapes UBEM approach choice and replicability, and proposes ways to overcome availability barriers.
- `chen2017automatic`: verified. CityBES-related workflow (Chen, Hong and Piette, Applied Energy 205) that generates UBEMs automatically from city datasets.
- `chen2019development`: verified, with a correction. Energy and Buildings 183:252-265 is by Chen, Hong, **Luo and Hooper** (not Piette); it builds a standardised city buildings dataset for UBEM from heterogeneous city data.
- `malhotra2022information`: verified. **Novelty threat #2**: a taxonomic review of UBEM input data formats, tools and validation, reporting that most studies are not reproducible.
- `wang2022data`: verified. **Novelty threat #3**: reviews UBEM data acquisition, classifying inputs (geometric, non-geometric, weather, calibration) and assessing availability and cost.
- `cerezodavila2016modeling`: verified. The "Modeling Boston" workflow for generating and maintaining a UBEM from existing municipal geospatial datasets.
- `roth2020syncity`: verified. Builds a synthetic city of hourly building energy estimates from open data alone.
- `roth2020examining`: verified. Examines whether open data can benchmark city building energy use (data science and policy view).
- `nouvel2017influence`: verified. Quantifies how 3D city-model data quality affects urban heating-demand results; Nouvel's main data-quality paper.
- `prataviera2022evaluation`: verified. Uncertainty and sensitivity analysis of how UBEM input uncertainty propagates to results.
- `bass2022close`: verified. Shows that bias in building metadata (e.g., tax-assessor attributes) drives UBEM error against measured data.
- `hosseinihaghighi2022characterizing`: verified. Workflow that characterises, integrates and structures urban GIS data into CityGML for housing-stock UBEM; a data-structuring precedent.
- `jin2023review`: verified. Reviews more than 190 open datasets of city-level building energy use and their applications; the closest dataset inventory.
- `kong2023urban`: verified. Systematic review of UBEM challenges and opportunities (2023).
- `piro2023from`: verified. Reviews input data and modelling approaches from BEM to UBEM (Building Simulation 2023).
- `geske2023impact`: verified. Quantifies how different input datasets affect UBEM results for the German building stock.
- `salvalai2024from`: verified. Recent (2024) review of UBEM research trends and simulation tools.
- `bishop2024review`: verified. **Novelty threat #3**: reviews multi-domain urban energy modelling data across seven domains (formats, sources, acquisition, challenges); a categorisation, not a formal schema.
- `song2024developing`: verified. Builds UBEMs for Shanghai from multi-source open data; an example of an open-data UBEM pipeline.
- `ali2024urban`: verified. Releases synthetic urban residential building-stock datasets for energy analysis (Data in Brief).
- `choi2024gpt`: verified. GPT-based data-driven UBEM; relevant to the LLM framing (the other agent covers LLM literature).
- `choi2025multisource`: verified. Fuses multiple open and administrative data sources for UBEM; shows that data integration is a bottleneck.
- `hong2025ten`: verified. "Ten questions on building stock modeling" (2025), including data needs for stock models.
- `anselmo2026urban`: verified. 2026 review of GIS and remote-sensing integration in UBEM, including OSM and EUBUCCO; it links the energy and GIS literatures.
- `colverd2026national`: verified. NEBULA, a national neighbourhood-level UBEM dataset for England and Wales with documented sources and licences.
- `wilson2022enduse`: verified. NREL End-Use Load Profiles methodology, calibration, validation and uncertainty-quantification report (NREL/TP-5500-80889) behind ResStock and ComStock data.
- `parker2023comstock`: verified. ComStock Reference Documentation V.1 (NREL/TP-5500-83819), which documents commercial stock-model inputs and data sources.
- `present2024resstock`: verified. ResStock Dataset 2024.1 Documentation (NREL/TP-5500-88109), which documents residential stock-model data and outputs.
- `new2022model`: verified as a preprint only. "Model America" (ORNL; SSRN 2022) is a crude energy model and data for nearly every U.S. building; no peer-reviewed journal version was found.
- `zhang2023taxonomy`: verified (arXiv). **Novelty threat #1 (self-overlap)**: taxonomy, per-category semantic schema, and an LLM case study on three open datasets.

## B. Semantic and metadata standards

- `groger2012citygml`: verified. Canonical journal description of CityGML (2.0) semantic 3D city models.
- `ogc2012citygml`: verified (OGC 12-019, DOI 10.62973/12-019, published 2012-04-04). The CityGML 2.0 encoding standard itself.
- `kutzner2020citygml`: verified. Describes the CityGML 3.0 conceptual model and its new modules (versioning, dynamizers, and others).
- `ogc2021citygml3`: verified (OGC 20-010; approved 2021-06-04, published 2021-09-13). The CityGML 3.0 Part 1 conceptual model standard.
- `nouvel2015development`: verified. Building Simulation 2015 paper presenting development of the CityGML Energy ADE.
- `agugiaro2018energy`: verified. **Novelty threat #4**: the journal reference for the Energy ADE, a CityGML extension that standardises UBEM data.
- `agugiaro2019open`: verified. Book chapter on open data-modelling standards for city-wide energy simulation.
- `agugiaro2025proposal`: verified. 2025 proposal to update the Energy ADE; shows the standard is still evolving.
- `agugiaro2026further`: verified. 2026 further development toward Energy ADE 3.0.
- `ledoux2019cityjson`: verified. CityJSON, a compact JSON encoding of the CityGML data model and the developer-friendly target format.
- `bhattacharya2015short`: verified. Compares Haystack, IFC and SSN against real building metadata and finds that none covers it well; the "good, bad and ugly" paper.
- `balaji2016brick`: verified. Brick, the original BuildSys 2016 unified building metadata schema.
- `balaji2018brick`: verified. Applied Energy journal version of Brick for portable building applications.
- `luo2022extending`: verified. Brick extension for occupant metadata (Automation in Construction 139:104307).
- `pritoni2021metadata`: verified. Critical review and use-case analysis of building metadata schemas and ontologies (Brick, Haystack, 223P, BEDES, BuildingSync, among others); the best single citation for the building-scale schema landscape.
- `haystack4`: verified (official site; Haystack 4.0.0). Tagging-based semantic standard for building and IoT data.
- `hammar2019realestatecore`: verified. RealEstateCore ontology for real-estate and smart-building data (ISWC 2019).
- `rasmussen2021bot`: verified. BOT, the W3C LBD building topology ontology. Crossref dates it 2020-11-19 and places it in volume 12(1); the year is kept as 2021 with a note.
- `daniele2015saref`: verified. Original SAREF ontology paper (LNBIP 2015).
- `etsi2024saref`: verified (official ETSI SAREF portal). SAREF core, ETSI TS 103 264 V4.1.1 (2024).
- `etsi2025saref4bldg`: verified (official ETSI SAREF portal). SAREF4BLDG building extension, ETSI TS 103 410-3 V2.1.1 (2025).
- `long2021buildingsync`: verified. Peer-reviewed description of BuildingSync, a schema for commercial building audit data exchange.
- `buildingsync2025`: verified (official site). BuildingSync schema v2.7.0 (2025-09-26).
- `bedes`: verified (LBNL BEDES page). Building Energy Data Exchange Specification, a dictionary of building-energy terms that is a direct mapping target for a UBEM schema's vocabulary.
- `ashrae223p`: verified as a proposed standard; publication UNVERIFIED. ASHRAE 223P ("Semantic Data Model for Analytics and Automation Applications in Buildings") is still in public review; cite it as a proposed standard, not a published one.
- `w3c2024dcat3`: verified. DCAT version 3, a W3C Recommendation (22 August 2024) and the natural dataset-level vocabulary for catalogue metadata.
- `schemaorgDataset`: verified. The schema.org Dataset type (release V30.1), used for web discoverability (e.g., Google Dataset Search).
- `wilkinson2016fair`: verified. The FAIR Guiding Principles.
- `moxon2025linkml`: verified. The peer-reviewed LinkML paper (GigaScience 15:giaf152; online 2025-12-12; 2026 volume). The author list in the bib is abbreviated with "others".
- `qudt`: verified (official site). Units, quantity kinds and dimensions vocabulary for unit-aware schema fields.
- `w3c2009skos`: verified. SKOS Reference, a W3C Recommendation (18 August 2009), for encoding taxonomy facets as concept schemes.
- `w3c2017ssn`: verified. The SSN/SOSA W3C Recommendation (19 October 2017).
- `haller2019modular`: verified. Journal description of the modular SSN/SOSA ontology. Crossref dates it 2018-12-28 in volume 10(1); the year is kept as 2019.
- `janowicz2019sosa`: verified. SOSA lightweight ontology for sensors and observations (Journal of Web Semantics 56).
- `ogc2024geosparql`: verified (OGC 22-047r1, published 2024-01-29). The GeoSPARQL 1.1 standard.
- `car2022geosparql`: verified. Journal paper on the GeoSPARQL 1.1 update.
- `battle2012enabling`: verified. The original GeoSPARQL and Parliament paper (Semantic Web 3(4)).
- `corrado2015data`: verified. SEMANCO project data structuring for an urban energy-system ontology; an early urban energy ontology (2015, before the 2018-2026 window).
- `allan2020linked`: verified (IBPSA proceedings PDF; no DOI). **Novelty threat #5**: the UES linked-data ontology for UBEM data handling, aimed at availability, accuracy and traceability.
- `chadzynski2021semantic`: verified. Semantic 3D City Database: CityGML expressed as a dynamic geospatial knowledge graph (Cities Knowledge Graph, Energy and AI).
- `ma2024ontology`: verified. **Novelty threat #5**: ontology-driven UBEM with Building Template and Urban Building ontologies for multi-domain data fusion.
- `lygerakis2022knowledge`: verified. Review of knowledge-graph ontologies for building energy efficiency.
- `lee2025metadata`: verified. Metadata schema (Brick extension) for virtual building models in digital twins, implemented with GPT; a building-scale metadata-plus-LLM precedent.
- `pan2022semantic`: verified. Semantic-similarity and pre-trained language model schema matching for building energy data. It belongs to the LLM/schema-matching scope but threatens the benchmark claim, so flag it to that agent.

## C. GIS and remote-sensing building data

- `biljecki2015applications`: verified. State-of-the-art review of 3D city-model applications, including energy; the reviewer-requested GIS citation.
- `biljecki2022global`: verified. Global Building Morphology Indicators: open, computed building-morphology metrics at global scale.
- `heris2020rasterized`: verified. Rasterised U.S. building footprint dataset derived from Microsoft footprints (Scientific Data).
- `sirko2021continental`: verified (arXiv 2107.12283). Google Open Buildings: continental-scale building detection from satellite imagery.
- `milojevicdupont2023eubucco`: verified. EUBUCCO v0.1: an open, harmonised European building-stock database (more than 200 million buildings); a harmonisation precedent.
- `esch2022world`: verified. World Settlement Footprint 3D, a global 3D building-stock survey.
- `pesaresi2013global`: verified. The original GHSL concept paper (IEEE JSTARS).
- `pesaresi2024advances`: verified. Recent GHSL descriptor paper (International Journal of Digital Earth 2024) for the GHS-BUILT products.
- `haklay2008openstreetmap`: verified. Original OpenStreetMap description.
- `zhang2023carbon`: verified. Reviewer-suggested Nature Communications 14:2347 paper on rooftop PV carbon mitigation in China, built on building-rooftop remote-sensing data.
- `touzani2021open`: verified. Open data and deep semantic segmentation for building-footprint extraction (LBNL).
- `oostwegel2025footprints`: verified. Global semantic building-footprint dataset with GEM-taxonomy attributes (2025); a precedent for attaching a taxonomy to building data.

## D. Open data in science and open-data quality

- `reichman2011challenges`: verified. Challenges and opportunities of open data in ecology (Science 331:703-705).
- `vetro2016open`: verified. Open data quality measurement framework applied to open government data (Government Information Quarterly).
- `wang1996beyond`: verified. Classic data-quality dimensions framework ("fitness for use").
- `janssen2012benefits`: verified. Benefits, adoption barriers and myths of open government data.

---

## UNVERIFIED or corrected items

- **Nouvel et al. 2015, CISBAT (Energy ADE genesis paper)**: UNVERIFIED. No Crossref record or official URL was found. Cite `nouvel2015development` (Building Simulation 2015, DOI-verified) and `agugiaro2018energy` instead.
- **"Sola et al. 2020, Simulation tools to build urban-scale energy models: A review"**: CORRECTED. That title is Energies 2018 (`sola2018simulation`). The 2020 Sola paper is "Multi-domain urban-scale energy modelling tools: A review", Sustainable Cities and Society (`sola2020multidomain`).
- **"Chen, Hong & Piette 2019, Energy and Buildings 183:252-265"**: CORRECTED. The authors of that paper are Chen, Hong, Luo and Hooper (`chen2019development`). The Chen, Hong and Piette paper is Applied Energy 205 (2017) (`chen2017automatic`).
- **ASHRAE Standard 223 as a published standard**: UNVERIFIED. Only the proposed or public-review status could be confirmed (`ashrae223p`).
- **Model America journal article**: UNVERIFIED. Only the 2022 SSRN preprint exists in Crossref (`new2022model`).
