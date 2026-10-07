#!/usr/bin/env python3
"""GLO-BUS weekly progress report (StratOS GLO-BUS Coach, Mode 5).

Usage: python weekly_report.py globus-capture-C-Y6.json globus-capture-C-Y7.json [...]
                               [--team C] [--out-dir report] [--title "Company C"] [--ledger ledger.json]
  --ledger: the team's ledger; if it holds a management brief (stratos-management-interview), the report
            adds a section comparing this round's results with management's goals and the team's takeaways.
Reads every capture file so far (stratos-globus-capture) and writes, for the latest year with results:
  weekly-report-Y<n>.html   one self-contained page with the graphs (open in a browser, print to PDF)
  weekly-report-Y<n>.docx   the same report in Word (needs python-docx; skipped if missing)
  weekly-report-Y<n>.json   the facts behind it, for the coach's narrative
Sections: the scorecard (KPIs vs investor expectations), the apparent strategic position by product,
progress graphs, where the team stands in the contest, what rivals changed (public reports only), what
to look out for next round, and questions for the team.

Rules built in: feedback, not recommendations. The report names the position the team's inputs reveal and
general things to watch; it never proposes decision values. Rival data comes only from the class-wide
reports every team can see (scoreboard_rows, cir_rows).
"""
import base64, html, io, json, os, sys

NAVY, GOLD, GREY, RED, GREEN = "#1E2761", "#FF6900", "#8A949E", "#C44536", "#2D936C"
PRODUCTS = [("camera", "Cameras"), ("drone", "Drones")]
CREDIT = ["AAA", "AA+", "AA", "AA-", "A+", "A", "A-", "BBB+", "BBB", "BBB-", "BB+", "BB", "BB-", "B+", "B", "B-",
          "CCC+", "CCC", "CCC-", "CC", "C"]

PRINCIPLES = {
    "Low-cost provider": "Low-cost providers win by keeping cost per unit at or below the industry low and pricing "
                         "below average, while holding quality at the minimum customers will accept.",
    "Differentiation": "Differentiators win when the quality, models, warranty and image they pay for earn a price "
                       "premium large enough to cover the extra cost, and when marketing makes the difference visible.",
    "Best-cost provider": "Best-cost providers offer above-average quality at an average or slightly lower price, so "
                          "costs must stay tightly controlled to fund both.",
    "Stuck in the middle": "A position with no clear cost or quality edge usually earns middling share and margins; "
                           "teams in this spot generally decide which edge they are building before the next round.",
    "Middle of the market": "A position close to the industry average on both price and quality has no edge yet; "
                            "the strategy shows up in which way the inputs move next.",
}


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def load(paths):
    caps = [json.load(open(p, encoding="utf-8")) for p in paths]
    caps.sort(key=lambda c: c.get("year", 0))
    return caps


def gap(a, b, pct=True):
    a, b = num(a), num(b)
    if a is None or b is None or (pct and b == 0):
        return None
    return a / b - 1 if pct else a - b


def classify(price_gap, pq_gap):
    if price_gap is None or pq_gap is None:
        return "Unclear", "unclear"
    if price_gap <= -0.05 and pq_gap <= 0.1:
        lab = "Low-cost provider"
        conf = "clear" if price_gap <= -0.08 else "mixed"
    elif price_gap >= 0.05 and pq_gap >= 0.2:
        lab = "Differentiation"
        conf = "clear" if price_gap >= 0.08 and pq_gap >= 0.3 else "mixed"
    elif price_gap < 0.05 and pq_gap >= 0.1:
        lab = "Best-cost provider"
        conf = "clear" if pq_gap >= 0.2 and price_gap <= 0 else "mixed"
    elif price_gap >= 0.05 and pq_gap < 0.2:
        lab = "Stuck in the middle"
        conf = "mixed"
    else:
        lab = "Middle of the market"
        conf = "mixed"
    return lab, conf


def norm_strategy(s):
    s = (s or "").lower()
    if "best" in s:
        return "Best-cost provider"
    if "low" in s:
        return "Low-cost provider"
    if "differ" in s:
        return "Differentiation"
    return None


def public_positions(cap):
    """Per company and product: average price, P/Q and share over the regions in the CIR."""
    agg = {}
    for r in cap.get("cir_rows") or []:
        agg.setdefault((str(r.get("company")), r.get("product")), []).append(r)
    out = {}
    for (co, prod), rows in agg.items():
        g = [x for x in rows if (x.get("region") or "Global").lower() == "global"] or rows
        f = lambda k: (sum(num(x.get(k)) for x in g if num(x.get(k)) is not None) /
                       max(1, sum(1 for x in g if num(x.get(k)) is not None))) if any(num(x.get(k)) is not None for x in g) else None
        out[(co, prod)] = {"price": f("price"), "pq": f("pq"), "share": f("share")}
    return out


def industry_avg(pos, prod):
    rows = [v for (co, p), v in pos.items() if p == prod and v["price"] is not None and v["pq"] is not None]
    if not rows:
        return None, None
    w = [v["share"] or 1 for v in rows]
    return (sum(v["price"] * x for v, x in zip(rows, w)) / sum(w), sum(v["pq"] * x for v, x in zip(rows, w)) / sum(w))


def group_of(price, pq, p_avg, q_avg):
    hi_p, hi_q = price > p_avg, pq >= q_avg
    return {(True, True): "Premium differentiator", (False, True): "Value leader",
            (False, False): "Low-cost / economy", (True, False): "Stuck in the middle"}[(hi_p, hi_q)]


