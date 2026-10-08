---
name: stratiq-industry-overview
description: "Strat-IQ Industry Overview. A high-level, business-plan-style introduction to an industry in ten components: definition and scope, market size (two or more sources with definitions), growth and forecast ranges, segments and customers, industry economics and value chain, recent history timeline, key players and level of competition, life-cycle stage, trends influencing the industry, and a roadmap of the analysis to follow. Runs first in the Strat-IQ chain and is finalised at report time; also works on its own. Use for 'industry overview', 'overview of the X industry', 'industry background', 'market overview', 'how big is the market', or 'introduce the industry'."
license: CC-BY-NC-4.0 AND PolyForm-Noncommercial-1.0.0
---
# ©2026 Brad Scheller

# Industry Overview (Strat-IQ IO)

**Runs:** right after intake, and again at report time (finalise mode). **Reads:** the scope from
intake; at finalise time also Porter's Five Forces and Trending Influence Factors. **Writes:**
`industry_layer.overview`. **Feeds:** Competitive Analysis (which starts from the market structure
found here) and the first section of Part I of the final report.

The overview answers one question for a reader new to the industry: **what is this industry, how big
is it, how does it make money, who plays, and where is it heading?** It sets up the analysis; it does
not do it. Keep it to **1-2 pages**, plain narrative with small tables.

## Two modes

| Mode | When | What it does |
|---|---|---|
| **Profile** | After intake (and whenever run on its own) | Researches components 1-8, writes preliminary trends for 9 from a quick scan, and a draft roadmap for 10 |
| **Finalise** | At report time, after the other stages | Replaces the preliminary trends with the Trending Influence Factors, adds the Five Forces rivalry score to component 7, finalises the roadmap, and checks that no number conflicts with later stages |

Run on its own, Profile mode produces a complete, stand-alone overview; label component 9 "preliminary
— from a quick scan" so nobody mistakes it for the full trends analysis.

## The ten components

### 1. Definition and scope
What the industry is, from the demand side (the job customers hire it to do), and what is in and out:
products, segments, geography, value-chain stage. Name the industry codes (NAICS / GICS) if useful.
One paragraph. This is what makes every later number comparable.

### 2. Market size
Value (revenue) and, where the industry reports it, volume (units). For every figure: year,
publisher, and **how the source defines the market**. Estimates for the same industry often differ
several-fold because of definitions (units vs revenue, which products count, retail vs wholesale,
geography). Show at least two sources side by side, say which definition matches the scope, and
explain the gap. Never present one number as "the" market size.

### 3. Growth and projections
Historical growth (e.g. 5-year CAGR from actual data), then forecasts to the horizon **as a range from
named forecasters**, each with publisher and date, labelled `[Forecast]`. Say what drives the spread
(usually adoption-rate or price assumptions).

### 4. Segments and customers
The industry is rarely one market. Show the 3-5 segments that behave differently — by product type,
customer type, price tier or region — with each one's size or share and growth where available, and
who buys and why. Example (illustrative): passenger EVs split by battery-electric vs plug-in hybrid,
by region, and by mass vs premium price tier.

| Segment | Size or share | Growth | Who buys, and why |
|---|---|---|---|

### 5. Industry economics and value chain
How money is made: the main stages of the value chain (inputs → production → distribution → sale →
service/software), where margin sits along it, the typical gross and operating margin range, capital
intensity, and the cost structure (fixed vs variable). A short paragraph plus a one-line chain:

```
[raw materials] → [components] → [assembly] → [distribution] → [after-sales / software]
   margin: low        medium          thin          low              high
```

### 6. Recent history
6-12 significant events over roughly the last 5-10 years: entries and exits, major M&A, technology
breakthroughs, regulatory changes, price wars, supply shocks. One dated line each, with why it
mattered and an evidence id.

| Year | Event | Why it mattered |
|---|---|---|

### 7. Key players and level of competition
The leaders by revenue or volume with their approximate shares (cited; "n/a" if unavailable), the
number of meaningful players, concentration (top-4 share, HHI if computable), whether shares have been
stable, and whether the industry is consolidating or fragmenting. In finalise mode, add the Five Forces
rivalry score in one sentence. Name the players; save firm-by-firm profiles for Competitive Analysis.

### 8. Life-cycle stage
Emerging, growth, shakeout, mature, or declining — with the evidence:

| Stage | Typical signals |
|---|---|
| Emerging | Few players, unproven demand, no dominant design, heavy losses |
| Growth | Rapid growth, many entrants, prices falling, demand outrunning supply |
| Shakeout | Growth slowing, price wars, exits and consolidation, margins squeezed |
| Mature | Slow growth, stable shares, cost and efficiency competition |
| Declining | Shrinking demand, capacity cuts, harvest or exit strategies |

Different segments can sit at different stages — say so. End with one sentence on what the stage
implies for strategy (e.g. a shakeout rewards scale and cost position over new features).

### 9. Trends influencing the industry
The top 3-5 forces of change, one or two lines each. In finalise mode these are the Trending Influence
Factors (the full analysis follows later in the report); in profile mode, a preliminary scan.

### 10. What this analysis covers
Two or three sentences that turn the overview into an introduction: the key questions from the run
brief, and the order in which the report answers them (PESTEL → Five Forces → trends → competitive
landscape → KSFs → strategic maps → recommendations).

## Evidence discipline

- Every figure carries a source and date; forecasts are `[Forecast]`; estimates are `[E]`.
- Where good data sits behind paid research, use what is public (press summaries of those reports,
  trade associations, government statistics, company filings) and cite the summary.
- Never invent a market size, share, growth rate or date. A visible "n/a — not publicly reported" is
  better than a plausible number.

## Keep out of the overview

- **No framework verdicts** — attractiveness scores, KSF rankings and whitespace belong in their own
  sections. The overview previews; it does not conclude.
- **No firm-by-firm profiles** — name the leaders and their shares only.
- **No padding** — if it runs past two pages, it has started doing the analysis.

## Output

```markdown
## Industry Overview — [industry] ([geography], [horizon])

**Definition and scope.** …

**Market size.**
| Estimate | Year | Source | Definition | Matches our scope? |

**Growth and projections.** Historical [x]% CAGR ([years]); forecast [a]–[b]% to [year] [Forecast] ([publishers]).

**Segments and customers.**
| Segment | Size or share | Growth | Who buys, and why |

**Industry economics.** … [value-chain line]

**Recent history.**
| Year | Event | Why it mattered |

**Key players and competition.** Leaders: … · top-4 share [x]% · [n] meaningful players · consolidating / fragmenting · rivalry [score] (finalise)

**Life-cycle stage.** [stage] — evidence … — implication …

**Trends influencing the industry.** 1… 2… 3… ([preliminary] in profile mode)

**What this analysis covers.** …
```

Write `industry_layer.overview` to the ledger, then return to the orchestrator for the checkpoint (or,
on its own, hand the overview to the user and offer the full analysis).
