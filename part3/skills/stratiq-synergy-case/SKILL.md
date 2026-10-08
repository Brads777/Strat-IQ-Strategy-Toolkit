---
name: stratiq-synergy-case
description: "Strat-IQ Synergy Case. Runs when an option is an acquisition, merger, joint venture or alliance: builds cost and revenue synergies line by line, haircuts revenue synergies (30-40% or more) and phases them in, nets out one-off integration costs, values the result with synergy_case.py, and asks the test that matters: do the synergies cover the premium paid? Use for 'synergies', 'acquisition', 'merger', 'JV', 'alliance', 'is the deal worth the premium', or 'should we buy X'."
license: CC-BY-NC-4.0 AND PolyForm-Noncommercial-1.0.0
---
# ©2026 Brad Scheller

# Synergy Case (Strat-IQ · Part 3 · Choose)

**Runs:** only when an option is a deal (acquisition, merger, JV, alliance). **Reads:**
`strategy_layer.options`, `competitors[].financials`, `company_layer.internal.value_chain`, `vrio`.
**Writes:** `strategy_layer.synergy_case`. **Feeds:** Business Case, Negotiation Prep, Stress Test.

Most deals destroy value for the buyer because the premium is paid up front and the synergies arrive
late, smaller, or not at all. Revenue synergies are the most overstated number in deal-making.

## Step 1 — List the synergies, line by line

| Type | Examples | Evidence needed |
|---|---|---|
| **Cost** | Procurement scale, overlapping SG&A, plant consolidation, shared R&D platform | The two cost bases from the filings or value chains; the overlap named |
| **Revenue** | Cross-selling, new channels, new geographies, bundled products | A customer or channel overlap that shows the mechanism |
| **Capability** | A capability VRIO rated a `gap` that the target supplies | The VRIO item |

Each line: annual run-rate value, the year it starts, years to full run-rate, and its source.

## Step 2 — Haircut and phase

- **Revenue synergies** are haircut by at least **30-40%** by default (state the haircut used).
- **Cost synergies** are haircut by 10-20% unless the overlap is contractual.
- Phase every line in over its ramp years; nothing is at full run-rate in year 1.

## Step 3 — Net the integration cost and value it

One-off integration costs (systems, severance, rebranding, retention bonuses) are typically 1-1.5×
annual run-rate cost synergies *[rule of thumb]*; use real estimates when there are any. Fill
`templates/synergy-case.csv` and run `scripts/synergy_case.py`. It returns the PV of synergies after
haircuts and integration costs, and compares it with the **premium** (price paid above the target's
standalone value).

## Step 4 — The verdict

One sentence: *"Synergies are worth $X after haircuts and integration; the premium is $Y; the deal
creates (or destroys) $Z for the buyer's shareholders."* If PV < premium, say what would have to be
true (a lower price, a smaller stake, an alliance instead) and hand that to Negotiation Prep.

## Rules

- No synergy without a named mechanism and source.
- Never present un-haircut revenue synergies as the case.
- An alliance or JV gets the same discipline: the "premium" is the value given up (equity, IP, margin).
