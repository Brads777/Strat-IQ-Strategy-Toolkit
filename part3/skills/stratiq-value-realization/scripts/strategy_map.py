#!/usr/bin/env python3
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
# Copyright (c) 2026 G. Bradley Scheller · Strat-IQ Toolkit · commercial licences: BScheller@ToolsIQ.ai
"""Draw a Balanced Scorecard strategy map and check its cause-and-effect links (Strat-IQ Exhibit U).

Usage: python strategy_map.py strategy-map.csv [--out strategy-map.png] [--title "..."] [--json check.json]
CSV columns: id, perspective, objective, drives
  perspective: financial | customer | internal | learning   (also accepts "internal process",
               "learning and growth", "learning & growth")
  drives: ids of objectives this one leads to, separated by ';' (normally in the perspective above)
Checks: every non-financial objective drives something; every non-learning objective is driven by
something; links that point down or sideways are flagged.
"""
import csv, json, sys, textwrap

ORDER = ["learning", "internal", "customer", "financial"]          # bottom -> top
LABEL = {"financial": "Financial", "customer": "Customer", "internal": "Internal process",
         "learning": "Learning and growth"}
ALIAS = {"internal process": "internal", "learning and growth": "learning", "learning & growth": "learning",
         "l&g": "learning", "process": "internal", "finance": "financial"}
NAVY, GOLD, BAND, INK = "#1D3557", "#C9A55C", "#F3F1EC", "#1F2933"


def load(path):
    objs = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            i = (r.get("id") or "").strip()
            if not i:
                continue
            p = (r.get("perspective") or "").strip().lower()
            p = ALIAS.get(p, p)
            if p not in ORDER:
                sys.exit(f"ERROR: unknown perspective '{r.get('perspective')}' for {i}")
            objs.append({"id": i, "perspective": p, "objective": (r.get("objective") or "").strip(),
                         "drives": [x.strip() for x in (r.get("drives") or "").split(";") if x.strip()]})
    return objs


def check(objs):
    ids = {o["id"]: o for o in objs}
    driven = {o["id"]: [] for o in objs}
    issues = []
    for o in objs:
        for d in o["drives"]:
            if d not in ids:
                issues.append(f"{o['id']} drives unknown objective {d}")
                continue
            driven[d].append(o["id"])
            if ORDER.index(ids[d]["perspective"]) <= ORDER.index(o["perspective"]):
                issues.append(f"{o['id']} -> {d} does not point up a level")
    orphans_up = [o["id"] for o in objs if o["perspective"] != "financial" and not o["drives"]]
    orphans_down = [o["id"] for o in objs if o["perspective"] != "learning" and not driven[o["id"]]]
    covered = {p: sum(1 for o in objs if o["perspective"] == p) for p in ORDER}
    return {"objectives": len(objs), "per_perspective": covered,
            "missing_perspectives": [LABEL[p] for p in ORDER if covered[p] == 0],
            "drive_nothing": orphans_up, "driven_by_nothing": orphans_down, "link_issues": issues,
            "ok": not (orphans_up or orphans_down or issues) and all(covered.values())}


def draw(objs, path, title):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
    W, BH = 12.0, 1.9
    fig, ax = plt.subplots(figsize=(W, BH * 4 + 1.0))
    ax.set_xlim(0, W)
    ax.set_ylim(0, BH * 4 + 0.6)
    ax.axis("off")
    pos = {}
    for k, p in enumerate(ORDER):
        y0 = k * BH
        ax.add_patch(plt.Rectangle((0, y0 + 0.08), W, BH - 0.16, color=BAND, zorder=0))
        ax.text(0.15, y0 + BH / 2, LABEL[p], rotation=90, va="center", ha="center", fontsize=10,
                color=NAVY, fontweight="bold", family="DejaVu Sans")
        row = [o for o in objs if o["perspective"] == p]
        n = max(1, len(row))
        slot = (W - 0.6) / n
        for j, o in enumerate(row):
            cx = 0.6 + slot * (j + 0.5)
            bw, bh = min(slot - 0.3, 2.9), BH - 0.6
            ax.add_patch(FancyBboxPatch((cx - bw / 2, y0 + 0.3), bw, bh, boxstyle="round,pad=0.02,rounding_size=0.12",
                                        fc="white", ec=NAVY if p != "financial" else GOLD, lw=1.6, zorder=2))
            txt = "\n".join(textwrap.wrap(o["objective"] or o["id"], 26)[:3])
            ax.text(cx, y0 + 0.3 + bh / 2, txt, ha="center", va="center", fontsize=8.5, color=INK, zorder=3)
            ax.text(cx - bw / 2 + 0.08, y0 + 0.3 + bh - 0.12, o["id"], ha="left", va="top", fontsize=7,
                    color=GOLD if p == "financial" else NAVY, fontweight="bold", zorder=3)
            pos[o["id"]] = (cx, y0 + 0.3, y0 + 0.3 + bh)
    for o in objs:
        for d in o["drives"]:
            if d in pos and o["id"] in pos:
                x1, _, top = pos[o["id"]]
                x2, bot, _ = pos[d]
                ax.add_patch(FancyArrowPatch((x1, top), (x2, bot), arrowstyle="-|>", mutation_scale=11,
                                             color=NAVY, lw=1.1, alpha=0.75, zorder=1,
                                             connectionstyle="arc3,rad=0.0"))
    ax.text(W / 2, BH * 4 + 0.35, title, ha="center", va="center", fontsize=13, color=NAVY, fontweight="bold")
    fig.tight_layout()
    fig.savefig(path, dpi=170)
    plt.close(fig)


def main():
    a = sys.argv
    if len(a) < 2:
        sys.exit(__doc__)
    objs = load(a[1])
    res = check(objs)
    title = a[a.index("--title") + 1] if "--title" in a else "Strategy Map"
    if "--out" in a:
        draw(objs, a[a.index("--out") + 1], title)
        res["image"] = a[a.index("--out") + 1]
    txt = json.dumps(res, indent=2)
    if "--json" in a:
        open(a[a.index("--json") + 1], "w").write(txt)
    print(txt)


if __name__ == "__main__":
    main()
