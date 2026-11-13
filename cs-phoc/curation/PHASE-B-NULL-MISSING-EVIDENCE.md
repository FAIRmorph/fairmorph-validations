# CS-PHOC Phase B — Original-CSV Null/Missing Evidence

**Status:** TECHNICAL SOURCE REVIEW — SCIENTIFIC APPROVAL OPEN  
**Review date:** 2026-11-13  
**Upstream source commit:** `64f0b77e631c711c681306bbb56a7636ae91a471`  
**Engine review:** `FAIRmorph/fairmorph-engine` main, code inspected (not runtime executed)

## 1. Scope and provenance

Reviewed unmodified upstream CSV contents at the pinned commit, the upstream field description, the existing validation baseline, and the generic pipeline implementation. The evidence below describes the **literal CSV tokens** (empty cell `""`, explicit `"0"`, or positive integer) and the Engine code path separately. No scientific SourceFieldDefinition, entity mapping or approval was registered.

- [Source counts CSV](https://github.com/us-amlr/cs-phoc/blob/64f0b77e631c711c681306bbb56a7636ae91a471/data/manuscript/cs-phoc-counts.csv) — Git blob SHA-1 `d81e36792cad4de0108f7d0bcd0cef4e89d103a0`
- [Source events CSV](https://github.com/us-amlr/cs-phoc/blob/64f0b77e631c711c681306bbb56a7636ae91a471/data/manuscript/cs-phoc-events.csv) — Git blob SHA-1 `d129fa00d10fa11caf5f2f0481681ea5c22cb8a6`
- [Upstream CSV description](https://github.com/us-amlr/cs-phoc/blob/64f0b77e631c711c681306bbb56a7636ae91a471/data/manuscript/README.md)
- [Validation source baseline](../validation/source-baseline.json)
- [Current technical pipeline draft](../configurations/drafts/pipeline-technical.json)

The Git blob SHA-1 values identify Git objects, not Engine SHA-256 byte hashes. No FAIRmorph RUN/2 was performed for this review.

## 2. Concrete source examples

CSV row numbers below are 1-based **physical lines including the header**; raw examples are quoted verbatim as token values.

| CSV line | `count_id` | Observed literal tokens | Meaning limited to source evidence |
|---|---|---|---|
| 2 | `1-1-344008` | `pup_count="1"`, `ad_female_count="0"`, `unk_female_count=""`, `unk_male_count=""`, `unk_unk_count=""`, `total_count="1"` | Positive, zero and blank coexist in one record |
| 3 | `1-1-231413` | `ad_female_count="2"`, `ad_unk_count="0"`, `pup_count="73"`, `unk_female_count=""`, `unk_unk_count="0"`, `total_count="123"` | Explicit unknown-category zero is **not** blank |
| 4 | `1-1-231417` | `total_count="0"`, seven explicitly `"0"` count categories, three blank `unk_*` fields | Zero total does **not** imply that all ten categories were recorded |
| 5 | `1-1-195932` | `ad_female_count="12"`, `juv_female_count="0"`, `unk_female_count=""`, `total_count="31"` | Further mixed example |
| 7 | `1-2-231413` | `location="Punta San Telmo"`, `ad_female_count="0"`, `ad_male_count="1"`, `unk_unk_count="0"`, `unk_female_count=""` | Mixed categories also occur at PST |

Source line 4 explicitly demonstrates that `total_count=0` does not mean every subgroup has a measured zero.

## 3. Exhaustive literal-token census

Count CSV contains **2,144** data rows and ten explicit count columns, yielding **21,440** potential cells.

| Count field | Blank | Explicit 0 | Positive |
|---|---:|---:|---:|
| `ad_female_count` | 0 | 942 | 1202 |
| `ad_male_count` | 0 | 1397 | 747 |
| `ad_unk_count` | 254 | 1554 | 336 |
| `juv_female_count` | 130 | 1176 | 838 |
| `juv_male_count` | 130 | 1112 | 902 |
| `juv_unk_count` | 284 | 1247 | 613 |
| `pup_count` | 200 | 1598 | 346 |
| `unk_female_count` | 1396 | 742 | 6 |
| `unk_male_count` | 1396 | 746 | 2 |
| `unk_unk_count` | 710 | 1085 | 349 |
| **Total** | **4500** | **11599** | **5341** |

Derived cross-checks: **16,940** nonblank cells, **79,232** sum of nonblank numeric count values, **0** negative numeric count tokens, **0** noninteger nonblank tokens, **0** rows with `total_count` inconsistent with the sum of observed component tokens when blanks are excluded, and **0** count rows where all ten component fields are blank.

Events CSV contains **322** data rows, seven fields, **0** empty field tokens; `surveyed_pst` uses the literal tokens `TRUE` and `FALSE`. Example: `event_id="1"` appears in events CSV physical line **128**, with `surveyed_pst="TRUE"`, `research_program="USAMLR"`. These findings match the pre-existing source baseline where applicable.

## 4. Meaning asserted by the upstream source

The [upstream CSV README](https://github.com/us-amlr/cs-phoc/blob/64f0b77e631c711c681306bbb56a7636ae91a471/data/manuscript/README.md) states that numeric values are recorded when a given count type was conducted, while blank (NA) means no data were recorded. Therefore **literal `0`** represents a recorded zero-count; **literal blank** represents an unrecorded count. Do not silently equate them.

This is a documented source rule, **not** a FAIRmorph scientific sign-off or permission to infer absence at every target Entity level.

## 5. Engine parser and filter code-path audit

Inspected the generic pipeline sources on Engine `main`:

- [`core/pipeline_run.py`](https://github.com/FAIRmorph/fairmorph-engine/blob/main/src/fairmorph_engine/core/pipeline_run.py), lines 114–146: `resolve_resources` loads CSV using bare `pl.read_csv(path)` with no explicit `null_values`, schema override or version pin.
- [`core/pipeline.py`](https://github.com/FAIRmorph/fairmorph-engine/blob/main/src/fairmorph_engine/core/pipeline.py), lines 91–97: `table.unpivot/1` calls Polars `DataFrame.unpivot`.
- Same module, lines 39–59 and 80–81: `table.filter/1` with `is_not_null` evaluates `pl.col(column).is_not_null()`.
- [Technical pipeline draft](../configurations/drafts/pipeline-technical.json) unpivots the ten source count fields and filters `count_value` with `is_not_null`.

**Expected behavior, subject to runtime confirmation:** if Polars parses empty count tokens as null and `"0"` as numeric zero, the filter retains all **16,940** nonnull count cells, including **11,599** zero cells, and excludes **4,500** missing cells. The source token census proves the expected target counts but **does not prove actual Engine output**.

**Unresolved runtime dependency:** Engine `pyproject.toml` declares `polars>=1.0.0` without an upper bound or exact version. A complete parser claim requires testing the actual installed Polars version and the real Engine RUN path. No Polars runtime execution, environment lock verification, actual resource imports, or RUN/2 manifest verification was performed in this review.

## 6. Required runtime evidence before confirming parser compatibility

1. Record Engine Git commit and installed `polars.__version__` (and relevant lock/environment manifest).
2. Import both unchanged CSV files as immutable FAIRmorph source resources; record Engine-assigned SHA-256 and resource IDs.
3. Execute the current DAG draft with these real resource IDs and inspect `count_value` dtype and null statistics both **before** and **after** filtering.
4. Require before-filter total **21,440**, of which **4,500** null, **11,599** numeric zero and **5,341** positive; after filter **16,940** rows, **0** null, **11,599** zeros; sum **79,232**. Require unchanged join count and `m:1` join integrity.
5. Inspect row-level provenance for the five source examples above; verify `0` survives, blank does not produce a recorded count, and identifiers remain strings as needed.
6. Record RUN/2 manifest, pipeline hash, input object pins, step-level metrics and `verify-project` result. Explain **every** discrepancy; do not automatically approve an altered interpretation.

## 7. Decision status

- **B-06 / S-B-02 explicit zero:** SOURCE RULE SUPPORTED; RUNTIME VALIDATION OPEN; SCIENTIFIC APPROVAL OPEN.
- **B-07 / S-B-03 blank/missing:** SOURCE RULE SUPPORTED; RUNTIME VALIDATION OPEN; SCIENTIFIC APPROVAL OPEN.
- No `SourceFieldDefinition` registered.
- No Entity, Occurrence or MeasurementOrFact mapping approved.
- No Engine or Workbench expansion proposed.

**Next gate:** Verify the concrete Polars/Engine runtime results, then request explicit scientific approval for the field-level semantic definitions.
