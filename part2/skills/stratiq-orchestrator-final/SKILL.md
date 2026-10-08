---
name: stratiq-orchestrator-final
description: "Strat-IQ Strategic Analysis: the orchestrator for the whole toolkit. Replaces stratiq-orchestrator and takes precedence over it. Reads the saved ledger and continues from the last finished step: Part 1 external analysis (industry, competitors, PESTEL, Five Forces, trends, KSFs, maps), Part 2 internal analysis (value chain, unit economics, VRIO, full potential, growth barriers, SWOT), Part 3 making the strategy work (options, business case, expected value, stress test, go-to-market, plan, KPIs, pitch). Also routes GLO-BUS questions to the GLO-BUS Coach and builds case-memo exhibits. Use for 'run Strat-IQ', 'continue my analysis', 'Part 2', 'Part 3', 'make the strategy work', 'GLO-BUS', or 'make X the base company'. Not for running one framework alone."
license: CC-BY-NC-4.0 AND PolyForm-Noncommercial-1.0.0
---
# ©2026 Brad Scheller

# Strat-IQ Strategic Analysis (orchestrator — final)

This skill replaces `stratiq-orchestrator`, the Part 1 orchestrator. Part 1 is taught first with the
old orchestrator; this one is uploaded in the second session, with the Part 2 skills.

## Turning off the old orchestrator

When both are installed, **this skill takes over**:

- Never invoke `stratiq-orchestrator`, and never follow its instructions if it has loaded. Every
  orchestration request — run, resume, a specific question, case exhibits, a base-company swap — is
  handled here.
- If the old orchestrator's eight-step intro has already been shown in this chat, say that the updated
  orchestrator is taking over, and restart at Step 0 below. Keep any ledger already written.
- The first time this skill opens in a chat, check whether `stratiq-orchestrator` is among the
  available skills. If it is, tell the user once, before the intro screen: *"The Part 1 orchestrator is
  still switched on. Go to Settings → Capabilities → Skills and switch off `stratiq-orchestrator`, so
  that 'run Strat-IQ' always opens this version."* Then continue; do not wait for them to do it.

A skill cannot switch another skill off. The user has to do that in settings; until they do, the rules
above keep the old one out of the way.

It does no analysis itself. It runs the intake, checks what has already been done, calls each Strat-IQ
skill in order, checks each stage's output before moving on, and keeps the ledger. The stage skills
must also be installed.

**Part 1 — External analysis** (what the industry rewards):

| Order | Display name | Skill ID | Stage | Produces |
|---|---|---|---|---|
| 1 | Set up | this skill | Intake | Industry, competitors, base company, perspective, depth |
| 2 | Industry Overview | `stratiq-industry-overview` | IO | Definition, market size, growth, segments, economics, history, players, life-cycle stage (profile mode) |
| 3 | Competitive Analysis | `stratiq-competitor-intel` | CI | Financials, 10-K risk factors and MD&A trends, news and signals, candidate KSFs |
| 4 | PESTEL Analysis | `stratiq-pestel` | S1 | 15-25 macro findings, each tied to a P&L line |
| 5 | Porter's Five Forces | `stratiq-five-forces` | S2 | Forces scored 1-5 now, attractiveness, profit pool |
| 6 | Trending Influence Factors | `stratiq-driving-forces` | S3 | 3-5 drivers from all sources; forces re-scored at the horizon |
| 7 | KSFs | `stratiq-ksf` | KSF | Tier 1 industry scorecard; Tier 2 per-company view |
| 8 | Strategic Mapping | `stratiq-strategic-mapping` | S4-S6 | Vector shortlist, conventional and disruption maps, blue-ocean candidates |

**Part 2 — Internal analysis** (what the base company can do about it):

| Order | Display name | Skill ID | Stage | Produces |
|---|---|---|---|---|
| 9 | Value Chain | `stratiq-value-chain` | S8 | The firm's activities by cost, value and evolution stage |
| 10 | Unit Economics | `stratiq-unit-economics` | UE | Contribution per unit, break-even, CAC and LTV, sensitivity (J-1) |
| 11 | Resources and Capabilities | `stratiq-resources-capabilities` | RC | Resources, capabilities, candidate core competencies (inventory mode) |
| 12 | VRIO Analysis | `stratiq-vrio` | S9 | Advantage verdicts, the reality check, the capability stamp on each blue-ocean candidate |
| 13 | Resources and Capabilities | `stratiq-resources-capabilities` | RC | Confirmed core competencies and competitive advantage (finalise mode) |
| 14 | Full Potential | `stratiq-full-potential` | FP | The profit gap to benchmark, driver by driver, and how controllable it is (K-1) |
| 15 | Growth Barriers | `stratiq-growth-barriers` | GB | The binding constraint on growth (K-2) |
| 16 | SWOT Analysis | `stratiq-swot` | S10 | Four traced lists and the TOWS strategic options |

