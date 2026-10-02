# StratOS Part 2 — Internal Analysis

**The second session of StratOS.** Part 1 (the skills in [`../skills`](../skills)) reads the industry:
what it rewards and where the empty space is. Part 2 reads the **company**: what it can actually do
about it.

Part 2 is a separate, smaller upload. It adds to the fourteen Part 1 skills; it does not replace them,
apart from the orchestrator.

## What it adds

| Display name | Skill ID | What it produces |
|---|---|---|
| **Strategic Analysis** | [`stratos-orchestrator-final`](skills/stratos-orchestrator-final/SKILL.md) | Replaces `stratos-orchestrator`. Checks the saved ledger: if Part 1 is done it continues into Part 2; if not, it runs the entire process |
| **Value Chain** | [`stratos-value-chain`](skills/stratos-value-chain/SKILL.md) | Exhibit J — Porter's activities with cost share against value share ([`value_chain.py`](skills/stratos-value-chain/scripts/value_chain.py)), each filed under its evolution stage: commodity, product, custom, genesis |
| **Resources and Capabilities** | [`stratos-resources-capabilities`](skills/stratos-resources-capabilities/SKILL.md) | Exhibit H — resources, capabilities, core competencies, competitive advantage |
| **VRIO Analysis** | [`stratos-vrio`](skills/stratos-vrio/SKILL.md) | Exhibit I — four tests in order on cited evidence ([`vrio_screen.py`](skills/stratos-vrio/scripts/vrio_screen.py)), competence-trap check against the KSFs, and the capability stamp on each blue-ocean candidate |
| **SWOT Analysis** | [`stratos-swot`](skills/stratos-swot/SKILL.md) | Exhibit K — four lists traced to the earlier stages, crossed into SO, WO, ST and WT strategic options |

Two Part 1 skills are updated to work with these:

| Skill | Change |
|---|---|
| [`stratos-case-exhibits`](skills/stratos-case-exhibits/SKILL.md) | Builds the Case Analysis Memo exhibits C–O, including H–K |
| [`stratos-strategic-mapping`](skills/stratos-strategic-mapping/SKILL.md) | Blue-ocean candidates move from `capability: UNVALIDATED` to `supported` or `gap` once VRIO has run |

## How Part 2 connects to Part 1

- **It picks up where Part 1 stopped.** Everything Part 1 produced is in the `strategy-ledger` file.
  The new orchestrator reads it, keeps the finished work, and starts at Value Chain.
- **VRIO tests the map.** A whitespace found in Part 1 is only an opportunity if this company can
  reach it. VRIO sets each candidate to `supported` or `gap`.
- **Nothing is brainstormed.** Every strength, weakness, opportunity and threat points to the finding
  it came from. Internal facts come from filings or the user's own notes; gaps are marked
  `[ask in interview]`, never filled in.

## Install

Step-by-step, with links: **[the Part 2 guide](https://brads777.github.io/stratos-external-analysis/part2-guide.html)**
(source: [`../docs/part2-guide.html`](../docs/part2-guide.html)). The short version:

### Claude.ai

1. Download **`stratos-part2-skills.zip`** from the **[latest release](https://github.com/Brads777/stratos-external-analysis/releases/latest)** and
   unzip it once. Inside are seven zips, one per skill (leave those zipped).
2. In **Settings → Capabilities → Skills**, upload the five new skills, then upload
   `stratos-case-exhibits` and `stratos-strategic-mapping` again to replace the Part 1 versions.
3. Switch **off** `stratos-orchestrator`. Leave `stratos-orchestrator-final` on.
4. Make sure your saved `strategy-ledger` file is in the Project's knowledge.
5. Open a new chat in the Project and type **"Run StratOS and continue my analysis from where I left
   off."**

### Claude Code

```bash
cp -r stratos-external-analysis/part2/skills/stratos-* ~/.claude/skills/
rm -r ~/.claude/skills/stratos-orchestrator      # the final orchestrator replaces it
```

The ledger at `.strategy/ledgers/<scope>.json` is found automatically. The two scripts need Python
3.10+.

## What is not included

The proprietary capability-fit scoring (SFI) runs behind the private StratOS API and is not in this
repository. Without it, VRIO uses a transparent public screen — a link check against the industry's
KSFs — and stamps its output `method: "public-screen"`.

## Licence

© 2026 Brad Scheller, [Apache License 2.0](../LICENSE). Sources:
[`SOURCES.md`](skills/stratos-orchestrator-final/references/SOURCES.md).
