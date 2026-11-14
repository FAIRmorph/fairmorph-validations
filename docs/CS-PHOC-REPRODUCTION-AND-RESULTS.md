# CS-PHOC validation: reproduction and interpretation

This is the **reviewer-oriented guide** to the FAIRmorph CS-PHOC test case. It separates the original research observations, generic Engine processing and dataset-specific validation code, then shows exactly what passed, what remains unapproved and how to reproduce the results. For a concise result overview, begin with the [CS-PHOC validation results](../cs-phoc/validation/README.md).

**Conclusion:** The real-data, dataset-specific **technical proof of concept passed**: immutable source import, generic Engine RUN/2, locally registered field-description drafts, reproducible test exports, and independent content auditing. **Not demonstrated:** complete Workbench operation, generic publication processing for other datasets, independently approved scientific semantics, or a publishable dataset.

## 1. Start with the research dataset, not the software

**CS-PHOC** is an independently produced research dataset of censuses of phocid seals near Cape Shirreff, Livingston Island, Antarctica. FAIRmorph did not collect or publish it.

- Original repository and exact revision: [`us-amlr/cs-phoc@64f0b77e631c711c681306bbb56a7636ae91a471`](https://github.com/us-amlr/cs-phoc/tree/64f0b77e631c711c681306bbb56a7636ae91a471).
- Original data DOI: https://doi.org/10.48361/gklk1u.
- Methods/reference paper: Woodman et al. (2024), https://doi.org/10.1038/s41597-024-03744-9.
- Input file 1: `data/manuscript/cs-phoc-events.csv` (322 rows; seven fields). Its `event_id` denotes a **survey window**; it is not the output's site-specific event ID.
- Input file 2: `data/manuscript/cs-phoc-counts.csv` (2,144 rows; 16 fields). Each record has a `count_id`, location and species, `total_count`, and ten age/sex count categories.
- The pinned original CSVs are **read unchanged**, never modified or committed here.

**Pinned raw byte SHA-256:**

| Source | SHA-256 |
| --- | --- |
| Events | `4362ae650cb72cc74901f7719920db5c8bbcfdc2ee09842595d04bf5e587bddc` |
| Counts | `be4a28aa5036dea103e9e6bbc6af5fef13d80354ef2750e0960bf78e320c3545` |

### What the source values mean

There are `2,144 × 10 = 21,440` possible count-category cells in the input. **4,500 are blank** and **16,940 contain numbers**, of which **11,599 are recorded zeros** and **5,341 are positive**. The sum of nonblank categories is **79,232** and equals the original per-row `total_count` sums.

| Source example | Meaning in this test | Output consequence |
| --- | --- | --- |
| `ad_female_count = 0` | Recorded zero for that count category, with source harmonization caveats | A category record with numerical zero; never silently dropped |
| `unk_female_count = blank` | No category count recorded | **No** category record; never silently changed to zero |
| `pup_count = 73` | 73 pups **with sexes combined**, not “unknown sex” | `individualCount=73`; `sex` is empty in DwC-A and “sexes combined” in TSV |
| `total_count` | Existing sum of category columns | A check, **not** a new independent observation |

**Important scientific limit:** Some zeros were potentially introduced by the upstream harmonization process. The test does not establish that each zero was directly observed, does not estimate population abundance, and does not infer species absence outside the counted category, location and survey window. The publisher-style export maps a zero category to `occurrenceStatus=absent`; this is a **test projection rule**, not a biological conclusion.

## 2. What each component actually does

```text
PINNED ORIGINAL CS-PHOC CSVs (external research)
    |
    v
FAIRmorph Engine: import unchanged CSVs, hash objects, run generic
  unpivot -> omit nulls -> validated event join -> verified RUN/2
    |
    +----> Engine registry: 23 English SourceFieldDefinition drafts
    |      (unreviewed; no scientific approval)
    |
    v
THIS REPOSITORY: CS-PHOC-specific publication-style projection
    |             (compare every recorded cell against RUN/2)
    +----> test DwC-A: 536 Event rows + 16,940 Occurrence rows
    +----> test PANGAEA-preparation TSV: 16,940 rows
    +----> test GeoJSON: 536 representative site-event points
    |
    v
THIS REPOSITORY: independent read-only file/content audit
    +----> actual export hashes, exact original cell comparison,
           joins, location attributes, ZIP/XSD checks, 7 samples

FAIRmorph Workbench: NOT invoked or validated by this chain.
```

**Engine proof:** Two source objects are imported and registered. The real `fairmorph.pipeline/1` performs generic `table.unpivot/1`, `table.filter/1` (excluding null only), and `table.join/1` (`event_id`, `m:1`). A versioned, immutable RUN/2 is verified. The Engine's registry accepts 23 schema-valid, immutable field-definition **draft revisions**, explicitly **unreviewed**.

**Validation-repository proof:** The CS-PHOC-specific exporter derives site-specific Event identifiers, age/sex category Occurrence identifiers, English tabular values, and site GeoJSON features. It checks every count value against the verified generic RUN before writing files. The independent auditor then reads **the written files**, their ZIP members, and original source objects again.

**Not an Engine generic export test:** The actual three test files are produced by `scripts/export_cs_phoc_test_formats.py` in *this repository*, not by the Engine's general `export_dwca()` pipeline. The test does use the Engine's existing `validate_dwca_archive()` to validate the TDWG DwC text metadata and ZIP references. Do not interpret the result as general-purpose DwC-A/PANGAEA/GeoJSON support within the Engine.

**Not a Workbench test:** The Workbench UI does not participate. The test does not show that a user can configure source field meanings, perform scientific review, approve mappings, or export all three formats through the Workbench interface.

## 3. Repository files explained

| File or directory | What it is | Is it authoritative? |
| --- | --- | --- |
| `cs-phoc/validation/source-baseline.json` | Independent expected counts, pinned upstream revision and source Git blob IDs | **Reference expectations**, not an Engine output |
| `cs-phoc/configurations/drafts/pipeline-technical.json` | Generic Engine pipeline template with placeholder resource IDs | **Template**; runner substitutes actual Engine IDs |
| `cs-phoc/configurations/drafts/dataset-metadata.json` | Proposed dataset title/metadata | **Unapproved draft** |
| `cs-phoc/configurations/drafts/source-field-definitions.ai-fairmorph.json` | 23 English source-field interpretations, with provenance and caveats | **AI-assisted PoC drafts**, not author-reviewed or formally approved |
| [Dataset-specific test export rules](../cs-phoc/validation/TEST-EXPORTS.md) | Bounded rules for site split, ten categories, IDs, representative coordinates and target formats | **Dataset-specific configuration**, not a general Engine contract |
| `scripts/run_cs_phoc.py` | Engine import, generic RUN/2 and baseline checks | **Executable technical test** |
| `scripts/register_cs_phoc_field_drafts.py` | Preflight and separate `--apply` for 23 unreviewed Engine revisions | **Engine registry test**, no approval |
| `scripts/export_cs_phoc_test_formats.py` | RUN-checked publication-style test files | **Dataset-specific test transformation**, no publication claim |
| `scripts/audit_cs_phoc_test_exports.py` | Independent inspection of already created files | **Read-only verification** |
| [Validation results and evidence](../cs-phoc/validation/README.md) | Results summary, technical test export details and independently audited outputs | **Reader-oriented evidence** with explicit scientific limitations |
| [Automated validation workflow](https://github.com/FAIRmorph/fairmorph-validations/actions) | Rebuild and audit the full test from pinned sources in CI | **Automated reproducibility check**, not scientific approval |

Generated projects, original source objects, export files and evidence JSON are written to local `validation-output/` or `artifacts/`. These are **not** expected to be committed to Git.

## 4. Reproduce the full outcome

These commands are designed for a **fresh clone**. Use Bash in a shell with `python` referring to Python **3.11 or later**, `git`, and package installation access. Start in the root of a clone of `FAIRmorph/fairmorph-validations`. The pinned Engine installation brings its declared dependencies (including Polars). A virtual environment is recommended.

### Obtain the exact software and source revision

```bash
mkdir -p dependencies

git clone https://github.com/FAIRmorph/fairmorph-engine.git dependencies/fairmorph-engine
git -C dependencies/fairmorph-engine checkout c84b6f87585bab1237d6383cd3a47311f57250c2

git clone https://github.com/us-amlr/cs-phoc.git dependencies/cs-phoc
git -C dependencies/cs-phoc checkout 64f0b77e631c711c681306bbb56a7636ae91a471

python -m pip install -e dependencies/fairmorph-engine
```

**Reproducibility note:** The dataset and Engine are pinned; this repository's `main` is a moving branch. For a frozen historical evaluation, also record or check out the validations repository commit being tested.

### Import and run the generic Engine workflow

```bash
python scripts/run_cs_phoc.py \
  --upstream dependencies/cs-phoc \
  --project validation-output/cs-phoc.fairmorph
```

The runner rejects an existing destination and verifies imported source identities and the pipeline's recorded values. It writes a project-local `validation/phase-a-result.json` and a small root-level `artifacts/phase-a-result.json`. The machine-generated `run_id` must be **read from that output**, not guessed.

### Register field-description drafts (no approvals)

```bash
python scripts/register_cs_phoc_field_drafts.py \
  --project validation-output/cs-phoc.fairmorph

python scripts/register_cs_phoc_field_drafts.py \
  --project validation-output/cs-phoc.fairmorph --apply
```

The first call is read-only and should print `preflight_passed`. The second registers 23 immutable, **unreviewed** draft revisions and writes a project-local evidence report. Do not rerun `--apply` on an already registered project; the script intentionally refuses overwrite.

### Generate three local **test** export formats

```bash
RUN_ID=$(python -c 'import json; print(json.load(open("artifacts/phase-a-result.json"))["run_id"])')

python scripts/export_cs_phoc_test_formats.py \
  --project validation-output/cs-phoc.fairmorph \
  --run-id "$RUN_ID" \
  --output validation-output/cs-phoc-test-exports
```

This produces:

| File | Contents |
| --- | --- |
| `cs-phoc-test.dwca.zip` | Event-core / Occurrence-extension DwC-A containing `Event.csv`, `Occurrence.csv`, `meta.xml`; **no publication EML** |
| `pangaea-test.tsv` | UTF-8 tab-separated **submission-preparation** data; not an accepted PANGAEA dataset |
| `site-events.geojson` | RFC 7946 FeatureCollection of **representative census-site** Event points |
| `test-metadata.json` | English source attribution, source DOI, caveats and test-only status |
| `test-report.json` | Source/RUN/configuration checksums, output hashes and exporter checks |

The output directory must **not exist** before execution. Repetition requires a *new* directory, not an overwrite.

### Independently audit the existing exported files

```bash
python scripts/audit_cs_phoc_test_exports.py \
  --project validation-output/cs-phoc.fairmorph \
  --exports validation-output/cs-phoc-test-exports \
  --report validation-output/cs-phoc-final-content-audit.json
```

Expected console output includes:

```json
{
  "status": "passed",
  "checked_occurrences": 16940,
  "sample_checks_passed": 7
}
```

The console also prints the path of the **new** audit JSON. This script reads the originals, source identities, existing project registry/RUN evidence and actual export bytes. It **does not** regenerate or modify exports. The output report path also must not exist.

**For an easier independent reproduction:** Use the [validation runs on GitHub Actions](https://github.com/FAIRmorph/fairmorph-validations/actions) and their small downloadable audit reports. CI creates a fresh project using the pinned Engine and source commit; it does not retain original research data or full export files.

## 5. What passed—and what the numbers prove

| Check | Expected result | Interpretation |
| --- | ---: | --- |
| Original source survey windows | 322 | Unchanged research input, **not** 322 independent site-events |
| Original count records | 2,144 | Source table rows, **not** 2,144 individual seals |
| Source numeric count-category cells | 16,940 | Only nonblank cells yield exported category records |
| Explicit recorded zero cells | 11,599 | These are retained; not automatically all directly field-observed |
| Source blanks | 4,500 | These are omitted from the long table; **never zero-filled** |
| Sum of all category values | 79,232 | Arithmetic invariant, **not** a population estimate |
| Test DwC-A Events | 536 | 322 Core site events plus 214 Punta San Telmo site events |
| Test DwC-A Occurrences | 16,940 | Source category records, **not unique tagged individuals** |
| TSV data rows | 16,940 | Same source category content with contextual columns |
| GeoJSON features | 536 | Repeated representative points for site-events, **not animal tracks** |
| Seven fixed source-grounded samples | 7/7 pass | Covers positive, zero, missing, PST, sex aggregation and edge cases |
| DwC-A ZIP and metadata XSD | Pass | Technical archive structure; **not** EML publication validation |

The exporter independently compares source category keys/values against the generic Engine RUN. The auditor separately compares **every** source nonblank category against **both** output tables, validates event relations and exact site coordinates, and checks that archive member bytes equal the corresponding CSV/XML files. Checksums bind the evidence to one set of local artifacts.

### Examples actually inspected

| Case | Original cell | Expected export |
| --- | --- | --- |
| Positive pup | `1-1-344008 / pup_count = 1` | One record with count 1 |
| Explicit zero | `1-1-344008 / ad_female_count = 0` | One record with count 0 |
| Blank | `1-1-344008 / unk_female_count = blank` | **No** record |
| Blank despite zero total | `1-1-231417 / unk_unk_count = blank` | **No** record |
| Punta San Telmo | `1-2-231413 / juv_male_count = 11` | One correct PST-linked record |
| Combined pup sexes | `1-1-231413 / pup_count = 73` | Count 73, sex **not** “unknown” |
| Recorded zero unknown age/sex | `1-1-231413 / unk_unk_count = 0` | One record with zero |

## 6. What does **not** follow from a pass

1. **No scientific sign-off:** 23 Engine SourceFieldDefinition revisions are `partially_defined` and `unreviewed`. There is no separate approved review event or approved mapping. The FAIRmorph project user's acceptance of bounded drafts is not formal Registry review and is **not** upstream author approval.
2. **No upstream authorship of the added descriptions:** The 23 interpretations were prepared with AI assistance **for this PoC only** and labelled **“AI Description — added by FAIRmorph”**. The original CS-PHOC authors/owners did **not** write, review, approve or endorse them. FAIRmorph Engine and Workbench have **no AI runtime requirement**.
3. **No general-purpose publication export demonstration:** This case uses dataset-specific export code in this repository, not the Engine's generic `export_dwca()` implementation. No generic PANGAEA or GeoJSON Engine adapter is tested.
4. **No finished Workbench integration:** The UI does not run this end-to-end sequence; its field-semantic interview, reviewer decisions and publication workflow remain outside this test.
5. **No publishable DwC-A/EML or submitted PANGAEA package:** The ZIP has validated `meta.xml` but no publication EML; PANGAEA TSV is only a preparation file.
6. **No independent ecological inference:** No population abundance extrapolation, precise animal geolocation, or universal absence claim is justified. Preserve the provenance and uncertainty of harmonized zero values.

## 7. Evidence, provenance and attribution

- [Source-derived baseline JSON](../cs-phoc/validation/source-baseline.json) — independently calculated **expectations**, not generated by the Engine.
- [Independent output content audit](../cs-phoc/validation/INDEPENDENT-CONTENT-AUDIT.md) — exact source-to-output checks, including seven fixed examples.
- [Validation results overview](../cs-phoc/validation/README.md) — essential counts, interpretation and recommended reading order.
- [Original authors and source licensing](../THIRD-PARTY-NOTICES.md).
- Small CI audit reports are attached to eligible [GitHub Actions runs](https://github.com/FAIRmorph/fairmorph-validations/actions), subject to artifact retention.

**How to cite this work:** Cite CS-PHOC / Woodman et al. for the **research dataset and published scientific interpretation**. Cite this repository and the pinned Engine commit for the **technical PoC validation**, not as authors of the original research observations.

**Review summary:** **Passed technical validation for this fixed real-data test case. Scientific approval, publication-readiness, generality beyond CS-PHOC, and Workbench coverage remain unproven.**
