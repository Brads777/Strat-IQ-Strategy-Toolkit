---
name: stratos-negotiation-prep
description: "StratOS Negotiation Prep. Runs when an option needs a deal struck (a supplier contract, a partnership, an acquisition price, a licence): a concrete, priced BATNA for each side, a walk-away point set from the BATNA, the zone of possible agreement (ZOPA), the interests behind each side's position, tradeable issues, and an opening anchor inside the ZOPA. If there is no ZOPA: restructure the deal or walk. Use for 'negotiation', 'BATNA', 'ZOPA', 'walk-away price', 'how much should we offer', 'deal terms', or 'prepare for the negotiation'."
license: Apache-2.0
---
# ©2026 Brad Scheller

# Negotiation Prep (StratOS · Part 3 · Plan)

**Runs:** only when an option depends on a deal (the orchestrator says when it skips it). **Reads:**
`strategy_layer.synergy_case`, `business_case[]`, `stakeholders`, `industry_layer.forces[]` (supplier
and buyer power), `competitors[]`. **Writes:** `strategy_layer.negotiations[]`.

## Step 1 — BATNA, both sides, priced

**BATNA**: the best alternative to a negotiated agreement, i.e. what each side actually does if this
deal fails. It must be **concrete and priced**: "buy cells from Supplier B at $X/kWh with a 9-month
qualification delay, costing $Y in lost contribution", not "find another supplier". Estimate the
other side's BATNA from Part 1 evidence (their capacity, other customers, financial need).

## Step 2 — Walk-away and ZOPA

- **Walk-away point** = the value of your BATNA (adjusted for risk and timing). Set it **from the
  BATNA, not from hope** and write it down before talks start.
- The other side's walk-away from their BATNA.
- **ZOPA** = the range between the two walk-away points. **If there is no ZOPA**, no tactic will close
  it: restructure (add issues, change scope, change term) or walk.

## Step 3 — Interests and tradeables

Behind each position, the interests (volume certainty, cash timing, technology access, reputation).
List 4-8 tradeable issues (price, volume commitment, term, exclusivity, payment terms, IP, co-investment)
with what each is worth to each side. Trade what is cheap for you and valuable to them.

## Step 4 — Anchor and sequence

An opening **anchor inside the ZOPA**, near the other side's walk-away, with the evidence that
justifies it. The concession plan: what you give, in what order, and what you ask for in return.

## Output

| Side | BATNA (priced) | Walk-away | Interests |
|---|---|---|---|

ZOPA (or "no ZOPA: restructure / walk") · tradeables table · anchor and concession plan. Write
`strategy_layer.negotiations[]`.

## Rules

- Never recommend misrepresentation, bluffing about facts, or bad-faith tactics.
- Every price cites the business case, synergy case or market evidence.
