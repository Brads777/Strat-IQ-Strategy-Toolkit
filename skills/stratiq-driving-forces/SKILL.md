---
name: stratiq-driving-forces
description: "Strat-IQ driving-forces synthesis. Pulls candidate changes from every source in the ledger — PESTEL findings, competitors' 10-K risk factors and MD&A trends, news and hiring/patent signals, industry reports, and the Five Forces structure — then filters to the 3-5 forces actually altering industry economics. Each driver gets a transmission mechanism, P&L line, profit-pool call (expanding, compressing, redistributing) and the forces it moves, and the Five Forces are re-scored at the horizon. Use for driving forces, industry change drivers, key trends reshaping an industry, or how trends change Five Forces."
license: CC-BY-NC-4.0 AND PolyForm-Noncommercial-1.0.0
---
# ©2026 Brad Scheller

# Trending Influence Factors (Strat-IQ S3)

**Runs:** after Five Forces. **Reads:** the whole industry layer — `evidence[]`, `ci.pestel_seeds[]`,
`competitors[].signals`, `industry_layer.pestel[]`, `industry_layer.forces[]`. **Writes:**
`industry_layer.drivers[]`, and adds `score_horizon` and `moved_by` to each force plus
`attractiveness.horizon`. **Feeds:** KSFs and the vector shortlist.

A driving force is a **major underlying cause of change** in the industry's structure and economics
over the horizon. PESTEL lists what is happening in the world; Five Forces describes the structure
today; driving forces are the few changes that will **move the forces**. Most findings are not
drivers.

## Step 1 — Gather candidates from every source

Drivers do not come only from PESTEL. Collect candidates from all of these, keeping each one's
evidence ids:

| Source in the ledger | What it contributes |
|---|---|
| PESTEL findings | Macro shifts with velocity and P&L line |
| 10-K risk factors (CI seeds), especially `shared: true` | Threats management disclosed under legal liability |
| MD&A trend statements (CI seeds) | What management says actually moved price, volume, mix and cost |
| Competitor signals (hiring, patents, launches, M&A, pricing) | Where the industry's leaders are placing bets |
| News and industry reports | Recent events and market data |
| Five Forces | Which structural pressure a change would intensify or relieve |

Check the candidates against the common categories of industry drivers, so none is missed:

1. Changes in the long-term growth rate
2. Changes in who buys and how they use the product
3. Product and marketing innovation
4. Technological change and manufacturing process innovation
5. Entry or exit of major firms, and consolidation
6. Diffusion of technical know-how (across firms and countries)
7. Changes in cost and efficiency
8. Buyer preference shifts (e.g. toward standardised or toward differentiated offers)
9. Regulatory influence and government policy
10. Changing societal concerns, attitudes and lifestyles
11. Reductions in uncertainty and business risk

## Step 2 — Filter to the 3-5 that matter

Promote a candidate to a driver only if it passes all four tests:

1. **Moves structure** — it changes at least one force's score by at least one point over the horizon.
2. **Material to the P&L** — it moves an identifiable P&L line for most firms in the industry, not one
   firm. (One firm's problem is company-level; leave it to the KSF scorecard.)
3. **Inside the horizon** — it will play out within the scope's time horizon.
4. **Corroborated** — it rests on at least two **different source types** (for example a shared 10-K
   risk factor plus a news trend, or a PESTEL finding plus a pattern in competitor hiring). One source
   alone gets a `[single-source]` flag.

Typical yield is 3-5 drivers. If you are promoting more than ~40% of the candidates, the filter has
probably not run — warn, and say why if this really is a structural break.

## Step 3 — Write each driver

For each driver:

- **Name** — a short phrase for the change, not the category ("Autonomy software replaces trained
  pilots", not "Technology").
- **Sources** — the finding and evidence ids it rests on, across source types.
- **Transmission mechanism** — one sentence: *change → effect on buyers, suppliers, rivals or costs →
  P&L line and direction.*
- **Profit pool** — `expanding`, `compressing` or `redistributing` (value shifting between players or
  along the value chain; say from whom to whom).
- **Forces moved** — which forces, in which direction.
- **Timing and velocity** — when it bites, and whether it is slow, accelerating or exponential.

## Step 4 — Re-score the forces at the horizon

For each force, set `score_horizon` (1-5) after the drivers act, and list the driver ids in
`moved_by`. Recompute attractiveness for the horizon with the same method the Five Forces stage used
(the API, or the public roll-up `6 − mean(scores)`). The gap between now and the horizon is the
headline: is this industry getting more or less attractive, and why?

## Output

```markdown
## Driving forces — [industry], [horizon]

| ID | Driver | Sources (types) | Transmission | P&L line | Profit pool | Forces moved | Velocity |
|---|---|---|---|---|---|---|---|
| D1 | … | P4, E021 (10-K), E033 (news) | … | cogs.labor | redistributing → software vendors | substitutes ↑, buyers ↑ | accelerating |

### Five Forces: now → horizon
| Force | Now | Horizon | Moved by |
|---|---|---|---|

**Attractiveness:** now 2.4 → horizon 2.0 (method: …)
**What this means:** [2-3 sentences — where the industry is heading and who it favours]
**Filter check:** [n] candidates → [k] drivers ([k/n]%) · single-source flags: […]
```

Write the ledger, then return to the orchestrator for the checkpoint.

## Pitfalls

- **Renaming PESTEL** — a list of all the PESTEL findings with a new heading. Drivers are the filtered few.
- **Categories as drivers** — "technology" or "regulation" is a category, not a driver.
- **No mechanism** — a driver that does not say which P&L line it moves is a trend, not a driver.
- **Company problems promoted to industry drivers** — one firm's recall is not an industry force.
- **Forces never re-scored** — drivers that do not change a force score have not been connected to the
  structure.
