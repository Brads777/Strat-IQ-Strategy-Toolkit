# StratOS v3.0.0 — Parts 2 + 3 together, and GLO-BUS cameras and drones

**One upload:** `stratos-part2-3-skills.zip` (29 skill zips) installs Part 2 and Part 3 on top of Part 1.
With the Part 1 orchestrator switched off, 39 StratOS skills are on.

## Part 2 — the company
- New: **Unit Economics** (J-1, `unit_economics.py`), **Full Potential** (K-1, `full_potential.py`),
  **Growth Barriers** (K-2).
- Orchestrator-final: description now under Claude.ai's 1,024-character limit; modes A-E; checks R13-R19.

## Part 3 — making the strategy work (17 new skills, 10 scripts)
Choose: **Strategy Interview** (new: a one-question-at-a-time interview in which the student chooses
their own strategy and positioning from the maps, trending influence factors, KSFs and VRIO; it never
picks), Strategic Options (P), Business Case (Q-1), Pricing, Synergy Case, Expected Value (Q-2).
Test: Stress Test (R). Plan: Go-to-Market (T), Initiative Prioritizer (S), Operating Model,
Stakeholder Map, Negotiation Prep, Execution Roadmap (S). Track: Value Realization with a
Balanced Scorecard and Strategy Map (U, `strategy_map.py`), Memo Coach, Pitch, and the **StratOS Workbook**:
a branded Excel file of live worksheets for every framework, pre-filled from the ledger (`build_workbook.py`).

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

## Updated Part 1 skills (replace on upload)
`stratos-case-exhibits` (optional J-1, K-1, K-2, P-T), `stratos-strategic-mapping`, `stratos-globus-coach`.

## Assets
- `stratos-part2-3-skills.zip` — Parts 2 + 3 (29 skills)
- `stratos-all-skills.zip` — Part 1 (14 skills, with the updated GLO-BUS Coach)
- `industries.json` — version 2
- `StratOS_Workbook_template.xlsx` — the workbook with example rows; `StratOS_Workbook_blank.xlsx` — empty

Guide: https://brads777.github.io/stratos-external-analysis/part2-3-guide.html
