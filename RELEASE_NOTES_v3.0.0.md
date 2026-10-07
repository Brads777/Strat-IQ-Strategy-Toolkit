# StratOS v3.0.0 — Parts 2 + 3 together, and GLO-BUS cameras and drones

**One upload:** `stratos-part2-3-skills.zip` (29 skill zips) installs Part 2 and Part 3 on top of Part 1.
With the Part 1 orchestrator switched off, 39 StratOS skills are on.

## Part 2 — the company
- New: **Unit Economics** (J-1, `unit_economics.py`), **Full Potential** (K-1, `full_potential.py`),
  **Growth Barriers** (K-2).
- Orchestrator-final: description now under Claude.ai's 1,024-character limit; modes A-E; checks R13-R19.

## Part 3 — making the strategy work (17 new skills, 12 scripts)
Choose: **Strategy Interview** (new: a one-question-at-a-time interview in which the student chooses
their own strategy and positioning from the maps, trending influence factors, KSFs and VRIO; it never
picks), Strategic Options (P), Business Case (Q-1), Pricing, Synergy Case, Expected Value (Q-2).
Test: Stress Test (R). Plan: Go-to-Market (T), Initiative Prioritizer (S), Operating Model,
Stakeholder Map, Negotiation Prep, Execution Roadmap (S). Track: Value Realization with a
Balanced Scorecard and Strategy Map (U, `strategy_map.py`), Memo Coach, Pitch, and the **StratOS Workbook**:
a branded Excel file of live worksheets for every framework, pre-filled from the ledger (`build_workbook.py`).

**Statistical decision making (Exhibit Q-3, Risk Analysis).** Business Case adds `risk_analysis.py`: a
tornado over the student's low / likely / high ranges and a 10,000-run Monte Carlo simulation (median,
P10-P90, chance NPV is below zero). Expected Value adds `bayes_update.py`: posterior probabilities after a
pilot result, the best option after each result, and EVSI, the value of an imperfect pilot net of its cost.
The workbook gains a Risk Analysis sheet (tornado chart, 1,000-run simulation, histogram) and a Bayes pilot
block on the Expected Value sheet.

## GLO-BUS
- `industries.json` v2 adds `cameras` (GoPro, Garmin, DJI Osmo, Insta360, Akaso) and `drones`
  (DJI, Parrot, Skydio, Autel, Yuneec) as real-world analogues of the GLO-BUS product lines.
- GLO-BUS Coach: three modes — learn the real industry, **CIR gap analysis** (`globus_groups.py`:
  strategic group maps, share leader, spend efficiency, white space), year coaching with guardrails.
  Student fill-in template in `references/cir-gap-prompt.md`. New mode 4: full-year review — names the strategy the team's inputs reveal and gives general lessons, not specific recommendations.
- New **GLO-BUS Capture** skill: after the team signs in, Claude in Chrome walks GLO-BUS read-only and
  captures the year's decision screens, projections, company reports and class-wide reports into one
  file (`capture_check.py` flags missing screens). Never handles passwords or changes a decision.
  Upload route for teams without the extension. Step 5 checks the entered decisions against the
  team's plan (`plan_check.py`).
- **GLO-BUS Decision Planner** sheet in the StratOS Workbook: every decision for Years 6-15 in screen
  order, the strategy anchor, projected KPIs, a change-vs-last-year flag and a price-and-advertising-cut
  guardrail. Teams enter the decisions in GLO-BUS themselves.
- **Year results tabs and Tracking:** each GLO-BUS capture becomes a Y# Results tab (KPIs vs
  investor expectations, product results, market share by region); the Tracking tab charts the trends
  across years.
- **Process flow diagram:** `docs/img/StratOS_Process_Flow.png` (and the editable `.excalidraw`): every
  skill, what it does, what it passes down, and its P&L or valuation impact.

## Updated Part 1 skills (replace on upload)
`stratos-case-exhibits` (optional J-1, K-1, K-2, P-T), `stratos-strategic-mapping`, `stratos-globus-coach`.

## Assets
- `stratos-part2-3-skills.zip` — Parts 2 + 3 (29 skills)
- `stratos-all-skills.zip` — Part 1 (14 skills, with the updated GLO-BUS Coach)
- `industries.json` — version 2
- `StratOS_Workbook_template.xlsx` — the workbook with example rows; `StratOS_Workbook_blank.xlsx` — empty
- `Case_Analysis_Memo_Guide_and_Template_v3.docx` / `.pdf` — the memo template with the optional exhibit menu (including Q-3)
- `StratOS_v3_Process_Walkthrough.pptx` — the process video deck, with nine live-demo slides
- `demo/` (in the repo) — demo kit: sample EV ledger, GLO-BUS files, a weak memo draft, the demo workbook and the run sheet

Guide: https://brads777.github.io/stratos-external-analysis/part2-3-guide.html
