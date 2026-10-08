#!/usr/bin/env python3
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Copyright (c) 2026 G. Bradley Scheller · Strat-IQ Toolkit · commercial licences: BScheller@ToolsIQ.ai
"""VRIO verdict ladder and public reality check for the case-memo VRIO exhibit.

Usage: python vrio_screen.py vrio.csv [--out results.json]
CSV columns: item, type, valuable, rare, inimitable, organized, ksf, ksf_weight
The four tests are yes | no | ? (blank counts as ?). The ladder stops at the first no or ?.
ksf is the KSF id(s) the item delivers; ksf_weight is the highest weight among them (fraction, may be blank).
Reality check (public screen): an item passing V, R and I with ksf_weight under 0.10 is a competence trap.
"""
import csv, json, sys

REQUIRED = ["item", "type", "valuable", "rare", "inimitable", "organized"]
TESTS = ["valuable", "rare", "inimitable", "organized"]
VERDICT_AT_NO = {"valuable": "Competitive disadvantage", "rare": "Competitive parity",
                 "inimitable": "Temporary advantage", "organized": "Unexploited advantage"}
ADVANTAGE = ("Temporary advantage", "Unexploited advantage", "Sustained advantage")
MIN_WEIGHT = 0.10


def answer(r, k):
    v = (r.get(k) or "").strip().lower()
    if v in ("yes", "y", "true", "1"):
        return "yes"
    if v in ("no", "n", "false", "0"):
        return "no"
    if v in ("", "?", "unknown", "n/a", "na"):
        return "?"
    sys.exit(f"ERROR: {k} must be yes, no or ? ('{r['item']}')")


def screen(r):
    ans = {k: answer(r, k) for k in TESTS}
    passed, verdict, shown = [], "Sustained advantage", {k: "-" for k in TESTS}
    for k in TESTS:
        if ans[k] == "yes":
            passed.append(k)
            shown[k] = "Yes"
            continue
        if ans[k] == "no":
            shown[k] = "No"
            verdict = VERDICT_AT_NO[k]
        else:
            shown[k] = "?"
            verdict = f"Undetermined beyond {passed[-1]}" if passed else "Undetermined"
        break
    w = (r.get("ksf_weight") or "").strip()
    weight = float(w) if w else None
    if weight is not None and not 0 <= weight <= 1:
        sys.exit(f"ERROR: ksf_weight must be a fraction 0-1 ('{r['item']}')")
    low = weight is None or weight < MIN_WEIGHT
    if all(k in passed for k in ("valuable", "rare", "inimitable")) and low:
        check = "Competence trap"
    elif verdict in ADVANTAGE and not low:
        check = "Supported"
    elif verdict == "Competitive parity" and not low:
        check = "Table stakes"
    else:
        check = ""
    return {"item": r["item"], "type": r["type"], "answers": shown, "passed": passed, "verdict": verdict,
            "ksf": (r.get("ksf") or "").strip(), "ksf_weight": weight, "reality_check": check}


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
    out = [screen(r) for r in rows]

    print("| Item | Type | V | R | I | O | Implication | Links to KSF (weight) | Reality check |")
    print("|---|---|---|---|---|---|---|---|---|")
    for s in out:
        a = s["answers"]
        link = "none" if not s["ksf"] else s["ksf"] + (f" ({s['ksf_weight']:.2f})" if s["ksf_weight"] is not None else "")
        print(f"| {s['item']} | {s['type']} | {a['valuable']} | {a['rare']} | {a['inimitable']} | "
              f"{a['organized']} | {s['verdict']} | {link} | {s['reality_check'] or '-'} |")

    for label, key in (("Valuable", "valuable"), ("Rare", "rare"), ("Inimitable", "inimitable"),
                       ("Organised to exploit", "organized")):
        hits = [s["item"] for s in out if key in s["passed"]]
        print(f"\n== {label} ==")
        print("\n".join(hits) if hits else "None identified")
    traps = [s["item"] for s in out if s["reality_check"] == "Competence trap"]
    print("\n== Competence traps ==")
    print("\n".join(traps) if traps else "None")
    open_q = [s["item"] for s in out if s["verdict"].startswith("Undetermined")]
    if open_q:
        print("\n== Undetermined (ask in interview) ==")
        print("\n".join(open_q))
    if len(out) >= 4 and all(s["verdict"] == "Sustained advantage" for s in out):
        print("\nWARN: every item is a sustained advantage - check that rarity was counted against the competitor set")

    if "--out" in sys.argv:
        path = sys.argv[sys.argv.index("--out") + 1]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2)
        print(f"\nSaved {path}")


if __name__ == "__main__":
    main()
