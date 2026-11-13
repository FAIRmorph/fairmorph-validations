# CS-PHOC — Scientific Curation Baseline, **Not an Engine Approval**

> **Historical context:** This document records the initial pre-registration curation questions. Its table statuses and outstanding decisions describe that initial stage; they are **not current registration status**. Subsequently, 23 English FAIRmorph AI-assisted field-description drafts were registered as **unreviewed** Engine revisions. The technical technical test exports were validated, but no formal field or mapping approval was recorded. See [Phase B Registry Drafts](../validation/PHASE-B-REGISTRY-DRAFTS.md) and the [technical closure checkpoint](../validation/CS-PHOC-TECHNICAL-CLOSURE.md). The AI-assisted descriptions are not authored, reviewed, approved, or endorsed by the original CS-PHOC authors or owners.

## Sources

- Scientific project source: [US AMLR / CS-PHOC](https://github.com/us-amlr/cs-phoc/tree/64f0b77e631c711c681306bbb56a7636ae91a471)
- Primary CSV documentation: [data/manuscript/README.md](https://github.com/us-amlr/cs-phoc/blob/64f0b77e631c711c681306bbb56a7636ae91a471/data/manuscript/README.md)
- Publication transformation logic: [R/data_to_dwca.R](https://github.com/us-amlr/cs-phoc/blob/64f0b77e631c711c681306bbb56a7636ae91a471/R/data_to_dwca.R)

All statements in this document are drawn from the sources above or explicitly marked as **interpretations requiring confirmation**. This curation note does not replace a `SourceFieldDefinition` contract; the Engine Registry must have a separate, reviewed revision for **each field** before formal approval.

## Identities and Tables

| CSV | Field | Source-supported meaning | Registration status at initial review |
|---|---|---|---|
| events | `event_id` | Unique identifier of a survey-window record; joins to counts | Not yet registered |
| events | `season_name` | Field-season designation | Not yet registered |
| events | `census_date_start` | Beginning of the census window (actual CSV header) | Not yet registered |
| events | `census_date_end` | End of the census window (actual CSV header) | Not yet registered |
| events | `census_days` | Duration in days as described by the source documentation | Not yet registered |
| events | `surveyed_pst` | Whether Punta San Telmo was surveyed | Not yet registered |
| events | `research_program` | `INACH` or `USAMLR` | Not yet registered |
| counts | `count_id` | Unique count-record key; **not automatically** a Darwin Core `occurrenceID` | Not yet registered |
| counts | `event_id` | Associated source survey window | Not yet registered |
| counts | `location` | Census location | Not yet registered |
| counts | `species` | Scientific species name as recorded in the original dataset | Not yet registered |
| counts | `species_common` | Common species name as documented | Not yet registered |
| counts | `total_count` | Sum of the other component count columns, already present in the original source | Not yet registered |

**Documentation discrepancy:** The upstream file documentation also refers to the date fields as `census_start_date` and `census_end_date`, whereas the actual CSV headers are **`census_date_start`** and **`census_date_end`**. Do not silently introduce aliases or modify the original file. At the initial review stage, the discrepancy required clarification against the source authors' or manuscript documentation. The subsequent Phase B evidence separately checks the actual headers and inclusive `census_days` calculation.

## Explicit Count Fields

The upstream documentation describes the following ten fields. For **all ten**, an empty CSV value means *no count value was collected or recorded* and must not be replaced with the number zero. An explicit `0` is a recorded zero count and **must be preserved**. **Qualification from subsequent Phase B evidence:** Some zeros may have been generated during upstream data harmonization or completion; do not claim that every zero was directly observed in the field.

| Count field | Scientific meaning documented in the upstream README |
|---|---|
| `ad_female_count` | Adult female animals |
| `ad_male_count` | Adult male animals |
| `ad_unk_count` | Adult animals of unknown sex |
| `juv_female_count` | Juvenile female animals |
| `juv_male_count` | Juvenile male animals |
| `juv_unk_count` | Juvenile animals of unknown sex |
| `pup_count` | Pups younger than one year, **all sexes combined** |
| `unk_female_count` | Animals of unknown age class, female |
| `unk_male_count` | Animals of unknown age class, male |
| `unk_unk_count` | Animals of unknown age class and unknown sex |

**Checks required before formal confirmation:** Establish the scientific counting unit (animals/individuals), precisely what `0` implies about observed absence within the relevant count context, the encoding of missing information, and the distinctions between count, Observation, and Occurrence. The Engine must not infer these decisions from column names. For `total_count`, **do not** invent a second independent measurement: it is an already computed sum in the source material.

## Target Projections Explicitly Unconfirmed at Initial Review

- `SamplingEvent`: Source `event_id` identifies a survey window. In the published DwC-A, events are further split by location group, using `-1`/`-2` suffixes in `eventID`. **Do not** silently treat these two identities as equivalent.
- `MeasurementOrFact`: One recorded count cell per `count_id × count_type` is a **possible** scientific projection; formal adoption requires SourceFieldDefinition review and approval of the profile/entity mapping. Preserve `0` and omit blanks.
- `Occurrence`: The published DwC-A contains `occurrenceID` values incorporating age and sex codes; any target projection must version this distinct identifier rule explicitly.
- Relationships: The source relation is `counts.event_id → events.event_id`, technically checked against unique event keys. This is not automatically a scientifically approved `MeasurementOrFact.sampling_event_ref` relationship.
- Profiles: Use only explicitly confirmed Engine-registered schema versions pinned to their exact SHA-256 hashes.

## Outstanding Decisions / Review Questions from the Initial Curation Stage

1. Which Entity type is appropriate for CS-PHOC count values: `Occurrence` with `individualCount`, `MeasurementOrFact` as a count measurement, or both, without duplicating their scientific meaning?
2. When should a single CSV event record become one or two Darwin Core sampling events? The upstream R scripts establish the publication decision, not the raw import.
3. What citable, responsible-party-confirmed source supports each field definition, including the `census_days` calculation?
4. How should age and sex codes for `pup_count` and `unk_*_count` be explicitly transferred into a separate later publication configuration?
5. Which value and immutable revision constitute the confirmed project/publication metadata (EML)? The supplied title was only an unconfirmed draft.

**No person, approval, or schema pin is fabricated in these templates.**

**Later PoC outcome:** The published-style Event/Occurrence transformation was documented and independently validated as a **test export** in [C.1–C.4](../validation/C1-C4-TEST-EXPORTS.md). This does not retrospectively turn the initial review questions into formal Engine approvals.
