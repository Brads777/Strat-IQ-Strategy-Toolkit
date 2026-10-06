---
name: stratos-strategic-options
description: "StratOS Strategic Options (optional case-memo Exhibit P). Frames the decision in three lines (situation, complication, question), builds at least three structurally different options plus 'do nothing' from the analysis already done (TOWS options, KSF gaps, supported whitespace, the binding growth constraint), and designs a staged first step for any large or irreversible bet. In a graded case, the student's own alternatives come first and anything Claude adds is marked SUGGESTED. Use for 'strategic options', 'alternatives', 'what are our choices', 'build vs partner vs buy', 'Exhibit P', or 'issue tree'."
license: Apache-2.0
---
# ©2026 Brad Scheller

# Strategic Options (StratOS · Part 3 · Choose · Exhibit P)

**Runs:** after the Strategy Interview. **Reads:** `strategy_layer.positioning` (the student's chosen
strategy), `company_layer.internal.tows`, `growth_barriers`, `full_potential`,
`vrio`, `company_layer.candidates[]`, `industry_layer.drivers[]`, `ksf[]`. **Writes:**
`strategy_layer.options`. **Feeds:** Decision Criteria and Matrix, Business Case, Expected Value,
Stress Test.

Analysis describes; it does not choose. This skill turns the analysis into a short list of real
choices, so that everything after it compares like with like.

## Step 1 — Frame the decision (SCQ)

Three lines, each citing its evidence:

- **Situation** — what everyone agrees on (a Part 1 fact about the industry and the firm's place in it).
- **Complication** — what broke it: a trending influence factor, a weakening force, a Part 2 gap or the
  binding growth constraint.
- **Question** — **one** decision, phrased as a choice: *"How should BYD compete in Europe's sub-€30k
  segment by 2029: build, partner or reposition?"*

Under the question, a short **issue tree**: the 2-4 sub-questions the choice depends on (demand,
capability, economics, competitor response). Each later Part 3 skill answers one of them.

## Step 2 — Build the options

When the Strategy Interview has run, the student's chosen position is **one of the options**, stated
in their words; the others are the strongest alternatives to it.

At least **three structurally different** options, plus **0. Do nothing** (the baseline every option
must beat; in a declining position, do nothing is not zero, so say what it costs).

- **Structurally different** means a different *route*: build vs partner vs buy vs reposition vs
  exit, not one idea at three levels of aggressiveness.
- **Every option names what it exploits**: a TOWS option (`SO-2`), a KSF gap, a whitespace candidate
  stamped `supported`, or the move that lifts the binding constraint.
- **No option rests on a `capability: "gap"` candidate** unless the option itself closes the gap
  (a partnership or acquisition that supplies the capability), and it says so.
- One line each on what it would take (money, capability, time) and what it gives up.

## Step 3 — Stage the big bets

For any option that is large or hard to reverse, design the **staged version**: the smallest first
step that reveals which future is unfolding (a pilot market, a minority stake, a supply MoU) and the
**gate** that releases the next commitment, with its threshold written now. This links to Expected
Value: the value of information says how much the first step is worth.

## In a graded case

The student's alternatives come first, in their words. Claude may add options only if the student
asks, and marks each `SUGGESTED`. The student confirms the final list before any later exhibit uses it.
Claude never chooses among them.

## Output

```markdown
### P. Strategic Options
**Situation:** … [id] · **Complication:** … [id] · **Question:** …
**Issue tree:** 1… 2… 3…
| # | Option | Route | Exploits (id) | What it takes | What it gives up | Staged first step / gate |
|---|---|---|---|---|---|---|
| 0 | Do nothing | baseline | — | — | — | — |
**Impact Summary — Strategic Options**
> _[Student writes this summary.]_
```

Write `strategy_layer.options = {scq, issue_tree[], options[], confirmed_by_user: bool}`.

## Rules

- Never fewer than three real options plus do nothing.
- Every option traces to the analysis; an option nobody's evidence points to is not an option yet.
- Never pick the option. Ranking happens in the Decision Matrix and Expected Value, and the choice is
  the user's.