**Part 3 — Making the strategy work** (what to do, whether it survives attack, how to make it work).
Mode D runs it in four moves, with a checkpoint after each step:

| Move | Order | Display name | Skill ID | Produces |
|---|---|---|---|---|
| Choose | 17 | Strategy Interview | `stratiq-strategy-interview` | One question at a time, the student chooses their own strategy and positioning from the evidence; positioning statement and fit check |
| Choose | 18 | Strategic Options | `stratiq-strategic-options` | SCQ framing, 3+ options plus do nothing, staged bets (P) |
| Choose | 19 | Decision Criteria and Matrix | `stratiq-decision-criteria`, `stratiq-decision-matrix` | Criteria, pros/cons, weighted scoring of the options |
| Choose | 20 | Business Case | `stratiq-business-case` | NPV, IRR, payback, break-even sentence (Q-1); tornado and Monte Carlo on request (Q-3) |
| Choose | — | Pricing | `stratiq-pricing` | Only when price is a lever |
| Choose | — | Synergy Case | `stratiq-synergy-case` | Only when an option is a deal |
| Choose | 21 | Expected Value | `stratiq-expected-value` | Expected NPV, maximin, flip point, EVPI (Q-2); Bayesian pilot value and, with Business Case, tornado and Monte Carlo (Q-3) |
| Test | 22 | Stress Test | `stratiq-stress-test` | Assumption audit, war-game, risk register, hostile drill (R) |
| Plan | 23 | Go-to-Market | `stratiq-gtm` | Beachhead, ICP, channels, funnel and CAC, launch gates (T) |
| Plan | 24 | Initiative Prioritizer | `stratiq-initiative-prioritizer` | Ranked, traced initiatives cut to capacity (S) |
| Plan | 25 | Operating Model | `stratiq-operating-model` | Must-win capabilities, RAPID, structure, 7S |
| Plan | 26 | Stakeholder Map | `stratiq-stakeholder-map` | Power-interest grid, coalition math, plans for sceptics |
| Plan | — | Negotiation Prep | `stratiq-negotiation-prep` | Only when a deal must be struck |
| Plan | 27 | Execution Roadmap | `stratiq-execution-roadmap` | First 100 days, milestones, stage gates (S) |
| Track | 28 | Value Realization | `stratiq-value-realization` | Balanced Scorecard and Strategy Map now (U); plan vs actual later |
| Track | — | Strat-IQ Workbook | `stratiq-workbook` | The whole analysis as live Excel worksheets, pre-filled from the ledger, plus the GLO-BUS Decision Planner. Two-way: `read_workbook.py` writes the team's edits back into the ledger |
| Track | — | Memo Coach | `stratiq-memo-coach` | Checks a case memo draft; never writes it |
| Track | — | Executive and VC Pitch | `stratiq-pitch` | Board or VC pitch from the ledger, readiness scorecard |

Steps marked — run only when an option needs them or the user asks. Say when one is skipped and why.

**Deliverable:** `stratiq-exec-deck` (Deck) — the 15-slide executive PowerPoint built from the ledger
and the report.

