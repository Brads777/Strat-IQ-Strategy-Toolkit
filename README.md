# StratOS External Analysis

**A Claude skill pack that analyses an industry and its competitors the way a strategy consultant
does — from annual reports to blue-ocean whitespace — with every claim traced to evidence.**

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
![Skills: 8](https://img.shields.io/badge/skills-8-brightgreen)
![Works in: Claude.ai · Claude Code · Cowork](https://img.shields.io/badge/works%20in-Claude.ai%20%C2%B7%20Claude%20Code%20%C2%B7%20Cowork-orange)

Built by **Brad Scheller** for MGT4850 Strategic Management (Northeastern University, Fall 2026) and
for real client work. Part of the StratOS (Strategy OS) toolkit.

---

## What it does

Pick an industry, list the competitors, choose a base company — and StratOS runs one connected
external analysis:

```mermaid
flowchart LR
    A[Intake<br/>industry · competitors<br/>base company] --> B[Competitive Analysis<br/>10-Ks · financials · news]
    B --> C[PESTEL Analysis<br/>macro → P&L line]
    C --> D[Porter's Five Forces<br/>scored 1–5 · profit pool]
    D --> E[Trending Influence Factors<br/>3–5 drivers · forces re-scored]
    E --> F[KSFs<br/>industry scorecard +<br/>per-company view]
    F --> G[Strategic Mapping<br/>36 vectors · whitespace ·<br/>blue ocean · ERRC]
    G --> H[Detailed research report<br/>+ saved ledger] --> I[Executive<br/>PowerPoint deck]
```

Most AI strategy prompts produce five disconnected frameworks. StratOS treats them as **one evidence
base rendered five ways**, so they cannot contradict each other:

- **Primary evidence first.** Competitors' 10-K risk factors and MD&A are mined *before* PESTEL —
  management's own disclosure of what threatens the business, made under legal liability.
- **Every finding hits the P&L.** Each PESTEL factor, trend and force names the P&L line it moves
  (price, volume, mix, input costs, opex, capex, financing, levies) and in which direction.
- **Chain rules, enforced.** No force score without evidence; no trend without at least two source
  types; no KSF that does not trace to a force or trend; no map axis chosen freely.
- **KSFs in two tiers.** One industry yardstick scores every competitor comparably — then each firm
  gets a strategy-weighted view and its own critical success factors.
- **Maps that find something.** Instead of price vs. quality (where everyone lines up on a diagonal),
  firms are re-plotted on orthogonal vectors from a 36-vector library to expose empty space.
- **Honest about whitespace.** Blue-ocean candidates ship stamped `capability: UNVALIDATED` — an empty
  space may be a *Mirage Trap* that nobody wants or this firm cannot serve.
- **Nothing is lost between chats.** Every stage writes to one JSON ledger. Swap the base company and
  only the company layer reruns.

## The skills

| Display name | Skill ID | What it produces |
|---|---|---|
| **External Analysis** | [`stratos-orchestrator`](skills/stratos-orchestrator/SKILL.md) | Intro screen, guided or question mode, intake, chain checks, ledger, final report |
| **Competitive Analysis** | [`stratos-competitor-intel`](skills/stratos-competitor-intel/SKILL.md) | Financial benchmark (3 yrs + LTM), 10-K seeds, hiring/patent/news signals, moats |
| **PESTEL Analysis** | [`stratos-pestel`](skills/stratos-pestel/SKILL.md) | 15–25 findings with impact, certainty, velocity, P&L line, transmission mechanism |
| **Porter's Five Forces** | [`stratos-five-forces`](skills/stratos-five-forces/SKILL.md) | Forces scored 1–5 on evidence, attractiveness, profit-pool close |
| **Trending Influence Factors** | [`stratos-driving-forces`](skills/stratos-driving-forces/SKILL.md) | 3–5 drivers from all sources, forces re-scored at the horizon |
| **KSFs** | [`stratos-ksf`](skills/stratos-ksf/SKILL.md) | 6–10 KSFs, weighted scorecard ([`score_ksf.py`](skills/stratos-ksf/scripts/score_ksf.py)), sensitivity, white space |
| **Strategic Mapping** | [`stratos-strategic-mapping`](skills/stratos-strategic-mapping/SKILL.md) | Conventional and disruption maps, whitespace, blue-ocean candidates with ERRC |
| **Executive Deck** | [`stratos-exec-deck`](skills/stratos-exec-deck/SKILL.md) | 15-slide executive PowerPoint: action titles, one chart per slide, sources, speaker notes |

Each stage skill also works on its own — ask for "a PESTEL of the EV industry" and only that skill runs.

---

## Install

A full step-by-step guide with links is in **[the install guide](https://brads777.github.io/stratos-external-analysis/install-guide.html)** (source: [docs/install-guide.html](docs/install-guide.html)).
The short version:

### Claude.ai (web — no install; what MGT4850 students use)

1. In **Settings → Capabilities**, turn on **Code execution and file creation** (needed for skills).
   On a university or company plan, an admin may need to enable skills for you.
2. Download **`stratos-all-skills.zip`** from the **[latest release](../../releases/latest)** and unzip
   it — inside are eight zips, one per skill (leave those zipped).
3. In **Settings → Capabilities → Skills**, choose **Upload skill** and upload all eight zips.
   *Instructors:* if your admin provisions the skills org-wide, students skip steps 1–3.
4. Create a **Project** (e.g. "StratOS — EV industry") and add
   [`project-data/industries.json`](project-data/industries.json) to its **Project knowledge**.
5. Open a chat in that Project and type **"Run StratOS External Analysis."**

### Claude Code (terminal)

```bash
git clone https://github.com/Brads777/stratos-external-analysis.git
cp -r stratos-external-analysis/skills/stratos-* ~/.claude/skills/
cd your-analysis-folder && mkdir -p project-data
cp /path/to/stratos-external-analysis/project-data/industries.json project-data/
claude    # then: "Run StratOS External Analysis"
```

The KSF scoring script needs Python 3.10+ (`python skills/stratos-ksf/scripts/score_ksf.py <csv>`).

### Optional: live financial data via OpenBB

Competitive Analysis uses the [OpenBB](https://github.com/OpenBB-finance/OpenBB) MCP server as its
default data source when connected, and falls back to SEC EDGAR and web research when not.
Setup: [`openbb-mcp.md`](skills/stratos-competitor-intel/references/openbb-mcp.md).

---

## Using it

When the orchestrator opens it shows an intro screen and asks how you want to work:

| Mode | What happens |
|---|---|
| **A. Walk me through it** | All seven steps in order, with a checkpoint after each (continue / revise / stop), ending in a full report: executive summary, an **industry overview** (recent history, market size, level of competition, growth and projections, trends), attractiveness verdict, KSF scorecard, strategic maps, recommended moves, watch list — delivered as a detailed, cited Word report plus a 15-slide executive PowerPoint. |
| **B. Ask a specific question** | Runs only the steps your question depends on, says which it ran, and answers. |
| **Resume** | Attach a saved `strategy-ledger-*.json` and continue where you stopped. |

Example prompts:

- *"Run StratOS External Analysis on the EV industry with BYD as the base company."*
- *"What are the key success factors for EVs, and who is strongest?"*
- *"How does Stellantis compare financially with BYD and Xiaomi?"*
- *"Where is the whitespace in this industry?"*
- *"Now make Xiaomi the base company."* — keeps the industry analysis, reruns only the company view.

### Adding your own industry

Choose **"Add another industry"** at intake, or add an entry to
[`project-data/industries.json`](project-data/industries.json):

```json
{ "id": "dental-dso", "name": "Dental service organisations", "boundary": "…",
  "geography": "US", "horizon": "2026-2029", "scenario": "Enterprise", "locked": false,
  "competitors": [ { "name": "…", "ownership": "private", "ticker": null } ] }
```

Entries with `"locked": true` keep a fixed class competitor list that students cannot edit.

### Where your work is saved

Every stage writes to a single ledger (schema: [`ledger-schema.md`](skills/stratos-orchestrator/references/ledger-schema.md)).
In Claude.ai, download it at each checkpoint and add it to the Project's knowledge; in Claude Code it
lives at `.strategy/ledgers/<scope>.json`.

---

## What is not included

StratOS's proprietary scoring algorithms (W-B-A-F-D vector scoring, P-E-F decision-criteria
weighting, SFI and SCE) run behind a private StratOS API and are **not** in this repository. Without
the API the skills use transparent public fallbacks and stamp their output `method: "public-screen"`.

**Known gap:** the public fallback screen for assigning the five vector roles in Strategic Mapping is
still being written (marked `TODO(Brad)` in the skill).

## Evidence discipline

The skills never invent market shares, margins, prices, regulation names, dates or statistics.
Figures without a source are marked `[unverified]`; private-company figures are marked `[E]`
(estimate) with low confidence; missing data is shown as a visible caveat, never hidden.
Outputs are analysis aids, not investment advice.

## Credits and licence

Original skill text © 2026 Brad Scheller, released under the [Apache License 2.0](LICENSE).
The skills synthesise methods from open-source work by Anthropic (`financial-services-plugins`),
DogInfantry (B1 management consultant), Eric Young (`alpha-insights`), Pawel Huryn (`pm-skills`),
ironyjk (`strategy-frameworks`) and Yoichi Ojima (`consultant`). Full provenance and licences:
[`SOURCES.md`](skills/stratos-orchestrator/references/SOURCES.md) and [`NOTICE`](NOTICE).

Issues and pull requests are welcome.
