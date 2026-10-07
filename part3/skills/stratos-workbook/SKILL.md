---
name: stratos-workbook
description: "StratOS Workbook. Builds a StratOS-branded Excel workbook of working worksheets, pre-filled from the student's strategy ledger (and GLO-BUS capture files) when there are any: PESTEL with impact x certainty priority, Five Forces scored up to industry attractiveness, a weighted KSF scorecard with ranks, VRIO with the verdict ladder and KSF reality check, SWOT and TOWS, a decision matrix, expected value with maximin, value of information and a Bayes pilot check, a driver-based business case with NPV and IRR, a Risk Analysis sheet with tornado and Monte Carlo, a Balanced Scorecard with status and balance checks, a Strategy Map with cause-and-effect checks and picture, a GLO-BUS CIR sheet that places each company in a strategic group, a GLO-BUS Decision Planner, one results tab per GLO-BUS year, and a Tracking tab charting the trends. Every result is a live formula. Use for 'StratOS workbook', 'Excel worksheets', 'spreadsheet version of my analysis', 'template', or 'worksheet'."
license: Apache-2.0
---
# ©2026 Brad Scheller

# StratOS Workbook

One Excel file that holds a whole StratOS analysis in working worksheets. Students can see the
arithmetic, change an input, and watch the scores, verdicts, ranks and statuses update. It complements
the report and the exhibits; it never replaces the reasoning in them.

## Three ways to build it

| Ask | Command | Result |
|---|---|---|
| "Build our GLO-BUS planner" | `python scripts/build_workbook.py --ledger <ledger> --capture globus-capture-C-Y6.json [--capture …] --out StratOS_Workbook_<team>.xlsx` | Adds each captured year's entered decisions to the Decision Planner and the latest CIR to the GLO-BUS CIR sheet |
| "Build my StratOS workbook" (a ledger exists) | `python scripts/build_workbook.py --ledger strategy-ledger-<scope>.json --out StratOS_Workbook_<company>.xlsx` | Pre-filled from the ledger: PESTEL, forces, KSFs and competitor scores, VRIO, SWOT and TOWS, options, scorecard, strategy map with picture. Sections the ledger lacks stay blank |
| "Give me the worksheets" (no ledger) | `python scripts/build_workbook.py --out StratOS_Workbook.xlsx` | Template with one realistic example row per sheet so the format is clear |
| "A blank template" | `python scripts/build_workbook.py --blank --out StratOS_Workbook_blank.xlsx` | Empty template |

The strategy map picture needs matplotlib; without it the table and its checks still work.

## The sheets

| Sheet | What the formulas do |
|---|---|
| Start | How to use it, the colour key, what each sheet does |
| PESTEL | Priority = impact × certainty, coloured strategic focus / scenario-plan / monitor; counts findings missing a source |
| Five Forces | Sub-factor scores (the course template's sub-factors) average to each force; a force score entered directly overrides; strength label; industry attractiveness = 6 − average force score, now and at the horizon |
| KSF Scorecard | Weights must sum to 100% (flagged); SUMPRODUCT weighted score per competitor; rank |
| VRIO | Verdict ladder stops at the first No or ?; reality check flags competence traps (passes V, R and I but the KSF it delivers weighs under 10%) and marks supported advantages |
| SWOT-TOWS | Four traced lists with sources; TOWS options with the items they pair |
| Decision Matrix | Weighted score (out of 5) and rank per option; do nothing included |
| Expected Value | Probability check per option, expected NPV, worst and best case, leader, maximin choice, value of perfect information; a Bayes' rule pilot block (likelihoods → posteriors, best option after each result, EVSI, net value after the pilot's cost). Matches `bayes_update.py` |
| Business Case | Filled from `strategy_layer.business_case[0].inputs` when present. Revenue, contribution, EBIT, tax, working capital (released in the final year), cash flow, cumulative cash, NPV, IRR, hurdle check. Matches `stratos-business-case` |
| Risk Analysis | Exhibit Q-3. Low / likely / high per driver (filled from `strategy_layer.risk_analysis.ranges` when present); exact tornado NPVs and a sorted tornado chart; a 1,000-run Monte Carlo (RAND, triangular) with mean, median, P10, P90, standard deviation, P(NPV < 0) and a histogram. The tornado matches `risk_analysis.py` exactly; the simulation moves slightly with each recalculation (F9) |
| Balanced Scorecard | % of target and status (on target / caution / below plan, inverted when lower is better); balance check: every perspective covered, at least a third of measures leading, measures with no owner |
| Strategy Map | Flags objectives that drive nothing or that nothing drives; picture of the map when built from a ledger |
| GLO-BUS CIR | Share-weighted industry average price and P/Q per product; each company placed as premium differentiator, value leader, low-cost or stuck in the middle |
| Y# Results | One tab per GLO-BUS year from its capture file (`references/globus-results.json`): the five scored KPIs against investor expectations with gap and met / not met (credit rating in notches), company results, product results with price and cost per unit against the industry, market share by region, the decisions entered and the CIR |
| Tracking | Every year side by side by formula, with eight line charts: EPS, ROE and stock price against expectations, image rating and credit score, market share, cost per unit against the industry, revenue and profit, operating margins. Rebuild after each round to add the new year |
| GLO-BUS Planner | Every decision field for Years 6-15 in screen order (fields in `references/globus-fields.json`), the strategy anchor from the Strategy Interview, the projected KPIs; change-vs-last-year block flagged above a threshold you set (default 15%), and a guardrail flag when price and advertising are cut in the same year. The team enters the decisions in GLO-BUS itself; `stratos-globus-capture` Step 5 then checks the entries against this plan |

## Before handing it over

1. Recalculate (open in Excel, or LibreOffice headless) and confirm there are **no formula errors**.
2. Spot-check two numbers against the ledger or the skill outputs (e.g. the Business Case NPV against
   `business_case.py`, a VRIO verdict against `vrio_screen.py`).
3. Give the student the file and say which sheets were pre-filled and which are blank.

## Rules

- Formulas only: never paste a computed result over a formula.
- In graded work, the inputs, choices and every Impact Summary are the student's. The workbook ranks
  and scores; it never decides, and Claude never fills it with invented case facts.
- GLO-BUS sheets hold the team's own figures; they are not a source of numbers to enter in the game.
- Never enter, upload or submit planner values into GLO-BUS; the team does that, screen by screen.
