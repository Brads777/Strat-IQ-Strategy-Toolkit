---
name: stratiq-strategic-mapping
description: "Strat-IQ strategic group mapping and blue-ocean discovery. Screens Brad Scheller's 36-vector library against the industry's KSFs and driving forces, assigns the five vector roles, plots the conventional strategic group map (where incumbents cluster) and the orthogonal disruption map (where whitespace is), then turns the best whitespace into ranked blue-ocean candidates with a strategy canvas and ERRC grid. The base company can be swapped to see the map from any competitor's side. Use for strategic group map, positioning map, perceptual map, whitespace, blue ocean, ERRC, strategy canvas, disruption axes, or 'what if X were the base company'."
license: CC-BY-NC-4.0 AND PolyForm-Noncommercial-1.0.0
---
# ©2026 Brad Scheller

# Strategic Mapping (Strat-IQ S4-S6)

**Runs:** after KSFs, and again on every base-company swap. **Reads:** `industry_layer.ksf[]`,
`industry_layer.drivers[]`, `industry_layer.forces[]`, `competitors[]`. **Writes:**
`industry_layer.vector_shortlist[]` (industry layer — computed once) and `company_layer` (roles,
maps, candidates — recomputed per base company). **Library:** `references/vector-library.md`.

Most strategic group maps are drawn on price against quality, and the competitors line up on a
diagonal: cheap bottom-left, premium top-right. That shows where firms stand today and reveals no
whitespace. This skill derives the axes from the industry's KSFs, then re-plots the same firms on
**orthogonal** vectors — dimensions uncorrelated with price — where the empty coordinates are.

## S4 — Screen the 36 vectors and assign the five roles

### Step 1 — Shortlist (industry layer)

Read `references/vector-library.md`. Build a shortlist of 8-10 vectors:

1. **Relevance** — drop vectors that do not apply to this industry (the library's examples lean
   toward hardware; translate the mechanism, not the example).
2. **Traceability (R5)** — each shortlisted vector must link to at least one KSF (`from_ksf`). A
   vector that no KSF supports cannot become an axis.
3. **Spread** — cover at least four of the six dimensions.

The shortlist is industry-level: it does not change when the base company changes.

### Step 2 — Assign the five roles

If the Strat-IQ scoring API is connected, send the shortlist with the industry layer and record the
returned roles with `scoring: "api"`. Otherwise run the public screen below and stamp
`scoring: "public-screen"`.

| Role | Purpose |
|---|---|
| 1. Primary benchmark | The conventional axis incumbents compete on (S5) |
| 2. Primary disruption (X) | First orthogonal axis (S6) |
| 3. Secondary disruption (Y) | Second orthogonal axis (S6) |
| 4. Moat reinforcer | What makes a whitespace position hard to copy |
| 5. Adoption driver | What removes friction so buyers actually move |

**Public screen** (used when the API is not connected; deliberately simpler than the proprietary
scoring):

<!-- TODO(Brad): define the public screen. See the note in the session summary. -->

### Pairing rules for the disruption axes

- **Never pair within one dimension** (e.g. not TCO with Pricing Predictability; not P/Q with
  Durability) — they move together and the map collapses to a diagonal.
- **Never pair correlated vectors across dimensions** either. Watch these families: TCO (1) with
  Residual Value (4); Risk-Sharing (6) with Fear of Failure (24); Modularity (13), Interoperability
  (17) and Accessory Ecosystem (35); Data Sovereignty (25) with Cyber-Resilience (29).
- **Neither disruption axis may be price or P/Q.** Those belong only to the S5 benchmark.
- **Cross-check the KSF hand-off.** The KSF skill proposes the pair of heavily weighted KSFs whose
  competitor scores are least correlated. If that pair maps onto shortlisted vectors from different
  dimensions and correlation families, prefer it; if not, say why the vector pair was chosen instead.

## S5 — Conventional strategic group map

Plot every competitor on the primary benchmark against price (or the industry's standard second
axis). Place each firm from `competitors[]` evidence and cite it. Mark clusters (strategic groups) —
firms close together are competing for the same buyers. This is the **red ocean**: say what the
cluster fights on.

