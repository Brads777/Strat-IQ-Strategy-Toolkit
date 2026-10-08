# Financial metric set

Read this during steps 2 and 6 of the competitive-analysis workflow.

## Core metrics (always collect)

| Group | Metric | Formula / note |
|---|---|---|
| Scale | Revenue | Segment revenue for conglomerates |
| Growth | Revenue CAGR (3y), YoY growth | Separate organic from M&A-driven when disclosed |
| Profitability | Gross margin, EBITDA margin, operating margin, net margin | Adjusted: exclude one-time items |
| Returns | ROIC | NOPAT / (debt + equity − cash) |
| Returns | ROE, ROA | Compare within capital-structure peers only |
| Efficiency | Asset turnover, inventory days, DSO, DPO, cash conversion cycle | CCC = DIO + DSO − DPO |
| Investment | Capex / revenue, R&D / revenue, SG&A / revenue | Cost structure signals strategy |
| Cash | FCF margin, FCF conversion | FCF / net income |
| Balance sheet | Net debt / EBITDA, interest coverage, current ratio | Resilience |
| Market (public) | EV/Revenue, EV/EBITDA, P/E, market share | Valuation shows what the market expects |
| People | Revenue per employee, headcount growth | Useful proxy for private peers |

## Industry-specific KPIs (add when relevant)

| Industry | KPIs |
|---|---|
| SaaS / software | ARR, net revenue retention, gross retention, CAC payback, Rule of 40, magic number |
| Healthcare services / dental | Revenue per location/provider, patient volume, payer mix, same-store growth, chair utilization |
| Retail / consumer | Same-store sales, sales per sq ft, inventory turns, e-commerce mix |
| Manufacturing / industrials | Capacity utilization, backlog, book-to-bill, warranty cost % |
| Banking / fintech | NIM, efficiency ratio, NPL ratio, CET1, take rate |
| Telecom / media | ARPU, churn, subscribers, content spend % |
| Energy / commodities | Production volume, lifting cost, reserve life, realized price |
| Airlines / logistics | RASM/CASM, load factor, yield, on-time rate |

## Normalization checklist

- Calendarize to a common year-end when fiscal years are more than 3 months apart.
- Use the same FX rate for all competitors, and say which rate you used (average rate for P&L items, spot rate for balance-sheet items).
- IFRS 16 vs. ASC 842: EBITDA is not comparable until you adjust for leases.
- Exclude impairments, restructuring, and M&A gains, and footnote each exclusion.
- Quartiles: compute across the peer set only, and note if n < 5.
