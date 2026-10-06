---
name: stratos-full-potential
description: "StratOS Full Potential (supplementary case-memo Exhibit K-1). Sizes the gap between the base company's current performance and what it could earn if each value driver reached a credible benchmark (peer median, best-in-class peer, or its own best year), driver by driver: price, mix, volume, variable cost, fixed cost, capital. Produces a bridge from today's operating profit to full potential, ranked by size and by how controllable each gap is. Use for 'full potential', 'performance gap', 'how much better could it be', 'profit bridge', 'value at stake', or 'Exhibit K-1'."
license: Apache-2.0
---
# ©2026 Brad Scheller

# Full Potential (StratOS · Part 2 · Exhibit K-1)

**Runs:** after Unit Economics and VRIO. **Reads:** `company_layer.internal.unit_economics`,
`competitors[].financials`, `industry_layer.ksf[]`, `company_layer.internal.vrio`. **Writes:**
`company_layer.internal.full_potential`. **Feeds:** Growth Barriers, SWOT (weaknesses), Initiative
Prioritizer and Value Realization.

Full potential answers one question: **how much is the gap worth, and where is it?** It stops a
strategy chasing a small gap loudly while a large one sits unnoticed.

## Step 1 — Choose the benchmark for each driver

| Benchmark | Use when |
|---|---|
| **Peer median** | Default. Credible and hard to argue with |
| **Best-in-class peer** | The firm's strategy claims leadership on that driver |
| **Own best year** | Peers are not comparable (different model, different unit) |

State the benchmark and its source for every driver. Never use a benchmark from outside the competitor
set without saying why.

## Step 2 — Size each gap

Drivers, from the unit economics: price (ASP), mix, volume, variable cost per unit, fixed cost
(R&D, SG&A, overhead) as % of revenue, and capital intensity (capex and working capital as % of
revenue). For each, value the gap in operating profit **holding the other drivers at today's level**.

Run `scripts/full_potential.py` on `templates/full-potential.csv`. It values each gap, removes
overlaps by applying the drivers in sequence (price → mix → volume → variable cost → fixed cost), and
returns the bridge from current operating profit to full potential.

## Step 3 — Judge controllability

For each gap, one of:

- **Controllable** — management can close it with known moves (procurement, pricing discipline, SG&A).
- **Capability-bound** — needs a capability VRIO rated `disadvantage` or `parity`; closing it is a
  build, partner or buy decision.
- **Structural** — set by the industry (Five Forces, scale, regulation); out of reach without changing
  position.

## Output

```markdown
### K-1. Full Potential — [company]
| Driver | Today | Benchmark (source) | Gap value ($) | Controllability | Traces to |
|---|---|---|---|---|---|
**Bridge:** current operating profit $[x] → full potential $[y] (+[z]%)
**Largest controllable gap:** [driver] — [one sentence]
**Impact Summary — Full Potential**
> _[Student writes this summary.]_
```

Present the bridge as a waterfall chart when file creation is available.

Write `company_layer.internal.full_potential = {drivers[], bridge, largest_controllable, sources[]}`.

## Rules

- The full-potential number is a ceiling, not a forecast. Say so in the exhibit.
- Every benchmark is cited; every gap traces to a unit-economics line or a KSF.
- Do not add the gaps naively; use the script's sequenced bridge.
