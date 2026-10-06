---
name: stratos-execution-roadmap
description: "StratOS Execution Roadmap (part of optional case-memo Exhibit S). Turns the ranked initiatives into time: a first-100-days plan (diagnose with a listening tour and the cheapest assumption tests, one or two quick wins, priorities and hard structural calls, launch with owners and an operating rhythm), then workstreams, dated milestones and stage gates whose go / hold / exit thresholds are written in advance. Use for 'roadmap', 'implementation plan', 'first 100 days', 'milestones', 'stage gates', 'execution plan', or 'Exhibit S'."
license: Apache-2.0
---
# ©2026 Brad Scheller

# Execution Roadmap (StratOS · Part 3 · Plan · Exhibit S)

**Runs:** after the Stakeholder Map (and Negotiation Prep when it ran). **Reads:**
`strategy_layer.initiatives[]`, `operating_model`, `stakeholders`, `stress_test`, `gtm`. **Writes:**
`strategy_layer.roadmap`. **Feeds:** Value Realization, Pitch.

## Step 1 — The first 100 days

| Phase | Days | What happens |
|---|---|---|
| **1. Diagnose** | 1-30 | Listening tour of 15-25 people across the stakeholder map (powerful sceptics included); run the **cheapest tests** of the danger-zone assumptions from the Stress Test. No big announcement yet |
| **2. Quick wins** | 1-60, in parallel | One or two visible wins the organisation values, each tied to an initiative |
| **3. Direction** | 31-60 | State 3-5 priorities (the "now" initiatives); make the hard structural calls from the Operating Model, not before the diagnosis and not long after |
| **4. Launch** | 61-100 | First initiatives start, each with an owner and an early milestone; set the operating rhythm (weekly initiative review, monthly KPI review, quarterly gate review) |

## Step 2 — Workstreams and milestones

Group the "now" and "waits" initiatives into 3-6 workstreams. For each initiative: owner (a role from
the Operating Model), start, dated milestones, and dependencies. Present as a Gantt-style table or chart.

## Step 3 — Stage gates

For each staged bet (Strategic Options Step 3) and each major commitment, a gate with thresholds
written **now**:

| Gate | Date | Evidence reviewed | **Go** if | **Hold** if | **Exit** if |
|---|---|---|---|---|---|

Thresholds come from the Business Case break-even, the Expected Value flip points and the Stress Test
early-warning triggers, so the decision at the gate is not made up after the fact.

## Output

```markdown
### S. Implementation Plan
**Ranked initiatives:** (from the Initiative Prioritizer)
**First 100 days:** table · **Workstreams and milestones:** chart · **Stage gates:** table
**KPIs:** (from Value Realization)
**Impact Summary — Implementation Plan**
> _[Student writes this summary.]_
```

Write `strategy_layer.roadmap`.

## Rules

- Every milestone has an owner and a date; "ongoing" is not a milestone.
- Gate thresholds are numbers or observable events, never "if things look good".
