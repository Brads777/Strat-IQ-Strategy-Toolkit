---
name: stratos-value-realization
description: "StratOS Value Realization. Closes the loop. Before launch it sets 4-8 KPIs, each traced to the analysis (a KSF, the growth constraint, a unit-economics line, a danger-zone assumption), with a leading indicator, target, owner and trigger. After results arrive it compares actuals with the business case driver by driver (variance.py) and attributes each variance to assumption error, execution gap or external shock, then writes the actuals back into the ledger as evidence for the next StratOS run. Use for 'KPIs', 'scorecard', 'is the strategy working', 'plan vs actual', 'variance analysis', or 'value realization'."
license: Apache-2.0
---
# ©2026 Brad Scheller

# Value Realization (StratOS · Part 3 · Track)

**Runs:** at the end of the Plan stage (KPI design), and again whenever actual results arrive
(variance). **Reads:** `strategy_layer.business_case[]`, `initiatives[]`, `roadmap`, `stress_test`,
`company_layer.internal.unit_economics`. **Writes:** `strategy_layer.kpis[]`, `strategy_layer.actuals[]`,
and new evidence items.

## Mode 1 — Set the KPIs (before launch)

4-8 KPIs. Each one:

| KPI | Traces to | Leading indicator | Target (and date) | Owner | Trigger (re-plan if…) |
|---|---|---|---|---|---|

- **Traces to** a KSF, the binding growth constraint, a unit-economics line or a danger-zone
  assumption. A KPI that traces to nothing is vanity.
- **Leading indicator**: what moves before the KPI does (supplier quote index before cell cost;
  qualified volume before deliveries).
- **Trigger** reuses the Stress Test's early-warning thresholds.

## Mode 2 — Plan vs actual (after results)

Fill `templates/variance.csv` with plan and actual for each business-case driver and run
`scripts/variance.py`. It computes each driver's variance and its effect on operating profit, so a
headline that hits plan cannot hide drivers that missed in opposite directions.

For every material variance, attribute **one** cause, with evidence:

| Cause | Meaning | What changes |
|---|---|---|
| **Assumption error** | The input was wrong from the start | Update the assumption and re-run the Business Case |
| **Execution gap** | The assumption held; delivery fell short | Fix the initiative (owner, resources, design) |
| **External shock** | Outside any reasonable forecast | Log it; check whether a PESTEL or driver item should be added |

## Mode 3 — Feed back

Write the actuals to the ledger as dated evidence, mark affected Part 1-3 items `stale`, and tell the
user which stages a re-run would update. The next StratOS run starts from reality, not last year's
forecast.

## Rules

- Never attribute a variance without evidence; `unclear` is an acceptable answer.
- In GLO-BUS, "actuals" are the next year's reports; log them to `globus.decisions_log[]` as well.
