# CS-PHOC Phase B.4 — Local Engine Registry Drafts

**Document status:** FAIRmorph PoC execution instructions, English (en).  
**Description attribution:** **AI Description — added by FAIRmorph**.  
**Upstream authorship:** The field descriptions are FAIRmorph AI-assisted test interpretations, **not** statements authored, approved or endorsed by CS-PHOC dataset owners or authors.

## Purpose and bounded scope

Stage the **23 English, user-accepted source field descriptions** as **unreviewed Engine SourceFieldDefinition revisions** in an existing local project created by the validated `scripts/run_cs_phoc.py` workflow. This is **not** a scientific registration approval. The runner creates real, immutable Engine revision IDs, and records them in the local validation evidence file.

- No additional source imports or changed original CSVs
- No new Engine or Workbench features
- No new RUN/2; completed RUN evidence remains unchanged
- No reviewer identities, approval events, Entity/Relation mappings or export publication
- No generated projects or original source files in Git

## Preconditions

From the root of the **up-to-date `fairmorph-validations` repository**, in the same Python environment in which FAIRmorph Engine is installed:

1. Keep the previously created local project, for example `validation-output/cs-phoc-phase-b.fairmorph`.
2. Use a project with the two original imported resources. The script checks the exact source SHA-256 values, 23 physical CSV headers and Engine Schema 1.0.0.
3. Review [AI-attributed field proposals](../curation/PHASE-B-APPROVAL-PROPOSAL.md) and [structured definition arguments](../configurations/drafts/source-field-definitions.ai-fairmorph.json).

## Execution

First run **read-only preflight**:

```bash
python scripts/register_cs_phoc_field_drafts.py \
  --project validation-output/cs-phoc-phase-b.fairmorph
```

Expected: `"status": "preflight_passed"`, `"fields": 23`, `"will_register": false`, `"scientific_approval": false`.

Only if preflight passes, stage the definition drafts:

```bash
python scripts/register_cs_phoc_field_drafts.py \
  --project validation-output/cs-phoc-phase-b.fairmorph \
  --apply
```

Expected: `"status": "drafts_registered"`, `"field_count": 23`, `"review_status": "unreviewed"`, `"project_verified": "verified"`.

Actual IDs will be written to **`validation-output/cs-phoc-phase-b.fairmorph/validation/phase-b-field-drafts.json`**, including one source field ID, definition revision ID and definition content SHA-256 per field. This local evidence file is intentionally **not** committed to Git, because it binds to a specific project ID and imported resources.

## Acceptance criteria

- Both immutable source resources match the pinned source byte SHA-256 values
- Exactly 7 events and 16 counts definition revisions, with no duplicate locators
- Each definition: `language: en`, `definition_source: suggested`, `semantic_status: partially_defined`, `review_status: unreviewed` and an attribution notice including **AI Description — added by FAIRmorph**
- All ten numeric category definitions use `counting_unit: individual` (exact Engine contract token)
- After staging, `verify_project` still returns `verified`
- No reviewer or source-author approval is written

The script **refuses** to overwrite an existing set of current SourceFieldDefinitions or an existing local evidence file. On a partial failure, inspect the catalog and evidence before retrying; do not reset a project with completed RUNs as a casual workaround.

## Phase C gate

For PoC **mapping prototyping**, stable draft revision IDs are sufficient to document source-field semantics and provenance. Formal approved Entity/Relation mapping execution will require actual `semantic_status: defined` revisions and explicit, identified review decisions under the Engine's existing rules. Do not automatically promote these drafts or claim external CS-PHOC approval.

No additional local parser/regression run is required just to stage these drafts.
