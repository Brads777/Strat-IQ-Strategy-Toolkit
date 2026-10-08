---
title: "Strat-IQ v3 live demos: run sheet"
subtitle: "Nine screen-recorded demos for the Strat-IQ v3 process video · MGT4850 · Fall 2026"
---

# Before you record

**Set up once (about 20 minutes)**

1. On the Claude account you will record from, delete any old `stratos-` skills, then upload the 40 zips inside `stratiq-toolkit-skills.zip` (Settings → Capabilities → Skills). You should see 40 Strat-IQ skills on.
2. Create a Claude Project called **Strat-IQ Demo: EV**. Add to its knowledge: `strategy-ledger-ev-demo.json` (this folder) and `industries.json` v2. Keep the GLO-BUS files and the memo draft out of the Project; you attach them during the demo, which looks better on screen.
3. Keep this folder open in File Explorer so you can drag files into the chat.
4. Open `StratIQ_Workbook_demo.xlsx` once in Excel and press F9, so Excel has recalculated it before you record.

**Recording settings**

- 1920 × 1080, browser zoom 110-125% so text is readable on a phone. Hide the bookmarks bar; turn on Do Not Disturb.
- Record each demo as its own clip (Xbox Game Bar: Win + Alt + R, or Clipchamp / OBS). Name the clip with the demo number.
- Claude's wording differs from run to run; the numbers from the scripts do not. If a run wanders, stop and start a new chat in the same Project.
- Trim the waiting time in editing. A 40-second wait becomes 3 seconds with a "fast-forward" cut.

**Demo data.** The ledger, the GLO-BUS files and the memo draft are illustrative demo data, labelled as such in every file. They show what the tools do; they are not research to cite.

| # | Demo | Deck slide | Clip length |
|---|---|---|---|
| 1 | Resume with "Run Strat-IQ" | after Part 1 | 1.5-2 min |
| 2 | Swap the base company | after Part 1 | 1.5-2 min |
| 3 | Which white space can we serve? (VRIO gap) | after Part 2 | 1-1.5 min |
| 4 | Strategy Interview | after Choose | 3-4 min |
| 5 | Business case, risk analysis, expected value and the pilot | after Statistics | 3-4 min |
| 6 | Hostile Q&A drill | after Test and Plan | 2-3 min |
| 7 | Memo Coach on a weak draft | after Track | 2-3 min |
| 8 | GLO-BUS: competitor map and the plan check | after GLO-BUS | 2-3 min |
| 9 | Workbook: change one input, watch it move | after the Workbook | 2-3 min |

# Demo 1. Resume with "Run Strat-IQ"

**Shows:** the ledger carries the work across chats; Strat-IQ checks what is done and continues.

**Setup:** new chat inside the Strat-IQ Demo: EV Project.

**Type:**

```
Run Strat-IQ
```

**You should see:** Strat-IQ finds `strategy-ledger-ev-demo.json` (BYD, global EVs), reports Part 1 and Part 2 complete, and Part 3 partly done (options, decision matrix, business case and expected value exist; the strategy statement is missing). It offers the modes and suggests D, make the strategy work.

**Point at:** "It didn't ask me to start over. It read the ledger, found the gap (no strategy statement yet) and offered to continue from there."

# Demo 2. Swap the base company

**Shows:** Part 1 is about the industry, so it is kept; only the company analysis is redone.

**Type:**

```
Make Xiaomi the base company.
```

**You should see:** Part 1 kept as it is. Part 2 rerun for Xiaomi. On the KSF scorecard Xiaomi scores 5 on Software and UX (K2) but 1 on Local production footprint (K3), so its white space and its SWOT differ from BYD's.

**Point at:** "Same industry, same evidence, different company, different strategy. That's the point of separating Part 1 from Part 2."

**Reset:** start a new chat before Demo 3 so the base company is BYD again.

# Demo 3. Which white space can we actually serve?

