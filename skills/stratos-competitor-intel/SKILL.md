---
name: stratos-competitor-intel
description: "StratOS competitor intelligence pass. For every firm in the competitor set, gathers financials (growth, margins, R&D and SG&A intensity, segment mix), mines 10-K / annual-report risk factors and MD&A for macro and industry trends, reads news, hiring, patent and regulatory signals, and rates each firm's moat. Runs first in the StratOS pipeline so PESTEL and driving forces start from audited, primary evidence. Use for competitor analysis, competitive landscape, peer benchmarking, comps, 'who competes with X', or competitor financials and news."
license: Apache-2.0
---
# ©2026 Brad Scheller

# Competitive Analysis (StratOS CI)

**Runs:** after intake, before PESTEL. **Reads:** the ledger scope (industry, boundary, competitor
set, base company). **Writes:** `competitors[]`, `evidence[]`, and `ci.pestel_seeds[]` for the
PESTEL stage.

A landscape slide that says "Competitor A is a large player with broad capabilities" is a label.
"Competitor A has posted 30 autonomy-engineering roles in 18 months and filed a cluster of
obstacle-avoidance patents" is intelligence. This skill produces the second kind.

## Step 0 — Pick the industry's defining metrics

Before pulling any numbers, choose the 4-6 metrics this industry actually runs on, and use the same
ones for every competitor. Examples:

| Industry | Metrics to benchmark |
|---|---|
| Drones / hardware | Revenue growth, gross margin, enterprise vs consumer mix, recurring software or service revenue %, R&D % of revenue, units or installed fleet if disclosed |
| SaaS | ARR, net revenue retention, gross margin, CAC payback, Rule of 40 |
| Consumer packaged goods | Organic growth, price/mix vs volume, gross margin, A&P % of sales |
| Automotive | Deliveries, ASP, automotive gross margin, capex and R&D % of revenue |
| Banking / fintech | Customers, revenue per customer, cost-to-serve, credit losses, capital ratio |

For an industry not listed, pick what its investors and operators benchmark on, and say why.

## Step 1 — Financials for each competitor

Collect the last 3 fiscal years plus LTM, using the metric set in `references/financial-metrics.md`.
For a conglomerate, use **segment-reported** figures only, never the parent's consolidated totals.

**Default source: the OpenBB MCP server** (setup, tools to activate, and provider order in
`references/openbb-mcp.md`). Use one provider per metric across the whole peer set, record the
provider on every figure (e.g. `provider=fmp`), and spot-check at least one figure per competitor
against its SEC filing. If OpenBB is not reachable, say so once and fall back in the order below.

| Ownership | Where to look (in priority order) |
|---|---|
| Public (US) | OpenBB → a finance connector → 10-K and 10-Q via SEC EDGAR → earnings-call transcripts and investor decks → analyst estimates |
| Public (non-US) | Annual report / 20-F → exchange filings → investor presentations |
| Private | Company press releases and funding announcements → reputable press → industry reports. Mark every figure `[E]` (estimate) with its source. |
| State-owned | Annual report if published → state or regulator filings → press |

Record for each: revenue, growth, gross and operating margin, R&D and SG&A as % of revenue, segment
mix, and any metric from Step 0. **Comparability rules:** the same fiscal year for everyone (flag
exceptions such as "FY24 vs H1 2025"); the same metric definitions; one currency with the rate and
date noted; missing values shown as "n/a", never blank; every number cited as
`[Company] [Document] ([Date])`.

**Normalise** before comparing (checklist in `references/financial-metrics.md`): calendarise fiscal
years more than 3 months apart; average FX for P&L items and spot FX for balance-sheet items; adjust
EBITDA for IFRS 16 vs ASC 842 leases; strip impairments, restructuring and M&A gains. Footnote every
adjustment.

**Benchmark** the peer set: for each metric show the industry median and each firm's quartile, and
flag outliers more than 1.5× the IQR from the median, with the reason (note when n < 5). Put the
table first and judgements after it — facts before interpretation.

If a firm publishes no audited financials, say so as a visible caveat. That absence is itself
information — it limits how confidently anything downstream can be scored. Give every competitor an
overall data confidence: High, Medium or Low.

## Step 2 — Mine the filings for PESTEL and driving-force seeds

