#!/usr/bin/env python3
"""Stage 23 English FAIRmorph AI source-field drafts in an existing CS-PHOC project.

No source imports, RUNs, review approvals, schema changes or publishing.
Default: read-only preflight. Use --apply to register unreviewed draft revisions.
"""
import argparse
import csv
import hashlib
import json
import sqlite3
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from fairmorph_engine.core.registry import define_field
from fairmorph_engine.core.export import verify_project
from fairmorph_engine.core import registry
from fairmorph_engine.core import project as engine_project

ROOT = Path(__file__).resolve().parents[1]
DRAFT_PATH = ROOT / "cs-phoc/configurations/drafts/source-field-definitions.ai-fairmorph.json"
SOURCE_SHA256 = {
    "events": "4362ae650cb72cc74901f7719920db5c8bbcfdc2ee09842595d04bf5e587bddc",
    "counts": "be4a28aa5036dea103e9e6bbc6af5fef13d80354ef2750e0960bf78e320c3545",
}
SOURCE_FIELD_COUNTS = {"events": 7, "counts": 16}
AI_MARK = "AI Description — added by FAIRmorph"


def preflight(project: Path):
    """Check every field and resource before changing the project catalog."""
    if not (project / "project.json").is_file() or not (project / "catalog/catalog.sqlite").is_file():
        raise ValueError("Existing FAIRmorph project with project.json and catalog is required")
    doc = json.loads(DRAFT_PATH.read_text(encoding="utf-8"))
    fields = doc["fields"]
    if len(fields) != 23 or doc["language"] != "en":
        raise ValueError("Expected exactly 23 English FAIRmorph drafts")
    p = json.loads((project / "project.json").read_text(encoding="utf-8"))
    schema_path = Path(registry.__file__).resolve().parents[1] / "contracts/SourceFieldDefinition.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    con = sqlite3.connect(f"file:{(project / 'catalog/catalog.sqlite').resolve()}?mode=ro", uri=True)
    try:
        resource_rows = con.execute("SELECT resource_id, object_sha256, original_name FROM source_resources").fetchall()
        resources = {}
        for role, wanted in SOURCE_SHA256.items():
            matches = [r for r in resource_rows if r[1] == wanted]
            if len(matches) != 1:
                raise ValueError(f"Expected exactly one imported {role} resource with pinned SHA-256")
            resources[role] = matches[0][0]
            object_file = project / "objects/sha256" / wanted[:2] / wanted
            if not object_file.is_file() or object_file.is_symlink():
                raise ValueError(f"Missing immutable {role} object")
            digest = hashlib.sha256(object_file.read_bytes()).hexdigest()
            if digest != wanted:
                raise ValueError(f"Source checksum mismatch for {role}")
        headers = {}
        for role, sha in SOURCE_SHA256.items():
            with (project / "objects/sha256" / sha[:2] / sha).open(
                encoding="utf-8-sig", newline=""
            ) as handle:
                headers[role] = next(csv.reader(handle))

        tables = {row[0] for row in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if "current_field_definitions" in tables:
            existing = con.execute("SELECT COUNT(*) FROM current_field_definitions").fetchone()[0]
            if existing:
                raise ValueError(
                    f"Project already has {existing} current SourceFieldDefinitions; "
                    "refusing to overwrite or silently re-register them"
                )
    finally:
        con.close()

    seen = set()
    batch = []
    for item in fields:
        role, column = item["resource_alias"], item["source_column"]
        key = (role, column)
        if key in seen or role not in SOURCE_SHA256 or column not in headers[role]:
            raise ValueError(f"Invalid or duplicate source field locator: {key}")
        seen.add(key)
        definition = item["definition"]
        if (
            definition.get("language") != "en"
            or definition.get("definition_source") != "suggested"
            or definition.get("review_status") != "unreviewed"
            or definition.get("semantic_status") != "partially_defined"
            or AI_MARK not in definition.get("notes", "")
        ):
            raise ValueError(f"AI attribution and unreviewed contract status required: {key}")
        if role == "counts" and column.endswith("_count") and column != "total_count":
            if definition.get("counting_unit") != "individual":
                raise ValueError(f"Incorrect counting_unit token for {key}")
        resource_id = resources[role]
        field_id = "field-" + hashlib.sha256(
            f"{resource_id}\0{column}".encode("utf-8")
        ).hexdigest()
        full = {
            "contract_version": "1.0.0",
            "dataset_id": p["project_id"],
            "source_resource_id": resource_id,
            "source_field_id": field_id,
            "field_locator": {"kind": "column", "path": column},
            "semantic_status": "unresolved",
            "review_status": "unreviewed",
            "definition_source": "unknown",
            "description": None,
            "value_semantics": {"missing_values": [], "zero_meaning": "unknown"},
            **definition,
        }
        validator.validate(full)
        batch.append((role, column, resource_id, definition))
    for role, expected in SOURCE_FIELD_COUNTS.items():
        if sum(1 for r, _, _, _ in batch if r == role) != expected:
            raise ValueError(f"Unexpected number of {role} fields")
    return batch, resources


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--project", required=True, type=Path)
    ap.add_argument("--apply", action="store_true", help="Register unreviewed drafts")
    args = ap.parse_args()
    path = args.project.resolve()
    entries, resources = preflight(path)
    if not args.apply:
        print(json.dumps({
            "status": "preflight_passed",
            "mode": "read_only",
            "fields": len(entries),
            "source_resource_ids": resources,
            "will_register": False,
            "scientific_approval": False,
        }, indent=2))
        return
    results = []
    for role, column, resource_id, definition in entries:
        registered = define_field(path, resource_id, column, definition)
        results.append({
            "resource": role,
            "source_column": column,
            "source_field_id": registered["source_field_id"],
            "revision_id": registered["revision_id"],
            "content_sha256": registered["content_sha256"],
        })
    if len(results) != 23:
        raise ValueError("Unexpected registry result count")
    checked = verify_project(path)
    if checked["status"] != "verified":
        raise ValueError("Project verification failed")
    evidence = {
        "status": "drafts_registered",
        "description_type": AI_MARK,
        "language": "en",
        "review_status": "unreviewed",
        "scientific_approval": False,
        "source_commit": "64f0b77e631c711c681306bbb56a7636ae91a471",
        "source_resource_ids": resources,
        "field_count": len(results),
        "project_verified": checked["status"],
        "fields": results,
    }
    dest = path / "validation/phase-b-field-drafts.json"
    dest.parent.mkdir(exist_ok=True)
    if dest.exists():
        raise ValueError("Evidence file already exists; refusing to overwrite")
    dest.write_text(json.dumps(evidence, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": evidence["status"],
        "field_count": evidence["field_count"],
        "review_status": evidence["review_status"],
        "project_verified": evidence["project_verified"],
        "evidence_file": str(dest),
    }, indent=2))


if __name__ == "__main__":
    main()
