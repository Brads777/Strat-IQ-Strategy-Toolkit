---
name: stratos-swot
description: "StratOS SWOT Analysis with a TOWS matrix (case-memo Exhibit K). Builds the four lists from the analysis already done rather than from brainstorming — strengths and weaknesses from the VRIO verdicts, the value chain and the KSF scorecard; opportunities and threats from PESTEL, Five Forces, the trending influence factors and the strategic maps — with every item traced to its source, then crosses them into SO, WO, ST and WT strategic options. Use for 'SWOT', 'Exhibit K', 'TOWS', 'strengths and weaknesses', 'opportunities and threats', or 'what options does the company have'."
license: Apache-2.0
---
# ©2026 Brad Scheller

# SWOT Analysis and TOWS (StratOS S10 · Exhibit K)

**Runs:** last in the internal analysis. **Reads:** `company_layer.internal` (value chain, resources,
capabilities, VRIO), `company_layer.ksf_view`, `competitors[].ksf_scores`, `industry_layer.pestel[]`,
`forces[]`, `drivers[]`, `ksf[]`, and `company_layer.candidates[]`. **Writes:**
`company_layer.internal.swot` and `company_layer.internal.tows`. **Feeds:** the report's implications
section, and in a case the student's list of alternatives.

A SWOT written from memory is a list of opinions. This one is a **summary of the stages already run**:
every item points to the finding it came from. It is where the external branch and the internal branch
meet.

## Gate — both branches must exist

- **External:** PESTEL and Five Forces at least; trending influence factors and KSFs where they have
  been run.
- **Internal:** VRIO, or at minimum the Resources and Capabilities inventory.

If a branch is missing, say which stages are needed and offer to run them. Do not fill the missing
half from general knowledge. If the user asks to proceed anyway, build the half that has evidence,
leave the other half marked `not yet analysed`, and record a warning.

## Step 1 — Sort internal from external

One test decides the row: **could the firm change this by its own decision?**

- Yes → internal: a strength or a weakness.
- No → external: an opportunity or a threat.

"Expand into Asia" is not an opportunity; it is a strategy. The opportunity is the external fact behind
it ("demand in the region is growing 12% a year").

## Step 2 — Build the four lists

3-6 items per list, ranked by how much each matters to profit, most important first.

| List | Draw from | Each item cites |
|---|---|---|
| **Strengths** | VRIO items at temporary, unexploited or sustained advantage · value-chain differentiating engines · KSFs where the firm leads the peer set | The VRIO item, activity or KSF id |
| **Weaknesses** | VRIO items at disadvantage · unexploited advantages (the organisation fails to use them) · competence traps · value traps and stage-sourcing mismatches · heavily weighted KSFs where the firm trails · `capability: "gap"` on a blue-ocean candidate | The same |
| **Opportunities** | PESTEL findings with direction `+` · trending factors that expand or redistribute the profit pool · forces that are weak or weakening · KSF white space · map whitespace | The P, D, force or KSF id |
| **Threats** | PESTEL findings with direction `-` · trending factors that compress the profit pool · forces that are strong or strengthening · competitor moves from CI signals | The P, D or force id, or the evidence id |

Rules:

- **Strengths and weaknesses are relative to competitors.** Something every rival also has is not a
  strength. Parity items stay out unless losing them would be a weakness.
- **A `±` finding** goes where the firm's position puts it, and the item says why.
- **One fact, one list.** If a fact seems to belong in two, split it into its internal and external
  parts.
- **No item without a source.** If the analysis did not produce it, it does not go in.
- In a case, internal items may also cite `Interview notes ([persona])`.

## Step 3 — Cross them: the TOWS matrix

The four lists describe; the TOWS matrix turns them into options. Cross each internal list with each
external one and write 1-2 options per cell:

| | **Strengths** | **Weaknesses** |
|---|---|---|
| **Opportunities** | **SO** — use a strength to take an opportunity | **WO** — use an opportunity to repair a weakness |
| **Threats** | **ST** — use a strength to blunt a threat | **WT** — reduce a weakness to avoid a threat |

Each option:

- names the items it pairs, by number (`S2 × O1`);
- is written as something the firm could do, concretely enough to be costed ("offer a 2-year warranty
  on the strength of the low defect rate"), not as a direction ("leverage quality");
- rests on a pairing that makes sense: the strength must actually bear on the opportunity or threat.
  Leave a cell at one option, or empty with a reason, rather than forcing a pairing.

An SO option built on a strength that VRIO rated a competence trap, or on a candidate stamped
`capability: "gap"`, is not available to the firm; do not write it.

**These are options, not recommendations.** The matrix does not rank them or choose among them. In a
case, the student decides which options become the alternatives in Exhibits N and M, and confirms them
before those exhibits are built.

## Output

```markdown
## SWOT — [base company]

**Strengths**
S1. [item] — [source id]

**Weaknesses**
W1. …

**Opportunities**
O1. …

**Threats**
T1. …

### TOWS — strategic options

| | Strengths | Weaknesses |
|---|---|---|
| **Opportunities** | SO1 (S2 × O1): … | WO1 (W1 × O2): … |
| **Threats** | ST1 (S1 × T2): … | WT1 (W3 × T1): … |
```

### Exhibit K (template format)

```markdown
### K. SWOT Analysis

**Strengths:**
- [Key internal strength] — [source exhibit and item]

**Weaknesses:**
- [Key internal weakness] — [source]

**Opportunities:**
- [Key external opportunity] — [source]

**Threats:**
- [Key external threat] — [source]

**TOWS — strategic options**
[the TOWS table above]

**Impact Summary — SWOT Analysis**
> _[Student writes this summary.]_
```

In the exhibit, cite sources by exhibit letter (D PESTEL, E Five Forces, G Key Success Factors, H, I,
J). Leave the Impact Summary blank.

Write the ledger, then return to the orchestrator for the checkpoint.

## Pitfalls

- **Brainstormed lists** — an item with no source is an opinion.
- **Strategies in the opportunity list** — opportunities are external facts.
- **Strengths that are table stakes** — if rivals have it too, it is not a strength.
- **Four balanced lists** — a firm in trouble has more weaknesses than strengths; the lists do not have
  to be the same length.
- **TOWS options that pair nothing** — every option names the items it crosses.
- **Choosing the winner** — the matrix generates options; the decision matrix and the memo choose.