This is why CI runs first. Management must disclose what threatens the business, under legal
liability, in the risk-factors section (10-K Item 1A, or the equivalent annual-report section), and
must explain what moved revenue and cost in MD&A (Item 7).

For each competitor with filings, extract:

- **Risk factors** — tag each with its PESTEL dimension (P/E/S/T/E/L) and P&L line. A risk that three
  or more competitors all disclose is industry-level: flag it `shared: true`.
- **MD&A trend statements** — what management says moved price, volume, mix, input costs or opex, and
  why. These are candidate driving forces with a transmission mechanism already stated.

Write these to `ci.pestel_seeds[]` with evidence ids. The PESTEL skill starts from them, and the
driving-forces skill cites them.

## Step 3 — Signals: what they are doing, not what they say

Read signals for **strategic intent**, not collected facts:

- **Hiring** — job-posting volume and themes reveal priorities 12-18 months out. A cluster of
  autonomy or AI roles means they are building; a shift from engineers to solutions architects means
  the platform is maturing into custom work.
- **Patents** — filing themes and volume over time (Google Patents, national patent offices). A firm
  claiming technology leadership with no recent filings is a signal too.
- **Regulatory filings and actions** — certifications, approvals, bans, trade-list designations,
  government procurement eligibility.
- **Pricing and packaging** — list prices, bundles, subscription moves, discount behaviour.
- **Customer voice** — review sites, forums, app stores. Negative reviews are the honest ones.
- **News** — launches, partnerships, M&A, layoffs, executive moves. Recent events only, verified
  against a primary source where possible.

For each competitor, write the **apparent strategy** — what their actions reveal, which may differ
from their press releases ("they say enterprise; they are hiring consumer-channel sales").

## Step 4 — Moat rating

Rate each competitor Strong / Moderate / Weak on each moat type, with one line of evidence:

| Moat | Assess |
|---|---|
| Network effects | Does each added user or device make the product better for others? |
| Switching costs | Integration depth, contracts, retraining, data lock-in |
| Scale economies | Unit-cost advantage at volume; minimum efficient scale |
| Intangibles | Brand, proprietary data, licences, certifications, patents |

Then name each firm's **durable advantage** (hard to copy) and **structural vulnerability** (hard to
fix).

## Step 5 — Likely responses

For the base company's plausible moves (a price cut, a new capability, a new segment), how would each
major competitor respond, and how fast? This is where intelligence becomes strategy.

## Data sources worth connecting

All free or open source; use whichever the surface provides.

| Source | Gives you | Notes |
|---|---|---|
| SEC EDGAR (web) | 10-K, 10-Q, 20-F, 8-K; full-text search | Free, no key needed, works through web fetch in Claude.ai |
| `edgartools` (Python, MIT) | Parsed filings, financial statements, segment data, risk-factor sections | For Claude Code or code-execution runs |
| OpenBB | Financials, ratios, peers, macro series across many data vendors | Non-standard licence — fine for teaching, check before commercial use; some vendors need their own free API key |
| Anthropic `financial-services-plugins` (Apache-2.0) | `comps-analysis`, `competitive-analysis`, `sector-overview` workflows | Use for deck-style comps once this ledger is filled |

Coverage is strongest for public companies. For private or state-owned competitors, rely on web
research and label every figure as an estimate.

## Output

```markdown
## Competitor intelligence — [industry] (base company: [X])

**Defining metrics:** […]

| Firm | Ownership | FY | Revenue | Growth | Gross margin | R&D % | Key segment | Moat (N/S/Sc/I) | Evidence |
|---|---|---|---|---|---|---|---|---|---|

### [Firm] — apparent strategy
- Signals: … (E0xx)
- Durable advantage: … · Structural vulnerability: …
- Likely response to [base company move]: …

**PESTEL seeds from filings:** [dimension] — [risk or trend] — shared by [n] firms — E0xx
**Data gaps:** [firm] — no audited financials; figures are estimates.
```

Write the ledger, then return to the orchestrator for the checkpoint.

## Pitfalls

- **Facts without intent** — a list of revenues is a table, not intelligence. Say what the signals mean.
- **Mixed periods and currencies** — comparing FY23 for one firm with FY25 for another.
- **Invented precision for private firms** — a market-share figure with no source.
- **Axes chosen to flatter the base company** — positioning belongs to the mapping skill, which
  derives axes from KSFs.
