# CS-PHOC v0.13 — Phase B Technical Review Checkpoint

**Date:** 2026-11-13  
**Review status:** SOURCE & TECHNICAL EVIDENCE COMPLETE FOR THE PINNED PoC INPUTS; SCIENTIFIC APPROVAL NOT GRANTED  
**Source revision:** `us-amlr/cs-phoc@64f0b77e631c711c681306bbb56a7636ae91a471`

## Completed without extending the PoC

1. Inspected all 23 original CSV fields and documented meanings, provenance, open questions and proposed count semantics in [PHASE-B-SOURCE-FIELD-DEFINITIONS.md](PHASE-B-SOURCE-FIELD-DEFINITIONS.md).
2. Reconciled all ten source count fields against original CSV values and [source-baseline.json](../validation/source-baseline.json): 21,440 possible cells; 4,500 blank; 11,599 explicit zero; 5,341 positive; 16,940 recorded; sum 79,232.
3. Recorded contributor-reported successful independent generic Engine RUN/2, source SHA-256 object IDs, pipeline hash and `verify-project=verified`.
4. Recorded contributor-reported successful Polars **2.1.0** standalone regression: 21,440 unpivoted, 4,500 null, 16,940 filtered, 0 remaining null, 11,599 zeros, 5,341 positives, sum 79,232. `count_value` is `String` after unpivot and is strictly cast to `Int64` in the numeric validation.
5. Independently reviewed all 322 source event rows: observed `census_days = (end - start) + 1` for every row (303/18/1 records with values 1/2/3). This **disagrees with the upstream README's literal date-difference formula**; source behavior is verified, but scientific interpretation remains open.
6. Source domains: surveyed PST TRUE/FALSE = 214/108; programs USAMLR/INACH = 222/100; Core/PST count rows = 1,288/856; four scientific source names with 536 rows each. Zero unmatched `event_id` in counts; zero duplicate `count_id`.

## Scientific/contractual decisions remaining OPEN

- **SF-01:** Scientific review and approval of each of 23 field definitions, with named responsible reviewer and actual revision IDs.
- **SF-02:** Formal explanation/approval of the discrepancy between CSV date headers and upstream README names.
- **SF-03:** Scientific confirmation that inclusive `census_days` describes intended sampling duration, not merely the source's observed calculation.
- **SF-04–SF-07:** Explicit approval of count unit, sampling scope, age/sex categories, `0`/blank semantics, and `total_count` treatment. Existing technical evidence supports but cannot approve these.
- **SF-08–SF-10:** Target event splitting, Occurrence vs MeasurementOrFact, relationships, external taxonomy mapping and target profile pins — deferred to Phase C; no implicit approval.
- **SF-11:** Formal, version-bound review record in Engine registry, only after decisions are made. No synthetic reviewer or approval event.

## Minimal local completion gate

The previously executed `scripts/run_cs_phoc.py` is the authoritative PoC technical runner and already returned `status=passed` and `verified=verified`; **no repeat required merely to change documentation**. Before later scientific approval, capture these metadata from the same local environment (without modifying sources):

```bash
python -c 'import sys, polars as pl; print("Python:", sys.version.split()[0], "Polars:", pl.__version__)'
git -C dependencies/fairmorph-engine rev-parse HEAD
git -C dependencies/cs-phoc rev-parse HEAD
```

Expected upstream commit: `64f0b77e631c711c681306bbb56a7636ae91a471`. The Engine reference in validation CI is `c84b6f87585bab1237d6383cd3a47311f57250c2`; a different local Engine commit should be recorded, **not silently treated as equivalent**.

Only if additional runtime evidence is requested, use an entirely new output directory with `scripts/run_cs_phoc.py`, and retain the resulting limited JSON evidence outside Git. Do not copy original CSVs or generated full projects into the validation repository.

## Completion boundary

**Technical source review:** complete for this pinned PoC dataset and contributor-reported runtime.  
**Scientific SourceFieldDefinition approval:** not complete; explicit accountable reviewer required.  
**Entity/relationship mappings and scientific publication sign-off:** not completed or registered.  
**Engine/Workbench:** unchanged.

This checkpoint is intentionally the smallest reproducible handover needed to finish the v0.13 vertical PoC scientifically after human approvals. It is **not** a claim that all scientific validation phases have passed.
