#!/usr/bin/env python3
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Copyright (c) 2026 G. Bradley Scheller · Strat-IQ Toolkit · commercial licences: BScheller@ToolsIQ.ai
"""Expected NPV, maximin, flip points and EVPI for strategic options (Strat-IQ Exhibit Q-2).

Usage: python expected_value.py expected-value.csv [--out results.json]
CSV columns: option, scenario, probability, npv
  probability as a fraction (0.3) or percent (30). Each option's probabilities must sum to 1.
  Scenarios should share names across options (e.g. strong, moderate, weak) for EVPI and flip points.
Flip points: holding the first scenario's probability fixed, shift probability between the second and the
last scenario and report the last-scenario probability at which the leader is overtaken by each rival.
"""
import csv, json, sys
from collections import OrderedDict


def load(path):
    opts = OrderedDict()
    with open(path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            o = (r.get("option") or "").strip()
            if not o:
                continue
            p = float((r.get("probability") or "0").replace("%", ""))
            p = p / 100 if p > 1 else p
            npv = float((r.get("npv") or "0").replace(",", "").replace("$", ""))
            opts.setdefault(o, OrderedDict())[(r.get("scenario") or "").strip().lower()] = (p, npv)
    for o, sc in opts.items():
        s = sum(p for p, _ in sc.values())
        if abs(s - 1) > 0.001:
            sys.exit(f"ERROR: probabilities for '{o}' sum to {s:.3f}, not 1")
    return opts


def ev(sc, probs=None):
    return sum((probs[k] if probs else p) * v for k, (p, v) in sc.items())


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    opts = load(sys.argv[1])
    res = []
    for o, sc in opts.items():
        vals = [v for _, v in sc.values()]
        res.append({"option": o, "expected_npv": ev(sc), "worst": min(vals), "best": max(vals),
                    "never_loses": min(vals) >= 0})
    leader = max(res, key=lambda x: x["expected_npv"])
    maximin = max(res, key=lambda x: x["worst"])
    out = {"options": res, "leader": leader["option"], "maximin": maximin["option"]}
    # EVPI: needs shared scenarios and a common probability set (use the leader's)
    lead_sc = opts[leader["option"]]
    scen = list(lead_sc.keys())
    if all(set(sc.keys()) == set(scen) for sc in opts.values()):
        perfect = sum(lead_sc[s][0] * max(opts[o][s][1] for o in opts) for s in scen)
        out["evpi"] = perfect - leader["expected_npv"]
        out["best_by_scenario"] = {s: max(opts, key=lambda o: opts[o][s][1]) for s in scen}
        if len(scen) >= 3:
            first, mid, last = scen[0], scen[1], scen[-1]
            p_first = lead_sc[first][0]
            room = 1 - p_first
            flips = {}
            for o in opts:
                if o == leader["option"]:
                    continue
                lo, hi = 0.0, room
                diff = lambda w: (ev(opts[leader["option"]], {first: p_first, mid: room - w, last: w,
                                                                **{s: 0 for s in scen[2:-1]}}) -
                                  ev(opts[o], {first: p_first, mid: room - w, last: w,
                                               **{s: 0 for s in scen[2:-1]}}))
                if diff(lo) * diff(hi) > 0:
                    flips[o] = None
                    continue
                for _ in range(100):
                    m = (lo + hi) / 2
                    if diff(lo) * diff(m) <= 0:
                        hi = m
                    else:
                        lo = m
                flips[o] = round((lo + hi) / 2, 4)
            out["flip_points"] = {"scenario_shifted_to": last, "held_fixed": f"{first} at {p_first:.0%}",
                                  "current": lead_sc[last][0], "overtaken_at": flips}
    txt = json.dumps(out, indent=2, default=lambda x: round(x, 4))
    if "--out" in sys.argv:
        open(sys.argv[sys.argv.index("--out") + 1], "w").write(txt)
    print(txt)


if __name__ == "__main__":
    main()
