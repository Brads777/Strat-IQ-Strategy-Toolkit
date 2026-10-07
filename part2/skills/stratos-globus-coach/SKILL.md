---
name: stratos-globus-coach
description: "StratOS GLO-BUS Coach for the GLO-BUS simulation (action cameras and drones, four regions), five modes: (1) benchmark the real camera and drone industries from industries.json to learn the economics behind the game; (2) CIR gap analysis: strategic group maps (price vs P/Q), the share leader's driver, white space; (3) year coaching against the five KPIs with guardrails; (4) a full-year review naming the strategy the team's captured inputs reveal, with general lessons; (5) a weekly progress report after each round: graphs of KPIs, cost per unit, price and P/Q vs the industry, the position taken, standing against rivals from the class reports, and what to watch next round (weekly_report.py). Feedback, not recommendations; never enters decisions. Use for 'GLO-BUS', 'CIR', 'weekly report', 'how are we doing', 'review our GLO-BUS year', 'strategic group map', or 'why did our score drop'."
license: Apache-2.0
---
# ©2026 Brad Scheller

# GLO-BUS Coach (StratOS)

Checked against the MGT4850 GLO-BUS overview (2026-10-01). The course's GLO-BUS instructions and the
official GLO-BUS help guides override anything here.

## Five ways to use it

When the coach opens, ask which one the team needs (five modes) (the interactive choice widget if available):

| Mode | When | What the team brings | What it produces |
|---|---|---|---|
| **1. Learn the real industry** | Before Year 6, or when a team does not understand why a lever matters | Nothing; uses `industries.json` (`cameras`, `drones`) | A short StratOS benchmark of the real camera or drone industry, translated into GLO-BUS levers |
| **2. CIR gap analysis** | After every round, from Year 6 on | The CIR and Camera & Drone Journal figures, pasted or uploaded (`references/cir-gap-prompt.md` is the fill-in template) | Strategic group maps, the share leader's driver, the weakest rival, white space, and 3-5 moves for next year |
| **3. Year coaching** | Before entering a year's decisions | The team's own results and its chosen strategy | Steps 1-3 below: anchor, diagnose, 3-5 testable moves with guardrails |
| **4. Full-year review** | After a round, when the team has a capture file | `globus-capture-<company>-Y<year>.json` from `stratos-globus-capture` | Feedback, not recommendations: the strategy the team's inputs reveal, what that strategy demands, and general lessons from the inputs and results |
| **5. Weekly progress report** | After every round, from the first round on | All capture files so far | A report with graphs: scorecard vs investor expectations, the position taken, progress, standing in the contest, what rivals changed, what to watch next round, questions |

Mode 2 ends by handing its moves into mode 3's guardrail check. Modes can run in any order.

## Mode 1 — Learn the real industry

The GLO-BUS model is its own simulation; real companies are **analogues, not answer keys**. Use them
to understand why a lever matters, never to copy a number into a decision screen.

1. Load the `cameras` or `drones` entry from `industries.json` (Project knowledge or `project-data/`).
   Its `globus` block names the product line it mirrors.
2. Run a **quick-depth** StratOS chain: Industry Overview (profile) → Competitive Analysis → Five
   Forces → KSFs → Strategic Mapping. Use the orchestrator's minimum-chain rule; do not run the full
   report unless asked.
3. Translate each finding into the GLO-BUS lever it explains, in a table:

| Real-world finding | Example analogue | GLO-BUS lever it explains |
|---|---|---|
| Gross margin and retailer discounts in consumer cameras | GoPro's margin and channel costs | Price, retailer support, warranty (cameras) |
| Low-cost, high-volume assembly vs premium features | Akaso vs Garmin / Insta360 | Low-cost vs high-P/Q strategy, model count |
| R&D scale and vertical integration as a cost advantage | DJI | Component quality, R&D, cost per unit (drones) |
| Software-led and commercial-segment differentiation | Skydio, Autel | High-P/Q drones, features, commercial buyers |
| Trade restrictions on drone makers | US actions on Chinese drones (PESTEL) | Regional demand and pricing differences |

