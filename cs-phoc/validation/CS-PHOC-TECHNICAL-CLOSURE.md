# CS-PHOC technical validation closure

**Checkpoint date:** 2026-11-13  
**Repository:** [FAIRmorph/fairmorph-validations](https://github.com/FAIRmorph/fairmorph-validations)  
**Outcome:** **Technical validation passed; scientific publication approval outstanding.**  
**Scope:** A bounded, reproducible, local-first **vertical proof of concept**, not a released publication workflow.

## 1. Pinned provenance and scope

- FAIRmorph Engine: `c84b6f87585bab1237d6383cd3a47311f57250c2`.
- Original CS-PHOC repository: `us-amlr/cs-phoc@64f0b77e631c711c681306bbb56a7636ae91a471`.
- Source events CSV SHA-256: `4362ae650cb72cc74901f7719920db5c8bbcfdc2ee09842595d04bf5e587bddc`.
- Source counts CSV SHA-256: `be4a28aa5036dea103e9e6bbc6af5fef13d80354ef2750e0960bf78e320c3545`.
- Source dataset DOI: https://doi.org/10.48361/gklk1u; methods paper: https://doi.org/10.1038/s41597-024-03744-9.
- No original CSVs, generated projects or full export files are committed to the validation repository.

## 2. Verified capabilities

| Phase | Evidence and technical outcome |
| --- | --- |
| **A — Source import and immutable generic RUN/2** | Two imported, checksum-pinned resources; 322 source survey windows, 2,144 source count rows; reproducible technical unpivot and event join; verified RUN/2 manifest and input objects. |
| **B — Field semantics** | 23 English descriptions accepted as bounded interpretations by the FAIRmorph project user; registered locally as schema-valid immutable **unreviewed** SourceFieldDefinition drafts (7 events fields, 16 counts fields). |
| **C.1 — Dataset-specific projection** | Explicit source-to-Event/Occurrence IDs, Core/PST site split, ten age/sex count categories and source identity checks. |
| **C.2 — Metadata and provenance** | English test metadata; source attribution, checksums, source RUN identity, provenance and publication limitations. |
| **C.3 — Test formats** | Local Event-core / Occurrence-extension Darwin Core Archive, UTF-8 tab-separated PANGAEA **preparation** file, and RFC 7946 GeoJSON site-event FeatureCollection. |
| **C.4 — Independent audit** | Independent read-only examination of existing export bytes, original source cells, exact IDs, zero/missing handling, site feature properties, ZIP contents and vendored DwC-A metadata XSD. |

All tests preserve the distinction between **recorded zero** and **unrecorded/missing source count cell**. Harmonization of the original dataset may itself have generated some zero values; the PoC **does not claim that every zero is a directly observed zero**. Neither the count sum nor the occurrence rows are an animal population estimate.

## 3. Baseline and export results

| Metric | Verified result |
| --- | ---: |
| Source survey windows | 322 |
| Source count rows | 2,144 |
| Site-specific Darwin Core Events | 536 (322 Core + 214 Punta San Telmo) |
| Nonblank source category cells / DwC-A Occurrences | 16,940 |
| PANGAEA-preparation TSV data rows | 16,940 |
| GeoJSON Point features | 536 |
| Explicit recorded zero category cells | 11,599 |
| Blank/unrecorded source category cells omitted | 4,500 |
| Positive recorded category cells | 5,341 |
| Count sum | 79,232 |
| Fixed targeted sample cases passing | 7 / 7 |
| Archive metadata XSD validation | Passed |

The seven targeted independently checked samples cover a positive pup count, a recorded zero, omitted blank count, a zero-total source row with a blank category, Punta San Telmo juvenile count, pups with all sexes combined, and an unknown age/sex recorded zero. The independent audit also compares **all 16,940** original recorded count cells against both corresponding exported tabular representations; it is not limited to those samples.

GeoJSON contains only **representative census site reference points**, not individual animal locations or surveyed polygons. Source-site coordinate uncertainty is carried as an explicit property. The PANGAEA TSV labels `pup_count` sex as **sexes combined**; the Darwin Core Occurrence sex field is empty, not biological `unknown sex`.

## 4. CI and locally reported validation evidence

The validation workflow uses pinned source and Engine revisions on Python 3.11 and performs the full source import, Phase B draft registration, three test exports and independent final content audit.

**Merged validation PR history:**

| PR | Scope | Squash merge commit |
| --- | --- | --- |
| [#1](https://github.com/FAIRmorph/fairmorph-validations/pull/1) | Phase B evidence and English AI-attributed field drafts | `5e71162a15f517e39266a687e11fe2ccbacee6ad` |
| [#2](https://github.com/FAIRmorph/fairmorph-validations/pull/2) | Engine count-unit token alignment | `0b1348f3b0c20f56612ea4fd2b5b7018cf8e0f8b` |
| [#3](https://github.com/FAIRmorph/fairmorph-validations/pull/3) | Local registration of 23 unreviewed field revisions | `eae3eece1c6c0d273babb81e17978c19ff05e34a` |
| [#4](https://github.com/FAIRmorph/fairmorph-validations/pull/4) | RUN-bound three-format test exports | `8e54778a3783f420deaa8b49229a801855ac8935` |
| [#5](https://github.com/FAIRmorph/fairmorph-validations/pull/5) | Independent final content and seven-case audit | `ae9a9f30e67041318d0089b20bdb98467eef79ce` |

The `main` branch's CI completed successfully for `ae9a9f30`: [Actions run 43456998642](https://github.com/FAIRmorph/fairmorph-validations/actions/runs/43456998642). The final audit implementation also passed both PR CI checks before merge.

**User-reported local checks (not a remotely uploaded audit-report body):**

- Phase B registration: `preflight_passed`, then `drafts_registered`, `field_count: 23`, `review_status: unreviewed`, `project_verified: verified`.
- C.1–C.4 export runner: `status: passed`, Event 536, Occurrence and PANGAEA 16,940, GeoJSON 536, count sum 79,232, `dwca_meta_xsd_validated: true`, `publication_ready: false`.
- Independent local final audit: `status: passed`, `checked_occurrences: 16940`, `sample_checks_passed: 7`.

The original per-file SHA-256 values for **that particular local export** remain in the user's local `validation-output/cs-phoc-c1-c4-test-exports/test-report.json`; the detailed local audit remains in `validation-output/cs-phoc-final-content-audit.json`. The user supplied successful command summaries, not the full reports or local archive bytes. Do not imply that the remote checkpoint itself independently opened the user's local files.

## 5. Scientific, semantic and publication limits

- **Field descriptions:** The 23 CS-PHOC-specific interpretations were prepared with AI assistance solely to accelerate the PoC and carry the provenance notice **“AI Description — added by FAIRmorph”**. They were accepted by the FAIRmorph project user as *bounded English draft descriptions*, including stated caveats. They were **not authored, reviewed, approved or endorsed by the original CS-PHOC authors/owners**.
- **Formal Engine reviews:** The actual 23 registered SourceFieldDefinition revisions remain `review_status: unreviewed` with `semantic_status: partially_defined`. No `review_field` approval, no identified reviewer event, and no approved scientific mapping are claimed. Project-user acceptance is not equivalent to Registry review.
- **Publication:** All three generated outputs are **TEST** artefacts, with `publication_ready: false`. The DwC-A ZIP has an Event core, an Occurrence extension and schema-validated `meta.xml` but **no publication EML**. The TSV is a **PANGAEA preparation**, not an accepted PANGAEA dataset. GeoJSON describes coarse, representative site-event locations, not precise seal observations.
- **Transformation status:** The CS-PHOC projection/export script and final audit are dataset-specific validation code in this repository; they are **not** evidence that the generic Engine's `export_dwca` adapter materially created these particular files. The existing technical RUN/2 does not provide independent Event/Occurrence publication tables needed by that generic adapter.
- **Scientific semantics:** Source blanks were omitted, explicit zeros retained, and `occurrenceStatus=absent` used for zero-count *category records* in the specific publication projection only. This does not prove species absence outside the documented census scope. The source pup-count category combines sexes.
- **Framework boundaries:** The FAIRmorph Engine and Workbench contain no AI runtime requirement and were not extended with CS-PHOC-specific scientific code. Future user interviews should collect and review human/source-documented semantics under existing Engine contracts, not require AI assistance.
- **External publication:** Formal scientific decisions, version-bound reviewed `defined` field semantics, final metadata, generic publication profiles and any required owner/publisher authorization remain separate future work.

## 6. Technical closure and future scope

**Closure:** The **technical CS-PHOC vertical proof of concept is complete and validated** for the pinned original revision and local test-export workflow. **No scientific publication sign-off is asserted.**

Keep the PoC bounded. Subsequent framework development should focus on existing contract-backed Workbench interviews for field semantics, reviewer decisions and mappings, then generic publication adapter wiring as a separate milestone. Do not expand this bounded PoC with unnecessary CS-PHOC special cases or permanent AI workflow features.

**Closure integrity:** This checkpoint records the status of PRs #1–#5 after merge. Their historical squash-merge commits and CI runs are permanent evidence; deletion of disposable merged review branch refs is a separate repository housekeeping action and does not affect the merged content.
