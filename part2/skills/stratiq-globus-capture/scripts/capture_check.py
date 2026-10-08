#!/usr/bin/env python3
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Copyright (c) 2026 G. Bradley Scheller · Strat-IQ Toolkit · commercial licences: BScheller@ToolsIQ.ai
"""Check a GLO-BUS capture file against the capture checklist (Strat-IQ GLO-BUS Capture).

Usage: python capture_check.py globus-capture-C-Y6.json [--out check.json]
Page ids should start with a checklist prefix (e.g. cir-cameras-na, dec-marketing-drones-ea).
Reports: required groups missing, CIR and marketing product x region combinations missing,
thin pages (text under 200 characters) and pages carrying warnings.
"""
import json, sys

REQUIRED = ["scoreboard", "cir", "cdj", "highlights", "dec-product", "dec-marketing", "dec-operations",
            "dec-compensation", "dec-csr", "dec-finance", "projections", "company-reports"]
OPTIONAL = ["industry-reports", "special-contracts"]
PRODUCTS = ["cameras", "drones"]
REGIONS = ["na", "ea", "ap", "la"]
SPLIT = {"cir": (PRODUCTS, REGIONS), "dec-marketing": (PRODUCTS, REGIONS),
         "dec-product": (PRODUCTS, None), "dec-operations": (PRODUCTS, None)}


def main():
    a = sys.argv
    if len(a) < 2:
        sys.exit(__doc__)
    cap = json.load(open(a[1], encoding="utf-8"))
    pages = cap.get("pages", [])
    ids = [p.get("id", "").lower() for p in pages]
    has = lambda pre: [i for i in ids if i == pre or i.startswith(pre + "-")]
    missing = [g for g in REQUIRED if not has(g)]
    combos = {}
    for g, (prods, regs) in SPLIT.items():
        if not has(g):
            continue
        want = [f"{g}-{p}-{r}" for p in prods for r in regs] if regs else [f"{g}-{p}" for p in prods]
        miss = [w for w in want if not any(i.startswith(w) for i in ids)]
        if miss:
            combos[g] = miss
    thin = [p.get("id") for p in pages if len((p.get("text") or "").strip()) < 200]
    warned = {p.get("id"): p.get("warnings") for p in pages if p.get("warnings")}
    out = {"company": cap.get("company"), "year": cap.get("year"), "pages": len(pages),
           "missing_required": missing, "missing_combinations": combos,
           "optional_present": [g for g in OPTIONAL if has(g)], "thin_pages": thin, "warnings": warned,
           "complete": not missing and not combos}
    txt = json.dumps(out, indent=2)
    if "--out" in a:
        open(a[a.index("--out") + 1], "w").write(txt)
    print(txt)


if __name__ == "__main__":
    main()
