---
name: stratos-initiative-prioritizer
description: "StratOS Initiative Prioritizer (part of optional case-memo Exhibit S). Turns the chosen strategy into a short, ranked list of initiatives, each traced to the analysis (a Full Potential gap, the binding growth constraint, a VRIO capability gap, a staged step, a Stress Test mitigation or the GTM plan). Scores reach, impact, confidence and effort (RICE) plus cost of delay, respects dependencies, and cuts the list to the capacity available with prioritize.py. The binding constraint goes first. Use for 'prioritize initiatives', 'what do we do first', 'RICE', 'too many priorities', 'initiative list', or 'Exhibit S'."
license: Apache-2.0
---
# ©2026 Brad Scheller

# Initiative Prioritizer (StratOS · Part 3 · Plan · Exhibit S)

**Runs:** after Go-to-Market. **Reads:** `strategy_layer.*`, `company_layer.internal.full_potential`,
`growth_barriers`, `vrio`. **Writes:** `strategy_layer.initiatives[]`. **Feeds:** Operating Model,
Execution Roadmap, Value Realization.

A strategy with fifteen priorities has none.

## Step 1 — List candidate initiatives, each traced

Every initiative names its source. Nothing new appears here that the analysis did not point to.

| Source | Example |
|---|---|
| Binding growth constraint (Growth Barriers) | "Qualify a second cell supplier" |
| Full Potential gap | "Close the variable-cost gap to the peer median" |
| VRIO capability gap | "Build in-house battery-management software" |
| Staged step (Strategic Options) | "Pilot in one EU market before a plant decision" |
| Stress Test mitigation | "Dual-track supplier qualification" |
| Go-to-Market | "Launch the fleet-sales team for the beachhead" |

## Step 2 — Score

For each: **Reach** (customers, units or revenue affected per period), **Impact** (0.25 minimal · 0.5
low · 1 medium · 2 high · 3 massive), **Confidence** (0.5-1.0, from the evidence grade: belief 0.5,
analogous 0.8, proven 1.0), **Effort** (person-months or $M), and **cost of delay** (1 = can wait, 3 =
value lost every month it waits, e.g. a closing regulatory window). Fill
`templates/initiatives.csv` and run `scripts/prioritize.py --capacity <effort available>`.

The script computes RICE = Reach × Impact × Confidence ÷ Effort, weights it by cost of delay, puts
the initiative tagged `binding` first, schedules in rank order while **respecting dependencies**, and
stops at capacity. What does not fit is listed as **waits**, not dropped.

## Step 3 — Sense-check

- Is the binding constraint first? If not, explain why.
- Are 3-5 initiatives "now"? More than that and the plan is not prioritised.
- Does any high-RICE item depend on a "waits" item? Then move the dependency up or move both down.

## Output

A ranked table (rank · initiative · traces to · RICE · cost of delay · effort · depends on · now / waits)
and a one-line rationale for the top three. Write `strategy_layer.initiatives[]`.

## Rules

- Scores are judgments; show them so they can be challenged. In a case, the student confirms them.
- Never pad the list. Six well-traced initiatives beat twenty.
