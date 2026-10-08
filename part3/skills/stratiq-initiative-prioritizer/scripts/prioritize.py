#!/usr/bin/env python3
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Copyright (c) 2026 G. Bradley Scheller · Strat-IQ Toolkit · commercial licences: BScheller@ToolsIQ.ai
"""RICE + cost-of-delay ranking with dependencies and a capacity cut (Strat-IQ Initiative Prioritizer).

Usage: python prioritize.py initiatives.csv [--capacity 40] [--out results.json]
CSV columns: id, initiative, traces_to, reach, impact, confidence, effort, cost_of_delay, depends_on, binding
  impact: 0.25 / 0.5 / 1 / 2 / 3. confidence: 0.5-1.0. effort > 0. cost_of_delay: 1-3 (default 1).
  depends_on: ids separated by ';'. binding: yes for the binding-constraint initiative(s).
Priority score = RICE x (1 + (cost_of_delay - 1) / 2). Binding initiatives rank first.
Scheduling: in rank order; an item is 'now' only if its dependencies are 'now' and effort fits capacity.
"""
import csv, json, sys


def f(v, d=0.0):
    v = (v or "").strip()
    return float(v) if v else d


def main():
    a = sys.argv
    if len(a) < 2:
        sys.exit(__doc__)
    cap = float(a[a.index("--capacity") + 1]) if "--capacity" in a else None
    items = []
    with open(a[1], newline="", encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            if not (r.get("initiative") or "").strip():
                continue
            e = f(r.get("effort"))
            if e <= 0:
                sys.exit(f"ERROR: effort must be > 0 ('{r['initiative']}')")
            rice = f(r.get("reach")) * f(r.get("impact")) * f(r.get("confidence"), 0.8) / e
            cod = min(3, max(1, f(r.get("cost_of_delay"), 1)))
            items.append({"id": r["id"].strip(), "initiative": r["initiative"].strip(),
                          "traces_to": (r.get("traces_to") or "").strip(), "rice": rice, "cost_of_delay": cod,
                          "score": rice * (1 + (cod - 1) / 2), "effort": e,
                          "depends_on": [x.strip() for x in (r.get("depends_on") or "").split(";") if x.strip()],
                          "binding": (r.get("binding") or "").strip().lower() in ("yes", "y", "true", "1")})
    ids = {i["id"] for i in items}
    for i in items:
        if not i["traces_to"]:
            i.setdefault("warnings", []).append("does not trace to the analysis")
        for d in i["depends_on"]:
            if d not in ids:
                sys.exit(f"ERROR: '{i['id']}' depends on unknown id '{d}'")
    items.sort(key=lambda x: (not x["binding"], -x["score"]))
    used, now = 0.0, set()
    for rank, i in enumerate(items, 1):
        i["rank"] = rank
        deps_ok = all(d in now for d in i["depends_on"])
        fits = cap is None or used + i["effort"] <= cap
        if deps_ok and fits:
            i["status"] = "now"
            now.add(i["id"])
            used += i["effort"]
        else:
            i["status"] = "waits"
            i["reason"] = "dependency not scheduled" if not deps_ok else "over capacity"
    # second pass: a dependency ranked below its dependent may now be scheduled
    changed = True
    while changed:
        changed = False
        for i in items:
            if i["status"] == "waits" and all(d in now for d in i["depends_on"]) and \
                    (cap is None or used + i["effort"] <= cap):
                i["status"], changed = "now", True
                i.pop("reason", None)
                now.add(i["id"])
                used += i["effort"]
    out = {"capacity": cap, "effort_used": used, "initiatives": items,
           "now": [i["id"] for i in items if i["status"] == "now"]}
    if len(out["now"]) > 5:
        out["warning"] = "More than five initiatives are 'now': the plan may not be prioritised."
    txt = json.dumps(out, indent=2, default=lambda x: round(x, 3))
    if "--out" in a:
        open(a[a.index("--out") + 1], "w").write(txt)
    print(txt)


if __name__ == "__main__":
    main()
