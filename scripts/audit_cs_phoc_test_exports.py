#!/usr/bin/env python3
"""Read-only independent content/format audit of local CS-PHOC C1-C4 TEST exports.

Reads exported files, original imported CSV objects, and verified RUN identity.
Writes a small English-only audit report outside the exported directory.
No exports are republished, uploaded, regenerated, or modified.
"""
import argparse
import csv
import hashlib
import json
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET

from fairmorph_engine.core.publication_adapters import validate_dwca_archive

ROOT = Path(__file__).resolve().parents[1]
CFG = ROOT / "cs-phoc/configurations/drafts/c1-c4-test-projection.json"
REQUIRED = ("Event.csv", "Occurrence.csv", "meta.xml", "cs-phoc-test.dwca.zip",
            "pangaea-test.tsv", "site-events.geojson", "test-metadata.json", "test-report.json")


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_rows(path, delimiter=","):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=delimiter))


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def audit(project, directory):
    cfg = load(CFG)
    report = load(directory / "test-report.json")
    metadata = load(directory / "test-metadata.json")
    require(set(REQUIRED).issubset({p.name for p in directory.iterdir() if p.is_file()}),
            "Missing expected test export files")
    require(report["status"] == "passed" and report["publication_ready"] is False
            and report["scientific_approval"] is False, "Incorrect test-only status")
    require(metadata["status"] == "test_only_not_for_publication"
            and "AI Description — added by FAIRmorph" in metadata["description_provenance"],
            "Missing FAIRmorph-only AI attribution")
    require(report["projection_config_sha256"] == digest(CFG), "Changed projection config")
    require(report["phase_b_field_evidence_sha256"] ==
            digest(project / "validation/phase-b-field-drafts.json"),
            "Phase B.4 revisions do not match")
    run = project / "runs" / report["source_run_id"] / "manifest.json"
    require(digest(run) == report["run_manifest_sha256"], "Changed RUN manifest")
    for name, expected_sha in report["artifacts_sha256"].items():
        require(name in REQUIRED and digest(directory / name) == expected_sha,
                f"Exported artifact modified: {name}")

    sources = {}
    for role, sha256 in cfg["source_sha256"].items():
        source = project / "objects/sha256" / sha256[:2] / sha256
        require(source.is_file() and digest(source) == sha256, f"Source {role} differs")
        sources[role] = read_rows(source)
    events, occ = read_rows(directory / "Event.csv"), read_rows(directory / "Occurrence.csv")
    tsv = read_rows(directory / "pangaea-test.tsv", delimiter="\t")
    geo = load(directory / "site-events.geojson")
    require(len(events) == 536 and len(occ) == 16940 and len(tsv) == 16940,
            "Export table rows differ")
    require(geo["type"] == "FeatureCollection" and len(geo["features"]) == 536,
            "GeoJSON collection or count differs")
    require(len(set(r["eventID"] for r in events)) == 536, "Duplicate event ID")
    require(len(set(r["occurrenceID"] for r in occ)) == 16940, "Duplicate occurrence ID")
    require(all(set(r) == set(events[0]) for r in events), "Event columns vary")
    require(all(set(r) == set(occ[0]) for r in occ), "Occurrence columns vary")
    event_map = {row["eventID"]: row for row in events}
    require(all(r["eventID"] in event_map for r in occ), "Orphan occurrence")
    require(all(r["occurrenceStatus"] == ("absent" if int(r["individualCount"]) == 0 else "present")
                for r in occ), "Zero/presence status does not follow source projection")
    require(Counter(r["occurrenceStatus"] for r in occ) ==
            Counter({"absent": 11599, "present": 5341}), "Zero/positive totals differ")
    require(sum(int(r["individualCount"]) for r in occ) == 79232, "Occurrence sum differs")

    # Cross-format cell equality is independent of list order and row serialization.
    # Source count ID + category are encoded into published-style occurrence IDs.
    source_events = {e["event_id"]: e for e in sources["events"]}
    require(len(source_events) == 322, "Source event IDs differ")
    expected_events = {}
    for event_id, source in source_events.items():
        for site_name in (["Core census locations"] +
                          (["Punta San Telmo"] if source["surveyed_pst"] == "TRUE" else [])):
            site = cfg["sites"][site_name]
            key = f"{event_id}-{site['suffix']}"
            expected_events[key] = (source, site_name, site)
    require(set(expected_events) == set(event_map), "Site split differs from pinned source")
    for event_id, (source, _, site) in expected_events.items():
        actual = event_map[event_id]
        require(actual["eventDate"] == source["census_date_start"]
                and int(actual["sampleSizeValue"]) == int(source["census_days"])
                and float(actual["decimalLongitude"]) == site["longitude"]
                and float(actual["decimalLatitude"]) == site["latitude"]
                and int(actual["coordinateUncertaintyInMeters"]) == site["coordinate_uncertainty_m"],
                f"Event mapping differs: {event_id}")

    expected_occ = {}
    expected_tsv = {}
    missing_cells = 0
    for row in sources["counts"]:
        event_id = f"{row['event_id']}-{cfg['sites'][row['location']]['suffix']}"
        require(event_id in expected_events, "Source Count references non-surveyed event")
        for col, category in cfg["categories"].items():
            val = row[col]
            if val == "":
                missing_cells += 1
                continue
            count = int(val)
            oid = f"{row['count_id']}-{category['stage_code']}-{category['sex_code']}"
            require(oid not in expected_occ, "Duplicate source-derived occurrence")
            expected_occ[oid] = (event_id, row["species"], count, category)
            key = (event_id, row["count_id"], col)
            expected_tsv[key] = (
                count, category["stage"], category["sex"] or "sexes combined",
                row["species"], row["location"], source_events[row["event_id"]]["research_program"]
            )
    require(missing_cells == 4500, "Unexpected missing source count cells")
    require(set(expected_occ) == set(r["occurrenceID"] for r in occ),
            "Omitted/extra occurrences or unwanted missing-to-zero substitution")
    for row in occ:
        event_id, species, value, cat = expected_occ[row["occurrenceID"]]
        require(row["eventID"] == event_id and row["scientificName"] == species
                and int(row["individualCount"]) == value
                and row["lifeStage"] == cat["stage"] and row["sex"] == cat["sex"],
                f"Occurrence source/sample mismatch: {row['occurrenceID']}")
    actual_tsv = {}
    for row in tsv:
        key = (row["Event ID"], row["Source count ID"], row["Count category"])
        require(key not in actual_tsv, "Duplicate PANGAEA TSV category key")
        actual_tsv[key] = (
            int(row["Individual count"]), row["Age class"], row["Sex class"],
            row["Scientific name"], row["Location group"], row["Research program"]
        )
    require(actual_tsv == expected_tsv, "PANGAEA TSV not identical to source categories")
    require(all("\t" not in row["Scientific name"] for row in tsv), "Unexpected embedded tab")

    features = geo["features"]
    feature_map = {f["id"]: f for f in features}
    require(len(feature_map) == len(features) and set(feature_map) == set(event_map),
            "GeoJSON event correspondence differs")
    aggregated = defaultdict(lambda: defaultdict(int))
    for source in sources["counts"]:
        event_id = f"{source['event_id']}-{cfg['sites'][source['location']]['suffix']}"
        aggregated[event_id][source["species"]] += int(source["total_count"])
    coord_counter = Counter()
    for eid, feature in feature_map.items():
        source, location, site = expected_events[eid]
        coords = feature["geometry"]["coordinates"]
        require(feature["type"] == "Feature" and feature["geometry"]["type"] == "Point"
                and len(coords) == 2, "Unexpected GeoJSON feature geometry")
        require(coords == [site["longitude"], site["latitude"]], "Site coordinate mapping differs")
        require(-180 <= coords[0] <= 180 and -90 <= coords[1] <= 90,
                "Invalid WGS84 lon/lat range")
        coord_counter[location] += 1
        props = feature["properties"]
        require(props["eventID"] == eid and props["source_location"] == location
                and props["source_event_id"] == source["event_id"]
                and props["species_count_totals"] == dict(aggregated[eid])
                and props["total_individuals_counted"] == sum(aggregated[eid].values())
                and props["coordinate_uncertainty_m"] == site["coordinate_uncertainty_m"]
                and "not an individual animal location" in props["position_meaning"],
                "GeoJSON semantics or aggregated values differ")
    require(coord_counter == Counter({"Core census locations": 322, "Punta San Telmo": 214}),
            "Unexpected GeoJSON location feature distribution")

    archive = directory / "cs-phoc-test.dwca.zip"
    schema_validation = validate_dwca_archive(archive)
    require(schema_validation["schema_validated"] and schema_validation["references_verified"],
            "DwC-A schema validation failed")
    with zipfile.ZipFile(archive) as z:
        require(set(z.namelist()) == {"Event.csv", "Occurrence.csv", "meta.xml"},
                "Unexpected ZIP contents")
        for name in ("Event.csv", "Occurrence.csv", "meta.xml"):
            require(z.read(name) == (directory / name).read_bytes(),
                    f"Archive member does not match exported file: {name}")
    root = ET.fromstring((directory / "meta.xml").read_bytes())
    ns = {"d": "http://rs.tdwg.org/dwc/text/"}
    sections = root.findall("d:core", ns) + root.findall("d:extension", ns)
    require(len(sections) == 2, "Expected Event core and Occurrence extension")
    require(sections[0].get("rowType", "").endswith("/Event") and
            sections[1].get("rowType", "").endswith("/Occurrence"),
            "Incorrect Darwin Core record types")

    # Fixed, source-grounded samples cover positive, explicit zero, blank,
    # Core/PST split, and pup-sex aggregation. Evaluate against BOTH exports.
    sample_checks = {}
    sample_cases = [
        ("positive_pup", "1-1-344008", "pup_count", 1),
        ("explicit_zero", "1-1-344008", "ad_female_count", 0),
        ("blank_omitted", "1-1-344008", "unk_female_count", None),
        ("zero_total_with_missing", "1-1-231417", "unk_unk_count", None),
        ("pst_positive", "1-2-231413", "juv_male_count", 11),
        ("pup_sexes_combined", "1-1-231413", "pup_count", 73),
        ("unknown_age_recorded_zero", "1-1-231413", "unk_unk_count", 0),
    ]
    source_counts = {row["count_id"]: row for row in sources["counts"]}
    for label, count_id, col, value in sample_cases:
        source = source_counts[count_id]
        require((None if source[col] == "" else int(source[col])) == value,
                f"Source sample differs from expected reference: {label}")
        sem = cfg["categories"][col]
        oid = f"{count_id}-{sem['stage_code']}-{sem['sex_code']}"
        key = (f"{source['event_id']}-{cfg['sites'][source['location']]['suffix']}", count_id, col)
        actual_occ = [r for r in occ if r["occurrenceID"] == oid]
        actual_tsv_row = [r for r in tsv if
                          (r["Event ID"], r["Source count ID"], r["Count category"]) == key]
        require(len(actual_occ) == len(actual_tsv_row) == (0 if value is None else 1),
                f"CSV/TSV sample presence mismatch: {label}")
        if value is not None:
            require(int(actual_occ[0]["individualCount"]) ==
                    int(actual_tsv_row[0]["Individual count"]) == value,
                    f"Count sample value mismatch: {label}")
            if col == "pup_count":
                require(actual_occ[0]["sex"] == "" and
                        actual_tsv_row[0]["Sex class"] == "sexes combined",
                        "Pup sex aggregation mislabelled")
        sample_checks[label] = {"count_id": count_id, "source_category": col,
                                "source_value": value, "export_rows": len(actual_occ),
                                "status": "passed"}

    return {
        "status": "passed",
        "audit_kind": "independent_read_only_export_content_audit/1",
        "language": "en",
        "test_only_not_for_publication": True,
        "description_origin": "FAIRmorph AI-assisted PoC description; not endorsed by CS-PHOC authors",
        "source_run_id": report["source_run_id"],
        "checks": {
            "export_sha256_verified": True,
            "source_byte_sha256_verified": True,
            "phase_b_revision_evidence_verified": True,
            "run_manifest_sha256_verified": True,
            "dwca_meta_xsd_and_zip_members": True,
            "all_16940_occurrences_equal_original_cells": True,
            "all_16940_tsv_rows_equal_original_cells": True,
            "4500_missing_cells_omitted": True,
            "11599_explicit_zero_cells_preserved": True,
            "536_geojson_features_equal_source_events_and_totals": True,
            "representative_coordinate_meaning_verified": True,
        },
        "counts": {
            "source_event_rows": len(sources["events"]),
            "source_count_rows": len(sources["counts"]),
            "events": len(events),
            "occurrences": len(occ),
            "pangaea_tsv_rows": len(tsv),
            "geojson_features": len(features),
            "missing_source_category_cells": missing_cells,
            "explicit_zero_values": sum(int(r["individualCount"]) == 0 for r in occ),
            "individual_count_sum": sum(int(r["individualCount"]) for r in occ),
        },
        "sample_checks": sample_checks,
        "geojson_site_feature_counts": dict(coord_counter),
        "findings": [
            "DwC-A contains no EML metadata; it is a test archive, not publisher-ready.",
            "PANGAEA TSV is preparation data, not a published or accepted PANGAEA record.",
            "GeoJSON contains representative site coordinates, not animal locations.",
            "Source pup_count sexes are combined; never interpret the occurrenceID code as an observed unknown sex.",
            "FAIRmorph's source description and publication projection are PoC additions, not CS-PHOC owner endorsements.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--exports", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    if args.report.exists():
        parser.error("Report path already exists; refusing overwrite")
    data = audit(args.project.resolve(), args.exports.resolve())
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": data["status"], "checked_occurrences": data["counts"]["occurrences"],
                      "sample_checks_passed": len(data["sample_checks"]),
                      "report": str(args.report.resolve())}, indent=2))


if __name__ == "__main__":
    main()
