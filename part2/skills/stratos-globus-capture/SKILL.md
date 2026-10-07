---
name: stratos-globus-capture
description: "StratOS GLO-BUS Capture. After a team signs in to GLO-BUS themselves in their own Chrome, walks the site with Claude in Chrome in read-only mode and captures one year: the team's own decision screens and projections, and the class-wide reports the team can see (scoreboard, Competitive Intelligence Report, Camera & Drone Journal, performance highlights). Saves the page text and screenshots into one capture file, checks it for missing screens, and hands it to the GLO-BUS Coach, which names the strategy the inputs reveal and gives general lessons (feedback, not recommendations). Never handles passwords and never changes or submits a decision. Also accepts uploaded screenshots or PDFs. Also checks entered decisions against the team's Decision Planner. Use for 'capture GLO-BUS', 'screenshot our GLO-BUS year', 'check our entries against the plan', or 'review our whole GLO-BUS year'."
license: Apache-2.0
---
# ©2026 Brad Scheller

# GLO-BUS Capture (StratOS)

Collects everything the GLO-BUS Coach needs to comment on a whole year, so a team does not have to
copy figures by hand. **Read-only, in the team's own browser, after the team signs in.**

The MGT4850 GLO-BUS instructions and the GLO-BUS terms of use override this skill. If the course or
GLO-BUS does not allow automated browsing, use the upload route (below) instead.

## Hard rules

1. **Never handle credentials.** Do not ask for, type, store or repeat a GLO-BUS username, password,
   access code or SSO login. If a sign-in page appears at any point, stop and ask the student to sign
   in, then continue when they say so.
2. **Read-only.** Click only navigation: menu links, tabs, region or product selectors, report and
   year selectors, and "next page". **Never** click Save, Submit, Enter, Update, Apply, Accept, Confirm,
   Reset or any button that records a decision; never type into a decision field; never change a
   dropdown on a decision screen. If a dialog asks about unsaved changes, choose the option that leaves
   without saving, and tell the student.
3. **Only what this team can already see.** Their own company's screens, and the class-wide reports
   GLO-BUS shows every company. Never try other teams' logins, instructor pages, or URLs the menus do
   not offer.
4. **Go at a human pace.** One page at a time, waiting for each to load. No bulk downloading, no
   repeated reloads.
5. **Everything stays the team's.** The capture file is offered to the team only.

## Before starting

- **Claude in Chrome must be installed and connected** in the student's Chrome. Load the
  `claude-in-chrome` skill and call `tabs_context_mcp` first. If the extension is not available, use
  the **upload route**.
- Ask which **year** to capture (e.g. Year 6 results, or Year 7 decisions before the deadline) and the
  team's **company letter**.
- Ask the student to open GLO-BUS in a Chrome tab and **sign in themselves**, then say "ready". Work in
  that tab; do not open GLO-BUS in a new one unless the student asks.

## Step 1 — Map the menus

Read the page (`read_page` or `find`) to list the site's menus as they actually appear. GLO-BUS menu
names change between versions, so **match by meaning, not by exact label**, against the checklist in
`references/capture-checklist.md`. Show the student the list of screens you plan to capture, marked
`found` or `not found`, and wait for "go".

## Step 2 — Capture each screen

For each screen on the confirmed list:

1. Navigate to it with menu clicks only.
2. Capture the **page text** (`get_page_text`). Text is the record: numbers are copied exactly, never
   read off a picture.
3. Take a **screenshot** for layout, charts and anything the text misses. If a table scrolls, capture
   each part.
4. For screens split by product (cameras, drones) or region (North America, Europe-Africa,
   Asia-Pacific, Latin America), capture **every** combination, switching only the view selector.
5. Add an entry to the capture file (format below), with the URL path, the time, and any warning
   (e.g. "table truncated", "chart only, no numbers").

After every five screens, tell the student in one line what has been captured so far.

## Step 3 — Save and check

With code execution, write the capture to `globus-capture-<company>-Y<year>.json`:

