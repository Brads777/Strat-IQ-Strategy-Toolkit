---
name: stratos-expected-value
description: "StratOS Expected Value (optional case-memo Exhibit Q-2), following the course handout 'Choosing Among Strategic Alternatives'. For each option plus do nothing: strong, moderate and weak outcomes, probabilities summing to 100%, the NPV of each, expected NPV, and then the checks the average hides: worst case and maximin, the probability at which the ranking flips, and the value of perfect information (EVPI) that prices a pilot. Run by expected_value.py. Adds a Bayesian pilot update (bayes_update.py): posterior probabilities after a pilot signal and EVSI, the value of an imperfect test. Use for 'expected value', 'decision tree', 'which is the better bet', 'EVPI', 'is a pilot worth it', 'Bayes', 'update my probabilities', or 'Exhibit Q-2'."
license: Apache-2.0
---
# ©2026 Brad Scheller

# Expected Value (StratOS · Part 3 · Choose · Exhibit Q-2)

**Runs:** after Business Case. **Reads:** `strategy_layer.options`, `business_case[]`,
`industry_layer.drivers[]` (for the scenarios). **Writes:** `strategy_layer.expected_value`.
**Feeds:** Strategic Options (staging), Stress Test, Pitch.

Every strategic choice is a bet on an uncertain future. This follows the five steps in the course
handout, then adds the three checks that keep an average from hiding the risk.

## The five steps (the handout)

1. **Alternatives** — the confirmed options, always with **do nothing** as the baseline.
2. **Outcomes** — three scenarios, usually **strong, moderate and weak** demand. Build them from the
   trending influence factors, so each scenario is a story the evidence supports.
3. **Probabilities** — within each option they sum to 100%. Base them on evidence (PESTEL, Five
   Forces, market data, history); say what each rests on. In a case, the student sets them.
4. **NPV of each outcome** — from the Business Case run at that scenario's volume and price.
5. **Multiply and add** — expected NPV per option.

Fill `templates/expected-value.csv` and run `scripts/expected_value.py`.

## The checks the average hides

| Check | What it shows | Script output |
|---|---|---|
| **Risk** | Each option's worst and best case; the **maximin** choice (best worst case) | `worst`, `best`, `maximin` |
| **Fragility** | Holding the strong-case probability fixed, the weak-case probability at which the leader loses first place | `flip_points` |
| **Value of information** | EVPI: expected value with perfect foresight minus the best expected value. The most worth paying to learn which scenario is real (a pilot, a market test) | `evpi` |

Say each in a sentence. Handout example: *"A wins on average, $4.4M against $4.0M, but can lose $6M;
B never loses. If the chance of weak demand rises from 20% to 25.7%, B wins. Information is worth
up to $1.4M: a pilot that reveals demand first is worth up to that much."*

## Is a pilot worth it? (Bayesian update)

EVPI prices a *perfect* test. Real pilots are imperfect, so price the one the student could run:

1. In `templates/pilot.csv`, one row per scenario and one column per pilot result (e.g. positive,
   negative): how likely the pilot shows that result **if** that scenario is real. A good pilot shows
   "positive" often under strong demand and rarely under weak. The student sets these from a test
   market, a comparable launch or an expert view.
2. Run `scripts/bayes_update.py expected-value.csv pilot.csv --cost <pilot cost>`. It applies Bayes'
   rule to give the **posterior** probabilities after each result, the best option after each result,
   the expected value with the pilot, **EVSI** (the expected value of the sample information) and the
   net value after the pilot's cost. With `--observed <result>` it updates on the result the student
   actually saw.
3. Say it in a sentence. Template example: *"A pilot that is right about 80% of the time is worth
   $0.83M, 59% of perfect information. It matters because a negative result would switch the choice
   from A to B. At a cost of $0.5M it is worth running."* A pilot no result of which changes the
   choice is worth nothing for this decision, however interesting.

This block goes in Exhibit Q-3 (Risk Analysis) with Business Case's tornado and simulation.

## Output

```markdown
### Q-2. Expected Value
| Option | Strong (p × NPV) | Moderate | Weak | Expected NPV | Worst case |
|---|---|---|---|---|---|
**Risk:** … **Fragility:** … **Value of information:** …
**Impact Summary — Expected Value**
> _[Student writes this summary.]_
```

Draw the decision tree as a chart when file creation is available.

## Rules

- Probabilities must sum to 100% per option; the script rejects them otherwise.
- Expected value does not remove judgment; it makes it visible. Never call the top expected value
  "the answer".
- A large EVPI is a reason to stage the bet (Strategic Options Step 3), not to delay forever.
