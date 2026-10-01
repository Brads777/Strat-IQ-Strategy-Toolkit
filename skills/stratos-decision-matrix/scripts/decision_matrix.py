#!/usr/bin/env python3
"""Weighted decision matrix for case-memo Exhibit M.

Usage: python decision_matrix.py decision-matrix.csv [--out results.json]
CSV columns: issue, criterion, weight, <alternative 1>, <alternative 2>, ...
One row per criterion per issue. Weights 1-5; ratings 1-10 (blank or n/a = not rated).
Alternatives that do not apply to an issue are left blank for every row of that issue.
"""
import csv, json, sys
from collections import OrderedDict

TIE_SHARE = 0.03  # within 3% of the leader's total counts as a tie


def load(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        sys.exit("ERROR: empty CSV")
    alts = [c for c in rows[0].keys() if c not in ("issue", "criterion", "weight")]
    issues = OrderedDict()
    for r in rows:
        w = float(r["weight"])
        if not 1 <= w <= 5:
            sys.exit(f"ERROR: weight {w} for '{r['criterion']}' outside 1-5")
        ratings = {}
        for a in alts:
            v = (r[a] or "").strip().lower()
            if v in ("", "n/a", "na"):
                continue
            s = float(v)
            if not 1 <= s <= 10:
                sys.exit(f"ERROR: rating {s} for {a} / '{r['criterion']}' outside 1-10")
            ratings[a] = s
        issues.setdefault(r["issue"], []).append(
            {"criterion": r["criterion"], "weight": w, "ratings": ratings})
    return issues


def totals(rows, weights=None):
    weights = weights or [r["weight"] for r in rows]
    alts = sorted({a for r in rows for a in r["ratings"]})
    out = {}
    for a in alts:
        missing = [r["criterion"] for r in rows if a not in r["ratings"]]
        out[a] = {"total": sum(w * r["ratings"][a] for w, r in zip(weights, rows) if a in r["ratings"]),
                  "missing": missing}
    return out


def ranked(res):
    return sorted(res, key=lambda a: -res[a]["total"])


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    issues = load(sys.argv[1])
    report = {}
    for issue, rows in issues.items():
        res = totals(rows)
        order = ranked(res)
        print(f"\n== {issue} ==")
        alts = order
        print("| Criteria | Weight | " + " | ".join(f"{a} | Score" for a in alts) + " |")
        print("|---|---|" + "---|---|" * len(alts))
        for r in rows:
            cells = []
            for a in alts:
                s = r["ratings"].get(a)
                cells += ([f"{s:g}", f"{r['weight'] * s:g}"] if s is not None else ["n/a", "—"])
            print(f"| {r['criterion']} | {r['weight']:g} | " + " | ".join(cells) + " |")
        print("| **Total Score** | | " + " | ".join(f" | **{res[a]['total']:g}**" for a in alts) + " |")

        for a in alts:
            if res[a]["missing"]:
                print(f"WARN: {a} not rated on: {', '.join(res[a]['missing'])} (total understated)")
        leader = order[0]
        ties = [a for a in order[1:]
                if res[leader]["total"] - res[a]["total"] <= TIE_SHARE * res[leader]["total"]]
        if ties:
            print(f"TIE: {leader} vs {', '.join(ties)} (within {TIE_SHARE:.0%} of the leader)")
        else:
            print(f"Leader: {leader} ({res[leader]['total']:g})")

        flips = []
        for i, r in enumerate(rows):
            for d in (-1, 1):
                w = [x["weight"] for x in rows]
                if not 1 <= w[i] + d <= 5:
                    continue
                w[i] += d
                new = totals(rows, w)
                best_other = max((a for a in new if a != leader), key=lambda a: new[a]["total"], default=None)
                if best_other is None:
                    continue
                gap = new[leader]["total"] - new[best_other]["total"]
                if gap < 0:
                    flips.append({"criterion": r["criterion"], "weight_change": d, "new_leader": best_other})
                    print(f"SENSITIVITY: leader becomes {best_other} when '{r['criterion']}' weight {d:+d}")
                elif gap == 0:
                    flips.append({"criterion": r["criterion"], "weight_change": d, "tie_with": best_other})
                    print(f"SENSITIVITY: {leader} ties {best_other} when '{r['criterion']}' weight {d:+d}")
        if not flips:
            print("SENSITIVITY: leader stable under every +/-1 weight change")
        report[issue] = {"totals": res, "rank": order, "ties": ties, "sensitivity": flips}

    if "--out" in sys.argv:
        path = sys.argv[sys.argv.index("--out") + 1]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        print(f"\nSaved {path}")


if __name__ == "__main__":
    main()