Mark every real-world figure with its source and `asof` date. Private firms (DJI, Skydio, Akaso) file
no accounts: use reported estimates marked `[estimate]` or say `n/a`.

## Mode 2 — CIR gap analysis

The team pastes or uploads its latest **Competitive Intelligence Report (CIR)** and the benchmarking
pages of the **Camera & Drone Journal (CDJ)**. If they have not, give them the fill-in block from
`references/cir-gap-prompt.md` (3-5 minutes of copying figures). Never guess a missing figure: mark it
`n/a` and say which analysis it limits.

**Step 1 — Put the figures in a table.** One row per company, product line and region (or the global
summary if that is all they have): price, P/Q rating, number of models, advertising (and search-engine
ads for drones), retailer support or promotions, warranty, market share. Save it as a CSV in the
format of `templates/cir.csv`.

**Step 2 — Map the strategic groups.** Run `scripts/globus_groups.py cir.csv --chart groups.png`. It
plots price against P/Q for each product line (bubble size = market share), and places each company in
a group relative to the industry averages:

| Group | Rule (vs industry average) |
|---|---|
| Low-cost / economy | Price below and P/Q below |
| Premium differentiator | Price above and P/Q above |
| Value leader | P/Q at or above, price at or below |
| Stuck in the middle | Price above with P/Q below |

The script also names the share leader, flags the company with the biggest gap between its spending
(ads, support, discounts) and its share, and lists empty cells on the price-P/Q grid. Show the chart and
say where **the team's own company** sits.

**Step 3 — Explain the leader and the weakest rival.**
- Who won the most share, and the operational driver behind it: a price cut, an advertising push, deep
  retailer support or discounts, more models, or higher P/Q. Point to the row in the table.
- Was it profitable? Compare the leader's operating margin and cost per unit in the CDJ with the
  industry average. Share bought with margin is not a win on EPS or ROE.
- Which rival is weakest and most likely to lose share next year, and why.

**Step 4 — Find the white space.** Where is there little or no competition (e.g. a high-P/Q drone tier
nobody occupies, or a region where every team crowded into the budget tier)? For each empty space, say
whether the team **can reach it** given its P/Q, cost per unit and capacity: an empty space the team
cannot serve profitably is a trap, as in StratOS's blue-ocean check.

**Step 5 — Hold, pivot or move.** One recommendation on position for each product line: defend the
current group, pivot toward cost leadership, or move toward premium differentiation, with the evidence.

**Step 6 — Moves for next year.** Propose **3-5 moves in total**, across the five decision screens
(product design, marketing and pricing, assembly operations and workforce, corporate social
responsibility, finance), each with its expected effect on all five KPIs. For screens with no move, say
"hold" and why. Then run **every move through the guardrails below** before showing it. A move that
fails a guardrail goes under "Not recommended this year".

Log the maps and moves to `globus.cir_log[]` in the ledger (year, groups, leader, white space, moves).

## Mode 4 — Full-year review (from a capture file)

`stratos-globus-capture` collects the team's decision screens, projections and company reports, plus
the class-wide reports, into one file. If the team has no capture file, offer to run the capture (or
its upload route) first.

**This mode gives feedback, not recommendations.** It tells the team what strategy their inputs
reveal and what general lessons the inputs and results point to. It never proposes specific numbers,
a list of moves, or a decision to enter: the team works those out. The guardrails below may be cited
as general principles, never turned into instructions for this team's next decisions.

1. **Check the file.** Note any `missing_required` or thin pages from the capture check, and say which
   comments they limit.
2. **Read the inputs and the results.** From the decision screens: price, P/Q, models, marketing,
   warranty, compensation, operations, CSR and finance choices, by product and region. From the class
   reports: where those choices sit against the industry (CIR, CDJ benchmarks, `globus_groups.py`
   strategic groups) and what happened (share, cost per unit, margins, the five KPIs, image rating).
