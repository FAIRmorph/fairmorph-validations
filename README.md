# FAIRmorph Validations

Independent, reproducible technical and scientific validation of FAIRmorph against real, documented research datasets. The validation project is **not** part of the FAIRmorph Engine or Workbench source tree.

## Reference datasets

- [CS-PHOC](cs-phoc/README.md): pinned original public research sources, v0.13 technical DAG, source-derived baseline, and explicitly unapproved scientific field-review decisions.

## Repository organization

- `cs-phoc/configurations/drafts/`: technical pipeline template and unapproved metadata draft
- `cs-phoc/curation/`: documented field definitions and outstanding scientific decisions
- `cs-phoc/validation/`: source-derived baseline values, **not** Engine results
- `scripts/run_cs_phoc.py`: independent technical regression runner; stays **outside** generated FAIRmorph projects
- `.github/workflows/cs-phoc-phase-a.yml`: CI for reference data regression
- `docs/VALIDATION-PLAN.md`: phased evidence and acceptance criteria
- `THIRD-PARTY-NOTICES.md`: source provenance and third-party licenses

## Local technical regression (Phase A)

Requires Python 3.11+, git, and a fresh, nonexistent output directory. Use separate checkouts of the exact pinned upstream sources and FAIRmorph Engine:

```sh
git clone https://github.com/FAIRmorph/fairmorph-engine.git dependencies/fairmorph-engine
git -C dependencies/fairmorph-engine checkout c84b6f87585bab1237d6383cd3a47311f57250c2
python -m pip install -e dependencies/fairmorph-engine

git clone https://github.com/us-amlr/cs-phoc.git dependencies/cs-phoc
git -C dependencies/cs-phoc checkout 64f0b77e631c711c681306bbb56a7636ae91a471

python scripts/run_cs_phoc.py --upstream dependencies/cs-phoc --project validation-output/cs-phoc.fairmorph
```

The runner refuses to overwrite an existing project. It writes real source objects and RUN/2 artifacts only into a generated local FAIRmorph project. CI publishes a limited JSON evidence summary, not the upstream CSV files. Do not commit generated projects, imported originals, or local credentials.

## Status and scope

Phase A tests technical structure, source invariants, zero-versus-missing handling, DAG joins and RUN integrity. It does **not** approve scientific field semantics, entity projections, relations or publication. Those require explicit scientific review and approval (see [validation plan](docs/VALIDATION-PLAN.md)).

The reference files originated in unmerged [Engine PR #12](https://github.com/FAIRmorph/fairmorph-engine/pull/12), head `91c93b9404d3e26550cc7a2c5fb238e5dc873e89`. The original technical reference CI passed in that branch; the separated workflow must be independently verified here.

## License

Original FAIRmorph validation scripts, configurations and documentation are licensed under [Apache License 2.0](LICENSE), unless explicitly indicated otherwise. Third-party CS-PHOC source data and upstream material retain their **CC0 1.0 Universal** designation; this repository does not relicense them. See [third-party notices](THIRD-PARTY-NOTICES.md). Scientific citation is requested even when not legally required by CC0.
