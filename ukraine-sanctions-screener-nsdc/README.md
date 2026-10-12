# Ukraine Sanctions Screener (NSDC)

Screen **people, companies and vessels** against **Ukraine's State Sanctions Register** (Державний реєстр санкцій), maintained by the National Security and Defense Council of Ukraine (RNBO / NSDC).

- **Fuzzy name matching across scripts.** Ukrainian, Russian and Latin spellings all match. Names and aliases are transliterated, legal-form words (LLC, ТОВ, ООО, JSC…) are ignored, and word order does not matter. "Viktor Medvedchuk" matches "Медведчук Віктор Володимирович".
- **Exact ID matching.** Tax numbers (INN / РНОКПП), registration numbers (EDRPOU, OGRN), passport numbers, and vessel IMO and MMSI numbers.
- **All three registers:** individuals, legal entities and vessels, with the **status** of each subject (active, lifted or expired), decrees, dates, sanctions term and end date.
- **Fast, with no scraping.** The index is bundled into the actor, so runs never download from the NSDC site.

Built for KYC/AML, compliance, procurement and due-diligence teams, and for Super Intelligence agents (available as an MCP tool).

## Data snapshot: please read
The register website is protected against automated downloads, so this actor ships an **offline snapshot** built from the official NSDC "actions" CSV exports dated **09.10.2026**. The snapshot covers 22,625 individual, 13,700 legal-entity and 888 vessel action rows, which collapse to 13,943 individuals, 9,682 legal entities and 888 vessels (24,513 subjects).
Sanctions imposed, changed or lifted after the snapshot date are **not** included. Every result carries `snapshot_date`. The maintainer refreshes the index by re-downloading the CSVs from drs.nsdc.gov.ua and redeploying. Always confirm a hit on https://drs.nsdc.gov.ua before acting on it.

## Pricing
Pay-per-event: **$0.004 per screened name or ID**. Screening 1,000 names costs $4.

## Input
```json
{"names": ["Viktor Medvedchuk", "Rosneft", "Acme Maple Trading Ltd"], "ids": ["9410210"], "fuzzyThreshold": 0.85}
```
- `names`: names to screen. `ids`: optional IDs for exact lookup.
- `fuzzyThreshold`: minimum similarity from 0 to 1, default 0.85.
- `entityTypes`: any of `individual`, `legal`, `vessel`.
- `activeOnly`: hide lifted or expired subjects.
- `maxMatchesPerName`: cap on matches returned per name.

## Output (one item per screened name/ID)
```json
{"query": "Viktor Medvedchuk", "query_type": "name", "matched": true, "active_match": true, "match_count": 1, "top_score": 1.0,
 "matches": [{"name": "Медведчук Віктор Володимирович", "translit_name": "Medvedchuk Viktor Volodymyrovych", "type": "individual",
   "score": 1.0, "status": "active", "ids": [{"type": "Податковий номер", "value": "…", "country": "Україна"}],
   "decree": "…", "date": "…", "first_decree": "…", "sanctions_term": "…", "sanctions_end_date": "…",
   "register_id": "…", "sourceUrl": "https://drs.nsdc.gov.ua"}],
 "snapshot_date": "09.10.2026", "sourceUrl": "https://drs.nsdc.gov.ua", "attribution": "Source: State Sanctions Register …"}
```
`decree` and `date` give the decree currently in force for the subject. `first_decree` is the original listing. `last_action` records whether the latest decree applied, amended or lifted the sanctions.

## Data source & attribution
Source: **State Sanctions Register of Ukraine, National Security and Defense Council of Ukraine (RNBO / NSDC)**, https://drs.nsdc.gov.ua. The data is a snapshot dated 09.10.2026, reprocessed (normalized, deduplicated, indexed) by this actor. See LICENSES.md.

## Disclaimer
This actor is not affiliated with or endorsed by the NSDC or the Government of Ukraine. Fuzzy matches are *potential* matches and need human review. A non-match does not prove a party is unsanctioned, since the data may be out of date. This is not legal advice. Screen against other lists (OFAC, EU, UK, Canada SEMA) as your obligations require.
