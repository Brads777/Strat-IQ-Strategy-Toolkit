---
name: stratiq-ksf
description: "Strat-IQ KSFs (key success factors), in two tiers. Tier 1 derives 6-10 industry KSFs from Porter's Five Forces, Trending Influence Factors, PESTEL and competitor intel, weights them, and scores every competitor on the same yardstick in a weighted competitive strength assessment with sensitivity testing. Tier 2 re-weights those KSFs for each company's strategy and strategic group and adds its firm-specific critical success factors. Use for KSFs, key success factors, critical success factors, CSFs, competitive strength assessment, competitor scorecard, or 'what does it take to win'."
license: CC-BY-NC-4.0 AND PolyForm-Noncommercial-1.0.0
---
# ©2026 Brad Scheller

# KSFs — Key success factors and the competitor scorecard

**Runs:** after driving forces. **Reads:** `industry_layer.forces[]` (now and horizon),
`industry_layer.drivers[]`, `competitors[]` (financials, signals, moats). **Writes:**
`industry_layer.ksf[]` and `competitors[].ksf_scores`. **Feeds:** the strategic-mapping skill, which
chooses its map axes from these KSFs.

A key success factor is what **any** firm must do well to survive and prosper in this industry's
changed structure. It is industry-level. Each competitor is then scored on how well it delivers them.

## Step 1 — Derive the industry KSFs

Build 6-10 KSFs by asking of each strong force and each driver: *what capability, resource or
position lets a firm win against this?*

| From | Ask | Example (illustrative) |
|---|---|---|
| Strong buyer power | What keeps buyers from switching or squeezing price? | Integrated software lock-in |
| Strong supplier power | What protects input cost and supply? | Secured component supply or in-house key parts |
| High rivalry on price | What wins a price fight? | Lowest unit cost at scale |
| Threat of substitutes | What keeps the job being done this way? | Capability the substitute cannot match |
| Each driver | What must a firm have when this change has played out? | Autonomy that non-specialists can operate |

Also pull the **candidate KSFs** the competitor-intel pass listed (what leaders have that laggards
lack), and ask of each strong PESTEL finding which capability it rewards.

Keep a candidate only if it passes the **three tests** in `references/ksf-criteria.md`:
**differentiating** (leaders and laggards visibly differ — if everyone scores 7-8 it is table stakes;
note it as a threshold requirement instead), **measurable** (at least one observable indicator), and
**controllable** (a firm can build it by its own decisions — "a favourable regulatory climate" is a
PESTEL factor, not a KSF). Merge overlaps.

Rules:

- **Every KSF traces to at least one force or driver** (`from_forces`, `from_drivers`). No
  free-floating "innovation", "agility" or "customer focus".
- Phrase each as a capability ("Scale procurement cost advantage"), not an outcome ("High margins").
- Cover cost, differentiation and access (channels, licences, supply), not only product features.
- Give each a **status**: `current`, `emerging` (rising in weight because of a driver) or `fading`.
  Emerging KSFs are where positions will shift.

## Step 2 — Convert each KSF to a KPI

For each KSF, give an operational KPI that can be checked, a benchmark or target, and why it matters:

| KSF | Operational KPI | Benchmark / target | Strategic purpose | Traces to |
|---|---|---|---|---|
| … | … | … | Protects margin during price wars | Rivalry, D1 |

## Step 3 — Weight the KSFs

Assign weights summing to 1.00 that reflect how much each KSF decides profitability in this industry
at the horizon.

- If Strat-IQ decision-criteria weights are available from the scoring API or a completed market
  research stage, use them and record `weights: "api"`.
- Otherwise assign analyst weights, each justified by the force or driver it ties to, and stamp
  `weights: "analyst"`. Weight emerging KSFs up. **No single weight above 0.25.**

## Step 4 — Score every competitor (weighted competitive strength)

For each KSF, name 1-3 indicators (financial metrics from the CI benchmark table wherever possible)
and use the **anchor scale** in `references/ksf-criteria.md` the same way for every firm: 9-10 clear
leader (top quartile, hard to copy) · 6-8 above median · 4-5 around the median · 2-3 bottom quartile ·
1 a weakness visibly costing share or margin. Score **relative to the peer set**, not an ideal.

Rate each competitor 1-10 on each KSF. **Every rating cites evidence** — a CI metric, a signal, a moat
rating. Do not let one financial metric count toward more than one KSF. Missing evidence:

- up to 1 KSF → score `n/a`; that firm's weights are rescaled over the KSFs it has, and it is flagged
- more than 1 KSF → list the firm as "insufficient evidence" and leave it out of the ranking
- private firms may be scored on proxies (pricing, headcount, reviews, funding) at confidence Low

