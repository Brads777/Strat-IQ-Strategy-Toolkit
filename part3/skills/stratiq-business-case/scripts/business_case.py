#!/usr/bin/env python3
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Copyright (c) 2026 G. Bradley Scheller · Strat-IQ Toolkit · commercial licences: BScheller@ToolsIQ.ai
"""NPV, IRR, payback, break-even and sensitivity for one strategic option (Strat-IQ Exhibit Q-1).

Usage: python business_case.py business-case.csv [--out results.json]
CSV columns: year, units, price, variable_cost, fixed_cost, capex
  Year 0 is the investment year (units may be 0). One row per year.
Settings rows (same columns, year = setting name, value in 'units'):
  rate (e.g. 0.10), tax (e.g. 0.21), wc_pct (working capital as a fraction of revenue, e.g. 0.08),
  terminal_growth (optional, e.g. 0.02; blank = no terminal value)
Working capital: the change in (wc_pct x revenue) each year is a cash outflow; it is released in the final year.
"""
import csv, json, sys


def num(v):
    v = (v or "").strip().replace(",", "").replace("$", "")
    return float(v) if v else 0.0


def load(path):
    years, cfg = [], {"rate": 0.10, "tax": 0.0, "wc_pct": 0.0, "terminal_growth": None}
    with open(path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            y = (r.get("year") or "").strip()
            if not y:
                continue
            if y in cfg:
                v = (r.get("units") or "").strip()
                cfg[y] = float(v) if v else cfg[y]
                continue
            years.append({"year": int(y), **{k: num(r.get(k)) for k in
                          ("units", "price", "variable_cost", "fixed_cost", "capex")}})
    years.sort(key=lambda x: x["year"])
    if not years:
        sys.exit("ERROR: no year rows")
    return years, cfg


def flows(years, cfg, rev_x=1.0, cost_x=1.0):
    out, prev_wc = [], 0.0
    for i, y in enumerate(years):
        rev = y["units"] * y["price"] * rev_x
        var = y["units"] * y["variable_cost"] * cost_x
        ebit = rev - var - y["fixed_cost"] * cost_x
        tax = max(0.0, ebit) * cfg["tax"]
        wc = cfg["wc_pct"] * rev
        d_wc = wc - prev_wc
        prev_wc = wc
        cf = ebit - tax - d_wc - y["capex"]
        if i == len(years) - 1:
            cf += wc  # release working capital
        out.append(cf)
    return out


def npv(cfs, r, years, g=None):
    v = sum(cf / (1 + r) ** y["year"] for cf, y in zip(cfs, years))
    if g is not None and g < r:
        last = cfs[-1]
        v += last * (1 + g) / (r - g) / (1 + r) ** years[-1]["year"]
    return v


def irr(cfs, years):
    lo, hi = -0.99, 10.0
    f = lambda r: sum(cf / (1 + r) ** y["year"] for cf, y in zip(cfs, years))
    if f(lo) * f(hi) > 0:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(lo) * f(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def payback(cfs, years):
    cum = 0.0
    for i, (cf, y) in enumerate(zip(cfs, years)):
        prev = cum
        cum += cf
        if cum >= 0 and i > 0 and cf > 0:
            return y["year"] - 1 + (-prev / cf)
    return None


def solve(fn, lo, hi):
    if fn(lo) * fn(hi) > 0:
        return None
    for _ in range(100):
        mid = (lo + hi) / 2
        if fn(lo) * fn(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    years, cfg = load(sys.argv[1])
    r, g = cfg["rate"], cfg["terminal_growth"]
    cfs = flows(years, cfg)
    base = npv(cfs, r, years)
    be_rev = solve(lambda x: npv(flows(years, cfg, rev_x=x), r, years), 0.3, 3.0)
    be_cost = solve(lambda x: npv(flows(years, cfg, cost_x=x), r, years), 0.3, 3.0)
    grid = [{"revenue_change": dr, "cost_change": dc,
             "npv": npv(flows(years, cfg, 1 + dr, 1 + dc), r, years)}
            for dr in (-0.10, -0.05, 0, 0.05, 0.10) for dc in (-0.05, 0, 0.05)]
    i = irr(cfs, years)
    out = {"rate": r, "cash_flows": dict(zip([y["year"] for y in years], cfs)), "npv": base,
           "npv_with_terminal_value": npv(cfs, r, years, g) if g is not None else None,
           "irr": i, "clears_hurdle": (i is not None and i >= r), "payback_years": payback(cfs, years),
           "break_even_revenue_change": be_rev - 1 if be_rev else None,
           "break_even_cost_change": be_cost - 1 if be_cost else None, "sensitivity": grid}
    if be_rev:
        d = be_rev - 1
        out["in_words"] = (f"The case holds only if revenue beats plan by {d:.1%}." if d > 0 else
                           f"NPV stays positive unless revenue falls more than {-d:.1%} below plan.")
    txt = json.dumps(out, indent=2, default=lambda x: round(x, 4))
    if "--out" in sys.argv:
        open(sys.argv[sys.argv.index("--out") + 1], "w").write(txt)
    print(txt)


if __name__ == "__main__":
    main()
