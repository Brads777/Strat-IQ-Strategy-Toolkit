---
name: stratiq-operating-model
description: "Strat-IQ Operating Model. Asks how the organisation must work to execute the chosen strategy: starts from the 3-5 things the strategy needs done exceptionally well, assigns decision rights with RAPID for the decisions that set speed, chooses a structure for a stated reason, runs a McKinsey 7S coherence check (do incentives fight the strategy?), and offers spans and layers as hypotheses to investigate. Use for 'operating model', 'org design', 'RAPID', 'decision rights', '7S', 'how should we organise', or 'who decides'."
license: CC-BY-NC-4.0 AND PolyForm-Noncommercial-1.0.0
---
# ©2026 Brad Scheller

# Operating Model (Strat-IQ · Part 3 · Plan)

**Runs:** after the Initiative Prioritizer. **Reads:** `strategy_layer.options` (chosen),
`initiatives[]`, `company_layer.internal.value_chain`, `resources_capabilities`, `vrio`. **Writes:**
`strategy_layer.operating_model`. **Feeds:** Stakeholder Map, Execution Roadmap.

## Step 1 — The 3-5 must-win capabilities

From the strategy and the initiatives: the few things the organisation must do **exceptionally well**
(not merely adequately) for the strategy to work. Each traces to a KSF, a VRIO item or a top initiative.
Everything else in the organisation is designed to serve these.

## Step 2 — Decision rights (RAPID)

For the 4-8 decisions that set the strategy's speed (e.g. launch pricing, supplier selection, model
cancellation, market entry), assign:

| Decision | **R**ecommend | **A**gree (veto) | **P**erform | **I**nput | **D**ecide (one person) |
|---|---|---|---|---|---|

One **D** per decision. Too many **A**s are where speed dies; flag any decision with more than one.

## Step 3 — Structure, with the reason

Choose the primary axis (function, product/business unit, geography, customer, or matrix) for the
must-win capabilities, and say **why** in one sentence. Name what the choice makes harder and how that
is compensated (a council, a shared service, a coordination role).

## Step 4 — 7S coherence check

| S | Current state (evidence) | What the strategy needs | Coherent? |
|---|---|---|---|
| Strategy · Structure · Systems · Shared values · Style · Staff · Skills | | | |

The most common failure: **incentives and systems that fight the strategy** (a speed strategy whose
reviews punish mistakes; a cost strategy that pays for revenue). Name each incoherence and its fix.

## Step 5 — Spans and layers (hypotheses)

Where evidence allows (filings, interview notes), note layers between the CEO and the front line and
typical spans of control. Present as **hypotheses to investigate**, never as findings, unless the data
is real.

## Output

Must-win capabilities · RAPID table · structure choice and reason · 7S table with fixes · spans and
layers hypotheses. Write `strategy_layer.operating_model`.

## Rules

- Never invent headcounts or reporting lines; mark gaps `[ask in interview]` or `n/a`.
- Structure follows strategy: every structural choice cites a must-win capability.
