# StratOS v3.0.0 — Parts 2 + 3 together, and GLO-BUS cameras and drones

**One upload:** `stratos-part2-3-skills.zip` (30 skill zips) installs Part 2 and Part 3 on top of Part 1.
With the Part 1 orchestrator switched off, 40 StratOS skills are on.

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

## Start here: Management Interview (new)
`stratos-management-interview` is the first step for every team. After the team interviews management, it
records, one question at a time, the central problem, the decisions management needs made, the required
goals (B1-B5), management's questions, nine questions every team answers, the team's own questions and
the takeaways the team holds itself to. It feeds the memo's Key Issues and Exhibit B, the decision
criteria, the Strategy Interview and the weekly GLO-BUS report, and fills the workbook's new
**Management Interviews** sheet (right after Start). The brief stays in the team's own ledger.

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
- **The season on one tab:** **Season by Year** puts every decision (top) and result (below) for every
  year side by side, each year followed by its change (▲ ▼, green = better), with the labels frozen.
  **Competition by Year** compares every company from the class-wide reports; **KPI Charts** graphs the
  trends; **Findings & Questions** collects each week's watch items and questions with the team's response.
- **Process flow diagram:** `docs/img/StratOS_Process_Flow.png` (and the editable `.excalidraw`): every
  skill, what it does, what it passes down, and its P&L or valuation impact.

**Weekly progress report (new, GLO-BUS Coach mode 5):** `weekly_report.py` turns every capture so far
into a report with graphs (HTML, Word and JSON): scorecard, the position taken, progress, standing in the
contest and rivals' moves from the class reports only, what to watch next round, and, with `--ledger`, a
check against the management brief. Each run writes a memo (Word) and a short executive deck (PowerPoint) in the StratOS executive format.

**Workbook: one sheet per process step (new).** The StratOS Workbook now has a live worksheet for every step,
in process order and colour-coded by part (36 sheets): Management Interviews; Industry Overview,
Competitive Analysis, PESTEL, Five Forces, Trending Factors, KSFs, Strategic Mapping; Value Chain, Unit
Economics, Resources & Capabilities, VRIO, Full Potential, Growth Barriers, SWOT-TOWS; Positioning,
Strategic Options, Decision Matrix, Business Case, Expected Value, Risk Analysis, Pricing, Stress Test,
Go-to-Market, Initiatives, Operating Model, Execution Roadmap, Balanced Scorecard, Strategy Map; and the
GLO-BUS tabs. Scripts and sheets agree (unit economics, full potential, business case, risk analysis).

## Updated Part 1 skills (replace on upload)
`stratos-case-exhibits` (optional J-1, K-1, K-2, P-T), `stratos-strategic-mapping`, `stratos-globus-coach`.

## Assets
- `stratos-part2-3-skills.zip` — Parts 2 + 3 (30 skills)
- `stratos-all-skills.zip` — Part 1 (14 skills, with the updated GLO-BUS Coach)
- `industries.json` — version 2
- `StratOS_Workbook_template.xlsx` — the workbook with example rows; `StratOS_Workbook_blank.xlsx` — empty
- `Student_Case_Strategic_Analysis_Guide_and_template_v3.docx` / `.pdf` — your memo guide and template, edited in place, with the optional exhibit menu (including Q-3)
- `StratOS_v3_Process_Walkthrough.pptx` — the process video deck, with nine live-demo slides
- `demo/` (in the repo) — demo kit: sample EV ledger, GLO-BUS files, a weak memo draft, the demo workbook and the run sheet

Guide: https://brads777.github.io/stratos-external-analysis/part2-3-guide.html