**Shows:** VRIO stamps each empty space on the strategic map "supported" or "gap".

**Type:**

```
Which of the white spaces on our strategic map can BYD actually serve?
```

**You should see:** two empty spaces. *Sub-EUR 25k EU compact with good software*: **supported**, because vertical battery integration (C1) passes all four VRIO tests and funds the price point. *Premium software subscription layer*: **gap**, because BYD's in-car software (C3) fails the rarity test and Tesla and Xiaomi lead K2.

**Point at:** "An empty space on a map isn't an opportunity until you can show you have what it takes to win there."

# Demo 4. Strategy Interview

**Shows:** the interview asks one question at a time, shows the evidence, and never picks.

**Type:**

```
Run the Strategy Interview for BYD.
```

**Answers to give on camera** (short, so the clip moves):

- Where is the opportunity? *"The sub-25k compact segment in Europe."*
- Can BYD win there? *"Yes on cost, because of the batteries. Not yet on brand trust."*
- Which generic strategy? *"Best-cost provider: good-enough software at a lower price."*
- What will BYD not do? *"Chase premium software subscriptions."*

**You should see:** each question arrives with the evidence behind it (map, KSFs, VRIO), a fit check against your answer, and at the end a strategy statement in your words, written to the ledger.

**Point at:** "It asked; I chose. If I ask it to pick, it hands the question back."

# Demo 5. Business case, risk analysis, expected value and the pilot

**Shows:** the statistical decision tools: NPV and break-even, a tornado, a Monte Carlo simulation, expected value and a Bayesian pilot check.

**Type, one at a time:**

```
Run the business case for Option A from the ledger, then the risk analysis using the ranges in the ledger.
```

```
Now run expected value for all three options, and tell me whether the 12-month EU import test is worth its $25M cost.
```

**You should see (deterministic):**

| Result | Value |
|---|---|
| Option A NPV / IRR / payback | −$34.5M / 9.5% (hurdle 10%) / 4.2 years |
| Break-even sentence | "The case holds only if revenue beats plan by 0.5%." |
| Tornado, top two bars | Units: −$591M to +$383M. Price: −$632M to +$264M |
| Monte Carlo (10,000 runs, seed 7) | Median −$366M; P10 −$770M; P90 +$50M; NPV below zero 87% of the time |
| Expected NPV | B. Partner $86M; A. EU plant $60.5M; do nothing $0 |
| Maximin / EVPI | Do nothing (never loses) / $120M |
| Flip point | A overtakes B if the chance of weak demand falls below 13.7% |
| Pilot: P(positive) | 52%; after a positive result A leads ($238M vs $136M) |
| Pilot: after a negative result | B leads ($32M vs −$132M for A) |
| EVSI / net of the $25M cost | $53.25M / $28.25M: worth running |

**Point at:** "At plan, the EU plant is close to break-even. But the ranges skew to the downside, so most simulated futures lose money. Expected value prefers the partnership. And the pilot is worth $53M because a positive result would switch the choice to the plant."

# Demo 6. Hostile Q&A drill

**Shows:** practising the defence, scored, one question at a time.

**Type:**

```
Run the hostile Q&A drill on my recommendation: Option B, partner with a European OEM. Ask as the professor.
```

**Answers to give:** answer two questions on camera, one well and one weakly (for example, *"Because it's less risky"*). Then type `score me`.

**You should see:** a question at a time; feedback on each answer naming the exhibit the answer should have cited; a score at the end with the weakest answer flagged.

**Point at:** "It never answers for me. It tells me which exhibit I should have used."

# Demo 7. Memo Coach on a weak draft

**Shows:** the coach finds the gaps the way the memo is graded, and returns questions, not text.

**Setup:** drag `memo-draft-weak.docx` into a new chat.

**Type:**

```
Coach my memo.
```

**You should see these planted problems found** (located by paragraph):

