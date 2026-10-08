# Ledger schema and P&L line taxonomy

One ledger per industry scope. Every stage reads it on entry and writes its own section on exit.
The industry layer and the company layer are separate keys so a base-company swap rewrites only
`company_layer`.

## P&L line taxonomy — used by every stage

Every PESTEL finding, driver and force carries a `pl_line` and a `direction`. This is what turns a
list of macro trends into an argument about margins.

| `pl_line` | Covers | Typical transmission |
|---|---|---|
| `revenue.price` | Realised price, discounting, take rate | Buyer power, price wars, regulation of pricing |
| `revenue.volume` | Units, customers, usage | Demand shifts, demographics, substitutes |
| `revenue.mix` | Product, segment or geographic mix | Trading down, premiumisation, market access |
| `cogs.inputs` | Materials, commodities, components, energy | Supplier power, commodity spikes, tariffs |
| `cogs.labor` | Direct labour and conversion cost | Wage law, unions, automation |
| `opex.sga` | Selling, marketing, general and admin | Customer acquisition cost, compliance overhead |
| `opex.rnd` | R&D and product development | Technology races, certification cycles |
| `capex` | Plant, fleet, retooling, platform build | Transition mandates, capacity races |
| `working_capital` | Inventory, receivables, payables | Supply-chain disruption, payment terms |
| `financing` | Interest, FX translation, cost of capital | Rate cycles, currency devaluation, capital rules |
| `tax_and_levies` | Tariffs paid, carbon price, sugar taxes, royalties | Fiscal and environmental policy |

`direction` is `+` (improves profit), `-` (erodes profit) or `±` (depends on the firm's response —
say which response). A finding that touches no P&L line is context, not a finding; keep it out of
the table.

## Schema

Values below are synthetic.

