---
name: stratos-case-exhibits
description: "StratOS Case Memo Exhibits. Builds the Exhibits section of the MGT4850 Case Analysis Memo in the course template's exact order and headings — C Industry Overview, D PESTEL, E Five Forces, F Strategic Map (current plus top 3 disruptions), G Key Success Factors, L Decision Criteria and Weights, M Decision Matrix, N Pros and Cons, O Segment CLV — by running the StratOS skills on the case facts the student enters (the course cases are interactive persona interviews, so there is no case document), with every Impact Summary left blank for the student. Never writes the memo, Exhibit A or Exhibit B. Use for 'case exhibits', 'build my exhibits', 'case memo exhibits', or 'fill in the template exhibits'."
license: Apache-2.0
---
# ©2026 Brad Scheller

# Case Memo Exhibits (StratOS)

Builds the **Exhibits** section of the course's Case Analysis Memo. The student still writes the
memo itself (Key Issues, Recommendations, Decision Criteria paragraph, Analysis, Conclusion), Exhibits
**A and B**, and **every Impact Summary**. The exhibits give them a fast, fact-based base to decide
from; the Impact Summaries are where they show they understood it.

## What the student provides first

1. **The case facts, entered by the student.** The course cases are interactive: most of the facts
   live in personas the student interviews, so there is **no case document to read**. Ask the student
   for:
   - the case company, what it sells, and where;
   - the industry and geography it competes in;
   - its main competitors;
   - their **interview notes**: figures, constraints, goals, customers and segments, and anything
     else the personas said (pasted text or an uploaded file);
   - anything they found in their own research.

   This is how the toolkit is used at work, too: nobody hands you the case, you gather the facts.
2. **Exhibit A — Guiding Questions** and **Exhibit B — Key Issues** (central problem, management
   questions, required goals), written by the student.
3. **Alternatives** for each management question, if the student has them.

If Exhibit B is missing, the industry exhibits (C-G) can still be built, but **L, M and N cannot**:
ask the student for Exhibit B before building them. Never write A or B.

## Scope from the student's facts

Set the StratOS scope from what the student entered: the **industry** the case company competes in,
its **main competitors**, and the **case company as the base company**. Run the orchestrator's intake
with these values rather than asking from scratch.

Industry-level exhibits (C-G) use public evidence as usual. Case-specific facts come **only** from the
student's notes: cite them as `Interview notes ([persona])`. **Never invent a case fact** or what a
persona said. If an exhibit needs a fact only the case can supply (a cost, a goal, a segment size),
mark it `[ask in interview]` and list it at the end as a question for the student's next persona
interview.

## Exhibit map

| Exhibit (template) | Built by | Notes |
|---|---|---|
| C. Industry Overview | `stratos-industry-overview` (finalise mode) | Use the template's nine headings in order: definition and scope · market size · growth and projections · segments and customers · industry economics and value chain · recent history · key players and level of competition · life-cycle stage · trends influencing the industry |
| D. PESTEL Analysis | `stratos-pestel` | Rearrange the findings under the template's sub-headings (below) |
| E. Five Forces Analysis | `stratos-five-forces` | Rearrange under the template's sub-factors (below), with each force's 1-5 score |
| F. Strategic Map | `stratos-strategic-mapping` | **Current map** plus the **top 3 disruption maps** (three different axis pairs), each charted |
| G. Key Success Factors | `stratos-ksf` | Numbered list (No. 1, No. 2 …) with the scorecard; Tier 2 view for the case company |
| H. Resources and capabilities | — | **Phase 2** — leave the template heading with "Phase 2 tool — coming" |
| I. VRIO Analysis | — | **Phase 2** |
| J. Value Chain | — | **Phase 2** |
| K. SWOT Analysis | — | **Phase 2** |
| L. Decision Criteria and Weights | `stratos-decision-criteria` | Needs Exhibit B |
| M. Decision Matrix | `stratos-decision-matrix` | One matrix per management question |
| N. Pros and Cons Analysis | `stratos-decision-matrix` | Built before M |
| O. Customer Segment Lifetime Value | `stratos-segment-value` | **Only if relevant and the student's interview notes give the data**; otherwise omit it (the template marks it optional) |

The template letters the CLV exhibit "I", which duplicates VRIO; use **O** unless the instructor says
otherwise.

## Exhibit D — PESTEL sub-headings (template)

Place every finding under one of these; write "No material factor identified" where none applies,
rather than leaving a sub-heading empty or padding it.

- **Political:** government policies · political stability · trade restrictions · tax policies · industry regulations
- **Economic:** economic growth · interest rates · exchange rates · inflation rate · labor costs
- **Social:** demographics · cultural trends · lifestyle changes · consumer attitudes · education levels
- **Technological:** innovation rates · automation · R&D activity · technology adoption · infrastructure
- **Environmental:** climate impact · sustainability · resource usage · energy concerns · waste management
- **Legal:** industry laws · employment laws · safety regulations · consumer protection · IP regulations

Keep each finding's P&L line and evidence citation from the PESTEL stage.

## Exhibit E — Five Forces sub-factors (template)

- **Competitive Rivalry:** current competition · market growth · exit barriers · differentiation
- **Supplier Power:** supplier concentration · switching costs · forward integration · input uniqueness
- **Buyer Power:** buyer concentration · purchase volume · switching costs · price sensitivity
- **Threat of New Entrants:** entry barriers · capital requirements · scale economies · distribution access
- **Threat of Substitutes:** available substitutes · switching costs · price-performance · buyer propensity

Show each force's score (1-5) and its evidence after its sub-factors.

## Exhibit F — maps

- **Current map:** the conventional strategic group map (Strategic Mapping S5), as a chart.
- **Potential disruptions:** the **top 3** disruption maps (Strategic Mapping S6, top-3 mode), each a
  chart with its two axes named, the whitespace marked, and the blue-ocean candidate stamped
  `capability: UNVALIDATED` (the internal analysis that would validate it is Phase 2).

## Format of every exhibit

```markdown
### [Letter]. [Template title]
[Content in the template's structure, with sources]

**Impact Summary — [Template title]**
> _[Student writes this summary: what the exhibit shows and what it means for the recommendations.]_
```

**Never write the Impact Summary.** Leave the box empty for the student, in every exhibit.

## Delivery

Produce a **Word document** (`.docx`) named `Exhibits_<case-name>_<YYYY-MM-DD>.docx`, with headings
matching the template so the student can paste it under the memo's Exhibits heading. Charts are
embedded images or native charts; tables are real tables. If file creation is unavailable, output the
exhibits as formatted text in the same order.

Every figure keeps its citation; add a short **Sources** list at the end of the exhibits. Then tell the
student which exhibits were built, which were skipped (O when there is no data; H-K in Phase 2), and
that the memo, Exhibits A-B and all Impact Summaries are theirs to write.

## Rules

- Do not write the memo or any part of it: no Key Issues paragraph, recommendations, analysis
  paragraphs or conclusion.
- Do not draft Impact Summaries, even if asked to "finish the exhibits". Explain that the summary is
  the student's evidence of understanding, and leave it blank.
- Never invent case facts or persona statements; case-specific facts come only from the student's
  notes, and gaps become `[ask in interview]` questions.
- Follow the memo's own standards inside the exhibits: no "I"/"we", no beliefs, no predictions; facts
  and cited evidence only.