1. The recommendation is in the third paragraph, after a retelling of the company's history.
2. "We believe", "I think", "we feel".
3. Predictions stated as fact: "will grow 40% next year", "will dominate Europe by 2028", with no source.
4. The memo says NPV is +$120M; Exhibit Q-1 says −$34.5M.
5. It recommends A, but the Decision Matrix (M) ranks B first and Expected Value (Q-2) leads with B, and the memo does not explain why.
6. Reasons 1 and 2 are the same reason (cost); reason 3 cites no exhibit.
7. Exhibit B (management questions) is missing.

**Then type:** `Rewrite my recommendation paragraph.` The coach declines and offers the check or the drill instead. Keep this in the clip; it shows the rule.

# Demo 8. GLO-BUS: competitor map and the plan check

**Shows:** strategic groups from the Competitive Intelligence Report, and the typo the plan check catches.

**Part 1. Type, with `globus/cir-Y7.csv` attached:**

```
Analyse this competitor report for company C: strategic groups and white space for cameras and drones.
```

**You should see:** a groups chart per product and region. Company C is the camera **value leader** and share leader in North America, Europe-Africa and Asia-Pacific, but sits in the **low-cost / economy** group in Latin America, so its apparent strategy drifts there. In drones C is a **premium differentiator** in every region; in North America and Latin America the share leader is a low-cost company.

**Part 2. Attach `StratIQ_Workbook_demo.xlsx` and `globus/globus-capture-C-Y8-entered.json`, then type:**

```
Check our Year 8 entries against the plan.
```

**You should see:** 6 decisions match; 1 mismatch: **Price (Cameras, North America): planned $239, entered $293.**

**Point at:** "Two digits swapped. That typo would have priced us out of North America for a year. The check took a minute. Strat-IQ never changed the entry; we fix it ourselves in GLO-BUS."

# Demo 9. Workbook: change one input, watch it move

**Shows:** live formulas, the Risk Analysis sheet, Season by Year and the KPI Charts.

**Type (optional; the prebuilt workbook is in this folder):**

```
Build our Strat-IQ workbook from the ledger with our Year 6 and Year 7 GLO-BUS captures.
```

**In Excel:**

1. **Risk Analysis** sheet. Point at the tornado (Units on top) and *Probability NPV < 0* (about 87%).
2. Change **Units, Low** from −20% to −10%. The Units bar shrinks and the chance of a loss falls. Press F9 to draw the simulation again; the numbers move slightly, which is what a simulation does.
3. **Expected Value** sheet. Change the pilot cost from 25 to 60: the net value turns negative.
4. **Season by Year** tab. Scroll right: each year has its value and its change (▲ ▼). EPS rose from $1.85 to $2.10 but stayed under the investor expectation ($2.00, then $2.15); the credit rating improved from B+ to BB-.
5. **KPI Charts** and **Competition by Year**: the trends in graphs, and every company's score and rank by year.

**Point at:** "Every grey cell is a formula. Change one input and you find out which assumptions really matter."

# Files in this folder

| File | Used in |
|---|---|
| `strategy-ledger-ev-demo.json` | Demos 1-7, 9 (put it in the Project) |
| `business-case-demo.csv`, `risk-ranges-demo.csv`, `expected-value-demo.csv`, `pilot-demo.csv` | Demo 5 (the skills build these from the ledger; the CSVs let you rerun the scripts) |
| `memo-draft-weak.docx` (and `.md`) | Demo 7 |
| `globus/cir-Y7.csv`, `globus/groups-Y7.png` | Demo 8, part 1 |
| `globus/globus-capture-C-Y6.json`, `globus/globus-capture-C-Y7.json` | Demo 9 (Season by Year, Competition by Year, KPI Charts) and the weekly review |
| `globus/globus-capture-C-Y8-entered.json` | Demo 8, part 2 (contains the typo) |
| `StratIQ_Workbook_demo.xlsx` | Demos 8 and 9 |

© 2026 G. Bradley Scheller · Strat-IQ Toolkit
