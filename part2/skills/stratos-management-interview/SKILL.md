---
name: stratos-management-interview
description: "StratOS Management Interview debrief, the first step for a team. After the team has interviewed management (week 1 for GLO-BUS, or the persona interview for a case), interviews the team one question at a time about what management said and records it: the central problem, the decisions management needs made, the required goals, the questions management needs answered, nine questions every team must answer, the team's own questions, and three to five takeaways the team will hold itself to. Records what management said, never invents answers, and marks anything inferred. Writes the management brief to the team's own ledger and the workbook's Management Interviews sheet; it feeds the memo's Key Issues and Exhibit B, the decision criteria, the Strategy Interview and the GLO-BUS weekly report. Use for 'management interview', 'debrief our interview', 'what did management say', 'start StratOS for our team', or 'Exhibit B'."
license: Apache-2.0
---
# ©2026 Brad Scheller

# Management Interview debrief (StratOS · Step 0 · Start here)

**Runs:** first, before anything else, once the team has interviewed management. Again whenever the team
learns something new from management. **Reads:** the team's interview notes, recording or transcript if
they have one, and the course's interview instructions if pasted. **Writes:**
`company_layer.management_brief` (for a GLO-BUS team, in the team's GLO-BUS ledger). **Feeds:** the
memo's Key Issues section and Exhibit B, Decision Criteria (goals become criteria B1-B5), the Strategy
Interview (the strategy must fit the brief), the GLO-BUS Coach weekly report (position vs the brief),
and the StratOS Workbook's **Management Interviews** sheet.

## The rule that defines this skill

**Record what management said, not what the team hoped they meant.** Claude asks and writes down; it
never fills a blank with a plausible answer. Each answer is marked **Stated** (management said it),
**Implied** (it follows clearly from what they said) or **Our interpretation** (the team's reading). A
question nobody asked is marked **Not asked yet** and becomes a follow-up. The brief stays in the
team's own ledger; it is not shared with other teams.

If the course gives interview instructions or a question list, use it: its questions replace or extend
the nine below, and its wording wins.

## How to run it

One question at a time. Short answers are fine. Read each answer back in one line before moving on,
and ask for the exact words when the team remembers them.

### Part 1. Key issues (the memo's Key Issues section and Exhibit B use the same structure)

1. **Central problem.** "In one sentence, what decision does management need made?"
2. **Decisions** (D1-D5). "Which decisions did management say you have to make, and by when?"
3. **Required goals** (B1-B5). "What goals must you reach? For each one: which measure, what target,
   by when?" Tie GLO-BUS goals to a scored measure (EPS, ROE, stock price, credit rating, image rating)
   where management did.
4. **Questions management needs answered** (Q1-Q5). "What did management want you to answer for them?"

### Part 2. Questions every team must answer (M1-M9)

| # | Area | Question |
|---|---|---|
| M1 | Goals | Which scored measures matter most to management: EPS, ROE, stock price, credit rating or image rating? |
| M2 | Goals | What would management call a successful season, and what would be a failure? |
| M3 | Strategy | What strategy does management favour for cameras, and for drones? Why? |
| M4 | Markets | Are there regions or segments management wants to lead in, or to avoid? |
| M5 | Risk | How much risk will management accept: debt, issuing stock, dividends, the lowest credit rating it will tolerate? |
| M6 | Brand | Are there minimum quality, warranty, image or CSR standards the company must keep? |
| M7 | Operations | What are management's views on capacity, workforce and pay? |
| M8 | Rivals | What does management expect competitors to do? |
| M9 | Decision rights | Which decisions must the team check with management before entering them? |

For a case company, adapt the wording to the case (products, markets, measures), keeping the nine
areas. For each answer record: what management said, their words if remembered, what it means for the
strategy, which decision area or KPI it touches, how sure, and a follow-up question if needed.

### Part 3. The team's own questions (T1-T8)

"What else did you ask, and what did they say?" Record each the same way.

### Part 4. Management brief (K1-K5)

Ask the team to state three to five takeaways they will hold themselves to, each traced to a row
(e.g. "K1: Protect the credit rating; from M5") and how they will check it each round (which number,
which report). Claude may point out a tension between two answers ("M1 puts EPS first, but M5 rules out
debt"); it does not resolve it for them.

## Output

1. Write `company_layer.management_brief`:
   ```json
   { "central_problem": "…", "decisions": [ { "text": "…", "by_when": "…" } ],
     "goals": [ { "id": "B1", "text": "…", "kpi": "EPS", "target": "…", "by_when": "…" } ],
     "questions": [ { "text": "…", "why": "…" } ],
     "answers": [ { "id": "M1", "said": "…", "quote": "…", "meaning": "…", "touches": "EPS", "confidence": "Stated", "follow_up": "" } ],
     "team_questions": [ { "area": "…", "question": "…", "said": "…", "confidence": "Implied" } ],
     "takeaways": [ { "text": "…", "from": "M5", "check": "Credit rating each round" } ],
     "interviewed_on": "…", "source": "GLO-BUS | case" }
   ```
2. Show a one-page summary: the central problem, the goals (B1-B5), the takeaways, the open follow-ups,
   and how complete it is (M1-M9 answered).
3. Offer: the StratOS Workbook (the **Management Interviews** sheet fills from the brief), then the next
   step: for GLO-BUS, the Strategy Interview; for a case, Part 1.

## Where it is used later

- **Case memo:** Key Issues and Exhibit B (central problem, management questions, required goals) come
  straight from Part 1. The student writes them in their own words.
- **Decision Criteria:** each required goal becomes a criterion tied to it (B1-B5).
- **Strategy Interview:** checks the chosen strategy against M3-M6 and the takeaways, and asks the team
  to explain any departure.
- **GLO-BUS weekly report:** run with `--ledger`, it compares each round's results with the goals and
  takeaways ("management said protect the credit rating; it fell to B+").

## Rules

- Never invent an answer, a quote or a target. Blank is better than plausible.
- Label every answer's confidence. Keep management's words and the team's reading separate.
- Feedback, not decisions: Claude may point out gaps and tensions; the team decides what they mean.
- The brief belongs to the team. Do not compare it with, or copy it to, other teams.
