---
name: stratos-orchestrator
description: "StratOS External Analysis — the orchestrator for an end-to-end industry and competitor analysis. Walks the user through choosing an industry (EVs are pre-loaded; they can add another), the competitor list, the base company, perspective and depth, then runs the StratOS skills in order: Industry Overview (size, growth, segments, economics, history, players, life-cycle stage), Competitive Analysis (10-Ks, financials, news), PESTEL Analysis, Porter's Five Forces, Trending Influence Factors, KSFs (industry scorecard plus a per-company view), and Strategic Mapping with blue-ocean candidates — then delivers a detailed, cited Deep Research-style report (Word) and a 15-slide executive PowerPoint deck. Saves every step to one ledger in Project knowledge so work resumes across chats and the base company can be swapped. Use for 'external analysis', 'run StratOS', 'analyze the EV industry', 'industry and competitor analysis', or 'make X the base company'. Not for running one framework alone."
license: Apache-2.0
---
# ©2026 Brad Scheller

# StratOS External Analysis (orchestrator)

This skill does no analysis itself. It runs the intake, calls each StratOS skill in order, checks each
stage's output before moving on, and keeps the ledger. The stage skills must also be installed:

| Order | Display name | Skill ID | Stage | Produces |
|---|---|---|---|---|
| 1 | External Analysis | this skill | Intake | Industry, competitors, base company, perspective, depth |
| 2 | Industry Overview | `stratos-industry-overview` | IO | Definition, market size, growth, segments, economics, history, players, life-cycle stage (profile mode) |
| 3 | Competitive Analysis | `stratos-competitor-intel` | CI | Financials, 10-K risk factors and MD&A trends, news and signals, candidate KSFs |
| 4 | PESTEL Analysis | `stratos-pestel` | S1 | 15-25 macro findings, each tied to a P&L line |
| 5 | Porter's Five Forces | `stratos-five-forces` | S2 | Forces scored 1-5 now, attractiveness, profit pool |
| 6 | Trending Influence Factors | `stratos-driving-forces` | S3 | 3-5 drivers from all sources; forces re-scored at the horizon |
| 7 | KSFs | `stratos-ksf` | KSF | Tier 1 industry scorecard; Tier 2 per-company view |
| 8 | Strategic Mapping | `stratos-strategic-mapping` | S4-S6 | Vector shortlist, conventional and disruption maps, blue-ocean candidates |
| 9 | Executive Deck | `stratos-exec-deck` | Deck | 15-slide executive PowerPoint built from the ledger and the report |

