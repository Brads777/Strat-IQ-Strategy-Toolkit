---
name: stratos-orchestrator
description: "StratOS External Analysis — the orchestrator for an end-to-end industry and competitor analysis. Walks the user through choosing an industry (EVs are pre-loaded; they can add another), the competitor list, the base company, perspective and depth, then runs the StratOS skills in order: Competitive Analysis (10-Ks, financials, news), PESTEL Analysis, Porter's Five Forces, Trending Influence Factors, KSFs (industry scorecard plus a per-company view), and Strategic Mapping with blue-ocean candidates. Saves every step to one ledger in Project knowledge so work resumes across chats and the base company can be swapped. Use for 'external analysis', 'run StratOS', 'analyze the EV industry', 'industry and competitor analysis', or 'make X the base company'. Not for running one framework alone."
license: Apache-2.0
---
# ©2026 Brad Scheller

# StratOS External Analysis (orchestrator)

This skill does no analysis itself. It runs the intake, calls each StratOS skill in order, checks each
stage's output before moving on, and keeps the ledger. The stage skills must also be installed:

| Order | Display name | Skill ID | Stage | Produces |
|---|---|---|---|---|
| 1 | External Analysis | this skill | Intake | Industry, competitors, base company, perspective, depth |
| 2 | Competitive Analysis | `stratos-competitor-intel` | CI | Financials, 10-K risk factors and MD&A trends, news and signals, candidate KSFs |
| 3 | PESTEL Analysis | `stratos-pestel` | S1 | 15-25 macro findings, each tied to a P&L line |
| 4 | Porter's Five Forces | `stratos-five-forces` | S2 | Forces scored 1-5 now, attractiveness, profit pool |
| 5 | Trending Influence Factors | `stratos-driving-forces` | S3 | 3-5 drivers from all sources; forces re-scored at the horizon |
| 6 | KSFs | `stratos-ksf` | KSF | Tier 1 industry scorecard; Tier 2 per-company view |
| 7 | Strategic Mapping | `stratos-strategic-mapping` | S4-S6 | Vector shortlist, conventional and disruption maps, blue-ocean candidates |

Competitive Analysis runs **first** because competitors' 10-K risk factors and MD&A are primary
evidence for PESTEL and for the trending influence factors. Stage ids S1-S6 follow the StratOS build
plan; CI and KSF are named rather than numbered so the plan's cross-references stay valid.

If a stage skill does not load, run that stage with the standard framework, put a note at the top of
its output saying it ran without its skill, and continue.

## Step 0 — Intro screen and mode

When this skill opens, show the intro screen from `templates/intro.md`: what StratOS does, the seven
steps in one table, and the two ways to work. In Claude.ai, render it as a clean, visually structured
card (a simple self-contained artifact is fine); elsewhere, as formatted text. Then offer the choice
with the interactive widget:

- **A. Guided walkthrough** — Steps 1-4 below in order, a checkpoint after every stage, and the full
  final report at the end.
- **B. Ask a specific question** — the question resolver below.
- **Resume** — if a ledger is attached or in Project knowledge, offer to continue from its last stage.

The user can switch modes at any time: "walk me through the rest" turns a question into a guided run
from wherever the ledger stands.

### The question resolver (mode B)

1. **Set scope first.** Every question still needs Steps 1-3 (industry, competitors, base company).
   Ask only for what is missing, briefly.
2. **Answer from the ledger if you can.** If the stages the question needs are already in the ledger
   and not stale, answer from them, and say which stage and `asof` date the answer comes from.
3. **Otherwise run the minimum chain** the question depends on — never a later stage without its
   inputs:

| The question is about… | Stages to run (in order) |
|---|---|
| A competitor's financials, news, moves or moat | CI |
| Macro threats, regulation, economy, social or tech trends | CI (filings scan) → PESTEL |
| Industry attractiveness, profitability, bargaining power | CI → PESTEL → Five Forces |
| What is changing, the future of the industry | CI → PESTEL → Five Forces → Trending Influence Factors |
| What it takes to win, KSFs, who is strongest | … → KSFs |
| Positioning, strategic groups, whitespace, blue ocean | … → KSFs → Strategic Mapping |
| "What if X were the base company?" | the base-company swap (below) |

4. **Say what you ran.** Start the answer with one line: which stages ran, which came from the ledger,
   and any stage run in quick depth. Then answer the question directly, citing evidence ids.
5. **Offer the next step** — the natural follow-up question, or "want the full report?"

If a question fits no row, answer it from whatever the ledger holds and say what analysis would make
the answer stronger.

## Step 1 — Choose the industry