# ---------- facts ----------
def build_facts(caps, team, brief=None):
    with_res = [c for c in caps if c.get("results")]
    if not with_res:
        sys.exit("ERROR: no capture file has results yet")
    cur = with_res[-1]
    prev = with_res[-2] if len(with_res) > 1 else None
    y = cur["year"]
    R = cur["results"]
    facts = {"team": team, "year": y, "years": [c["year"] for c in with_res], "kpis": [], "products": {},
             "contest": {}, "rivals": [], "watch": [], "questions": []}
    for k, lab in (("eps", "EPS"), ("roe", "ROE"), ("stock", "Stock price"), ("credit", "Credit rating"),
                   ("image", "Image rating")):
        d = (R.get("kpis") or {}).get(k) or {}
        a, t = d.get("actual"), d.get("target")
        if k == "credit":
            met = (a in CREDIT and t in CREDIT and CREDIT.index(a) <= CREDIT.index(t)) if a and t else None
        else:
            met = (num(a) >= num(t)) if num(a) is not None and num(t) is not None else None
        show = lambda v: (f"{num(v):.1%}" if k == "roe" and num(v) is not None else
                          f"${num(v):.2f}" if k in ("eps", "stock") and num(v) is not None else v)
        facts["kpis"].append({"key": k, "label": lab, "actual": show(a), "target": show(t), "met": met})
    co = R.get("company") or {}
    facts["contest"] = {"score": co.get("score"), "rank": co.get("rank"),
                        "prev_rank": ((prev or {}).get("results") or {}).get("company", {}).get("rank") if prev else None}
    sb = {str(r.get("company")): r for r in cur.get("scoreboard_rows") or []}
    if sb:
        ranked = sorted(sb.values(), key=lambda r: num(r.get("score")) or 0, reverse=True)
        facts["contest"]["leader"] = ranked[0].get("company")
        facts["contest"]["leader_score"] = ranked[0].get("score")
        facts["contest"]["n"] = len(sb)
    stated = {p: norm_strategy((cur.get("decisions") or {}).get(f"strategy.{p}")) for p, _ in PRODUCTS}
    pos_now, pos_prev = public_positions(cur), public_positions(prev) if prev else {}
    if not pos_prev and len(caps) > 1:
        prior = [c for c in caps if c.get("year", 0) < y and c.get("cir_rows")]
        pos_prev = public_positions(prior[-1]) if prior else {}
    for p, pl in PRODUCTS:
        r = ((R.get("product") or {}).get(p)) or {}
        rp = (((prev or {}).get("results") or {}).get("product") or {}).get(p) or {}
        pg, qg, cg = gap(r.get("price"), r.get("ind_price")), gap(r.get("pq"), r.get("ind_pq"), pct=False), \
            gap(r.get("cost_unit"), r.get("ind_cost_unit"))
        pg0, qg0, cg0 = gap(rp.get("price"), rp.get("ind_price")), gap(rp.get("pq"), rp.get("ind_pq"), pct=False), \
            gap(rp.get("cost_unit"), rp.get("ind_cost_unit"))
        lab, conf = classify(pg, qg)
        shares = [v for v in (r.get("share") or {}).values() if num(v) is not None]
        shares0 = [v for v in (rp.get("share") or {}).values() if num(v) is not None]
        share = sum(shares) / len(shares) if shares else None
        share0 = sum(shares0) / len(shares0) if shares0 else None
        focus = None
        if r.get("share") and shares and max(shares) - min(shares) >= 3:
            names = {"na": "North America", "ea": "Europe-Africa", "ap": "Asia-Pacific", "la": "Latin America"}
            top = max(r["share"], key=lambda k: num(r["share"][k]) or 0)
            focus = names.get(top, top)
        facts["products"][p] = {"label": pl, "apparent": lab, "confidence": conf, "stated": stated[p],
                                "price_gap": pg, "pq_gap": qg, "cost_gap": cg, "price_gap_prev": pg0,
                                "pq_gap_prev": qg0, "cost_gap_prev": cg0, "share": share, "share_prev": share0,
                                "op_margin": num(r.get("op_margin")), "op_margin_prev": num(rp.get("op_margin")),
                                "strongest_region": focus}
        # rivals: public positions only
        pa, qa = industry_avg(pos_now, p)
        mine = pos_now.get((team, p))
        if pa and mine and mine["price"] is not None:
            my_group = group_of(mine["price"], mine["pq"], pa, qa)
            facts["products"][p]["group"] = my_group
            for (c2, p2), v in pos_now.items():
                if p2 != p or c2 == team or v["price"] is None:
                    continue
                g_now = group_of(v["price"], v["pq"], pa, qa)
                old = pos_prev.get((c2, p))
                pa0, qa0 = industry_avg(pos_prev, p) if pos_prev else (None, None)
                g_old = group_of(old["price"], old["pq"], pa0, qa0) if old and pa0 else None
                facts["rivals"].append({"company": c2, "product": p, "group": g_now, "group_prev": g_old,
                                        "price_change": gap(v["price"], (old or {}).get("price")),
                                        "pq_change": gap(v["pq"], (old or {}).get("pq"), pct=False),
                                        "share": v["share"], "share_change": gap(v["share"], (old or {}).get("share"), pct=False),
                                        "entered_your_group": g_now == my_group and g_old is not None and g_old != my_group,
                                        "score": num((sb.get(c2) or {}).get("score"))})
    facts["brief"] = brief_check(brief, R) if brief else None
    watch(facts, cur, prev)
    return facts


KPI_KEYS = {"eps": "eps", "roe": "roe", "stock price": "stock", "stock": "stock", "credit rating": "credit",
            "credit": "credit", "image rating": "image", "image": "image"}


def brief_check(b, R):
    out = {"central_problem": b.get("central_problem"), "goals": [], "takeaways": []}
    kp = R.get("kpis") or {}
    for i, gl in enumerate(b.get("goals") or []):
        if isinstance(gl, str):
            gl = {"text": gl}
        k = KPI_KEYS.get((gl.get("kpi") or "").strip().lower())
        row = {"id": gl.get("id") or f"B{i+1}", "text": gl.get("text") or gl.get("goal"), "kpi": gl.get("kpi"),
               "target": gl.get("target"), "actual": None, "status": "not measured here"}
        if k and kp.get(k):
            a, t_inv = kp[k].get("actual"), kp[k].get("target")
            tgt = num(gl.get("target"))
            row["actual"] = a
            if k == "credit":
                t_ = gl.get("target") if gl.get("target") in CREDIT else t_inv
                if a in CREDIT and t_ in CREDIT:
                    row["status"] = "met" if CREDIT.index(a) <= CREDIT.index(t_) else "missed"
                    row["target"] = row["target"] or t_
            else:
                t_ = tgt if tgt is not None else num(t_inv)
                if num(a) is not None and t_ is not None:
                    row["status"] = "met" if num(a) >= t_ else "missed"
                    if tgt is None:
                        row["target"] = f"investor expectation {t_inv}"
        out["goals"].append(row)
    for t in b.get("takeaways") or []:
        out["takeaways"].append(t if isinstance(t, dict) else {"text": t})
    return out