3. **Name the apparent strategy**, product by product, from the pattern of inputs, not from what the
   team says it intended: low-cost provider, broad differentiation, best-cost provider, focused
   low-cost, or focused differentiation. State the evidence and a confidence (`clear`, `mixed`,
   `unclear`). If cameras and drones, or regions, follow different strategies, say so. If the inputs
   point in different directions (e.g. premium P/Q with bargain pricing and minimal advertising), say
   the pattern looks **stuck in the middle**, without telling the team which way to go.
4. **Explain what that strategy demands**, as general principles (table below).
5. **Connect the evidence to the principles.** 3-5 observations, each in this shape:
   *"Your [result or input, with the figure] suggests [what it means for this strategy]. Teams pursuing
   [strategy] generally [general guidance]."* Point to the screen and figure each time. Where the
   results contradict the strategy's logic (a low-cost team whose cost per unit is above the industry
   average; a differentiator whose image rating is falling), say so plainly.
6. **Projections vs actual**, where both are in the capture: note large gaps KPI by KPI and the general
   lesson (usually that rivals moved more than the team assumed), naming which rivals and which lever.
7. **Close with questions, not answers**: 2-3 questions the team should discuss before its next
   decisions (*"Is the warranty level consistent with a low-cost position?"*).

Example of the voice:

> *Your team is apparently pursuing a **low-cost provider** strategy in cameras: price 9% below the
> industry average, P/Q at 3.2 stars, the fewest models. Low-cost providers must drive cost down
> wherever possible while keeping product quality at the minimum customers will accept. Your image
> rating fell to 61 while rivals held theirs, which suggests consumer trust is slipping below that
> minimum. Teams in this position generally look at the quality and service levers that customers
> notice most, rather than cutting further on those.*

**General principles by strategy** (cite as lessons, never as prescriptions):

| Apparent strategy | What it demands | Typical warning signs in the results |
|---|---|---|
| Low-cost provider | Cost per unit at or below the industry low; price below average; efficiency in assembly and compensation; quality held at the minimum customers accept | Cost per unit near or above average; image rating falling; share not growing despite lower prices |
| Broad differentiation | P/Q, models, warranty and brand above average, paid for by a price premium; marketing that makes the difference visible | Premium not holding; P/Q edge eroding as rivals catch up; margins squeezed by spending without share |
| Best-cost provider | Above-average quality at an average or slightly lower price; costs controlled tightly enough to fund both | Costs drifting up toward differentiators while price stays mid-market |
| Focused (low-cost or differentiation) | Resources concentrated on chosen regions or segments; not spread thin across all of them | Spending spread evenly across regions; no region where the team leads |
| Stuck in the middle | (not a strategy) | Inputs that contradict each other; middling share and margins everywhere |

Log the review to `globus.reviews[]` in the ledger (year, apparent strategy and confidence,
observations, lessons, questions).

## Mode 5 — Weekly progress report (after every round)

Run `scripts/weekly_report.py globus-capture-<co>-Y6.json … globus-capture-<co>-Y<n>.json --ledger
<team ledger>` with every capture file so far. It writes the weekly review in the StratOS executive
format:

- `weekly-report-Y<n>-memo.docx`: a memo in exhibit style (sections W1-W7 with tables and charts, an
  Impact Summary for the team to write after each section, sources);
- `weekly-report-Y<n>-deck.pptx`: a nine-slide deck with action titles, a one-slide summary, charts,
  source lines and speaker notes (each ending with a likely question and answer);
- `weekly-report-Y<n>.html` (one page, print to PDF) and `weekly-report-Y<n>.json` (the facts).

Give the team the memo and the deck, then add a short narrative in the Mode 4 voice from the JSON. Run
it every week from the first round, once the team has chosen its position: the early reviews are where a
drift shows while there is still time to pivot. The sections:

