#!/usr/bin/env python3
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Copyright (c) 2026 G. Bradley Scheller · Strat-IQ Toolkit · commercial licences: BScheller@ToolsIQ.ai
"""Bayesian update and the value of a pilot (Strat-IQ Exhibit Q-3, Risk Analysis; extends Exhibit Q-2).

Usage: python bayes_update.py expected-value.csv pilot.csv [--cost 0.5] [--observed positive] [--out pilot.json]
pilot.csv: one row per scenario (names must match expected-value.csv), one column per pilot signal,
  each cell = P(signal | scenario), i.e. how likely the pilot shows that signal if that scenario is real.
  Each row must sum to 100%. The student sets these (from a test market, a comparable launch, an expert).
Prior probabilities come from expected-value.csv (all options must share the same scenario probabilities).
Reports: P(each signal); the posterior scenario probabilities after each signal (Bayes' rule);
  the best option after each signal; the expected value with the pilot; EVSI (the expected value of the
  pilot's sample information) and, with --cost, the net value of running the pilot. --observed reports the
  update for the signal the student actually saw.
"""
import csv, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from expected_value import load as load_ev  # noqa: E402


def p(v):
    v = (v or "0").strip()
    x = float(v.rstrip("%"))
    return x / 100 if v.endswith("%") or x > 1 else x


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    opts = load_ev(sys.argv[1])
    names = list(opts)
    scen = list(opts[names[0]].keys())
    prior = {s: opts[names[0]][s][0] for s in scen}
    for o in names:
        if set(opts[o]) != set(scen) or any(abs(opts[o][s][0] - prior[s]) > 1e-9 for s in scen):
            sys.exit("ERROR: every option must use the same scenarios and probabilities")
    lik, signals = {}, None
    with open(sys.argv[2], newline="", encoding="utf-8-sig") as f:
        rd = csv.DictReader(f)
        signals = [c for c in rd.fieldnames if c.strip().lower() != "scenario"]
        for r in rd:
            s = r["scenario"].strip().lower()
            lik[s] = {g: p(r[g]) for g in signals}
            if abs(sum(lik[s].values()) - 1) > 0.001:
                sys.exit(f"ERROR: pilot likelihoods for '{s}' sum to {sum(lik[s].values()):.3f}, not 1")
    if set(lik) != set(scen):
        sys.exit(f"ERROR: pilot.csv scenarios {sorted(lik)} must match {sorted(scen)}")

    ev = lambda o, pr: sum(pr[s] * opts[o][s][1] for s in scen)
    best_now = max(names, key=lambda o: ev(o, prior))
    ev_now = ev(best_now, prior)
    by_signal, ev_pilot = [], 0.0
    for g in signals:
        pg = sum(prior[s] * lik[s][g] for s in scen)
        if pg == 0:
            continue
        post = {s: prior[s] * lik[s][g] / pg for s in scen}
        best = max(names, key=lambda o: ev(o, post))
        ev_pilot += pg * ev(best, post)
        by_signal.append({"signal": g, "probability": pg, "posterior": post, "best_option": best,
                          "expected_npv_by_option": {o: ev(o, post) for o in names},
                          "changes_the_choice": best != best_now})
    perfect = sum(prior[s] * max(opts[o][s][1] for o in names) for s in scen)
    out = {"prior": prior, "best_without_pilot": best_now, "expected_npv_without_pilot": ev_now,
           "signals": by_signal, "expected_npv_with_pilot": ev_pilot, "evsi": ev_pilot - ev_now,
           "evpi": perfect - ev_now,
           "pilot_efficiency": (ev_pilot - ev_now) / (perfect - ev_now) if perfect > ev_now else None}
    if "--cost" in sys.argv:
        c = float(sys.argv[sys.argv.index("--cost") + 1])
        out["pilot_cost"] = c
        out["net_value_of_pilot"] = out["evsi"] - c
    if "--observed" in sys.argv:
        g = sys.argv[sys.argv.index("--observed") + 1]
        out["observed"] = next((x for x in by_signal if x["signal"] == g), None)
    flips = [x["signal"] for x in by_signal if x["changes_the_choice"]]
    out["in_words"] = (
        f"Without a pilot, {best_now} leads at {ev_now:,.2f}. A pilot is worth up to {out['evsi']:,.2f} "
        f"(EVSI), {out['pilot_efficiency'] or 0:.0%} of perfect information ({out['evpi']:,.2f}). "
        + (f"It matters because a {', '.join(flips)} result would change the choice." if flips else
           "No pilot result would change the choice, so the pilot is worth nothing for this decision."))
    txt = json.dumps(out, indent=2, default=lambda v: round(v, 4))
    if "--out" in sys.argv:
        open(sys.argv[sys.argv.index("--out") + 1], "w").write(txt)
    print(txt)


if __name__ == "__main__":
    main()
