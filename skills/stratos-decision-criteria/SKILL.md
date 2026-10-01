---
name: stratos-decision-criteria
description: "StratOS Decision Criteria and Weights (case-memo Exhibit L). Turns the student's Key Issues — the central problem, management questions and required goals — into the specific criteria management will use to judge the recommendations, each tied to a stated goal, weighted 1-5 with a rationale. Rejects generic criteria that do not serve this decision. Use for 'decision criteria', 'criteria and weights', 'Exhibit L', or 'how will management evaluate the options'."
license: Apache-2.0
---
# ©2026 Brad Scheller

# Decision Criteria and Weights (StratOS · Exhibit L)

**Reads:** the student's **Exhibit B — Key Issues** (central problem, management questions, required
goals), and where available the industry analysis (KSFs, trending influence factors, Five Forces).
**Writes:** `case.criteria[]` and Exhibit L. **Feeds:** the Decision Matrix (Exhibit M), which
multiplies these weights by each alternative's ratings.

Decision criteria are **indicators of achieving the required goals**. They state how management will
judge the recommendations. If they are wrong, management sends the analysis back.

## Step 1 — Get the goals

Criteria can only be derived from the case's own goals. Read the student's Exhibit B. If it is missing
or has no required goals, **stop and ask the student to write Exhibit B first**. Do not invent the
goals; framing the problem is the student's work.

## Step 2 — Derive the criteria

For each required goal, ask: *what observable result would show this goal was achieved?* That result
is a criterion. Typically 4-6 criteria in total.

- **Every criterion traces to at least one required goal.** Record which one.
- **Measurable or clearly judgeable** — "12-month payback", "protects the premium brand position",
  "executable with current cash".
- **Specific to this decision.** Reject generic criteria that could apply to any case — "quality",
  "innovation", "customer satisfaction" — unless a stated goal demands them. Generic criteria add
  non-relevant input and can tilt the decision.
- **Use the industry analysis where it sharpens a criterion.** A KSF or driving force can show *why* a
  goal matters now (e.g. a battery-cost KSF makes "cost per kWh" the right measure of a cost goal).
  Cite the exhibit (C-G) it came from.
- **No duplicates.** Two criteria that measure the same thing double-count it; merge them.

## Step 3 — Weight each criterion 1-5

5 = decisive, 1 = minor. Base each weight on the goals as the case states them: explicit priorities,
constraints ("must", "cannot exceed") and emphasis from management. Give every weight a one-line
rationale that points to the case. Weights need not differ, but if every criterion is a 5, nothing
was prioritised; say which goal dominates.

## Output — Exhibit L (template format)

```markdown
### L. Decision Criteria and Weights

| Criterion | Weight (1-5) | Rationale |
|---|---|---|
| [Criterion 1] | [w] | [Which required goal it measures, and why this weight — cite the case or Exhibit C-G] |
| [Criterion 2] | [w] | … |

**Impact Summary — Decision Criteria and Weights**
> _[Student writes this summary.]_
```

Leave the Impact Summary blank: the student writes it to show understanding.

## Rules

- Do not write or suggest the recommendations. Criteria describe how options will be judged, not which
  option wins.
- Do not refer to "I" or "we", and state nothing as a belief — criteria rest on the case's stated goals.
- If a goal cannot be turned into any measurable criterion, say so and ask the student to sharpen the
  goal.
