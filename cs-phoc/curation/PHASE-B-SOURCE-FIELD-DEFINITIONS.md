# CS-PHOC Phase B.2 — Source Field Definition Review Draft

**Status:** DRAFT / UNREVIEWED / NOT SCIENTIFICALLY APPROVED  
**Date:** 2026-11-13  
**Scope:** All 23 original CSV columns (7 events + 16 counts)  
**Source revision:** `us-amlr/cs-phoc@64f0b77e631c711c681306bbb56a7636ae91a471`  
**Source identity:** events Git blob `d129fa00d10fa11caf5f2f0481681ea5c22cb8a6`; counts Git blob `d81e36792cad4de0108f7d0bcd0cef4e89d103a0`

## 1. Authoritative references and evidence grades

- **SRC:** [Upstream manuscript CSV README](https://github.com/us-amlr/cs-phoc/blob/64f0b77e631c711c681306bbb56a7636ae91a471/data/manuscript/README.md)
- **PUB:** [Upstream DwC-A conversion script](https://github.com/us-amlr/cs-phoc/blob/64f0b77e631c711c681306bbb56a7636ae91a471/R/data_to_dwca.R)
- **RAW:** literal headers and tokens in the [events](https://github.com/us-amlr/cs-phoc/blob/64f0b77e631c711c681306bbb56a7636ae91a471/data/manuscript/cs-phoc-events.csv) and [counts](https://github.com/us-amlr/cs-phoc/blob/64f0b77e631c711c681306bbb56a7636ae91a471/data/manuscript/cs-phoc-counts.csv) CSVs
- **TEST:** [Phase B null/missing evidence](PHASE-B-NULL-MISSING-EVIDENCE.md), incl. successful locally reported RUN/2 and Polars 2.1.0 parser checks
- **ENGINE:** [Executable SourceFieldDefinition.schema.json](https://github.com/FAIRmorph/fairmorph-engine/blob/main/src/fairmorph_engine/contracts/SourceFieldDefinition.schema.json), plus [core/registry.py](https://github.com/FAIRmorph/fairmorph-engine/blob/main/src/fairmorph_engine/core/registry.py)

**Reading guide:** A statement supported by SRC, PUB, RAW or TEST is a **documented fact** about the source or pipeline, **not** an approved FAIRmorph scientific interpretation. Every field still requires a separate explicit review event. Missing/zero entries for context fields must not inherit count-field semantics.

## 2. Proposed fields — events.csv (7)

| Field (literal CSV header) | Source-supported meaning / evidence | Source representation and semantic open issues |
|---|---|---|
| `event_id` | Unique source survey-window key; join to counts via `event_id` [SRC, RAW] | Identifier **text**, even if tokens look numeric; not automatically DwC `eventID`; validate one-to-many count references |
| `season_name` | Field-season name (e.g. `2016/17`) [SRC] | Text; acceptable domain/format and time-zone/season convention need review |
| `census_date_start` | Start date of census window [RAW, PUB] | Actual CSV header differs from SRC's `census_start_date`; date parsing/time precision require confirmation; do not silently alias |
| `census_date_end` | End date of census window [RAW, PUB] | Actual CSV header differs from SRC's `census_end_date`; date parsing/time precision require confirmation |
| `census_days` | Census duration in days [SRC, PUB] | Integer-like source token; SRC describes difference between dates, while PUB uses `sampleSizeValue` and `<=1` for days labeling; one-day same-start/end examples merit explicit inclusive/derived-duration review |
| `surveyed_pst` | Whether Punta San Telmo was surveyed during window [SRC, PUB] | Literal CSV tokens `TRUE`/`FALSE` [RAW]; Boolean interpretation documented; no inference that FALSE proves absence of animals |
| `research_program` | Surveying program `INACH` or `USAMLR` [SRC] | Text category; authority, full program names and possible future codes require confirmation |

**Observed source context:** 322 event rows, 322 unique event IDs, no blank event CSV tokens in the pinned source [TEST]. Never generalize this to other datasets. The sample survey window is distinct from any location-split publication events.

## 3. Proposed fields — counts.csv identity / context (6)

| Field | Source-supported meaning / evidence | Source representation and semantic open issues |
|---|---|---|
| `count_id` | Unique count source-row key [SRC, RAW] | Text identifier; **not** DwC `occurrenceID`; preserve entire token including hyphens and leading zeros, if any |
| `event_id` | Foreign key to source survey-window `events.event_id` [SRC, RAW] | Text identifier; source join is `m:1` with zero unmatched in reference baseline, not a scientifically approved Entity relation |
| `location` | Cape Shirreff count location [SRC, RAW] | Source text labels incl. `Core census locations` and `Punta San Telmo`; whether/how linked to split sampling events requires separate mapping |
| `species` | Original scientific name [SRC] | Original text, not automatically accepted taxon ID; WoRMS enrichment is a separate sourced decision [PUB] |
| `species_common` | Original common name [SRC] | Text; language and authoritative name mapping not established |
| `total_count` | Original calculated sum of ten component count fields [SRC] | Integer source token, NOT an independent 11th measured count; confirm aggregation of blanks and whether sum 0 can coexist with unrecorded subcategories [RAW, TEST] |

**Constraint:** The primary raw CSV contains **16 count-table fields** including the ten component count columns. `count_type` and `count_value` are generated DAG outputs and **not** additional original SourceFields.

## 4. Proposed fields — ten explicit count columns

All ten are source-described as **aggregated count of individual animals** for the corresponding survey window/location/species [SRC]. Source literals are empty or nonnegative integer tokens in the pinned CSV [RAW, TEST]. **Proposed** `counting_unit = "individuals"`, `aggregation_level = "survey window × source location × source species × age/sex category"`; approve only after responsible scientific review. No method, repeat-count exclusion, detection probability or sampling effort can be inferred from these tokens.

| Field | Documented category | Blank | Explicit zero | Positive | Individual review open |
|---|---|---:|---:|---:|---|
| `ad_female_count` | adult / female | 0 | 942 | 1,202 | Confirm age/sex protocol |
| `ad_male_count` | adult / male | 0 | 1,397 | 747 | Confirm age/sex protocol |
| `ad_unk_count` | adult / unknown sex | 254 | 1,554 | 336 | Distinguish unknown from not surveyed |
| `juv_female_count` | juvenile / female | 130 | 1,176 | 838 | Confirm juvenile classification |
| `juv_male_count` | juvenile / male | 130 | 1,112 | 902 | Confirm juvenile classification |
| `juv_unk_count` | juvenile / unknown sex | 284 | 1,247 | 613 | Confirm unknown category |
| `pup_count` | pup under one year / any sex | 200 | 1,598 | 346 | Any sex is **not** unknown sex; PUB maps to `pup_unk_count` for its own projection |
| `unk_female_count` | unknown age / female | 1,396 | 742 | 6 | Unknown age not the same as `juvenile` |
| `unk_male_count` | unknown age / male | 1,396 | 746 | 2 | Unknown age not the same as `juvenile` |
| `unk_unk_count` | unknown age / unknown sex | 710 | 1,085 | 349 | Both classifications unknown |

**Common proposed `value_semantics` for each count field:**
- `missing_values: [{"token":"","meaning":"No count data recorded for this specific category; not a recorded zero"}]` [SRC, RAW, TEST].
- `zero_meaning: "true_zero"` **as a review candidate** for a performed count yielding zero individuals in that category [SRC]; do not silently substitute `absence` at an Occurrence or taxon level. PUB independently maps `individualCount == 0` to `occurrenceStatus = "absent"`, a **separate** publication rule.
- `zero_explanation`: "Explicit 0 is a recorded zero count for this source count category; it does not establish that other blank categories were surveyed."
- No additional missing token beyond the observed blank is asserted.
- Data type validation: strict `Int64` conversion of retained Long count values succeeded in the contributor's Polars **2.1.0** test. Long `count_value` is `String` after `unpivot`; downstream numeric inspection must cast explicitly [TEST]. This is technical evidence, not itself a semantic contract field.

**Count evidence cross-check:** 2,144 source count rows × 10 categories = 21,440 candidate cells; 4,500 blanks; 11,599 explicit zeros; 5,341 positives; 16,940 nonblank values; sum 79,232; no `total_count` mismatch when unrecorded components are excluded [TEST].

## 5. Actual Engine schema alignment (no registration yet)

The executable [SourceFieldDefinition v1.0.0 contract](https://github.com/FAIRmorph/fairmorph-engine/blob/main/src/fairmorph_engine/contracts/SourceFieldDefinition.schema.json) requires:
`contract_version`, `dataset_id`, `source_resource_id`, `source_field_id`, `field_locator`, `semantic_status`, `review_status`, `definition_source`, `description` and `value_semantics`. It supports `counting_unit`, `unit`, `aggregation_level`, `evidence_refs`, `notes`, etc.; `additionalProperties: false` means arbitrary proposed keys must **not** be inserted into a Contract.

For each of the **23 field instances** in a real FAIRmorph project, `define_field(project, resource_id, locator, definition)` constructs and checks dataset/resource/field IDs, column locators and canonical versioned content. An **unreviewed** draft should keep `review_status = "unreviewed"`; use `semantic_status = "partially_defined"` or `"unresolved"` for the remaining questions. Documented source provenance can use `definition_source = "source_documentation"`; source-supported statements and proposals must be distinguished in `description`/`notes`.

**Crucial:** `semantic_status = "defined"` must not be equated with approval. Scientific review is an explicit, separate revision-bound event (`review_field`), and approval requires substantive descriptions and complete semantics. Do not invent `reviewer_id`, `reviewed_at`, project identifiers, schema SHA-256 pins, or an approved mapping. The CSV file and registry source identities are different from count/entity projection identities.

This document is intentionally **not** a schema-valid 23-object payload; the Engine will supply project-specific identities when individual drafts are instantiated in a project. No such instantiation is authorized by this review.

## 6. Open decision register / required approval evidence

| ID | Decision requiring explicit scientific review | Suggested evidence | Status |
|---|---|---|---|
| SF-01 | Confirm each of 23 field definitions and source reference | Upstream SRC/RAW + reviewer decision per field | OPEN |
| SF-02 | Resolve documented vs actual date header discrepancy | Manuscript, source author clarification or version-pinned review rationale | OPEN |
| SF-03 | Define `census_days` precisely (inclusive days vs date difference) | Raw examples and calculation or author review | OPEN |
| SF-04 | Approve count unit, sampling scope and aggregation level | Study methods/source publication | OPEN |
| SF-05 | Approve explicit zero and blank count semantics | SRC + standalone Polars/Engine evidence + reviewer | OPEN |
| SF-06 | Confirm complete category age/sex rules, especially pup and `unk_*` | Study methods and PUB mapping rules | OPEN |
| SF-07 | Confirm how `total_count` treats blanks without materializing false zeros | SRC + source row examples + reviewer | OPEN |
| SF-08 | Define Survey Window vs split publication SamplingEvents and identifier provenance | PUB + mapping review | OPEN (later Phase C) |
| SF-09 | Select Occurrence vs MeasurementOrFact and relationships | Explicit target schema and scientific justification | OPEN (later Phase C) |
| SF-10 | Pin taxonomic enrichment reference, version and publication provenance | PUB, WoRMS evidence if used | OPEN (later Phase C/D) |
| SF-11 | Confirm reviewer, revision, and contractual schema pins | Formal registry approval event after review | OPEN |

## 7. Gate to actual SourceFieldDefinition draft registration

1. Independently check any unclear source semantics and record unresolved distinctions rather than inventing defaults.
2. Have a responsible reviewer assess the field definitions individually; approval must be explicit and revision-bound.
3. In a real FAIRmorph project, derive field IDs from the Engine, point locators at **actual** CSV headers and bind the existing immutable imported resources.
4. Create *unreviewed* definition revisions only when project-specific registration is deliberately authorized; this review file alone does not instantiate registry records.
5. Keep entity/profile/relation mappings separate and unapproved until Phase C.

**No scientific sign-off, Engine change, Workbench change, source-file change or registry write was performed by this document.**
