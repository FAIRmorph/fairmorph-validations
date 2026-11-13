# CS-PHOC C.1–C.4 — three local FAIRmorph test exports

**Status:** proposed, local test only — NOT FOR PUBLICATION.  
**Language:** English (en).  
**FAIRmorph description provenance:** **AI Description — added by FAIRmorph** for this PoC only. This language is not a permanent FAIRmorph feature. None of these derivative descriptions or mappings are attributed to or endorsed by CS-PHOC source authors.

## C.1 — Source-to-target mapping

The [pinned C.1–C.4 projection](../configurations/drafts/c1-c4-test-projection.json) declares two location identifiers (Core / Punta San Telmo), ten source count categories, source DOI and byte hashes. This is a dataset-specific test of the **published CS-PHOC Event-core / Occurrence-extension transformation**, not a new generic Engine mapping contract.

- 322 source survey windows become **536 location-specific Event records**: Core `event_id-1` for each window plus PST `event_id-2` only where `surveyed_pst=TRUE`.
- Ten recorded category values per source count may become individual Occurrence category records; blank source cells are omitted and explicit zero values retained.
- The publisher-style Occurrence ID is `count_id-age_code-sex_code` with stable code tables in the projection. `pup_count` covers **all sexes combined**, and an internal code `3` does not authorize a biological unknown-sex claim.
- The publisher's `individualCount=0 → occurrenceStatus=absent` rule is reproduced as a **category-record transformation only**, not evidence of wider species absence.
- No external taxonomy lookup, inferred individual organism identifiers, or population extrapolation is performed.
- Existing locally registered English field descriptions are referenced by their **Phase B.4 evidence**, but these are still `unreviewed` draft revisions. No formal Engine mapping approval is implied.

## C.2 — Metadata and reproducibility

The output contains a separate `test-metadata.json` with source/method DOI, source commit, explicit FAIRmorph derivative attribution, caveats, coordinate meaning and format limitations. `test-report.json` captures source file SHA-256, verified RUN manifest SHA-256, Phase B.4 evidence SHA-256, projection SHA-256, row counts, key checks, ZIP/XSD checks and output file checksums.

**No original publisher EML is copied or impersonated.** The first test DwC-A is an Event/Occurrence ZIP with `meta.xml`, without a publication EML file. A later publication-ready EML must use the Engine's validated EML adapter with explicit metadata and responsible approval.

## C.3 — Outputs

Produced in a **new** output directory outside Git:

| File | Test purpose |
|---|---|
| `cs-phoc-test.dwca.zip` | DwC-A ZIP with Event core and Occurrence extension |
| `Event.csv`, `Occurrence.csv`, `meta.xml` | Inspectable components of the ZIP |
| `pangaea-test.tsv` | English UTF-8 tab-separated **PANGAEA submission preparation**, not a published/curated PANGAEA dataset |
| `site-events.geojson` | RFC 7946 `FeatureCollection`: 536 site-event Point features with species totals |
| `test-metadata.json`, `test-report.json` | Explicit source / FAIRmorph provenance and technical evidence |

PANGAEA's official author guidance prefers UTF-8 tab-delimited tables with contextual metadata, and submission undergoes editorial review; this test file has not been submitted: https://wiki.pangaea.de/wiki/Ticket_System and https://pangaea.de/submit/.

GeoJSON uses longitude–latitude WGS84 position order under RFC 7946: https://www.rfc-editor.org/rfc/rfc7946.html. Site coordinates are **representative published location points** from the source DwC-A projection, not animal tracking coordinates or site polygons. Their source coordinate uncertainty is recorded as a property.

## C.4 — Validation gates

Before writing output, `scripts/export_cs_phoc_test_formats.py`:

1. Confirms the existing FAIRmorph project, two original source byte hashes and 23 bound Phase B.4 field draft identities.
2. Verifies an unchanged immutable generic RUN/2 with Engine `verified_run()`.
3. Compares every recorded source category **cell-by-cell** against `counts_with_events.parquet`, including count, source record, event, location, species and category.
4. Checks Event/Occurrence ID uniqueness and foreign keys, `total_count` per source row, source census dates, expected 536/16,940 record counts, 11,599 recorded zero values and 79,232 sum.
5. Checks TSV row counts, RFC 7946 coordinate ranges, GeoJSON feature count and aggregate total.
6. Validates `meta.xml` against the official vendored TDWG DwC text XSD using the **existing Engine `validate_dwca_archive()`**, including referenced ZIP members.
7. Writes a SHA-256-pinned test report with `publication_ready: false`.

This is intentionally **not** a claim that the Engine's generic `export_dwca()` produced the archive. That adapter expects previously materialized Event/Occurrence RUN artifacts and separate projection/integrity declarations, which the existing verified technical CS-PHOC RUN does not yet include. The PoC-specific adapter is kept outside the Engine.

## Local run

From the root of `fairmorph-validations`, after checking out the latest `main` once this review PR is merged, use the **existing Phase B.4 project**.

```bash
python scripts/export_cs_phoc_test_formats.py \
  --project validation-output/cs-phoc-phase-b.fairmorph \
  --run-id 20261113T135729Z-3eb02546db55 \
  --output validation-output/cs-phoc-c1-c4-test-exports
```

The run ID above is the previously reported local technical RUN/2 ID. If the project is different, use **that project's real RUN/2 ID** instead. `--output` must not exist; use a new directory on every repeat. No input is modified.

Expected output: `status=passed`, Event=536, Occurrence=16,940, PANGAEA TSV rows=16,940, GeoJSON features=536, count sum=79,232, explicit zeros=11,599, `dwca_meta_xsd_validated=true`, `publication_ready=false`.

The CI workflow independently recreates a new project from the pinned sources, registers the field drafts as unreviewed, creates the three test outputs and checks the metrics on Python 3.11. It does **not** upload source data or publication exports as GitHub artifacts.

## What remains for a formal publisher-grade export

Approve the finalized mapping and appropriate entity relationships through the Engine's existing revision-bound review flow; create RUN-pinned publication projection tables; provide complete EML/PANGAEA editorial metadata, appropriately reviewed taxonomic and coordinate decisions; and obtain the relevant dataset-owner/publication authorizations. These are **not** prerequisites for local TEST files and are outside this C.1–C.4 PoC validation scope.
