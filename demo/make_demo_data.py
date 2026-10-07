"""Build the StratOS v3 demo kit data files (illustrative data, not research)."""
import csv, json, os, random
D = "/home/claude/repo/demo"
NOTE = ("DEMO DATA. Illustrative figures for screen-recorded demonstrations of StratOS v3. "
        "Not verified research: do not cite in graded work.")

ev = lambda i, t, d="2026-09": {"id": i, "source": t, "date": d, "note": "demo source label; verify before use"}
ledger = {
 "scope_id": "global-ev-demo-2026", "asof": "2026-10-01", "demo": True, "_note": NOTE,
 "scope": {"industry": "Global electric vehicles (passenger BEV and PHEV)", "horizon": "2026-2030",
           "geography": "Global, with the EU as the decision market"},
 "evidence": [ev("E001", "BYD annual report 2025 (demo label)"), ev("E002", "EU countervailing duties on Chinese BEVs (demo label)"),
              ev("E003", "Battery cell price survey 2026 (demo label)"), ev("E004", "Tesla 10-K 2025 risk factors (demo label)"),
              ev("E005", "Volkswagen Group annual report 2025 (demo label)"), ev("E006", "Xiaomi EV launch disclosures (demo label)"),
              ev("E007", "EU charging infrastructure report (demo label)"), ev("E008", "Consumer software-feature survey (demo label)"),
              ev("E009", "Stellantis half-year report 2026 (demo label)"), ev("E010", "BYD vertical integration disclosures (demo label)")],
 "industry_layer": {
  "overview": {"market_units_2026_m": 21, "growth_cagr": 0.14, "note": "demo figures"},
  "pestel": [
   {"id": "P1", "dimension": "E", "finding": "Battery cell prices keep falling", "impact": "high", "certainty": "medium",
    "pl_line": "cogs.inputs", "direction": "+", "evidence": ["E003"]},
   {"id": "P2", "dimension": "P", "finding": "EU tariffs on China-built BEVs", "impact": "high", "certainty": "high",
    "pl_line": "tax_and_levies", "direction": "-", "evidence": ["E002"]},
   {"id": "P3", "dimension": "T", "finding": "Software-defined vehicles shift value to features", "impact": "high",
    "certainty": "medium", "pl_line": "revenue.mix", "direction": "+", "evidence": ["E008"]},
   {"id": "P4", "dimension": "S", "finding": "Range and charging anxiety slow mass-market adoption", "impact": "medium",
    "certainty": "medium", "pl_line": "revenue.volume", "direction": "-", "evidence": ["E007"]},
   {"id": "P5", "dimension": "Env", "finding": "Fleet CO2 targets push OEMs to sell more BEVs", "impact": "medium",
    "certainty": "high", "pl_line": "revenue.volume", "direction": "+", "evidence": ["E005"]},
   {"id": "P6", "dimension": "L", "finding": "Local-content rules for EU incentives", "impact": "medium", "certainty": "medium",
    "pl_line": "revenue.price", "direction": "-", "evidence": ["E002"]}],
  "forces": [{"force": "rivalry", "score_now": 5, "score_horizon": 5}, {"force": "suppliers", "score_now": 4, "score_horizon": 3},
             {"force": "buyers", "score_now": 3, "score_horizon": 4}, {"force": "entrants", "score_now": 4, "score_horizon": 4},
             {"force": "substitutes", "score_now": 2, "score_horizon": 2}],
  "drivers": [{"id": "D1", "name": "Cell cost curve", "from": ["P1"]}, {"id": "D2", "name": "Trade barriers", "from": ["P2", "P6"]},
              {"id": "D3", "name": "Software value shift", "from": ["P3"]}],
  "ksf": [{"id": "K1", "name": "Battery cost and supply", "weight": 0.30, "from_forces": ["suppliers"], "from_drivers": ["D1"]},
          {"id": "K2", "name": "Software and UX", "weight": 0.25, "from_forces": ["rivalry"], "from_drivers": ["D3"]},
          {"id": "K3", "name": "Local production footprint", "weight": 0.20, "from_drivers": ["D2"]},
          {"id": "K4", "name": "Brand trust in Europe", "weight": 0.15, "from_forces": ["buyers"]},
          {"id": "K5", "name": "Charging and service network", "weight": 0.10, "from_drivers": ["D3"]}],
  "strategic_maps": [{"axes": ["price position", "software depth"],
    "white_space": [{"id": "W1", "space": "Sub-EUR 25k EU compact with good software", "vrio_stamp": "supported",
                     "because": "C1 battery cost (VRIO sustained) funds the price point"},
                    {"id": "W2", "space": "Premium software subscription layer", "vrio_stamp": "gap",
                     "because": "No VRIO-passing software capability; Tesla and Xiaomi lead K2"}]}]},
 "competitors": [
  {"name": "BYD", "ksf_scores": {"K1": {"score": 5}, "K2": {"score": 3}, "K3": {"score": 2}, "K4": {"score": 2}, "K5": {"score": 3}}},
  {"name": "Tesla", "ksf_scores": {"K1": {"score": 4}, "K2": {"score": 5}, "K3": {"score": 4}, "K4": {"score": 3}, "K5": {"score": 5}}},
  {"name": "Volkswagen Group", "ksf_scores": {"K1": {"score": 3}, "K2": {"score": 2}, "K3": {"score": 5}, "K4": {"score": 5}, "K5": {"score": 4}}},
  {"name": "Geely", "ksf_scores": {"K1": {"score": 4}, "K2": {"score": 3}, "K3": {"score": 3}, "K4": {"score": 3}, "K5": {"score": 3}}},
  {"name": "Xiaomi", "ksf_scores": {"K1": {"score": 3}, "K2": {"score": 5}, "K3": {"score": 1}, "K4": {"score": 2}, "K5": {"score": 2}}},
  {"name": "Stellantis", "ksf_scores": {"K1": {"score": 2}, "K2": {"score": 2}, "K3": {"score": 5}, "K4": {"score": 4}, "K5": {"score": 3}}}],
 "company_layer": {
  "focal_firm": "BYD",
  "internal": {
   "resources": [{"id": "R1", "name": "In-house cell and pack plants"}, {"id": "R2", "name": "Scale in China"}],
   "capabilities": [{"id": "C1", "name": "Vertical battery integration"}, {"id": "C2", "name": "Fast model cadence"},
                    {"id": "C3", "name": "In-car software and OTA"}],
   "vrio": [
    {"item": "C1", "v": "yes", "r": "yes", "i": "yes", "o": "yes", "links_ksf": ["K1"], "ksf_weight": 0.30, "evidence": ["E010"]},
    {"item": "C2", "v": "yes", "r": "yes", "i": "no", "o": "yes", "links_ksf": ["K2"], "ksf_weight": 0.25, "evidence": ["E001"]},
    {"item": "C3", "v": "yes", "r": "no", "i": "no", "o": "?", "links_ksf": ["K2"], "ksf_weight": 0.25, "evidence": ["E008"]},
    {"item": "R2", "v": "yes", "r": "yes", "i": "?", "o": "yes", "links_ksf": ["K1"], "ksf_weight": 0.30, "evidence": ["E001"]}],
   "swot": {"strengths": [{"id": "S1", "text": "Lowest cell cost in the industry", "source": ["C1"]},
                          {"id": "S2", "text": "Fast model cadence", "source": ["C2"]}],
            "weaknesses": [{"id": "W1", "text": "Low brand trust in Europe", "source": ["K4"]},
                           {"id": "W2", "text": "Software lags the leaders", "source": ["C3"]}],
            "opportunities": [{"id": "O1", "text": "Affordable EU compact segment is under-served", "source": ["W1"]},
                              {"id": "O2", "text": "Fleet CO2 targets lift BEV demand", "source": ["P5"]}],
            "threats": [{"id": "T1", "text": "EU tariffs on China-built BEVs", "source": ["P2"]},
                        {"id": "T2", "text": "Local-content rules for incentives", "source": ["P6"]}]},
   "tows": [{"id": "ST1", "pairs": ["S1", "T1"], "option": "Build an EU plant to avoid tariffs"},
            {"id": "SO1", "pairs": ["S1", "O1"], "option": "Launch a sub-EUR 25k compact"},
            {"id": "WT1", "pairs": ["W1", "T2"], "option": "Partner with a European OEM for local assembly and brand"}]}},
 "strategy_layer": {
  "strategy_statement": None,
  "options": {"options": [{"name": "A. EU plant"}, {"name": "B. Partner"}, {"name": "0. Do nothing"}]},
  "decision_matrix": {"criteria": [
    {"name": "Profit by 2029", "weight": 5, "goal": "B1", "scores": {"A. EU plant": 4, "B. Partner": 3, "0. Do nothing": 1}},
    {"name": "Avoids tariffs", "weight": 4, "goal": "B2", "scores": {"A. EU plant": 5, "B. Partner": 4, "0. Do nothing": 1}},
    {"name": "Capital at risk (low = good)", "weight": 3, "goal": "B1", "scores": {"A. EU plant": 1, "B. Partner": 4, "0. Do nothing": 5}},
    {"name": "Builds EU brand trust", "weight": 3, "goal": "B3", "scores": {"A. EU plant": 3, "B. Partner": 5, "0. Do nothing": 1}}]},
  "business_case": [{"option": "A. EU plant", "inputs": {"rate": 0.10, "tax": 0.21, "wc_pct": 0.05, "years": [
    {"units": 0, "price": 32000, "variable_cost": 20000, "fixed_cost": 0, "capex": 2000000000},
    {"units": 32400, "price": 32000, "variable_cost": 20000, "fixed_cost": 180000000, "capex": 100000000},
    {"units": 64800, "price": 32000, "variable_cost": 20000, "fixed_cost": 180000000, "capex": 100000000},
    {"units": 97200, "price": 32000, "variable_cost": 20000, "fixed_cost": 180000000, "capex": 50000000},
    {"units": 108000, "price": 32000, "variable_cost": 20000, "fixed_cost": 180000000, "capex": 50000000},
    {"units": 108000, "price": 32000, "variable_cost": 20000, "fixed_cost": 180000000, "capex": 50000000}]}}],
  "expected_value": {"table": [
    {"option": "A. EU plant", "p_strong": 0.3, "npv_strong": 620, "p_moderate": 0.5, "npv_moderate": -35, "p_weak": 0.2, "npv_weak": -540},
    {"option": "B. Partner", "p_strong": 0.3, "npv_strong": 260, "p_moderate": 0.5, "npv_moderate": 40, "p_weak": 0.2, "npv_weak": -60},
    {"option": "0. Do nothing", "p_strong": 0.3, "npv_strong": 0, "p_moderate": 0.5, "npv_moderate": 0, "p_weak": 0.2, "npv_weak": 0}],
    "units": "$M",
    "pilot": {"name": "12-month EU import test of the compact", "cost": 25,
              "likelihoods": {"strong": [0.80, 0.20], "moderate": [0.50, 0.50], "weak": [0.15, 0.85]}}},
  "risk_analysis": {"ranges": {"price": [-0.08, 0.0, 0.04], "units": [-0.20, 0.0, 0.15], "variable_cost": [-0.05, 0.0, 0.08],
                               "fixed_cost": [-0.05, 0.0, 0.10], "capex": [-0.05, 0.0, 0.20], "rate": [0.09, 0.10, 0.12]}},
  "scorecard": {
   "objectives": [{"id": "F1", "perspective": "financial", "objective": "Profitable EU growth"},
                  {"id": "C1", "perspective": "customer", "objective": "Value choice below EUR 30k"},
                  {"id": "I1", "perspective": "internal", "objective": "Local cell supply"},
                  {"id": "L1", "perspective": "learning", "objective": "EU plant workforce"}],
   "links": [{"from": "C1", "to": "F1"}, {"from": "I1", "to": "C1"}, {"from": "L1", "to": "I1"}],
   "measures": [{"objective": "F1", "measure": "EU operating margin", "type": "Lagging", "target": 0.08, "actual": 0.06, "owner": "CFO"},
                {"objective": "C1", "measure": "EU registrations (000s)", "type": "Lagging", "target": 90, "actual": 74, "owner": "CMO"},
                {"objective": "I1", "measure": "Local cell share", "type": "Leading", "target": 0.5, "actual": 0.55, "owner": "COO"},
                {"objective": "L1", "measure": "Trained line staff", "type": "Leading", "target": 1200, "actual": 900, "owner": "CHRO"}]}},
 "globus": {"company": "C", "strategy": {"camera": "Best-cost", "drone": "Focused differentiation"},
            "plans": {"8": {"strategy.camera": "Best-cost", "strategy.drone": "Focused differentiation",
                            "mkt.camera.na.price": 239, "mkt.camera.na.ads": 6800, "mkt.camera.ea.price": 262,
                            "mkt.camera.ea.ads": 6200, "comp.base": 22000}}}}
