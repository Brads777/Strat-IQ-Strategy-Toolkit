#!/usr/bin/env python3
"""Customer segment lifetime value for the case-memo CLV exhibit.

Usage: python segment_value.py segment-value.csv [--out results.json]
CSV columns: segment, avg_purchase_value, purchase_frequency, lifespan_years, margin,
             cac, retention_cost_per_year, addressable_customers, expected_share
margin and expected_share are fractions (0.30 = 30%). cac and retention_cost_per_year may be blank.
Total Segment Value = CLV per customer x (addressable_customers x expected_share).
"""
import csv, json, sys

REQUIRED = ["segment", "avg_purchase_value", "purchase_frequency", "lifespan_years", "margin",
            "addressable_customers", "expected_share"]


def num(r, k, required=True):
    v = (r.get(k) or "").strip()
    if v == "":
        if required:
            sys.exit(f"ERROR: '{k}' missing for segment '{r.get('segment')}'")
        return None
    return float(v.replace(",", "").replace("$", ""))


def money(x):
    a = abs(x)
    s = f"${a/1e9:,.2f}B" if a >= 1e9 else f"${a/1e6:,.1f}M" if a >= 1e6 else f"${a:,.2f}"
    return "-" + s if x < 0 else s


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    with open(sys.argv[1], newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        sys.exit("ERROR: empty CSV")
    missing_cols = [c for c in REQUIRED if c not in rows[0]]
    if missing_cols:
        sys.exit(f"ERROR: missing columns: {', '.join(missing_cols)}")
    out = []
    for r in rows:
        apv, freq, yrs, m = (num(r, k) for k in ("avg_purchase_value", "purchase_frequency", "lifespan_years", "margin"))
        tam, share = num(r, "addressable_customers"), num(r, "expected_share")
        if not 0 <= m <= 1 or not 0 <= share <= 1:
            sys.exit(f"ERROR: margin and expected_share must be fractions 0-1 ('{r['segment']}')")
        cac, ret = num(r, "cac", False), num(r, "retention_cost_per_year", False)
        gross = apv * freq * yrs * m
        net = gross - (cac or 0) - (ret or 0) * yrs if (cac is not None or ret is not None) else None
        clv = net if net is not None else gross
        cust = tam * share
        out.append({"segment": r["segment"], "gross_clv": gross, "net_clv": net, "clv_used": clv,
                    "basis": "net" if net is not None else "gross", "est_customers": cust,
                    "total_value": clv * cust,
                    "share_range": [clv * cust * 0.75, clv * cust * 1.25],
                    "formula": f"${apv:g} x {freq:g}/yr x {yrs:g} yrs x {m:.0%}"
                               + (f" - CAC ${cac:g}" if cac else "") + (f" - ${ret:g}/yr retention" if ret else "")})
    out.sort(key=lambda s: -s["total_value"])
    print("| Segment | CLV/Customer | Est. Customers | Total Value |")
    print("|---|---|---|---|")
    for s in out:
        print(f"| {s['segment']} | {money(s['clv_used'])} ({s['basis']}: {s['formula']}) | "
              f"{s['est_customers']:,.0f} | {money(s['total_value'])} |")
    print("\nShare sensitivity (+/-25%):")
    for s in out:
        lo, hi = s["share_range"]
        print(f"  {s['segment']}: {money(lo)} to {money(hi)}")
        if s["clv_used"] < 0:
            print(f"  WARN: {s['segment']} has negative CLV - value-destroying at any size")
    if "--out" in sys.argv:
        path = sys.argv[sys.argv.index("--out") + 1]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2)
        print(f"\nSaved {path}")


if __name__ == "__main__":
    main()
