---
name: stratos-value-realization
description: "StratOS Value Realization. Closes the loop. Before launch it sets the KPIs as a Balanced Scorecard (financial, customer, internal process, learning and growth; leading and lagging measures), each traced to the analysis, with target, owner and trigger, and draws the Strategy Map that links the objectives cause to effect (Exhibit U). After results arrive it compares actuals with the business case driver by driver (variance.py) and attributes each variance to assumption error, execution gap or external shock, then writes the actuals back into the ledger as evidence for the next StratOS run. Use for 'KPIs', 'balanced scorecard', 'strategy map', 'scorecard', 'is the strategy working', 'plan vs actual', 'variance analysis', or 'value realization'."
license: Apache-2.0
---
# ©2026 Brad Scheller

# Value Realization (StratOS · Part 3 · Track)

**Runs:** at the end of the Plan stage (KPI design), and again whenever actual results arrive
(variance). **Reads:** `strategy_layer.business_case[]`, `initiatives[]`, `roadmap`, `stress_test`,
`company_layer.internal.unit_economics`. **Writes:** `strategy_layer.scorecard` (objectives, links, measures), `strategy_layer.kpis[]`,
`strategy_layer.actuals[]`,
and new evidence items.

## Mode 1 — The Balanced Scorecard and Strategy Map (before launch)

### 1a. Objectives in four perspectives

Turn the chosen strategy into 2-3 **objectives per perspective**, built bottom-up, each tracing to the
analysis (a KSF, the binding growth constraint, a unit-economics line, a VRIO capability gap, an
initiative or a danger-zone assumption). An objective that traces to nothing is vanity.

| Perspective | The question | Typical sources in the ledger |
|---|---|---|
| **Financial** | If we succeed, how will we look to shareholders? | Business Case, Full Potential, Unit Economics |
| **Customer** | What must customers see and value? | GTM value proposition, KSFs, Pricing |
| **Internal process** | What must we do exceptionally well? | Operating Model must-win capabilities, value chain, initiatives |
| **Learning and growth** | What capabilities, people and systems must we build? | VRIO gaps, Growth Barriers, Operating Model 7S |

### 1b. Strategy Map

Link the objectives **cause to effect**, bottom to top: learning and growth enables internal
process, which delivers what customers value, which produces the financial result. Every objective
except the financial ones must drive at least one objective in the perspective above; a financial
objective with nothing beneath it is a wish. Record the links as `from → to` pairs and draw the map
with `scripts/strategy_map.py` (input: `templates/strategy-map.csv`): four horizontal bands, one box
per objective, arrows for the links. It flags orphans (objectives that drive nothing or are driven by
nothing).

### 1c. Measures (the scorecard)

1-2 measures per objective, **8-16 in total**:

| Perspective | Objective | Measure | Leading / lagging | Target (and date) | Owner | Initiative | Trigger (re-plan if…) | Traces to |
|---|---|---|---|---|---|---|---|---|

- **Balance check:** every perspective has at least one measure, and at least a third of the
  measures are **leading** (they move before the result does: supplier quote index before cell cost,
  qualified pipeline before deliveries). A scorecard of lagging financials only tells you too late.
- **Initiative** names the Initiative Prioritizer item that moves the measure; a measure with no
  initiative and no owner is a hope.
- **Trigger** reuses the Stress Test's early-warning thresholds.
- **Status** once actuals exist: on target (≥100% of target), caution (90-99%), below plan (<90%),
  inverted for measures where lower is better. The `stratos-workbook` Balanced Scorecard sheet
  computes it.

### Output — Exhibit U (optional in a case)

```markdown
### U. Balanced Scorecard and Strategy Map
[Strategy map image]
| Perspective | Objective | Measure | Leading/lagging | Target | Owner | Initiative |
**Balance check:** [perspectives covered · share of leading measures · orphans]
**Impact Summary — Balanced Scorecard and Strategy Map**
> _[Student writes this summary.]_
```

In a graded case, objectives and targets are the student's; Claude may propose them marked
`SUGGESTED`.

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