def watch(f, cur, prev):
    W, Q = f["watch"], f["questions"]
    add = lambda title, why, lesson: W.append({"title": title, "evidence": why, "lesson": lesson})
    for p, d in f["products"].items():
        pl = d["label"]
        if d["stated"] and d["apparent"] not in ("Unclear",) and d["stated"] != d["apparent"]:
            add(f"{pl}: the position your inputs show differs from the strategy you chose",
                f"You chose {d['stated'].lower()}; price {fmt_pct(d['price_gap'])} vs the industry and P/Q "
                f"{fmt_pts(d['pq_gap'])} stars put you closer to {d['apparent'].lower()}.",
                "Teams that drift between positions usually pay for both and get credit for neither. "
                "Decide whether the drift is deliberate.")
            Q.append(f"Is the {pl.lower()} position your inputs now show the one you meant to build?")
        if d["apparent"] == "Low-cost provider" and d["cost_gap"] is not None and d["cost_gap"] > -0.02:
            add(f"{pl}: the cost advantage is thin",
                f"Cost per unit is {fmt_pct(d['cost_gap'])} vs the industry while price is {fmt_pct(d['price_gap'])}.",
                PRINCIPLES["Low-cost provider"])
        if d["apparent"] in ("Differentiation", "Best-cost provider") and d["pq_gap"] is not None and \
                d["pq_gap_prev"] is not None and d["pq_gap"] < d["pq_gap_prev"] - 0.05:
            add(f"{pl}: the quality edge is narrowing",
                f"P/Q lead over the industry went from {fmt_pts(d['pq_gap_prev'])} to {fmt_pts(d['pq_gap'])} stars.",
                PRINCIPLES[d["apparent"]])
        if d["cost_gap"] is not None and d["cost_gap_prev"] is not None and d["cost_gap"] > d["cost_gap_prev"] + 0.02:
            add(f"{pl}: cost per unit is rising relative to the industry",
                f"From {fmt_pct(d['cost_gap_prev'])} to {fmt_pct(d['cost_gap'])} vs the industry average.",
                "Whatever the strategy, a widening cost gap has to be earned back in price or volume.")
        if d["share"] is not None and d["share_prev"] is not None and d["share"] < d["share_prev"] - 0.3:
            add(f"{pl}: market share slipped",
                f"Average share across regions fell from {d['share_prev']:.1f}% to {d['share']:.1f}%.",
                "Share usually moves because rivals changed price, P/Q or marketing more than you did; "
                "the CIR shows which.")
        if d["op_margin"] is not None and d["op_margin_prev"] is not None and d["op_margin"] < d["op_margin_prev"] - 0.01:
            add(f"{pl}: operating margin fell",
                f"From {d['op_margin_prev']:.1%} to {d['op_margin']:.1%}.",
                "A falling margin with flat or rising share often means the volume was bought; check which costs grew.")
    covered = {KPI_KEYS.get((gl.get("kpi") or "").strip().lower()) for gl in ((f.get("brief") or {}).get("goals") or [])
               if gl["status"] in ("met", "missed")}
    for k in f["kpis"]:
        if k["met"] is False and k["key"] in ("eps", "image", "credit") and k["key"] not in covered:
            add(f"{k['label']} below investor expectations",
                f"{k['label']}: {k['actual']} against an expectation of {k['target']}.",
                {"eps": "EPS is scored directly; it reflects price, cost and volume together, so look for which of "
                        "the three moved against you.",
                 "image": "Image rating builds slowly from P/Q, models, warranty, advertising and CSR; it is hard "
                          "to recover quickly once it falls behind.",
                 "credit": "Credit rating follows debt, interest coverage and cash; it also affects borrowing costs."}[k["key"]])
    c = f["contest"]
    if c.get("rank") and c.get("prev_rank") and c["rank"] > c["prev_rank"]:
        add("You lost ground in the standings", f"Rank went from {c['prev_rank']} to {c['rank']}.",
            "Rank is relative: rivals' moves matter as much as yours. The Rivals section shows who moved.")
    for r in f["rivals"]:
        if r["entered_your_group"]:
            add(f"Company {r['company']} moved into your {r['product']} group",
                f"It is now in the {r['group'].lower()} group with you (price {fmt_pct(r['price_change'])}, "
                f"P/Q {fmt_pts(r['pq_change'])} stars vs last year).",
                "When a rival moves onto your ground, price pressure in that group usually rises. Watch its "
                "next move and what it does to your share.")
    for gl in ((f.get("brief") or {}).get("goals") or []):
        if gl["status"] == "missed":
            add(f"Management goal {gl['id']} missed: {gl['text']}",
                f"{gl['kpi']}: {gl['actual']} against {gl['target']}. This goal came from your management interview.",
                {"eps": "EPS reflects price, cost and volume together; look for which of the three moved against you.",
                 "credit": "Credit rating follows debt, interest coverage and cash; it also sets borrowing costs.",
                 "image": "Image rating builds slowly from P/Q, models, warranty, advertising and CSR."}.get(
                    KPI_KEYS.get((gl.get("kpi") or "").strip().lower()),
                    "The question is whether the team's position can still reach it."))
    if not Q:
        Q.append("Which one result from this year surprised the team most, and what does it say about your assumptions?")
    Q.append("Which input did you change most this year, and did the result move the way the projections said?")
    if any(w["title"].endswith("thin") or "cost" in w["title"] for w in W):
        Q.append("Which cost lines grew fastest this year, and are they ones customers notice?")
    f["questions"] = Q[:3]


def fmt_pct(x):
    return "n/a" if x is None else f"{x:+.1%}"


def fmt_pts(x):
    return "n/a" if x is None else f"{x:+.1f}"