**Confirm the strategic groups from KSF Tier 2.** Each firm's Tier 2 view names its strategy and
group from positioning evidence. Where a firm plots outside the group it claims (e.g. says premium,
sits with the budget cluster), flag the mismatch — it is a finding about that firm's strategy, not an
error to smooth over.

## S6 — Orthogonal disruption map

Re-plot the same firms on **disruption X × disruption Y**. Score each firm's position 0-1 on each
axis from evidence (the vector's spectrum defines 0 and 1). Then:

1. **Mark the incumbent cluster** — where most firms sit.
2. **Find whitespace** — coordinates with buyer value and **zero or near-zero competitor density**.
   Record each as `{ "at": [x, y], "occupied_by": [] }`.
3. **Say why it is empty.** Every empty coordinate is empty for a reason: nobody wants it (a demand
   question), it is too hard or costly to reach (a capability or cost question), or incumbents are
   structurally blocked (a business-model conflict — the best kind).

**Top-3 mode** (used for the case-memo Exhibit F, or when asked for "alternatives"): build **three**
disruption maps from three different axis pairs. Each pair must pass the pairing rules on its own, and
no two maps may share both axes. Rank them by the value of their whitespace, chart each one, and say in
one line what each reveals that the others do not. Store them as a list in `s6_disruption`.

## Blue-ocean candidates (company layer)

For the 1-3 best whitespace coordinates, **from the base company's side**:

1. **Thesis** — one sentence: who buys, what job, why the base company can get there.
2. **Strategy canvas** — the industry's competing factors on the x-axis, offering level on the y-axis;
   draw the incumbent value curve and the proposed one.
3. **ERRC grid** — what the offer **Eliminates** (factors the industry takes for granted), **Reduces**
   (well below standard), **Raises** (well above) and **Creates** (never offered).
4. **Six Paths check** — note which path the move uses: alternative industries, strategic groups,
   buyer chain (purchaser, user, influencer), complements, functional vs emotional appeal, or time
   trends (a driving force).
5. **Blue-ocean idea test** — buyer utility (is it exceptional?), price (accessible to the mass of
   target buyers?), cost (can the target cost be hit?), adoption (are the hurdles addressed? — this is
   role 5's job).
6. **Stamps** — `demand: "unpriced"` and `capability: "UNVALIDATED"` until the internal analysis
   (value chain, VRIO) and market research run. `stratiq-vrio` later sets `capability` to `supported`
   or `gap`. This skill can find and rank candidates; it cannot certify one. An unvalidated gap may be a **Mirage Trap**: an empty space that looks like an
   opportunity and is not.

## Swapping the base company

Keep the shortlist and every firm's coordinates. Recompute only the company layer: the base company's
distance to each whitespace, which candidates fit its moats and KSF scores, and its ERRC. Say plainly
that the whitespace itself did not move; only who is best placed to reach it did.

## Rendering

- **Claude.ai** — build an interactive artifact: a scatter chart with a toggle between the
  conventional and disruption maps, the base company highlighted, the whitespace shaded, and a
  base-company selector that re-labels from the chosen firm's side. Use the coordinates in the ledger;
  the artifact must be self-contained (no external API calls).
- **Claude Code / text** — ASCII maps with labelled axes, plus the coordinate table.

## Output

```markdown
## Strategic mapping — [industry] (base company: [X]) · scoring: [api | public-screen]

**Vector shortlist:** [id — name — from KSF] …
**Roles:** benchmark [v] · disruption X [v] · disruption Y [v] · moat [v] · adoption [v]

### Conventional map (S5): [benchmark] × [price]
[map] · Clusters: … · The red ocean fights on …

### Disruption map (S6): [X] × [Y]
[map] · Incumbent cluster: … · Whitespace: (x, y) — empty because …

### Blue-ocean candidates
1. [thesis] — ERRC: E … / R … / R … / C … — path: … — test: utility ✓ price ? cost ? adoption ✓
   demand: unpriced · capability: UNVALIDATED
```

Write the ledger, then return to the orchestrator for the checkpoint.
