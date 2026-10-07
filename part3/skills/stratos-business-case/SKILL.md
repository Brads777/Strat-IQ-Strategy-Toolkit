---
name: stratos-business-case
description: "StratOS Business Case (optional case-memo Exhibit Q-1). Puts money on each strategic option: revenue built from drivers (units × price), costs split into variable and fixed, full investment including working capital, then NPV, IRR, payback and a sensitivity grid from business_case.py, with the break-even stated in one plain sentence. Inputs come from the ledger and the user; in a case, every input is confirmed by the student. Adds Exhibit Q-3 Risk Analysis on request: a tornado chart and a Monte Carlo simulation over the student's own ranges (risk_analysis.py). Use for 'business case', 'NPV', 'IRR', 'payback', 'is this option worth it', 'tornado', 'Monte Carlo', 'risk analysis', or 'Exhibit Q-1' or 'Q-3'."
license: Apache-2.0
---
# ©2026 Brad Scheller

# Business Case (StratOS · Part 3 · Choose · Exhibit Q-1)

**Runs:** after Strategic Options (and the Decision Matrix when there is one). **Reads:**
`strategy_layer.options`, `company_layer.internal.unit_economics`, `competitors[].financials`.
**Writes:** `strategy_layer.business_case[]`. **Feeds:** Expected Value, Go-to-Market, Pitch, Value
Realization (the plan actuals are compared with).

## Step 1 — Build the drivers, per option

| Block | Inputs | Rule |
|---|---|---|
| Revenue | Units per year × price, by year | From Unit Economics and the option's volume logic; never a top-down "share of market" alone |
| Variable cost | Cost per unit (and its learning curve, if any) | From Unit Economics |
| Fixed cost | Per year | Opex the option adds |
| Investment | Capex by year **plus working capital** (a % of revenue change) | Capex alone understates the cash need |
| Horizon and rate | Years (default 5-7), discount rate (the firm's WACC or the course's hurdle), tax rate | Stated and cited |
| Terminal value | Optional growth rate after the horizon | Off by default; shown separately when used |

Fill `templates/business-case.csv` and run `scripts/business_case.py`. It returns NPV, IRR, payback,
the cash flows, the **break-even change** in revenue (and in cost) that sets NPV to zero, and a
sensitivity grid over revenue and cost.

## Step 2 — State the break-even in words

The single most useful sentence in the exhibit: *"The case holds only if revenue beats plan by 1%,"*
or *"NPV stays positive unless volume falls more than 18% below plan."* Then ask the next question:
would a terminal value, a staged start or a lower-capex route change that?

## Step 3 — Compare the options

One row per option (including do nothing), with NPV, IRR, payback and break-even margin. Do not
declare a winner; Expected Value adds the uncertainty, and the choice is the user's.

## Step 4 (optional) — Risk Analysis (Exhibit Q-3)

When the student asks how risky the case is, or the memo needs Exhibit Q-3:

1. **The student sets a range for each driver** in `templates/risk-ranges.csv`: low, likely and high
   for price, units, variable cost, fixed cost and capex (as % change from plan) and the discount rate.
   Claude may suggest ranges marked `SUGGESTED`, each tied to evidence (a competitor's price cut, a
   PESTEL factor, a cost trend); the student confirms them.
2. Run `scripts/risk_analysis.py business-case.csv risk-ranges.csv`. It returns:
   - **Tornado**: NPV with each driver at its low and its high, the others at plan, sorted by swing.
     The top bar is the assumption to test first (and the one the Stress Test attacks).
   - **Monte Carlo** (10,000 draws, triangular distributions, fixed seed so results repeat): mean,
     median, P10-P90 range, standard deviation, the **probability NPV is below zero**, and a histogram.
3. State it in two sentences: which driver matters most, and how often the case loses money. Say the
   limit too: drivers are drawn independently, so if price and volume move together the real spread
   differs.

```markdown
### Q-3. Risk Analysis
| Driver | Range (low / likely / high) | NPV at low | NPV at high | Swing |
|---|---|---|---|---|
**Tornado chart:** [bars sorted by swing]
**Simulation:** median NPV …, 80% of outcomes between … and …, P(NPV < 0) = …%
**Value of a pilot:** [from Expected Value's bayes_update.py, when used]
**Impact Summary — Risk Analysis**
> _[Student writes this summary.]_
```

The workbook's Risk Analysis sheet holds the same tornado and an Excel simulation the student can
re-run (F9).

## Output

```markdown
### Q-1. Business Case
| Option | NPV | IRR | Payback (yrs) | Break-even revenue change | Key assumption |
|---|---|---|---|---|---|
**Sensitivity:** [grid or chart]
**In words:** [the break-even sentence]
**Impact Summary — Business Case**
> _[Student writes this summary.]_
```

## Rules

- In a graded case, the student confirms every input; Claude may propose ranges marked `SUGGESTED`.
- Every input cites its source or is marked `[assumption]`; assumptions are listed for the Stress Test.
- Ranges, like inputs, are the student's; a skewed range (more downside than upside) is a finding, not an error.
- Use the script for all arithmetic. Round to the precision the inputs support.