# ---------- charts ----------
def charts(caps, facts, team):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.spines.top": False,
                         "axes.spines.right": False, "axes.edgecolor": "#C8CDD3", "axes.titleweight": "bold",
                         "axes.titlecolor": NAVY, "axes.titlesize": 10})
    res = [c for c in caps if c.get("results")]
    ys = [c["year"] for c in res]
    out = {}

    def save(fig, name):
        b = io.BytesIO()
        fig.savefig(b, format="png", dpi=150, bbox_inches="tight")
        plt.close(fig)
        out[name] = b.getvalue()

    def series(path):
        v = []
        for c in res:
            d = c["results"]
            for k in path:
                d = (d or {}).get(k) if isinstance(d, dict) else None
            v.append(num(d))
        return v

    # 1 KPIs vs expectations
    fig, axs = plt.subplots(1, 4, figsize=(11, 2.4))
    for ax, (k, lab, f_) in zip(axs, [("eps", "EPS ($)", "{:.2f}"), ("roe", "ROE", "{:.0%}"),
                                      ("stock", "Stock price ($)", "{:.0f}"), ("image", "Image rating", "{:.0f}")]):
        a, t = series(["kpis", k, "actual"]), series(["kpis", k, "target"])
        ax.plot(ys, a, color=NAVY, lw=2.2, marker="o", label="You")
        ax.plot(ys, t, color=GOLD, lw=1.6, ls="--", marker="o", ms=3, label="Investor expectation")
        ax.set_title(lab)
        ax.set_xticks(ys)
        ax.set_xticklabels([f"Y{y}" for y in ys])
        if k == "roe":
            ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=1))
    axs[0].legend(frameon=False, fontsize=7, loc="upper left")
    save(fig, "kpis")
    fig, axs = plt.subplots(2, 2, figsize=(7, 4.6))
    for ax, (k, lab) in zip(axs.flat, [("eps", "EPS ($)"), ("roe", "ROE"), ("stock", "Stock price ($)"), ("image", "Image rating")]):
        ax.plot(ys, series(["kpis", k, "actual"]), color=NAVY, lw=2.2, marker="o", label="You")
        ax.plot(ys, series(["kpis", k, "target"]), color=GOLD, lw=1.6, ls="--", marker="o", ms=3, label="Expectation")
        ax.set_title(lab)
        ax.set_xticks(ys)
        ax.set_xticklabels([f"Y{y}" for y in ys])
        if k == "roe":
            ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=1))
    axs[0][0].legend(frameon=False, fontsize=7)
    fig.tight_layout()
    save(fig, "kpis_grid")

    # 2 position vs industry: price, P/Q, cost per unit
    fig, axs = plt.subplots(1, 3, figsize=(11, 2.6))
    for p, pl in PRODUCTS:
        col = NAVY if p == "camera" else GOLD
        pr = series(["product", p, "price"]); ip = series(["product", p, "ind_price"])
        q = series(["product", p, "pq"]); iq = series(["product", p, "ind_pq"])
        cu = series(["product", p, "cost_unit"]); ic = series(["product", p, "ind_cost_unit"])
        axs[0].plot(ys, [a / b - 1 if a and b else None for a, b in zip(pr, ip)], color=col, lw=2, marker="o", label=pl)
        axs[1].plot(ys, [a - b if a is not None and b is not None else None for a, b in zip(q, iq)], color=col, lw=2, marker="o", label=pl)
        axs[2].plot(ys, [a / b - 1 if a and b else None for a, b in zip(cu, ic)], color=col, lw=2, marker="o", label=pl)
    for ax, t in zip(axs, ["Price vs industry average", "P/Q vs industry (stars)", "Cost per unit vs industry"]):
        ax.axhline(0, color=GREY, lw=0.8)
        ax.set_title(t)
        ax.set_xticks(ys)
        ax.set_xticklabels([f"Y{y}" for y in ys])
    for ax in (axs[0], axs[2]):
        ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=0))
    axs[0].legend(frameon=False, fontsize=7)
    save(fig, "position_trend")

    # 3 share and margin
    fig, axs = plt.subplots(1, 2, figsize=(11, 2.4))
    for p, pl in PRODUCTS:
        col = NAVY if p == "camera" else GOLD
        sh = []
        for c in res:
            s = ((c["results"].get("product") or {}).get(p) or {}).get("share") or {}
            v = [num(x) for x in s.values() if num(x) is not None]
            sh.append(sum(v) / len(v) if v else None)
        axs[0].plot(ys, sh, color=col, lw=2, marker="o", label=pl)
        axs[1].plot(ys, series(["product", p, "op_margin"]), color=col, lw=2, marker="o", label=pl)
    axs[0].set_title("Market share (average of regions, %)")
    axs[1].set_title("Operating margin")
    axs[1].yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=0))
    for ax in axs:
        ax.set_xticks(ys)
        ax.set_xticklabels([f"Y{y}" for y in ys])
    axs[0].legend(frameon=False, fontsize=7)
    save(fig, "share_margin")

    # 4 contest: scores by company
    sb_years = [c for c in caps if c.get("scoreboard_rows")]
    if sb_years:
        fig, ax = plt.subplots(figsize=(8, 4.2))
        comps = sorted({str(r["company"]) for c in sb_years for r in c["scoreboard_rows"]})
        yy = [c["year"] for c in sb_years]
        for co in comps:
            v = [num(next((r.get("score") for r in c["scoreboard_rows"] if str(r["company"]) == co), None)) for c in sb_years]
            mine = co == team
            ax.plot(yy, v, color=GOLD if mine else "#B8C2CC", lw=3 if mine else 1.2, marker="o", ms=5 if mine else 3,
                    zorder=3 if mine else 1)
            if v[-1] is not None:
                ax.annotate(f"{co}{' (you)' if mine else ''}", (yy[-1], v[-1]), xytext=(6, 0), textcoords="offset points",
                            va="center", fontsize=8, color=NAVY if mine else GREY, fontweight="bold" if mine else "normal")
        ax.set_title("Overall score by company (class scoreboard)")
        ax.set_xticks(yy)
        ax.set_xticklabels([f"Y{y}" for y in yy])
        ax.set_xlim(yy[0] - 0.2, yy[-1] + 0.5)
        save(fig, "contest")

    # 5 position maps from the CIR (latest year, arrows from the year before)
    cir_caps = [c for c in caps if c.get("cir_rows")]
    if cir_caps:
        now = public_positions(cir_caps[-1])
        before = public_positions(cir_caps[-2]) if len(cir_caps) > 1 else {}
        fig, axs = plt.subplots(1, 2, figsize=(11, 3.6))
        for ax, (p, pl) in zip(axs, PRODUCTS):
            pa, qa = industry_avg(now, p)
            if pa is None:
                ax.set_visible(False)
                continue
            for (co, p2), v in now.items():
                if p2 != p or v["price"] is None:
                    continue
                mine = co == team
                old = before.get((co, p))
                if old and old["price"] is not None:
                    ax.annotate("", xy=(v["pq"], v["price"]), xytext=(old["pq"], old["price"]),
                                arrowprops=dict(arrowstyle="->", color=GOLD if mine else "#C8CDD3", lw=1.4 if mine else 0.8))
                ax.scatter(v["pq"], v["price"], s=40 + 18 * (v["share"] or 10), color=GOLD if mine else NAVY,
                           alpha=0.95 if mine else 0.55, edgecolor="white", zorder=3)
                ax.annotate(co, (v["pq"], v["price"]), ha="center", va="center", fontsize=8, color="white",
                            fontweight="bold", zorder=4)
            ax.axvline(qa, color=GREY, lw=0.8, ls=":")
            ax.axhline(pa, color=GREY, lw=0.8, ls=":")
            ax.set_xlabel("P/Q rating (stars)")
            ax.set_ylabel("Price ($)")
            ax.set_title(f"{pl}: positions in Year {cir_caps[-1]['year']} (arrows from Year {cir_caps[-2]['year']})"
                         if before else f"{pl}: positions in Year {cir_caps[-1]['year']}")
            for txt, xa, ya, ha, va in (("Premium", 0.98, 0.98, "right", "top"), ("Value", 0.98, 0.02, "right", "bottom"),
                                        ("Economy", 0.02, 0.02, "left", "bottom"), ("Overpriced", 0.02, 0.98, "left", "top")):
                ax.text(xa, ya, txt, transform=ax.transAxes, ha=ha, va=va, fontsize=7, color=GREY)
        save(fig, "maps")
    return out


# ---------- report ----------
def sections(f):
    """Text blocks shared by the HTML and Word versions."""
    c = f["contest"]
    snap = []
    if c.get("rank"):
        s = f"Rank {c['rank']}" + (f" of {c['n']}" if c.get("n") else "") + f", overall score {c.get('score')}"
        if c.get("prev_rank"):
            s += f" (rank {c['prev_rank']} last year)"
        if c.get("leader") and c.get("leader") != f["team"]:
            s += f". Leader: Company {c['leader']} at {c.get('leader_score')}."
        snap.append(s)
    pos = []
    for p, d in f["products"].items():
        t = (f"{d['label']}: your inputs look like a **{d['apparent'].lower()}** position ({d['confidence']}). "
             f"Price {fmt_pct(d['price_gap'])} vs the industry, P/Q {fmt_pts(d['pq_gap'])} stars, cost per unit "
             f"{fmt_pct(d['cost_gap'])}.")
        if d.get("group"):
            t += f" On the competitor report you sit in the {d['group'].lower()} group."
        if d.get("strongest_region"):
            t += f" Your strongest region is {d['strongest_region']}."
        if d["stated"]:
            t += (" That matches the strategy you chose." if d["stated"] == d["apparent"]
                  else f" You chose {d['stated'].lower()}.")
        t += " " + PRINCIPLES.get(d["apparent"], "")
        pos.append(t)
    riv = []
    for r in sorted(f["rivals"], key=lambda r: -(abs(r["price_change"] or 0) + abs(r["pq_change"] or 0) / 5))[:5]:
        if r["price_change"] is None:
            continue
        riv.append(f"Company {r['company']} ({r['product']}s): price {fmt_pct(r['price_change'])}, P/Q "
                   f"{fmt_pts(r['pq_change'])} stars, share {fmt_pts(r['share_change'])} points; now in the "
                   f"{r['group'].lower()} group" + (" (moved into yours)" if r["entered_your_group"] else "") + ".")
    br = []
    b = f.get("brief")
    if b:
        if b.get("central_problem"):
            br.append(f"Central problem from your management interview: {b['central_problem']}")
        for gl in b["goals"]:
            st = {"met": "met", "missed": "missed", "not measured here": "not measured in this report"}[gl["status"]]
            br.append(f"{gl['id']}. {gl['text']}" + (f" ({gl['kpi']}: {gl['actual']} vs {gl['target']}): {st}."
                                                     if gl["actual"] is not None else f": {st}."))
        for i, t in enumerate(b["takeaways"]):
            br.append(f"K{i+1}. {t.get('text')}" + (f" (check: {t['check']})" if t.get("check") else ""))
    return snap, pos, riv, br


