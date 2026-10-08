#!/usr/bin/env python3
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Copyright (c) 2026 G. Bradley Scheller · Strat-IQ Toolkit · commercial licences: BScheller@ToolsIQ.ai
"""Tornado sensitivity and Monte Carlo simulation for one business case (Strat-IQ Exhibit Q-3, Risk Analysis).

Usage: python risk_analysis.py business-case.csv risk-ranges.csv [--sims 10000] [--seed 7] [--out risk.json]
risk-ranges.csv columns: driver, low, likely, high
  drivers: price, units, variable_cost, fixed_cost, capex (as % change from plan, e.g. -10%, 0%, 5%)
           rate (as an absolute discount rate, e.g. 0.08, 0.10, 0.13)
  The student sets every range. Claude may suggest ranges marked SUGGESTED; the student confirms them.
Tornado: NPV with each driver at its low and high value, all others at plan, sorted by swing.
Monte Carlo: every driver drawn independently from a triangular(low, likely, high) distribution.
  Independence is an assumption; correlated drivers (e.g. price and units) widen or narrow the real spread.
"""
import csv, json, os, random, statistics, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from business_case import load, npv  # noqa: E402

PCT = ("price", "units", "variable_cost", "fixed_cost", "capex")


def parse(v):
    v = (v or "").strip()
    if v.endswith("%"):
        return float(v[:-1]) / 100
    return float(v)


def load_ranges(path):
    out = {}
    with open(path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            d = (r.get("driver") or "").strip().lower()
            if not d:
                continue
            if d not in PCT + ("rate",):
                sys.exit(f"ERROR: unknown driver '{d}'")
            lo, mid, hi = parse(r["low"]), parse(r["likely"]), parse(r["high"])
            if not lo <= mid <= hi:
                sys.exit(f"ERROR: {d}: need low <= likely <= high")
            out[d] = (lo, mid, hi)
    return out


def case_npv(years, cfg, x):
    """x: dict of % changes for PCT drivers and an absolute 'rate'."""
    out, prev_wc = [], 0.0
    for i, y in enumerate(years):
        units = y["units"] * (1 + x.get("units", 0))
        rev = units * y["price"] * (1 + x.get("price", 0))
        var = units * y["variable_cost"] * (1 + x.get("variable_cost", 0))
        ebit = rev - var - y["fixed_cost"] * (1 + x.get("fixed_cost", 0))
        tax = max(0.0, ebit) * cfg["tax"]
        wc = cfg["wc_pct"] * rev
        cf = ebit - tax - (wc - prev_wc) - y["capex"] * (1 + x.get("capex", 0))
        prev_wc = wc
        if i == len(years) - 1:
            cf += wc
        out.append(cf)
    return npv(out, x.get("rate", cfg["rate"]), years)


def pct(sorted_vals, q):
    k = (len(sorted_vals) - 1) * q
    f = int(k)
    c = min(f + 1, len(sorted_vals) - 1)
    return sorted_vals[f] + (sorted_vals[c] - sorted_vals[f]) * (k - f)


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    years, cfg = load(sys.argv[1])
    rng = load_ranges(sys.argv[2])
    arg = lambda k, d: type(d)(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else d
    sims, seed = arg("--sims", 10000), arg("--seed", 7)

    base_x = {"rate": cfg["rate"]}
    base = case_npv(years, cfg, base_x)
    likely_x = {d: v[1] for d, v in rng.items()}
    likely_x.setdefault("rate", cfg["rate"])

    tornado = []
    for d, (lo, _, hi) in rng.items():
        a = case_npv(years, cfg, {**base_x, d: lo})
        b = case_npv(years, cfg, {**base_x, d: hi})
        tornado.append({"driver": d, "low_input": lo, "high_input": hi, "npv_at_low": a, "npv_at_high": b,
                        "swing": abs(b - a), "crosses_zero": min(a, b) < 0 < max(a, b)})
    tornado.sort(key=lambda t: -t["swing"])

    random.seed(seed)
    draws = []
    for _ in range(sims):
        x = {d: random.triangular(lo, hi, mid) for d, (lo, mid, hi) in rng.items()}
        x.setdefault("rate", cfg["rate"])
        draws.append(case_npv(years, cfg, x))
    s = sorted(draws)
    p_loss = sum(v < 0 for v in s) / sims
    edges = [s[0] + (s[-1] - s[0]) * i / 20 for i in range(21)]
    hist = [{"from": edges[i], "to": edges[i + 1],
             "count": sum(edges[i] <= v < edges[i + 1] or (i == 19 and v == edges[-1]) for v in s)}
            for i in range(20)]
    out = {
        "base_npv": base, "npv_at_likely_values": case_npv(years, cfg, likely_x),
        "tornado": tornado,
        "monte_carlo": {"simulations": sims, "seed": seed, "mean": statistics.fmean(s), "median": pct(s, 0.5),
                        "p10": pct(s, 0.10), "p90": pct(s, 0.90), "stdev": statistics.pstdev(s),
                        "prob_npv_below_zero": p_loss, "histogram": hist,
                        "assumption": "drivers drawn independently from triangular distributions"},
    }
    top = tornado[0]
    out["in_words"] = (
        f"{top['driver'].replace('_', ' ').capitalize()} moves NPV the most (a swing of {top['swing']:,.0f}). "
        f"Across {sims:,} simulated futures the median NPV is {out['monte_carlo']['median']:,.0f}, "
        f"80% of outcomes fall between {out['monte_carlo']['p10']:,.0f} and {out['monte_carlo']['p90']:,.0f}, "
        f"and NPV is negative {p_loss:.0%} of the time.")
    txt = json.dumps(out, indent=2, default=lambda v: round(v, 4))
    if "--out" in sys.argv:
        open(sys.argv[sys.argv.index("--out") + 1], "w").write(txt)
    print(txt)


if __name__ == "__main__":
    main()