**Case-memo tools** (mode C — the course's Case Analysis Memo):

| Display name | Skill ID | Produces |
|---|---|---|
| Case Memo Exhibits | `stratiq-case-exhibits` | The template's Exhibits C-O in order, Impact Summaries blank |
| Decision Criteria | `stratiq-decision-criteria` | Exhibit L — goal-linked criteria, weights 1-5 |
| Decision Matrix | `stratiq-decision-matrix` | Exhibits N (pros/cons) and M (weighted matrix, `decision_matrix.py`) |
| Segment Value | `stratiq-segment-value` | Exhibit O — segment CLV × customers (`segment_value.py`), when data exists |

**Simulation tool (mode E):** `stratiq-globus-coach` (GLO-BUS Coach). Any question about GLO-BUS
decisions, rounds, scores, the CIR or the Camera & Drone Journal goes straight to it. It has four
modes: learn the real camera or drone industry (`cameras` and `drones` in `industries.json`, run as a
quick Strat-IQ chain), a CIR gap analysis (strategic group maps, white space and next-year moves),
year-by-year coaching with guardrails, and a full-year review. Requests to capture, screenshot or pull
a team's GLO-BUS screens go to `stratiq-globus-capture` (read-only, after the team signs in), which
then hands its capture file to the coach. Part 2 and Part 3 skills also work on a GLO-BUS company: Unit
Economics, Growth Barriers, Pricing and Value Realization read the team's own reports instead of
filings.

In Part 1, Industry Overview runs first to set the scene. Competitive Analysis follows because
competitors' 10-K risk factors and MD&A are primary evidence for PESTEL and for the trending influence
factors. At report time the Industry Overview runs again in **finalise mode** to add the trends, the
rivalry score and the roadmap. In Part 2, the Value Chain runs first because capabilities are found in
the activities; Unit Economics follows because every later number rests on what one unit earns; VRIO
tests what the inventory lists; Full Potential and Growth Barriers size the gap and find what binds;
and SWOT runs last because it is where the two parts meet. Part 3 starts from the SWOT's TOWS options. Stage ids S1-S10 follow the Strat-IQ build plan (S7, market research, is not in this
toolkit); IO, CI, KSF and RC are named rather than numbered so the plan's cross-references stay valid.

If a stage skill does not load, run that stage with the standard framework, put a note at the top of
its output saying it ran without its skill, and continue.

## Step 0 — Intro screen and mode

When this skill opens, show the intro screen from `templates/intro.md`: what Strat-IQ does, the steps in
the three parts, and the ways to work. In Claude.ai, render it as a clean, visually structured card (a
simple self-contained artifact is fine); elsewhere, as formatted text. Then offer the choice with the
interactive widget:

- **A. Guided walkthrough** — the Part 1 check below, then every remaining stage in order, a
  checkpoint after each, and the full final report at the end.
- **B. Ask a specific question** — the question resolver below.
- **C. Build my case-memo exhibits** — hand off to `stratiq-case-exhibits`, which asks the student
  for the case facts (the cases are persona interviews, so there is no case document): company,
  industry, competitors and interview notes. It sets the scope from them and builds the course
  template's Exhibits C-O (and, if asked, the optional J-1, K-1, K-2 and P-T). The student writes the
  memo, Exhibits A-B and every Impact Summary.
- **D. Make the strategy work** — Part 3 from the saved ledger: confirm the 1-3 decisions it must
  answer, then Choose → Test → Plan → Track, with a checkpoint after every step. Needs Part 2 at least
  through SWOT (R15); if it is missing, offer to run it first.
- **E. Help with GLO-BUS** — start with `stratiq-management-interview` if there is no brief yet, then
  hand off to `stratiq-globus-coach`, which asks which of its five modes the team needs (learn the real
  industry, CIR gap analysis, year coaching, full-year review, weekly progress report).

**Start with the management interview.** Before any mode, check the ledger for
`company_layer.management_brief` (or `globus.management_brief`). If the team has interviewed management
and there is no brief, offer `stratiq-management-interview` first: it records the central problem,
decisions, required goals and management's questions that the memo, the decision criteria, the Strategy
Interview and the GLO-BUS weekly report all build on. A team can skip it, but say what it costs.

The user can switch modes at any time: "walk me through the rest" turns a question into a guided run
from wherever the ledger stands.

## Step 1 — Has Part 1 been done?

Run this check before asking any intake question, in every mode.

**1. Find the ledger.** Look for `strategy-ledger-{scope_id}.json` attached to the chat or in Project
knowledge (Claude.ai), or in `.strategy/ledgers/` (Claude Code / Cowork). If there is none, ask once:
*"Have you already run the external analysis for this industry? If so, upload the saved
`strategy-ledger` file."* A ledger written by the earlier `stratiq-orchestrator` is valid; it simply
has no `company_layer.internal` section yet.

**2. Read what it holds.** Part 1 is **complete** when all of these are present:

| Section | Written by |
|---|---|
| `scope` with industry, competitor set and a base company (`company_layer.focal_firm`) | Set up |
| `industry_layer.overview` | Industry Overview |
| `competitors[]` with financials or a stated reason for each gap | Competitive Analysis |
| `industry_layer.pestel[]` | PESTEL |
| `industry_layer.forces[]` with `score_now` and `score_horizon` | Five Forces, Trending Influence Factors |
| `industry_layer.drivers[]` | Trending Influence Factors |
| `industry_layer.ksf[]` and `company_layer.ksf_view` | KSFs |
| `company_layer.s5_conventional`, `s6_disruption` and `candidates[]` | Strategic Mapping |