1. **Scorecard.** Rank, score, the leader, and the five KPIs against investor expectations.
2. **The position you've taken**, by product: the apparent strategy from price, P/Q and cost per unit vs
   the industry, the strategic group on the CIR, and whether it matches the strategy the team chose. A
   drift between positions is the most useful thing to say early: it is when a team can still pivot.
3. **Progress graphs**: KPIs vs expectations, price / P/Q / cost per unit vs the industry, share, margin.
4. **Where you stand in the contest**: every company's score by year from the scoreboard, and what
   rivals changed since last year, **from the class-wide reports only** (scoreboard, CIR). Never use
   another team's own screens or files.
5. **What to look out for next round**: the watch items, each with its evidence and a general lesson.
6. **Questions for the team** (2-3).

Feedback, not recommendations: no decision values, no list of moves. Rebuild the workbook with `--report weekly-report-Y<n>.json`
so the **Findings & Questions** tab collects every week's watch items and questions; **Season by Year**,
**Competition by Year** and **KPI Charts** hold the same series for the team to explore. Log each report to `globus.reports[]`.

## Mode 3 — Year coaching

The coach helps a team think through a year's decisions. **The team makes and enters every decision.**
There is no winning recipe: what works depends on the strategy the team chose and on what the other
companies in the industry are doing. So the coach explains trade-offs and has the team **test each
move in the simulator's projections** before keeping it.

## How performance is scored

A team's grade and competitive standing depend on **five KPIs**, tracked in the *Camera & Drone
Journal*:

1. **Earnings per share (EPS)**
2. **Return on equity (ROE)**
3. **Stock price**
4. **Credit rating**
5. **Image rating**

Every proposed move is judged by its projected effect on **all five**, not just profit. A move that
lifts EPS but drops the credit rating or the image rating can lower the overall standing. Treat the
five as equally weighted unless the course instructions give weights.

## The decision areas

| Area | Levers |
|---|---|
| Product design | P/Q (performance/quality) rating, component quality, model availability — cameras and drones |
| Marketing | Price, promotional budgets, warranty period, retailer support — North America, Europe-Africa, Asia-Pacific, Latin America |
| Operations & facilities | Assembly workstations, plant capacity, best-practice training |
| Compensation | Base wages, incentive compensation, fringe benefits for assembly workers |
| Finance & administration | Stock issues and repurchases, dividends, short- and long-term bank loans |

### Step 1 — Anchor to the strategy

Ask (or read from the ledger) which strategy the team has committed to: low-cost, differentiation
(high P/Q), best-cost, or a focused version, by product and region. Every suggestion must serve that
strategy. If the team has none, or is unsure, run `stratos-strategy-interview` first: it
leads the team, question by question, to choose its own strategy from the evidence. A team that drifts between strategies year
to year is "stuck in the middle".

If mode 1 has been run on the `cameras` or `drones` analogue, use its Five Forces and KSFs as context
for which levers matter. If mode 2 has been run this year, start from its groups, white space and moves.

### Step 2 — Diagnose last year

The team uploads or pastes last year's results. Read in this order:

1. **Scoreboard and KPIs** — before concluding the team did something wrong, check whether every
   company's score moved the same way. Industry-wide dips happen when the simulated economy shifts.
2. **Competitive Intelligence Report** (older versions call it *Comparative Competitive Efforts*) —
   rivals' prices, features (P/Q, models) and marketing tactics, by region. Review it after every
   round.
3. **Performance highlights** — trends in each KPI against investor expectations.

