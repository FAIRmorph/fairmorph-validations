# FAIRmorph real-data validation criteria

This document gives the **general evaluation criteria** behind the reference case. It does not define scientific decisions, Engine contracts, or the sequence of a private project conversation. For the **actual CS-PHOC evidence and exact reproduction commands**, use the [reviewer guide](CS-PHOC-REPRODUCTION-AND-RESULTS.md).

## Three different claims need three different kinds of evidence

| Claim | Evidence required | Status for the pinned CS-PHOC test |
| --- | --- | --- |
| **Technical integrity** | Source byte identities, immutable project resources, reproducible Engine execution, verified RUN manifest and stable row-level values | **Passed** |
| **Dataset-specific transformation accuracy** | Source-supported mapping rules; every source value checked against the actual export files; keys, nulls, zeros, arithmetic, geometry and file format validation | **Passed as a bounded test projection** |
| **Scientific/publication approval** | Explicitly reviewed field semantics and mappings, responsible reviewer identity, version-pinned decisions, complete publication metadata and editorial/owner permissions when applicable | **Not granted; test exports only** |

A checksum or successful Engine RUN proves technical consistency, **not** scientific validity by itself. A validated archive `meta.xml` proves its technical structure, **not** that the data product has been accepted for publication.

## Required verification steps for a comparable new dataset

1. Identify **real external source data**, a fixed upstream revision, source licensing, known interpretation limits, and exact input byte hashes.
2. Derive **independent source-baseline expectations** before comparing with the Engine (counts, unique identifiers, missing/zero values and source relationships).
3. Run the **generic Engine** without embedding dataset-specific biological assumptions. Verify imported resource identities, pipeline declarations, source-to-result row-level consistency and immutable RUN artifacts.
4. Record source-field semantics with evidence and limitations. Keep **draft acceptance** separate from formal version-bound **review/approval**.
5. Document any **dataset-specific projection** with explicit target IDs, relationships, null/zero policy, coordinate meaning and provenance.
6. Audit actual exported **bytes and records** independently of the export code, using exact comparisons and targeted edge cases; record output checksums.
7. State which results belong to the **Engine**, which belong to the **validation harness**, and whether the **Workbench** was invoked.
8. Declare **publication readiness separately**, without inferring scientific endorsement or broader framework generality from a local passing test.

## Implementation boundary

The [FAIRmorph Engine](https://github.com/FAIRmorph/fairmorph-engine) owns generic runtime, contracts, data identities, registries and review events. The [FAIRmorph Workbench](https://github.com/FAIRmorph/fairmorph-workbench) owns its user interface. This repository owns external dataset-specific test configurations, source-derived expectations, independent validation scripts and concise evidence.

All generated FAIRmorph projects, imported original source objects, large output datasets and runtime credentials remain out of Git by default. Source license terms are described in [third-party notices](../THIRD-PARTY-NOTICES.md).

For the current dataset, the full audit passed but publication approval remains outstanding. See the [CS-PHOC interpretation and limitations](CS-PHOC-REPRODUCTION-AND-RESULTS.md#6-what-does-not-follow-from-a-pass).