json.dump(ledger, open(f"{D}/strategy-ledger-ev-demo.json", "w"), indent=1)

# CSV inputs for the Part 3 scripts
bc = ledger["strategy_layer"]["business_case"][0]["inputs"]
with open(f"{D}/business-case-demo.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["year", "units", "price", "variable_cost", "fixed_cost", "capex"])
    for k in ("rate", "tax", "wc_pct"): w.writerow([k, bc[k], "", "", "", ""])
    w.writerow(["terminal_growth", "", "", "", "", ""])
    for i, y in enumerate(bc["years"]): w.writerow([i, y["units"], y["price"], y["variable_cost"], y["fixed_cost"], y["capex"]])
with open(f"{D}/risk-ranges-demo.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["driver", "low", "likely", "high"])
    for k, (a, b, c) in ledger["strategy_layer"]["risk_analysis"]["ranges"].items():
        if k == "rate": w.writerow([k, a, b, c])
        else: w.writerow([k, f"{a:.0%}", f"{b:.0%}", f"{c:.0%}"])
with open(f"{D}/expected-value-demo.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["option", "scenario", "probability", "npv"])
    for o in ledger["strategy_layer"]["expected_value"]["table"]:
        for s in ("strong", "moderate", "weak"): w.writerow([o["option"], s, int(o["p_" + s] * 100), o["npv_" + s]])
with open(f"{D}/pilot-demo.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["scenario", "positive", "negative"])
    for s, (a, b) in ledger["strategy_layer"]["expected_value"]["pilot"]["likelihoods"].items():
        w.writerow([s, f"{a:.0%}", f"{b:.0%}"])

# GLO-BUS CIR (8 companies, cameras and drones, 4 regions)
def make_cir(seed, drift):
  random.seed(seed)
  rows = []
  for co, (_, pm, qm) in prof.items():
    pm = pm * drift.get(co, (1, 1))[0]; qm = qm * drift.get(co, (1, 1))[1]
    for prod, (bp, bq, bads) in base.items():
        for reg in ("NA", "EA", "AP", "LA"):
            rf = {"NA": 1.03, "EA": 1.02, "AP": 0.97, "LA": 0.95}[reg]
            pmx = pm if not (co == "C" and prod == "drone") else 1.10
            qmx = qm if not (co == "C" and prod == "drone") else 1.12
            price = round(bp * pmx * rf * random.uniform(0.98, 1.02))
            pq = round(bq * qmx * random.uniform(0.97, 1.03), 1)
            share = round(12.5 * (qmx / pmx) ** 3 * random.uniform(0.85, 1.15), 1)
            rows.append({"company": co, "product": prod, "region": reg, "price": price, "pq": pq,
                         "models": random.choice([4, 5, 5, 6]), "ads": round(bads * random.uniform(0.7, 1.3) / 100) * 100,
                         "support": random.choice([3, 4, 5]), "warranty": random.choice([90, 90, 120, 180]), "share": share})
  for prod in base:
    for reg in ("NA", "EA", "AP", "LA"):
        g = [r for r in rows if r["product"] == prod and r["region"] == reg]
        t = sum(r["share"] for r in g)
        for r in g: r["share"] = round(r["share"] * 100 / t, 1)
  return rows
prof = {"A": ("Differentiation", 1.08, 1.10), "B": ("Low-cost", 0.86, 0.85), "C": ("Best-cost", 0.96, 1.00),
        "D": ("Differentiation", 1.12, 1.05), "E": ("Low-cost", 0.90, 0.88), "F": ("Middle", 1.00, 0.98),
        "G": ("Focused differentiation", 1.18, 1.18), "H": ("Middle", 1.02, 0.96)}
base = {"camera": (270, 4.0, 9000), "drone": (1190, 4.1, 2400)}
rows6 = make_cir(41, {"C": (1.01, 0.98), "F": (0.97, 0.99), "D": (1.04, 1.0)})
rows = make_cir(42, {})
with open(f"{D}/globus/cir-Y6.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows6[0])); w.writeheader(); w.writerows(rows6)
with open(f"{D}/globus/cir-Y7.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
cir_rows = []
for co in prof:
    for prod in base:
        g = [r for r in rows if r["company"] == co and r["product"] == prod]
        cir_rows.append({"company": co, "product": prod, "price": round(sum(r["price"] for r in g) / 4),
                         "pq": round(sum(r["pq"] for r in g) / 4, 1), "share": round(sum(r["share"] for r in g) / 4, 1),
                         "models": g[0]["models"]})

def cap(year, decisions, results=None, cir=None, note="", sb=None):
    c = {"company": "C", "year": year, "demo": True, "_note": NOTE + " " + note, "pages": [], "decisions": decisions}
    if cir: c["cir_rows"] = cir
    if sb: c["scoreboard_rows"] = sb
    if results: c["results"] = results
    return c
y6 = json.load(open("/tmp/claude-0/cap6r.json")); y7 = json.load(open("/tmp/claude-0/cap7r.json"))
SB = {6: {"A": (81, 2.05, .152, 24.9, "BB", 71), "B": (70, 1.52, .121, 19.0, "B", 60), "C": (78, 1.85, .142, 22.4, "B+", 68),
          "D": (83, 2.15, .158, 26.0, "BB", 74), "E": (66, 1.31, .110, 17.2, "B-", 58), "F": (74, 1.70, .133, 21.0, "B+", 64),
          "G": (77, 1.92, .141, 23.1, "BB-", 72), "H": (69, 1.45, .118, 18.4, "B", 62)},
      7: {"A": (83, 2.18, .160, 26.8, "BB", 72), "B": (72, 1.60, .126, 20.1, "B+", 61), "C": (84, 2.10, .155, 26.1, "BB-", 71),
          "D": (86, 2.31, .166, 28.3, "BB+", 75), "E": (63, 1.20, .101, 16.0, "B-", 57), "F": (75, 1.76, .137, 21.9, "B+", 65),
          "G": (80, 2.02, .147, 24.6, "BB-", 73), "H": (67, 1.40, .114, 17.7, "B", 61)}}
def scoreboard(y):
    d = SB[y]; ranked = sorted(d, key=lambda k: -d[k][0])
    return [{"company": k, "score": v[0], "rank": ranked.index(k) + 1, "eps": v[1], "roe": v[2], "stock": v[3],
             "credit": v[4], "image": v[5]} for k, v in d.items()]
y6["decisions"]["strategy.drone"] = "Focused differentiation"; y7["decisions"]["strategy.drone"] = "Focused differentiation"
json.dump(cap(6, y6["decisions"], y6["results"], rows6, sb=scoreboard(6)), open(f"{D}/globus/globus-capture-C-Y6.json", "w"), indent=1)
json.dump(cap(7, y7["decisions"], y7["results"], rows, sb=scoreboard(7)), open(f"{D}/globus/globus-capture-C-Y7.json", "w"), indent=1)
d8 = dict(ledger["globus"]["plans"]["8"]); d8["mkt.camera.na.price"] = 293  # the typo: 239 planned, 293 entered
json.dump(cap(8, d8, note="Year 8 decisions as entered, before the round is submitted. Contains one deliberate typo."),
          open(f"{D}/globus/globus-capture-C-Y8-entered.json", "w"), indent=1)
print("ok", len(rows))
