# Sources and licences

The Strat-IQ skills are original text by Brad Scheller (©2026). They synthesise methods from the
sources below. No text was copied from a non-commercial source. Methods and ideas are not
copyrightable; attribution is given anyway.

| Source | Licence | Used in | What was taken |
|---|---|---|---|
| Brad Scheller — 36-vector library (.docx), agent definitions, threat-allocation skill, group-map artifact, build plan | This repo (PolyForm NC / CC BY-NC) | all | Vector catalog (verbatim), pairing heuristic, five vector roles, transmission mechanism, velocity, CSF→KPI matrix, chain rules R1-R7, ledger, Mirage Trap. **Not included:** the W-B-A-F-D, P-E-F, SFI and SCE algorithms, which stay private behind the Strat-IQ scoring API |
| Brad Scheller — Industry Strategy Toolkit drafts (2026-09-30) | This repo (PolyForm NC / CC BY-NC) | competitor-intel, ksf, orchestrator | `score_ksf.py`, KSF three tests and anchor scale, OpenBB MCP guide, financial-metric set and normalisation checklist, run brief, report outline, cross-stage consistency check |
| [anthropics/financial-services-plugins](https://github.com/anthropics/financial-services-plugins) — `competitive-analysis`, `comps-analysis` | Apache-2.0 | competitor-intel, exec-deck | Industry-defining metrics first, source priority order, data-comparability rules, moat rating; deck standards (insight titles, real chart objects, typography, quantified signposts) |
| [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) — `competitive-brief`, sales `competitive-intelligence` | Apache-2.0 | competitor-intel | Reviewed; overlaps the above |
| [DogInfantry/claude-skill-management-consultant-B1](https://github.com/DogInfantry/claude-skill-management-consultant-B1) — `competitive-intelligence` | Apache-2.0 | competitor-intel, mapping | Signals-for-intent (hiring, patents, reviews), apparent strategy vs stated, likely responses, customer-criteria axes |
| [Ericyoung-183/alpha-insights](https://github.com/Ericyoung-183/alpha-insights) — `pestel`, `porters_five_forces` | MIT | pestel, five-forces | Impact × certainty matrix, cross-dimension chains, monitor variables, 1-5 force scoring, barrier quantification, evidence ledger idea |
| [phuryn/pm-skills](https://github.com/phuryn/pm-skills) — `pestle-analysis`, `porters-five-forces`, `competitor-analysis` | MIT | pestel, five-forces, ksf | Force high/low condition lists, KSFs in market overview |
| [ironyjk/strategy-frameworks](https://github.com/ironyjk/strategy-frameworks) — `porter`, `swot-pestel`, `blue-ocean` | MIT | five-forces, mapping | Complementors (Porter 2008), strategy canvas, ERRC, Six Paths, blue-ocean idea test |
| Brad Scheller — internal strategy suite and internal diagnostician drafts (2026-09-23) | This repo (PolyForm NC / CC BY-NC) | value-chain, resources-capabilities, vrio, swot | Value-cost gap per activity (value trap, differentiating engine), the VRIO reality check and competence trap, TOWS as operational options. **Not included:** the SFI algorithm; the public skills use a KSF link check instead |
| [ironyjk/strategy-frameworks](https://github.com/ironyjk/strategy-frameworks) — `rbv`, `wardley`, `swot-pestel` | MIT | resources-capabilities, vrio, value-chain, swot | Resource types, the unexploited-advantage row of the VRIO ladder, the three core-competence tests, the four evolution stages, the TOWS cell definitions |
| [yoichiojima-2/consultant](https://github.com/yoichiojima-2/consultant) | MIT | orchestrator | Answer-first (pyramid) synthesis |
| [deanpeters/Product-Manager-Skills](https://github.com/deanpeters/Product-Manager-Skills) — `pestel-analysis`, `pestel-delta-monitor`, `porters-five-forces` | CC BY-NC-SA 4.0 | ideas only | Broken-assumptions-first delta, materiality rule, do-not-invent list, AI as named substitute, profit-pool close. **No text copied** — NC-SA is non-commercial and viral. |

Driving-force categories follow the standard strategy-textbook treatment of industry driving forces.

The GLO-BUS Coach's rules of thumb marked *[tutorial rule of thumb]* summarise ideas (not text) from a
public tutorial, "The ULTIMATE Glo Bus Business Strategy Game (BSG) Guide" (MegaMilez, YouTube). They
are checked against the course's GLO-BUS overview. GLO-BUS is a product of GLO-BUS Software, Inc.; this
toolkit is not affiliated with it.

## Data sources referenced (not bundled)

- SEC EDGAR — public, free
- [dgunning/edgartools](https://github.com/dgunning/edgartools) — MIT
- [OpenBB-finance/OpenBB](https://github.com/OpenBB-finance/OpenBB) — AGPLv3 (GitHub shows
  NOASSERTION). The skills only *call* an OpenBB MCP server the user runs; no OpenBB code is bundled
  here. If you ever modify OpenBB and offer it over a network (a SaaS), AGPL requires publishing those
  modifications. Check each connected data vendor's terms too.

Verify each repo's current licence before any commercial redistribution.
