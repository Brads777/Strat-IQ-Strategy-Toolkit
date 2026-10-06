---
name: stratos-growth-barriers
description: "StratOS Growth Barriers (supplementary case-memo Exhibit K-2). Finds the binding constraint on the base company's growth, the one barrier that caps everything else, by testing six candidate barriers in order (demand, supply and capacity, capability, capital, channel access, regulation) against evidence from Parts 1 and 2. Ranks the rest as secondary, and states what would have to be true to lift the binding one. Use for 'growth barriers', 'what is holding growth back', 'binding constraint', 'bottleneck', 'why can't it grow faster', or 'Exhibit K-2'."
license: Apache-2.0
---
# ©2026 Brad Scheller

# Growth Barriers (StratOS · Part 2 · Exhibit K-2)

**Runs:** after Full Potential, before SWOT. **Reads:** the whole Part 1 industry layer, Unit
Economics, Full Potential and VRIO. **Writes:** `company_layer.internal.growth_barriers`. **Feeds:**
SWOT (weaknesses and threats), Strategic Options, and the Initiative Prioritizer, where the binding
constraint goes first.

A firm usually has many problems and **one binding constraint**: the barrier that, if lifted, lets
growth rise until it meets the next one. Effort spent anywhere else improves nothing yet.

## Step 1 — Test the six candidate barriers

Test each against evidence. A barrier is **binding** if growth would rise were it lifted *and* the
other barriers have slack.

| Barrier | Evidence that it binds | Typical sources |
|---|---|---|
| **Demand** | Utilisation below capacity, rising inventory, discounting, share loss | Unit Economics, CI, PESTEL demand findings |
| **Supply and capacity** | Order backlog, waiting lists, sold-out allocations, input shortages (e.g. cells, chips) | Filings, news, Five Forces supplier power |
| **Capability** | A heavily weighted KSF where the firm trails and VRIO rates `disadvantage` | KSF scorecard, VRIO |
| **Capital** | Negative free cash flow, rising leverage, a credit-rating or covenant limit | Financial benchmark |
| **Channel access** | Distribution controlled by rivals or intermediaries; high CAC relative to contribution | Five Forces buyer power, Unit Economics |
| **Regulation** | Licences, homologation, tariffs, local-content rules that cap the reachable market | PESTEL political and legal |

## Step 2 — Name the binding constraint

Choose one. State it in one sentence with its evidence ids, then say **what would have to be true** to
lift it and **how much growth** would follow before the next barrier binds (use the Full Potential
gaps for the size).

If two barriers truly bind together (e.g. capital and capacity in a plant build), say so and explain
the link; do not list five as "binding".

## Step 3 — Rank the rest

List the other barriers as `secondary` (will bind next), `slack` (not limiting now) or `n/a`, each
with its evidence.

## Output

```markdown
### K-2. Growth Barriers — [company]
**Binding constraint:** [barrier] — [one sentence, evidence ids]
**To lift it:** [what must be true] · **Growth unlocked before the next barrier:** [estimate, source]
| Barrier | Status (binding / secondary / slack / n/a) | Evidence |
|---|---|---|
**Impact Summary — Growth Barriers**
> _[Student writes this summary.]_
```

Write `company_layer.internal.growth_barriers = {binding, to_lift, unlocked, barriers[], sources[]}`.

## Rules

- One binding constraint unless the evidence shows a genuine pair.
- No barrier without evidence; an untested barrier is `n/a — not enough evidence`, not `slack`.
- In GLO-BUS, test the barriers on the team's own reports: demand (unsold inventory), capacity
  (overtime, workstations), capital (credit rating, cash) and image rating.
