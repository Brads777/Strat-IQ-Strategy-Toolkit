---
name: stratos-stress-test
description: "StratOS Stress Test (optional case-memo Exhibit R). Attacks the leading option before anyone plans, in four modules: an assumption audit (load-bearing assumptions graded proven, analogous or belief, each danger-zone one with its cheapest test and an early-warning trigger), a competitor war-game grounded in Part 1 evidence, a risk register scored likelihood × impact and raised for velocity (risk_register.py), and a hostile Q&A drill of ten hard questions asked one at a time and scored. Use for 'stress test', 'pre-mortem', 'what could go wrong', 'war-game', 'risk register', 'devil's advocate', 'hostile Q&A', or 'Exhibit R'."
license: Apache-2.0
---
# ©2026 Brad Scheller

# Stress Test (StratOS · Part 3 · Test · Exhibit R)

**Runs:** after Expected Value, on the leading option (or the option the user names), **before any
planning**. **Reads:** the whole ledger. **Writes:** `strategy_layer.stress_test`. **Feeds:**
Initiative Prioritizer (mitigations become initiatives), Execution Roadmap (gates), Value Realization
(early-warning triggers), Memo Coach and Pitch (the hostile drill).

Attack the leader while changing course is still cheap. Run the four modules in order, with a
checkpoint after each; the user can run one alone ("just the war-game").

## Module 1 — Assumption audit

1. Pull out the **load-bearing assumptions**: the 5-10 inputs that, if wrong, flip the Business Case or
   the Expected Value ranking. Use the break-even sentence and the flip points to find them.
2. Grade each assumption's evidence: **proven** (direct evidence for this firm), **analogous** (true for
   a comparable firm or market), **belief** (no evidence yet).
3. Plot importance against evidence. The **danger zone** is high importance with `belief` or weak
   `analogous` evidence.
4. For each danger-zone assumption: the **cheapest test** that would prove or kill it (a pilot, a
   supplier quote, ten customer interviews) and an **early-warning trigger** (the indicator and
   threshold that says it is failing).

## Module 2 — Competitor war-game

For each major rival from the competitor set:

| Rival | Capability to respond (Part 1 evidence) | Incentive to respond | Most likely response | Timing | Effect on our option |
|---|---|---|---|---|---|

Ground capability in the financial benchmark (cash, margins, capacity) and incentive in what the move
threatens for them. Then re-check: **does the option still beat do nothing after the likely
responses?** If not, that is the headline.

## Module 3 — Risk register

List 8-15 risks across strategic, operational, financial, regulatory and reputational categories.
Score likelihood (1-5) and impact (1-5); add **velocity** (how fast it would hit: slow, medium, fast).
Run `scripts/risk_register.py` on `templates/risk-register.csv`: it scores, raises fast risks one band,
and flags every **high or critical** risk without an owner or with a non-mitigation. "Monitor",
"monitor closely" and "watch" are **not** mitigations; a mitigation changes likelihood or impact.

## Module 4 — Hostile Q&A drill

Ask **ten hard questions, one at a time**, in the voice the user chooses (board member, investor,
professor cold-calling). Wait for each answer. Score it 1-5 on directness, evidence used and
whether it conceded what must be conceded, and show the **evidence from the ledger they missed**.
At the end, the three weakest answers and what would make them strong. Never answer the questions for
the user.

## Output

```markdown
### R. Stress Test — [option]
**Danger-zone assumptions:** table (assumption · evidence grade · cheapest test · early-warning trigger)
**War-game:** table · **Still beats do nothing?** yes / no — why
**Risk register:** heat map + table (risk · L · I · velocity · score · band · owner · mitigation)
**Drill:** scores and the three weakest answers
**Impact Summary — Stress Test**
> _[Student writes this summary.]_
```

## Rules

- The stress test never changes the recommendation itself; it reports what the user must answer.
- Every rival response cites Part 1 evidence; no generic "competitors may respond".
- In a graded case, the student's recommendation is attacked as written; Claude does not repair it.
