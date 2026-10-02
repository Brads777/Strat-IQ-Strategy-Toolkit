---
name: stratos-vrio
description: "StratOS VRIO Analysis (case-memo Exhibit I). Tests each of the base company's key resources and capabilities on four questions in order — Valuable, Rare, Inimitable (costly to imitate), Organised to exploit — on cited evidence, assigns the competitive implication from disadvantage through parity, temporary, unexploited and sustained advantage, then checks every advantage against the industry's KSFs to flag competence traps, and updates the capability stamp on the blue-ocean candidates. Computed with a script. Use for 'VRIO', 'Exhibit I', 'sustainable competitive advantage', 'is this a core competency', 'resource-based view', or 'can the company actually do this'."
license: Apache-2.0
---
# ©2026 Brad Scheller

# VRIO Analysis (StratOS S9 · Exhibit I)

**Runs:** after Resources and Capabilities. **Reads:** `company_layer.internal.resources[]` and
`capabilities[]`, `industry_layer.pestel[]`, `forces[]`, `drivers[]` and `ksf[]`,
`company_layer.ksf_view`, `competitors[]`, and `company_layer.candidates[]`. **Writes:**
`company_layer.internal.vrio[]` and the `capability` stamp on each blue-ocean candidate. **Feeds:**
Resources and Capabilities (finalise mode) and SWOT.

Every firm believes it has core competencies. VRIO is the test: four questions, asked in order, each
answered from evidence. It is the one stage that can overturn an earlier conclusion — a strength the
firm claims, or a blue-ocean candidate the map found.

## Step 1 — Choose what to test

Take every capability from the Resources and Capabilities stage, plus the resources that are not
already inside a capability and matter on their own (a patent, a licence, a location). Aim for 6-12
items.

## Step 2 — Ask the four questions, in order

Answer each **Yes**, **No** or **?** (the evidence does not say). Every Yes and No cites evidence.

| Test | Question | What counts as evidence |
|---|---|---|
| **V — Valuable** | Does it let the firm exploit an opportunity or neutralise a threat? | Name the opportunity or threat by id (a PESTEL finding, a trending influence factor, a force) or the KSF it delivers. If it links to none, the answer is No. |
| **R — Rare** | Do only a few competitors have it? | Count the firms in the competitor set that have it. Rare means one or two; if most have it, it is table stakes. |
| **I — Inimitable** | Would a firm without it face a cost disadvantage in getting it? | Name the barrier (below) and estimate how long and how much a rival would need. |
| **O — Organised** | Is the firm set up to capture the value? | Structure, systems, incentives and culture that put it to use; and evidence it is being used. |

**Barriers to imitation.** Name which one applies, or answer No:

- **History** — it was built under conditions that cannot be recreated (a first-mover position, a
  long-accumulated dataset or relationship).
- **Causal ambiguity** — rivals cannot tell which practices produce the result.
- **Social complexity** — it rests on trust, culture or relationships that cannot be bought.
- **Legal protection** — a patent, licence or exclusive contract. Give the expiry date; protection
  with an end date is temporary by definition.

Substitution counts as imitation: if a rival can reach the same result a different way, answer No.

**Stop at the first No.** Later answers do not change the verdict. A **?** stops the ladder too: the
verdict is "undetermined beyond [the last Yes]", and the open question goes on the
`[ask in interview]` list (case) or the data-gap list.

## Step 3 — Read the verdict

| V | R | I | O | Competitive implication | Expected return |
|---|---|---|---|---|---|
| No | — | — | — | Competitive disadvantage | Below normal |
| Yes | No | — | — | Competitive parity (table stakes) | Normal |
| Yes | Yes | No | — | Temporary advantage | Above normal until copied |
| Yes | Yes | Yes | No | Unexploited advantage | Below its potential |
| Yes | Yes | Yes | Yes | Sustained advantage | Above normal, durable |

**Compute it deterministically.** Fill `templates/vrio.csv` and, where code execution is available,
run:

```
python scripts/vrio_screen.py vrio.csv
```

