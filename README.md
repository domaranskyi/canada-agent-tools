# Canada Agent Tools

MCP tools for AI agents, hosted on Apify (remote MCP, streamable HTTP; Apify OAuth/token required).

## Canada Company Due Diligence Check
- MCP: `https://mcp.apify.com/?tools=canada-dd/canada-due-diligence`
- Apify Store: https://apify.com/canada-dd/canada-due-diligence
- Smithery: https://smithery.ai/search?q=canada-due-diligence
- Registry: `io.github.domaranskyi/canada-due-diligence`

## Vancouver Building Permits & New Business Leads
- MCP: `https://mcp.apify.com/?tools=canada-dd/vancouver-building-permits-leads`
- Apify Store: https://apify.com/canada-dd/vancouver-building-permits-leads
- Registry: `io.github.domaranskyi/vancouver-building-permits-leads`

## Canada Sales Tax & CAD Exchange Rates
- MCP: `https://mcp.apify.com/?tools=canada-dd/canada-sales-tax-exchange-rates`
- Apify Store: https://apify.com/canada-dd/canada-sales-tax-exchange-rates
- Registry: `io.github.domaranskyi/canada-tax-fx`
- GST/HST/PST/QST rates & calculation by province and date; Bank of Canada exchange rates (Source: Bank of Canada; data free at bankofcanada.ca). Not tax advice.

## US Economic Calendar + Canada (Official Sources)
- MCP: `https://mcp.apify.com/?tools=canada-dd/us-canada-economic-calendar`
- Apify Store: https://apify.com/canada-dd/us-canada-economic-calendar
- Registry: `io.github.domaranskyi/us-canada-economic-calendar`
- CPI, NFP, PPI, JOLTS, GDP, PCE, retail sales, housing, FOMC, jobless claims, Treasury auctions, plus Statistics Canada and Bank of Canada. Release times and actuals come from official sources only. Not investment advice.

`server.json` files for the official MCP registry are in each subfolder.

## NYC Construction & Property Leads
- MCP: `https://mcp.apify.com/?tools=canada-dd/nyc-construction-property-leads`
- Apify Store: https://apify.com/canada-dd/nyc-construction-property-leads
- Registry: `io.github.domaranskyi/nyc-construction-property-leads`
- NYC DOB NOW job filings (early stage) + approved permits as leads. Data: NYC Open Data (NYC DOB), NYC Open Data Terms of Use.

## Ukraine Sanctions Screener (NSDC)
- MCP: `https://mcp.apify.com/?tools=canada-dd/ukraine-sanctions-screener-nsdc`
- Apify Store: https://apify.com/canada-dd/ukraine-sanctions-screener-nsdc
- Registry: `io.github.domaranskyi/ukraine-sanctions-screener-nsdc`
- Fuzzy name and ID screening against Ukraine's State Sanctions Register (individuals, legal entities, vessels). Source: State Sanctions Register / RNBO NSDC (drs.nsdc.gov.ua), offline snapshot dated 09.10.2026, refreshed by re-uploading the CSV exports. The data index is not committed here; build it with `build_index.py`.
