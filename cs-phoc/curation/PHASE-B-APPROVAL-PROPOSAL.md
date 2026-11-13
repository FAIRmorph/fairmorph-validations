# CS-PHOC Phase B — Begründeter Freigabevorschlag (keine Freigabe)

**Stand:** 2026-11-13  
**Status:** REVIEW PROPOSAL — NOT APPROVED; NO REGISTRY WRITE  
**Gültigkeitsbereich:** Quellsemantik der 23 CSV-Felder des fixierten CS-PHOC-Commits `64f0b77e631c711c681306bbb56a7636ae91a471`. Keine wissenschaftliche Validierung eines DwC-/FAIRmorph-Zielmappings.

## Evidenzhierarchie

1. [Woodman et al. (2024), Scientific Data, DOI 10.1038/s41597-024-03744-9](https://doi.org/10.1038/s41597-024-03744-9): Methoden, Standardisierung, Beobachtungsgegenstand, Einschränkungen, technische Validierung.
2. [Fixierte Original-CSV-Feldbeschreibung](https://github.com/us-amlr/cs-phoc/blob/64f0b77e631c711c681306bbb56a7636ae91a471/data/manuscript/README.md): Feldnamen und Wertsemantik.
3. [Fixiertes Erstellungsskript](https://github.com/us-amlr/cs-phoc/blob/64f0b77e631c711c681306bbb56a7636ae91a471/R/manuscript_data.R): Quelltabellengenerierung, Zero-Completion, Aggregation.
4. [Fixiertes DwC-A-Skript](https://github.com/us-amlr/cs-phoc/blob/64f0b77e631c711c681306bbb56a7636ae91a471/R/data_to_dwca.R) und [Upstream-README](https://github.com/us-amlr/cs-phoc/blob/64f0b77e631c711c681306bbb56a7636ae91a471/README.md): **separate** Publikationsprojektion.
5. [Phase-B-Quell- und Polars-Evidenz](PHASE-B-NULL-MISSING-EVIDENCE.md) und [Feldinventar](PHASE-B-SOURCE-FIELD-DEFINITIONS.md): technisch belegte Eigenschaften des fixierten PoC-Standes.

**Versionierungswarnung:** Die 2024er Publikation beschreibt 284 Zensen zum damaligen Publikationsstand; die fixierte spätere CSV-Revision enthält 322. Die aktuell online veröffentlichte DwC-A-Fassung kann erneut eine andere Datenrevision sein. Nicht unbemerkt als identische Revisionen vergleichen.

## Zentrale Erkenntnis: explizite Null vs. Quelle der Null

Der Artikel beschreibt: INACH-Daten enthielten explizite Nullen; U.S.-AMLR-Daten enthielten zunächst überwiegend Nicht-Null-Count-Einträge und wurden bei der Standardisierung um notwendige Null-Records ergänzt. Core-Standorte wurden über Teilgebiete aggregiert; Pup-Alters-/Geschlechtsdetails wurden zu einem einzigen Pup-Count vereinheitlicht. Das fixierte `R/manuscript_data.R` enthält dazu `complete_csphoc()` sowie ausdrücklich nachgetragene Nullzeilen für PST-Erhebungen ohne Phocid-Einträge.

**Deshalb nicht freigeben:** „Jede 0 wurde direkt vor Ort als 0 protokolliert.“  
**Freigabefähige präzise Quellbedeutung:** „Ein explizites `0` ist im **standardisierten, veröffentlichten CS-PHOC-CSV** ein vorhandener Nullzählwert für die betreffende Art/Count-Kategorie/Erhebungseinheit. Er kann aus dokumentierter Datenstandardisierung/Completion hervorgegangen sein. Eine leere Zelle bedeutet dagegen, dass für diese Count-Kategorie kein Datenwert aufgezeichnet wurde; sie darf nicht als `0` ausgegeben werden.“

Die Publikationsregel `individualCount==0 → occurrenceStatus='absent'` ist als Upstream-DwC-A-Projektion belegbar, aber **nicht** als allgemeingültige Aussage über regionale Artabwesenheit, Nichtbeobachtung außerhalb des Zensusraums oder Bestandsentwicklung zu genehmigen.

## Entscheidungsvorschläge zu allen 23 Quellfeldern

„**A**“ = fachliche Quellbeschreibung zur **expliziten** Freigabe empfehlen, auf fixierte Revision begrenzt, keine bereits erteilte Freigabe. „**B**“ = nur mit ausdrücklich vermerkter Einschränkung/Interpretation. „**C**“ = zusätzliche fachliche Entscheidung vor endgültiger semantischer Festlegung erforderlich.

| Tabelle | Feld | Vorschlag | Konkret freigebbare Quellbedeutung / Grenze |
|---|---|---|---|
| events | `event_id` | A | Textidentifikator des Survey Windows und Quell-Joins; kein DwC `eventID` |
| events | `season_name` | A | Ursprüngliche Feldsaisonbezeichnung als Text; keine automatische Kalenderjahrsableitung |
| events | `census_date_start` | B | Tatsächlicher CSV-Header; Beginn des Survey Windows; README schreibt abweichend `census_start_date`; keine stille Aliasregistrierung |
| events | `census_date_end` | B | Tatsächlicher CSV-Header; Ende des Survey Windows; README schreibt abweichend `census_end_date` |
| events | `census_days` | B | In 322/322 Quellzeilen `end-start+1` Kalendertage; Manuskript beschreibt ein- bis dreitägige Fenster, CSV-README formuliert inkonsistent `end-start`; als **inklusive erfasste Kalendertage**, nicht Arbeitsstunden oder Aufwand, freigeben |
| events | `surveyed_pst` | A | Boolean: PST im Survey Window untersucht; `FALSE` ist **nicht** Nachweis der Abwesenheit von Phociden |
| events | `research_program` | A | In der Quelle `INACH` oder `USAMLR`; Attribut des Erhebungsprogramms, kein individueller Bearbeiter |
| counts | `count_id` | A | Eindeutige Textidentität einer Quell-Count-Zeile; keine automatisch gültige `occurrenceID` |
| counts | `event_id` | A | Text-Fremdschlüssel zu `events.event_id`; keine freigegebene FAIRmorph-Entity-Relation |
| counts | `location` | B | Quell-Ortsgruppe, insbesondere `Core census locations` oder `Punta San Telmo`; Core ist **aggregierte Fläche**, keine feste Einzelbeach-Geometrie |
| counts | `species` | A | Wissenschaftlicher Artenname **wie im Quell-CSV**, nicht automatisch aktueller akzeptierter WoRMS-Name oder taxonomischer Identifier |
| counts | `species_common` | A | Gebräuchlicher Artenname wie im Quell-CSV; keine automatische Sprach-/Taxonomie-Normalisierung |
| counts | `total_count` | B | Von den zehn Komponenten abgeleitete Quellsumme für Event × Standortgruppe × Art; leere Komponenten bleiben fehlend, keine elfte eigenständige Zählung |
| counts | `ad_female_count` | B | Aggregierte Anzahl erwachsener weiblicher Individuen im untersuchten Zensuskontext |
| counts | `ad_male_count` | B | Aggregierte Anzahl erwachsener männlicher Individuen |
| counts | `ad_unk_count` | B | Aggregierte Anzahl erwachsener Individuen mit nicht bestimmtem Geschlecht |
| counts | `juv_female_count` | B | Aggregierte Anzahl juveniler weiblicher Individuen |
| counts | `juv_male_count` | B | Aggregierte Anzahl juveniler männlicher Individuen |
| counts | `juv_unk_count` | B | Aggregierte Anzahl juveniler Individuen mit nicht bestimmtem Geschlecht |
| counts | `pup_count` | B | Aggregierte Anzahl Pups (Jungtiere unter einem Jahr), **beide/alle Geschlechter zusammen**; `any sex` ist nicht gleichbedeutend mit `unknown sex` |
| counts | `unk_female_count` | B | Aggregierte Anzahl weiblicher Individuen unbekannter Altersklasse |
| counts | `unk_male_count` | B | Aggregierte Anzahl männlicher Individuen unbekannter Altersklasse |
| counts | `unk_unk_count` | B | Aggregierte Anzahl Individuen, deren Altersklasse und Geschlecht unbekannt sind |

Für die zehn Count-Felder gelten gemeinsam:
- **Quellrepräsentation:** leer oder ganzzahlig `>=0` im fixierten Bestand; einheitenbezogener Vorschlag `counting_unit = "individuals"`.
- **Beobachtungsgegenstand:** lebende, **an Land ruhende/aufgehaltene** Phociden, die beim Zensus erfasst wurden; keine Populationsschätzung, keine See-/Eisbeobachtungen.
- **Aggregation:** standardisierter Count pro Survey Window × Ortsgruppe × Art × Alters-/Geschlechtskategorie; nicht als Zählung pro einzelner ursprünglicher Beobachtungsstelle interpretieren.
- **Missing:** leeres Feld = keine Zahl für diese Kategorie aufgezeichnet; `0` = standardisierter, vorhandener Nullzählwert; nie Missing zu Null konvertieren.
- **Alters-/Geschlechtsmethoden:** Zuordnungen entsprechen der dokumentierten aggregierten Quellkategorie; detaillierte biologische Klassifikationskriterien oder Sicherheit der Geschlechtsbestimmung sind nicht aus dem CSV zu rekonstruieren.
- **Vorsicht:** Beobachtete Counts hängen u. a. von Haul-out-Verhalten, Wetter, Uhrzeit und zeitlich veränderlichen Erhebungsbedingungen ab. Keine implizite ökologische Bestands-/Abwesenheitsbehauptung.

## Empfohlene Freigabeentscheidung für Phase B

**Empfehlung: bedingte Einzelgenehmigung aller 23 *Quellfelddefinitionen* nach fachlicher Durchsicht dieses Entwurfs**, begrenzt auf die oben präzisierten, versionierten Aussagen. Die „B“-Felder sind genehmigungsfähig **mit den aufgeführten Einschränkungen**, nicht unter stärkeren unbewiesenen Annahmen. Keine Quelle erfordert die Erfindung eines zusätzlichen Entitätstyps.

Vor dem Auslösen tatsächlicher `review_field(..., decision="approved", reviewer=...)`-Ereignisse müssen ein fachlich verantwortlicher Reviewer, die konkret angelegten Definition-Revisions-IDs und die explizite Zustimmung pro Feld vorliegen. Für ungeklärte Punkte bleibt `semantic_status = "partially_defined"` bzw. `review_status = "unreviewed"` im Draft; keine synthetische Bestätigung.

**Nicht Teil dieser Freigabe:** `SamplingEvent`-Aufspaltung, `Occurrence` vs. `MeasurementOrFact`, Ziel-Identitäten, WoRMS-Anreicherung, Profil-SHA-Pins, Publikationsmetadaten und EML/DwC-A. Diese sind Phase-C-/D-Entscheidungen.

## Minimaler verantwortlicher Review-Check (PoC)

- [ ] **Quellgebunden:** Die 23 feldweisen Bedeutungen und Einschränkungen entsprechen dem fixierten CS-PHOC und dem Methodenartikel.
- [ ] **Null-/Missing-Statement:** `0` als im standardisierten CSV vorhandener Wert (nicht zwingend originale Feld-Null); leer != `0`.
- [ ] **Datum/Dauer:** tatsächliche Header und inklusive Kalendertage mit explizitem Vermerk zur README-Abweichung akzeptiert.
- [ ] **Counts:** Aggregationsraum, Tiere an Land, Pup-Zusammenfassung und methodische Grenzen akzeptiert.
- [ ] **Freigabeumfang:** Nur SourceFieldDefinitions; keine Entity-/Publikationsprojektion bestätigt.
- [ ] **Reviewer/Revision:** Verantwortliche Person bestätigt die konkret registrierten, unveränderten Definition-Revisions-IDs.

**Dokumentstatus bleibt ohne diese Schritte ausdrücklich „REVIEW PROPOSAL / NOT APPROVED“.**
