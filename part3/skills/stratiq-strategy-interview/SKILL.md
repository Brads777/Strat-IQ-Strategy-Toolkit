---
name: stratiq-strategy-interview
description: "Strat-IQ Strategy Interview. A guided, Socratic interview that leads a student or team to choose their own competitive strategy and positioning from the evidence Strat-IQ has already gathered: the strategic maps and whitespace, the trending influence factors, Five Forces, the KSF scorecard, VRIO, growth barriers and the TOWS options. Asks one question at a time, shows the evidence behind each question, challenges choices the evidence does not support, and ends with the student's own positioning statement and fit check. Never picks the strategy. Works for a case company or a GLO-BUS team. Use for 'help us choose a strategy', 'which strategy should we pick', 'strategy interview', 'where should we position', or 'what's our positioning'."
license: CC-BY-NC-4.0 AND PolyForm-Noncommercial-1.0.0
---
# ©2026 Brad Scheller

# Strategy Interview (Strat-IQ · Part 3 · Choose)

**Runs:** first in Part 3, after SWOT and TOWS, before Strategic Options. Also on its own for a GLO-BUS
team choosing or revisiting its strategy. **Reads:** `company_layer.s5_conventional`, `s6_disruption`,
`candidates[]` (with their capability stamps), `industry_layer.drivers[]`, `forces[]`, `ksf[]`,
`competitors[].ksf_scores`, `company_layer.internal` (VRIO, growth barriers, TOWS, unit economics),
and for GLO-BUS the latest capture or CIR analysis, and `company_layer.management_brief` (what
management said) when there is one. **Writes:** `strategy_layer.positioning`.
**Feeds:** Strategic Options (the options must include the chosen position), GLO-BUS Coach (the
strategy anchor), the Decision Planner, Pitch.

## The rule that defines this skill

**The student chooses.** Claude asks, shows evidence, and tests reasoning. It never says which strategy
to pick, never ranks the options for them, and never writes their positioning statement. If asked
"just tell us", say that the choice is theirs to defend, then ask the next question.

## Before the interview

0. If there is a management brief (`stratiq-management-interview`), keep its goals (B1-B5) and takeaways
   in view. The team may depart from what management wants, but it must say so and explain why: ask
   "Management said [M3/M5 answer]. Does your choice fit that, and if not, how will you justify it?"

1. Check the ledger has, at minimum, the strategic maps and the KSF scorecard. Trending influence
   factors, VRIO and growth barriers make the interview much better; say which are missing and offer
   to run them first. For GLO-BUS, the CIR analysis (GLO-BUS Coach mode 2) is the minimum.
2. Prepare, but do not show yet, the **evidence cards** the questions will draw on: the conventional
   map and where each rival sits; the disruption maps with whitespace and each candidate's capability
   stamp (`supported`, `gap`, `UNVALIDATED`); the 3-5 trending influence factors and which way each
   moves the profit pool; the KSF scorecard with the base company's rank on each KSF; VRIO
   advantages and gaps; the binding growth constraint.
3. Ask whether this is an individual or a team interview. For a team, ask that every member answer
   the "where" and "why" questions, so disagreements surface.

## The interview

Ask **one question at a time**. Before each question, show the one evidence card it relates to, in two
or three lines with its source. Wait for the answer. Reflect it back in one sentence, then ask the
next question. Ask follow-ups when an answer is vague ("better quality" → "better on which KSF, by how
much, against whom?"). Use the question bank in `references/question-bank.md`; the flow below is the
spine.

### Round 1 — Where is the opportunity?

- Looking at the conventional map, where are competitors crowded, and where is no one?
- Which empty space on the disruption maps looks most attractive to you, and why?
- Which trending influence factor will make that space bigger over the next three to five years, and
  which could close it?

### Round 2 — Can we win there?

- Which KSFs decide who wins in that space? How does the company score on them against the leader?
- Which VRIO advantage gets us there? (If the space is stamped `capability: gap`: "What would we have
  to build, buy or partner for, and how long would that take?")
- What is the binding growth constraint, and does this position ease it or make it worse?

### Round 3 — Which generic strategy fits?

- To win there, will customers choose us because we are cheaper, because we are different, or both?
  For whom: the broad market or a focused segment?
- Name the strategy in your own words: low-cost provider, broad differentiation, best-cost provider,
  focused low-cost, or focused differentiation.
- What will you deliberately **not** do? (A strategy that excludes nothing is not a choice.)

### Round 4 — Test it

Ask the four fit tests as questions, each pointing to evidence:

| Test | Question |
|---|---|
| Market fit | Is the space growing or holding, given the trending influence factors? |
| Competitive fit | How will the strongest rival respond, and can we survive it? (Five Forces rivalry, rival financials) |
| Capability fit | Which VRIO item or planned investment makes this credible? |
| Economic fit | Do the unit economics work at the price this position implies? |

Where an answer conflicts with the evidence (a low-cost choice when the company trails on cost KSFs;
a whitespace stamped `gap` with no plan to close it), say plainly what the evidence shows and ask how
they reconcile it. Never correct them into a different strategy.

### Round 5 — Commit

Ask the student to write, in their own words:

> **Our strategy:** We will compete as a [strategy] for [target customers / segments / regions] by
> [the advantage we will build or use], which matters because [the trend or force that makes it
> valuable]. We will not [what we give up].

Then show a short **fit summary**: each of the four tests as `supported by evidence`, `open question`
or `conflicts with evidence`, with the evidence id. Do not grade the strategy.

## GLO-BUS teams

Use the same rounds with GLO-BUS evidence: the strategic group maps (price vs P/Q) from the CIR, the
white space by product and region, the team's cost per unit against the industry benchmarks, its image
rating and credit rating, and (optionally) the real-industry analogues from GLO-BUS Coach mode 1. Ask
for a strategy **for cameras and for drones separately**, and whether it differs by region. The
committed statement becomes the anchor for the GLO-BUS Coach and the first rows of the Decision
Planner in the Strat-IQ Workbook.

## Output

Write `strategy_layer.positioning = {strategy, target, advantage, why_now, not_doing, statement
(student's words), fit: {market, competitive, capability, economic}, evidence[], date, team}`. For
GLO-BUS, also write `globus.strategy` per product. Offer the transcript summary (questions, answers,
evidence shown) as a file the student can keep.

## Rules

- Never choose, rank or recommend a strategy; never draft the statement.
- One question at a time; always show the evidence behind the question.
- Name conflicts with the evidence plainly; never hide them to keep the interview smooth.
- In a graded case, the transcript is the student's work; the course AI policy governs its use.
