---
name: stratiq-five-forces
description: "Strat-IQ Porter's Five Forces margin engine. Scores rivalry, entry threat, supplier power, buyer power and substitutes 1-5 on cited evidence (including competitor filings), notes complementors, diagnoses whether margin pressure is price- or cost-driven, rolls up industry attractiveness, and closes with where the profit pool is going. Scores each force now; the driving-forces stage re-scores it at the horizon. Use for Five Forces, Porter, industry structure, industry attractiveness, competitive forces, or profit pool."
license: CC-BY-NC-4.0 AND PolyForm-Noncommercial-1.0.0
---
# ©2026 Brad Scheller

# Porter's Five Forces (Strat-IQ S2)

**Runs:** after PESTEL. **Reads:** the scope, `competitors[]` and `evidence[]` from CI, and
`industry_layer.pestel[]`. **Writes:** `industry_layer.forces[]` (with `score_now`), `complementors`,
`attractiveness.now`, `profit_pool`. **Feeds:** driving forces (which re-score each force at the
horizon) and KSFs (every KSF traces to a force or driver).

Five Forces reads what the industry structure does to **everyone** who plays. It is not a list of who
plays — that is the competitor set.

## Step 1 — Confirm the industry boundary

Use the ledger's boundary. Check it from the demand side (what need does this satisfy?) on three
edges: product scope, geography, and customer type (B2B vs B2C; premium vs mass). A boundary drawn
too narrowly hides the substitutes that matter most.

## Step 2 — Score each force 1-5 on evidence

1 = very weak force (fat margins available) … 5 = very strong force (margins competed away).
**Every score cites at least one evidence id.** "It feels crowded" is not evidence. Competitor
filings are strong evidence here: gross-margin trends show who is winning the price and cost fights,
and risk factors name the customers, suppliers and substitutes management worries about.

### Rivalry among existing competitors
Stronger when: many similar-sized rivals; slow growth (zero-sum share fights); low differentiation;
high fixed or storage costs (pressure to fill capacity); high exit barriers; price is the main
weapon; rivals have diverse goals or emotional commitments. Weaker when: a clear leader, high growth,
real differentiation, compatible rival goals.
*Evidence to seek:* concentration (CR4/CR5, HHI), price-war history, margin trends across the CI
table, capacity utilisation, promotion intensity.

### Threat of new entrants
Stronger when: low capital needs; weak scale economies; open distribution; weak brands and switching
costs; permissive regulation; a technology that lets outsiders leapfrog. Weaker when: scale or
learning-curve cost advantages, network effects, licences and certification, control of scarce inputs
or channels, credible incumbent retaliation.
*Quantify barriers:* minimum efficient scale, leading firms' capex and R&D, licence count and approval
time, retention and contract lengths, channel exclusivity.

### Bargaining power of suppliers
Stronger when: few or concentrated suppliers; unique or critical inputs; high switching costs; the
supplier can integrate forward; the industry is a small customer to them. Weaker when: commodity
inputs, many suppliers, credible backward integration by the industry.
*P&L line:* usually `cogs.inputs` or `cogs.labor`.

### Bargaining power of buyers
Stronger when: concentrated or large-volume buyers; undifferentiated product; low switching costs;
price-sensitive buyers with full information; credible backward integration. Weaker when: fragmented
buyers, lock-in, strong brand, high cost of failure. **Distinguish the decision-maker from the user**
in B2B, and treat powerful channels (retailers, distributors, platforms, government procurement) as
buyers.
*P&L line:* usually `revenue.price`.

### Threat of substitutes
Stronger when: a different way of doing the same job has improving price-performance and low
switching cost. Always name **"do nothing"**, **in-house build**, and — in most knowledge and service
industries — an **AI-driven workflow** as candidate substitutes, then say how strong each is.
*P&L line:* usually `revenue.volume`.

### Complementors (not a sixth force)
Following Porter's 2008 update: complements are not a separate force, but they raise or lower the
five. Note who they are and which force they move (e.g. a software ecosystem raises switching costs
and so weakens buyer power).

## Step 3 — Diagnose where margin pressure comes from

Say whether the dominant pressure on margin is **price** (buyer power, rivalry, substitutes →
`revenue.price`) or **cost** (supplier power, input inflation → `cogs.*`), or both. This decides which
KSFs matter later.

## Step 4 — Attractiveness and the profit-pool close

**Attractiveness (1.0-5.0, 5 = most attractive).** If the Strat-IQ scoring API is connected, send the
force scores and record its weighted result with `method: "api"`. Otherwise use the unweighted public
roll-up and stamp it:

> attractiveness = 6 − mean(force scores)   → `method: "public-screen"`

**Profit pool — the "so what".** Five rated forces with no answer to *where does the margin go?* is an
incomplete analysis. Close with 2-4 sentences: who captures value today (suppliers, buyers, a leader,
nobody), where it is migrating, and which positions can still earn above-average returns (for
example, only cost leadership or a brand premium survive and the middle is squeezed).

## Output

```markdown
## Five Forces — [industry], [geography]

| Force | Score now | Key drivers of the score | P&L line | Evidence |
|---|---|---|---|---|
| Rivalry | 4 | … | revenue.price | E004, E009 |
| New entrants | 2 | … | revenue.volume | E011 |
| Suppliers | 4 | … | cogs.inputs | E001 |
| Buyers | 3 | … | revenue.price | E007 |
| Substitutes | 2 | … (incl. AI workflow) | revenue.volume | E012 |

**Complementors:** …
**Margin pressure:** price / cost / both — …
**Attractiveness now:** 2.4 (method: public-screen) — the driving-forces stage adds the horizon score
**Profit pool:** …
**Assumptions to validate:** 1… 2… 3…
```

Write the ledger, then return to the orchestrator for the checkpoint.

## Pitfalls

- **Ratings as vibes** — a score with no evidence id fails the chain check.
- **Confusing competitors with structure** — naming rivals instead of reading forces.
- **Skipping the AI substitute** — assessing only adjacent products while a workflow replaces the job.
- **Equal weighting** — call out the 2-3 forces that actually decide profitability.
- **Forcing structure on a nascent category** — when forces have not formed, say so and report them
  as "forming" rather than inventing precise scores.
