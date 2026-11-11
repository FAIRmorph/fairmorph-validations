# CS-PHOC validation reference (FAIRmorph v0.13)

This directory contains **portable, unapproved project inputs** and source-derived expectations. It is not itself an initialized FAIRmorph project and contains no original CSV files.

## Source

Pinned upstream: https://github.com/us-amlr/cs-phoc/tree/64f0b77e631c711c681306bbb56a7636ae91a471

Source CSVs:
- `data/manuscript/cs-phoc-events.csv`: 322 event rows
- `data/manuscript/cs-phoc-counts.csv`: 2,144 count rows

Upstream license: **CC0 1.0 Universal**. See [third-party notices](../THIRD-PARTY-NOTICES.md) for attribution and licensing.

## Technical files

- `configurations/drafts/pipeline-technical.json`: generic `fairmorph.pipeline/1` DAG; original source resource IDs are **placeholders** and must be replaced with actual Engine-imported IDs before registration.
- `configurations/drafts/dataset-metadata.json`: an **unapproved** dataset metadata draft.
- `validation/source-baseline.json`: measured expectations from the pinned upstream CSV files, not results from an Engine RUN.
- `curation/FIELD-REVIEW.md`: source-grounded field descriptions and unanswered scientific questions, **not** approved SourceFieldDefinition revisions.

Technical DAG stages: `table.unpivot/1` ten count columns, `table.filter/1` null exclusion while preserving explicit zeros, and `table.join/1` to events with `m:1` on `event_id`.

Expected baseline: 322 events; 2,144 counts; 16,940 nonblank long-count rows; 11,599 explicit zero cells; 4,500 blank source count cells; count sum 79,232. See JSON baseline for details.

## Execute independently

Follow the [root README](../README.md). The runner imports the pinned originals into a **new** local project, registers the technical DAG, executes a RUN/2 and verifies the generated project; it does not approve scientific semantics.

## Scientific scope

Before a scientific entity projection: review field meanings with the source description and domain experts; explicitly register and confirm SourceFieldDefinitions, exact schema/version/hash profile pins and any projection or relationship revisions. A passing technical regression is not approval of an entity mapping, a scientific publication or an export.