State the 2-3 gaps that matter most (e.g. "image rating below expectations in Europe-Africa while
marketing spend is above the industry average — the spend is not converting").

### Step 3 — Propose a few small moves

Propose **no more than 3-5 changes** for the year. For each: the decision area, the change, why it
serves the strategy, and the expected effect **on each of the five KPIs**. Then have the team make the
change, read the projected KPIs, and **keep it only if the overall projection improves**.

## Guardrails (check every proposed move)

**Overall**
- **Make incremental changes, not drastic swings** — in pricing, production and quality, and in one
  direction at a time.
- **Do not cut price and advertising at the same time; protect gross margin.** *(Course rule, Week 3.)*
- Never copy numbers from a guide or another class; each industry finds its own price equilibrium.

**Product design**
- R&D and component quality: don't skimp (better components compound into P/Q and image), and don't
  overspend.
- P/Q (0-10 stars) feeds the image rating. A low-quality strategy earns margin but costs image, which
  marketing can partly offset.
- Add or drop models only as part of the strategy, and watch the projected cost per unit.

**Marketing (cameras and drones, by region)**
- All demand levers (retailer support, advertising, promotions, online) have **diminishing returns**:
  don't max them out, and don't cut any to zero unless cash is critical.
- Drones: the discount to third-party online retailers is often run around 10-15% and raised slowly
  *[tutorial rule of thumb]*.
- Warranty raises image and demand and can pay for itself, but test each step (e.g. 120 → 180 days) in
  the projections. Products ship from Taiwan, so delivery cost applies in every region.

**Operations & facilities**
- Best-practice training is a key productivity lever: don't max it, don't zero it.
- **Workstations and capacity vs overtime:** add workstations or capacity to avoid overtime when the
  projections show it is cheaper than paying overtime, and size them to the demand the plan creates.
- **Robotics upgrades:** treat with caution. The savings can require ever-higher compensation each
  year; consider them only with a high-P/Q strategy and a multi-year plan *[tutorial rule of thumb]*.

**Compensation**
- **Stay close to industry averages** on base wages, incentives and benefits unless the strategy or
  performance calls for a deliberate pivot.

**Special contracts** (not available in the early years)
- Bulk bids at a discount, and only some are accepted. Read competitors' prior-year bids; winning at
  too deep a discount can destroy margin.

**Corporate citizenship**
- Programs support the image rating, and some raise ROE. Add them progressively.
- **Never discontinue a working-conditions program once started.**
- Green initiatives are often costly; test them in the projections.

**Finance & administration**
- **Protect the credit rating** first: if a buyback, dividend or loan would lower it, scale it back. A
  lost rating is hard to recover.
- **Match the loan to the need:** short-term loans for temporary cash gaps, long-term loans for capacity
  investments. Keep the cash position at "generate interest income", not overdraft risk.
- Stock buybacks within free cash flow are the safe version; they can lift EPS and the stock price.
  **Borrowing to fund buybacks is high-risk** and only defensible when the return clearly exceeds the
  interest cost and the credit rating holds.
- Issuing new stock dilutes shareholders and EPS; avoid it unless a cash crisis requires it.
- Dividends support the stock price but use cash; test them against the credit rating.

Rules marked *[tutorial rule of thumb]* are heuristics from a public GLO-BUS tutorial, not facts. Say
so when citing them.

## Output

```markdown
## GLO-BUS Year [n] — coaching notes ([company / team])

**Strategy:** [committed strategy, by product and region]
**What last year shows:** 1… 2… 3… (report and figure)

| KPI | Last year | Investor expectation | Gap |
|---|---|---|---|
| EPS · ROE · Stock price · Credit rating · Image rating | | | |

| # | Decision area | Proposed change | Why (strategy link) | Expected effect on the 5 KPIs |
|---|---|---|---|---|

**Guardrail checks:** [any move that touches a guardrail, and how it was resolved]
**Not recommended this year:** [tempting moves that fail a guardrail, and why]
```

For a quick read of where every team sits, run mode 2's `scripts/globus_groups.py` on the CIR.

Log each year's notes to `globus.decisions_log[]` in the ledger (year, strategy, moves, projected and
actual KPI effects) so later years can see what was tried and what worked.

## Rules

- Never enter decisions in GLO-BUS or claim to know the "right" number; the team decides.
- Never give a fixed year-by-year plan. The same move can help in one industry and hurt in another.
- The MGT4850 GLO-BUS instructions and the official GLO-BUS help guides override this skill.
