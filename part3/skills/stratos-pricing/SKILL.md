---
name: stratos-pricing
description: "StratOS Pricing. Runs when price is a lever in an option: maps competitor prices against the generic strategy, bounds the price with willingness to pay (Van Westendorp's four questions), tests revenue and contribution across candidate prices with a stated elasticity using pricing.py, and asks whether rivals would match a cut. Feeds the Business Case and Go-to-Market. Use for 'pricing', 'what price should we charge', 'price war', 'Van Westendorp', 'willingness to pay', 'price elasticity', or 'should we cut price'."
license: Apache-2.0
---
# ©2026 Brad Scheller

# Pricing (StratOS · Part 3 · Choose)

**Runs:** only when an option moves price (the orchestrator says when it skips it). **Reads:**
`competitors[]` (prices, positioning), `company_layer.internal.unit_economics`, `industry_layer.forces[]`
(rivalry, buyer power), `company_layer.s5_conventional`. **Writes:** `strategy_layer.pricing`.
**Feeds:** Business Case, Go-to-Market, Pitch.

## Step 1 — Price map

Plot each competitor's price for the comparable product against its quality or performance position
(from the conventional strategic map). Mark the base company's generic strategy: low-cost,
differentiation, best-cost or focused. A price that contradicts the strategy (a differentiator priced
below the low-cost players) is the first finding.

## Step 2 — Willingness to pay (Van Westendorp)

The four questions, asked of customers or estimated from evidence (surveys, reviews, interview notes):

1. At what price is it **too cheap** to trust the quality?
2. At what price is it a **bargain**?
3. At what price is it **getting expensive** but still worth considering?
4. At what price is it **too expensive** to consider?

The acceptable range runs from where "too cheap" crosses "getting expensive" to where "bargain" crosses
"too expensive". With survey data, run `scripts/pricing.py --vw responses.csv`. Without data, give the
range as `[estimate]` from evidence and say so.

## Step 3 — Revenue vs contribution

Run `scripts/pricing.py templates/pricing.csv` with the current price, volume, variable cost and a
**stated price elasticity** (cite its source, or give a range). It returns the revenue-maximising and
the contribution-maximising price within the acceptable range. They differ, and the
contribution-maximising one is what the Business Case should use unless the strategy is share-buying,
which must then be said.

## Step 4 — Will rivals match?

For a price cut, judge each major rival's likely response from Part 1 evidence: cost position (can
they match?), capacity (do they need volume?), and stated strategy. If the likely response is to match,
rerun Step 3 with the volume gain removed. A cut that only works if nobody follows is a price war.

## Output

A price map, the acceptable range, a table of candidate prices with volume, revenue and contribution,
the recommended price basis for the Business Case (marked `SUGGESTED` in a case), and the rival
response table. Write `strategy_layer.pricing`.

## Rules

- Elasticity is always stated and sourced; never assume it silently.
- In GLO-BUS, never suggest a price number to copy; explain the trade-off and have the team test it in
  the projections (see `stratos-globus-coach`).
