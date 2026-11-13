#!/usr/bin/env python3
"""C.1–C.4: CS-PHOC local TEST exports from an immutable verified FAIRmorph RUN/2.

Dataset-scoped validation harness. No scientific approvals, public submission,
source modifications, engine modifications, or new generic export capability.
"""
import argparse
import csv
import hashlib
import json
import sqlite3
import zipfile
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from xml.etree import ElementTree as ET

import polars as pl
from fairmorph_engine.core.export import verified_run
from fairmorph_engine.core.publication_adapters import validate_dwca_archive

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "cs-phoc/configurations/drafts/c1-c4-test-projection.json"
DWC = "http://rs.tdwg.org/dwc/terms/"
DWC_TEXT = "http://rs.tdwg.org/dwc/text/"
EVENT_FIELDS = [
    "eventID", "eventDate", "decimalLongitude", "decimalLatitude",
    "locality", "coordinateUncertaintyInMeters", "sampleSizeValue",
    "sampleSizeUnit", "eventRemarks", "samplingProtocol",
]
OCC_FIELDS = [
    "occurrenceID", "eventID", "scientificName", "vernacularName",
    "individualCount", "occurrenceStatus", "basisOfRecord", "lifeStage", "sex",
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def write_json(path, data):
    path.write_text(
        json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def write_table(path, fields, rows, delimiter=","):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(
            stream, fieldnames=fields, delimiter=delimiter, lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def source_resources(project, cfg):
    catalog = project / "catalog/catalog.sqlite"
    if not catalog.is_file():
        raise ValueError("FAIRmorph project catalog missing")
    with sqlite3.connect(f"file:{catalog.resolve()}?mode=ro", uri=True) as con:
        resources = con.execute(
            "SELECT resource_id, object_sha256 FROM source_resources"
        ).fetchall()
    result = {}
    for role, expected_sha in cfg["source_sha256"].items():
        matches = [rid for rid, digest in resources if digest == expected_sha]
        if len(matches) != 1:
            raise ValueError(f"Expected exactly one pinned {role} resource")
        path = project / "objects/sha256" / expected_sha[:2] / expected_sha
        if not path.is_file() or path.is_symlink() or sha(path) != expected_sha:
            raise ValueError(f"Original source missing or modified: {role}")
        result[role] = {"id": matches[0], "path": path}
    return result


def validate_field_drafts(project, resources):
    file = project / "validation/phase-b-field-drafts.json"
    if not file.is_file():
        raise ValueError("Phase B.4 registration evidence not found")
    evidence = load_json(file)
    if (
        evidence.get("field_count") != 23
        or evidence.get("review_status") != "unreviewed"
        or evidence.get("scientific_approval") is not False
        or len(evidence.get("fields", [])) != 23
    ):
        raise ValueError("Expected 23 unreviewed, clearly non-approved field drafts")
    for role in ("events", "counts"):
        if evidence["source_resource_ids"][role] != resources[role]["id"]:
            raise ValueError(f"Field drafts bind to different {role} resource")
    catalog = project / "catalog/catalog.sqlite"
    with sqlite3.connect(f"file:{catalog.resolve()}?mode=ro", uri=True) as con:
        total = con.execute("SELECT COUNT(*) FROM current_field_definitions").fetchone()[0]
        if total != 23:
            raise ValueError("Expected exactly 23 current registry definitions")
        seen = set()
        for field in evidence["fields"]:
            field_id, revision_id = field["source_field_id"], field["revision_id"]
            if field_id in seen:
                raise ValueError("Repeated field in Phase B.4 evidence")
            seen.add(field_id)
            row = con.execute(
                "SELECT d.content_json, d.content_sha256 FROM current_field_definitions c "
                "JOIN field_definition_revisions d ON d.revision_id = c.revision_id "
                "WHERE c.source_field_id=? AND c.revision_id=?",
                (field_id, revision_id),
            ).fetchone()
            if row is None or row[1] != field["content_sha256"]:
                raise ValueError("Phase B.4 revision evidence differs from active Engine registry")
            definition = json.loads(row[0])
            if (
                definition.get("language") != "en"
                or definition.get("review_status") != "unreviewed"
                or definition.get("semantic_status") != "partially_defined"
                or "AI Description — added by FAIRmorph" not in definition.get("notes", "")
            ):
                raise ValueError("Unexpected registered field semantics or attribution")
            reviews = con.execute(
                "SELECT COUNT(*) FROM field_definition_reviews WHERE revision_id=?",
                (revision_id,),
            ).fetchone()[0]
            if reviews:
                raise ValueError("A registered source field has a separate review; do not silently treat it as an unreviewed PoC draft")
    return sha(file)


def build_rows(events_source, counts_source, cfg):
    sites = cfg["sites"]
    category = cfg["categories"]
    events = read_csv(events_source)
    counts = read_csv(counts_source)
    if len(events) != cfg["expected"]["source_events"] or len(counts) != cfg["expected"]["source_counts"]:
        raise ValueError("Pinned source record count changed")

    event_by_id = {}
    event_rows = []
    event_properties = {}
    for src in events:
        original = src["event_id"]
        if original in event_by_id or src["surveyed_pst"] not in ("TRUE", "FALSE"):
            raise ValueError("Repeated event key or invalid PST flag")
        start, end = date.fromisoformat(src["census_date_start"]), date.fromisoformat(src["census_date_end"])
        days = int(src["census_days"])
        if days != (end - start).days + 1:
            raise ValueError(f"Unexpected census_days semantics: {original}")
        event_by_id[original] = src
        locations = ["Core census locations"]
        if src["surveyed_pst"] == "TRUE":
            locations.append("Punta San Telmo")
        for site_name in locations:
            site = sites[site_name]
            event_id = f"{original}-{site['suffix']}"
            event_rows.append({
                "eventID": event_id,
                "eventDate": src["census_date_start"],
                "decimalLongitude": str(site["longitude"]),
                "decimalLatitude": str(site["latitude"]),
                "locality": site["locality"],
                "coordinateUncertaintyInMeters": str(site["coordinate_uncertainty_m"]),
                "sampleSizeValue": str(days),
                "sampleSizeUnit": "day" if days == 1 else "days",
                "eventRemarks": "Representative site location; survey start date of a multi-day window." if days > 1 else "Representative site location; not an exact animal position.",
                "samplingProtocol": cfg["method_doi"],
            })
            event_properties[event_id] = {
                "source_event_id": original,
                "source_location": site_name,
                "survey_start": src["census_date_start"],
                "survey_end": src["census_date_end"],
                "census_days": days,
                "research_program": src["research_program"],
                "species_count_totals": {},
            }
    if len({e["eventID"] for e in event_rows}) != len(event_rows):
        raise ValueError("Nonunique derived eventID")
    event_ids = set(event_properties)
    occurrence_rows = []
    pangaea_rows = []
    seen_ids = set()
    source_oracle = Counter()
    for row in counts:
        if row["event_id"] not in event_by_id or row["location"] not in sites:
            raise ValueError("Unlinked source count")
        event_id = f"{row['event_id']}-{sites[row['location']]['suffix']}"
        if event_id not in event_ids or not row["count_id"].startswith(f"{event_id}-"):
            raise ValueError("Missing site event or inconsistent count key")
        source_total = 0
        for column, semantics in category.items():
            value_text = row[column]
            if value_text == "":
                continue
            if not value_text.isascii() or not value_text.isdecimal():
                raise ValueError(f"Invalid nonnegative integer {column}")
            value = int(value_text)
            source_total += value
            occ_id = f"{row['count_id']}-{semantics['stage_code']}-{semantics['sex_code']}"
            if occ_id in seen_ids:
                raise ValueError("Duplicate derived occurrenceID")
            seen_ids.add(occ_id)
            source_oracle[(row["count_id"], row["event_id"], row["location"], row["species"], column, value)] += 1
            occurrence_rows.append({
                "occurrenceID": occ_id, "eventID": event_id,
                "scientificName": row["species"], "vernacularName": row["species_common"],
                "individualCount": str(value),
                "occurrenceStatus": "absent" if value == 0 else "present",
                "basisOfRecord": "HumanObservation",
                "lifeStage": semantics["stage"], "sex": semantics["sex"],
            })
            event = event_by_id[row["event_id"]]
            pangaea_rows.append({
                "Event ID": event_id,
                "Source count ID": row["count_id"],
                "Survey start date": event["census_date_start"],
                "Survey end date": event["census_date_end"],
                "Location group": row["location"],
                "Scientific name": row["species"],
                "Common name": row["species_common"],
                "Age class": semantics["stage"],
                "Sex class": semantics["sex"] or "sexes combined",
                "Count category": column,
                "Individual count": str(value),
                "Research program": event["research_program"],
            })
        if source_total != int(row["total_count"]):
            raise ValueError("Source total_count does not equal recorded component sum")
        totals = event_properties[event_id]["species_count_totals"]
        totals[row["species"]] = totals.get(row["species"], 0) + int(row["total_count"])
    return events, counts, event_rows, occurrence_rows, pangaea_rows, event_properties, source_oracle


def match_verified_run(project, run_id, expected, source_oracle):
    run_dir, manifest = verified_run(project, run_id)
    if manifest.get("schema_version") != "fairmorph.poc.run/2":
        raise ValueError("A verified generic RUN/2 is required")
    path = run_dir / "outputs/counts_with_events.parquet"
    if path.is_symlink() or not path.is_file() or not any(
        x["path"] == "outputs/counts_with_events.parquet" for x in manifest["artifacts"]
    ):
        raise ValueError("Expected RUN/2 count-and-event artifact missing")
    frame = pl.read_parquet(path)
    required = ["count_id", "event_id", "location", "species", "count_type", "count_value"]
    if not set(required).issubset(frame.columns):
        raise ValueError("RUN/2 lacks required provenance columns")
    actual = Counter(
        (str(r["count_id"]), str(r["event_id"]), str(r["location"]),
         str(r["species"]), str(r["count_type"]), int(r["count_value"]))
        for r in frame.select(required).iter_rows(named=True)
    )
    if actual != source_oracle:
        raise ValueError("RUN/2 count cells are not identical to the pinned source oracle")
    values = [int(r["count_value"]) for r in frame.select("count_value").iter_rows(named=True)]
    if len(values) != expected["occurrences"] or sum(x == 0 for x in values) != expected["zeros"] or sum(values) != expected["sum"]:
        raise ValueError("RUN/2 baseline counts differ")
    return sha(run_dir / "manifest.json")


def dwca_meta_xml():
    ET.register_namespace("", DWC_TEXT)
    root = ET.Element(f"{{{DWC_TEXT}}}archive")
    for kind, name, columns in (
        ("core", "Event", EVENT_FIELDS), ("extension", "Occurrence", OCC_FIELDS)
    ):
        item = ET.SubElement(root, f"{{{DWC_TEXT}}}{kind}", {
            "encoding": "UTF-8", "fieldsTerminatedBy": ",",
            "linesTerminatedBy": "\\n", "fieldsEnclosedBy": "\"",
            "ignoreHeaderLines": "1", "rowType": DWC + name,
        })
        files = ET.SubElement(item, f"{{{DWC_TEXT}}}files")
        ET.SubElement(files, f"{{{DWC_TEXT}}}location").text = name + ".csv"
        key = "id" if kind == "core" else "coreid"
        ET.SubElement(item, f"{{{DWC_TEXT}}}{key}", {
            "index": str(columns.index("eventID"))
        })
        for index, column in enumerate(columns):
            ET.SubElement(item, f"{{{DWC_TEXT}}}field", {
                "index": str(index), "term": DWC + column
            })
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def zip_dwca(output):
    path = output / "cs-phoc-test.dwca.zip"
    names = ["Event.csv", "Occurrence.csv", "meta.xml"]
    with zipfile.ZipFile(path, "w") as zipped:
        for name in names:
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            zipped.writestr(info, (output / name).read_bytes())
    result = validate_dwca_archive(path)
    if result["schema_validated"] is not True or result["references_verified"] is not True:
        raise ValueError("DwC-A archive did not pass official schema validation")
    return path, result


def geojson(event_rows, event_properties, cfg):
    features = []
    for row in event_rows:
        id_ = row["eventID"]
        properties = event_properties[id_]
        feature = {
            "type": "Feature",
            "id": id_,
            "geometry": {
                "type": "Point",
                "coordinates": [
                    float(row["decimalLongitude"]), float(row["decimalLatitude"])
                ],
            },
            "properties": {
                "eventID": id_,
                **properties,
                "total_individuals_counted": sum(properties["species_count_totals"].values()),
                "coordinate_uncertainty_m": int(row["coordinateUncertaintyInMeters"]),
                "position_meaning": "Representative census site coordinate, not an individual animal location",
                "data_status": "test_only_not_for_publication",
            },
        }
        if not (-180 <= feature["geometry"]["coordinates"][0] <= 180
                and -90 <= feature["geometry"]["coordinates"][1] <= 90):
            raise ValueError("GeoJSON coordinate out of range")
        features.append(feature)
    return {"type": "FeatureCollection", "features": features}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True, help="Existing registered Phase B.4 FAIRmorph project")
    parser.add_argument("--run-id", required=True, help="Existing immutable, verified generic RUN/2")
    parser.add_argument("--output", type=Path, required=True, help="New, nonexistent TEST output directory")
    args = parser.parse_args()
    project = args.project.resolve()
    output = args.output.resolve()
    if output.exists() or output.is_symlink():
        parser.error("Output must be a NEW, nonexistent directory; existing output is never overwritten")
    cfg = load_json(CONFIG_PATH)
    resources = source_resources(project, cfg)
    registry_sha = validate_field_drafts(project, resources)
    sources, counts, events, occ, tsv, event_properties, oracle = build_rows(
        resources["events"]["path"], resources["counts"]["path"], cfg
    )
    run_sha = match_verified_run(project, args.run_id, cfg["expected"], oracle)
    expected = cfg["expected"]
    if (len(events), len(occ), sum(int(r["individualCount"]) == 0 for r in occ),
        sum(int(r["individualCount"]) for r in occ)) != (
        expected["events"], expected["occurrences"], expected["zeros"], expected["sum"]
    ):
        raise ValueError("Export preflight baseline mismatch")
    if len(tsv) != len(occ) or set(r["eventID"] for r in occ) - set(r["eventID"] for r in events):
        raise ValueError("Export row alignment or foreign-key failure")
    features = geojson(events, event_properties, cfg)
    if len(features["features"]) != len(events):
        raise ValueError("GeoJSON event count mismatch")
    if sum(f["properties"]["total_individuals_counted"] for f in features["features"]) != expected["sum"]:
        raise ValueError("GeoJSON sum differs from original count totals")

    output.mkdir(parents=True)
    try:
        write_table(output / "Event.csv", EVENT_FIELDS, sorted(events, key=lambda x: x["eventID"]))
        write_table(output / "Occurrence.csv", OCC_FIELDS, sorted(occ, key=lambda x: x["occurrenceID"]))
        write_table(output / "pangaea-test.tsv", list(tsv[0]), sorted(tsv, key=lambda x: (x["Event ID"], x["Source count ID"], x["Count category"])), delimiter="\t")
        write_json(output / "site-events.geojson", features)
        (output / "meta.xml").write_bytes(dwca_meta_xml())
        zip_path, archive_validation = zip_dwca(output)
        metadata = {
            "title": "CS-PHOC FAIRmorph v0.13 local test exports",
            "language": "en", "status": cfg["status"],
            "description_provenance": cfg["description_provenance"],
            "source_attribution": "CS-PHOC original dataset and Woodman et al. (2024); FAIRmorph is not the publisher or dataset owner.",
            "source_repository_commit": cfg["source_commit"],
            "source_doi": cfg["source_doi"], "method_doi": cfg["method_doi"],
            "projection": "FAIRmorph dataset-specific test, derived from immutable original CSV and compared cell-by-cell with verified generic RUN/2.",
            "description": "No publication, submission, publisher endorsement, population estimate, or precise animal geolocation is claimed.",
            "caveats": cfg["caveats"],
            "format_scope": cfg["format_scope"],
            "pangaea_note": "Tab-delimited, UTF-8 data-file preparation only; PANGAEA requires submission metadata, editorial processing and acceptance.",
            "geojson_coordinate_system": "WGS 84 longitude, latitude (RFC 7946)",
        }
        write_json(output / "test-metadata.json", metadata)
        artifacts = {
            name: sha(output / name)
            for name in ["Event.csv", "Occurrence.csv", "pangaea-test.tsv",
                         "site-events.geojson", "meta.xml", zip_path.name, "test-metadata.json"]
        }
        report = {
            "status": "passed", "scientific_approval": False, "publication_ready": False,
            "export_formats": ["dwca/1", "pangaea-preparation-tsv", "geojson/rfc7946"],
            "source_run_id": args.run_id, "run_manifest_sha256": run_sha,
            "phase_b_field_evidence_sha256": registry_sha,
            "projection_config_sha256": sha(CONFIG_PATH),
            "source_resource_ids": {role: r["id"] for role, r in resources.items()},
            "source_sha256": cfg["source_sha256"],
            "source_rows": {"events": len(sources), "counts": len(counts)},
            "derived_rows": {"events": len(events), "occurrences": len(occ),
                             "pangaea_tsv": len(tsv), "geojson_features": len(features["features"])},
            "explicit_zero_count_values": sum(int(r["individualCount"]) == 0 for r in occ),
            "count_sum": sum(int(r["individualCount"]) for r in occ),
            "cell_by_cell_run_match": True, "source_to_occurrence_references_verified": True,
            "dwca_meta_xsd_validated": archive_validation["schema_validated"],
            "dwca_archive_references_verified": archive_validation["references_verified"],
            "artifacts_sha256": artifacts,
            "description_provenance": cfg["description_provenance"],
        }
        write_json(output / "test-report.json", report)
        print(json.dumps({
            "status": report["status"], "output": str(output),
            "derived_rows": report["derived_rows"],
            "count_sum": report["count_sum"],
            "dwca_meta_xsd_validated": report["dwca_meta_xsd_validated"],
            "publication_ready": False,
            "test_report": str(output / "test-report.json"),
        }, indent=2))
    except BaseException:
        (output / "INCOMPLETE").write_text("TEST export did not finish successfully.\n", encoding="utf-8")
        raise


if __name__ == "__main__":
    main()