Read `industries.json` from Project knowledge (or the project's `project-data/` folder). Offer the
listed industries as a choice, plus **"Add another industry"**.

- **Existing industry** — load its boundary note, geography, horizon and competitor list.
- **Add another** — ask for the industry name, a one-line demand-side boundary (what job customers
  hire this industry to do, what is in and out), geography, and horizon (default 3-5 years). Append
  it to `industries.json` and tell the user to re-save the file to Project knowledge.

Use the interactive choice widget when the surface has one; otherwise a numbered list.

## Step 2 — Build the competitor list

- **Course industry** (flagged `"locked": true`, e.g. EVs for MGT4850): show the fixed class list.
  Students analyse exactly these firms; do not add or drop any.
- **Any other industry**: show the saved list if there is one, then let the user add, remove or
  rename firms. Aim for 4-8, and suggest (never silently add) one non-obvious substitute or adjacent
  entrant. Save the result back to `industries.json`.

For each competitor record: name, ownership (public / private / state-owned / segment of a
conglomerate), and ticker or filing identifier if public. Ownership decides what can be found —
private firms have no 10-K, and that gap must show in the output.

## Step 3 — Base company, perspective, depth

- **Base company** — the firm whose strategy we are reading.
- **Perspective** — incumbent, entrant, investor, or neutral. It shapes the implications section.
- **Depth** — *quick* (3-4 competitors, top 5 items per framework, 6 KSFs) or *full* (each skill's
  defaults).
- **Key questions** — 1-3 decisions this analysis should inform.

Write the run brief from `templates/run-brief.md` and record the scope in the ledger.

**Hard gate:** do not start Competitive Analysis until industry, competitors and base company are
set. Ask for anything missing; never substitute a default.

## Step 4 — Run the stages

For each stage: invoke the skill, pass it the ledger, receive its section, run the checks below,
write the ledger, then **checkpoint** — show the stage's table and a 3-5 bullet **handoff** (what the
next stages most need), list any warnings, and ask *continue / revise / stop*. If the user says "run
it all", run through and checkpoint once at the end with every warning listed.

If a ledger for this scope already exists, hydrate from it, say which stage it reached and its `asof`
date, and resume from the next stage.

## Checks between stages

- **R1 (revised by Brad, 2026-09-29)** — every trending influence factor cites at least one finding or
  evidence id and should draw on **at least two different source types** (e.g. a 10-K risk factor plus
  a news item). The original rule required a PESTEL finding; drivers now come from all data sources.
- **R2** — every force score cites at least one evidence id.
- **R3** — drivers are a filtered subset, typically 3-5. If more than ~40% of candidates were
  promoted, warn that the filter may not have run (warn, do not refuse).
- **R4** — every KSF traces to a force or a driver.
- **R5** — map axes come from the KSFs and the vector shortlist, never free choice.
- **R6** — every claim carries an evidence id or `[unverified]`; the competitor benchmark has no
  unsourced cells (`n/a` with a reason). Missing data is a visible caveat, never silence.
- **R7** — scope is set (Steps 1-3) before any evidence is gathered.

**Consistency check after KSFs:** every heavily weighted KSF traces to a force or trending factor, and
no PESTEL finding rated high-impact was dropped from Five Forces, trending factors or KSFs without a
stated reason. Resolve conflicts or record them.

A failed check sends the stage back once with the reason. If it fails again, pass it through with the
failure listed in `warnings` and shown at the checkpoint.

## Swapping the base company

The ledger has two layers:

- **Industry layer** — Competitive Analysis evidence, PESTEL, Five Forces, trending influence
  factors, Tier 1 KSFs and scorecard, vector shortlist. The same whichever firm is the base.
- **Company layer** — KSF Tier 2 (the firm's strategy-weighted view and its own critical success
  factors), and the maps, whitespace, blue-ocean candidates and ERRC read from that firm's side.

When the user says "make X the base company", keep the industry layer, set the new base company, and
rerun only **KSF Tier 2** and **Strategic Mapping**. Say which layer was reused and its `asof` date.
This is the class's central point: industry forces are shared, and positioning is a choice.

## Where the ledger lives

| Surface | Location |
|---|---|
| Claude.ai | `strategy-ledger-{scope_id}.json` in the chat sandbox. At every checkpoint, offer it as a download and remind the user to replace the copy in Project knowledge, so the next chat resumes where this one stopped. |
| Claude Code / Cowork | `.strategy/ledgers/{scope_id}.json`, plus a one-line `json:context_update` to `.strategy/context.json` on exit. |

The full schema and the P&L line taxonomy are in `references/ledger-schema.md`. Each stage skill also
states the section it writes, so it can run on its own.

## Proprietary scoring

The attractiveness weights and the vector scoring are proprietary StratOS algorithms that run behind
the scoring API. No StratOS skill contains them. When the API is not connected (the normal case in a
classroom chat), stages use their public fallbacks and stamp `method: "public-screen"`.

## Final report

Write it from `templates/report-outline.md`, synthesising rather than copying the stage outputs, and
linking every number to the stage that sourced it:

1. **Executive summary** — 5-7 bullets, each answering a key question from the brief. Lead with the
   governing thought: where this industry's profit is going, and where the base company could stand.
2. **Industry attractiveness** — verdict and trend (now → horizon).
3. **Trending influence factors** shaping the next 3-5 years.
4. **Competitive landscape** — benchmark highlights and cross-peer insights.
5. **KSFs** — Tier 1 scorecard with sensitivity notes and white space; the base company's Tier 2 view.
6. **Strategic maps** — conventional and disruption, with blue-ocean candidates stamped
   `demand: "unpriced"` and `capability: "UNVALIDATED"` until the internal analysis runs. An
   unvalidated gap may be a **Mirage Trap**: empty because nobody wants it, or because this firm
   cannot serve it.
7. **Implications for the perspective** — 3-5 moves, each tied to a KSF gap or whitespace.
8. **Watch list** — leading indicators, each with the threshold that would trigger a re-run.
9. **Consistency check and confidence** — cross-stage results, open conflicts, data gaps.

Then hand over the ledger file and say where to save it.

Sources and licences: `references/SOURCES.md`.
