#!/usr/bin/env python3
"""Weighted KSF competitive strength assessment.

Usage: python score_ksf.py ksf-scores.csv [--out results.json]
CSV columns: ksf, weight, status, <competitor 1>, <competitor 2>, ...
Scores are 1-10 or 'n/a'. Weights must sum to 1.00 (+/- 0.01).
"""
import csv, json, sys, itertools, statistics

def load(path):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        sys.exit("ERROR: empty CSV")
    comps = [c for c in rows[0].keys() if c not in ("ksf", "weight", "status")]
    ksfs = []
    for r in rows:
        w = float(r["weight"])
        if w > 0.25:
            print(f"WARN: weight {w} for '{r['ksf']}' exceeds 0.25 cap")
        scores = {}
        for c in comps:
            v = (r[c] or "").strip().lower()
            if v in ("", "n/a", "na"):
                scores[c] = None
            else:
                s = float(v)
                if not 1 <= s <= 10:
                    sys.exit(f"ERROR: score {s} for {c}/{r['ksf']} outside 1-10")
                scores[c] = s
        ksfs.append({"ksf": r["ksf"], "weight": w, "status": r.get("status", ""), "scores": scores})
    total = sum(k["weight"] for k in ksfs)
    if abs(total - 1.0) > 0.01:
        sys.exit(f"ERROR: weights sum to {total:.3f}, must be 1.00")
    return comps, ksfs

def weighted(comps, ksfs, weights=None):
    weights = weights or [k["weight"] for k in ksfs]
    out = {}
    for c in comps:
        pairs = [(w, k["scores"][c]) for w, k in zip(weights, ksfs)]
        missing = sum(1 for _, s in pairs if s is None)
        if missing > 1:
            out[c] = {"total": None, "missing": missing, "note": "insufficient evidence - excluded"}
            continue
        avail = sum(w for w, s in pairs if s is not None)
        total = sum(w * s for w, s in pairs if s is not None) / avail
        out[c] = {"total": round(total, 2), "missing": missing,
                  "note": "weights rescaled for 1 n/a" if missing else ""}
    return out

def rank(res):
    ranked = sorted([c for c in res if res[c]["total"] is not None], key=lambda c: -res[c]["total"])
    return ranked

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    comps, ksfs = load(sys.argv[1])
    base = weighted(comps, ksfs)
    order = rank(base)
    leader = base[order[0]]["total"] if order else None

    print("\n== Competitive strength assessment ==")
    for i, c in enumerate(order, 1):
        t = base[c]["total"]
        print(f"{i}. {c:<30} {t:5.2f}  gap to leader {t - leader:+.2f}  {base[c]['note']}")
    for c in comps:
        if base[c]["total"] is None:
            print(f"-  {c:<30} excluded ({base[c]['missing']} n/a)")
    ties = [(a, b) for a, b in zip(order, order[1:]) if base[a]["total"] - base[b]["total"] < 0.3]
    for a, b in ties:
        print(f"TIE: {a} vs {b} (diff < 0.3)")

    print("\n== Sensitivity (+/-20% on each KSF weight, renormalized) ==")
    changes = []
    for i, k in enumerate(ksfs):
        for f in (0.8, 1.2):
            w = [x["weight"] for x in ksfs]
            w[i] *= f
            s = sum(w); w = [x / s for x in w]
            new = rank(weighted(comps, ksfs, w))
            if new != order:
                changes.append({"ksf": k["ksf"], "factor": f, "rank": new})
                print(f"Rank change when '{k['ksf']}' x{f}: {' > '.join(new)}")
    if not changes:
        print("Ranking stable under all +/-20% weight shifts.")

    print("\n== White space (no competitor scores above 6) ==")
    ws = [k["ksf"] for k in ksfs if all((s or 0) <= 6 for s in k["scores"].values())]
    print("\n".join(ws) if ws else "None")

    print("\n== Suggested strategic-map axes ==")
    top = sorted(ksfs, key=lambda k: -k["weight"])[:5]
    best = None
    for a, b in itertools.combinations(top, 2):
        xs, ys = [], []
        for c in comps:
            if a["scores"][c] is not None and b["scores"][c] is not None:
                xs.append(a["scores"][c]); ys.append(b["scores"][c])
        if len(xs) < 3 or len(set(xs)) < 2 or len(set(ys)) < 2:
            continue
        r = statistics.correlation(xs, ys)
        if best is None or abs(r) < abs(best[2]):
            best = (a["ksf"], b["ksf"], r)
    print(f"X: {best[0]}  |  Y: {best[1]}  (r = {best[2]:.2f})" if best else "Not enough data")

    if "--out" in sys.argv:
        path = sys.argv[sys.argv.index("--out") + 1]
        with open(path, "w") as f:
            json.dump({"results": base, "rank": order, "sensitivity": changes,
                       "white_space": ws, "axes": best}, f, indent=2)
        print(f"\nSaved {path}")

if __name__ == "__main__":
    main()
