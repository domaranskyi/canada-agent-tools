# NYC Construction & Property Leads

Daily **construction sales leads for New York City** from official NYC Open Data (Department of Buildings, DOB NOW):

- **DOB NOW job filings** – the *earliest* signal: new buildings, alterations and demolitions as soon as they are filed, often weeks before a permit is issued and before trades are locked in. Flagged `early_stage: true` while still in review.
- **DOB NOW approved permits** – issued work permits by trade (general construction, plumbing, mechanical, structural, solar, sprinklers, scaffolds, sidewalk sheds…).

Each lead includes: source, filing/permit number, status, early-stage flag, filing/issue date, borough, address, ZIP, **BBL & BIN**, job type / work type, work description, **estimated job cost**, **owner business name**, **applicant / contractor business name and licence number**, coordinates, and a simple **lead score** (0–100: cost + recency + early stage). Results are sorted by score.

Great for GCs and subcontractors, building-material suppliers, MEP/solar/HVAC firms, expediters, insurers, lenders, architects and commercial real-estate teams.

## Pricing
Pay-per-event: **$0.005 per lead** (record returned). Use `maxItems` to cap cost – 200 leads = $1.

## Input examples
New buildings filed in Brooklyn & Queens in the last 14 days, $1M+:
```json
{"sources": ["filings"], "daysBack": 14, "boroughs": ["Brooklyn", "Queens"], "jobTypes": ["New Building"], "minEstimatedCost": 1000000}
```
Plumbing and mechanical permits issued this week in Manhattan:
```json
{"sources": ["permits"], "boroughs": ["Manhattan"], "workTypes": ["Plumbing", "Mechanical Systems"]}
```
Everything from the last 7 days (default): `{}`

## Output example
```json
{"source": "DOB NOW job filing", "id": "B00123456-I1", "status": "Plan Examiner Review", "early_stage": true,
 "date": "2026-10-06", "borough": "Brooklyn", "address": "123 EXAMPLE STREET, Brooklyn, NY, 11211",
 "bbl": "3023450012", "bin": "3061234", "job_type": "New Building", "estimated_cost": 2400000,
 "owner_business_name": "EXAMPLE DEVELOPMENT LLC", "applicant_business_name": "EXAMPLE ARCHITECTS PC",
 "applicant_license": "012345", "lead_score": 90}
```

## Privacy
Only business information is returned. Names, phone numbers and email addresses of individual people (owners, applicants, filing representatives, permittees) are **not** output; phone numbers and emails inside work descriptions are redacted. Business names and professional licence numbers are kept. Comply with CAN-SPAM, TCPA and applicable laws when using leads for outreach.

## Data source & attribution
Data from [NYC Open Data](https://opendata.cityofnewyork.us/), published by the NYC Department of Buildings: [DOB NOW: Build – Job Application Filings](https://data.cityofnewyork.us/d/w9ak-ipjd) and [DOB NOW: Build – Approved Permits](https://data.cityofnewyork.us/d/rbx6-tga4). Used under the [NYC Open Data Terms of Use](https://opendata.cityofnewyork.us/overview/#termsofuse). Records are normalized and filtered by this actor; personal contact fields are removed. Data is updated daily by the City and may lag.

## Disclaimer
Not affiliated with or endorsed by the City of New York or NYC DOB. Data is provided "as is" and may be incomplete, delayed or inaccurate; verify with DOB before relying on it. Not legal, financial or real-estate advice.
