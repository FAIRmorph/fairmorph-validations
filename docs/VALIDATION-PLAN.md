# FAIRmorph v0.13 validation plan

## Purpose

Establish **separate, inspectable** evidence for (1) project integrity, (2) technical transformation correctness, and (3) approved scientific validity. The first two are necessary but not sufficient for the third.

## Phase A — source identity and technical regression

- Pin an upstream CS-PHOC revision and verify exact original Git object identities.
- Import the unchanged CSV files into a fresh FAIRmorph project. Record Engine-generated SHA-256 object identities.
- Register a technical-only DAG with actual resource IDs and use only existing operators.
- Unpivot ten source count fields, preserve explicit zero counts while excluding truly blank fields, join using `event_id` with checked `m:1` cardinality.
- Compare resulting row counts, unique source keys, explicit-zero counts and sums against `cs-phoc/validation/source-baseline.json`.
- Verify project and RUN/2 integrity through `verify-project`. Store evidence, but **do not** assert scientific approval.

A technical pass is required for subsequent phases.

## Phase B — source-field scientific review

- Check source descriptions, the accompanying publication and documented data-generation scripts.
- Review every relevant field: identity, measurement unit, domain, missing/zero meaning and provenance.
- Resolve any discrepancies between the source's documentation and actual CSV headers.
- Create versioned SourceFieldDefinitions; obtain explicit responsible-user approval.
- Treat all unsupported assumptions as open review findings. Never infer semantic identities from column names alone.

## Phase C — curated entity and relationship validation

- Determine the justified mappings to SamplingEvent and MeasurementOrFact, and evaluate if/how Occurrence is needed.
- Pin and approve exact schema IDs/versions/SHA-256 and mappings.
- Confirm cardinality, joins, relationships, sampling-window identity and any published event splitting rules.
- Test row-level reference cases, missing/zero semantics, sum invariants and value-change/audit expectations.
- Validate against an independently calculated reference, with explanation for every discrepancy.

## Phase D — scientific sign-off and reproducible evidence

- Record who reviewed which decisions, exact data/contract revision identifiers and acceptance criteria.
- Reproduce RUNs from frozen originals and approved declarations.
- Record expected-vs-observed summary, errors, scientific sign-off (when actually granted) and any limitations.
- Do not treat a successful RUN or hash verification as proof of scientific correctness.

## Repository boundaries

- Engine/Workbench repositories hold generic code and shared contracts.
- This repository holds dataset-specific test inputs, baseline values, validation procedures and evidence summaries.
- Generated FAIRmorph projects, original imported objects and full local RUN directories remain outside Git history by default. Commit only carefully selected evidence/manifests and approved contractual records, avoiding unintended redistribution.
- Source licensing is recorded per dataset in `THIRD-PARTY-NOTICES.md`.
