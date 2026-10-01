---
name: stratos-decision-matrix
description: "StratOS Decision Matrix and Pros/Cons (case-memo Exhibits M and N). For each management question, takes the student's alternatives (or suggests 2-3 for the student to confirm), builds an evidence-backed pros-and-cons table, then rates every alternative 1-10 on each weighted decision criterion and computes the weighted totals, ties and weight sensitivity with a script. Use for 'decision matrix', 'weighted scoring', 'pros and cons', 'evaluate the alternatives', 'Exhibit M', or 'Exhibit N'."
license: Apache-2.0
---
# ©2026 Brad Scheller

# Decision Matrix and Pros/Cons (StratOS · Exhibits M and N)

**Reads:** the student's **Exhibit B** (management questions, goals), **Exhibit L** (criteria and
weights from `stratos-decision-criteria`), and the evidence in Exhibits C-G. **Writes:**
`case.issues[]`, Exhibit N (pros and cons) and Exhibit M (decision matrix).

Run N before M. Listing the pros and cons first gives every rating in the matrix a reason someone can
check.

## Step 1 — Issues and alternatives

Each **management question** from Exhibit B is one issue. For each issue, collect its alternatives:

- **The student supplies them.** Use exactly the alternatives the student lists.
- **If the student lists none for an issue,** suggest 2-3 distinct, realistic alternatives, label each
  `SUGGESTED — confirm or replace`, and **stop for the student to confirm or edit them before any
  scoring**. Defining the options is part of the student's analysis.
- Alternatives must be mutually exclusive answers to the same question. "Do nothing / status quo" is a
  legitimate alternative when management could choose it.
- If Exhibit L is missing, run `stratos-decision-criteria` first.

## Step 2 — Exhibit N: pros and cons

For each alternative, list 2-4 pros and 2-4 cons. Each one:

- is **specific to this case**, not a generic statement ("raises fixed cost by adding a second
  plant", not "expensive");
- **cites its evidence** — an exhibit (e.g. "Exhibit E: buyer power 4/5") or a case fact;
- connects, where it can, to a decision criterion.

## Step 3 — Exhibit M: rate and weight

For each issue, rate every alternative **1-10 on each criterion**, where 10 best satisfies the
criterion. Every rating needs a one-line reason drawn from Exhibit N or C-G; keep those reasons in the
working notes (the template's matrix shows numbers only). Rate each criterion **across** the
alternatives side by side so the scale stays consistent.

**Compute deterministically.** Fill `templates/decision-matrix.csv` (columns `issue, criterion, weight`,
then one column per alternative; one row per criterion per issue). Where code execution is available,
run:

```
python scripts/decision_matrix.py decision-matrix.csv
```

It checks weights are 1-5 and ratings 1-10, computes Weight × Rating and the totals per issue, ranks
the alternatives, flags near-ties (within 3% of the leader), and runs a sensitivity test (each weight
moved ±1 within 1-5) to show whether the leading alternative changes. Without code execution, do the
same steps by hand and say so.

- **A near-tie is not a win.** Report it as a tie and say which criterion would decide it.
- **If the leader changes under a ±1 weight shift,** say which weight is pivotal; the student must
  defend that weight in Exhibit L.

## Output (template format)

```markdown
### M. Decision Matrix

**Issue 1: [management question]**

| Criteria | Weight | [Alt 1] | Score | [Alt 2] | Score |
|---|---|---|---|---|---|
| [Criterion 1] | [w] | [1-10] | [W×R] | [1-10] | [W×R] |
| **Total Score** | | | **[sum]** | | **[sum]** |

Sensitivity: [stable | leader changes when … ] · Tie: [none | Alt X vs Alt Y]

**Impact Summary — Decision Matrix**
> _[Student writes this summary.]_

### N. Pros and Cons Analysis

| Issue | | Pros | Cons |
|---|---|---|---|
| **Issue 1: [question]** | Alternative 1 | • … (Exhibit E) | • … (case p. 4) |
| | Alternative 2 | • … | • … |

**Impact Summary — Pros and Cons Analysis**
> _[Student writes this summary.]_
```

Leave both Impact Summaries blank.

## Rules

- The matrix **informs** the recommendation; it does not write it. The student writes the
  Recommendations and Analysis sections of the memo.
- Never rate an alternative without a reason, and never change a rating to produce a preferred winner.
- No predictions and no "I believe"; ratings rest on the case and the exhibits.