Judge by the sections present, not only by the `checkpoint` field.

**3. Decide the route**, and tell the user which one it is and why before running anything:

| What the check finds | Route |
|---|---|
| **Part 1 complete** | Say so, with the industry, base company and `asof` date. Skip the intake. **Continue from there: start Part 2** at Value Chain. |
| **Part 1 partly done** | Say which stage it reached. Resume Part 1 at the next missing stage, finish it, then run Part 2. |
| **Part 2 partly done** | Resume Part 2 at the next missing stage. A ledger from v2 without `unit_economics`, `full_potential` or `growth_barriers` is Part 2 partly done: run only those three. |
| **Parts 1 and 2 complete** | Say so. Offer mode D (Part 3), the report and deck, a base-company swap, or a refresh of stale items. |
| **Part 3 partly done** | Resume mode D at the next missing step of `strategy_layer`. |
| **The request is about GLO-BUS** | Skip the check; go to `stratiq-globus-coach`. A GLO-BUS ledger is separate from the course-industry ledger. |
| **No ledger, or the ledger is for a different industry** | **Run the entire process**: the intake (Steps 2-4), Part 1, then Part 2. |

**4. Before continuing from an existing Part 1, check three things:**

- **Staleness.** If any ids are in `stale`, or evidence has passed its `expires` date, list the
  affected stages and re-run them before Part 2. Part 2 built on a stale Part 1 inherits the error.
- **Base company.** Confirm the base company with the user. If they want a different one, do the
  base-company swap first (below), then Part 2.
- **Depth.** If Part 1 was run at quick depth, say so; Part 2 will rest on fewer KSFs and competitors.

Never re-run a completed stage that is not stale unless the user asks. The point of the check is that
finished work is kept.

**In mode C** the same check applies: Exhibits C-G come from the Part 1 stages. If the ledger holds
them, `stratiq-case-exhibits` builds H-K from Part 2 and then L-O, instead of starting again at C.

### The question resolver (mode B)

1. **Set scope first.** Every question needs the industry, competitors and base company. Take them
   from the ledger if the Part 1 check found one; otherwise ask only for what is missing, briefly.
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
| Where the company's costs go, which activities create value, build or buy | … → KSFs → Value Chain |
| What the company is good at, its resources, core competencies | … → KSFs → Value Chain → Resources and Capabilities |
| Whether an advantage is sustainable, VRIO, whether the company can reach a whitespace | … → Resources and Capabilities → VRIO |
| Strengths, weaknesses, opportunities, threats, strategic options | Part 1 through KSFs → Part 2 → SWOT |
| "What if X were the base company?" | the base-company swap (below) |
| A deck, slides, a presentation | the full chain if the ledger is incomplete → Executive Deck |
| Case-memo exhibits, decision criteria, decision matrix, pros/cons, segment CLV | Case Memo Exhibits (mode C), or the single case-memo tool asked for |
| Contribution per unit, break-even volume, CAC, LTV | … → Value Chain → Unit Economics |
| How much better the company could perform, the profit gap | … → Unit Economics → VRIO → Full Potential |
| What is holding growth back, the bottleneck | … → Full Potential → Growth Barriers |
| Which strategy or positioning to choose (the student decides) | Part 1 through Strategic Mapping (ideally Part 2) → Strategy Interview |
| What the company's options are, build vs partner vs buy | Part 2 through SWOT → Strategy Interview → Strategic Options |
| Whether an option is worth it, NPV, IRR | … → Strategic Options → Business Case |
| Which option is the better bet under uncertainty | … → Business Case → Expected Value |
| How risky the case is; which assumption matters most; whether a pilot is worth it | Business Case (Risk Analysis) → Expected Value (pilot) |
| What price to charge; whether a deal's synergies cover the premium; how to negotiate it | Pricing; Synergy Case; Negotiation Prep (each needs Strategic Options and Business Case) |
| What could go wrong, war-game, risk register, hostile questions | … → Expected Value → Stress Test (one module if asked) |
| How to win customers, beachhead, channels, CAC | … → Stress Test → Go-to-Market |
| What to do first, organisation, stakeholders, first 100 days | … → Initiative Prioritizer → Operating Model → Stakeholder Map → Execution Roadmap |
| KPIs, balanced scorecard, strategy map, plan vs actual | Value Realization |
| An Excel workbook or worksheets of the analysis, or a GLO-BUS decision planner | `stratiq-workbook` (from the ledger as it stands, plus any GLO-BUS capture files) |
| "We edited the workbook" / "read our workbook back" | `stratiq-workbook` read-back (`read_workbook.py --dry-run`, show the changes, then write them to the ledger) before any other step |
| Checking GLO-BUS entries against the plan | `stratiq-globus-capture` Step 5 |
| Feedback on a memo draft | Memo Coach |
| A board or investor pitch | the Part 3 chain the ledger lacks → Pitch |
| Anything about GLO-BUS, the CIR or the Camera & Drone Journal | `stratiq-globus-coach` |

