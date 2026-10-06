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
    "overview": {                              // written by stratos-industry-overview
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
      "evidence": [], "demand": "unpriced",
      "capability": "UNVALIDATED"              // UNVALIDATED | supported | gap  (set by stratos-vrio)
    } ],
    "internal": {                              // Part 2 — the internal analysis: S8, RC, S9, S10
      "evidence_basis": "interview-notes",     // interview-notes | filings | user-supplied
      "value_chain": [ {                       // written by stratos-value-chain
        "id": "A1", "activity": "…", "porter_category": "Service",
        "stage": "custom",                     // commodity | product | custom | genesis
        "sourcing": "in-house",                // in-house | outsourced | mixed
        "cost_share": 0.12, "value_share": 0.35, "gap": 0.23,
        "reading": "differentiating engine",   // differentiating engine | value trap | in balance | no figures
        "moving_to": null, "moved_by": [], "delivers_ksf": ["K2"], "evidence": []
      } ],
      "linkages": [ { "between": ["A1", "A4"], "effect": "…", "evidence": [] } ],
      "resources": [ {                         // written by stratos-resources-capabilities
        "id": "R1", "name": "…", "type": "intangible",   // tangible | intangible | human | organisational
        "measure": "…", "evidence": []
      } ],
      "capabilities": [ {
        "id": "C1", "name": "…", "combines": ["R1", "R3"], "from_activity": ["A1"],
        "performance": "…", "class": "distinctive", "evidence": []   // threshold | distinctive
      } ],
      "core_competencies": [ {
        "capability": "C1", "customer_benefit": "K2", "hard_to_imitate": "…", "extendable": "…",
        "status": "confirmed"                  // candidate | confirmed | removed
      } ],
      "competitive_advantage": { "basis": "differentiation", "mode": "final",   // provisional | final
                                 "confirmed_in_results": true, "evidence": [] },
      "vrio": [ {                              // written by stratos-vrio
        "item": "C1", "v": "yes", "r": "yes", "i": "yes", "o": "yes",          // yes | no | ?
        "barrier": "social complexity",        // history | causal ambiguity | social complexity | legal protection
        "verdict": "Sustained advantage",
        "links_ksf": ["K2"], "ksf_weight": 0.20,
        "reality_check": "Supported",          // Supported | Table stakes | Competence trap
        "method": "public-screen", "evidence": []
      } ],
      "swot": {                                // written by stratos-swot
        "strengths":     [ { "id": "S1", "text": "…", "source": ["C1"] } ],
        "weaknesses":    [ { "id": "W1", "text": "…", "source": ["A3"] } ],
        "opportunities": [ { "id": "O1", "text": "…", "source": ["D2"] } ],
        "threats":       [ { "id": "T1", "text": "…", "source": ["P3"] } ]
      },
      "tows": [ { "id": "SO1", "pairs": ["S1", "O1"], "option": "…" } ],
      "unit_economics": {                      // written by stratos-unit-economics (J-1)
        "unit": "one vehicle", "lines": [ { "line": "ASP", "value": 0, "peer_median": 0,
        "position": "behind", "evidence": [] } ], "break_even": 0, "margin_of_safety": 0.17,
        "ltv_cac": 4.5, "payback_months": 6, "top_driver": "price"
      },
      "full_potential": {                      // written by stratos-full-potential (K-1)
        "drivers": [ { "driver": "variable_cost", "today": 0, "benchmark": 0, "benchmark_source": "peer median",
                       "gap_value": 0, "controllability": "capability-bound", "traces_to": "K3" } ],
        "bridge": { "current": 0, "full_potential": 0 }, "largest_controllable": "price"
      },
      "growth_barriers": {                     // written by stratos-growth-barriers (K-2)
        "binding": "supply", "to_lift": "…", "unlocked": "…",
        "barriers": [ { "barrier": "demand", "status": "slack", "evidence": [] } ]
      },
      "ask_in_interview": [ "…" ]
    }
  },

  "strategy_layer": {                          // Part 3 — written in mode D
    "decisions": [ "How should Firm A compete below $35k by 2029?" ],
    "options": { "scq": {}, "issue_tree": [], "options": [ { "id": "O-A", "name": "…", "route": "partner",
                 "exploits": ["SO1"], "staged_step": "…", "gate": "…", "suggested": false } ],
                 "confirmed_by_user": true },
    "business_case": [ { "option": "O-A", "npv": 0, "irr": 0.095, "payback": 4.2,
                         "break_even_revenue_change": 0.005, "assumptions": [] } ],
    "pricing": {}, "synergy_case": {}, "negotiations": [],
    "expected_value": { "leader": "O-A", "maximin": "O-B", "evpi": 0, "flip_points": {} },
    "chosen_option": "O-A",                    // set by the user, never by Claude
    "stress_test": { "assumptions": [], "war_game": [], "risks": [], "drill": [] },
    "gtm": { "beachhead": "…", "icp": "…", "value_prop": "…", "channels": [], "blended_cac": 0, "phases": [] },
    "initiatives": [ { "id": "I1", "initiative": "…", "traces_to": "GB:supply", "rice": 0, "status": "now" } ],
    "operating_model": {}, "stakeholders": {},
    "roadmap": { "first_100_days": [], "milestones": [], "gates": [] },
    "kpis": [ { "kpi": "…", "traces_to": "K2", "leading": "…", "target": "…", "owner": "…", "trigger": "…" } ],
    "actuals": [], "pitch": {}
  },

  "globus": {                                  // GLO-BUS Coach; kept in its own ledger file
    "company": "C", "strategy": { "cameras": "best-cost", "drones": "differentiation" },
    "cir_log": [ { "year": 6, "groups": {}, "leader": {}, "white_space": [], "moves": [] } ],
    "decisions_log": [ { "year": 7, "moves": [], "projected": {}, "actual": {} } ],
    "captures": [ { "year": 6, "file": "globus-capture-C-Y6.json", "complete": true } ],
    "reviews": [ { "year": 6, "apparent_strategy": { "cameras": "low-cost", "confidence": "clear" }, "observations": [], "lessons": [], "questions": [] } ]
  },

  "stale": [],
  "warnings": [ "R3: 9 of 18 findings promoted to drivers" ]
}
```

## Rules

- **Write after every stage.** A failure at S6 must not cost S1-S5.
- **Base-company swap** rewrites `company_layer` — including `company_layer.internal`, which belongs to
  one firm — and re-reads `competitors[*].positions` from the new focal firm's side. It never touches
  `industry_layer`.
- **Part 1 and Part 2.** Part 1 (external) is complete when `industry_layer` holds the overview,
  PESTEL, forces, drivers and KSFs and `company_layer` holds `ksf_view`, the maps and `candidates`.
  Part 2 (internal) writes `company_layer.internal`. A ledger with no `internal` key is a finished or
  unfinished Part 1, not a broken ledger. `checkpoint` takes the stage ids IO, CI, S1-S6, KSF, S8, UE,
  RC, S9, FP, GB, S10, and for Part 3 OPT, BC, EV, ST, GTM, IP, OM, SM, RM, VR.
- **Part 3** writes only `strategy_layer`. It never edits Parts 1-2, except that Value Realization adds
  actuals as new evidence and marks dependent ids `stale`.
- **Staleness.** When an evidence item passes `expires`, add every dependent id (findings, forces,
  drivers, KSFs) to `stale` and say so on the next hydration. Re-check cadence follows `volatility`:
  fast weekly, seasonal quarterly, stable annually.
- **Source decay is not falsification.** When a URL fails, mark the item `source_moved`, not false.
  Only contradicting evidence makes a claim `broken`.
