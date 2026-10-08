---
name: stratiq-workbook
description: "Strat-IQ Workbook. One live Excel worksheet for every Strat-IQ step, in process order, pre-filled from the team's ledger and GLO-BUS capture files: Management Interviews; Part 1 (industry overview, competitive analysis, PESTEL, Five Forces, trending factors, KSFs, strategic mapping); Part 2 (value chain, unit economics, resources and capabilities, VRIO, full potential, growth barriers, SWOT-TOWS); Part 3 (positioning, options, decision matrix, business case, expected value, risk analysis, pricing, stress test, go-to-market, initiatives, operating model, execution roadmap, Balanced Scorecard, strategy map); and GLO-BUS (CIR, planner, Season by Year, Competition by Year, KPI Charts, Findings & Questions). Every result is a live formula. Two-way: read_workbook.py writes the cells the team changed back into the ledger, so the workbook is the team's database. Use for 'Strat-IQ workbook', 'Excel worksheets', 'spreadsheet version of my analysis', 'template', or 'read our workbook back into the ledger'."
license: CC-BY-NC-4.0 AND PolyForm-Noncommercial-1.0.0
---
# ©2026 Brad Scheller

# Strat-IQ Workbook

One Excel file that holds a whole Strat-IQ analysis in working worksheets. Students can see the
arithmetic, change an input, and watch the scores, verdicts, ranks and statuses update. It complements
the report and the exhibits; it never replaces the reasoning in them.

## Three ways to build it

| Ask | Command | Result |
|---|---|---|
| "Build our GLO-BUS workbook" | `python scripts/build_workbook.py --ledger <ledger> --capture globus-capture-C-Y6.json [--capture …] [--report weekly-report-Y7.json …] --out StratIQ_Workbook_<team>.xlsx` | Every captured year on Season by Year and Competition by Year, the charts, the latest CIR, and the weekly findings |
| "Build my Strat-IQ workbook" (a ledger exists) | `python scripts/build_workbook.py --ledger strategy-ledger-<scope>.json --out StratIQ_Workbook_<company>.xlsx` | Pre-filled from the ledger: PESTEL, forces, KSFs and competitor scores, VRIO, SWOT and TOWS, options, scorecard, strategy map with picture. Sections the ledger lacks stay blank |
| "Give me the worksheets" (no ledger) | `python scripts/build_workbook.py --out StratIQ_Workbook.xlsx` | Template with one realistic example row per sheet so the format is clear |
| "A blank template" | `python scripts/build_workbook.py --blank --out StratIQ_Workbook_blank.xlsx` | Empty template |

The strategy map picture needs matplotlib; without it the table and its checks still work.

## Two-way: read the workbook back into the ledger

The workbook is the team's database as well as its worksheets. Each blue-on-cream input cell is mapped (in
a hidden `_ledger_map` sheet) to its field in the ledger, with the value it had when the workbook was built.
When the team has edited the workbook, read it back:

| Ask | Command |
|---|---|
| "What did we change in the workbook?" | `python scripts/read_workbook.py StratIQ_Workbook_<team>.xlsx --ledger <ledger> --dry-run` |
| "Read our workbook back into the ledger" | `python scripts/read_workbook.py StratIQ_Workbook_<team>.xlsx --ledger <ledger>` (keeps `<ledger>.before-sync.json`) |
| "Turn our filled-in blank workbook into a ledger" | `python scripts/read_workbook.py StratIQ_Workbook_blank.xlsx --out strategy-ledger-<scope>.json` |

- Only changed cells are written; fields the workbook does not show (evidence ids, notes) are kept.
- A new row adds an item; a row whose inputs are all cleared removes it. Edit rows in place; do not sort
  or move rows (rows map to list positions).
- A workbook built from a different ledger (another `scope_id`) is refused unless `--force`.
- Planner edits go to `globus.plans`; responses and statuses on Findings & Questions go to
  `globus.findings_log` and come back on the next build.
- After a read-back, rebuild the workbook from the updated ledger before the next weekly report, so the
  report, the memo, the deck and the workbook all start from the same numbers.
- Show the student the change list (sheet, cell, field, was → now) before writing.

## The sheets

