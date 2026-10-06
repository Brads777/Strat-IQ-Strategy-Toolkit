---
name: stratos-unit-economics
description: "StratOS Unit Economics (supplementary case-memo Exhibit J-1). Breaks the base company's economics down to one unit (a car, a camera, a subscriber, an order): price, variable cost, contribution margin, fixed-cost absorption and break-even volume, and, where customers are acquired, CAC, lifetime value and payback. Compares each line with the competitor set and runs a sensitivity on the three drivers that move contribution most. Every input is cited or marked [ask in interview]. Use for 'unit economics', 'contribution margin', 'cost per unit', 'break-even volume', 'CAC', 'LTV', 'payback', or 'Exhibit J-1'."
license: Apache-2.0
---
# ©2026 Brad Scheller

# Unit Economics (StratOS · Part 2 · Exhibit J-1)

**Runs:** after Value Chain, before Resources and Capabilities. **Reads:** `company_layer.internal.value_chain`,
`competitors[].financials`, `industry_layer.ksf[]`. **Writes:** `company_layer.internal.unit_economics`.
**Feeds:** Full Potential, Growth Barriers, Pricing, Business Case, Go-to-Market (CAC check) and Pitch.

The value chain says where the money goes across the firm. Unit economics says whether **one more
unit** makes money, and how many units it takes to cover the fixed base. A strategy that grows volume
on negative contribution grows losses.

## Step 1 — Choose the unit

Pick the unit the business is actually sold by: one vehicle, one camera, one drone, one subscriber-year,
one order. State it in one line. If the firm sells several units with very different economics (e.g.
cameras and drones), run one table per unit and do not average them.

## Step 2 — Build the unit table

| Line | Definition | Source rule |
|---|---|---|
| Average selling price (ASP) | Net of discounts, rebates and retailer margin | Filing (revenue ÷ units), or interview notes |
| Variable cost per unit | Materials, assembly labour, freight, warranty, payment fees | Filing (COGS ÷ units, minus fixed items), teardown estimates marked `[estimate]` |
| **Contribution per unit** | ASP − variable cost | Calculated |
| Contribution margin % | Contribution ÷ ASP | Calculated |
| Fixed costs per period | R&D, SG&A, depreciation, plant overhead | Filing |
| **Break-even volume** | Fixed costs ÷ contribution per unit | Calculated |
| Margin of safety | (Actual volume − break-even) ÷ actual volume | Calculated |

When the firm acquires customers directly (subscriptions, direct-to-consumer, fleets), add:

| Line | Definition |
|---|---|
| CAC | Sales and marketing spend ÷ new customers |
| Contribution per customer per year | Contribution × units per customer per year (+ services/software margin) |
| Retention / repurchase rate | Share of customers who buy again or stay |
| **LTV** | Annual contribution per customer × expected lifetime (discounted at the stated rate) |
| **LTV : CAC** | Healthy is usually ≥ 3 : 1 *[rule of thumb]* |
| **CAC payback (months)** | CAC ÷ monthly contribution per customer |

Run `scripts/unit_economics.py` on `templates/unit-economics.csv` for the arithmetic, the
break-even and the sensitivity. Do not do the arithmetic in prose.

## Step 3 — Benchmark against the peers

For each line, place the base company against the competitor set from Competitive Analysis (gross
margin, R&D and SG&A per unit where units are disclosed). Mark each line `ahead`, `parity` or
`behind`, and name the KSF it relates to. A line that is `behind` on a heavily weighted KSF is a
candidate for Full Potential.

## Step 4 — Sensitivity

The script flexes price, variable cost and volume by ±10% and reports which one moves contribution and
break-even most. Report the top driver in one plain sentence: *"A 10% fall in price wipes out 60% of
contribution; price discipline matters more than volume."*

## Output

```markdown
### J-1. Unit Economics — [company], unit = [unit]
| Line | Base company | Peer median | Position | Source |
|---|---|---|---|---|
**Break-even:** [n] units per [period] · margin of safety [x]%
**Most sensitive driver:** [sentence]
**Impact Summary — Unit Economics**
> _[Student writes this summary.]_
```

Write `company_layer.internal.unit_economics = {unit, lines[], break_even, margin_of_safety, ltv_cac,
payback_months, top_driver, sources[]}`.

## Rules

- Never invent a cost, a price or a retention rate. Missing inputs are `[ask in interview]` (case) or
  `n/a` with a reason (public firm). Teardown or analyst estimates are labelled `[estimate]`.
- Keep fixed and variable costs apart; a per-unit figure that silently includes fixed cost makes
  every volume decision look worse than it is.
- In GLO-BUS, the unit economics come from the team's own reports (cost per unit, price, marketing
  cost per unit in the Camera & Drone Journal), not from public filings.
