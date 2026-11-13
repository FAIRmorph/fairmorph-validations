# CS-PHOC Phase B — FAIRmorph AI Description and Source-Field Review

**Language:** English (en)  
**Description type:** **AI Description — added by FAIRmorph**  
**Attribution:** FAIRmorph test scenario; AI-assisted field descriptions and interpretation  
**Status:** USER-ACCEPTED FOR THE FAIRmorph PoC REVIEW; NOT AN UPSTREAM AUTHOR APPROVAL; NO ENGINE REGISTRY APPROVAL  
**Review recorded:** 2026-11-13  
**Source revision:** `us-amlr/cs-phoc@64f0b77e631c711c681306bbb56a7636ae91a471`

> **Attribution notice — mandatory for every field below:** The **AI Description — added by FAIRmorph** is an AI-assisted description prepared for FAIRmorph scientific proof-of-concept testing. It is **not text written, endorsed, approved or supplied by the CS-PHOC dataset authors, owners, or maintainers**. Original source values and upstream documentation remain unmodified. Source citations provide evidence, not authorship or endorsement of FAIRmorph's interpretations.

## 1. Source evidence (not description authorship)

- **[SRC]** [Upstream manuscript CSV field documentation](https://github.com/us-amlr/cs-phoc/blob/64f0b77e631c711c681306bbb56a7636ae91a471/data/manuscript/README.md)
- **[METHOD]** [Woodman et al. (2024), Scientific Data, DOI 10.1038/s41597-024-03744-9](https://doi.org/10.1038/s41597-024-03744-9)
- **[GEN]** [Upstream CSV-generation script](https://github.com/us-amlr/cs-phoc/blob/64f0b77e631c711c681306bbb56a7636ae91a471/R/manuscript_data.R)
- **[PUB]** [Upstream DwC-A projection script](https://github.com/us-amlr/cs-phoc/blob/64f0b77e631c711c681306bbb56a7636ae91a471/R/data_to_dwca.R)
- **[RAW]** [Events CSV](https://github.com/us-amlr/cs-phoc/blob/64f0b77e631c711c681306bbb56a7636ae91a471/data/manuscript/cs-phoc-events.csv) and [counts CSV](https://github.com/us-amlr/cs-phoc/blob/64f0b77e631c711c681306bbb56a7636ae91a471/data/manuscript/cs-phoc-counts.csv) at the pinned source revision
- **[TEST]** [FAIRmorph null/missing evidence](PHASE-B-NULL-MISSING-EVIDENCE.md) and [23-field review inventory](PHASE-B-SOURCE-FIELD-DEFINITIONS.md)

The original publication reports a different historical scope than this pinned later CSV revision (322 event rows). No cross-revision equivalence is assumed.

## 2. AI Description — added by FAIRmorph: 23 source fields

Each description in the following tables is **AI Description — added by FAIRmorph** (English, `en`). The source references are evidence, not authorization or endorsement by upstream owners. **Scope** is the original CSV field only, not a Darwin Core or FAIRmorph target-entity mapping.

### Events CSV (7 fields)

| Source field | AI Description — added by FAIRmorph | Qualification / evidence |
|---|---|---|
| `event_id` | Text identifier uniquely identifying one source survey window and linking count records to their survey context. | Distinct from published Darwin Core `eventID` [SRC, RAW, PUB]. |
| `season_name` | Original field-season designation as provided in the source dataset. | Preserve as text; do not infer a calendar year [SRC]. |
| `census_date_start` | First calendar date of the reported census survey window. | Actual CSV header; upstream field README uses `census_start_date` [RAW, SRC, GEN]. |
| `census_date_end` | Last calendar date of the reported census survey window. | Actual CSV header; upstream field README uses `census_end_date` [RAW, SRC, GEN]. |
| `census_days` | Number of calendar dates spanned by the reported survey window, counting both start and end dates. | Exactly `(end - start).days + 1` in all 322 pinned event rows; upstream README's unadjusted subtraction statement is inconsistent [RAW, TEST]. This describes observed source behavior, not confirmed survey-hours or field effort. |
| `surveyed_pst` | Boolean indicator that Punta San Telmo was surveyed during this source survey window. | `FALSE` does not imply animal absence [SRC, RAW, PUB]. |
| `research_program` | Label identifying the research program responsible for the survey window. | Source labels are `INACH` and `USAMLR`; not an individual reviewer or observer identity [SRC, RAW]. |

### Counts CSV — identifiers and context (6 fields)

| Source field | AI Description — added by FAIRmorph | Qualification / evidence |
|---|---|---|
| `count_id` | Unique source identifier for one standardized count record. | Text token; not a Darwin Core `occurrenceID` [SRC, RAW, PUB]. |
| `event_id` | Reference to the source survey-window identifier in the events CSV. | A technically validated `m:1` source join, not an approved semantic entity relation [SRC, TEST]. |
| `location` | Original source location-group label associated with this count record. | Core census locations represent an aggregated group, not a single point location; Punta San Telmo is a separate group [SRC, METHOD, GEN]. |
| `species` | Scientific species name as written in the original standardized source CSV. | Does not assert a current WoRMS accepted taxon identifier [SRC, PUB]. |
| `species_common` | Common species name as written in the original standardized source CSV. | No additional vernacular-name normalization or language conversion is claimed [SRC]. |
| `total_count` | Source-provided aggregate total across the ten component count categories for the corresponding survey window, location group and species. | Calculated source field, **not** an independent eleventh count; missing component values remain distinguishable from zero [SRC, RAW, TEST, GEN]. |

### Counts CSV — recorded count categories (10 fields)

The shared count semantics in §3 apply to **every** field below; category labels specify how the aggregate count is partitioned.

| Source field | AI Description — added by FAIRmorph | Source evidence |
|---|---|---|
| `ad_female_count` | Aggregated number of adult female phocid individuals counted for this survey context. | [SRC, METHOD] |
| `ad_male_count` | Aggregated number of adult male phocid individuals counted for this survey context. | [SRC, METHOD] |
| `ad_unk_count` | Aggregated number of adult phocid individuals whose sex was not determined for this survey context. | [SRC] |
| `juv_female_count` | Aggregated number of juvenile female phocid individuals counted for this survey context. | [SRC] |
| `juv_male_count` | Aggregated number of juvenile male phocid individuals counted for this survey context. | [SRC] |
| `juv_unk_count` | Aggregated number of juvenile phocid individuals whose sex was not determined for this survey context. | [SRC] |
| `pup_count` | Aggregated number of pups (less than one year old), with sexes combined rather than individually classified in this source field. | [SRC, METHOD, GEN]; **all sexes combined** must not be equated to **unknown sex**. |
| `unk_female_count` | Aggregated number of female phocid individuals whose age class was not determined for this survey context. | [SRC] |
| `unk_male_count` | Aggregated number of male phocid individuals whose age class was not determined for this survey context. | [SRC] |
| `unk_unk_count` | Aggregated number of phocid individuals for which both age class and sex were not determined. | [SRC] |

## 3. AI Description — added by FAIRmorph: shared count value semantics

**Proposed standardized source semantics accepted for FAIRmorph PoC review:**

- **Counting unit:** individual phocid animals; nonnegative integers in the pinned source.
- **Sampling scope:** animals counted while hauled out in the surveyed land areas, not an estimate of the whole population or animals at sea.
- **Aggregation:** source survey window × source location group × source species × listed age/sex category. Counts may have been aggregated or completed during standardized dataset preparation.
- **Explicit `0`:** a recorded zero count value **in the standardized published CSV** for that category; some zeros were introduced through documented harmonization or completion and need not have been directly written down as zero during field work [METHOD, GEN].
- **Blank cell:** no count value recorded for that category, distinct from the numeric value `0`; do not impute blanks as zeros [SRC, RAW, TEST].
- **`total_count`:** a source-supplied derived sum, not an additional independent measurement.
- **Limits:** these source field descriptions alone do not establish absence outside the surveyed space/time, abundance, detectability, or population trends.

For an eventual Engine `SourceFieldDefinition`, the existing schema can represent provenance using `definition_source = "suggested"` for the AI-generated description plus explicit `evidence_refs`; `notes` should include **"AI Description — added by FAIRmorph; FAIRmorph PoC interpretation, not authored or endorsed by CS-PHOC data owners."** Set `language = "en"`. This attribution must not be squeezed into or replace the original values. These are **instructions for later drafting**, not registrations or approved registry revisions.

## 4. User review decision and authorization boundary

**Decision reported in conversation on 2026-11-13:** The FAIRmorph project user explicitly agrees with the proposed source-field definitions **including the documented limitations**, with one mandatory condition: descriptions and formats must consistently be in English, labelled **"AI Description"** and marked **"added by FAIRmorph"**, making clear that the interpretive text originates in the FAIRmorph test scenario rather than from CS-PHOC authors or dataset owners.

**Recorded status:** `user_accepted_for_fairmorph_poc_review`. This is a documented project-user acceptance of the **textual, source-bounded interpretation**; it is **not** an assertion that any upstream data author approved these interpretations or that an identified scientific reviewer completed 23 immutable registry approval events.

The exact reviewer identity, authority, Engine-generated SourceFieldDefinition revision IDs, and actual approval events are **not recorded here and must not be fabricated**. The registry remains unchanged. No Entity/Relation/Occurrence/MeasurementOrFact profile or publication mapping is confirmed by this decision.

## 5. Remaining next gate (minimal v0.13 PoC scope)

1. Preserve this English-only, clearly attributed text and cited source evidence.
2. If registry field drafts are later requested, create 23 schema-valid draft records against actual imported resource IDs, retaining `language = "en"`, FAIRmorph AI attribution in `notes`, and source citations in `evidence_refs`.
3. Only an identified, authorized reviewer may carry out revision-bound formal approvals; no automatic conversion of user acceptance into `review_field(approved)`.
4. Evaluate target entity identity and relation mappings separately in Phase C.

**This document deliberately contains no SourceFieldDefinition registration, no scientific owner endorsement, and no FAIRmorph engine/workbench changes.**
