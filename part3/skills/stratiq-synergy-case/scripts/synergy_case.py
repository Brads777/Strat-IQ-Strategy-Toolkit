#!/usr/bin/env python3
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Copyright (c) 2026 G. Bradley Scheller · Strat-IQ Toolkit · commercial licences: BScheller@ToolsIQ.ai
"""Present value of deal synergies vs the premium paid (Strat-IQ Synergy Case).

Usage: python synergy_case.py synergy-case.csv [--out results.json]
CSV columns: item, type, run_rate, start_year, ramp_years, haircut
  type: cost | revenue | integration | premium | setting
  cost / revenue: annual run-rate value; haircut as fraction (blank = default 0.15 cost, 0.35 revenue)
  revenue synergies are converted to profit with the 'margin' setting (default 0.25)
  integration: one-off cost in run_rate, paid in start_year
  premium: price paid above standalone value, in run_rate (year 0)
  setting rows: item = rate | horizon | margin | tax, value in run_rate
"""
import csv, json, sys

DEFAULT_HAIRCUT = {"cost": 0.15, "revenue": 0.35}


def f(v, d=0.0):
    v = (v or "").strip().replace(",", "").replace("$", "")
    return float(v) if v else d


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cfg = {"rate": 0.10, "horizon": 10, "margin": 0.25, "tax": 0.21}
    lines, integ, premium = [], [], 0.0
    with open(sys.argv[1], newline="", encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            t = (r.get("type") or "").strip().lower()
            if t == "setting":
                cfg[r["item"].strip()] = f(r.get("run_rate"))
            elif t in ("cost", "revenue"):
                hc = f(r.get("haircut"), DEFAULT_HAIRCUT[t])
                lines.append({"item": r["item"], "type": t, "run_rate": f(r.get("run_rate")),
                              "start": int(f(r.get("start_year"), 1)), "ramp": max(1, int(f(r.get("ramp_years"), 1))),
                              "haircut": hc})
            elif t == "integration":
                integ.append((int(f(r.get("start_year"), 1)), f(r.get("run_rate"))))
            elif t == "premium":
                premium += f(r.get("run_rate"))
            elif t:
                sys.exit(f"ERROR: unknown type '{t}'")
    r, H = cfg["rate"], int(cfg["horizon"])
    by_year = {y: 0.0 for y in range(0, H + 1)}
    detail = []
    for ln in lines:
        pv = 0.0
        for y in range(1, H + 1):
            if y < ln["start"]:
                continue
            ramp = min(1.0, (y - ln["start"] + 1) / ln["ramp"])
            v = ln["run_rate"] * ramp * (1 - ln["haircut"])
            if ln["type"] == "revenue":
                v *= cfg["margin"]
            v *= (1 - cfg["tax"])
            by_year[y] += v
            pv += v / (1 + r) ** y
        detail.append({**ln, "pv_after_haircut_and_tax": pv})
    integ_pv = sum(c * (1 - cfg["tax"]) / (1 + r) ** y for y, c in integ)
    gross = sum(d["pv_after_haircut_and_tax"] for d in detail)
    net = gross - integ_pv
    out = {"settings": cfg, "lines": detail, "pv_synergies": gross, "pv_integration_cost": integ_pv,
           "pv_net_synergies": net, "premium": premium, "value_created_for_buyer": net - premium,
           "covers_premium": net >= premium,
           "share_from_revenue_synergies": (sum(d["pv_after_haircut_and_tax"] for d in detail if d["type"] == "revenue") / gross) if gross else None}
    out["in_words"] = (f"Net synergies are worth {net:,.0f} against a premium of {premium:,.0f}: the deal "
                       f"{'creates' if net >= premium else 'destroys'} {abs(net - premium):,.0f} for the buyer.")
    txt = json.dumps(out, indent=2, default=lambda x: round(x, 2))
    if "--out" in sys.argv:
        open(sys.argv[sys.argv.index("--out") + 1], "w").write(txt)
    print(txt)


if __name__ == "__main__":
    main()
