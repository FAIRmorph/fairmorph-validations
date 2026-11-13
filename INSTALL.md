# Installation and reproduction

> **Prototype Fund (Germany) · Proof of concept — not production software.** FAIRmorph is an experimental open-source project for Germany's [Prototype Fund](https://prototypefund.de/). This repository contains **dataset-specific technical validation**, not a general publishing application, a scientifically approved dataset or a substitute for publisher review.

## Requirements

- Python **3.11+**, Git and `pip`.
- Network access to clone the public original CS-PHOC research and the pinned FAIRmorph Engine revision.
- A writable folder for generated evidence; source CSVs and generated output packages are **not bundled** in this repository.

These are **development and scientific-reproduction instructions**, not an end-user installation. No GUI is needed.

## Obtain pinned dependencies

From the root of a clone of this validations repository:

```bash
python -m venv .venv
source .venv/bin/activate
# Windows PowerShell instead: .venv\Scripts\Activate.ps1

mkdir -p dependencies
git clone https://github.com/FAIRmorph/fairmorph-engine.git dependencies/fairmorph-engine
git -C dependencies/fairmorph-engine checkout c84b6f87585bab1237d6383cd3a47311f57250c2

git clone https://github.com/us-amlr/cs-phoc.git dependencies/cs-phoc
git -C dependencies/cs-phoc checkout 64f0b77e631c711c681306bbb56a7636ae91a471

python -m pip install -e dependencies/fairmorph-engine
```

## Reproduce and audit

The authoritative [CS-PHOC reproduction and results guide](docs/CS-PHOC-REPRODUCTION-AND-RESULTS.md) gives the exact run, field-draft registration, dataset-specific export and independent audit commands, including the expected values and limits. Follow those instructions in **new, nonexistent** output directories.

For automated coverage, see [reference validation CI](.github/workflows/cs-phoc-phase-a.yml). A passing technical audit does **not** establish scientific approval or production-readiness; the test exports remain `publication_ready: false`.

The separate [FAIRmorph Workbench](https://github.com/FAIRmorph/fairmorph-workbench) is not part of this automated test.
