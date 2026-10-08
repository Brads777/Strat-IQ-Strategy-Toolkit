---
name: stratiq-segment-value
description: "Strat-IQ Customer Segment Lifetime Value (case-memo CLV exhibit). Values market segments, not single customers: CLV per customer from purchase value, frequency, lifespan and margin (net of acquisition and retention cost when the student's case facts give them), multiplied by the estimated customers in each segment, so strategic alternatives can be compared on total segment value. Computed with a script. Include only when the student's case facts supply the data. Use for 'CLV', 'customer lifetime value', 'segment value', 'which segment is worth more', or the CLV exhibit."
license: CC-BY-NC-4.0 AND PolyForm-Noncommercial-1.0.0
---
# ©2026 Brad Scheller

# Customer Segment Lifetime Value (Strat-IQ · CLV exhibit)

**Reads:** the customer and segment data the student gathered (persona interview notes); segment sizes from the Industry Overview (Exhibit C)
where the notes lack them. **Writes:** `case.segment_value[]` and the CLV exhibit.

**Include this exhibit only if it is relevant to the case and the student's interview notes provide the data.** Otherwise
leave it out. Never fill it with invented numbers.

## The core idea

Businesses do not decide between one customer and another; they decide between **segments**. So the
value of an alternative is the value of the whole segment it targets:

> **Total Segment Value = CLV per Customer × Estimated Customers in the Segment**

## Step 1 — CLV per customer

For each segment:

| Input | From |
|---|---|
| Average purchase value | Case |
| Purchase frequency (per year) | Case |
| Expected relationship duration (years) | Case |
| Profit margin per customer | Case or Exhibit C economics |
| Customer acquisition cost | Case, if given |
| Retention cost / cost to serve (per year) | Case, if given |

> Gross CLV = average purchase value × purchase frequency × years × margin
> Net CLV = Gross CLV − acquisition cost − (retention cost × years)   *(when those costs are given)*

Use **net CLV** when the notes give acquisition and retention costs, and say which one is used. If a
segment's net CLV is negative, it destroys value at any size, so flag it.

## Step 2 — Estimated customers

Estimated customers = **total addressable customers × expected market share**. Use the figures from the student's notes;
where it gives none, use Exhibit C's market size and state the assumption. Note the qualitative factors
the template asks for — **growth potential, penetration rate, competition intensity** (Exhibit E) — in
one line per segment, because they decide how believable the share assumption is.

## Step 3 — Compute

Fill `templates/segment-value.csv` and, where code execution is available, run:

```
python scripts/segment_value.py segment-value.csv
```

It computes gross and net CLV, estimated customers and total segment value, ranks the segments, and
shows how total value moves if the share assumption is ±25%. Without code execution, do it by hand and
show the arithmetic.

## Output (template format)

```markdown
### O. Customer Segment Lifetime Value Analysis

| Segment | CLV/Customer | Est. Customers | Total Value |
|---|---|---|---|
| [Segment A] | $[value] ([formula]) | [number] | $[total] |
| [Segment B] | $[value] | [number] | $[total] |

Inputs and assumptions: [one line per segment — source of each input, net or gross CLV, share assumption]
Share sensitivity (±25%): [range per segment]

**Impact Summary — CLV Analysis**
> _[Student writes this summary.]_
```

Leave the Impact Summary blank.

## Rules

- Every input comes from the student's interview notes or a cited exhibit; label any assumption `[Assumption]`.
- Use the same years, margin basis and currency for every segment so the totals compare.
- This exhibit compares segments. It does not pick the recommendation; the decision matrix and the
  student's memo do that.
