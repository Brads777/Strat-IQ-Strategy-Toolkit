#!/usr/bin/env python3
"""Value chain reading for the case-memo Value Chain exhibit.

Usage: python value_chain.py value-chain.csv [--out results.json]
CSV columns: activity, porter_category, stage, sourcing, cost_share, value_share
stage is commodity | product | custom | genesis. sourcing is in-house | outsourced | mixed (may be blank).
cost_share and value_share are fractions (0.25 = 25%) and may be blank when the evidence gives no figure.
Value-cost gap = value_share - cost_share. Gaps within +/-0.05 are in balance.
"""
import csv, json, sys

REQUIRED = ["activity", "porter_category", "stage"]
STAGES = ["commodity", "product", "custom", "genesis"]   # the exhibit template's order
BAND = 0.05


def share(r, k):
    v = (r.get(k) or "").strip().lower()
    if v in ("", "n/a", "na"):
        return None
    x = float(v.replace("%", ""))
    if not 0 <= x <= 1:
        sys.exit(f"ERROR: {k} must be a fraction 0-1 ('{r['activity']}')")
    return x


def pct(x):
    return "n/a" if x is None else f"{x:.0%}"


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
        stage = (r["stage"] or "").strip().lower()
        if stage not in STAGES:
            sys.exit(f"ERROR: stage '{r['stage']}' for '{r['activity']}' must be one of {', '.join(STAGES)}")
        cost, value = share(r, "cost_share"), share(r, "value_share")
        gap = round(value - cost, 3) if cost is not None and value is not None else None
        reading = ("no figures" if gap is None else "value trap" if gap < -BAND
                   else "differentiating engine" if gap > BAND else "in balance")
        sourcing = (r.get("sourcing") or "").strip().lower()
        mismatch = ""
        if stage == "commodity" and sourcing == "in-house":
            mismatch = "commodity activity done in-house"
        elif stage in ("custom", "genesis") and sourcing == "outsourced" and reading == "differentiating engine":
            mismatch = "differentiating activity outsourced"
        out.append({"activity": r["activity"], "porter_category": r["porter_category"], "stage": stage,
                    "sourcing": sourcing, "cost_share": cost, "value_share": value,
                    "gap": gap, "reading": reading, "mismatch": mismatch})

    for k in ("cost_share", "value_share"):
        vals = [a[k] for a in out if a[k] is not None]
        if vals and len(vals) == len(out) and abs(sum(vals) - 1.0) > 0.02:
            print(f"WARN: {k} sums to {sum(vals):.2f}, expected 1.00")
        elif vals and len(vals) < len(out):
            print(f"NOTE: {k} missing for {len(out) - len(vals)} of {len(out)} activities")

    for stage in STAGES:
        print(f"\n**{stage.capitalize()}**")
        here = [a for a in out if a["stage"] == stage]
        if not here:
            print("- No activity at this stage")
        for a in here:
            src = f"; {a['sourcing']}" if a["sourcing"] else ""
            gap = "" if a["gap"] is None else f", gap {a['gap']:+.0%} ({a['reading']})"
            print(f"- {a['activity']} (Porter: {a['porter_category']}{src}) - "
                  f"cost {pct(a['cost_share'])}, value {pct(a['value_share'])}{gap}")

    for label, key in (("Differentiating engines", "differentiating engine"), ("Value traps", "value trap")):
        hits = sorted((a for a in out if a["reading"] == key), key=lambda a: -abs(a["gap"]))
        print(f"\n== {label} ==")
        print("\n".join(f"{a['activity']}  {a['gap']:+.0%}" for a in hits) if hits else "None")
    print("\n== Stage-sourcing mismatches ==")
    mm = [a for a in out if a["mismatch"]]
    print("\n".join(f"{a['activity']}: {a['mismatch']}" for a in mm) if mm else "None")

    if "--out" in sys.argv:
        path = sys.argv[sys.argv.index("--out") + 1]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2)
        print(f"\nSaved {path}")


if __name__ == "__main__":
    main()