It applies the ladder, stops at the first No or ?, runs the reality check below, and prints the
verdict table and the items grouped for the exhibit. Without code execution, do it by hand and say so.

## Step 4 — The reality check

An internal capability is only an advantage if it is one the market rewards. A firm can be the best in
its industry at something buyers will not pay for.

If the StratOS scoring API is connected, send the VRIO results with the decision-criteria weights and
record the returned fit with `method: "api"`. Otherwise run the public screen and stamp
`method: "public-screen"`:

1. Link each item to the KSFs it delivers (`links_ksf`), using the KSF ids from the KSF stage.
2. Take the **highest** weight among those KSFs — the base company's Tier 2 weight when it exists,
   otherwise Tier 1.
3. Flag the item:
   - **Competence trap** — it passes V, R and I, but links to no KSF or only to KSFs weighted under
     0.10. The firm is distinctive at something that decides little.
   - **Supported** — it holds an advantage verdict and links to a KSF weighted 0.10 or more.
   - **Table stakes** — parity on a KSF weighted 0.10 or more: necessary, not differentiating.
4. In a case, also check the item against what customers said they choose on in the interview notes,
   and cite the note.

A competence trap is a finding, not an error. Report it; do not adjust the VRIO answers to remove it.

## Step 5 — Update the blue-ocean candidates

Strategic Mapping stamps every candidate `capability: "UNVALIDATED"` because the map shows where
nobody is, not whether this firm can get there. For each candidate in `company_layer.candidates[]`:

1. List what the candidate requires the firm to be able to do (its ERRC **raise** and **create**
   items).
2. Match each requirement to an item in the VRIO table.
3. Set `capability` to:
   - `"supported"` — every requirement is covered by an item at temporary advantage or better;
   - `"gap"` — at least one requirement has no item, or only an item at parity or below. Name the
     missing capability.

`demand` stays `"unpriced"`; only market research can change it. A candidate with `capability: "gap"`
and `demand: "unpriced"` is the **Mirage Trap**: say so.

Then hand back to Resources and Capabilities for finalise mode.

## Output

```markdown
## VRIO — [base company] · method: [api | public-screen]

| Item | Type | V | R | I | O | Implication | Links to KSF (weight) | Reality check | Evidence |
|---|---|---|---|---|---|---|---|---|---|

**Sustained advantages:** …
**Temporary advantages (and what ends them):** …
**Unexploited advantages (what the organisation lacks):** …
**Competence traps:** …
**Blue-ocean candidates:** [thesis] — capability: supported | gap ([missing capability])
**Ask in interview:** …
```

### Exhibit I (template format)

The template's four headings. Under each, the items that pass that test and the template's second
line. Follow with the full VRIO table.

```markdown
### I. VRIO Analysis

**Valuable Resources**
- [Resource or capability] — value creation: [the opportunity exploited or threat neutralised]

**Rare Capabilities**
- [Capability] — market position impact: [how many competitors have it, and what that does to the firm's position]

**Inimitable Attributes**
- [Hard-to-copy element] — [barrier: history / causal ambiguity / social complexity / legal protection] — competitive advantage: [implication]

**Organizational Support**
- Systems and processes: […]
- Cultural elements: […]

[VRIO table from the output above]

**Impact Summary — VRIO Analysis**
> _[Student writes this summary.]_
```

Write "None identified" under a heading no item reaches, rather than padding it. Leave the Impact
Summary blank.

Write the ledger, then return to the orchestrator for the checkpoint.

## Pitfalls

- **Four Yeses for everything** — rarity is counted against the competitor set, not asserted.
- **Skipping the order** — an item that is not valuable cannot be an advantage, however rare.
- **Legal protection read as permanent** — a patent is a temporary advantage with a date on it.
- **Forgetting O** — a firm that owns a rare, costly-to-copy asset and does not use it earns nothing
  from it.
- **Hiding the competence trap** — the capability the firm is proudest of is the one to check hardest.
- **Guessing a ?** — an unknown answer is a question for the next interview, not a Yes.
