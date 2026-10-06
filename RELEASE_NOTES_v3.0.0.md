# StratOS v3.0.0 — Parts 2 + 3 together, and GLO-BUS cameras and drones

**One upload:** `stratos-part2-3-skills.zip` (27 skill zips) installs Part 2 and Part 3 on top of Part 1.
With the Part 1 orchestrator switched off, 37 StratOS skills are on.

## Part 2 — the company
- New: **Unit Economics** (J-1, `unit_economics.py`), **Full Potential** (K-1, `full_potential.py`),
  **Growth Barriers** (K-2).
- Orchestrator-final: description now under Claude.ai's 1,024-character limit; modes A-E; checks R13-R19.

## Part 3 — making the strategy work (15 new skills, 8 scripts)
Choose: Strategic Options (P), Business Case (Q-1), Pricing, Synergy Case, Expected Value (Q-2).
Test: Stress Test (R). Plan: Go-to-Market (T), Initiative Prioritizer (S), Operating Model,
Stakeholder Map, Negotiation Prep, Execution Roadmap (S). Track: Value Realization, Memo Coach, Pitch.

## GLO-BUS
- `industries.json` v2 adds `cameras` (GoPro, Garmin, DJI Osmo, Insta360, Akaso) and `drones`
  (DJI, Parrot, Skydio, Autel, Yuneec) as real-world analogues of the GLO-BUS product lines.
- GLO-BUS Coach: three modes — learn the real industry, **CIR gap analysis** (`globus_groups.py`:
  strategic group maps, share leader, spend efficiency, white space), year coaching with guardrails.
  Student fill-in template in `references/cir-gap-prompt.md`. New mode 4: full-year review — names the strategy the team's inputs reveal and gives general lessons, not specific recommendations.
- New **GLO-BUS Capture** skill: after the team signs in, Claude in Chrome walks GLO-BUS read-only and
  captures the year's decision screens, projections, company reports and class-wide reports into one
  file (`capture_check.py` flags missing screens). Never handles passwords or changes a decision.
  Upload route for teams without the extension.

## Updated Part 1 skills (replace on upload)
`stratos-case-exhibits` (optional J-1, K-1, K-2, P-T), `stratos-strategic-mapping`, `stratos-globus-coach`.

## Assets
- `stratos-part2-3-skills.zip` — Parts 2 + 3 (27 skills)
- `stratos-all-skills.zip` — Part 1 (14 skills, with the updated GLO-BUS Coach)
- `industries.json` — version 2

Guide: https://brads777.github.io/stratos-external-analysis/part2-3-guide.html
