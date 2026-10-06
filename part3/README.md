# StratOS Part 3 — Making the Strategy Work

**The third part of StratOS.** Part 1 reads the industry. Part 2 reads the company. Part 3 turns the
analysis into a strategy that works: it generates real options, puts money and probabilities on them,
attacks the leading option before anyone commits, and then plans, staffs, negotiates, measures and
pitches it.

Part 3 ships **together with Part 2** in release v3.0.0 (`stratos-part2-3-skills.zip`). Install
instructions: [`../part2/README.md`](../part2/README.md#install) and
**[the Parts 2 + 3 guide](https://brads777.github.io/stratos-external-analysis/part2-3-guide.html)**.

## The fifteen skills

| Move | Display name | Skill ID | Exhibit | Script |
|---|---|---|---|---|
| Choose | Strategic Options | [`stratos-strategic-options`](skills/stratos-strategic-options/SKILL.md) | P | — |
| Choose | Business Case | [`stratos-business-case`](skills/stratos-business-case/SKILL.md) | Q-1 | `business_case.py` |
| Choose | Pricing | [`stratos-pricing`](skills/stratos-pricing/SKILL.md) | — | `pricing.py` |
| Choose | Synergy Case | [`stratos-synergy-case`](skills/stratos-synergy-case/SKILL.md) | — | `synergy_case.py` |
| Choose | Expected Value | [`stratos-expected-value`](skills/stratos-expected-value/SKILL.md) | Q-2 | `expected_value.py` |
| Test | Stress Test | [`stratos-stress-test`](skills/stratos-stress-test/SKILL.md) | R | `risk_register.py` |
| Plan | Go-to-Market | [`stratos-gtm`](skills/stratos-gtm/SKILL.md) | T | `gtm_funnel.py` |
| Plan | Initiative Prioritizer | [`stratos-initiative-prioritizer`](skills/stratos-initiative-prioritizer/SKILL.md) | S | `prioritize.py` |
| Plan | Operating Model | [`stratos-operating-model`](skills/stratos-operating-model/SKILL.md) | — | — |
| Plan | Stakeholder Map | [`stratos-stakeholder-map`](skills/stratos-stakeholder-map/SKILL.md) | — | — |
| Plan | Negotiation Prep | [`stratos-negotiation-prep`](skills/stratos-negotiation-prep/SKILL.md) | — | — |
| Plan | Execution Roadmap | [`stratos-execution-roadmap`](skills/stratos-execution-roadmap/SKILL.md) | S | — |
| Track | Value Realization | [`stratos-value-realization`](skills/stratos-value-realization/SKILL.md) | — | `variance.py` |
| Track | Memo Coach | [`stratos-memo-coach`](skills/stratos-memo-coach/SKILL.md) | — | — |
| Track | Executive and VC Pitch | [`stratos-pitch`](skills/stratos-pitch/SKILL.md) | — | — |

The orchestrator (`stratos-orchestrator-final`, in `part2/skills`) runs them as **mode D**:
Choose → Test → Plan → Track, with a checkpoint after every step. Pricing, Synergy Case and Negotiation
Prep run only when an option needs them.

## The discipline

- **Nothing new appears in the plan.** Every option, initiative, milestone and KPI traces back to a
  finding in Parts 1-2 (checks R15-R19).
- **Do nothing is always an option.** Every alternative has to beat standing still.
- **Attack before planning.** The Stress Test runs on the leading option before any planning starts.
- **Students own the choice.** In graded work, the alternatives, the inputs, the recommendation, the
  memo and every Impact Summary are the student's. Part 3 suggests (marked `SUGGESTED`), calculates
  confirmed inputs, and coaches.

## Scripts

All need Python 3.10+, standard library only (the GLO-BUS chart uses matplotlib if present). Each
script's docstring gives its CSV format, and each skill has a worked template in `templates/`.

## Licence

© 2026 Brad Scheller, [Apache License 2.0](../LICENSE).
