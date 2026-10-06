# StratOS Parts 2 + 3 — Internal Analysis and Making the Strategy Work

**Released together as v3.0.0.** Part 1 (the skills in [`../skills`](../skills)) reads the industry.
**Part 2** (this folder) reads the **company**. **[Part 3](../part3/README.md)** turns both into a
strategy that works. This release also adds the **GLO-BUS camera and drone industries** and a CIR gap
analysis to the GLO-BUS Coach.

One upload, `stratos-part2-3-skills.zip`, installs both parts on top of Part 1.

## What Part 2 adds

| Display name | Skill ID | Exhibit |
|---|---|---|
| **Strategic Analysis** | [`stratos-orchestrator-final`](skills/stratos-orchestrator-final/SKILL.md) | Replaces `stratos-orchestrator`. Finds the saved ledger and continues from the last finished step through Parts 1, 2 and 3. Modes A-E, including **D. Make the strategy work** and **E. Help with GLO-BUS** |
| **Value Chain** | [`stratos-value-chain`](skills/stratos-value-chain/SKILL.md) | J — activities by cost share, value share and evolution stage ([`value_chain.py`](skills/stratos-value-chain/scripts/value_chain.py)) |
| **Unit Economics** | [`stratos-unit-economics`](skills/stratos-unit-economics/SKILL.md) | J-1 — contribution per unit, break-even, CAC, LTV, sensitivity ([`unit_economics.py`](skills/stratos-unit-economics/scripts/unit_economics.py)) |
| **Resources and Capabilities** | [`stratos-resources-capabilities`](skills/stratos-resources-capabilities/SKILL.md) | H — resources, capabilities, core competencies, competitive advantage |
| **VRIO Analysis** | [`stratos-vrio`](skills/stratos-vrio/SKILL.md) | I — the four tests on cited evidence ([`vrio_screen.py`](skills/stratos-vrio/scripts/vrio_screen.py)) and the capability stamp on each blue-ocean candidate |
| **Full Potential** | [`stratos-full-potential`](skills/stratos-full-potential/SKILL.md) | K-1 — the profit bridge to benchmark, driver by driver ([`full_potential.py`](skills/stratos-full-potential/scripts/full_potential.py)) |
| **Growth Barriers** | [`stratos-growth-barriers`](skills/stratos-growth-barriers/SKILL.md) | K-2 — the one binding constraint on growth |
| **SWOT Analysis** | [`stratos-swot`](skills/stratos-swot/SKILL.md) | K — four traced lists crossed into SO, WO, ST and WT options |

One new GLO-BUS skill, and three Part 1 skills updated and replace their Part 1 copies:

| Skill | Change |
|---|---|
| [`stratos-case-exhibits`](skills/stratos-case-exhibits/SKILL.md) | Exhibits C-O plus the optional J-1, K-1, K-2 and P-T |
| [`stratos-strategic-mapping`](skills/stratos-strategic-mapping/SKILL.md) | Blue-ocean candidates move from `UNVALIDATED` to `supported` or `gap` once VRIO has run |
| [`stratos-globus-capture`](skills/stratos-globus-capture/SKILL.md) | **New.** Captures a team's GLO-BUS year read-only in the team's own Chrome (Claude in Chrome), after the team signs in: decision screens, projections, company reports and the class-wide reports. Never handles passwords or changes a decision. Upload route for teams without the extension. Feeds the coach's full-year review |
| [`stratos-globus-coach`](skills/stratos-globus-coach/SKILL.md) | Three modes: learn the real camera and drone industries · **CIR gap analysis** with strategic group maps ([`globus_groups.py`](skills/stratos-globus-coach/scripts/globus_groups.py)) · year coaching with guardrails · **full-year review** from a capture file (the apparent strategy and general lessons, not recommendations). Student fill-in template: [`cir-gap-prompt.md`](skills/stratos-globus-coach/references/cir-gap-prompt.md) |

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

1. Download **`stratos-part2-3-skills.zip`** from the
   **[latest release](https://github.com/Brads777/stratos-external-analysis/releases/latest)** and unzip
   it once. Inside are 27 zips, one per skill. Leave those zipped.
2. In **Settings → Capabilities → Skills**, **delete** your current copies of
   `stratos-case-exhibits`, `stratos-strategic-mapping` and `stratos-globus-coach` (and
   `stratos-orchestrator-final` and the other Part 2 skills, if you installed v1.7.0).
3. Upload all 27 zips.
4. Switch **off** `stratos-orchestrator` (the Part 1 orchestrator). You should have **37 StratOS skills
   on**.
5. Replace `industries.json` in your Project knowledge with the new version (it adds `cameras` and
   `drones`), and make sure your saved `strategy-ledger` file is there too.
6. New chat in the Project: **"Run StratOS."** The intro should show three parts and modes A-E.

If your account limits how many skills can be on at once, keep the orchestrator and the skills you are
using this week switched on; the others still run from the standard framework, with a note.

### Claude Code

```bash
cp -r stratos-external-analysis/part2/skills/stratos-* ~/.claude/skills/
cp -r stratos-external-analysis/part3/skills/stratos-* ~/.claude/skills/
rm -r ~/.claude/skills/stratos-orchestrator      # the final orchestrator replaces it
```

## What is not included

The proprietary capability-fit scoring (SFI) runs behind the private StratOS API. Without it, VRIO uses
a transparent public screen and stamps its output `method: "public-screen"`.

## Licence

© 2026 Brad Scheller, [Apache License 2.0](../LICENSE). Sources:
[`SOURCES.md`](skills/stratos-orchestrator-final/references/SOURCES.md).
