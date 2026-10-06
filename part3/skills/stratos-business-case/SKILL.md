---
name: stratos-business-case
description: "StratOS Business Case (optional case-memo Exhibit Q-1). Puts money on each strategic option: revenue built from drivers (units × price), costs split into variable and fixed, full investment including working capital, then NPV, IRR, payback and a sensitivity grid from business_case.py, with the break-even stated in one plain sentence. Inputs come from the ledger and the user; in a case, every input is confirmed by the student. Use for 'business case', 'NPV', 'IRR', 'payback', 'is this option worth it', 'financial case for', or 'Exhibit Q-1'."
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
- Use the script for all arithmetic. Round to the precision the inputs support.
