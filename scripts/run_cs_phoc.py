#!/usr/bin/env python3
"""External v0.13 reference validation runner; never placed inside a FAIRmorph project.

Requires the pinned FAIRmorph Engine and Polars; no scientific approvals are created.
"""
import argparse
import json
import shutil
import subprocess
from pathlib import Path

import polars as pl
from fairmorph_engine.core.project import initialize_project, import_resource, register_package
from fairmorph_engine.core.pipeline_run import register_pipeline
from fairmorph_engine.core.project_execution import select_project_pipeline, execute_project_run
from fairmorph_engine.core.export import verify_project

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "cs-phoc"


def main():
    parser = argparse.ArgumentParser(description="Validate pinned CS-PHOC sources with FAIRmorph Engine")
    parser.add_argument("--upstream", type=Path, required=True, help="Pinned us-amlr/cs-phoc checkout")
    parser.add_argument("--project", type=Path, required=True, help="Nonexistent FAIRmorph project directory")
    args = parser.parse_args()
    project = args.project.resolve()
    if project.exists() or project.is_symlink():
        parser.error(f"Project already exists, refusing to overwrite: {project}")

    baseline = json.loads((REFERENCE / "validation/source-baseline.json").read_text(encoding="utf-8"))
    source_files = {
        "events": "data/manuscript/cs-phoc-events.csv",
        "counts": "data/manuscript/cs-phoc-counts.csv",
    }
    expected_blobs = {item["path"]: item["git_blob_sha1"] for item in baseline["source_files"]}
    sources = {}
    for role, relative in source_files.items():
        source = args.upstream.resolve() / relative
        if not source.is_file() or source.is_symlink():
            parser.error(f"Missing regular upstream source: {source}")
        actual = subprocess.check_output(["git", "hash-object", str(source)], text=True).strip()
        if actual != expected_blobs[relative]:
            raise ValueError(f"Upstream source identity mismatch: {relative} ({actual})")
        sources[role] = source

    initialize_project(project, "CS-PHOC reference (v0.13)")
    imported = {role: import_resource(project, source, role) for role, source in sources.items()}
    virtual = register_package(project, "cs-phoc-manuscript-sources", imported)

    drafts = project / "configurations/drafts"
    drafts.mkdir(parents=True, exist_ok=True)
    template = json.loads(
        (REFERENCE / "configurations/drafts/pipeline-technical.json").read_text(encoding="utf-8")
    )
    for role, item in imported.items():
        template["resources"][role]["resource_id"] = item["resource_id"]
    (drafts / "pipeline-technical.json").write_text(
        json.dumps(template, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    shutil.copyfile(REFERENCE / "configurations/drafts/dataset-metadata.json", drafts / "dataset-metadata.json")
    sha = register_pipeline(project, template)["pipeline_sha256"]
    select_project_pipeline(project, sha)
    run = execute_project_run(project)
    verification = verify_project(project)

    output = project / "runs" / run["run_id"] / "outputs/counts_with_events.parquet"
    table = pl.read_parquet(output)
    # Mixed CSV columns become strings during unpivot: cast only for independent numeric checks.
    count_values = table["count_value"].cast(pl.Int64, strict=True)
    checks = baseline["checks"]
    observed = {
        "long_rows": table.height,
        "explicit_zero_values": int((count_values == 0).sum()),
        "count_sum": int(count_values.sum()),
        "unique_count_ids": table["count_id"].n_unique(),
        "unique_joined_event_ids": table["event_id"].n_unique(),
        "null_count_values": count_values.null_count(),
    }
    assert observed["long_rows"] == checks["nonempty_count_cells"], observed
    assert observed["explicit_zero_values"] == checks["explicit_zero_count_cells"], observed
    assert observed["count_sum"] == checks["source_total_count_sum"], observed
    assert observed["unique_count_ids"] == baseline["source_files"][1]["unique_count_ids"], observed
    assert observed["unique_joined_event_ids"] <= baseline["source_files"][0]["unique_event_ids"], observed
    assert observed["null_count_values"] == 0, observed
    assert verification["status"] == "verified", verification
    assert verification["completed_runs"] == 1, verification
    assert verification["source_objects"] == 2, verification
    assert len(virtual["resources"]) == 2

    evidence = {
        "phase": "A",
        "status": "passed",
        "scientific_approval": False,
        "upstream_commit": baseline["upstream_commit"],
        "source_sha256": {role: item["sha256"] for role, item in imported.items()},
        "source_resource_ids": {role: item["resource_id"] for role, item in imported.items()},
        "package_id": virtual["package_id"],
        "pipeline_sha256": sha,
        "run_id": run["run_id"],
        **observed,
        "verified": verification["status"],
    }
    (project / "validation").mkdir()
    shutil.copyfile(REFERENCE / "validation/source-baseline.json", project / "validation/source-baseline.json")
    (project / "validation/phase-a-result.json").write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (project / "curation").mkdir()
    shutil.copyfile(REFERENCE / "curation/FIELD-REVIEW.md", project / "curation/FIELD-REVIEW.md")

    evidence_dir = ROOT / "artifacts"
    evidence_dir.mkdir(exist_ok=True)
    (evidence_dir / "phase-a-result.json").write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(evidence, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
