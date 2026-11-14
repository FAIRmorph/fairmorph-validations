# CS-PHOC validation: results and interpretation

The FAIRmorph CS-PHOC validation tests a **fixed, publicly available ecological research dataset** against independently derived expectations. It checks whether the Python Engine preserves the original records and produces a verifiable technical processing run, and whether separate, dataset-specific export scripts reproduce the recorded values correctly. An independent auditor then inspects the **files actually written**, rather than relying only on the exporter's success message.

**Result: the bounded technical test passed.** The reported outputs are **test artefacts**, not a scientifically approved dataset or a publication. The test does **not** demonstrate a finished Workbench workflow, generic publishing to GBIF or PANGAEA, or biological conclusions about seal abundance. FAIRmorph did not collect the original CS-PHOC observations.

## Results at a glance

| Evidence | Verified result | Meaning |
| --- | ---: | --- |
| Original survey windows | **322** | Source records, not 322 location-specific output Events |
| Original count records | **2,144** | Rows in the source counts table |
| Recorded count-category values | **16,940** | Checked against both exported tabular representations |
| Explicit zeros | **11,599** | Preserved as numeric zero; not silently discarded |
| Blank category cells | **4,500** | Omitted from exported category rows, never converted to zero |
| Test DwC-A Events / Occurrences | **536 / 16,940** | Location-specific Events and category records, not tracked individuals |
| Test PANGAEA-preparation TSV / GeoJSON | **16,940 rows / 536 features** | Preparation table and representative census-site points |
| Independent audit | **Passed; 7/7 targeted cases** | All recorded category cells compared, plus selected edge cases |

The sum of the recorded category values is **79,232**. This is an arithmetic consistency check, **not a population estimate**. Some zeros may have been introduced during upstream data harmonization, so the test cannot infer that every zero represents a directly observed absence. GeoJSON coordinates identify representative census locations, **not individual animals**.

## Read the evidence in this order

1. **[Reproduction and interpretation](../../docs/CS-PHOC-REPRODUCTION-AND-RESULTS.md)** — the main reviewer guide: original data and attribution, actual Engine operations, commands, expected results and scientific limitations.
2. **[Test export formats and their scope](TEST-EXPORTS.md)** — the dataset-specific DwC-A, TSV and GeoJSON outputs, and what each does and does not establish.
3. **[Independent audit of exported data](INDEPENDENT-CONTENT-AUDIT.md)** — how written files, source values, zeros, blanks, identifiers and spatial references are checked.
4. **[Validation criteria for other datasets](../../docs/VALIDATION-PLAN.md)** — what would need to be checked before claiming comparable evidence for another source.

For the original research, follow the [CS-PHOC source data and citation information](../../THIRD-PARTY-NOTICES.md). Reproducible CI runs are available via [GitHub Actions](https://github.com/FAIRmorph/fairmorph-validations/actions). Generated outputs, imported source data and local projects are **not published as downloads in this repository**.

## What remains outside the test

The Engine registers **23 source-field definition drafts** as `unreviewed`; there is no formal reviewer approval or endorsement by the original data authors. The actual conversion into the three output formats is **CS-PHOC-specific code in the validation repository**, not a general-purpose Engine/Workbench export. Technical reproducibility and output consistency therefore remain distinct from **scientific approval, publication readiness and generality across datasets**.
