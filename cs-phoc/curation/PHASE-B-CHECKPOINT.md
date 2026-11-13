# CS-PHOC technical — Phase B Technical Review Checkpoint

**Date:** 2026-11-13  
**Review status:** SOURCE & TECHNICAL EVIDENCE COMPLETE; FAIRmorph USER ACCEPTED ATTRIBUTED ENGLISH DESCRIPTIONS; NO REGISTRY OR UPSTREAM APPROVAL  
**Source revision:** `us-amlr/cs-phoc@64f0b77e631c711c681306bbb56a7636ae91a471`

## Completed without extending the PoC

1. Inspected all 23 original CSV fields and documented meanings, provenance, open questions and proposed count semantics in [PHASE-B-SOURCE-FIELD-DEFINITIONS.md](PHASE-B-SOURCE-FIELD-DEFINITIONS.md).
2. Reconciled all ten source count fields against original CSV values and [source-baseline.json](../validation/source-baseline.json): 21,440 possible cells; 4,500 blank; 11,599 explicit zero; 5,341 positive; 16,940 recorded; sum 79,232.
3. Recorded contributor-reported successful independent generic Engine RUN/2, source SHA-256 object IDs, pipeline hash and `verify-project=verified`.
4. Recorded contributor-reported successful Polars **2.1.0** standalone regression: 21,440 unpivoted, 4,500 null, 16,940 filtered, 0 remaining null, 11,599 zeros, 5,341 positives, sum 79,232. `count_value` is `String` after unpivot and is strictly cast to `Int64` in the numeric validation.
5. Independently reviewed all 322 source event rows: observed `census_days = (end - start) + 1` for every row (303/18/1 records with values 1/2/3). This **disagrees with the upstream README's literal date-difference formula**; source behavior is verified, but scientific interpretation remains open.
6. Source domains: surveyed PST TRUE/FALSE = 214/108; programs USAMLR/INACH = 222/100; Core/PST count rows = 1,288/856; four scientific source names with 536 rows each. Zero unmatched `event_id` in counts; zero duplicate `count_id`.

## User acceptance and AI attribution (2026-11-13)

The FAIRmorph project user accepted the proposed source-field interpretation **including its documented limitations**, requesting that all descriptions and formats be in English and clearly attributed as **"AI Description — added by FAIRmorph"**. This text was produced in the FAIRmorph PoC test scenario, **not** by the CS-PHOC dataset authors, owners, or maintainers. The complete English field-by-field interpretation and user decision are recorded in [PHASE-B-APPROVAL-PROPOSAL.md](PHASE-B-APPROVAL-PROPOSAL.md).

User acceptance is not an Engine registry `review_field(approved)` event and does not imply upstream scientific author endorsement.

## Scientific/contractual decisions remaining OPEN

- **SF-01:** FAIRmorph user acceptance of the 23 attributed descriptions is recorded; formal revision-bound Engine review, with identified reviewer and real revision IDs, remains open.
- **SF-02:** Source-README discrepancy is explicitly accepted as a caveat in the PoC description; upstream clarification or formal Engine field approval of the discrepancy between CSV date headers and upstream README names.
- **SF-03:** User accepted the observed inclusive-day interpretation with caveats; further source-author confirmation (if sought) and formal registry review that inclusive `census_days` describes intended sampling duration, not merely the source's observed calculation.
- **SF-04–SF-07:** Explicit approval of count unit, sampling scope, age/sex categories, `0`/blank semantics, and `total_count` treatment. Existing technical evidence supports but cannot approve these.
- **SF-08–SF-10:** Target event splitting, Occurrence vs MeasurementOrFact, relationships, external taxonomy mapping and target profile pins — deferred to Phase C; no implicit approval.
- **SF-11:** Formal, version-bound review record in Engine registry, only after decisions are made. No synthetic reviewer or approval event.

## Local environment identification — verified from contributor output (2026-11-13)

The contributor ran the requested read-only environment commands in the same local environment used for the preceding validation checks and reported:

```text
Python: 3.14.4 Polars: 2.1.0
c84b6f87585bab1237d6383cd3a47311f57250c2
64f0b77e631c711c681306bbb56a7636ae91a471
```

- Local **Python 3.14.4** and **Polars 2.1.0** are now explicitly identified. The earlier successful local RUN/2 and read-only Polars parser regression are documented in [PHASE-B-NULL-MISSING-EVIDENCE.md](PHASE-B-NULL-MISSING-EVIDENCE.md).
- Local Engine checkout is exactly the CI-pinned commit `c84b6f87585bab1237d6383cd3a47311f57250c2`.
- Local upstream checkout is exactly the expected source commit `64f0b77e631c711c681306bbb56a7636ae91a471`.
- The validation GitHub Actions workflow uses **Python 3.11**, so its green results and the local Python 3.14.4 result are evidence from **distinct interpreters**. Neither proves support for arbitrary runtime versions.
- This is contributor-reported command output, not an independently executed local environment inspection by the reviewer. No further local rerun is required for the existing Phase-B technical checkpoint.

**Remaining non-technical gate:** responsible scientific review and explicit revision-bound approval of field semantics, followed by separately reviewed target Entity/Relation mappings and scientific end-to-end sign-off. The local version report does **not** authorize those steps.

## Completion boundary

**Technical source review:** complete for this pinned PoC dataset and contributor-reported runtime.  
**FAIRmorph textual field-description acceptance:** recorded (English, labelled AI Description — added by FAIRmorph). **Engine SourceFieldDefinition revision approval:** not performed; identified reviewer and real revisions required.  
**Entity/relationship mappings and scientific publication sign-off:** not completed or registered.  
**Engine/Workbench:** unchanged.

This checkpoint is intentionally the smallest reproducible handover needed to finish the technical vertical PoC scientifically after human approvals. It is **not** a claim that all scientific validation phases have passed.