def md_bold(t):
    import re
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", html.escape(t))


def write_html(f, imgs, path, title):
    snap, pos, riv, br = sections(f)
    img = lambda k: (f'<img src="data:image/png;base64,{base64.b64encode(imgs[k]).decode()}" alt="{k}">' if k in imgs else "")
    krows = "".join(
        f"<tr><td>{html.escape(k['label'])}</td><td>{html.escape(str(k['actual']))}</td><td>{html.escape(str(k['target']))}</td>"
        f"<td class='{'ok' if k['met'] else ('no' if k['met'] is False else '')}'>"
        f"{'Met' if k['met'] else ('Below' if k['met'] is False else 'n/a')}</td></tr>" for k in f["kpis"])
    watch = "".join(f"<li><b>{html.escape(w['title'])}.</b> {html.escape(w['evidence'])} <i>{html.escape(w['lesson'])}</i></li>"
                    for w in f["watch"]) or "<li>Nothing stands out against your position this round.</li>"
    qs = "".join(f"<li>{html.escape(q)}</li>" for q in f["questions"])
    page = f"""<!doctype html><html><head><meta charset="utf-8"><title>{html.escape(title)}</title>
<style>body{{font-family:Arial,sans-serif;color:#1F2933;max-width:980px;margin:24px auto;padding:0 16px;line-height:1.45}}
h1{{font-family:Cambria,Georgia,serif;color:{NAVY};margin-bottom:2px}}h2{{font-family:Cambria,Georgia,serif;color:{NAVY};
border-bottom:2px solid {GOLD};padding-bottom:3px;margin-top:28px}}.sub{{color:#B5651D;font-weight:bold}}
table{{border-collapse:collapse}}td,th{{border:1px solid #C8CDD3;padding:4px 10px}}th{{background:{NAVY};color:#fff}}
.ok{{background:#D8F0DF}}.no{{background:#F8D7D3}}img{{max-width:100%}}.note{{color:#5F6B76;font-size:12px}}
li{{margin-bottom:6px}}</style></head><body>
<h1>{html.escape(title)}</h1><div class="sub">GLO-BUS weekly report · Year {f['year']} results · StratOS</div>
<p class="note">Feedback, not recommendations: this report names the position your inputs reveal and general things to
watch. Every decision is your team's. Rival figures come only from the class-wide reports every team can see.</p>
<h2>1. Your scorecard</h2>{''.join(f'<p>{html.escape(s)}</p>' for s in snap)}
<table><tr><th>Scored measure</th><th>You</th><th>Investor expectation</th><th></th></tr>{krows}</table>
{img('kpis')}
<h2>2. The position you've taken</h2>{''.join(f'<p>{md_bold(t)}</p>' for t in pos)}{img('maps')}{img('position_trend')}
{('<h2>Against your management brief</h2><ul>' + ''.join(f'<li>{html.escape(x)}</li>' for x in br) + '</ul>') if br else ''}
<h2>3. Progress</h2>{img('share_margin')}
<h2>4. Where you stand in the contest</h2>{img('contest')}
{'<p><b>What rivals changed since last year</b> (from the competitor report):</p><ul>' + ''.join(f'<li>{html.escape(r)}</li>' for r in riv) + '</ul>' if riv else ''}
<h2>5. What to look out for next round</h2><ul>{watch}</ul>
<h2>6. Questions for your team</h2><ol>{qs}</ol>
<p class="note">StratOS Strategy Lab · ©2026 G. Bradley Scheller · Generated by weekly_report.py</p></body></html>"""
    open(path, "w", encoding="utf-8").write(page)


# ---------- headline sentences (action titles) ----------
def headlines(f):
    c, y, team = f["contest"], f["year"], f["team"]
    P = f["products"]
    met = sum(1 for k in f["kpis"] if k["met"])
    ap = {p: d["apparent"].lower() for p, d in P.items()}
    if len(set(ap.values())) == 1:
        pos = f"a {list(ap.values())[0]} position in both products"
    else:
        pos = "; ".join(f"{d['label'].lower()} look like {d['apparent'].lower()}" for d in P.values())
    drift = [d for d in P.values() if d["stated"] and d["apparent"] != d["stated"]]
    H = {}
    rank = f"rank {c['rank']} of {c['n']}" if c.get("rank") and c.get("n") else (f"rank {c['rank']}" if c.get("rank") else "")
    H["title"] = f"Company {team} after Year {y}: {rank}" + (" — is the position paying off?" if rank else "")
    lead = f"{rank.capitalize()} with {pos}" if rank else pos.capitalize()
    H["summary"] = lead + (f"; {drift[0]['label'].lower()} have drifted from the strategy you chose" if drift else "")
    miss = [k for k in f["kpis"] if k["met"] is False]
    H["scorecard"] = f"{met} of {len(f['kpis'])} scored measures met investor expectations in Year {y}" + (
        f"; {miss[0]['label']} fell short ({miss[0]['actual']} vs {miss[0]['target']})" if miss else "")
    bits = []
    for d in P.values():
        if d["stated"] and d["apparent"] != d["stated"]:
            bits.append(f"{d['label']} have drifted toward {d['apparent'].lower()}")
        else:
            bits.append(f"{d['label']} read as {d['apparent'].lower()}" + (" (as chosen)" if d["stated"] else ""))
    H["position"] = "; ".join(b if i == 0 else b[0].lower() + b[1:] for i, b in enumerate(bits))
    cg = [(d["label"], d["cost_gap"]) for d in P.values() if d["cost_gap"] is not None]
    H["trend"] = ("Cost per unit vs the industry: " + ", ".join(f"{l.lower()} {fmt_pct(v)}" for l, v in cg)
                  + " — the number that decides whether the position pays") if cg else "Price, quality and cost against the industry"
    if c.get("leader") and c.get("leader") != team and c.get("leader_score") is not None and c.get("score") is not None:
        H["contest"] = f"{rank.capitalize()}, {num(c['leader_score']) - num(c['score']):.0f} points behind Company {c['leader']}"
    elif c.get("leader") == team:
        H["contest"] = f"Company {team} leads the industry after Year {y}"
    else:
        H["contest"] = "Where you stand against the other companies"
    movers = [r for r in f["rivals"] if r["price_change"] is not None]
    if movers:
        m = max(movers, key=lambda r: abs(r["price_change"] or 0) + abs(r["pq_change"] or 0) / 5)
        H["contest"] += f"; Company {m['company']} moved most in {m['product']}s"
    H["watch"] = f"{len(f['watch'])} things to watch before the Year {y + 1} decisions" if f["watch"] else \
        f"Nothing stands out against your position before Year {y + 1}"
    if f.get("brief"):
        gm = [gl for gl in f["brief"]["goals"] if gl["status"] == "missed"]
        H["brief"] = (f"{len(gm)} of {len(f['brief']['goals'])} goals from your management interview missed this round"
                      if gm else "Your results are on track against the goals management set")
    H["questions"] = f"Questions for the team before Year {y + 1}"
    return H


