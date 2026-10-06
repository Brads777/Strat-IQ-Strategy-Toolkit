#!/usr/bin/env python3
"""Plan-vs-actual variance by driver, with profit effect (StratOS Value Realization).

Usage: python variance.py variance.csv [--threshold 0.05] [--out results.json]
CSV rows (field, plan, actual): units, price, variable_cost, fixed_cost  (all required)
Profit = (price - variable_cost) x units - fixed_cost.
Effects are computed in sequence (units -> price -> variable cost -> fixed cost), so they add up exactly
to the total profit variance. A driver is material if its own variance, or its profit effect as a share
of planned profit, reaches the threshold.
"""
import csv, json, sys

ORDER = ["units", "price", "variable_cost", "fixed_cost"]


def profit(s):
    return (s["price"] - s["variable_cost"]) * s["units"] - s["fixed_cost"]


def main():
    a = sys.argv
    if len(a) < 2:
        sys.exit(__doc__)
    th = float(a[a.index("--threshold") + 1]) if "--threshold" in a else 0.05
    plan, act = {}, {}
    with open(a[1], newline="", encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            k = (r.get("field") or "").strip()
            if k in ORDER:
                plan[k] = float(r["plan"].replace(",", ""))
                act[k] = float(r["actual"].replace(",", ""))
    for k in ORDER:
        if k not in plan:
            sys.exit(f"ERROR: '{k}' row is required")
    state = dict(plan)
    rows = []
    for k in ORDER:
        before = profit(state)
        state[k] = act[k]
        eff = profit(state) - before
        rel = (act[k] - plan[k]) / plan[k] if plan[k] else None
        rows.append({"driver": k, "plan": plan[k], "actual": act[k], "variance_pct": rel,
                     "profit_effect": eff,
                     "material": (rel is not None and abs(rel) >= th) or abs(eff) >= th * abs(profit(plan))})
    out = {"plan_profit": profit(plan), "actual_profit": profit(act),
           "total_variance": profit(act) - profit(plan), "drivers": rows,
           "offsetting": any(r["profit_effect"] > 0 for r in rows if r["material"]) and
                         any(r["profit_effect"] < 0 for r in rows if r["material"])}
    if out["offsetting"]:
        out["note"] = "Material drivers moved in opposite directions: the headline hides offsetting misses."
    txt = json.dumps(out, indent=2, default=lambda x: round(x, 4))
    if "--out" in a:
        open(a[a.index("--out") + 1], "w").write(txt)
    print(txt)


if __name__ == "__main__":
    main()