```json
{
  "scope_id": "global-confectionery-2026",
  "asof": "2026-09-29",
  "evidence_mode": "web",                      // web | user-supplied
  "scoring": "public-screen",                  // api | public-screen
  "checkpoint": "S3",                          // last completed stage

  "scope": {
    "industry": "Global packaged confectionery",
    "boundary_note": "Includes chocolate and sugar confectionery; excludes bakery",
    "geography": "Global",
    "horizon": "2026-2029",
    "scenario": "Academic",                    // Academic | Simulation | Enterprise
    "competitor_set": ["Firm A", "Firm B", "Firm C", "Private-label"]
  },

  "evidence": [ {
    "id": "E001",
    "claim": "Cocoa futures rose sharply over the period",
    "kind": "figure",                          // observation | figure | policy | forecast
    "source": { "name": "…", "url": "…", "published": "2026-01-15", "tier": "primary" },
    "confidence": "high",                      // high | medium | low
    "volatility": "fast",                      // stable | seasonal | fast  -> re-check cadence
    "expires": "2026-12-31"
  } ],

  "ci": {
    "pestel_seeds": [ {
      "dimension": "L", "kind": "risk_factor",  // risk_factor (10-K Item 1A) | mdna_trend (Item 7)
      "text": "…", "pl_line": "revenue.volume",
      "shared": true, "firms": ["Firm A", "Firm C", "Firm D"], "evidence": ["E017"]
    } ]
  },

  "industry_layer": {
    "overview": {                              // written by stratiq-industry-overview
      "mode": "profile",                       // profile | final
      "scope": { "definition": "…", "in": [], "out": [], "codes": "NAICS 336110" },
      "market_size": [ { "value": "…", "unit": "USD bn", "year": 2025, "publisher": "…",
                         "definition": "…", "matches_scope": true, "evidence": ["E040"] } ],
      "growth": { "historical_cagr": "…", "period": "2020-2025",
                  "forecasts": [ { "cagr": "…", "to_year": 2030, "publisher": "…", "published": "2026-03-01" } ] },
      "segments": [ { "name": "…", "share": "…", "growth": "…", "buyers": "…", "evidence": [] } ],
      "economics": { "value_chain": "…", "margin_pool": "…", "gross_margin_range": "…",
                     "capital_intensity": "high", "evidence": [] },   // margin range filled by CI
      "timeline": [ { "year": 2023, "event": "…", "why_it_mattered": "…", "evidence": ["E041"] } ],
      "players": { "leaders": [ { "name": "…", "share": "…" } ], "meaningful_players": 12,
                   "top4_share": "…", "hhi": null, "direction": "consolidating",
                   "rivalry_score": null, "evidence": [] },          // rivalry added in finalise mode
      "lifecycle": { "stage": "shakeout", "by_segment": {}, "evidence": [], "implication": "…" },
      "trends": [ { "text": "…", "driver_id": null, "preliminary": true } ],
      "roadmap": "…"
    },
    "pestel": [ {
      "id": "P3", "dimension": "E", "finding": "…",
      "velocity": "accelerating",              // slow | accelerating | exponential
      "impact": "high", "certainty": "high",
      "quadrant": "strategic-focus",           // strategic-focus | scenario-plan | monitor | drop
      "pl_line": "cogs.inputs", "direction": "-",
      "transmission": "…", "evidence": ["E001"]
    } ],
    "forces": [ {
      "force": "suppliers",                    // rivalry | entrants | suppliers | buyers | substitutes
      "score_now": 4, "score_horizon": 5,      // 1 weak ... 5 strong; horizon = after drivers act
      "rationale": "…", "pl_line": "cogs.inputs",
      "evidence": ["E001"], "moved_by": ["D2"]
    } ],
    "complementors": "…",
    "attractiveness": { "now": 2.4, "horizon": 2.0, "method": "public-screen" },
    "profit_pool": "Margin is migrating upstream to …",
    "drivers": [ {
      "id": "D2", "name": "…", "from_pestel": ["P3"],
      "transmission": "…", "pl_line": "cogs.inputs",
      "profit_pool": "compressing",            // expanding | compressing | redistributing
      "forces_moved": ["suppliers"], "evidence": ["E001"]
    } ],
    "ksf": [ {
      "id": "K1", "name": "…",
      "from_forces": ["suppliers"], "from_drivers": ["D2"],
      "kpi": "…", "benchmark": "…", "weight": 0.20,
      "status": "emerging"                     // current | emerging | fading
    } ],
    "vector_shortlist": [ {
      "vector_id": 1, "name": "…", "from_ksf": ["K1"],
      "dimension": 1, "correlation_group": "cost-lifecycle", "screen_notes": "…"
    } ],
    "monitor": [ { "variable": "…", "trigger": "…", "response": "…", "evidence": ["E001"] } ]
  },

  "competitors": [ {
    "name": "Firm A",
    "ownership": "public",                     // public | private | state-owned
    "financials": { "fiscal_year": "FY2025", "revenue": "…", "gross_margin": "…",
                    "operating_margin": "…", "currency": "USD", "evidence": [] },
    "signals": [ { "kind": "hiring", "observation": "…", "inference": "…", "evidence": [] } ],
    "apparent_strategy": "…",
    "moat": { "network": "weak", "switching": "moderate", "scale": "strong", "intangibles": "moderate" },
    "ksf_scores": { "K1": { "score": 4, "evidence": [] } },
    "positions": { "v16": 0.7, "v1": 0.4, "v14": 0.2 }
  } ],

  "company_layer": {
    "focal_firm": "Firm A",
    "ksf_view": {                              // KSF Tier 2 — re-weighted for this firm's strategy
      "strategy": "focused differentiation", "strategic_group": "…", "evidence": [],
      "weights": { "K1": 0.15, "K2": 0.25 },   // same KSFs as Tier 1; sums to 1.00, each <= 0.25
      "csfs": [ { "name": "…", "traces_to": "K2", "kpi": "…" } ],
      "strength_industry": 6.8, "strength_strategy": 7.6
    },
    "roles": {
      "benchmark": 16, "disruption_x": 14, "disruption_y": 1,
      "moat_reinforcer": 6, "adoption_driver": 19
    },
    "s5_conventional": { "axes": [16, 1], "clusters": [ "…" ] },
    "s6_disruption":   { "axes": [14, 1], "whitespace": [ { "at": [0.85, 0.2], "occupied_by": [] } ] },
    "candidates": [ {
      "rank": 1, "at": [0.85, 0.2], "thesis": "…",
      "errc": { "eliminate": [], "reduce": [], "raise": [], "create": [] },
      "evidence": [], "demand": "unpriced", "capability": "UNVALIDATED"
    } ]
  },

  "stale": [],
  "warnings": [ "R3: 9 of 18 findings promoted to drivers" ]
}
```

## Rules

- **Write after every stage.** A failure at S6 must not cost S1-S5.
- **Base-company swap** rewrites `company_layer` and re-reads `competitors[*].positions` from the new
  focal firm's side. It never touches `industry_layer`.
- **Staleness.** When an evidence item passes `expires`, add every dependent id (findings, forces,
  drivers, KSFs) to `stale` and say so on the next hydration. Re-check cadence follows `volatility`:
  fast weekly, seasonal quarterly, stable annually.
- **Source decay is not falsification.** When a URL fails, mark the item `source_moved`, not false.
  Only contradicting evidence makes a claim `broken`.
