---
name: stratiq-exec-deck
description: "Strat-IQ Executive Deck. Turns a completed Strat-IQ external analysis (the ledger and the detailed report) into a 14-16 slide executive PowerPoint: action-title storyline, industry overview snapshot, macro heat grid, Five Forces now vs horizon, trending influence factors, competitor benchmark, KSF scorecard heatmap, both strategic maps, blue-ocean ERRC, recommended moves, watch list, with sources on every slide and the detail in speaker notes. Use for 'make the deck', 'executive presentation', 'PowerPoint', 'slides for the board', or 'present the analysis'."
license: CC-BY-NC-4.0 AND PolyForm-Noncommercial-1.0.0
---
# ©2026 Brad Scheller

# Executive Deck (Strat-IQ)

**Runs:** last, after the detailed report — or on its own from any saved ledger. **Reads:** the
ledger (all stages) and the detailed report. **Writes:**
`external-analysis_<industry>_<base-company>_<YYYY-MM-DD>.pptx`.

The report is for the working team; the deck is for the executive who has 15 minutes. Every slide
states one conclusion, shows the evidence for it in a single visual, and keeps the detail in the
speaker notes. The deck contains **no new analysis** — every number and claim comes from the ledger.

## Building the file

Use the platform's PowerPoint capability: in Claude.ai, the built-in PowerPoint skill (needs **Code
execution and file creation**); in Claude Code or Cowork, a PowerPoint skill if one is installed,
otherwise `python-pptx`. Produce a real `.pptx` file the user can download and edit. If file creation
is unavailable, output the slide-by-slide content as text in the same structure and say so.

## Storyline (default 15 slides + appendix)

Write the **action titles first**, as a storyline: read top to bottom, the titles alone must tell the
whole argument. A title is a full sentence stating the insight — "Scale leaders are pulling away on
cost as prices fall", not "Competitive Landscape".

| # | Slide | Visual | Source in the ledger |
|---|---|---|---|
| 1 | Title — industry, base company, perspective, date | — | scope |
| 2 | **Executive summary** — the governing thought plus 3-4 supporting points | Text, numbered | report exec summary |
| 3 | **Industry overview** — size, growth, segments, life-cycle stage in one view | Market-size range bar (each source, labelled) + segment split + growth and stage callouts | `overview` |
| 4 | **How we got here** — recent history | Horizontal timeline, 6-8 events | `overview.timeline` |
| 5 | **Macro forces that hit the P&L** | Heat grid: PESTEL dimension × impact, each cell naming its P&L line | `pestel` |
| 6 | **How attractive the industry is — now and at the horizon** | Paired bar chart, five forces now vs horizon; attractiveness score | `forces`, `attractiveness` |
| 7 | **What is changing** — the trending influence factors | 3-5 rows: driver → mechanism → profit pool ↑↓↔ | `drivers` |
| 8 | **Who wins today** — competitor benchmark | Bar or dot chart on 2-3 defining metrics; base company highlighted | `competitors[].financials` |
| 9 | **What it takes to win** — KSF scorecard | Heatmap table: KSFs × competitors, weights, weighted total, rank | `ksf`, `ksf_scores` |
| 10 | **Where the base company stands** — Tier 2 view and gap to close | Two-column: strengths vs gaps; industry vs strategy-weighted score | `company_layer.ksf_view` |
| 11 | **Where everyone competes today** — conventional strategic group map | Scatter, clusters circled | `s5_conventional` |
| 12 | **Where no one competes yet** — disruption map | Scatter, whitespace shaded | `s6_disruption` |
| 13 | **The opportunity** — top blue-ocean candidate | ERRC grid + one-line thesis; stamp *demand: unpriced · capability: UNVALIDATED* visibly | `candidates[0]` |
| 14 | **Recommended moves** | 3-5 moves, each tied to a KSF gap or whitespace, with timing | report implications |
| 15 | **What to watch** | Table: indicator · threshold · what it would change | `monitor` |
| A1 | Methodology, scoring method, confidence and data gaps | Text | `warnings`, `scoring`, confidence |
| A2 | Sources | Numbered list matching the report's references | `evidence` |

Quick depth: drop slides 4, 10 and 15 (12 slides). If the user asks for fewer, merge rather than
cram — never put two messages on one slide.

## Slide rules

- **One message per slide.** At most 5 bullets, about 12 words each. Detail belongs in speaker notes.
- **Charts are real, editable chart objects** with data labels, not pictures of tables. Use a table
  only for the scorecard, the ERRC grid and the watch list.
- **The base company is highlighted** in the one accent colour on every chart where it appears.
- **Sources on every data slide** — a small footer: "Source: [publisher/filing] ([date]); Strat-IQ
  ledger as of [asof]".
- **Honesty survives the summary.** Forecasts are labelled as forecasts and shown as ranges; estimates
  keep their `[E]`; `[unverified]` items are left out of the deck or footnoted; the UNVALIDATED stamp
  stays on slide 13.
- **Speaker notes on every slide:** 80-150 words — what to say, the supporting numbers, the evidence
  ids, and the likely executive question with its answer.

## Design

- 16:9. Clean, consistent layout: title at top, one visual, a takeaway line at the bottom if needed.
- Fonts: titles 28-32 pt bold; body 16-20 pt; tables and chart labels at least 12 pt; footers 10 pt.
- Colour: navy and greys plus **one accent** reserved for the base company; red, amber and green only
  for the heat grid and scorecard, and with labels, not colour alone.
- Nothing overflows its box, nothing overlaps, and the same element is the same size on every slide.

## Quality check before handing over

1. Read only the titles in order — do they tell the story?
2. Every number on a slide matches the ledger and the report exactly.
3. Every data slide has its source footer; every slide has notes.
4. Open or render the file and check each slide for overflow, overlap and unreadable text; fix and
   re-check.

Then give the user the file, the slide count, and one line on how it maps to the report.
