# Strat-IQ Parts 2 + 3 — Internal Analysis and Making the Strategy Work

**Released together as v3.0.0.** Part 1 (the skills in [`../skills`](../skills)) reads the industry.
**Part 2** (this folder) reads the **company**. **[Part 3](../part3/README.md)** turns both into a
strategy that works. This release also adds the **GLO-BUS camera and drone industries** and a CIR gap
analysis to the GLO-BUS Coach.

One upload, `stratiq-part2-3-skills.zip`, installs both parts on top of Part 1.

## What Part 2 adds

| Display name | Skill ID | Exhibit |
|---|---|---|
| **Strategic Analysis** | [`stratiq-orchestrator-final`](skills/stratiq-orchestrator-final/SKILL.md) | Replaces `stratiq-orchestrator`. Finds the saved ledger and continues from the last finished step through Parts 1, 2 and 3. Modes A-E, including **D. Make the strategy work** and **E. Help with GLO-BUS** |
| **Value Chain** | [`stratiq-value-chain`](skills/stratiq-value-chain/SKILL.md) | J — activities by cost share, value share and evolution stage ([`value_chain.py`](skills/stratiq-value-chain/scripts/value_chain.py)) |
| **Unit Economics** | [`stratiq-unit-economics`](skills/stratiq-unit-economics/SKILL.md) | J-1 — contribution per unit, break-even, CAC, LTV, sensitivity ([`unit_economics.py`](skills/stratiq-unit-economics/scripts/unit_economics.py)) |
| **Resources and Capabilities** | [`stratiq-resources-capabilities`](skills/stratiq-resources-capabilities/SKILL.md) | H — resources, capabilities, core competencies, competitive advantage |
| **VRIO Analysis** | [`stratiq-vrio`](skills/stratiq-vrio/SKILL.md) | I — the four tests on cited evidence ([`vrio_screen.py`](skills/stratiq-vrio/scripts/vrio_screen.py)) and the capability stamp on each blue-ocean candidate |
| **Full Potential** | [`stratiq-full-potential`](skills/stratiq-full-potential/SKILL.md) | K-1 — the profit bridge to benchmark, driver by driver ([`full_potential.py`](skills/stratiq-full-potential/scripts/full_potential.py)) |
| **Growth Barriers** | [`stratiq-growth-barriers`](skills/stratiq-growth-barriers/SKILL.md) | K-2 — the one binding constraint on growth |
| **SWOT Analysis** | [`stratiq-swot`](skills/stratiq-swot/SKILL.md) | K — four traced lists crossed into SO, WO, ST and WT options |

One new GLO-BUS skill, and three Part 1 skills updated and replace their Part 1 copies:

| Skill | Change |
|---|---|
| [`stratiq-case-exhibits`](skills/stratiq-case-exhibits/SKILL.md) | Exhibits C-O plus the optional J-1, K-1, K-2 and P-T |
| [`stratiq-strategic-mapping`](skills/stratiq-strategic-mapping/SKILL.md) | Blue-ocean candidates move from `UNVALIDATED` to `supported` or `gap` once VRIO has run |
| [`stratiq-globus-capture`](skills/stratiq-globus-capture/SKILL.md) | **New.** Captures a team's GLO-BUS year read-only in the team's own Chrome (Claude in Chrome), after the team signs in: decision screens, projections, company reports and the class-wide reports. Never handles passwords or changes a decision. Upload route for teams without the extension. Feeds the coach's full-year review, and checks entered decisions against the team's GLO-BUS Decision Planner (`plan_check.py`) |
| [`stratiq-globus-coach`](skills/stratiq-globus-coach/SKILL.md) | Three modes: learn the real camera and drone industries · **CIR gap analysis** with strategic group maps ([`globus_groups.py`](skills/stratiq-globus-coach/scripts/globus_groups.py)) · year coaching with guardrails · **full-year review** from a capture file (the apparent strategy and general lessons, not recommendations). Student fill-in template: [`cir-gap-prompt.md`](skills/stratiq-globus-coach/references/cir-gap-prompt.md) |

## GLO-BUS: cameras and drones

[`../project-data/industries.json`](../project-data/industries.json) (version 2) adds two industries
that mirror the GLO-BUS product lines:

| id | Mirrors | Competitors |
|---|---|---|
| `cameras` | AC cameras | GoPro, Garmin, DJI (Osmo), Insta360, Akaso |
| `drones` | UAV drones | DJI, Parrot, Skydio, Autel Robotics, Yuneec |

They are **analogues, not answer keys**: students use them to understand why a lever matters (margins,
retailer discounts, R&D intensity, low-cost vs premium positioning), never to copy numbers into the
game. After each round, students paste their Competitive Intelligence Report and get strategic group
maps, the share leader's driver, the weakest rival, reachable white space, and 3-5 moves checked
against the guardrails. **The team still makes and enters every decision.**

## Install

Step by step, with links:
**[the Parts 2 + 3 guide](https://brads777.github.io/stratos-external-analysis/part2-3-guide.html)**
(source: [`../docs/part2-3-guide.html`](../docs/part2-3-guide.html)). The short version:

### Claude.ai

1. In **Settings → Capabilities → Skills**, **delete every skill whose name starts with `stratos-`**
   (the old StratOS names, Parts 1-3).
2. Download **`stratiq-toolkit-skills.zip`** from the
   **[latest release](https://github.com/Brads777/stratos-external-analysis/releases/latest)** and unzip
   it once. Inside are 40 zips, one per skill (Parts 1-3). Leave those zipped.
3. Upload all 40 zips. You should have **40 Strat-IQ skills on**.
4. Replace `industries.json` in your Project knowledge with the new version (it adds `cameras` and
   `drones`), and make sure your saved `strategy-ledger` file is there too.
5. New chat in the Project: **"Run Strat-IQ."** The intro should show three parts and modes A-E.

If your account limits how many skills can be on at once, keep the orchestrator and the skills you are
using this week switched on; the others still run from the standard framework, with a note.

### Claude Code

```bash
cp -r stratos-external-analysis/part2/skills/stratiq-* ~/.claude/skills/
cp -r stratos-external-analysis/part3/skills/stratiq-* ~/.claude/skills/
rm -r ~/.claude/skills/stratiq-orchestrator      # the final orchestrator replaces it
```

## What is not included

The proprietary capability-fit scoring (SFI) runs behind the private Strat-IQ API. Without it, VRIO uses
a transparent public screen and stamps its output `method: "public-screen"`.

## Licence

© 2026 Brad Scheller. Noncommercial licence: see [LICENSE](../LICENSE); commercial licences BScheller@ToolsIQ.ai. Sources:
[`SOURCES.md`](skills/stratiq-orchestrator-final/references/SOURCES.md).
