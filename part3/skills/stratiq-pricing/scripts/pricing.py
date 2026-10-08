#!/usr/bin/env python3
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Copyright (c) 2026 G. Bradley Scheller · Strat-IQ Toolkit · commercial licences: BScheller@ToolsIQ.ai
"""Price sweep (constant elasticity) and Van Westendorp range for Strat-IQ Pricing.

Usage:
  python pricing.py pricing.csv [--out results.json]
      CSV columns: field, value. Fields: price, volume, variable_cost, elasticity (negative, e.g. -1.5),
      min_price, max_price (optional; default +/-30% of price), steps (optional, default 25)
  python pricing.py --vw responses.csv
      CSV columns: too_cheap, bargain, getting_expensive, too_expensive (one row per respondent)
Volume at price p = volume * (p / price) ** elasticity.
"""
import csv, json, sys


def kv(path):
    d = {}
    with open(path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            k, v = (r.get("field") or "").strip(), (r.get("value") or "").strip()
            if k and v:
                d[k] = float(v.replace(",", "").replace("$", ""))
    for k in ("price", "volume", "variable_cost", "elasticity"):
        if k not in d:
            sys.exit(f"ERROR: '{k}' is required")
    return d


def sweep(d):
    p0, lo = d["price"], d.get("min_price", d["price"] * 0.7)
    hi, n = d.get("max_price", d["price"] * 1.3), int(d.get("steps", 25))
    rows = []
    for i in range(n + 1):
        p = lo + (hi - lo) * i / n
        q = d["volume"] * (p / p0) ** d["elasticity"]
        rows.append({"price": p, "volume": q, "revenue": p * q, "contribution": (p - d["variable_cost"]) * q})
    base = {"price": p0, "volume": d["volume"], "revenue": p0 * d["volume"],
            "contribution": (p0 - d["variable_cost"]) * d["volume"]}
    return {"current": base, "grid": rows,
            "revenue_max_price": max(rows, key=lambda r: r["revenue"])["price"],
            "contribution_max_price": max(rows, key=lambda r: r["contribution"])["price"],
            "note": "Corner values mean the optimum lies outside the swept range; check it against the "
                    "Van Westendorp acceptable range before using it."}


def vw(path):
    cols = ["too_cheap", "bargain", "getting_expensive", "too_expensive"]
    data = {c: [] for c in cols}
    with open(path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            for c in cols:
                v = (r.get(c) or "").strip()
                if v:
                    data[c].append(float(v.replace("$", "").replace(",", "")))
    if any(len(v) < 5 for v in data.values()):
        sys.exit("ERROR: need at least 5 responses per question")
    prices = sorted(set(x for v in data.values() for x in v))
    share = lambda c, p, below: sum(1 for x in data[c] if (x >= p if below else x <= p)) / len(data[c])
    curves = [{"price": p, "too_cheap": share("too_cheap", p, True), "bargain": share("bargain", p, True),
               "getting_expensive": share("getting_expensive", p, False),
               "too_expensive": share("too_expensive", p, False)} for p in prices]

    def cross(a, b):
        for c in curves:
            if c[b] >= c[a]:
                return c["price"]
        return None
    return {"point_of_marginal_cheapness": cross("too_cheap", "getting_expensive"),
            "point_of_marginal_expensiveness": cross("bargain", "too_expensive"),
            "optimal_price_point": cross("too_cheap", "too_expensive"), "n": len(data["too_cheap"])}


def main():
    a = sys.argv
    if len(a) < 2:
        sys.exit(__doc__)
    out = vw(a[a.index("--vw") + 1]) if "--vw" in a else sweep(kv(a[1]))
    txt = json.dumps(out, indent=2, default=lambda x: round(x, 2))
    if "--out" in a:
        open(a[a.index("--out") + 1], "w").write(txt)
    print(txt if "--vw" in a else json.dumps({k: v for k, v in out.items() if k != "grid"} |
                                              {"grid_rows": len(out["grid"])}, indent=2, default=lambda x: round(x, 2)))


if __name__ == "__main__":
    main()
