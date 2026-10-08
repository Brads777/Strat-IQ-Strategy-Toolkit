#!/usr/bin/env python3
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Copyright (c) 2026 G. Bradley Scheller · Strat-IQ Toolkit · commercial licences: BScheller@ToolsIQ.ai
"""Reverse funnel: from target customers to spend and CAC per channel (Strat-IQ Go-to-Market).

Usage: python gtm_funnel.py gtm-funnel.csv [--contribution 13000] [--monthly-contribution 0] [--out r.json]
CSV columns: channel, target_customers, stage_rates, cost_per_lead, cost_per_sale, fixed_cost
  stage_rates: conversion rates from lead to customer, separated by '>' (e.g. 0.20>0.30>0.25)
  cost_per_lead: acquisition cost per top-of-funnel lead; cost_per_sale: variable selling cost per customer
  fixed_cost: channel fixed cost for the period (team, tools)
--contribution: contribution per customer (from Unit Economics) to test CAC against.
--monthly-contribution: if customers pay over time, contribution per customer per month (gives payback).
"""
import csv, json, sys


def f(v):
    v = (v or "").strip().replace(",", "").replace("$", "")
    return float(v) if v else 0.0


def main():
    a = sys.argv
    if len(a) < 2:
        sys.exit(__doc__)
    contrib = float(a[a.index("--contribution") + 1]) if "--contribution" in a else None
    monthly = float(a[a.index("--monthly-contribution") + 1]) if "--monthly-contribution" in a else None
    rows = []
    with open(a[1], newline="", encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            ch = (r.get("channel") or "").strip()
            if not ch:
                continue
            rates = [float(x) for x in (r.get("stage_rates") or "").split(">") if x.strip()]
            if not rates or any(not 0 < x <= 1 for x in rates):
                sys.exit(f"ERROR: stage_rates must be fractions 0-1 separated by '>' ('{ch}')")
            cust = f(r.get("target_customers"))
            overall = 1.0
            for x in rates:
                overall *= x
            leads = cust / overall
            spend = leads * f(r.get("cost_per_lead")) + cust * f(r.get("cost_per_sale")) + f(r.get("fixed_cost"))
            cac = spend / cust if cust else None
            row = {"channel": ch, "customers": cust, "overall_conversion": overall, "leads_needed": leads,
                   "spend": spend, "cac": cac}
            if contrib and cac is not None:
                row["cac_to_contribution"] = cac / contrib
                row["fits_unit_economics"] = cac < contrib
            if monthly and cac is not None:
                row["payback_months"] = cac / monthly
            rows.append(row)
    tot_c = sum(r["customers"] for r in rows)
    tot_s = sum(r["spend"] for r in rows)
    out = {"channels": rows, "total_customers": tot_c, "total_spend": tot_s,
           "blended_cac": tot_s / tot_c if tot_c else None}
    if contrib and tot_c:
        out["blended_cac_to_contribution"] = out["blended_cac"] / contrib
        out["breaks_business_case"] = [r["channel"] for r in rows if not r.get("fits_unit_economics", True)]
    txt = json.dumps(out, indent=2, default=lambda x: round(x, 4))
    if "--out" in a:
        open(a[a.index("--out") + 1], "w").write(txt)
    print(txt)


if __name__ == "__main__":
    main()
