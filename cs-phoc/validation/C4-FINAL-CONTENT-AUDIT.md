# CS-PHOC technical — Final local test export content audit

**Status:** Independent, read-only PoC verification; test only, **not approved for publication**.  
**Language:** English (en).  
**Provenance:** **AI Description — added by FAIRmorph** refers to the historical CS-PHOC PoC descriptions, not to any AI capability in the Engine/Workbench. CS-PHOC source authors did not create or endorse these FAIRmorph-specific interpretations.

## Purpose

The C.1–C.4 exporter verifies its own expected counts and generates `test-report.json`. This **separate** auditor reads the **already generated** files and independently compares their content against immutable source objects and the pinned source/category mapping. No exports are regenerated, sent to a service, overwritten, or committed.

It checks:

- Source SHA-256, RUN manifest hash, 23 Phase B.4 evidence identities, and checksums of every exported file.
- Exactly 536 unique Darwin Core Events and 16,940 unique Occurrences, all source-derived IDs and event foreign keys.
- All **16,940** nonblank source cells in `Occurrence.csv` and `pangaea-test.tsv` (not a sample-only count check); 4,500 source blanks are absent from both, and 11,599 explicit zeros are retained.
- Exact status values `absent` for standardized zero categories versus `present` for positive categories; no extension of that rule to wider species absence.
- All 536 RFC 7946 site-event GeoJSON features: source location reference, event identity, `[longitude, latitude]`, species totals, aggregate sum and explicit text warning that coordinates are **representative, not individual animal locations**.
- ZIP members exactly match independently written Event/Occurrence CSV files and `meta.xml`; existing Engine DwC-A validation checks archive references against the official local TDWG XSD.

## Seven targeted source-grounded sample cases

| Test case | Source count ID | Category | Expected source value | Expected exported records |
|---|---|---|---:|---:|
| Positive pup | `1-1-344008` | `pup_count` | 1 | 1 |
| Explicit zero | `1-1-344008` | `ad_female_count` | 0 | 1 |
| Missing category | `1-1-344008` | `unk_female_count` | blank | 0 |
| Total=0 with missing category | `1-1-231417` | `unk_unk_count` | blank | 0 |
| Punta San Telmo juvenile | `1-2-231413` | `juv_male_count` | 11 | 1 |
| Pup sexes combined | `1-1-231413` | `pup_count` | 73 | 1 |
| Recorded unknown age/sex zero | `1-1-231413` | `unk_unk_count` | 0 | 1 |

For both pup samples, `Occurrence.sex` is intentionally empty and the PANGAEA-preparation TSV says **sexes combined**, not `unknown sex`. The source category itself does not determine sex.

## Reproduce against your actual local files

From the checked-out `fairmorph-validations` root, once the audit change is merged:

```bash
python scripts/audit_cs_phoc_test_exports.py \
  --project validation-output/cs-phoc-phase-b.fairmorph \
  --exports validation-output/cs-phoc-c1-c4-test-exports \
  --report validation-output/cs-phoc-final-content-audit.json
```

This command **does not modify** the project or the exported files. It creates only the small JSON audit report at a **new** output path. If the path already exists, select another name. Expected `status: passed`, `checked_occurrences: 16940`, `sample_checks_passed: 7`.

Do **not** commit the DwC-A ZIP, GeoJSON, TSV, imported source objects, project directory, or generated full outputs to public GitHub for this test. If project reporting is useful, share the small `cs-phoc-final-content-audit.json` report instead; it contains identifiers for seven examples but no full source data.

## Remaining limitations

- This audit verifies local formats, content and mappings for the **pinned** CS-PHOC revision. It does not assert full data-publication equivalence against the upstream publisher's archive.
- DwC-A ZIP contains **no EML** and is not a final archive for publication.
- The TSV is a **PANGAEA submission preparation table**, not an accepted or published PANGAEA dataset.
- The GeoJSON Points encode **location reference coordinates**, not tracking or per-observation animal coordinates.
- Formal Engine SourceFieldDefinition approval events and external dataset-owner endorsements have not been recorded. None are fabricated here.

CI repeats the audit independently on a newly built pinned-source project using Python 3.11 and retains only the small metadata/evidence artefacts, never the original data or the generated test exports.
