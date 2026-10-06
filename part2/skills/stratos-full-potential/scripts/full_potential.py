#!/usr/bin/env python3
"""Full-potential bridge for the StratOS Exhibit K-1.

Usage: python full_potential.py full-potential.csv [--out results.json]
CSV columns: driver, today, benchmark, source, controllability
Drivers (rows, any subset; names exact):
  price            average selling price per unit
  mix_premium      extra price per unit from mix (0 today if not modelled)
  volume           units per period
  variable_cost    variable cost per unit
  fixed_cost       fixed costs per period
Gaps are applied in sequence (price -> mix -> volume -> variable cost -> fixed cost) so overlaps are
counted once. A benchmark worse than today counts as zero gap (full potential never lowers profit).
"""
import csv, json, sys

ORDER = ["price", "mix_premium", "volume", "variable_cost", "fixed_cost"]
LOWER_IS_BETTER = {"variable_cost", "fixed_cost"}


def profit(s):
    return (s["price"] + s["mix_premium"] - s["variable_cost"]) * s["volume"] - s["fixed_cost"]


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    rows = {}
    with open(sys.argv[1], newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            k = (r.get("driver") or "").strip()
            if k not in ORDER:
                sys.exit(f"ERROR: unknown driver '{k}'. Use: {', '.join(ORDER)}")
            num = lambda x: float((x or "0").replace(",", "").replace("$", "") or 0)
            rows[k] = {"today": num(r.get("today")), "benchmark": num(r.get("benchmark")),
                       "source": (r.get("source") or "").strip(),
                       "controllability": (r.get("controllability") or "").strip()}
    for k in ("price", "volume", "variable_cost", "fixed_cost"):
        if k not in rows:
            sys.exit(f"ERROR: driver '{k}' is required")
    rows.setdefault("mix_premium", {"today": 0, "benchmark": 0, "source": "", "controllability": ""})
    state = {k: rows[k]["today"] for k in ORDER}
    start = profit(state)
    steps = []
    for k in ORDER:
        b, t = rows[k]["benchmark"], rows[k]["today"]
        better = b < t if k in LOWER_IS_BETTER else b > t
        before = profit(state)
        if better:
            state[k] = b
        gap = profit(state) - before
        steps.append({"driver": k, "today": t, "benchmark": b, "gap_value": gap,
                      "source": rows[k]["source"], "controllability": rows[k]["controllability"]})
    end = profit(state)
    ctrl = [s for s in steps if s["controllability"].lower().startswith("controllable") and s["gap_value"] > 0]
    out = {"current_operating_profit": start, "full_potential_operating_profit": end,
           "uplift": end - start, "uplift_pct": (end - start) / abs(start) if start else None,
           "bridge": steps,
           "ranked": sorted([s["driver"] for s in steps if s["gap_value"] > 0],
                            key=lambda d: -next(s["gap_value"] for s in steps if s["driver"] == d)),
           "largest_controllable": max(ctrl, key=lambda s: s["gap_value"])["driver"] if ctrl else None,
           "note": "Full potential is a ceiling, not a forecast."}
    txt = json.dumps(out, indent=2, default=lambda x: round(x, 4))
    if "--out" in sys.argv:
        open(sys.argv[sys.argv.index("--out") + 1], "w").write(txt)
    print(txt)


if __name__ == "__main__":
    main()