4. **Say what you ran.** Start the answer with one line: which stages ran, which came from the ledger,
   and any stage run in quick depth. Then answer the question directly, citing evidence ids.
5. **Offer the next step** — the natural follow-up question, or "want the full report?"

If a question fits no row, answer it from whatever the ledger holds and say what analysis would make
the answer stronger.

## Step 2 — Choose the industry

*(Steps 2-4 are the intake. Skip them when the Part 1 check found a ledger with the scope set.)*

Read `industries.json` from Project knowledge (or the project's `project-data/` folder). Offer the
listed industries as a choice, plus **"Add another industry"**.

- **Existing industry** — load its boundary note, geography, horizon and competitor list.
- **Add another** — ask for the industry name, a one-line demand-side boundary (what job customers
  hire this industry to do, what is in and out), geography, and horizon (default 3-5 years). Append
  it to `industries.json` and tell the user to re-save the file to Project knowledge.

Use the interactive choice widget when the surface has one; otherwise a numbered list.

## Step 3 — Build the competitor list

- **Course industry** (flagged `"locked": true`, e.g. EVs for MGT4850): show the fixed class list.
  Students analyse exactly these firms; do not add or drop any.
- **Any other industry**: show the saved list if there is one, then let the user add, remove or
  rename firms. Aim for 4-8, and suggest (never silently add) one non-obvious substitute or adjacent
  entrant. Save the result back to `industries.json`.

For each competitor record: name, ownership (public / private / state-owned / segment of a
conglomerate), and ticker or filing identifier if public. Ownership decides what can be found —
private firms have no 10-K, and that gap must show in the output.

## Step 4 — Base company, perspective, depth

- **Base company** — the firm whose strategy we are reading. Part 2 analyses this firm from the
  inside, so say what internal evidence is available: filings for a public firm, the student's
  interview notes in a case, or what the user can supply.
- **Perspective** — incumbent, entrant, investor, or neutral. It shapes the implications section.
- **Depth** — *quick* (3-4 competitors, top 5 items per framework, 6 KSFs) or *full* (each skill's
  defaults).
- **Key questions** — 1-3 decisions this analysis should inform.

Write the run brief from `templates/run-brief.md` and record the scope in the ledger.

**Hard gate:** do not start Competitive Analysis until industry, competitors and base company are
set. Ask for anything missing; never substitute a default.

## Step 5 — Run the stages

Start at the stage the Part 1 check chose. For each stage: invoke the skill, pass it the ledger,
receive its section, run the checks below, write the ledger, then **checkpoint** — show the stage's
table and a 3-5 bullet **handoff** (what the next stages most need), list any warnings, and ask
*continue / revise / stop*. If the user says "run it all", run through and checkpoint once at the end
with every warning listed.

**Between Part 1 and Part 2**, checkpoint even on "run it all": say that the external analysis is
complete, that Part 2 reads inside the base company, and what internal evidence it will use. This is
where a user can stop with a complete external analysis.

## Checks between stages

**Part 1**

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
- **R7** — scope is set (Steps 2-4, or a ledger that holds it) before any evidence is gathered.

**Consistency check after KSFs:** every heavily weighted KSF traces to a force or trending factor, and
no PESTEL finding rated high-impact was dropped from Five Forces, trending factors or KSFs without a
stated reason. Resolve conflicts or record them.

**Part 2**

- **R8** — Part 2 does not start until Part 1 has reached KSFs at least. VRIO's value test and its
  reality check both read the KSFs; without them every capability looks valuable.
- **R9** — every internal fact cites its source (interview notes, a filing, user-supplied) or is
  marked `[ask in interview]` / `n/a`. No invented cost shares, headcounts or processes.
- **R10** — every capability names the resources it combines; every VRIO Yes and No cites evidence;
  rarity is counted against the competitor set.
- **R11** — every SWOT item cites the finding it came from, and every TOWS option names the items it
  pairs.
- **R12** — after VRIO, no blue-ocean candidate is still stamped `capability: "UNVALIDATED"`.

- **R13** — Unit Economics keeps fixed and variable costs apart, and every input is cited, `[estimate]`
  or `[ask in interview]`.
- **R14** — Growth Barriers names one binding constraint (or a justified pair), with evidence.

**Consistency check after SWOT:** no strength rests on a competence trap; no SO option rests on a
candidate stamped `capability: "gap"`; and the base company's KSF Tier 2 strategy agrees with the
competitive advantage Part 2 found — or the disagreement is reported as a finding.

**Part 3**

- **R15** — Part 3 does not start until Part 2 has reached SWOT. Options built without TOWS, VRIO and
  the binding constraint are guesses.
- **R16a** — the Strategy Interview never chooses for the student; the positioning statement is in
  the student's words, and Strategic Options includes the chosen position among its options.
- **R16** — at least three structurally different options plus do nothing, each tracing to a TOWS
  option, KSF gap, supported whitespace or the binding constraint. In a case, the student confirms the
  list; anything Claude adds is marked `SUGGESTED`.
- **R17** — every Business Case and Expected Value input is cited or listed as an assumption, and every
  listed assumption appears in the Stress Test's audit.
- **R18** — every initiative, milestone and KPI traces to a finding, an option, a mitigation or the GTM
  plan. Nothing new appears in the plan.
- **R19** — in a graded case, Part 3 never writes the recommendation, memo text or an Impact Summary.
  GTM's CAC fits Unit Economics, or the conflict is reported.

**Between Choose and Test**, checkpoint even on "run it all": show the options with NPV and expected
value, and ask which option to stress-test. The choice is the user's.

A failed check sends the stage back once with the reason. If it fails again, pass it through with the
failure listed in `warnings` and shown at the checkpoint.

## Swapping the base company

The ledger has two layers:

- **Industry layer** — Industry Overview, Competitive Analysis evidence, PESTEL, Five Forces, trending
  influence factors, Tier 1 KSFs and scorecard, vector shortlist. The same whichever firm is the base.
- **Company layer** — KSF Tier 2, the maps, whitespace, blue-ocean candidates and ERRC read from that
  firm's side, and **all of Part 2** (`company_layer.internal`).

When the user says "make X the base company", keep the industry layer, set the new base company, and
rerun **KSF Tier 2**, **Strategic Mapping**, and then **Part 2 in full** — a different firm has
different activities, resources and capabilities. Any `strategy_layer` (Part 3) belongs to the old base
company: archive it under `strategy_layer_archive[]` and offer to run mode D again. Say which layer was reused and its `asof` date. This
is the class's central point: industry forces are shared, and positioning is a choice.

## Where the ledger lives

| Surface | Location |
|---|---|
| Claude.ai | `strategy-ledger-{scope_id}.json` in the chat sandbox. At every checkpoint, offer it as a download and remind the user to replace the copy in Project knowledge, so the next chat resumes where this one stopped. |
| Claude Code / Cowork | `.strategy/ledgers/{scope_id}.json`, plus a one-line `json:context_update` to `.strategy/context.json` on exit. |

The full schema and the P&L line taxonomy are in `references/ledger-schema.md`. Each stage skill also
states the section it writes, so it can run on its own.

## Proprietary scoring

The attractiveness weights, the vector scoring and the capability-fit scoring are proprietary Strat-IQ
algorithms that run behind the scoring API. No Strat-IQ skill contains them. When the API is not
connected (the normal case in a classroom chat), stages use their public fallbacks and stamp
`method: "public-screen"`.

## Final report

The run ends with **two deliverables**: a detailed research report and an executive deck.

### 1. The detailed report (Deep Research style)

A long-form research document, not a summary: typically 20-35 pages at full depth. Write it from
`templates/report-outline.md` as connected narrative — each section explains what the evidence shows,
why it matters, and how it links to the sections around it — with the stage tables embedded where they
carry the argument.

- **Numbered citations** in the text ([1], [2] …) for every figure and factual claim, resolving to a
  **References** list at the end (publisher or filing, title, date, URL). Evidence ids map to reference
  numbers.
- **Appendices** hold the full stage tables so the body can stay readable.
- Deliver it as a **Word document** (`.docx`) when file creation is available, otherwise as Markdown in
  the chat. File name: `strategic-analysis_<industry>_<base-company>_<YYYY-MM-DD>.docx`.

Sections:

1. **Executive summary** — 5-7 bullets, each answering a key question from the brief. Lead with the
   governing thought: where this industry's profit is going, where the base company could stand, and
   whether it has what it takes to get there.

**Part I — External factors**

2. **Industry overview** — the opening of the external analysis, written the way the industry
   section of a business plan is: 1-2 pages of plain narrative with small tables, readable by someone
   who knows nothing about the industry. Run `stratiq-industry-overview` in **finalise mode** and use
   its ten components in order: definition and scope · market size · growth and projections ·
   segments and customers · industry economics and value chain · recent history · key players and
   level of competition (with the Five Forces rivalry score) · life-cycle stage · trends influencing
   the industry (the Trending Influence Factors, one or two lines each; the full analysis follows in
   section 4) · what this analysis covers.
3. **Industry attractiveness** — verdict and trend (now → horizon), from Five Forces and PESTEL.
4. **Trending influence factors** shaping the next 3-5 years, with mechanisms and forces moved.
5. **Competitive landscape** — benchmark highlights and cross-peer insights.
6. **KSFs** — Tier 1 scorecard with sensitivity notes and white space; the base company's Tier 2 view.
7. **Strategic maps** — conventional and disruption, with the blue-ocean candidates and their stamps.

**Part II — The base company**

8. **Value chain** — the firm's activities by evolution stage; differentiating engines, value traps,
   and stage-sourcing mismatches.
9. **Resources, capabilities and core competencies** — the inventory and the competencies that
   survived the tests.
10. **VRIO** — the verdict table, the reality check and any competence traps; which blue-ocean
    candidates are `supported` and which are a `gap`. A candidate still `demand: "unpriced"` with
    `capability: "gap"` is a **Mirage Trap**: empty because nobody wants it, or because this firm
    cannot serve it.
11. **SWOT and strategic options** — the four traced lists and the TOWS matrix.

    Before SWOT in this part: **unit economics**, **full potential** (the bridge) and **growth
    barriers** (the binding constraint).

**Part III — Position and opportunity**

12. **Implications for the perspective** — 3-5 moves, each tied to a TOWS option, a KSF gap or a
    supported whitespace. (When Part 3 has run, this section summarises it and points to Part IV.)
13. **Watch list** — leading indicators, each with the threshold that would trigger a re-run.
14. **Consistency check and confidence** — cross-stage results, open conflicts, data gaps.

**Part IV — Making the strategy work** (only when mode D has run)

15. **Options and the choice** — the student's positioning statement and fit check, SCQ, options, decision matrix, business case, expected value.
16. **Stress test** — danger-zone assumptions, war-game, top risks.
17. **Go-to-market and plan** — beachhead and CAC, ranked initiatives, operating model, stakeholders,
    first 100 days and gates.
18. **Balanced Scorecard and Strategy Map** — objectives in four perspectives, the cause-and-effect
    map, measures and triggers.

19. **References** — the numbered source list.
20. **Appendices** — full stage tables, methodology, and the scoring method used (`api` or
    `public-screen`).

In a graded case, Part IV presents the student's confirmed options and inputs and contains no
recommendation. If the user stops after Part 1, deliver the report without Part II and say that the blue-ocean
candidates remain `capability: "UNVALIDATED"`.

### 2. The executive deck

Invoke `stratiq-exec-deck` with the ledger and the finished report. It produces a 15-slide PowerPoint
(12 at quick depth) with action titles, one visual per slide, sources on every data slide, and the
detail in speaker notes. Every number must match the report. When Part 2 has run, ask it to give the
internal analysis its slides (the VRIO table and the SWOT with TOWS options) within the same count.

### 3. Hand-off

Give the user the report, the deck, and the ledger file (and offer the `stratiq-workbook` Excel file), and say where to save the ledger (Project
knowledge in Claude.ai) so the next chat can resume or swap the base company. On a base-company swap,
offer to regenerate Parts II and III of the report and the deck.

Sources and licences: `references/SOURCES.md`.