```json
{ "company": "C", "year": 6, "captured_at": "2026-10-06T14:05", "source": "chrome",
  "pages": [ { "id": "cir-cameras-na", "group": "class-report", "title": "Competitive Intelligence Report — Cameras — North America",
               "url_path": "/…", "text": "…", "screenshot": "cir-cameras-na.png", "warnings": [] } ],
  "decisions": { "mkt.camera.na.price": 249, "mkt.camera.na.ads": 6800, "comp.base": 21500 },
  "cir_rows": [ { "company": "A", "product": "camera", "region": "Global", "price": 279, "pq": 4.2, "share": 14.0, "models": 5 } ],
  "scoreboard_rows": [ { "company": "A", "score": 81, "rank": 2, "eps": 2.05, "roe": 0.152, "stock": 24.9, "credit": "BB", "image": 71 } ],
  "results": { "kpis": { "eps": { "actual": 1.85, "target": 2.00 }, "credit": { "actual": "B+", "target": "BB" } },
               "company": { "score": 78, "rank": 3, "revenue": 412000, "net_profit": 18500, "cash": 14200 },
               "product": { "camera": { "units": 1450, "price": 264, "pq": 4.0, "cost_unit": 182, "op_margin": 0.11,
                                        "ind_price": 276, "ind_pq": 4.0, "ind_cost_unit": 186,
                                        "share": { "na": 12.0, "ea": 11.5, "ap": 12.4, "la": 13.0 } } } } }
```

- **`decisions`**: transcribe the value of every decision field read on the team's own decision
  screens, keyed exactly as in `references/globus-fields.json` (the same keys as the StratOS
  Workbook's GLO-BUS Planner). Copy numbers exactly from the page text; leave out any field you could
  not read rather than guessing.
- **`cir_rows`**: one row per company, product and region from the Competitive Intelligence Report.
- **`scoreboard_rows`**: one row per company from the class scoreboard (public to every team): overall
  score, rank and the scored KPIs. With `cir_rows`, it feeds the workbook's Competition by Year tab and the weekly report's
  contest section. Take rival figures only from these class-wide reports.
- **`results`**: the year's outcomes, keyed as in `references/globus-results.json`: the five scored KPIs
  with investor expectations, company results, and per-product results with market share by region.
  The StratOS Workbook puts every capture on **Season by Year** (each year with its change) and charts it on **KPI Charts**.

Run `scripts/capture_check.py globus-capture-<company>-Y<year>.json`. It compares the pages with the
checklist and lists what is missing or thin. Offer to fetch the missing screens once; then stop.

Give the student the capture file to download and suggest adding it to the Project knowledge, so later
chats (and next year's review) can use it. Offer to rebuild the StratOS Workbook with all the capture
files so far (`stratos-workbook --capture …`): Season by Year, Competition by Year, KPI Charts, and Findings & Questions.

## Step 4 — Hand off to the coach

Invoke `stratos-globus-coach` in **mode 4, full-year review**, with the capture file. The coach names
the strategy the team's inputs reveal and gives general lessons from the inputs and results. It gives
feedback, not specific recommendations.

## Step 5 — Check the entries against the team's plan (optional)

When the team planned the year in the StratOS Workbook's **GLO-BUS Planner** and has now entered its
decisions in GLO-BUS, they can ask "check our GLO-BUS entries against the plan". Capture the decision
screens (Steps 1-3, decision screens only is enough), then run:

```bash
python scripts/plan_check.py StratOS_Workbook.xlsx globus-capture-<company>-Y<year>.json
```

It lists **mismatches** (planned one value, entered another: often a typo), **planned but not seen**
(a decision the plan has but the screens show blank or unchanged), and **entered but not planned**.
Report them in a short table and let the team fix them in GLO-BUS themselves. The check never changes
anything, in the game or in the workbook.

## Upload route (no extension, or automation not allowed)

The student saves the same screens themselves (screenshots, or the site's print-to-PDF) and uploads
them. Read each image or PDF page, transcribe the figures into the same capture format with
`"source": "upload"`, mark any figure you cannot read clearly as `[unclear]` rather than guessing, run
the check, and hand off as above.

## Rules

- Never enter, change or submit a GLO-BUS decision, and never claim a decision has been entered.
- Never handle credentials.
- A missing screen is reported as missing, never filled in from memory or from another team.
