---
name: stratos-expected-value
description: "StratOS Expected Value (optional case-memo Exhibit Q-2), following the course handout 'Choosing Among Strategic Alternatives'. For each option plus do nothing: strong, moderate and weak outcomes, probabilities summing to 100%, the NPV of each, expected NPV, and then the checks the average hides: worst case and maximin, the probability at which the ranking flips, and the value of perfect information (EVPI) that prices a pilot. Run by expected_value.py. Use for 'expected value', 'decision tree', 'which is the better bet', 'how risky is this choice', 'EVPI', or 'Exhibit Q-2'."
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
