#!/usr/bin/env python3
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Copyright (c) 2026 G. Bradley Scheller · Strat-IQ Toolkit · commercial licences: BScheller@ToolsIQ.ai
"""Risk register scoring for the Strat-IQ Stress Test (Exhibit R).

Usage: python risk_register.py risk-register.csv [--out results.json]
CSV columns: id, risk, category, likelihood, impact, velocity, owner, mitigation
  likelihood, impact: 1-5. velocity: slow | medium | fast (fast raises the band by one).
Score = likelihood x impact. Bands: 1-4 low, 5-9 medium, 10-16 high, 17-25 critical.
Flags: high/critical risks with no owner, or whose mitigation is only monitoring.
"""
import csv, json, re, sys

BANDS = [(4, "low"), (9, "medium"), (16, "high"), (25, "critical")]
ORDER = ["low", "medium", "high", "critical"]
WEAK = re.compile(r"^\s*(monitor|watch|track|keep an eye|review|tbd|n/?a|none)\b", re.I)


def band(score):
    return next(b for lim, b in BANDS if score <= lim)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    out = []
    with open(sys.argv[1], newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if not (r.get("risk") or "").strip():
                continue
            L, I = int(r["likelihood"]), int(r["impact"])
            if not (1 <= L <= 5 and 1 <= I <= 5):
                sys.exit(f"ERROR: likelihood and impact must be 1-5 ('{r['risk']}')")
            s = L * I
            b = band(s)
            vel = (r.get("velocity") or "medium").strip().lower()
            if vel == "fast" and b != "critical":
                b = ORDER[ORDER.index(b) + 1]
            flags = []
            owner, mit = (r.get("owner") or "").strip(), (r.get("mitigation") or "").strip()
            if b in ("high", "critical"):
                if not owner:
                    flags.append("no owner")
                if not mit or WEAK.match(mit):
                    flags.append("mitigation is monitoring only")
            out.append({"id": r.get("id", ""), "risk": r["risk"].strip(), "category": r.get("category", ""),
                        "likelihood": L, "impact": I, "velocity": vel, "score": s, "band": b,
                        "owner": owner, "mitigation": mit, "flags": flags})
    out.sort(key=lambda x: (-ORDER.index(x["band"]), -x["score"]))
    summary = {b: sum(1 for x in out if x["band"] == b) for b in ORDER}
    res = {"risks": out, "summary": summary, "flagged": [x["id"] or x["risk"] for x in out if x["flags"]]}
    txt = json.dumps(res, indent=2)
    if "--out" in sys.argv:
        open(sys.argv[sys.argv.index("--out") + 1], "w").write(txt)
    print(txt)


if __name__ == "__main__":
    main()
