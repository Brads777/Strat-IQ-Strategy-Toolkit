---
name: stratiq-stakeholder-map
description: "Strat-IQ Stakeholder Map. Lists everyone who can help or block the strategy, inside and outside (board, executives, unions, dealers, suppliers, regulators, investors, communities), scores each on power and interest, records their stance from evidence, places them on the power-interest grid (manage closely, keep satisfied, keep informed, monitor), runs the coalition math, and writes an individual plan for every powerful sceptic. Use for 'stakeholder map', 'stakeholder analysis', 'who must say yes', 'power interest grid', 'who will resist', or 'coalition'."
license: CC-BY-NC-4.0 AND PolyForm-Noncommercial-1.0.0
---
# ©2026 Brad Scheller

# Stakeholder Map (Strat-IQ · Part 3 · Plan)

**Runs:** after the Operating Model. **Reads:** `strategy_layer.*`, `industry_layer.pestel[]` (political
and legal actors), `competitors[]`, `industry_layer.forces[]` (suppliers, buyers). **Writes:**
`strategy_layer.stakeholders`. **Feeds:** Negotiation Prep, Execution Roadmap, Pitch.

## Step 1 — List them

Inside (board, CEO and executives, business units the strategy takes from, employees and unions) and
outside (dealers and retailers, key suppliers, regulators, governments, investors and lenders, major
customers, communities, partners). Group only when members truly share a position.

## Step 2 — Score and place

| Stakeholder | Power (1-5) | Interest (1-5) | Stance (champion · supporter · neutral · sceptic · blocker) | Evidence | What they want | What they fear |
|---|---|---|---|---|---|---|

Stance comes from **evidence** (public statements, filings, interview notes, past behaviour), never
assumed. Unknown stance is `unknown — find out`.

Place each on the grid:

| | Low interest | High interest |
|---|---|---|
| **High power** | Keep satisfied | **Manage closely** |
| **Low power** | Monitor | Keep informed |

Draw the grid as a chart when file creation is available.

## Step 3 — Coalition math

Sum power (score × 1) for champions and supporters against sceptics and blockers. **If the opposition's
power matches or exceeds the supporters', that is the headline**, before any plan. Name the swing
stakeholders: high power, neutral or unknown stance.

## Step 4 — Plans for the powerful sceptics

For every high-power sceptic or blocker: what they need to hear, from whom, what concession or
evidence might move them, the sequence (who before whom), and the fallback if they cannot be moved.
These plans happen **before** any announcement.

## Output

Table, grid, coalition sentence, individual plans. Write `strategy_layer.stakeholders`.

## Rules

- No stance without evidence. In a case, persona statements are the evidence: cite them.
- Never recommend manipulation or deception; plans are about evidence, interests and timing.
