---
name: stratos-pestel
description: "StratOS PESTEL macro diagnostic. Scans Political, Economic, Social, Technological, Environmental and Legal factors for one industry, starting from competitors' 10-K risk factors, and ties every finding to a P&L line with a transmission mechanism, impact, certainty and velocity. Includes cross-dimension causal chains, monitor triggers, a multi-firm threat-allocation variant for coursework, and a delta mode for re-runs. Use for PESTEL, PESTLE, PEST, macro environment, external factors, or macro threats to an industry or set of firms."
license: Apache-2.0
---
# ©2026 Brad Scheller

# PESTEL Analysis (StratOS S1)

**Runs:** after competitor intel. **Reads:** the ledger scope and `ci.pestel_seeds[]`. **Writes:**
`industry_layer.pestel[]` — 15-25 findings, each tied to a P&L line. **Feeds:** driving forces
(which cite these ids) and the Five Forces a finding moves. Run standalone, it asks for the industry,
geography and horizon first.

An unanchored PESTEL is a trivia exercise. Every finding must answer: *what does this do to this
industry's P&L, and through which mechanism?*

**P&L lines** used below: `revenue.price`, `revenue.volume`, `revenue.mix`, `cogs.inputs`,
`cogs.labor`, `opex.sga`, `opex.rnd`, `capex`, `working_capital`, `financing`, `tax_and_levies`.
Direction is `+`, `−` or `±` (depends on the firm's response — say which).

## Step 0 — Start from the filings

If the ledger holds `ci.pestel_seeds[]`, begin there. Risk factors that several competitors disclose
(`shared: true`) are the strongest candidates — management named them under legal liability. Carry
each seed's evidence id into the finding. Then fill the gaps with Step 1: filings under-report
threats management would rather not name, such as a substitute technology or a social shift.

## Step 1 — Scan the six dimensions

For each dimension, find 2-5 factors **specific to this industry and geography**. Ask of each:
current state → 1-3 year trend → which P&L line it hits → opportunity or threat.

| Dimension | Look for | Common P&L lines |
|---|---|---|
| **P** Political | Industrial policy and subsidies, trade barriers and tariffs, export controls, state ownership, procurement preferences, political stability | `tax_and_levies`, `cogs.inputs`, `revenue.volume` |
| **E** Economic | Growth and cycle stage, rates and credit, FX, inflation and input costs, consumer spending and trading down, labour costs | `financing`, `cogs.inputs`, `revenue.mix` |
| **S** Social | Demographics, preference shifts, health and ethical consumption, digital adoption, trust, urbanisation | `revenue.volume`, `revenue.mix`, `opex.sga` |
| **T** Technological | Core-technology inflection points, AI and automation, platform shifts, standards wars, IP barriers, obsolescence speed | `opex.rnd`, `capex`, `cogs.labor` |
| **E** Environmental | Carbon rules and pricing, Scope 1-3 disclosure, resource scarcity, climate exposure of supply, circularity mandates | `tax_and_levies`, `cogs.inputs`, `capex` |
| **L** Legal | Licensing and entry rules, antitrust, data and privacy law, consumer protection, labour and safety law, product liability | `opex.sga`, `capex`, `revenue.price` |

For a pure digital business the Environmental dimension may be thin — say "limited impact" in one
line rather than padding it.

## Step 2 — Rate each finding on three axes

1. **Impact** on this industry — High / Medium / Low.
2. **Certainty** that it plays out on the horizon — High / Medium / Low.
3. **Velocity** — Slow (years), Accelerating (quarters), or Exponential (compounding; e.g. a price
   war, a regulatory cascade, an AI capability curve).

Then place it in the **impact × certainty** matrix and act by quadrant:

| | Certainty high | Certainty low |
|---|---|---|
| **Impact high** | **Strategic focus** — analyse deeply; it becomes a core assumption | **Scenario plan** — prepare alternatives; name the trigger signal |
| **Impact low** | **Monitor** — one line; set an early-warning indicator | **Drop** — leave it out of the report |

## Step 3 — Write the transmission mechanism

This is the step most PESTELs skip and the one graders argue with. For every Strategic-focus and
Scenario-plan finding, state the mechanism in one sentence:

> *[Macro change] → [what it does to buyers, suppliers, rivals or costs] → [P&L line and direction].*

Example (illustrative): *Cocoa crop failures → bean prices multiply → `cogs.inputs` rises faster than
retail price can follow → gross margin compresses (−), with private label gaining as shoppers trade
down (`revenue.mix`, −).*

## Step 4 — Trace cross-dimension chains

Dimensions interact; the chains are often the real insight. List 3-6 links in arrow form:

```
P→E  Tariffs on imported components → input cost up → price increases lag → margin squeeze
P→L  Anti-subsidy duties → firms build local plants → must meet local data-residency rules
T→S  Charging network density → range anxiety eases → adoption moves to the mass market
```

## Step 5 — Name the monitor variables

For every Scenario-plan finding, write a monitor entry: the variable, the trigger that would change
the call, and the response direction. These go to `industry_layer.monitor` and are what a scheduled
re-run diffs against.

## Output

```markdown
## PESTEL — [industry], [geography], [horizon]

**Governing finding:** [the single most important macro shift, in one sentence]

| ID | Dim | Finding | Velocity | Impact | Certainty | P&L line | Dir | Transmission | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| P1 | P | … | Accelerating | High | High | tax_and_levies | − | … | E003 |

**Cross-dimension chains:** …
**Monitor:** [variable] — trigger: […] — response: […]
**Constraint check:** R2/R6 pass · [warnings]
```

## Course variant — multi-firm threat allocation (MGT4850 Week 3 pattern)

When the scope is a *set of firms* rather than one industry, run Steps 1-3 per threat and assign each
threat to the firm **most critically exposed**, with its transmission mechanism (revenue, COGS or
market share). Keep any instructor answer key out of the output — the student makes the mapping.

## Re-runs — the delta pass

On a scheduled or user-requested re-run against a prior ledger, do **not** rewrite all six
dimensions:

1. **Broken assumptions first.** A prior finding now contradicted by evidence outranks any new finding.
2. Then factors that **moved materially** — a regulation passed or credibly proposed, an indicator
   crossing its trigger, a named event. Think-pieces and proposals going nowhere are not movement.
3. Then factors **new to the frame**.
4. Unmoved factors get one line each: "no material movement".
5. If the scope changed (new market, pivot), stop — a diff across a scope change is meaningless; rerun
   S0.

## Pitfalls

- **Generic:** "The economy continues to grow." → quantify it and say what it does to this industry.
- **Static:** current state only, no trend or horizon.
- **Isolated:** six silos with no chains between them.
- **Equal weighting:** a paragraph per dimension regardless of importance; the matrix exists to cut.
- **Competitor analysis in disguise:** PESTEL is macro. Rival moves belong in S2 and CI.
