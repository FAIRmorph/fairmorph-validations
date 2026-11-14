# CS-PHOC: independent output content audit

**Result: passed for the pinned CS-PHOC technical test.** The independent auditor reads the **already generated** DwC-A, TSV and GeoJSON files and compares their contents with the original source objects and the verified Engine RUN. It **does not** regenerate exports, modify the project or establish scientific publication approval.

Start with the [validation results overview](README.md) or the [reproduction and interpretation guide](../../docs/CS-PHOC-REPRODUCTION-AND-RESULTS.md) if you need the source data, pinned revisions and commands.

## What was checked

- **Provenance:** The original input hashes, verified RUN manifest, source-field draft identities, projection checksums and individual output file checksums.
- **Record values:** All **16,940 nonblank source count-category cells** against both `Occurrence.csv` and `pangaea-test.tsv`. This is an exact comparison, **not just an aggregate-count test**.
- **Zeros and blanks:** **11,599 recorded zeros** remain numeric zeros; **4,500 blank source cells** do not become fabricated category records.
- **Identifiers and joins:** **536** distinct location-specific Events, **16,940** category Occurrences, appropriate source-derived IDs and valid Event references.
- **Spatial output:** All **536** GeoJSON features, representative site coordinates, longitude/latitude ordering, source-location links and uncertainty context.
- **Archive integrity:** ZIP member bytes, `Event.csv`, `Occurrence.csv` and `meta.xml`; TDWG DwC text metadata schema/reference checks through the existing Engine validator.

The sum of recorded category values is **79,232**. This is a consistency check of the source tables, **not a population estimate**.

## Seven targeted source examples

| Source case | Original count | Expected effect |
| --- | --- | --- |
| Positive `pup_count` | `1-1-344008`: 1 | One category record with count 1 |
| Recorded `ad_female_count` zero | `1-1-344008`: 0 | One category record with zero |
| Blank `unk_female_count` | `1-1-344008`: blank | No category record |
| Blank `unk_unk_count` with zero total | `1-1-231417`: blank | No category record |
| Punta San Telmo juvenile count | `1-2-231413`: 11 | Correct site-linked record |
| Combined-sex pup count | `1-1-231413`: 73 | Count 73; sex **not** “unknown” |
| Recorded `unk_unk_count` zero | `1-1-231413`: 0 | One category record with zero |

All **seven targeted examples passed**. For `pup_count`, the TSV represents sexes combined while DwC-A leaves `Occurrence.sex` empty. A zero-derived `occurrenceStatus=absent` is restricted to a **test category record**, not a general ecological absence claim.

## Reproduce the audit

From a fresh checkout, first follow the [complete reproduction procedure](../../docs/CS-PHOC-REPRODUCTION-AND-RESULTS.md). Once its export step has created the files, run:

```bash
python scripts/audit_cs_phoc_test_exports.py \
  --project validation-output/cs-phoc.fairmorph \
  --exports validation-output/cs-phoc-test-exports \
  --report validation-output/cs-phoc-final-content-audit.json
```

The report path must not already exist. The expected summary includes `status: passed`, `checked_occurrences: 16940` and `sample_checks_passed: 7`. The auditor writes only a **small new JSON report**, never the original source data or a replacement export.

## What this result does not establish

This audit covers the **pinned data revision and these dataset-specific test outputs**. It does not prove that every recorded zero was directly observed (some may reflect upstream harmonization), that GeoJSON points locate individual animals, or that the files were accepted by GBIF or PANGAEA. The archive contains **no publication EML**. The 23 field-description revisions remain `unreviewed`; original data authors have not approved FAIRmorph's added interpretations. The Workbench was not part of the test.

[Back to results](README.md) · [Test export formats](TEST-EXPORTS.md) · [Reproduction guide](../../docs/CS-PHOC-REPRODUCTION-AND-RESULTS.md)