def source_line(caps_years, f):
    return (f"Source: GLO-BUS captures, Years {caps_years[0]}–{caps_years[-1]} (company reports, class scoreboard, "
            f"Competitive Intelligence Report); StratOS weekly_report.py" if len(caps_years) > 1 else
            f"Source: GLO-BUS capture, Year {caps_years[0]}; StratOS weekly_report.py")


# ---------- Word memo (exhibit style) ----------
def write_memo(f, imgs, path, title):
    try:
        import docx
        from docx.shared import Pt, RGBColor, Inches
        from docx.enum.table import WD_TABLE_ALIGNMENT
        from docx.oxml import OxmlElement
        from docx.oxml.ns import qn
    except ImportError:
        return False
    H = headlines(f)
    snap, pos, riv, br = sections(f)
    d = docx.Document()
    for s in d.sections:
        s.left_margin = s.right_margin = Inches(0.9)
        s.top_margin = s.bottom_margin = Inches(0.8)
    st = d.styles["Normal"]
    st.font.name, st.font.size = "Calibri", Pt(10.5)
    navy, orange, muted = RGBColor(0x1E, 0x27, 0x61), RGBColor(0xFF, 0x69, 0x00), RGBColor(0x6B, 0x72, 0x80)

    def h(t, size=14, color=navy):
        p = d.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        r = p.add_run(t)
        r.bold, r.font.size, r.font.name, r.font.color.rgb = True, Pt(size), "Cambria", color
        return p

    def para(t, italic=False, size=None, color=None):
        p = d.add_paragraph()
        for i, part in enumerate(t.split("**")):
            r = p.add_run(part)
            r.bold = i % 2 == 1
            r.italic = italic
            if size:
                r.font.size = Pt(size)
            if color:
                r.font.color.rgb = color
        return p

    def shade(cell, hexcol):
        tcPr = cell._tc.get_or_add_tcPr()
        sh = OxmlElement("w:shd")
        sh.set(qn("w:val"), "clear"); sh.set(qn("w:color"), "auto"); sh.set(qn("w:fill"), hexcol)
        tcPr.append(sh)

    def table(rows, widths=None, head_fill="1E2761"):
        t = d.add_table(rows=len(rows), cols=len(rows[0]))
        t.style = "Table Grid"
        t.alignment = WD_TABLE_ALIGNMENT.LEFT
        for i, row in enumerate(rows):
            for j, v in enumerate(row):
                cell = t.cell(i, j)
                cell.text = "" if v is None else str(v)
                for p in cell.paragraphs:
                    for r in p.runs:
                        r.font.size = Pt(9.5)
                        if i == 0:
                            r.bold, r.font.color.rgb = True, RGBColor(0xFF, 0xFF, 0xFF)
                if i == 0:
                    shade(cell, head_fill)
                if widths:
                    cell.width = Inches(widths[j])
        return t

    def pic(k, w=6.7):
        if k in imgs:
            d.add_picture(io.BytesIO(imgs[k]), width=Inches(w))

    def impact():
        p = para("Impact Summary — the team writes this:", size=10, color=navy)
        p.runs[0].bold = True
        para("[In two or three sentences: what this tells you about your position, and what you will discuss before "
             "entering next year's decisions.]", italic=True, color=muted)

    y = f["year"]
    h(f"GLO-BUS Weekly Review — {title} (Year {y} results)", 18)
    para(f"StratOS GLO-BUS Coach output. Feedback, not recommendations: it names the position your inputs reveal and "
         f"what to watch; every decision is your team's. Rival figures come only from the class-wide reports "
         f"(scoreboard, Competitive Intelligence Report).", italic=True, size=9.5, color=muted)
    para(f"**In one line:** {H['summary']}.")
    table([["Section", "What it shows"], ["W1. Scorecard", H["scorecard"]], ["W2. Position", H["position"]],
           ["W3. Progress", H["trend"]], ["W4. Contest", H["contest"]]] +
          ([["W5. Management brief", H["brief"]]] if f.get("brief") else []) +
          [["W6. Watch list", H["watch"]], ["W7. Questions", H["questions"]]], [1.6, 5.1])
    h("W1. Scorecard")
    para(H["scorecard"] + ".")
    for s in snap:
        para(s)
    table([["Scored measure", "You", "Investor expectation", "Result"]] +
          [[k["label"], k["actual"], k["target"], "Met" if k["met"] else ("Below" if k["met"] is False else "n/a")]
           for k in f["kpis"]], [2.2, 1.3, 1.9, 1.3])
    pic("kpis")
    impact()
    h("W2. The position you've taken")
    para(H["position"] + ".")
    table([["Product", "Apparent position", "Chosen strategy", "Price vs industry", "P/Q vs industry", "Cost vs industry", "Group (CIR)"]] +
          [[d_["label"], f"{d_['apparent']} ({d_['confidence']})", d_["stated"] or "not recorded", fmt_pct(d_["price_gap"]),
            fmt_pts(d_["pq_gap"]) + " stars", fmt_pct(d_["cost_gap"]), d_.get("group") or ""] for d_ in f["products"].values()],
          [0.8, 1.3, 1.0, 0.9, 0.9, 0.9, 1.0])
    for t in pos:
        para(t)
    pic("maps")
    impact()
    h("W3. Progress")
    para(H["trend"] + ".")
    pic("position_trend")
    pic("share_margin")
    impact()
    h("W4. Where you stand in the contest")
    para(H["contest"] + ".")
    pic("contest", 6.3)
    if riv:
        para("**What rivals changed since last year** (Competitive Intelligence Report):")
        for s in riv:
            d.add_paragraph(s, style="List Bullet")
    impact()
    if br:
        h("W5. Against your management brief")
        para(H["brief"] + ".")
        gl = f["brief"]["goals"]
        if gl:
            table([["Goal", "Measure", "This round", "Target", "Status"]] +
                  [[f"{g_['id']}. {g_['text']}", g_.get("kpi") or "", g_["actual"] if g_["actual"] is not None else "",
                    g_.get("target") or "", g_["status"]] for g_ in gl], [2.6, 1.1, 0.9, 1.3, 0.8])
        for t in f["brief"]["takeaways"]:
            d.add_paragraph(f"{t.get('text')}" + (f" (check: {t['check']})" if t.get("check") else ""), style="List Bullet")
    h("W6. What to look out for next round")
    para(H["watch"] + ".")
    if f["watch"]:
        table([["Watch item", "Evidence", "General lesson"]] +
              [[w["title"], w["evidence"], w["lesson"]] for w in f["watch"]], [2.0, 2.3, 2.4])
    h("W7. Questions for the team")
    for q in f["questions"]:
        d.add_paragraph(q, style="List Number")
    h("Sources", 12)
    para(source_line(f["years"], f), size=9.5, color=muted)
    d.save(path)
    return True


