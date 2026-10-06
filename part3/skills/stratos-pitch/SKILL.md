---
name: stratos-pitch
description: "StratOS Executive and VC Pitch. Turns the finished StratOS analysis into the pitch that gets the strategy funded, in two versions: a board pitch (8-12 slides, decision and ask first) or a VC pitch (10-14 slides: problem, solution, why now, market sized top-down and bottom-up, traction, unit economics, go-to-market, competition, team, financials, risks, the ask and use of funds). Every number comes from the ledger; it never invents traction. Ends with a readiness scorecard and offers the hostile Q&A drill in an investor's voice. In graded work it follows the instructor's AI policy, defaulting to structure plus critique. Use for 'pitch', 'pitch deck', 'VC pitch', 'board pitch', 'investor deck', 'TAM SAM SOM', or 'get this funded'."
license: Apache-2.0
---
# ©2026 Brad Scheller

# Executive and VC Pitch (StratOS · Part 3 · Track and pitch)

**Runs:** at the end, from a ledger with at least Strategic Options and Business Case. **Reads:** the
whole ledger. **Writes:** `strategy_layer.pitch`. **Builds with:** `stratos-exec-deck` conventions
(action titles, one visual per slide, sources, speaker notes) and the pptx skill.

## Step 1 — Which pitch, and what the ask is

Ask: **board** (internal approval of a strategy and budget) or **VC/investor** (external funding)?
And: **what is the ask** (amount, decision, timing)? A pitch without an ask is a report.

## Board pitch · 8-12 slides

1. The decision and the ask (first, in one sentence)
2. Why now: the complication (Part 1 driver or Part 2 gap)
3. Options considered, including do nothing, and why they lost (Decision Matrix)
4. The recommended option and what it exploits
5. Business case: NPV, IRR, payback, the break-even sentence
6. Expected value and risk: worst case, flip point, value of information
7. Stress test: top risks with owners and mitigations; rival responses
8. Go-to-market (if relevant)
9. Plan: first 100 days, stage gates with thresholds
10. KPIs and how the board will know it is working
11. The ask again, with the gates that release each tranche

## VC pitch · 10-14 slides

Problem · solution · why now · **market size** · product · traction · business model and **unit
economics** · **go-to-market** · competition (the strategic map) · team · financials · risks and
mitigations · **the ask and use of funds**.

**Market sizing two ways:** TAM, SAM and SOM **top-down** (industry total → serviceable segment →
obtainable share, from the Industry Overview) and **bottom-up** (reachable customers × price, from the
GTM funnel). If the two SAMs differ by more than ~30%, flag it on the slide's speaker notes and say
which is more credible.

## Step 2 — Build it

Every number comes from the ledger, with its source on the slide. **Never invent traction**, customer
names, team credentials or quotes; missing items are placeholders the user must fill
(`[add: pilot customers]`). Speaker notes carry the narration.

## Step 3 — Readiness scorecard

Score each slide 1-5 on clarity, evidence and relevance to the ask. Name the **three weakest slides**
and what would fix each. Then offer the **hostile Q&A drill** (`stratos-stress-test` module 4) in the
voice of a sceptical investor or board member.

## In graded work

Follow the instructor's AI policy. **By default, build the structure (slide titles, what goes on each,
which ledger items feed it) and critique the student's draft**, rather than writing the slides. Write
full slide content only when the instructor's policy allows it.

## Rules

- No invented traction, metrics, customers, quotes or team facts.
- Every chart and figure carries its source; numbers match the report and the business case exactly.
