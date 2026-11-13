# FAIRmorph Validations

**What this repository is:** An independent, reproducible test of how the **FAIRmorph Engine v0.13 proof of concept** handles a real research dataset. It contains dataset-specific input declarations, checks, and evidence—not the FAIRmorph Engine or Workbench implementation, and not a released or approved scientific data product.

**Current result:** The pinned **CS-PHOC** test case passed the technical validation and export-content audit. The output is **test-only** (`publication_ready: false`). This result establishes technical correctness for this specific dataset and transformation; it does **not** establish formal scientific approval, general-purpose export support, or a completed Workbench workflow.

## Start here

- **[CS-PHOC: what was tested, what the results mean, and how to reproduce them](docs/CS-PHOC-REPRODUCTION-AND-RESULTS.md)** — the primary guide for external reviewers.
- [Original data and licensing](THIRD-PARTY-NOTICES.md).
- [GitHub Actions](https://github.com/FAIRmorph/fairmorph-validations/actions/workflows/cs-phoc-phase-a.yml) — automated run of the same test chain, with a small audit-report artifact.
- [Historical validation records](cs-phoc/validation/V0.13-VERTICAL-POC-CLOSURE.md) — detailed provenance and development checkpoint; not required to understand or reproduce the results.

## The actual research data vs. FAIRmorph

| Layer | Who provides it? | What is tested here? |
| --- | --- | --- |
| **Original CS-PHOC data** | The [US AMLR / CS-PHOC research project](https://github.com/us-amlr/cs-phoc) | Two pinned, unmodified source CSVs (322 survey-window records; 2,144 count records). |
| **FAIRmorph Engine** | [Generic Engine repository](https://github.com/FAIRmorph/fairmorph-engine) | Import, immutable project/source identities, a generic unpivot/filter/join pipeline, a verified RUN/2, and registration of 23 **unreviewed** field-definition drafts. |
| **Dataset-specific validation code** | **This repository** | A CS-PHOC-specific conversion of the verified counts into Event/Occurrence test rows, DwC-A, TSV and GeoJSON, plus independent checks of the resulting files. |
| **FAIRmorph Workbench** | [Separate UI repository](https://github.com/FAIRmorph/fairmorph-workbench) | **Not exercised** by this test. No claim that the UI can perform the complete workflow yet. |

### Results in plain language

The original tables contain **322** survey windows and **2,144** count records. Ten age/sex category columns give 21,440 possible cells: **16,940 contain a value** (including **11,599 explicit zeros**), and **4,500 are blank**. The count values sum to **79,232**; this is **not** an estimate of the seal population.

The tested publication-style transformation generates **536 location-specific event rows**, **16,940 category-level occurrence rows**, **16,940 TSV data rows**, and **536 GeoJSON features**. An independent auditor checks **every recorded category value** against both tabular exports, not just their aggregate totals, and also checks seven targeted edge cases. The DwC-A ZIP structure and its `meta.xml` pass validation using the Engine's existing TDWG archive validator.

**Interpretation matters:** A recorded zero stays zero; a blank cell is omitted. Some zeros may result from the upstream harmonization process, so they must not all be presented as directly observed absences. GeoJSON points are representative census-site locations, **not locations of individual animals**. The TSV is a PANGAEA **preparation**, not a submission or publication.

## Repository map

| Location | Contents |
| --- | --- |
| `scripts/run_cs_phoc.py` | Import original files, execute the generic Engine pipeline and verify RUN/2. |
| `scripts/register_cs_phoc_field_drafts.py` | Register 23 source-field **draft** definitions with the Engine; no review approvals. |
| `scripts/export_cs_phoc_test_formats.py` | Dataset-specific **test-only** DwC-A, TSV and GeoJSON generation with RUN/source cross-checking. |
| `scripts/audit_cs_phoc_test_exports.py` | Independent read-only audit of **already written** export files and seven source-grounded examples. |
| `cs-phoc/configurations/drafts/` | Technical pipeline template, metadata draft, 23 attributed field definitions, and the publication-style test projection. |
| `cs-phoc/validation/source-baseline.json` | Expectations measured independently from original source CSVs, **not** Engine results. |
| `cs-phoc/curation/` | Source interpretation, evidence, limitations and historical review notes. |
| `cs-phoc/validation/` | Detailed test/export specifications and historical checkpoint documents. |
| `.github/workflows/cs-phoc-phase-a.yml` | Full reproducibility test in CI (the historical filename does **not** limit it to the initial stage). |
| `docs/CS-PHOC-REPRODUCTION-AND-RESULTS.md` | Step-by-step reproduction, outcome interpretation, evidence and known limitations. |

## Reproduce

Requirements: **Python 3.11+**, Git, and access to the two public source repositories. Work from the root of this repository and use **new, nonexistent** local project and export directories. See the [full guide](docs/CS-PHOC-REPRODUCTION-AND-RESULTS.md) for exact pinned revisions and all commands.

```bash
# After cloning the pinned Engine and original CS-PHOC sources:
python scripts/run_cs_phoc.py --upstream dependencies/cs-phoc --project validation-output/cs-phoc.fairmorph
python scripts/register_cs_phoc_field_drafts.py --project validation-output/cs-phoc.fairmorph --apply
RUN_ID=$(python -c 'import json; print(json.load(open("artifacts/phase-a-result.json"))["run_id"])')
python scripts/export_cs_phoc_test_formats.py --project validation-output/cs-phoc.fairmorph --run-id "$RUN_ID" --output validation-output/cs-phoc-test-exports
python scripts/audit_cs_phoc_test_exports.py --project validation-output/cs-phoc.fairmorph --exports validation-output/cs-phoc-test-exports --report validation-output/cs-phoc-final-content-audit.json
```

Successful independent auditing reports `status: passed`, `checked_occurrences: 16940`, and `sample_checks_passed: 7`. **Do not confuse this with scientific review or publication approval.** CI regenerates its own project and does not publish the source data or full export files.

## Scientific and licensing boundaries

The 23 English field descriptions were prepared with AI assistance **only to accelerate this PoC**, are labelled **“AI Description — added by FAIRmorph”**, and are `unreviewed` Engine drafts. The original CS-PHOC authors/owners did **not** write, review, approve or endorse those additions. The Engine and Workbench do not require AI.

Original validation code and documentation use [Apache 2.0](LICENSE); upstream CS-PHOC materials retain their source [CC0 1.0](THIRD-PARTY-NOTICES.md) designation. Cite the original data and publication. Do not commit generated projects, source objects or bulk test exports.
