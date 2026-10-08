# Strat-IQ Part 3 — Making the Strategy Work

**The third part of Strat-IQ.** Part 1 reads the industry. Part 2 reads the company. Part 3 turns the
analysis into a strategy that works: it generates real options, puts money and probabilities on them,
attacks the leading option before anyone commits, and then plans, staffs, negotiates, measures and
pitches it.

Part 3 ships **together with Part 2** in release v3.0.0 (`stratiq-part2-3-skills.zip`). Install
instructions: [`../part2/README.md`](../part2/README.md#install) and
**[the Parts 2 + 3 guide](https://brads777.github.io/stratos-external-analysis/part2-3-guide.html)**.

## The seventeen skills

| Move | Display name | Skill ID | Exhibit | Script |
|---|---|---|---|---|
| Choose | Strategy Interview | [`stratiq-strategy-interview`](skills/stratiq-strategy-interview/SKILL.md) | — | — |
| Choose | Strategic Options | [`stratiq-strategic-options`](skills/stratiq-strategic-options/SKILL.md) | P | — |
| Choose | Business Case | [`stratiq-business-case`](skills/stratiq-business-case/SKILL.md) | Q-1 | `business_case.py` |
| Choose | Pricing | [`stratiq-pricing`](skills/stratiq-pricing/SKILL.md) | — | `pricing.py` |
| Choose | Synergy Case | [`stratiq-synergy-case`](skills/stratiq-synergy-case/SKILL.md) | — | `synergy_case.py` |
| Choose | Expected Value | [`stratiq-expected-value`](skills/stratiq-expected-value/SKILL.md) | Q-2 | `expected_value.py` |
| Test | Stress Test | [`stratiq-stress-test`](skills/stratiq-stress-test/SKILL.md) | R | `risk_register.py` |
| Plan | Go-to-Market | [`stratiq-gtm`](skills/stratiq-gtm/SKILL.md) | T | `gtm_funnel.py` |
| Plan | Initiative Prioritizer | [`stratiq-initiative-prioritizer`](skills/stratiq-initiative-prioritizer/SKILL.md) | S | `prioritize.py` |
| Plan | Operating Model | [`stratiq-operating-model`](skills/stratiq-operating-model/SKILL.md) | — | — |
| Plan | Stakeholder Map | [`stratiq-stakeholder-map`](skills/stratiq-stakeholder-map/SKILL.md) | — | — |
| Plan | Negotiation Prep | [`stratiq-negotiation-prep`](skills/stratiq-negotiation-prep/SKILL.md) | — | — |
| Plan | Execution Roadmap | [`stratiq-execution-roadmap`](skills/stratiq-execution-roadmap/SKILL.md) | S | — |
| Track | Value Realization | [`stratiq-value-realization`](skills/stratiq-value-realization/SKILL.md) | U | `strategy_map.py`, `variance.py` |
| Track | Memo Coach | [`stratiq-memo-coach`](skills/stratiq-memo-coach/SKILL.md) | — | — |
| Track | Executive and VC Pitch | [`stratiq-pitch`](skills/stratiq-pitch/SKILL.md) | — | — |
| Track | Strat-IQ Workbook | [`stratiq-workbook`](skills/stratiq-workbook/SKILL.md) | — | `build_workbook.py` |

The orchestrator (`stratiq-orchestrator-final`, in `part2/skills`) runs them as **mode D**:
Choose → Test → Plan → Track, with a checkpoint after every step. Pricing, Synergy Case and Negotiation
Prep run only when an option needs them.

## The discipline

- **Nothing new appears in the plan.** Every option, initiative, milestone and KPI traces back to a
  finding in Parts 1-2 (checks R15-R19).
- **The student chooses the strategy.** The Strategy Interview asks one question at a time, shows the
  evidence behind it, and tests the reasoning; it never picks.
- **Do nothing is always an option.** Every alternative has to beat standing still.
- **Attack before planning.** The Stress Test runs on the leading option before any planning starts.
- **Students own the choice.** In graded work, the alternatives, the inputs, the recommendation, the
  memo and every Impact Summary are the student's. Part 3 suggests (marked `SUGGESTED`), calculates
  confirmed inputs, and coaches.

## Scripts

All need Python 3.10+, standard library only (the GLO-BUS chart uses matplotlib if present). Each
script's docstring gives its CSV format, and each skill has a worked template in `templates/`.

## Licence

© 2026 Brad Scheller. Noncommercial licence: see [LICENSE](../LICENSE); commercial licences BScheller@ToolsIQ.ai.