# ---------- PowerPoint deck (executive style, action titles, notes) ----------
def write_deck(f, imgs, path, title):
    try:
        from pptx import Presentation
        from pptx.util import Inches, Pt, Emu
        from pptx.dml.color import RGBColor
        from pptx.enum.shapes import MSO_SHAPE
        from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    except ImportError:
        return False
    H = headlines(f)
    snap, pos, riv, br = sections(f)
    NV, OR, PN, INK, MU, WH = (RGBColor(0x1E, 0x27, 0x61), RGBColor(0xFF, 0x69, 0x00), RGBColor(0xF7, 0xF8, 0xFA),
                               RGBColor(0x22, 0x28, 0x31), RGBColor(0x6B, 0x72, 0x80), RGBColor(0xFF, 0xFF, 0xFF))
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(10), Inches(5.625)
    blank = prs.slide_layouts[6]
    src = source_line(f["years"], f)

    def text(slide, x, y, w, h, t, size=12, bold=False, color=INK, font="Calibri", align=None, anchor=None):
        tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = True
        if anchor:
            tf.vertical_anchor = anchor
        lines = t if isinstance(t, list) else [t]
        for i, ln in enumerate(lines):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            if align:
                p.alignment = align
            for j, part in enumerate(str(ln).split("**")):
                r = p.add_run()
                r.text = part
                r.font.size, r.font.name, r.font.color.rgb = Pt(size), font, color
                r.font.bold = bold or j % 2 == 1
        return tb

    def notes(slide, paras):
        tf = slide.notes_slide.notes_text_frame
        for i, t in enumerate(paras):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            r = p.add_run()
            r.text = t
            r.font.size = Pt(16)
            r.font.name = "Calibri"

    def page(title_txt, note_paras):
        s = prs.slides.add_slide(blank)
        text(s, 0.45, 0.25, 9.1, 0.8, title_txt, 20, True, NV, "Cambria", anchor=MSO_ANCHOR.TOP)
        text(s, 0.45, 5.22, 9.1, 0.3, src, 7.5, False, MU)
        notes(s, note_paras)
        return s

    def picture(s, k, x, y, w=None, h=None):
        """Fit the image inside a w x h box, keeping its aspect ratio."""
        if k not in imgs:
            return 0
        from PIL import Image as _I
        iw, ih = _I.open(io.BytesIO(imgs[k])).size
        a = iw / ih
        W = w or (h * a)
        Hh = W / a
        if h and Hh > h:
            Hh, W = h, h * a
        s.shapes.add_picture(io.BytesIO(imgs[k]), Inches(x), Inches(y), Inches(W), Inches(Hh))
        return Hh

    def panel(s, x, y, w, h, fill=PN):
        sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        sh.fill.solid(); sh.fill.fore_color.rgb = fill
        sh.line.fill.background()
        sh.adjustments[0] = 0.06
        return sh

    y = f["year"]
    c = f["contest"]
    # 1 title
    s = prs.slides.add_slide(blank)
    bg = s.background.fill; bg.solid(); bg.fore_color.rgb = NV
    circ = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(8.3), Inches(-0.9), Inches(2.6), Inches(2.6))
    circ.fill.solid(); circ.fill.fore_color.rgb = OR; circ.line.fill.background()
    text(s, 0.6, 0.9, 7, 0.3, "STRATOS GLO-BUS WEEKLY REVIEW", 10, True, RGBColor(0xCA, 0xDC, 0xFC))
    text(s, 0.6, 1.35, 7.6, 1.6, H["title"], 28, True, WH, "Cambria")
    text(s, 0.6, 3.25, 8, 0.8, [f"{title} · Year {y} results · Cameras and drones, four regions",
                                "Feedback, not recommendations: every decision is the team's"], 11, False,
         RGBColor(0xCA, 0xDC, 0xFC))
    text(s, 0.6, 4.9, 8, 0.3, src, 8, False, RGBColor(0xCA, 0xDC, 0xFC))
    notes(s, [f"Purpose: a ten-minute read of how Company {f['team']} did in Year {y}, the position its inputs show, "
              f"where it stands against the other companies, and what to watch before the Year {y + 1} decisions.",
              "Everything comes from the team's own captured screens and the class-wide reports every team can see. "
              "Nothing here tells the team what to enter; it names the pattern and asks the questions.",
              "Likely question: why no recommended numbers? Answer: the course rule is that the team decides; the review "
              "is feedback on the strategy the inputs reveal."])
    # 2 governing thought
    s = page(H["summary"], [
        "This is the one-slide summary. Read the four points top to bottom: how you scored, what position your inputs "
        "show, where you stand, and the one thing to watch most.",
        "Likely question: which point matters most this round? Answer: the position. If the inputs have drifted from the "
        "strategy you chose, this is the round to decide whether that drift is deliberate."])
    pts = [("Scorecard", H["scorecard"]), ("Position", H["position"]), ("Contest", H["contest"]),
           ("Watch first", f["watch"][0]["title"] if f["watch"] else H["watch"])]
    for i, (hd, tx) in enumerate(pts):
        yy = 1.2 + i * 0.95
        panel(s, 0.45, yy, 9.1, 0.82)
        o = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.65), Inches(yy + 0.2), Inches(0.42), Inches(0.42))
        o.fill.solid(); o.fill.fore_color.rgb = NV if i < 3 else OR; o.line.fill.background()
        o.text_frame.text = str(i + 1)
        r = o.text_frame.paragraphs[0].runs[0]; r.font.size, r.font.bold, r.font.color.rgb = Pt(13), True, WH
        o.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        text(s, 1.3, yy + 0.08, 8.1, 0.7, [f"**{hd}**", tx], 11.5)
    # 3 scorecard
    s = page(H["scorecard"], [
        "The five scored measures against investor expectations, this year and the trend since the first round.",
        " ".join(snap),
        "Likely question: why did a measure miss when we improved? Answer: expectations rise each year; improvement "
        "that does not keep pace still shows as a miss."])
    rows = [["Scored measure", "You", "Expectation", ""]] + [[k["label"], k["actual"], k["target"],
                                                               "Met" if k["met"] else ("Below" if k["met"] is False else "n/a")] for k in f["kpis"]]
    tbl = s.shapes.add_table(len(rows), 4, Inches(0.45), Inches(1.2), Inches(3.6), Inches(0.3 * len(rows))).table
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            cell = tbl.cell(i, j)
            cell.text = str(v)
            para_ = cell.text_frame.paragraphs[0]
            for r in para_.runs:
                r.font.size, r.font.name = Pt(10), "Calibri"
                r.font.color.rgb = WH if i == 0 else INK
                r.font.bold = i == 0
            cell.fill.solid()
            cell.fill.fore_color.rgb = NV if i == 0 else (RGBColor(0xD8, 0xF0, 0xDF) if v == "Met" else
                                                          RGBColor(0xF8, 0xD7, 0xD3) if v == "Below" else WH)
    tbl.columns[0].width = Inches(1.45)
    for j in (1, 2, 3):
        tbl.columns[j].width = Inches(0.72)
    picture(s, "kpis_grid", 4.25, 1.15, w=5.3, h=3.95)
    # 4 position
    s = page(H["position"], pos + ["Likely question: is the label fixed? Answer: no. It reads the pattern of price, "
                                   "P/Q and cost against the industry this year; it moves when the inputs move."])
    picture(s, "maps", 0.45, 1.2, w=9.1, h=3.9)
    # 5 trend
    s = page(H["trend"], [
        "Three lines per product against the industry average: price premium, P/Q lead and cost per unit gap. A strategy "
        "pays when the gaps line up with it: a low-cost provider needs a negative cost gap, a differentiator needs a price "
        "premium that covers its cost gap.",
        "Likely question: which line matters most? Answer: the cost gap, because it decides whether the price you charge "
        "earns a margin."])
    hh = picture(s, "position_trend", 0.45, 1.15, w=9.1, h=2.05)
    picture(s, "share_margin", 0.45, 1.2 + hh, w=9.1, h=5.1 - (1.2 + hh))
    # 6 contest
    s = page(H["contest"], [
        "Every company's overall score from the class scoreboard, year by year, with your line highlighted, and the "
        "biggest moves rivals made on the competitor report.",
        "Likely question: did we use other teams' data? Answer: only what the class-wide reports show every team."])
    picture(s, "contest", 0.45, 1.15, w=5.6, h=3.9)
    panel(s, 6.25, 1.15, 3.3, 3.9)
    text(s, 6.4, 1.25, 3.05, 3.7, ["**What rivals changed**"] + (riv[:4] or ["No prior year to compare."]), 8.5)
    # 7 brief
    if br:
        s = page(H["brief"], ["The goals and takeaways from your management interview, checked against this round's "
                              "results. A miss is information: the question is whether your position can still reach "
                              "the goal.", "Likely question: can we change a goal? Answer: only management can; you can "
                              "explain why your strategy departs from it."])
        gl = f["brief"]["goals"]
        rows = [["Goal", "Measure", "This round", "Target", "Status"]] + [
            [f"{g_['id']}. {g_['text']}", g_.get("kpi") or "", str(g_["actual"] if g_["actual"] is not None else ""),
             str(g_.get("target") or ""), g_["status"]] for g_ in gl]
        tbl = s.shapes.add_table(len(rows), 5, Inches(0.45), Inches(1.2), Inches(9.1), Inches(0.34 * len(rows))).table
        for i, row in enumerate(rows):
            for j, v in enumerate(row):
                cell = tbl.cell(i, j)
                cell.text = v
                for r in cell.text_frame.paragraphs[0].runs:
                    r.font.size, r.font.name, r.font.bold = Pt(10), "Calibri", i == 0
                    r.font.color.rgb = WH if i == 0 else INK
                cell.fill.solid()
                cell.fill.fore_color.rgb = NV if i == 0 else (RGBColor(0xF8, 0xD7, 0xD3) if v == "missed" else
                                                              RGBColor(0xD8, 0xF0, 0xDF) if v == "met" else WH)
        for j, w_ in enumerate([4.3, 1.3, 1.1, 1.5, 0.9]):
            tbl.columns[j].width = Inches(w_)
        tk = [t.get("text") for t in f["brief"]["takeaways"]]
        if tk:
            text(s, 0.45, 1.35 + 0.34 * len(rows), 9.1, 1.5, ["**Takeaways you hold yourselves to**"] + tk, 10.5)
    # 8 watch
    s = page(H["watch"], ["Each watch item names the evidence and a general lesson for the position you hold. None of "
                          "them is an instruction; together they are the agenda for the team's next decision meeting.",
                          "Likely question: which one first? Answer: the one that threatens the goal management cares "
                          "about most."])
    items = f["watch"][:5] or [{"title": "Nothing stands out", "evidence": "", "lesson": ""}]
    for i, w in enumerate(items):
        yy = 1.15 + i * 0.8
        panel(s, 0.45, yy, 9.1, 0.72)
        bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.45), Inches(yy), Inches(0.08), Inches(0.72))
        bar.fill.solid(); bar.fill.fore_color.rgb = OR; bar.line.fill.background()
        text(s, 0.65, yy + 0.04, 3.2, 0.66, f"**{w['title']}**", 10)
        text(s, 3.9, yy + 0.04, 2.6, 0.66, w["evidence"], 9, color=INK)
        text(s, 6.55, yy + 0.04, 2.95, 0.66, w["lesson"], 9, color=MU)
    # 9 questions
    s = page(H["questions"], ["Close the review with these questions. Discuss them as a team before you open the "
                              "decision screens, then use the Decision Planner and the plan check.",
                              "Likely question: where do we record the answers? Answer: the workbook's Findings & "
                              "Questions tab, in the 'Our response' column."])
    for i, q in enumerate(f["questions"]):
        yy = 1.3 + i * 1.1
        o = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.55), Inches(yy + 0.1), Inches(0.5), Inches(0.5))
        o.fill.solid(); o.fill.fore_color.rgb = OR; o.line.fill.background()
        o.text_frame.text = str(i + 1)
        r = o.text_frame.paragraphs[0].runs[0]; r.font.size, r.font.bold, r.font.color.rgb = Pt(14), True, WH
        o.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        text(s, 1.3, yy + 0.1, 8.2, 0.9, q, 15, color=INK)
    prs.save(path)
    return True


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    opt = lambda k, dflt=None: a[a.index(k) + 1] if k in a else dflt
    files = [x for i, x in enumerate(a) if x.endswith(".json") and
             (i == 0 or a[i - 1] not in ("--team", "--out-dir", "--title", "--ledger"))]
    brief = None
    if opt("--ledger"):
        L = json.load(open(opt("--ledger"), encoding="utf-8"))
        brief = (L.get("globus") or {}).get("management_brief") or (L.get("company_layer") or {}).get("management_brief")
    caps = load(files)
    team = opt("--team") or next((str(c.get("company")) for c in caps if c.get("company")), None)
    out = opt("--out-dir", ".")
    os.makedirs(out, exist_ok=True)
    facts = build_facts(caps, team, brief)
    y = facts["year"]
    title = opt("--title", f"Company {team}")
    imgs = charts(caps, facts, team)
    base = os.path.join(out, f"weekly-report-Y{y}")
    write_html(facts, imgs, base + ".html", title)
    ok = write_memo(facts, imgs, base + "-memo.docx", title)
    okd = write_deck(facts, imgs, base + "-deck.pptx", title)
    json.dump(facts, open(base + ".json", "w"), indent=1, default=lambda v: round(v, 4) if isinstance(v, float) else str(v))
    print(json.dumps({"year": y, "html": base + ".html", "memo": base + "-memo.docx" if ok else None, "deck": base + "-deck.pptx" if okd else None, "json": base + ".json",
                      "apparent": {p: d["apparent"] for p, d in facts["products"].items()},
                      "watch_items": len(facts["watch"])}))


if __name__ == "__main__":
    main()
