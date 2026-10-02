---
name: stratos-resources-capabilities
description: "StratOS Resources and Capabilities (case-memo Exhibit H). Inventories the base company's resources (tangible, intangible, human, organisational), names the capabilities it builds from them, tests which capabilities are core competencies, and states the competitive advantage they support — each item on cited evidence, with the advantage verdicts taken from the VRIO analysis. Use for 'resources and capabilities', 'Exhibit H', 'core competencies', 'resource audit', 'what is the company good at', or 'internal analysis'."
license: Apache-2.0
---
# ©2026 Brad Scheller

# Resources and Capabilities (StratOS RC · Exhibit H)

**Runs:** after the Value Chain, and again in **finalise mode** after VRIO. **Reads:** the base
company's internal evidence, `company_layer.internal.value_chain[]`, `competitors[]` (financials,
signals, moat, KSF scores) and `company_layer.ksf_view`. **Writes:**
`company_layer.internal.resources[]`, `capabilities[]`, `core_competencies[]` and
`competitive_advantage`. **Feeds:** VRIO (which tests these items) and SWOT.

The external analysis shows what the industry rewards. This skill records what the firm **has** and
what it **can do**, so the next stage can test whether any of it is an advantage.

- A **resource** is something the firm owns or controls.
- A **capability** is something the firm does repeatedly and well by combining resources.
- A **core competency** is a capability that buyers value, rivals find hard to copy, and the firm can
  use across several products or markets.
- A **competitive advantage** is what those competencies let the firm do that rivals cannot match:
  lower cost, or a difference buyers pay for.

Internal evidence comes from the student's interview notes in a case (`Interview notes ([persona])`),
or from the 10-K, investor material and the CI benchmark for a public company. Never invent an internal
fact; a gap is `[ask in interview]` or `n/a` with the reason.

## Step 1 — Inventory the resources

List 8-15 resources that matter to how this firm competes, by type:

| Type | Examples |
|---|---|
| **Tangible** | Plants, equipment, locations, cash and borrowing capacity, access to inputs |
| **Intangible** | Brand, patents, trade secrets, licences, data, reputation, contracts |
| **Human** | Specialist skills, experience, key relationships, leadership |
| **Organisational** | Culture, processes, control and reward systems, routines |

Each resource carries evidence and, where one exists, a measure (plant capacity, patent count, cash
balance, tenure). Leave out generic assets every rival also has unless their absence would be a
weakness.

## Step 2 — Name the capabilities

List 5-8 capabilities. Find them in the Value Chain: a capability is an activity, or a linkage between
activities, that the firm performs better than it would by chance.

For each capability record:

- **What it is**, as a verb phrase ("turns a repair around in 48 hours"), not a virtue ("service
  excellence").
- **The resources it combines** — ids from Step 1. A capability with no resources behind it is a
  slogan.
- **Evidence of performance** — a metric against the peer set, preferably the firm's KSF score or a CI
  benchmark figure. "The firm says it is good at this" is not evidence.
- **Threshold or distinctive** — a threshold capability is one every surviving rival has (table
  stakes); a distinctive one sets this firm apart.

## Step 3 — Test for core competencies

Put each distinctive capability through three tests:

| Test | Question |
|---|---|
| **Customer benefit** | Does it contribute materially to what buyers choose on? Name the KSF or customer criterion. |
| **Hard to imitate** | Would a rival need years, or a different history, to match it? |
| **Extendable** | Can it be used in more than one product, segment or market? |

A capability that passes all three is a **candidate** core competency. Expect 1-3; a firm with seven
core competencies has not been tested. It stays a candidate until VRIO confirms it.

## Step 4 — State the competitive advantage

**Inventory mode (before VRIO).** Record the advantage the firm *appears* to hold: cost or
differentiation, the strategy named in KSF Tier 2, and the evidence that it shows up in results (margin
or share against the peer set from the CI benchmark). Mark it `provisional`.

**Finalise mode (after VRIO).** For each candidate core competency, take the VRIO verdict and the
reality check from `company_layer.internal.vrio[]` and state:

- the verdict — sustained advantage, temporary advantage, unexploited advantage, parity or
  disadvantage;
- the basis — lower cost, or a difference buyers pay for;
- whether results confirm it — an advantage that does not appear in margin or share against the peer
  set is unproven, and the output says so.

A candidate that VRIO rates at parity or below is removed from the core-competency list and the
removal is stated. This is the point of running the test.

## Output

```markdown
## Resources and capabilities — [base company] · mode: [inventory | final]

| ID | Resource | Type | Measure | Evidence |
|---|---|---|---|---|

| ID | Capability | Resources combined | Performance evidence | Threshold / distinctive |
|---|---|---|---|---|

**Core competencies:** [capability] — customer benefit: … · hard to imitate: … · extendable: …
**Competitive advantage:** [basis] — [verdict or provisional] — confirmed in results: yes / no / n/a
**Ask in interview:** …
```

### Exhibit H (template format)

```markdown
### H. Resources and capabilities

**Resources**
- [Resource] ([type]) — [measure] — [evidence]

**Capabilities**
- [Capability] — built from [resources] — [performance evidence]

**Core competencies**
- [Capability] — [the three tests, one line] — VRIO: [verdict]

**Competitive advantage**
- [Basis of advantage] — [verdict] — [evidence in results]

**Impact Summary — Resources and capabilities**
> _[Student writes this summary.]_
```

Build Exhibit H in finalise mode, so the last two headings carry the VRIO verdicts. Leave the Impact
Summary blank.

Write the ledger, then return to the orchestrator for the checkpoint.

## Pitfalls

- **Resources listed as capabilities** — "a large factory" is a resource; "runs the factory at 95%
  utilisation" is a capability.
- **Virtues instead of capabilities** — "innovation" and "customer focus" with no activity or metric.
- **The firm's own claims as evidence** — mission statements and marketing copy are claims; cite a
  result.
- **Too many core competencies** — the tests are meant to fail most candidates.
- **Advantage with no result** — if the firm earns no more than its peers, say the advantage is
  unproven.