**Case-memo tools** (mode C — the course's Case Analysis Memo):

| Display name | Skill ID | Produces |
|---|---|---|
| Case Memo Exhibits | `stratos-case-exhibits` | The template's Exhibits C-G and L-O in order, Impact Summaries blank |
| Decision Criteria | `stratos-decision-criteria` | Exhibit L — goal-linked criteria, weights 1-5 |
| Decision Matrix | `stratos-decision-matrix` | Exhibits N (pros/cons) and M (weighted matrix, `decision_matrix.py`) |
| Segment Value | `stratos-segment-value` | Exhibit O — segment CLV × customers (`segment_value.py`), when data exists |

Industry Overview runs first to set the scene — what the industry is, how big, how it makes money, who
plays. Competitive Analysis follows because competitors' 10-K risk factors and MD&A are primary
evidence for PESTEL and for the trending influence factors. At report time the Industry Overview runs
again in **finalise mode** to add the trends, the rivalry score and the roadmap. Stage ids S1-S6
follow the StratOS build plan; IO, CI and KSF are named rather than numbered so the plan's
cross-references stay valid.

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
- **C. Build my case-memo exhibits** — hand off to `stratos-case-exhibits`, which sets the scope from
  the case (its industry, competitors, and the case company as base) and builds the course template's
  Exhibits C-G and L-O. The student writes the memo, Exhibits A-B and every Impact Summary.
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
| An industry overview, market size, growth and projections, segments, history, life-cycle stage | IO (profile mode) |
| A competitor's financials, news, moves or moat | CI |
| Macro threats, regulation, economy, social or tech trends | CI (filings scan) → PESTEL |
| Industry attractiveness, profitability, bargaining power | CI → PESTEL → Five Forces |
| What is changing, the future of the industry | CI → PESTEL → Five Forces → Trending Influence Factors |
| What it takes to win, KSFs, who is strongest | … → KSFs |
| Positioning, strategic groups, whitespace, blue ocean | … → KSFs → Strategic Mapping |
| "What if X were the base company?" | the base-company swap (below) |
| A deck, slides, a presentation | the full chain if the ledger is incomplete → Executive Deck |
| Case-memo exhibits, decision criteria, decision matrix, pros/cons, segment CLV | Case Memo Exhibits (mode C), or the single case-memo tool asked for |

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
  promoted, flag that the filter may not have run — a warning, not a blocking error.
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

- **Industry layer** — Industry Overview, Competitive Analysis evidence, PESTEL, Five Forces, trending influence
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

The run ends with **two deliverables**: a detailed research report and an executive deck.

### 1. The detailed report (Deep Research style)

A long-form research document, not a summary: typically 15-30 pages at full depth. Write it from
`templates/report-outline.md` as connected narrative — each section explains what the evidence shows,
why it matters, and how it links to the sections around it — with the stage tables embedded where they
carry the argument.

- **Numbered citations** in the text ([1], [2] …) for every figure and factual claim, resolving to a
  **References** list at the end (publisher or filing, title, date, URL). Evidence ids map to reference
  numbers.
- **Appendices** hold the full stage tables (all PESTEL findings, the complete benchmark, the full KSF
  scorecard and sensitivity results, vector shortlist and coordinates) so the body can stay readable.
- Deliver it as a **Word document** (`.docx`) when file creation is available, otherwise as Markdown in
  the chat. File name: `external-analysis_<industry>_<base-company>_<YYYY-MM-DD>.docx`.

Sections:

1. **Executive summary** — 5-7 bullets, each answering a key question from the brief. Lead with the
   governing thought: where this industry's profit is going, and where the base company could stand.

**Part I — External factors**

2. **Industry overview** — the opening of the external analysis, written the way the industry
   section of a business plan is: 1-2 pages of plain narrative with small tables, readable by someone
   who knows nothing about the industry. Run `stratos-industry-overview` in **finalise mode** and use
   its ten components in order: definition and scope · market size · growth and projections ·
   segments and customers · industry economics and value chain · recent history · key players and
   level of competition (with the Five Forces rivalry score) · life-cycle stage · trends influencing
   the industry (the Trending Influence Factors, one or two lines each; the full analysis follows in
   section 4) · what this analysis covers.
3. **Industry attractiveness** — verdict and trend (now → horizon), from Five Forces and PESTEL.
4. **Trending influence factors** shaping the next 3-5 years, with mechanisms and forces moved.
5. **Competitive landscape** — benchmark highlights and cross-peer insights.
6. **KSFs** — Tier 1 scorecard with sensitivity notes and white space; the base company's Tier 2 view.

**Part II — Position and opportunity**

7. **Strategic maps** — conventional and disruption, with blue-ocean candidates stamped
   `demand: "unpriced"` and `capability: "UNVALIDATED"` until the internal analysis runs. An
   unvalidated gap may be a **Mirage Trap**: empty because nobody wants it, or because this firm
   cannot serve it.
8. **Implications for the perspective** — 3-5 moves, each tied to a KSF gap or whitespace.
9. **Watch list** — leading indicators, each with the threshold that would trigger a re-run.
10. **Consistency check and confidence** — cross-stage results, open conflicts, data gaps.

11. **References** — the numbered source list.
12. **Appendices** — full stage tables, methodology, and the scoring method used (`api` or
    `public-screen`).

### 2. The executive deck

Invoke `stratos-exec-deck` with the ledger and the finished report. It produces a 15-slide PowerPoint
(12 at quick depth) with action titles, one visual per slide, sources on every data slide, and the
detail in speaker notes. Every number must match the report.

### 3. Hand-off

Give the user the report, the deck, and the ledger file, and say where to save the ledger (Project
knowledge in Claude.ai) so the next chat can resume or swap the base company. On a base-company swap,
offer to regenerate the report sections in Part II and the deck.

Sources and licences: `references/SOURCES.md`.
