#!/usr/bin/env python3
"""GLO-BUS strategic groups, leader and white space from Competitive Intelligence Report figures.

Usage: python globus_groups.py cir.csv [--team C] [--chart groups.png] [--out results.json]
CSV columns: company, product (camera|drone), region, price, pq, models, ads, support, warranty, share
  region  : NA, EA, AP, LA or Global. One row per company, product and region.
  pq      : P/Q rating in stars (0-10). share: market share in % (e.g. 14.5).
  ads, support, warranty, models may be blank. support = retailer support / promotions / discount.
Groups are set against the share-weighted industry averages of price and P/Q for each product and region.
White space: the price and P/Q ranges are split into a 3 x 3 grid; empty cells are listed (except
high price / low P/Q, which is never an opportunity). An empty cell is a lead to test, not a finding.
"""
import csv, json, sys
from collections import defaultdict


def num(v):
    v = (v or "").strip().replace(",", "").replace("$", "").replace("%", "")
    return float(v) if v else None


def load(path):
    rows = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if not (r.get("company") or "").strip():
                continue
            row = {"company": r["company"].strip(), "product": (r.get("product") or "").strip().lower(),
                   "region": (r.get("region") or "Global").strip() or "Global"}
            for k in ("price", "pq", "models", "ads", "support", "warranty", "share"):
                row[k] = num(r.get(k))
            if row["product"] not in ("camera", "drone"):
                sys.exit(f"ERROR: product must be camera or drone ('{row['company']}')")
            if row["price"] is None or row["pq"] is None:
                sys.exit(f"ERROR: price and pq are required ('{row['company']}', {row['product']}, {row['region']})")
            rows.append(row)
    if not rows:
        sys.exit("ERROR: no rows")
    return rows


def wavg(rows, k):
    w = [(r[k], r["share"] if r["share"] else 1.0) for r in rows]
    tot = sum(x[1] for x in w)
    return sum(a * b for a, b in w) / tot


def group(r, p_avg, q_avg):
    hi_p, hi_q = r["price"] > p_avg, r["pq"] >= q_avg
    if hi_p and hi_q:
        return "Premium differentiator"
    if not hi_p and hi_q:
        return "Value leader"
    if not hi_p and not hi_q:
        return "Low-cost / economy"
    return "Stuck in the middle"


def analyse(rows):
    out = []
    for key, rs in sorted(_bucket(rows).items()):
        product, region = key
        p_avg, q_avg = wavg(rs, "price"), wavg(rs, "pq")
        comps = []
        for r in rs:
            spend = sum(x for x in (r["ads"], r["support"]) if x is not None) if (r["ads"] or r["support"]) else None
            comps.append({**r, "group": group(r, p_avg, q_avg),
                          "price_vs_avg_pct": round(100 * (r["price"] / p_avg - 1), 1),
                          "pq_vs_avg": round(r["pq"] - q_avg, 2), "spend": spend})
        shared = [c for c in comps if c["share"] is not None]
        leader = max(shared, key=lambda c: c["share"]) if shared else None
        # spend efficiency: share points per unit of spend, relative to the median
        eff = [c for c in shared if c["spend"]]
        laggard = None
        if len(eff) >= 3:
            for c in eff:
                c["share_per_spend"] = c["share"] / c["spend"]
            med = sorted(c["share_per_spend"] for c in eff)[len(eff) // 2]
            worst = min(eff, key=lambda c: c["share_per_spend"])
            if worst["share_per_spend"] < 0.7 * med:
                laggard = worst["company"]
        lo_p, hi_p = min(r["price"] for r in rs), max(r["price"] for r in rs)
        lo_q, hi_q = min(r["pq"] for r in rs), max(r["pq"] for r in rs)
        cells, names = defaultdict(list), (("low", "mid", "high"))
        for c in comps:
            i = min(2, int(3 * (c["price"] - lo_p) / (hi_p - lo_p))) if hi_p > lo_p else 1
            j = min(2, int(3 * (c["pq"] - lo_q) / (hi_q - lo_q))) if hi_q > lo_q else 1
            cells[(i, j)].append(c["company"])
        # an empty high-price / low-P/Q cell is not white space: nobody should be there
        empty = [f"{names[i]} price / {names[j]} P/Q" for i in range(3) for j in range(3)
                 if (i, j) not in cells and not (i == 2 and j == 0)]
        out.append({"product": product, "region": region, "avg_price": round(p_avg, 2), "avg_pq": round(q_avg, 2),
                    "companies": [{k: c[k] for k in ("company", "price", "pq", "share", "models", "group",
                                                     "price_vs_avg_pct", "pq_vs_avg")} for c in comps],
                    "share_leader": leader["company"] if leader else None,
                    "leader_group": leader["group"] if leader else None,
                    "low_spend_efficiency": laggard,
                    "price_range": [lo_p, hi_p], "pq_range": [lo_q, hi_q], "empty_cells": empty})
    return out


def _bucket(rows):
    b = defaultdict(list)
    for r in rows:
        b[(r["product"], r["region"])].append(r)
    return b


def chart(results, path, team):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("NOTE: matplotlib not installed; chart skipped", file=sys.stderr)
        return
    n = len(results)
    cols = min(2, n)
    rows_n = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows_n, cols, figsize=(6.5 * cols, 5 * rows_n), squeeze=False)
    colors = {"Premium differentiator": "#2a6f97", "Value leader": "#2d936c",
              "Low-cost / economy": "#8d99ae", "Stuck in the middle": "#c44536"}
    for ax, res in zip([a for row in axes for a in row], results):
        for c in res["companies"]:
            s = 60 + 25 * (c["share"] or 3)
            ax.scatter(c["pq"], c["price"], s=s, color=colors[c["group"]], alpha=0.75,
                       edgecolor="black" if team and c["company"].upper().startswith(team.upper()) else "white",
                       linewidth=2.5 if team and c["company"].upper().startswith(team.upper()) else 0.8)
            ax.annotate(c["company"], (c["pq"], c["price"]), fontsize=8, ha="center", va="center")
        ax.axvline(res["avg_pq"], color="#999", ls="--", lw=0.8)
        ax.axhline(res["avg_price"], color="#999", ls="--", lw=0.8)
        ax.set_title(f"{res['product'].title()}s — {res['region']}", fontsize=11)
        ax.set_xlabel("P/Q rating (stars)")
        ax.set_ylabel("Price ($)")
        ax.spines[["top", "right"]].set_visible(False)
    for ax in [a for row in axes for a in row][n:]:
        ax.axis("off")
    handles = [plt.Line2D([], [], marker="o", ls="", color=v, label=k, markersize=9) for k, v in colors.items()]
    fig.legend(handles=handles, loc="lower center", ncol=4, frameon=False, fontsize=9)
    fig.suptitle("GLO-BUS strategic groups (bubble = market share; dashed = industry average)", fontsize=12)
    fig.tight_layout(rect=(0, 0.05, 1, 0.96))
    fig.savefig(path, dpi=160)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    a = sys.argv
    team = a[a.index("--team") + 1] if "--team" in a else None
    res = analyse(load(a[1]))
    if "--chart" in a:
        chart(res, a[a.index("--chart") + 1], team)
    txt = json.dumps(res, indent=2)
    if "--out" in a:
        open(a[a.index("--out") + 1], "w").write(txt)
    print(txt)


if __name__ == "__main__":
    main()