| Sheet | What the formulas do |
|---|---|
| Start | How to use it, the colour key, every sheet in process order |
| Management Interviews | Filled from `company_layer.management_brief` (or `globus.management_brief`): central problem, decisions D1-D5, required goals B1-B5, management's questions Q1-Q5, required questions M1-M9, the team's own T1-T8, takeaways K1-K5, completeness check |
| Industry Overview | `scope`, `industry_layer.overview`: scope; market-size estimates side by side; CAGR calculator; forecasts; segments; leaders with top-4 share and HHI; timeline; life-cycle stage |
| Competitive Analysis | `competitors[].financials / moat / signals / apparent_strategy`, `ci.pestel_seeds`: peer median, operating margin vs median and rank, moat score 0-8, signals, PESTEL seeds |
| PESTEL | Priority = impact × certainty, coloured strategic focus / scenario-plan / monitor; counts findings missing a source |
| Five Forces | Sub-factor scores average to each force; strength label; attractiveness = 6 − average force score, now and at the horizon |
| Trending Factors | `industry_layer.drivers`: the four tests; Driver or Demoted; 3-5 drivers check |
| KSF Scorecard | Weights must sum to 100%; SUMPRODUCT weighted score per competitor; rank |
| Strategic Mapping | `competitors[].positions`, `company_layer.s6_disruption / candidates`: two-vector scores (0-10) plotted on a scatter map; candidates with ERRC and the capability stamp (UNVALIDATED / supported / gap) |
| Value Chain | `company_layer.internal.value_chain`: value share − cost share, read as differentiating engine / in balance / value trap; totals check |
| Unit Economics | `internal.unit_economics`: contribution, margin, break-even, margin of safety, operating profit, LTV (same method as `unit_economics.py`), LTV/CAC, CAC payback, ±10% sensitivity |
| Resources & Capabilities | `internal.resources / capabilities / core_competencies`, with counts |
| VRIO | Verdict ladder stops at the first No or ?; reality check flags competence traps |
| Full Potential | `internal.full_potential`: drivers applied in sequence (as `full_potential.py`), gap captured per driver, current vs full-potential profit, bridge chart |
| Growth Barriers | `internal.growth_barriers`: six barriers binding / tight / slack; names the binding constraint and flags more than one |
| SWOT-TOWS | Four traced lists with sources; TOWS options with the items they pair |
| Positioning | `strategy_layer.positioning`: strategy, target, advantage, why now, not doing, statement; five fit tests (market, competitive, capability, economic, management) |
| Strategic Options | `strategy_layer.options`: SCQ; options with route, TOWS ids, staged step, gate; checks for do nothing and three or more options |
| Decision Matrix | Weighted score (out of 5) and rank per option; do nothing included |
| Business Case | Revenue, contribution, EBIT, tax, working capital, cash flow, NPV, IRR, hurdle check. Matches `business_case.py` |
| Expected Value | Expected NPV, worst and best case, leader, maximin, EVPI; Bayes pilot block with EVSI. Matches `bayes_update.py` |
| Risk Analysis | Tornado (exact, matches `risk_analysis.py`) and a 1,000-run Monte Carlo with P10, P90 and P(NPV < 0) |
| Pricing | Optional: price points × expected volume; contribution and profit; best price inside the acceptable range |
| Stress Test | `strategy_layer.stress_test`: assumption headroom to break-even and danger-zone flag; war-game; risk register with likelihood × impact, rating, owners, triggers |
| Go-to-Market | `strategy_layer.gtm`: channel funnel to customers and CAC; CAC checked against LTV from Unit Economics; blended CAC; launch phases |
| Initiatives | `strategy_layer.initiatives`: RICE score and rank; flags initiatives that trace to nothing |
| Operating Model | `strategy_layer.operating_model / stakeholders`: RAPID decision rights; power-interest quadrant and scatter |
| Execution Roadmap | `strategy_layer.roadmap`: first 100 days as week bars, milestones, stage gates |
| Balanced Scorecard | % of target and status; balance check |
| Strategy Map | Flags objectives that drive nothing or that nothing drives; picture when built from a ledger |
| GLO-BUS CIR | Industry averages per product; each company placed in a strategic group |
| GLO-BUS Planner | Every decision field for Years 6-15 in screen order; change flags and the price-and-advertising guardrail; `stratiq-globus-capture` checks entries against it |
| Season by Year | All years on one tab: decisions (top) and results (below), each year a value column then its change (▲ ▼, green = better); columns A-C frozen |
| Competition by Year | Every company from the class-wide reports only: score, rank, KPIs, price, P/Q, share by year with change; industry average; the team's rank on each measure |
| KPI Charts | Line charts from Season by Year and Competition by Year |
| Findings & Questions | Watch items, management-goal checks and questions by year from weekly-report JSON (`--report`), with the team's response and status |

## Before handing it over

1. Recalculate (open in Excel, or LibreOffice headless) and confirm there are **no formula errors**.
2. Spot-check two numbers against the ledger or the skill outputs (e.g. the Business Case NPV against
   `business_case.py`, a VRIO verdict against `vrio_screen.py`).
3. Give the student the file and say which sheets were pre-filled and which are blank.
4. After a read-back, run `read_workbook.py … --dry-run` on the rebuilt file: it should report 0 changes.

## Rules

- Formulas only: never paste a computed result over a formula.
- In graded work, the inputs, choices and every Impact Summary are the student's. The workbook ranks
  and scores; it never decides, and Claude never fills it with invented case facts.
- GLO-BUS sheets hold the team's own figures; they are not a source of numbers to enter in the game.
- Never enter, upload or submit planner values into GLO-BUS; the team does that, screen by screen.