Then:

> weighted score = Σ (KSF weight × rating)   → a 1-10 overall strength per competitor

**Compute it deterministically.** Fill `templates/ksf-scores.csv` (columns `ksf, weight, status`, then
one column per competitor) and, where code execution is available, run
`python scripts/score_ksf.py ksf-scores.csv`. It checks that weights sum to 1.00, ranks the firms,
reports gaps to the leader, flags ties, runs a ±20% weight-sensitivity test, lists white space, and
suggests map axes. Without code execution, do the same steps by hand and say so.

- **Ties:** a difference under 0.3 between two totals is a tie, not a ranking.
- **Sensitivity:** report any rank change when one KSF weight moves ±20%. A ranking that flips under
  small weight changes is not a finding.

Show the table with the base company highlighted:

| KSF (weight) | Firm A | Firm B | Firm C | … |
|---|---|---|---|---|
| K1 … (0.25) | 8 · E012 | 5 · E020 | 3 · [unverified] | |
| **Weighted strength** | **7.1** | **5.4** | **4.2** | |

Where a firm has no audited financials, score from signals and say so; a missing-data rating counts
as lower confidence, not as a low score.

## Step 5 — Name each competitor's own success factors

From the scorecard, for each competitor state in 2-3 lines:

- **Where it wins** — the KSFs where it leads the set, and the evidence.
- **Where it is exposed** — the KSFs where it trails, especially horizon-rising ones.
- **Net competitive position** — strongest, contender, or at risk, and against whom.

For the base company, add the **gap to close**: the one or two KSFs whose improvement would move its
weighted strength the most.

## Step 6 — Tier 2: the company view (per firm)

Tier 1 (Steps 1-5) is one yardstick for the whole industry. Tier 2 recognises that **what matters
most depends on where a firm competes**. A cost leader and a premium differentiator face the same
forces but win on different factors. Run Tier 2 for the base company, and for any competitor the user
asks about.

1. **Strategy and group.** From CI's positioning evidence, name the firm's generic strategy (cost
   leadership, broad differentiation, focused cost, focused differentiation, or best-cost) and its
   strategic group. Cite the evidence. The mapping skill later confirms this, or flags a mismatch —
   "claims premium, plots with the budget cluster" is itself a finding.
2. **Re-weight the same KSFs** for that strategy. The list does not change; only the weights do. They
   still sum to 1.00 and stay under 0.25, and every weight that moves more than 0.05 from Tier 1 gets a
   one-line reason tied to the strategy.
3. **Add 1-3 firm-specific critical success factors** — what this firm must execute for *its* chosen
   strategy to work (e.g. for a cost leader, "keep unit cost below the premium group's at half the
   volume"). Each one traces to a Tier 1 KSF or to the firm's position, and has a KPI.
4. **Report both totals.** Show the firm's industry-weighted strength (Tier 1, comparable across
   firms) beside its strategy-weighted strength (Tier 2, not comparable across firms). A big gap
   between them tells you the firm is strong at what its strategy needs but weak on what the industry
   rewards, or the other way round.

The scores themselves never change between tiers; only the weights and the added CSFs do. On a
base-company swap, rerun Tier 2 only.

Write Tier 2 to `company_layer.ksf_view`.

## Industry-wide findings

- **KSF white space** — any KSF where no competitor scores above 6. Nobody has won it yet.
- **Axis hand-off** — the pair of heavily weighted KSFs whose competitor scores are *least correlated*
  (the script prints it). Pass it to the mapping skill as the KSF-side axis candidate; the mapping skill
  checks it against the vector shortlist before plotting.

## Output

```markdown
## Key success factors — [industry], [horizon]

| ID | KSF | Traces to | KPI | Benchmark | Weight | Rising? |
|---|---|---|---|---|---|---|

## Competitive strength scorecard (weights: analyst | api)
[table from Step 4]

### [Firm] — wins on …; exposed on …; position: …
### Base company — gap to close: …
```

Write the ledger, then return to the orchestrator for the checkpoint.

## Pitfalls

- **Virtues instead of factors** — "quality" or "innovation" with no KPI.
- **KSFs that trace to nothing** — if it is not tied to a force or driver, it is an opinion.
- **Scores without evidence** — a 9 for "brand" needs a reason someone else could check.
- **Equal weights** — they erase the analysis; the point is that some factors matter more.
- **Confusing the firm's strengths with industry KSFs** — the KSFs are the same for everyone; only the
  scores differ.
