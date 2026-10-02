---
name: stratos-value-chain
description: "StratOS Value Chain (case-memo Exhibit J). Breaks the base company into Porter's primary and support activities, names each activity's cost and value drivers, compares the share of cost it absorbs with the share of buyer value it creates, and files every activity under its evolution stage — Commodity, Product, Custom or Genesis — to show what the firm should buy, standardise, build or explore. Computed with a script. Use for 'value chain', 'Exhibit J', 'primary and support activities', 'where does the cost go', 'build or buy', or 'which activities create the value'."
license: Apache-2.0
---
# ©2026 Brad Scheller

# Value Chain (StratOS S8 · Exhibit J)

**Runs:** first in the internal analysis, after KSFs. **Reads:** the base company's internal evidence,
`industry_layer.overview.economics`, `industry_layer.ksf[]`, `company_layer.ksf_view` and
`industry_layer.drivers[]`. **Writes:** `company_layer.internal.value_chain[]`. **Feeds:** Resources
and Capabilities (capabilities are found in the activities), VRIO, and SWOT.

A firm's advantage does not sit in the firm as a whole. It sits in the separate activities the firm
performs to design, make, sell, deliver and support what it offers. This skill reads those activities
two ways: by what they **cost against the value they create**, and by how **evolved** they are — which
decides whether the firm should be doing them itself at all.

## Internal evidence

The external stages read the industry; this one reads **inside one firm**, so the evidence is
different:

- **Case memo** — the student's interview notes. Cite them as `Interview notes ([persona])`.
- **Public company** — the 10-K (Item 1 Business, Item 2 Properties, segment notes, the cost discussion
  in MD&A), investor presentations, and the CI benchmark.
- **Private company** — whatever the user supplies, plus signals at confidence Low.

Never invent an internal fact. A missing cost, headcount or process becomes `[ask in interview]` in a
case, or `n/a` with the reason elsewhere.

## Step 1 — List the activities

Name 8-15 activities **this firm actually performs**, each under one of Porter's nine categories:

| Primary activities | Support activities |
|---|---|
| Inbound logistics — receiving, storing, handling inputs | Firm infrastructure — management, finance, legal, planning |
| Operations — turning inputs into the product or service | Human resource management — hiring, training, pay |
| Outbound logistics — getting it to the buyer | Technology development — R&D, design, process improvement |
| Marketing and sales — making buyers aware and able to buy | Procurement — buying inputs, equipment and services |
| Service — keeping the product working after the sale | |

Write each activity as the firm does it ("battery pack assembly in two owned plants"), not as the
category ("operations"). For service and digital firms, translate the mechanism: operations is the
delivery of the service, inbound logistics is acquiring data or content, outbound is the channel or
platform.

## Step 2 — Cost and value for each activity

For every activity record:

- **Cost drivers** — what makes it expensive: scale, capacity utilisation, learning, input prices,
  location, labour rates.
- **Value drivers** — what the buyer gets from it: quality, speed, customisation, reliability, trust.
- **Cost share** — the share of the firm's operating cost the activity absorbs, when the evidence gives
  it. If it does not, rate it High / Medium / Low and say so.
- **Value share** — the share of the buyer's reason to choose this firm that the activity creates.
  Base it on what buyers decide on: the KSFs the activity delivers (use the Tier 2 weights when they
  exist, otherwise Tier 1) and what customers say in the notes. Label it `[estimate]`.
- **Sourcing** — in-house, outsourced or mixed.

> value-cost gap = value share − cost share

- **Value trap** — the activity absorbs clearly more cost than the value it creates.
- **Differentiating engine** — it creates clearly more value than the cost it absorbs.
- A gap within ±5 points is **in balance**; do not read a finding into it.

## Step 3 — Place each activity on its evolution stage

| Stage | The activity is… | Evidence to look for |
|---|---|---|
| **Genesis** | New and uncertain; nobody knows yet how to do it well | Few or no others do it; nothing to buy; frequent change and failure |
| **Custom** | Built specially by or for this firm; understanding is growing | Done differently at each firm; no standard vendor offering |
| **Product** | Available as standard offerings; vendors compete on features | Several vendors sell it; rivals use similar solutions |
| **Commodity** | A utility; standardised and bought on price | Many interchangeable suppliers; sold by volume or usage |

Give one line of evidence for each placement. Then note **movement**: which activities are evolving
toward the next stage, and which trending influence factor (`D` id) is pushing them. An activity that
is custom today and a product tomorrow is an advantage with an expiry date.

## Step 4 — Read the chain

1. **Stage against sourcing.** A commodity activity done in-house, or custom-built when a standard
   product exists, is cost with no advantage attached. A custom or genesis activity that creates the
   buyer's reason to choose and is outsourced is an advantage the firm does not control.
2. **Stage against the value-cost gap.** The firm's differentiating engines should sit in the custom
   and genesis stages. An engine sitting in the commodity stage can be copied by anyone who buys the
   same input.
3. **Linkages.** Name 1-3 places where one activity changes the cost or value of another (design
   choices that cut service cost; procurement terms that set operations' unit cost). Advantage often
   lies in the linkage, and it is harder to copy than a single activity.
4. **Against the industry.** Compare with `overview.economics`: is the firm strong where the
   industry's margin sits?

## Step 5 — Compute

Fill `templates/value-chain.csv` and, where code execution is available, run:

```
python scripts/value_chain.py value-chain.csv
```

It checks the stages and shares, computes each value-cost gap, flags value traps, differentiating
engines and stage-sourcing mismatches, and prints the activities grouped under the four stage
headings. Without code execution, do the same by hand and say so.

## Output

```markdown
## Value chain — [base company]

| Activity | Porter category | Stage | Sourcing | Cost share | Value share | Gap | Evidence |
|---|---|---|---|---|---|---|---|

**Differentiating engines:** …
**Value traps:** …
**Stage-sourcing mismatches:** …
**Linkages:** …
**Movement:** [activity] custom → product, pushed by [D id]
**Ask in interview:** …
```

### Exhibit J (template format)

The template's four headings, in its order. Under each, the activities at that stage with their
Porter category, the value-cost reading and the evidence.

```markdown
### J. Value Chain

**Commodity**
- [Activity] (Porter: [category]; [sourcing]) — cost [share], value [share] — [evidence]

**Product**
- …

**Custom**
- …

**Genesis**
- …

**Impact Summary — Value Chain**
> _[Student writes this summary.]_
```

Write "No activity at this stage" under an empty heading rather than padding it. Leave the Impact
Summary blank. In a case exhibit, state what the evidence shows about each activity; do not say what
the firm should do about it — that belongs in the student's memo.

Write the ledger, then return to the orchestrator for the checkpoint.

## Rendering

- **Claude.ai** — a simple self-contained chart: activities placed left to right by stage (Genesis →
  Commodity) and top to bottom by how visible they are to the buyer, with value traps and
  differentiating engines marked.
- **Claude Code / text** — the table above.

## Pitfalls

- **Listing the nine categories instead of the firm's activities** — the categories are a checklist;
  the analysis is in what this firm does under each.
- **Invented percentages** — a cost share with no source is `[ask in interview]`, not a guess.
- **Everything is "custom"** — most of any firm is product or commodity; say so.
- **Ignoring support activities** — procurement and technology development are often where the
  advantage or the trap is.
- **Reading the chain without the buyer** — value share comes from what buyers choose on, not from
  what the firm is proud of.
