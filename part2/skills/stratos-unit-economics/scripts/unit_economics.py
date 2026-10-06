#!/usr/bin/env python3
"""Unit economics, break-even and sensitivity for the StratOS Exhibit J-1.

Usage: python unit_economics.py unit-economics.csv [--out results.json]
CSV columns: field, value   (one row per field; blank values are treated as missing)
Required fields: unit, price, variable_cost, fixed_costs, volume
Optional (customer economics): cac, units_per_customer_year, retention, discount_rate, service_margin_year
Retention is the annual share of customers kept (0-1). Lifetime = 1 / (1 - retention), capped at 10 years.
"""
import csv, json, sys

NUM = ["price", "variable_cost", "fixed_costs", "volume", "cac", "units_per_customer_year",
       "retention", "discount_rate", "service_margin_year"]


def load(path):
    d = {}
    with open(path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            k = (r.get("field") or "").strip()
            v = (r.get("value") or "").strip()
            if not k:
                continue
            if k in NUM:
                d[k] = float(v.replace(",", "").replace("$", "")) if v else None
            else:
                d[k] = v
    for k in ("price", "variable_cost", "fixed_costs", "volume"):
        if d.get(k) is None:
            sys.exit(f"ERROR: '{k}' is required")
    return d


def core(price, vc, fixed, vol):
    c = price - vc
    be = fixed / c if c > 0 else None
    return {"contribution": c, "contribution_margin": c / price if price else None,
            "break_even_volume": be,
            "margin_of_safety": (vol - be) / vol if be is not None and vol else None,
            "operating_profit": c * vol - fixed}


def customer(d, contribution):
    if d.get("cac") is None or d.get("units_per_customer_year") is None:
        return None
    annual = contribution * d["units_per_customer_year"] + (d.get("service_margin_year") or 0)
    ret = d.get("retention") or 0.0
    life = min(10, 1 / (1 - ret)) if ret < 1 else 10
    r = d.get("discount_rate") or 0.0
    years, ltv, left = 0, 0.0, life
    while left > 0:
        share = min(1, left)
        ltv += annual * share / (1 + r) ** years
        years += 1
        left -= 1
    return {"annual_contribution_per_customer": annual, "lifetime_years": round(life, 2), "ltv": ltv,
            "ltv_to_cac": ltv / d["cac"] if d["cac"] else None,
            "cac_payback_months": d["cac"] / (annual / 12) if annual > 0 else None}


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    d = load(sys.argv[1])
    base = core(d["price"], d["variable_cost"], d["fixed_costs"], d["volume"])
    sens = []
    for name, f in (("price", lambda s: core(d["price"] * s, d["variable_cost"], d["fixed_costs"], d["volume"])),
                    ("variable_cost", lambda s: core(d["price"], d["variable_cost"] * s, d["fixed_costs"], d["volume"])),
                    ("volume", lambda s: core(d["price"], d["variable_cost"], d["fixed_costs"], d["volume"] * s))):
        lo, hi = f(0.9), f(1.1)
        sens.append({"driver": name, "profit_at_-10%": lo["operating_profit"], "profit_at_+10%": hi["operating_profit"],
                     "swing": abs(hi["operating_profit"] - lo["operating_profit"])})
    sens.sort(key=lambda x: -x["swing"])
    out = {"unit": d.get("unit", "unit"), "base": base, "customer": customer(d, base["contribution"]),
           "sensitivity": sens, "top_driver": sens[0]["driver"]}
    if base["contribution"] <= 0:
        out["warning"] = "Contribution per unit is zero or negative: more volume increases losses."
    txt = json.dumps(out, indent=2, default=lambda x: round(x, 4))
    if "--out" in sys.argv:
        open(sys.argv[sys.argv.index("--out") + 1], "w").write(txt)
    print(txt)


if __name__ == "__main__":
    main()
