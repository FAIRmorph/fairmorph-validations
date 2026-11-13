# CS-PHOC: real-data validation case

This is the **dataset-specific test fixture** for the FAIRmorph Engine proof of concept. Start with the [reviewer guide](../docs/CS-PHOC-REPRODUCTION-AND-RESULTS.md) for the complete data-flow diagram, reproduction commands, expected values and audit interpretation. The general [repository README](../README.md) explains the separation between original research, the Engine, this validation code and the Workbench.

The original [US AMLR / CS-PHOC](https://github.com/us-amlr/cs-phoc/tree/64f0b77e631c711c681306bbb56a7636ae91a471) CSVs are **not** included here. The test checks them out at an immutable commit and imports them unchanged. See [source attribution and licensing](../THIRD-PARTY-NOTICES.md).

## What is in this directory?

| Path | Purpose |
| --- | --- |
| `configurations/drafts/pipeline-technical.json` | Generic Engine pipeline template. Resource IDs are placeholders until assigned by actual import. |
| `configurations/drafts/dataset-metadata.json` | Unapproved dataset metadata draft. |
| `configurations/drafts/source-field-definitions.ai-fairmorph.json` | 23 English AI-assisted source-field descriptions with limitations. **Drafts, not reviewed or approved.** |
| `configurations/drafts/c1-c4-test-projection.json` | CS-PHOC-only Event/Occurrence, TSV and GeoJSON test transformation rules. |
| `validation/source-baseline.json` | Source-derived expected row counts and Git blob identities; **not an Engine RUN result**. |
| `curation/` | Source interpretation and evidence, including early review questions. Some filenames reflect historical development milestones. |
| `validation/` | Detailed export/audit specifications and a historical closure record. |

## At a glance

- **Real input:** 322 survey-window records, 2,144 count records; 16,940 nonblank category values, 4,500 blanks, 11,599 explicit zeros, sum 79,232.
- **Engine actually demonstrated:** Unchanged source import, pinned and verifiable RUN/2 using generic unpivot/filter/join operators, and registration of 23 **unreviewed** SourceFieldDefinition drafts.
- **This repository's test transformation:** 536 site-specific Events, 16,940 category Occurrences, 16,940 PANGAEA-preparation TSV rows and 536 representative GeoJSON site-event points.
- **Independent audit:** All source-recorded cells versus exported tabular files, seven targeted samples, Event references and spatial values, ZIP integrity and TDWG `meta.xml` XSD.
- **Not demonstrated:** Complete Workbench UI flow, generic Engine publication export, formally approved scientific field/mapping decisions or a publication-ready package.

The AI-assisted descriptions are labelled **“AI Description — added by FAIRmorph”** and were not written, reviewed, approved or endorsed by the CS-PHOC authors/owners. FAIRmorph Engine and Workbench do not depend on AI.

To reproduce, follow **[the reviewer guide](../docs/CS-PHOC-REPRODUCTION-AND-RESULTS.md#4-reproduce-the-full-outcome)**. Generated source objects, projects and export files must remain outside the repository history.
