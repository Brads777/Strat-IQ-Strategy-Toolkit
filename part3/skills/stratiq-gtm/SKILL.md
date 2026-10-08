---
name: stratiq-gtm
description: "Strat-IQ Go-to-Market (optional case-memo Exhibit T). Turns the chosen strategy into how the firm wins its first customers and then the next: one named beachhead segment, the ideal customer profile, a value proposition against a named alternative, price and packaging from Pricing, channels and sales motion, a funnel worked backwards from the Business Case volume to spend and CAC (gtm_funnel.py), and launch phases with gates. CAC must fit Unit Economics. Use for 'go-to-market', 'GTM', 'launch plan', 'beachhead', 'ideal customer profile', 'how do we win customers', 'channel strategy', or 'Exhibit T'."
license: CC-BY-NC-4.0 AND PolyForm-Noncommercial-1.0.0
---
# ©2026 Brad Scheller

# Go-to-Market (Strat-IQ · Part 3 · Plan · Exhibit T)

**Runs:** after the Stress Test, once an option is chosen. **Reads:** `strategy_layer.options`,
`business_case[]`, `pricing`, `company_layer.internal.unit_economics`, `industry_layer.ksf[]`,
`company_layer.internal.vrio`, `competitors[]`. **Writes:** `strategy_layer.gtm`. **Feeds:**
Initiative Prioritizer, Execution Roadmap, Value Realization, Pitch.

A strategy says **where** to compete. Go-to-market says **how** the firm wins the first customers there,
then the next ones, at a cost the business case can carry.

## The seven steps

1. **Beachhead** — **one** segment, named and sized: reachable through one channel, with an urgent
   need the firm meets better than rivals. Not "everyone who wants an EV"; rather "urban fleet
   operators in Germany replacing diesel vans by 2027". Size it from the Industry Overview segments.
2. **Ideal customer profile (ICP)** — who uses it, who signs, who can block; what they use today; the
   trigger that makes them buy now; what disqualifies a prospect.
3. **Value proposition** — against a **named alternative** (the incumbent product, the status quo, a
   substitute from Five Forces), in one sentence: *for [ICP] who [need], [offer] gives [benefit] unlike
   [alternative], because [proof]*. The proof cites a KSF where the firm leads or a VRIO-supported
   capability.
4. **Price and packaging** — from Pricing: the price point, tiers or bundles, and what is in each.
5. **Channels and sales motion** — online/self-serve, dealers or retailers, direct or fleet sales,
   partners. For each channel: why this ICP buys there and the motion (self-serve, inside sales,
   field sales).
6. **Funnel and CAC** — work **backwards** from the Business Case volume: target customers ÷
   conversion rates per stage = the top-of-funnel volume each channel needs, × cost per lead and
   per-sale cost = spend and **CAC** per channel. Fill `templates/gtm-funnel.csv` and run
   `scripts/gtm_funnel.py`. It compares CAC with contribution per customer from Unit Economics and
   flags any channel where CAC payback is too long.
7. **Launch phases** — beachhead → adjacent segment → scale, each with an entry gate (e.g. "CAC
   payback under 12 months for two quarters before opening the second country").

## Two rules

- **One beachhead, named.** A GTM that targets everyone targets no one.
- **CAC must fit Unit Economics.** If CAC exceeds what contribution can repay, the plan breaks the
  business case: change the channel, the ICP or the price, or say the option fails.

## Output

```markdown
### T. Go-to-Market Plan
**Beachhead:** … (size, source) · **ICP:** … · **Value proposition:** …
| Channel | Motion | Customers | Conversion path | Spend | CAC | CAC / contribution | Payback (months) |
|---|---|---|---|---|---|---|---|
**Launch phases and gates:** …
**Impact Summary — Go-to-Market Plan**
> _[Student writes this summary.]_
```

## Rules

- Every conversion rate and cost per lead is cited or marked `[assumption]` (and listed for the
  Stress Test).
- In a graded case, the beachhead and ICP are proposals marked `SUGGESTED` until the student confirms.
