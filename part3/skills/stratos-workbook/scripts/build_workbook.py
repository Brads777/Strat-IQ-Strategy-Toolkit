#!/usr/bin/env python3
"""Build the StratOS Workbook (.xlsx): working worksheets for every StratOS framework, optionally
pre-filled from a strategy ledger.

Usage: python build_workbook.py [--ledger strategy-ledger.json] [--out StratOS_Workbook.xlsx]
                                [--blank] [--title "Company / industry"]
                                [--capture globus-capture-C-Y6.json ...] [--first-year 6]
  --capture: one or more GLO-BUS capture files (stratos-globus-capture). Their decision values fill that
             year's column of the GLO-BUS Planner, and the latest one with CIR rows fills the GLO-BUS CIR sheet.
  --ledger : fill the sheets from a StratOS ledger (missing sections stay blank)
  --blank  : no ledger and no example rows (a clean template)
  Without --ledger or --blank, each sheet gets one or two example rows so students see the format.
Formulas only (no hardcoded results). Recalculate before reading values: open in Excel, or run
LibreOffice headless. Requires openpyxl; matplotlib is used for the strategy map image if present.
"""
import json, os, sys, tempfile
from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

NAVY, GOLD, BAND = "1D3557", "C9A55C", "F3F1EC"
F = "Arial"
T_FONT = Font(name=F, size=16, bold=True, color=NAVY)
S_FONT = Font(name=F, size=10, italic=True, color="555555")
H_FONT = Font(name=F, size=10, bold=True, color="FFFFFF")
H_FILL = PatternFill("solid", fgColor=NAVY)
IN_FONT = Font(name=F, size=10, color="0000FF")
IN_FILL = PatternFill("solid", fgColor="FFF9DB")
FX_FONT = Font(name=F, size=10, color="000000")
FX_FILL = PatternFill("solid", fgColor="EEF2F7")
B_FONT = Font(name=F, size=10, bold=True, color=NAVY)
THIN = Side(style="thin", color="C8CDD3")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
GREEN = PatternFill("solid", fgColor="D8F0DF")
AMBER = PatternFill("solid", fgColor="FFF0C2")
RED = PatternFill("solid", fgColor="F8D7D3")
LEGEND = ("Blue text on cream = your inputs.  Black on grey = formulas (do not type over them).  "
          "Delete the example row before you start.")
LEGEND_TEXT = [LEGEND]
IMPACT = {"high": 5, "medium": 3, "med": 3, "low": 1}


# ---------- helpers ----------
def head(ws, title, subtitle, widths):
    ws["A1"] = title
    ws["A1"].font = T_FONT
    ws["A2"] = subtitle
    ws["A2"].font = S_FONT
    ws["A3"] = LEGEND_TEXT[0]
    ws["A3"].font = Font(name=F, size=9, color="0000FF")
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.sheet_view.showGridLines = False
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True


def header(ws, row, names):
    for i, n in enumerate(names, 1):
        c = ws.cell(row=row, column=i, value=n)
        c.font, c.fill, c.alignment, c.border = H_FONT, H_FILL, CENTER, BOX
    ws.row_dimensions[row].height = 30
    ws.freeze_panes = ws.cell(row=row + 1, column=1)


def inp(ws, ref, value=None, fmt=None):
    c = ws[ref]
    if value is not None:
        c.value = value
    c.font, c.fill, c.border, c.alignment = IN_FONT, IN_FILL, BOX, WRAP
    if fmt:
        c.number_format = fmt
    return c


def fx(ws, ref, formula, fmt=None, bold=False):
    c = ws[ref]
    c.value = formula
    c.font = Font(name=F, size=10, bold=bold, color="000000")
    c.fill, c.border, c.alignment = FX_FILL, BOX, Alignment(vertical="top", wrap_text=True)
    if fmt:
        c.number_format = fmt
    return c


def label(ws, ref, text, bold=True):
    c = ws[ref]
    c.value = text
    c.font = B_FONT if bold else Font(name=F, size=10)
    c.alignment = WRAP
    return c


def dv_list(ws, items, rng):
    dv = DataValidation(type="list", formula1='"' + ",".join(items) + '"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(rng)


def dv_whole(ws, lo, hi, rng):
    dv = DataValidation(type="whole", operator="between", formula1=str(lo), formula2=str(hi), allow_blank=True)
    dv.error, dv.errorTitle = f"Enter a whole number from {lo} to {hi}.", "StratOS"
    ws.add_data_validation(dv)
    dv.add(rng)


def traffic(ws, rng, good, warn, bad):
    ws.conditional_formatting.add(rng, FormulaRule(formula=[good], fill=GREEN))
    ws.conditional_formatting.add(rng, FormulaRule(formula=[warn], fill=AMBER))
    ws.conditional_formatting.add(rng, FormulaRule(formula=[bad], fill=RED))


def g(d, *path, default=None):
    for p in path:
        if isinstance(d, dict):
            d = d.get(p)
        elif isinstance(d, list) and isinstance(p, int) and p < len(d):
            d = d[p]
        else:
            return default
        if d is None:
            return default
    return d


# ---------- sheets ----------
def sheet_start(wb, L, title, mode):
    ws = wb.active
    ws.title = "Start"
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 4
    ws.column_dimensions["B"].width = 28
    ws.column_dimensions["C"].width = 90
    ws["B2"] = "StratOS Workbook"
    ws["B2"].font = Font(name=F, size=22, bold=True, color=NAVY)
    ws["B3"] = title
    ws["B3"].font = Font(name=F, size=12, color=GOLD, bold=True)
    src = {"ledger": f"Pre-filled from the StratOS ledger ({g(L, 'scope_id', default='')}, as of {g(L, 'asof', default='n/a')}).",
           "example": "Template with one example row per sheet. Replace the examples with your own work.",
           "blank": "Blank template."}[mode]
    ws["B4"] = src
    ws["B4"].font = S_FONT
    rows = [("How to use", "Each sheet is one StratOS framework. Type only in the cream cells (blue text). Grey "
                           "cells are formulas: they score, rank and flag automatically. Every finding should name "
                           "its evidence in the Source column, the same rule StratOS follows."),
            ("Colour key", "Blue on cream = input · black on grey = formula · green / amber / red = status."),
            ("PESTEL", "Macro findings with impact × certainty priority and the P&L line each one hits."),
            ("Five Forces", "Sub-factor scores roll up to each force and to an industry attractiveness score."),
            ("KSF Scorecard", "Weighted KSFs, every competitor scored, totals and rank; weights must sum to 100%."),
            ("VRIO", "Yes / No / ? for each test; the verdict and the KSF reality check are calculated."),
            ("SWOT-TOWS", "Four traced lists and the TOWS options that pair them."),
            ("Decision Matrix", "Criteria weights × option scores, with a weighted total and rank; do nothing included."),
            ("Expected Value", "Scenario probabilities × NPVs, expected NPV, worst case, maximin, value of information, and a Bayes' rule pilot check (EVSI)."),
            ("Business Case", "Driver-based cash flows, NPV, IRR and cumulative cash."),
            ("Risk Analysis", "Exhibit Q-3: a tornado chart (which driver moves NPV most) and a 1,000-run Monte Carlo "
                              "simulation (median, P10-P90, chance NPV is below zero) over your low / likely / high ranges."),
            ("Balanced Scorecard", "Objectives and measures in four perspectives, leading vs lagging, status vs target, balance check."),
            ("Strategy Map", "Objectives by perspective and their cause-and-effect links; picture included when built from a ledger."),
            ("GLO-BUS CIR", "Paste the CIR figures; each company is placed in a strategic group automatically."),
            ("Y# Results", "One tab per GLO-BUS year: the five scored KPIs against investor expectations, company and "
                           "product results, market share by region, the decisions entered and the CIR."),
            ("Tracking", "Trends across the years, pulled from the Year tabs, with charts: EPS, ROE, stock price, "
                         "image and credit rating, market share, cost per unit, revenue and profit, margins."),
            ("Rivals", "Where you stand in the contest: every company's overall score, rank, price, P/Q and market "
                       "share by year, from the class-wide reports only, with charts."),
            ("GLO-BUS Planner", "Plan every decision for each year in one place, in screen order; flags changes bigger than "
                                "your threshold and years where price and advertising are both cut. You enter the "
                                "decisions in GLO-BUS yourself; the capture skill can then check them against this plan."),
            ("Your work stays yours", "In graded work, the inputs, choices and every Impact Summary are the student's. "
                                      "The workbook calculates; it never decides.")]
    r = 6
    for k, v in rows:
        ws.cell(row=r, column=2, value=k).font = B_FONT
        c = ws.cell(row=r, column=3, value=v)
        c.font, c.alignment = Font(name=F, size=10), WRAP
        r += 1
    ws.cell(row=r + 1, column=2, value="© 2026 Brad Scheller · StratOS Strategy Lab · Apache-2.0").font = S_FONT


def sheet_pestel(wb, L, mode):
    ws = wb.create_sheet("PESTEL")
    head(ws, "PESTEL Analysis", "Macro findings, each tied to a P&L line. Priority = impact × certainty (1-25).",
         [7, 14, 52, 10, 9, 10, 10, 18, 40])
    header(ws, 5, ["ID", "Dimension", "Finding", "Direction (+ / - / ±)", "Impact 1-5", "Certainty 1-5",
                   "Priority", "P&L line", "Source / evidence"])
    rows = []
    if mode == "ledger":
        for p in g(L, "industry_layer", "pestel", default=[]) or []:
            dim = {"P": "Political", "E": "Economic", "S": "Social", "T": "Technological", "En": "Environmental",
                   "L": "Legal"}.get(p.get("dimension"), p.get("dimension"))
            rows.append([p.get("id"), dim, p.get("finding"), p.get("direction"),
                         IMPACT.get(str(p.get("impact", "")).lower(), p.get("impact")),
                         IMPACT.get(str(p.get("certainty", "")).lower(), p.get("certainty")),
                         p.get("pl_line"), ", ".join(p.get("evidence", []) or [])])
    elif mode == "example":
        rows = [["P1", "Economic", "Battery cell prices keep falling as LFP capacity grows", "+", 4, 4,
                 "cogs.inputs", "Example: industry price survey, 2026"]]
    n = max(25, len(rows) + 5)
    for i in range(n):
        r = 6 + i
        vals = rows[i] if i < len(rows) else [None] * 8
        for col, v in zip("ABCDEFH", vals[:6] + [vals[6]]):
            inp(ws, f"{col}{r}", v)
        inp(ws, f"I{r}", vals[7])
        fx(ws, f"G{r}", f'=IF(AND(ISNUMBER(E{r}),ISNUMBER(F{r})),E{r}*F{r},"")', "0")
    last = 5 + n
    dv_list(ws, ["Political", "Economic", "Social", "Technological", "Environmental", "Legal"], f"B6:B{last}")
    dv_list(ws, ["+", "-", "±"], f"D6:D{last}")
    dv_whole(ws, 1, 5, f"E6:F{last}")
    dv_list(ws, ["revenue.price", "revenue.volume", "revenue.mix", "cogs.inputs", "cogs.labor", "opex.sga",
                 "opex.rnd", "capex", "working_capital", "financing", "tax_and_levies"], f"H6:H{last}")
    traffic(ws, f"G6:G{last}", "AND(ISNUMBER(G6),G6>=16)", "AND(ISNUMBER(G6),G6>=9,G6<16)",
            "AND(ISNUMBER(G6),G6<9)")
    r = last + 2
    label(ws, f"B{r}", "Findings")
    fx(ws, f"C{r}", f'=COUNTA(C6:C{last})', "0")
    label(ws, f"B{r+1}", "High priority (≥16)")
    fx(ws, f"C{r+1}", f'=COUNTIF(G6:G{last},">=16")', "0")
    label(ws, f"B{r+2}", "Missing a source")
    fx(ws, f"C{r+2}", f'=SUMPRODUCT((C6:C{last}<>"")*(I6:I{last}=""))', "0")
    ws["G5"].comment = Comment("Green = strategic focus (16+), amber = scenario-plan (9-15), red = monitor.", "StratOS")


FORCES = [("Competitive rivalry", ["Current competition", "Market growth", "Exit barriers", "Differentiation"], "rivalry"),
          ("Supplier power", ["Supplier concentration", "Switching costs", "Forward integration", "Input uniqueness"], "suppliers"),
          ("Buyer power", ["Buyer concentration", "Purchase volume", "Switching costs", "Price sensitivity"], "buyers"),
          ("Threat of new entrants", ["Entry barriers", "Capital requirements", "Scale economies", "Distribution access"], "entrants"),
          ("Threat of substitutes", ["Available substitutes", "Switching costs", "Price-performance", "Buyer propensity"], "substitutes")]


def sheet_forces(wb, L, mode):
    ws = wb.create_sheet("Five Forces")
    head(ws, "Porter's Five Forces", "Score each sub-factor 1 (weak force, good for profit) to 5 (strong force). "
         "A force score you enter overrides the sub-factor average.", [26, 26, 12, 50])
    header(ws, 5, ["Force", "Sub-factor", "Score 1-5", "Evidence / source"])
    lf = {f.get("force"): f for f in (g(L, "industry_layer", "forces", default=[]) or [])} if mode == "ledger" else {}
    r = 6
    for name, subs, key in FORCES:
        for s in subs:
            label(ws, f"A{r}", name, bold=False)
            label(ws, f"B{r}", s, bold=False)
            v = 4 if (mode == "example" and key == "suppliers" and s == "Supplier concentration") else None
            inp(ws, f"C{r}", v)
            inp(ws, f"D{r}", "Example: top three cell makers hold most global capacity" if v else None)
            r += 1
    sub_last = r - 1
    dv_whole(ws, 1, 5, f"C6:C{sub_last}")
    r += 1
    top = r
    for i, h in enumerate(["Force", "Sub-factor average", "Your force score (optional)", "Score used",
                           "Strength", "Horizon score (optional)"], 1):
        c = ws.cell(row=r, column=i, value=h)
        c.font, c.fill, c.alignment, c.border = H_FONT, H_FILL, CENTER, BOX
    for i in range(5, 7):
        ws.column_dimensions[get_column_letter(i)].width = 16
    r += 1
    first = r
    for name, subs, key in FORCES:
        label(ws, f"A{r}", name)
        fx(ws, f"B{r}", f'=IFERROR(AVERAGEIF($A$6:$A${sub_last},A{r},$C$6:$C${sub_last}),"")', "0.0")
        inp(ws, f"C{r}", g(lf, key, "score_now"), "0.0")
        fx(ws, f"D{r}", f'=IF(ISNUMBER(C{r}),C{r},B{r})', "0.0")
        fx(ws, f"E{r}", f'=IF(D{r}="","",IF(D{r}>=4,"Strong",IF(D{r}>=2.5,"Moderate","Weak")))')
        inp(ws, f"F{r}", g(lf, key, "score_horizon"), "0.0")
        r += 1
    last = r - 1
    traffic(ws, f"E{first}:E{last}", f'E{first}="Weak"', f'E{first}="Moderate"', f'E{first}="Strong"')
    r += 1
    label(ws, f"A{r}", "Industry attractiveness (1-5)")
    fx(ws, f"B{r}", f'=IFERROR(6-AVERAGE(D{first}:D{last}),"")', "0.0", bold=True)
    label(ws, f"A{r+1}", "At the horizon")
    fx(ws, f"B{r+1}", f'=IF(COUNT(F{first}:F{last})=5,6-AVERAGE(F{first}:F{last}),"")', "0.0")
    for k, t in enumerate(["Attractiveness = 6 minus the average force score (1-5; higher is more attractive).",
                           "The horizon score appears once all five horizon scores are entered."]):
        c = ws.cell(row=r + 3 + k, column=1, value=t)
        c.font = S_FONT


def sheet_ksf(wb, L, mode):
    ws = wb.create_sheet("KSF Scorecard")
    comps = []
    ksfs = []
    if mode == "ledger":
        comps = [c.get("name") for c in (g(L, "competitors", default=[]) or [])][:8]
        for k in g(L, "industry_layer", "ksf", default=[]) or []:
            row = [k.get("id"), k.get("name"), k.get("weight"),
                   ", ".join((k.get("from_forces") or []) + (k.get("from_drivers") or []))]
            for c in (g(L, "competitors", default=[]) or [])[:8]:
                row.append(g(c, "ksf_scores", k.get("id"), "score"))
            ksfs.append(row)
    elif mode == "example":
        comps = ["BYD", "Stellantis", "Xiaomi"]
        ksfs = [["K1", "Battery cost per kWh", 0.25, "suppliers, D2", 5, 2, 3]]
    nc = max(6, len(comps))
    widths = [7, 34, 10, 18] + [13] * nc
    head(ws, "Key Success Factors Scorecard",
         "Weights are fractions that must sum to 100%. Score each competitor 1 (weak) to 5 (strong) on each KSF.",
         widths)
    header(ws, 5, ["ID", "Key success factor", "Weight", "Traces to (force / driver)"] +
           [f"Competitor {i+1}" for i in range(nc)])
    for i in range(nc):
        inp(ws, f"{get_column_letter(5+i)}5", comps[i] if i < len(comps) else f"Competitor {i+1}")
        ws[f"{get_column_letter(5+i)}5"].font = Font(name=F, size=10, bold=True, color="0000FF")
    n = max(10, len(ksfs) + 2)
    for i in range(n):
        r = 6 + i
        row = ksfs[i] if i < len(ksfs) else []
        inp(ws, f"A{r}", row[0] if row else None)
        inp(ws, f"B{r}", row[1] if row else None)
        inp(ws, f"C{r}", row[2] if row else None, "0%")
        inp(ws, f"D{r}", row[3] if row else None)
        for j in range(nc):
            inp(ws, f"{get_column_letter(5+j)}{r}", row[4 + j] if len(row) > 4 + j else None)
    last = 5 + n
    lastc = get_column_letter(4 + nc)
    dv_whole(ws, 1, 5, f"E6:{lastc}{last}")
    r = last + 1
    label(ws, f"B{r}", "Weight check (must be 100%)")
    fx(ws, f"C{r}", f"=SUM(C6:C{last})", "0%", bold=True)
    fx(ws, f"D{r}", f'=IF(ABS(C{r}-1)<0.001,"OK","Weights must sum to 100%")')
    traffic(ws, f"D{r}", f'D{r}="OK"', "FALSE", f'D{r}<>"OK"')
    label(ws, f"B{r+1}", "Weighted score (out of 5)")
    label(ws, f"B{r+2}", "Rank")
    for j in range(nc):
        col = get_column_letter(5 + j)
        fx(ws, f"{col}{r+1}", f'=IF(COUNT({col}6:{col}{last})=0,"",SUMPRODUCT($C$6:$C${last},{col}6:{col}{last}))',
           "0.00", bold=True)
        fx(ws, f"{col}{r+2}", f'=IF({col}{r+1}="","",RANK({col}{r+1},$E${r+1}:${lastc}${r+1}))', "0")


def sheet_vrio(wb, L, mode):
    ws = wb.create_sheet("VRIO")
    head(ws, "VRIO Analysis", "Answer the four tests in order with Yes / No / ?. The verdict stops at the first No "
         "or ?. KSF weight (a fraction) drives the reality check.", [30, 14, 10, 10, 11, 11, 26, 12, 10, 18, 36])
    header(ws, 5, ["Resource or capability", "Type", "Valuable?", "Rare?", "Inimitable?", "Organized?",
                   "Verdict", "KSF it delivers", "KSF weight", "Reality check", "Evidence"])
    rows = []
    if mode == "ledger":
        caps = {c.get("id"): c.get("name") for c in (g(L, "company_layer", "internal", "capabilities", default=[]) or [])}
        res = {c.get("id"): c.get("name") for c in (g(L, "company_layer", "internal", "resources", default=[]) or [])}
        yn = lambda v: {"yes": "Yes", "no": "No"}.get(str(v).lower(), "?")
        for v in g(L, "company_layer", "internal", "vrio", default=[]) or []:
            it = v.get("item")
            rows.append([caps.get(it) or res.get(it) or it, "capability" if it in caps else "resource",
                         yn(v.get("v")), yn(v.get("r")), yn(v.get("i")), yn(v.get("o")),
                         ", ".join(v.get("links_ksf", []) or []), v.get("ksf_weight"),
                         ", ".join(v.get("evidence", []) or [])])
    elif mode == "example":
        rows = [["Blade-cell battery know-how", "capability", "Yes", "Yes", "Yes", "Yes", "K1", 0.25,
                 "Example: patents and cost lead in filings"]]
    n = max(15, len(rows) + 3)
    for i in range(n):
        r = 6 + i
        row = rows[i] if i < len(rows) else [None] * 9
        for col, v in zip("ABCDEF", row[:6]):
            inp(ws, f"{col}{r}", v)
        inp(ws, f"H{r}", row[6])
        inp(ws, f"I{r}", row[7], "0%")
        inp(ws, f"K{r}", row[8])
        fx(ws, f"G{r}",
           f'=IF(A{r}="","",IF(C{r}<>"Yes",IF(C{r}="No","Competitive disadvantage","Undetermined"),'
           f'IF(D{r}<>"Yes",IF(D{r}="No","Competitive parity","Undetermined beyond valuable"),'
           f'IF(E{r}<>"Yes",IF(E{r}="No","Temporary advantage","Undetermined beyond rare"),'
           f'IF(F{r}="Yes","Sustained advantage",IF(F{r}="No","Unexploited advantage","Undetermined beyond inimitable"))))))')
        fx(ws, f"J{r}",
           f'=IF(A{r}="","",IF(AND(C{r}="Yes",D{r}="Yes",E{r}="Yes",N(I{r})<0.1),"Competence trap",'
           f'IF(AND(OR(G{r}="Temporary advantage",G{r}="Unexploited advantage",G{r}="Sustained advantage"),N(I{r})>=0.1),"Supported",'
           f'IF(AND(G{r}="Competitive parity",N(I{r})>=0.1),"Table stakes",""))))')
    last = 5 + n
    dv_list(ws, ["Yes", "No", "?"], f"C6:F{last}")
    dv_list(ws, ["resource", "capability"], f"B6:B{last}")
    traffic(ws, f"G6:G{last}", f'G6="Sustained advantage"',
            f'OR(G6="Temporary advantage",G6="Unexploited advantage",G6="Competitive parity")',
            f'G6="Competitive disadvantage"')
    ws.conditional_formatting.add(f"J6:J{last}", FormulaRule(formula=['J6="Competence trap"'], fill=RED))
    ws.conditional_formatting.add(f"J6:J{last}", FormulaRule(formula=['J6="Supported"'], fill=GREEN))
    ws["J5"].comment = Comment("Competence trap: passes V, R and I but delivers a KSF weighted under 10% — "
                               "rare and hard to copy, but not what this industry rewards.", "StratOS")


def sheet_swot(wb, L, mode):
    ws = wb.create_sheet("SWOT-TOWS")
    head(ws, "SWOT and TOWS", "Every item names the finding it came from. TOWS options pair the items by ID.",
         [6, 50, 22, 4, 6, 50, 22])
    sw = g(L, "company_layer", "internal", "swot", default={}) or {} if mode == "ledger" else {}
    ex = mode == "example"
    blocks = [("strengths", "Strengths (internal, helpful)", "S", 1), ("weaknesses", "Weaknesses (internal, harmful)", "W", 5),
              ("opportunities", "Opportunities (external, helpful)", "O", 1), ("threats", "Threats (external, harmful)", "T", 5)]
    for bi, (key, title, pre, col) in enumerate(blocks):
        top = 5 if bi < 2 else 14
        c1, c2, c3 = get_column_letter(col), get_column_letter(col + 1), get_column_letter(col + 2)
        for cc, h in zip((c1, c2, c3), ("ID", title, "Source")):
            c = ws[f"{cc}{top}"]
            c.value, c.font, c.fill, c.alignment, c.border = h, H_FONT, H_FILL, CENTER, BOX
        items = sw.get(key, []) if sw else []
        for i in range(6):
            r = top + 1 + i
            it = items[i] if i < len(items) else {}
            label(ws, f"{c1}{r}", f"{pre}{i+1}")
            v = it.get("text")
            s = ", ".join(it.get("source", []) or []) if it else None
            if ex and i == 0:
                v, s = {"S": ("Lowest battery cost in the peer set", "VRIO: C1"),
                        "W": ("No dealer network in Europe", "Value chain: A6"),
                        "O": ("EU fleet electrification mandates", "PESTEL: P7"),
                        "T": ("EU tariffs on imported EVs", "PESTEL: P2")}[pre]
            inp(ws, f"{c2}{r}", v)
            inp(ws, f"{c3}{r}", s)
    r = 23
    for cc, h in zip("ABC", ("Cell", "TOWS strategic option", "Pairs (e.g. S1 × O1)")):
        c = ws[f"{cc}{r}"]
        c.value, c.font, c.fill, c.alignment, c.border = h, H_FONT, H_FILL, CENTER, BOX
    tows = g(L, "company_layer", "internal", "tows", default=[]) or [] if mode == "ledger" else []
    if ex:
        tows = [{"id": "SO1", "option": "Use the battery cost lead to price fleet vans below diesel TCO",
                 "pairs": ["S1", "O1"]}]
    for i in range(12):
        rr = r + 1 + i
        t = tows[i] if i < len(tows) else {}
        inp(ws, f"A{rr}", (t.get("id") or "")[:2] if t else None)
        inp(ws, f"B{rr}", t.get("option"))
        inp(ws, f"C{rr}", " × ".join(t.get("pairs", []) or []) if t else None)
    dv_list(ws, ["SO", "WO", "ST", "WT"], f"A{r+1}:A{r+12}")


def sheet_matrix(wb, L, mode):
    ws = wb.create_sheet("Decision Matrix")
    opts, crits = [], []
    if mode == "ledger":
        opts = [o.get("name") for o in (g(L, "strategy_layer", "options", "options", default=[]) or [])][:6]
        for c in g(L, "strategy_layer", "decision_matrix", "criteria", default=[]) or []:
            sc = c.get("scores", {}) or {}
            crits.append([c.get("name"), c.get("weight"), c.get("goal")] + [sc.get(o) for o in opts])
    elif mode == "example":
        opts = ["A. Build in-house", "B. Partner for cells", "C. Reposition", "0. Do nothing"]
        crits = [["Fits the 2029 profit goal", 5, "Exhibit B, goal 1", 3, 4, 3, 1]]
    no = max(5, len(opts))
    head(ws, "Decision Matrix", "Weight each criterion 1-5 and score each option 1-5. Include do nothing.",
         [36, 9, 22] + [15] * no)
    header(ws, 5, ["Criterion", "Weight 1-5", "Tied to goal"] + [f"Option {i+1}" for i in range(no)])
    for i in range(no):
        col = get_column_letter(4 + i)
        inp(ws, f"{col}5", opts[i] if i < len(opts) else f"Option {i+1}")
        ws[f"{col}5"].font = Font(name=F, size=10, bold=True, color="0000FF")
    n = 8
    for i in range(n):
        r = 6 + i
        row = crits[i] if i < len(crits) else []
        inp(ws, f"A{r}", row[0] if row else None)
        inp(ws, f"B{r}", row[1] if row else None)
        inp(ws, f"C{r}", row[2] if row else None)
        for j in range(no):
            inp(ws, f"{get_column_letter(4+j)}{r}", row[3 + j] if len(row) > 3 + j else None)
    last = 5 + n
    lastc = get_column_letter(3 + no)
    dv_whole(ws, 1, 5, f"B6:{lastc}{last}")
    r = last + 1
    label(ws, f"A{r}", "Weighted score (out of 5)")
    label(ws, f"A{r+1}", "Rank")
    for j in range(no):
        col = get_column_letter(4 + j)
        fx(ws, f"{col}{r}", f'=IF(COUNT({col}6:{col}{last})=0,"",SUMPRODUCT($B$6:$B${last},{col}6:{col}{last})/'
                            f'SUMPRODUCT($B$6:$B${last}*({col}6:{col}{last}<>"")))', "0.00", bold=True)
        fx(ws, f"{col}{r+1}", f'=IF({col}{r}="","",RANK({col}{r},$D${r}:${lastc}${r}))', "0")
    label(ws, f"A{r+3}", "The matrix ranks; it does not choose. The recommendation is yours.", bold=False)


def sheet_ev(wb, L, mode):
    ws = wb.create_sheet("Expected Value")
    head(ws, "Expected Value", "Probabilities as percentages that sum to 100% per option; NPV in $M. "
         "Follows the course handout 'Choosing Among Strategic Alternatives'.",
         [26, 10, 11, 10, 11, 10, 11, 11, 13, 11, 11])
    header(ws, 5, ["Option", "P strong", "NPV strong ($M)", "P moderate", "NPV moderate ($M)", "P weak",
                   "NPV weak ($M)", "Probability check", "Expected NPV ($M)", "Worst case", "Best case"])
    rows = []
    if mode == "example":
        rows = [["A. Move upmarket", .3, 12, .5, 4, .2, -6], ["B. Cut costs", .3, 6, .5, 4, .2, 1],
                ["C. Do nothing", .3, 0, .5, 0, .2, 0]]
    elif mode == "ledger":
        for o in (g(L, "strategy_layer", "expected_value", "table", default=[]) or []):
            rows.append([o.get("option"), o.get("p_strong"), o.get("npv_strong"), o.get("p_moderate"),
                         o.get("npv_moderate"), o.get("p_weak"), o.get("npv_weak")])
    n = 6
    for i in range(n):
        r = 6 + i
        row = rows[i] if i < len(rows) else [None] * 7
        inp(ws, f"A{r}", row[0])
        for col, v, f_ in zip("BCDEFG", row[1:], ["0%", "0.0", "0%", "0.0", "0%", "0.0"]):
            inp(ws, f"{col}{r}", v, f_)
        fx(ws, f"H{r}", f'=IF(A{r}="","",IF(ABS(B{r}+D{r}+F{r}-1)<0.001,"OK","Must sum to 100%"))')
        fx(ws, f"I{r}", f'=IF(A{r}="","",B{r}*C{r}+D{r}*E{r}+F{r}*G{r})', "0.00", bold=True)
        fx(ws, f"J{r}", f'=IF(A{r}="","",MIN(C{r},E{r},G{r}))', "0.0")
        fx(ws, f"K{r}", f'=IF(A{r}="","",MAX(C{r},E{r},G{r}))', "0.0")
    last = 5 + n
    traffic(ws, f"H6:H{last}", 'H6="OK"', "FALSE", 'H6="Must sum to 100%"')
    r = last + 2
    label(ws, f"A{r}", "Leader on expected value")
    fx(ws, f"B{r}", f'=IFERROR(INDEX(A6:A{last},MATCH(MAX(I6:I{last}),I6:I{last},0)),"")', bold=True)
    label(ws, f"A{r+1}", "Maximin choice (best worst case)")
    fx(ws, f"B{r+1}", f'=IFERROR(INDEX(A6:A{last},MATCH(MAX(J6:J{last}),J6:J{last},0)),"")', bold=True)
    label(ws, f"A{r+2}", "Value of perfect information ($M)")
    lead = f"MATCH(MAX(I6:I{last}),I6:I{last},0)"
    fx(ws, f"B{r+2}", f'=IFERROR(INDEX(B6:B{last},{lead})*MAX(C6:C{last})+INDEX(D6:D{last},{lead})*MAX(E6:E{last})'
                      f'+INDEX(F6:F{last},{lead})*MAX(G6:G{last})-MAX(I6:I{last}),"")', "0.00", bold=True)
    label(ws, f"C{r+2}", "The most worth paying for a pilot that reveals the scenario first (leader's probabilities).",
          bold=False)
    ws.merge_cells(f"C{r+2}:K{r+2}")
    # ---- Bayesian pilot update ----
    b0 = r + 5
    label(ws, f"A{b0}", "Is a pilot worth it? (Bayes' rule)")
    label(ws, f"B{b0}", "How likely the pilot shows each result IF that scenario is real. Each row sums to 100%. "
                        "Uses the first option's scenario probabilities as the prior.", bold=False)
    ws.merge_cells(f"B{b0}:K{b0}")
    header(ws, b0 + 1, ["Scenario", "Prior", "P(positive | scenario)", "P(negative | scenario)", "Row check",
                        "Posterior if positive", "Posterior if negative"])
    ws.freeze_panes = "A6"
    pil = (g(L, "strategy_layer", "expected_value", "pilot", default={}) or {}) if mode == "ledger" else {}
    lk = pil.get("likelihoods", {}) or {}
    exl = {"strong": (.80, .20), "moderate": (.50, .50), "weak": (.15, .85)}
    pr = {"strong": "B6", "moderate": "D6", "weak": "F6"}
    for i, sc in enumerate(("strong", "moderate", "weak")):
        rr = b0 + 2 + i
        label(ws, f"A{rr}", sc.capitalize(), bold=False)
        fx(ws, f"B{rr}", f"=IF({pr[sc]}=\"\",\"\",{pr[sc]})", "0%")
        v = exl[sc] if mode == "example" else (tuple(lk.get(sc) or (None, None)) if mode == "ledger" else (None, None))
        inp(ws, f"C{rr}", v[0], "0%")
        inp(ws, f"D{rr}", v[1], "0%")
        fx(ws, f"E{rr}", f'=IF(C{rr}="","",IF(ABS(C{rr}+D{rr}-1)<0.001,"OK","Must sum to 100%"))')
        fx(ws, f"F{rr}", f'=IFERROR(B{rr}*C{rr}/SUMPRODUCT($B${b0+2}:$B${b0+4},$C${b0+2}:$C${b0+4}),"")', "0.0%")
        fx(ws, f"G{rr}", f'=IFERROR(B{rr}*D{rr}/SUMPRODUCT($B${b0+2}:$B${b0+4},$D${b0+2}:$D${b0+4}),"")', "0.0%")
    s1, s3 = b0 + 2, b0 + 4
    rp = s3 + 1
    label(ws, f"A{rp}", "P(result)")
    fx(ws, f"F{rp}", f'=IFERROR(SUMPRODUCT(B{s1}:B{s3},C{s1}:C{s3}),"")', "0.0%", bold=True)
    fx(ws, f"G{rp}", f'=IFERROR(SUMPRODUCT(B{s1}:B{s3},D{s1}:D{s3}),"")', "0.0%", bold=True)
    e0 = rp + 2
    header(ws, e0, ["Option", "Expected NPV now", "If positive", "If negative"])
    ws.freeze_panes = "A6"
    for i in range(n):
        rr = e0 + 1 + i
        src = 6 + i
        fx(ws, f"A{rr}", f'=IF(A{src}="","",A{src})')
        fx(ws, f"B{rr}", f'=IF(A{src}="","",I{src})', "0.00")
        fx(ws, f"C{rr}", f'=IF(OR(A{src}="",F{s1}=""),"",C{src}*F{s1}+E{src}*F{s1+1}+G{src}*F{s3})', "0.00")
        fx(ws, f"D{rr}", f'=IF(OR(A{src}="",G{s1}=""),"",C{src}*G{s1}+E{src}*G{s1+1}+G{src}*G{s3})', "0.00")
    e1, e2 = e0 + 1, e0 + n
    q = e2 + 2
    out_rows = [
        ("Best option if the pilot is positive", f'=IFERROR(INDEX(A{e1}:A{e2},MATCH(MAX(C{e1}:C{e2}),C{e1}:C{e2},0)),"")', None),
        ("Best option if the pilot is negative", f'=IFERROR(INDEX(A{e1}:A{e2},MATCH(MAX(D{e1}:D{e2}),D{e1}:D{e2},0)),"")', None),
        ("Expected NPV with the pilot ($M)", f'=IFERROR(F{rp}*MAX(C{e1}:C{e2})+G{rp}*MAX(D{e1}:D{e2}),"")', "0.00"),
        ("Value of the pilot, EVSI ($M)", f'=IFERROR(B{q+2}-MAX(I6:I{last}),"")', "0.00"),
        ("Pilot cost ($M)", None, "0.00"),
        ("Net value of running the pilot ($M)", f'=IFERROR(IF(B{q+4}="","",B{q+3}-B{q+4}),"")', "0.00"),
        ("Share of perfect information", f'=IFERROR(B{q+3}/B{r+2},"")', "0%")]
    for i, (nm, f_, fmt) in enumerate(out_rows):
        rr = q + i
        label(ws, f"A{rr}", nm)
        if f_ is None:
            inp(ws, f"B{rr}", 0.5 if mode == "example" else pil.get("cost"), fmt)
        else:
            fx(ws, f"B{rr}", f_, fmt, bold=True)
    label(ws, f"C{q}", "If both results point to the same option, the pilot cannot change the choice and is worth "
                       "nothing for this decision.", bold=False)
    ws.merge_cells(f"C{q}:K{q+1}")


def sheet_bc(wb, L, mode):
    ws = wb.create_sheet("Business Case")
    head(ws, "Business Case", "One option. Year 0 is the investment year. Working capital is released in the final "
         "year. Money in $.", [30, 15, 15, 15, 15, 15, 15])
    label(ws, "A5", "Assumptions")
    ex = mode == "example"
    bc = (g(L, "strategy_layer", "business_case", 0, default={}) or {}) if mode == "ledger" else {}
    bi = bc.get("inputs", {}) or {}
    led = bool(bi.get("years"))
    assume = [("Discount rate", 0.10 if ex else bi.get("rate"), "0.0%"), ("Tax rate", 0.21 if ex else bi.get("tax"), "0.0%"),
              ("Working capital (% of revenue)", 0.05 if ex else bi.get("wc_pct"), "0.0%")]
    if led:
        ws["A4"] = f"Option: {bc.get('option', '')} (from the ledger)"
        ws["A4"].font = S_FONT
    for i, (k, v, f_) in enumerate(assume):
        label(ws, f"A{6+i}", k, bold=False)
        inp(ws, f"B{6+i}", v, f_)
    if ex:
        ws["B6"].comment = Comment("Example values from the StratOS Business Case template (illustrative).", "StratOS")
    header_row = 10
    for i, h in enumerate(["$"] + [f"Year {y}" for y in range(6)], 1):
        c = ws.cell(row=header_row, column=i, value=h)
        c.font, c.fill, c.alignment, c.border = H_FONT, H_FILL, CENTER, BOX
    exu = [0, 32400, 64800, 97200, 108000, 108000]
    excap = [2000000000, 100000000, 100000000, 50000000, 50000000, 50000000]
    inputs = [("Units", exu, "#,##0"), ("Price per unit", [32000] * 6, "$#,##0"),
              ("Variable cost per unit", [20000] * 6, "$#,##0"), ("Fixed costs", [0] + [180000000] * 5, "$#,##0"),
              ("Capex", excap, "$#,##0")]
    r = header_row + 1
    keys = ["units", "price", "variable_cost", "fixed_cost", "capex"]
    yrs = (bi.get("years") or [])[:6] if led else []
    for k_i, (name, vals, f_) in enumerate(inputs):
        label(ws, f"A{r}", name, bold=False)
        for y in range(6):
            v = vals[y] if ex else (yrs[y].get(keys[k_i]) if y < len(yrs) else None)
            inp(ws, f"{get_column_letter(2+y)}{r}", v, f_)
        r += 1
    calc = [("Revenue", "={c}11*{c}12"), ("Contribution", "={c}11*({c}12-{c}13)"),
            ("Operating profit (EBIT)", "={c}17-{c}14"), ("Tax", "=MAX(0,{c}18)*$B$7"),
            ("Working capital", "={c}16*$B$8"), ("Change in working capital", "={c}20-{p}20"),
            ("Cash flow", "={c}18-{c}19-{c}21-{c}15{rel}"), ("Cumulative cash flow", "={p}23+{c}22")]
    for name, f_ in calc:
        label(ws, f"A{r}", name, bold=name in ("Cash flow",))
        for y in range(6):
            c = get_column_letter(2 + y)
            p = get_column_letter(1 + y)
            ff = f_
            if y == 0:
                ff = ff.replace("-{p}20", "").replace("={p}23+", "=")
            rel = "+{c}20".format(c=c) if y == 5 else ""
            fx(ws, f"{c}{r}", ff.format(c=c, p=p, rel=rel), "$#,##0;($#,##0);-", bold=name == "Cash flow")
        r += 1
    r += 1
    label(ws, f"A{r}", "NPV")
    fx(ws, f"B{r}", "=IF(COUNT(B11:G11)=0,\"\",B22+NPV($B$6,C22:G22))", "$#,##0;($#,##0);-", bold=True)
    label(ws, f"A{r+1}", "IRR")
    fx(ws, f"B{r+1}", '=IFERROR(IRR(B22:G22),"n/a")', "0.0%", bold=True)
    label(ws, f"A{r+2}", "Clears the hurdle?")
    fx(ws, f"B{r+2}", f'=IF(ISNUMBER(B{r+1}),IF(B{r+1}>=$B$6,"Yes","No"),"")', bold=True)
    traffic(ws, f"B{r+2}", f'B{r+2}="Yes"', "FALSE", f'B{r+2}="No"')
    label(ws, f"A{r+4}", "State the break-even in words in your exhibit (the Business Case skill computes it).",
          bold=False)


RISK_DRIVERS = [("price", "Price per unit", -0.10, 0.0, 0.05), ("units", "Units", -0.30, 0.0, 0.15),
                ("variable_cost", "Variable cost per unit", -0.05, 0.0, 0.10),
                ("fixed_cost", "Fixed costs", -0.10, 0.0, 0.15), ("capex", "Capex", -0.05, 0.0, 0.25),
                ("rate", "Discount rate (absolute)", 0.08, 0.10, 0.13)]
MC_ROWS = 1000


def _cf_formula(y, m):
    """Cash-flow formula for year index y (0-5) with multiplier refs m = dict(price, units, variable_cost,
    fixed_cost, capex) (each a cell holding 1 + change)."""
    B = "'Business Case'!"
    c = get_column_letter(2 + y)
    p = get_column_letter(1 + y)
    rev = lambda col: f"({B}{col}11*{m['units']}*{B}{col}12*{m['price']})"
    ebit = (f"({rev(c)}-{B}{c}11*{m['units']}*{B}{c}13*{m['variable_cost']}-{B}{c}14*{m['fixed_cost']})")
    dwc = f"{B}$B$8*({rev(c)}-{rev(p)})" if y > 0 else f"{B}$B$8*{rev(c)}"
    f_ = f"={ebit}-MAX(0,{ebit})*{B}$B$7-{dwc}-{B}{c}15*{m['capex']}"
    if y == 5:
        f_ += f"+{B}$B$8*{rev(c)}"
    return f_


def sheet_risk(wb, L, mode):
    from openpyxl.chart import BarChart, Reference
    ws = wb.create_sheet("Risk Analysis")
    head(ws, "Risk Analysis (Exhibit Q-3)", "Works on the Business Case sheet. Set a low / likely / high for each "
         "driver: % change from plan, except the discount rate (an absolute rate). Blank = no uncertainty.",
         [28, 11, 11, 11, 12, 12, 12, 15, 15, 15, 12, 12, 14])
    ra = (g(L, "strategy_layer", "risk_analysis", "ranges", default={}) or {}) if mode == "ledger" else {}
    header(ws, 5, ["Driver", "Low", "Likely", "High", "Eff. low", "Eff. likely", "Eff. high"])
    rows = {}
    for i, (key, name, lo, mid, hi) in enumerate(RISK_DRIVERS):
        r = 6 + i
        rows[key] = r
        label(ws, f"A{r}", name, bold=False)
        vals = (lo, mid, hi) if mode == "example" else tuple((ra.get(key) or [None] * 3)[:3]) if mode == "ledger" else (None,) * 3
        fmt = "0.0%"
        for col, v in zip("BCD", vals):
            inp(ws, f"{col}{r}", v, fmt)
        dflt = "'Business Case'!$B$6" if key == "rate" else "0"
        # effective values: blanks fall back to the likely value, then to plan
        fx(ws, f"F{r}", f'=IF(C{r}="",{dflt},C{r})', fmt)
        fx(ws, f"E{r}", f'=IF(B{r}="",F{r},B{r})', fmt)
        fx(ws, f"G{r}", f'=IF(D{r}="",F{r},D{r})', fmt)
    ws[f"H6"] = None
    chk = 6 + len(RISK_DRIVERS)
    label(ws, f"A{chk}", "Range check", bold=False)
    fx(ws, f"B{chk}", '=IF(SUMPRODUCT((E6:E11>F6:F11)+(F6:F11>G6:G11))=0,"OK","Need low <= likely <= high")')
    ws.merge_cells(f"B{chk}:D{chk}")
    traffic(ws, f"B{chk}", f'B{chk}="OK"', "FALSE", f'B{chk}<>"OK"')

    # ---- tornado scenarios (exact NPV, each driver alone at low / high) ----
    t0 = chk + 2
    label(ws, f"A{t0}", "Tornado: NPV with one driver at its low or high, the others at plan")
    header_r = t0 + 1
    for i, h in enumerate(["Scenario", "Price ×", "Units ×", "Var. cost ×", "Fixed ×", "Capex ×", "Rate",
                           "CF Y0", "CF Y1", "CF Y2", "CF Y3", "CF Y4", "CF Y5", "NPV"], 1):
        c = ws.cell(row=header_r, column=i, value=h)
        c.font, c.fill, c.alignment, c.border = H_FONT, H_FILL, CENTER, BOX
    ws.column_dimensions["N"].width = 16
    scen = [("Plan", None, None)] + [(f"{n} {s}", k, s) for k, n, *_ in RISK_DRIVERS for s in ("low", "high")]
    mcols = {"price": "B", "units": "C", "variable_cost": "D", "fixed_cost": "E", "capex": "F"}
    srow = {}
    for i, (nm, key, side) in enumerate(scen):
        r = header_r + 1 + i
        srow[(key, side)] = r
        label(ws, f"A{r}", nm, bold=False)
        for k, col in mcols.items():
            src = ("E" if side == "low" else "G") + str(rows[k])
            fx(ws, f"{col}{r}", f"=1+{src}" if key == k else "=1", "0.00")
        rate_src = ("E" if side == "low" else "G") + str(rows["rate"]) if key == "rate" else "'Business Case'!$B$6"
        fx(ws, f"G{r}", f"={rate_src}", "0.0%")
        m = {k: f"${col}{r}" for k, col in mcols.items()}
        for y in range(6):
            fx(ws, f"{get_column_letter(8 + y)}{r}", _cf_formula(y, m), "$#,##0;($#,##0);-")
        fx(ws, f"N{r}", f'=IF(COUNT(\'Business Case\'!B11:G11)=0,"",H{r}+NPV(G{r},I{r}:M{r}))', "$#,##0;($#,##0);-",
           bold=True)
    plan_r = srow[(None, None)]
    tz = header_r + 1 + len(scen) + 1
    label(ws, f"A{tz}", "Tornado table (sorted by swing; the chart reads this)")
    header(ws, tz + 1, ["Driver", "NPV at low", "NPV at high", "Swing", "Low − plan", "High − plan", "Crosses zero?",
                        "Rank key"])
    ws.freeze_panes = None
    # unsorted helper rows
    uz = tz + 2 + len(RISK_DRIVERS) + 1
    label(ws, f"A{uz}", "Helper (unsorted)", bold=False)
    for i, (key, name, *_) in enumerate(RISK_DRIVERS):
        r = uz + 1 + i
        label(ws, f"A{r}", name, bold=False)
        fx(ws, f"B{r}", f"=N{srow[(key, 'low')]}", "$#,##0;($#,##0);-")
        fx(ws, f"C{r}", f"=N{srow[(key, 'high')]}", "$#,##0;($#,##0);-")
        fx(ws, f"D{r}", f'=IFERROR(ABS(C{r}-B{r})+ROW()/1E9,0)', "$#,##0")
    u1, u2 = uz + 1, uz + len(RISK_DRIVERS)
    for i in range(len(RISK_DRIVERS)):
        r = tz + 2 + i
        mt = f"MATCH(LARGE($D${u1}:$D${u2},{i+1}),$D${u1}:$D${u2},0)"
        fx(ws, f"A{r}", f"=INDEX($A${u1}:$A${u2},{mt})")
        fx(ws, f"B{r}", f"=INDEX($B${u1}:$B${u2},{mt})", "$#,##0;($#,##0);-")
        fx(ws, f"C{r}", f"=INDEX($C${u1}:$C${u2},{mt})", "$#,##0;($#,##0);-")
        fx(ws, f"D{r}", f'=IFERROR(ABS(C{r}-B{r}),"")', "$#,##0", bold=True)
        fx(ws, f"E{r}", f'=IFERROR(B{r}-$N${plan_r},"")', "$#,##0;($#,##0);-")
        fx(ws, f"F{r}", f'=IFERROR(C{r}-$N${plan_r},"")', "$#,##0;($#,##0);-")
        fx(ws, f"G{r}", f'=IF(B{r}="","",IF(MIN(B{r},C{r})<0,IF(MAX(B{r},C{r})>0,"Yes","Below zero"),"No"))')
        fx(ws, f"H{r}", f"={i+1}")
    t1, t2 = tz + 2, tz + 1 + len(RISK_DRIVERS)
    ch = BarChart()
    ch.type, ch.grouping, ch.overlap = "bar", "clustered", 100
    ch.title = "Tornado: change in NPV from plan"
    ch.height, ch.width = 7.5, 15
    for col, color in ((5, "C44536"), (6, "1D3557")):
        ch.add_data(Reference(ws, min_col=col, min_row=t1 - 1, max_row=t2), titles_from_data=True)
        ch.series[-1].graphicalProperties.solidFill = color
        ch.series[-1].graphicalProperties.line.solidFill = color
    ch.set_categories(Reference(ws, min_col=1, min_row=t1, max_row=t2))
    ch.y_axis.numFmt = "$#,##0,,\"M\""
    ch.x_axis.scaling.orientation = "maxMin"
    ch.y_axis.majorGridlines = None
    ch.x_axis.delete = ch.y_axis.delete = False
    ch.legend.position = "b"
    ws.add_chart(ch, f"J{tz}")

    # ---- Monte Carlo ----
    m0 = u2 + 3
    label(ws, f"A{m0}", f"Monte Carlo simulation: {MC_ROWS:,} futures, each driver drawn from a triangular "
                        "(low, likely, high) distribution. Press F9 to draw again; results move slightly each time.")
    ws.merge_cells(f"A{m0}:N{m0}")
    s0 = m0 + 1
    stats = [("Mean NPV", "AVERAGE"), ("Median NPV", "MEDIAN"), ("P10 (1 in 10 worse than this)", "P10"),
             ("P90 (1 in 10 better than this)", "P90"), ("Standard deviation", "STDEV"),
             ("Probability NPV < 0", "PLOSS"), ("NPV at plan (for comparison)", "PLAN")]
    sim_top = s0 + len(stats) + 25
    sim_bot = sim_top + MC_ROWS - 1
    rng_ = f"$N${sim_top}:$N${sim_bot}"
    for i, (nm, kind) in enumerate(stats):
        r = s0 + i
        label(ws, f"A{r}", nm, bold=kind in ("MEDIAN", "PLOSS"))
        f_ = {"AVERAGE": f"=AVERAGE({rng_})", "MEDIAN": f"=MEDIAN({rng_})", "P10": f"=PERCENTILE({rng_},0.1)",
              "P90": f"=PERCENTILE({rng_},0.9)", "STDEV": f"=STDEV({rng_})",
              "PLOSS": f"=COUNTIF({rng_},\"<0\")/COUNT({rng_})", "PLAN": f"=N{plan_r}"}[kind]
        fx(ws, f"B{r}", f'=IFERROR({f_[1:]},"")', "0.0%" if kind == "PLOSS" else "$#,##0;($#,##0);-",
           bold=kind in ("MEDIAN", "PLOSS"))
    note = s0 + len(stats)
    label(ws, f"A{note}", "Drivers are drawn independently. If two move together (e.g. a price cut that lifts "
                          "volume), the real spread differs. For exact, repeatable figures use the Business Case "
                          "skill's risk_analysis.py.", bold=False)
    ws.merge_cells(f"A{note}:H{note}")
    ws.row_dimensions[note].height = 30
    # histogram (20 bins)
    hz = note + 2
    header(ws, hz, ["Bin from", "Bin to", "Count"])
    ws.freeze_panes = None
    for i in range(20):
        r = hz + 1 + i
        fx(ws, f"A{r}", f"=MIN({rng_})+(MAX({rng_})-MIN({rng_}))*{i}/20", "$#,##0,,\"M\"")
        fx(ws, f"B{r}", f"=MIN({rng_})+(MAX({rng_})-MIN({rng_}))*{i+1}/20", "$#,##0,,\"M\"")
        op = "<=" if i == 19 else "<"
        fx(ws, f"C{r}", f'=COUNTIFS({rng_},">="&A{r},{rng_},"{op}"&B{r})', "0")
    hc = BarChart()
    hc.type = "col"
    hc.gapWidth = 10
    hc.title = "Distribution of simulated NPV"
    hc.height, hc.width = 7.5, 15
    hc.add_data(Reference(ws, min_col=3, min_row=hz, max_row=hz + 20), titles_from_data=True)
    hc.set_categories(Reference(ws, min_col=2, min_row=hz + 1, max_row=hz + 20))
    hc.series[0].graphicalProperties.solidFill = "1D3557"
    hc.legend = None
    hc.y_axis.majorGridlines = None
    hc.x_axis.delete = hc.y_axis.delete = False
    ws.add_chart(hc, f"E{hz}")
    # simulation table
    hdr = sim_top - 1
    for i, h in enumerate(["Run", "Price ×", "Units ×", "Var. cost ×", "Fixed ×", "Capex ×", "Rate",
                           "CF Y0", "CF Y1", "CF Y2", "CF Y3", "CF Y4", "CF Y5", "NPV"], 1):
        c = ws.cell(row=hdr, column=i, value=h)
        c.font, c.fill, c.alignment, c.border = H_FONT, H_FILL, CENTER, BOX
    order = ["price", "units", "variable_cost", "fixed_cost", "capex", "rate"]
    for j, key in enumerate(order):
        c = ws.cell(row=hdr, column=16 + j, value=f"Random {j+1}")
        c.font, c.fill, c.alignment, c.border = H_FONT, H_FILL, CENTER, BOX
    small = Font(name=F, size=8, color="000000")
    for n in range(MC_ROWS):
        r = sim_top + n
        ws.cell(row=r, column=1, value=n + 1).font = small
        for j, key in enumerate(order):
            d = rows[key]
            a, mo, b = f"$E${d}", f"$F${d}", f"$G${d}"
            u = f"{get_column_letter(16 + j)}{r}"
            ws.cell(row=r, column=16 + j, value="=RAND()").font = Font(name=F, size=8, color="999999")
            tri = (f"IF({b}={a},{mo},IF({u}<({mo}-{a})/({b}-{a}),{a}+SQRT({u}*({b}-{a})*({mo}-{a})),"
                   f"{b}-SQRT((1-{u})*({b}-{a})*({b}-{mo}))))")
            ws.cell(row=r, column=2 + j, value=f"={tri}" if key == "rate" else f"=1+{tri}")
            ws.cell(row=r, column=2 + j).font = small
            ws.cell(row=r, column=2 + j).number_format = "0.0%" if key == "rate" else "0.00"
        m = {k: f"${get_column_letter(2 + j)}{r}" for j, k in enumerate(order[:5])}
        for y in range(6):
            c = ws.cell(row=r, column=8 + y, value=_cf_formula(y, m))
            c.font, c.number_format = small, "$#,##0;($#,##0);-"
        c = ws.cell(row=r, column=14, value=f'=IF(COUNT(\'Business Case\'!B11:G11)=0,"",H{r}+NPV(G{r},I{r}:M{r}))')
        c.font, c.number_format = small, "$#,##0;($#,##0);-"


PERSPECTIVES = ["Financial", "Customer", "Internal process", "Learning and growth"]


def sheet_bsc(wb, L, mode):
    ws = wb.create_sheet("Balanced Scorecard")
    head(ws, "Balanced Scorecard", "1-2 measures per objective, 8-16 in all. Status: on target ≥100% of target, "
         "caution 90-99%, below plan <90% (inverted when lower is better).",
         [18, 30, 28, 11, 12, 11, 11, 11, 13, 16, 26, 20])
    header(ws, 5, ["Perspective", "Objective", "Measure", "Leading / lagging", "Better when", "Target", "Actual",
                   "% of target", "Status", "Owner", "Initiative", "Traces to"])
    rows = []
    if mode == "ledger":
        sc = g(L, "strategy_layer", "scorecard", default={}) or {}
        objs = {o.get("id"): o for o in sc.get("objectives", []) or []}
        for m in sc.get("measures", []) or []:
            o = objs.get(m.get("objective"), {})
            rows.append([o.get("perspective_label") or {"financial": "Financial", "customer": "Customer",
                                                         "internal": "Internal process",
                                                         "learning": "Learning and growth"}.get(o.get("perspective"), o.get("perspective")),
                         o.get("objective") or m.get("objective"), m.get("measure"), m.get("type"),
                         m.get("better", "Higher"), m.get("target"), m.get("actual"), m.get("owner"),
                         m.get("initiative"), m.get("traces_to")])
        if not rows:
            for k in g(L, "strategy_layer", "kpis", default=[]) or []:
                rows.append([None, None, k.get("kpi"), "Lagging", "Higher", None, None, k.get("owner"), None,
                             k.get("traces_to")])
    elif mode == "example":
        rows = [["Financial", "Grow operating profit to full potential", "Contribution per car ($)", "Lagging",
                 "Higher", 13000, 12400, "CFO", "I2 Close variable-cost gap", "Unit Economics"],
                ["Internal process", "Secure a second qualified cell supplier", "Supplier qualification pass rate",
                 "Leading", "Higher", 0.95, 0.97, "VP Quality", "I1 Second cell supplier", "Growth Barriers: supply"]]
    n = max(16, len(rows) + 2)
    for i in range(n):
        r = 6 + i
        row = rows[i] if i < len(rows) else [None] * 10
        for col, v in zip("ABCDEFGJKL", row):
            inp(ws, f"{col}{r}", v, "#,##0.00" if col in "FG" else None)
        fx(ws, f"H{r}", f'=IF(AND(ISNUMBER(F{r}),ISNUMBER(G{r}),F{r}<>0,G{r}<>0),IF(E{r}="Lower",F{r}/G{r},G{r}/F{r}),"")',
           "0%")
        fx(ws, f"I{r}", f'=IF(H{r}="",IF(C{r}="","","No actual yet"),IF(H{r}>=1,"On target",IF(H{r}>=0.9,"Caution","Below plan")))')
    last = 5 + n
    dv_list(ws, PERSPECTIVES, f"A6:A{last}")
    dv_list(ws, ["Leading", "Lagging"], f"D6:D{last}")
    dv_list(ws, ["Higher", "Lower"], f"E6:E{last}")
    traffic(ws, f"I6:I{last}", 'I6="On target"', 'I6="Caution"', 'I6="Below plan"')
    r = last + 2
    label(ws, f"A{r}", "Balance check")
    for i, p in enumerate(PERSPECTIVES):
        label(ws, f"B{r+1+i}", p, bold=False)
        fx(ws, f"C{r+1+i}", f'=COUNTIFS($A$6:$A${last},B{r+1+i},$C$6:$C${last},"<>")', "0")
        fx(ws, f"D{r+1+i}", f'=IF(C{r+1+i}=0,"Add a measure","OK")')
        traffic(ws, f"D{r+1+i}", f'D{r+1+i}="OK"', "FALSE", f'D{r+1+i}="Add a measure"')
    rr = r + 6
    label(ws, f"B{rr}", "Measures", bold=False)
    fx(ws, f"C{rr}", f'=COUNTA(C6:C{last})', "0")
    label(ws, f"B{rr+1}", "Share that are leading", bold=False)
    fx(ws, f"C{rr+1}", f'=IF(C{rr}=0,"",COUNTIFS(D6:D{last},"Leading",C6:C{last},"<>")/C{rr})', "0%")
    fx(ws, f"D{rr+1}", f'=IF(C{rr+1}="","",IF(C{rr+1}>=1/3,"OK","Add leading measures"))')
    traffic(ws, f"D{rr+1}", f'D{rr+1}="OK"', "FALSE", f'D{rr+1}="Add leading measures"')
    label(ws, f"B{rr+2}", "Measures with no owner", bold=False)
    fx(ws, f"C{rr+2}", f'=SUMPRODUCT((C6:C{last}<>"")*(J6:J{last}=""))', "0")


def sheet_map(wb, L, mode, tmpdir):
    ws = wb.create_sheet("Strategy Map")
    head(ws, "Strategy Map", "Objectives by perspective, bottom to top. 'Drives' lists the IDs of the objectives "
         "each one leads to in the level above.", [8, 20, 46, 18, 22])
    header(ws, 5, ["ID", "Perspective", "Objective", "Drives (IDs, ; separated)", "Check"])
    objs = []
    if mode == "ledger":
        sc = g(L, "strategy_layer", "scorecard", default={}) or {}
        links = sc.get("links", []) or []
        for o in sc.get("objectives", []) or []:
            drives = [l.get("to") for l in links if l.get("from") == o.get("id")] or o.get("drives", []) or []
            objs.append([o.get("id"), o.get("perspective"), o.get("objective"), ";".join(drives)])
    elif mode == "example":
        objs = [["F1", "financial", "Grow operating profit to full potential", ""],
                ["C1", "customer", "Win the beachhead: urban fleets", "F1"],
                ["I1", "internal", "Secure a second qualified cell supplier", "C1"],
                ["L1", "learning", "Supplier-quality engineering capability", "I1"]]
    norm = {"financial": "Financial", "customer": "Customer", "internal": "Internal process",
            "learning": "Learning and growth"}
    n = max(16, len(objs) + 2)
    for i in range(n):
        r = 6 + i
        o = objs[i] if i < len(objs) else [None] * 4
        inp(ws, f"A{r}", o[0])
        inp(ws, f"B{r}", norm.get(o[1], o[1]) if o[1] else None)
        inp(ws, f"C{r}", o[2])
        inp(ws, f"D{r}", o[3] or None)
        fx(ws, f"E{r}", f'=IF(A{r}="","",IF(AND(B{r}<>"Financial",D{r}=""),"Drives nothing",'
                        f'IF(AND(B{r}<>"Learning and growth",COUNTIF($D$6:$D${5+n},"*"&A{r}&"*")=0),"Nothing drives it","OK")))')
    last = 5 + n
    dv_list(ws, PERSPECTIVES, f"B6:B{last}")
    traffic(ws, f"E6:E{last}", 'E6="OK"', "FALSE", 'OR(E6="Drives nothing",E6="Nothing drives it")')
    ws[f"E5"].comment = Comment("Every objective except financial ones should drive one above it; every objective "
                                "except learning-and-growth ones should be driven by one below it.", "StratOS")
    if objs and mode != "blank":
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import csv
            import strategy_map as sm
            p = os.path.join(tmpdir, "map.csv")
            with open(p, "w", newline="") as f:
                w = csv.writer(f)
                w.writerow(["id", "perspective", "objective", "drives"])
                for o in objs:
                    w.writerow(o)
            png = os.path.join(tmpdir, "map.png")
            sm.draw(sm.load(p), png, "Strategy Map")
            from openpyxl.drawing.image import Image
            img = Image(png)
            img.width, img.height = 720, int(720 * 1462 / 2040)
            ws.add_image(img, "G5")
        except Exception as e:  # matplotlib missing: the table still works
            ws["G5"] = f"(Strategy map picture not drawn: {e.__class__.__name__})"
            ws["G5"].font = S_FONT


def sheet_cir(wb, L, mode, caps=None):
    ws = wb.create_sheet("GLO-BUS CIR")
    head(ws, "GLO-BUS Competitive Intelligence Report", "One row per company and product. Groups are set "
         "against the share-weighted industry average for that product. Analogues, not answers: you decide.",
         [11, 11, 12, 10, 10, 12, 24])
    header(ws, 5, ["Company", "Product", "Price ($)", "P/Q (stars)", "Share (%)", "Models", "Strategic group"])
    rows = []
    latest = sorted([c for c in (caps or []) if c.get("cir_rows")], key=lambda c: c.get("year", 0))[-1:]
    if latest and latest[0].get("cir_rows"):
        title_note = f"From the capture of Year {latest[0].get('year')}"
        rows = [[r.get("company"), (r.get("product") or "").title(), r.get("price"), r.get("pq"), r.get("share"),
                 r.get("models")] for r in latest[0]["cir_rows"] if (r.get("region") or "Global") in ("Global", "global", "")][:24]
        ws["A4"] = title_note
        ws["A4"].font = S_FONT
    elif mode == "example":
        rows = [["A", "Camera", 279, 4.2, 14.0, 5], ["B", "Camera", 239, 3.4, 16.5, 4], ["C", "Camera", 264, 4.0, 12.0, 5],
                ["D", "Camera", 319, 5.1, 11.0, 6], ["E", "Camera", 299, 3.6, 9.5, 5]]
    n = 24
    for i in range(n):
        r = 6 + i
        row = rows[i] if i < len(rows) else [None] * 6
        for col, v, f_ in zip("ABCDEF", row, [None, None, "$#,##0", "0.0", "0.0", "0"]):
            inp(ws, f"{col}{r}", v, f_)
    last = 5 + n
    rng = lambda c: f"${c}$6:${c}${last}"
    for i in range(n):
        r = 6 + i
        avg_p = f'SUMPRODUCT(({rng("B")}=B{r})*{rng("C")}*{rng("E")})/SUMIF({rng("B")},B{r},{rng("E")})'
        avg_q = f'SUMPRODUCT(({rng("B")}=B{r})*{rng("D")}*{rng("E")})/SUMIF({rng("B")},B{r},{rng("E")})'
        fx(ws, f"G{r}", f'=IF(OR(A{r}="",B{r}="",C{r}="",D{r}="",E{r}=""),"",IFERROR(IF(C{r}>{avg_p},'
                        f'IF(D{r}>={avg_q},"Premium differentiator","Stuck in the middle"),'
                        f'IF(D{r}>={avg_q},"Value leader","Low-cost / economy")),""))')
    dv_list(ws, ["Camera", "Drone"], f"B6:B{last}")
    traffic(ws, f"G6:G{last}", 'OR(G6="Premium differentiator",G6="Value leader")', 'G6="Low-cost / economy"',
            'G6="Stuck in the middle"')
    r = last + 2
    label(ws, f"A{r}", "Industry averages (share-weighted)")
    for i, prod in enumerate(["Camera", "Drone"]):
        label(ws, f"A{r+1+i}", prod, bold=False)
        fx(ws, f"C{r+1+i}", f'=IFERROR(SUMPRODUCT(({rng("B")}="{prod}")*{rng("C")}*{rng("E")})/SUMIF({rng("B")},"{prod}",{rng("E")}),"")', "$#,##0")
        fx(ws, f"D{r+1+i}", f'=IFERROR(SUMPRODUCT(({rng("B")}="{prod}")*{rng("D")}*{rng("E")})/SUMIF({rng("B")},"{prod}",{rng("E")}),"")', "0.00")
    label(ws, f"C{r}", "Price")
    label(ws, f"D{r}", "P/Q")


def expand_fields(spec):
    """Expand the field templates in globus-fields.json into one row per product / region."""
    out = []
    P, R = spec["products"], spec["regions"]
    for f in spec["fields"]:
        if f["per"] == "once":
            out.append(dict(f))
        elif f["per"] == "product":
            for pk, pl in P.items():
                out.append({**f, "key": f["key"].format(p=pk), "label": f["label"].format(P=pl)})
        else:
            for pk, pl in P.items():
                for rk, rl in R.items():
                    out.append({**f, "key": f["key"].format(p=pk, r=rk), "label": f["label"].format(P=pl, R=rl)})
    return out


def sheet_planner(wb, L, mode, caps, years):
    ws = wb.create_sheet("GLO-BUS Planner")
    spec = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references",
                                       "globus-fields.json"), encoding="utf-8"))
    fields = expand_fields(spec)
    ny = len(years)
    head(ws, "GLO-BUS Decision Planner",
         "Plan each year's decisions here, test them in the game's projections, then enter them in GLO-BUS screen "
         "by screen in this order. Your team makes and enters every decision.",
         [22, 24, 40, 12] + [12] * ny)
    ws["A4"] = "Change threshold for the incremental-change check:"
    ws["A4"].font = B_FONT
    inp(ws, "D4", 0.15, "0%")
    ws["D4"].comment = Comment("Course guardrail: incremental changes, one direction at a time. Moves bigger "
                               "than this are flagged below.", "StratOS")
    header(ws, 5, ["Key (do not edit)", "Decision area", "Decision", "Unit"] + [f"Year {y}" for y in years])
    plans = {}
    for c in caps or []:
        for k, v in (c.get("decisions") or {}).items():
            plans.setdefault(c.get("year"), {})[k] = v
    if mode == "ledger":
        for y, d in (g(L, "globus", "plans", default={}) or {}).items():
            plans.setdefault(int(y), {}).update(d)
        st = g(L, "globus", "strategy", default={}) or {}
        if st and years:
            plans.setdefault(years[0], {})
            for pk in spec["products"]:
                if st.get(pk) and not plans[years[0]].get(f"strategy.{pk}"):
                    plans[years[0]][f"strategy.{pk}"] = st.get(pk)
    if mode == "example" and years:
        plans = {years[0]: {"strategy.camera": "Best-cost", "strategy.drone": "Focused differentiation",
                            "mkt.camera.na.price": 264, "mkt.camera.na.ads": 7500},
                 years[1]: {"strategy.camera": "Best-cost", "strategy.drone": "Focused differentiation",
                            "mkt.camera.na.price": 249, "mkt.camera.na.ads": 6800}} if ny > 1 else {}
    r0 = 6
    area_prev = None
    for i, f in enumerate(fields):
        r = r0 + i
        c = ws.cell(row=r, column=1, value=f["key"])
        c.font = Font(name=F, size=8, color="888888")
        label(ws, f"B{r}", f["area"] if f["area"] != area_prev else "", bold=True)
        area_prev = f["area"]
        label(ws, f"C{r}", f["label"], bold=False)
        label(ws, f"D{r}", f["unit"], bold=False)
        for j, y in enumerate(years):
            v = (plans.get(y) or {}).get(f["key"])
            fmt = {"$": "$#,##0.00", "%": "0%", "$000s": "#,##0", "count": "0", "days": "0", "stars": "0.0"}.get(f["unit"])
            inp(ws, f"{get_column_letter(5+j)}{r}", v, fmt)
    last = r0 + len(fields) - 1
    # change block
    top = last + 3
    label(ws, f"B{top-1}", "Change vs the year before (numbers only); amber = bigger than the threshold")
    header_cells = ["Key", "Decision area", "Decision", "Unit"] + [f"Year {y}" for y in years]
    for i, h in enumerate(header_cells, 1):
        c = ws.cell(row=top, column=i, value=h)
        c.font, c.fill, c.alignment, c.border = H_FONT, H_FILL, CENTER, BOX
    for i, f in enumerate(fields):
        r = top + 1 + i
        src = r0 + i
        ws.cell(row=r, column=1, value=f["key"]).font = Font(name=F, size=8, color="888888")
        label(ws, f"C{r}", f["label"], bold=False)
        for j in range(1, ny):
            cc, pc = get_column_letter(5 + j), get_column_letter(4 + j)
            fx(ws, f"{cc}{r}", f'=IF(AND(ISNUMBER({cc}{src}),ISNUMBER({pc}{src}),{pc}{src}<>0),{cc}{src}/{pc}{src}-1,"")', "0%")
    clast = top + len(fields)
    lc = get_column_letter(4 + ny)
    ws.conditional_formatting.add(f"F{top+1}:{lc}{clast}",
                                  FormulaRule(formula=[f'AND(ISNUMBER(F{top+1}),ABS(F{top+1})>$D$4)'], fill=AMBER))
    # guardrail: price and advertising cut together
    g0 = clast + 3
    label(ws, f"B{g0-1}", "Guardrail: price and advertising cut in the same year (course rule: protect gross margin)")
    for i, h in enumerate(["", "Product, region", "", ""] + [f"Year {y}" for y in years], 1):
        c = ws.cell(row=g0, column=i, value=h)
        c.font, c.fill, c.alignment, c.border = H_FONT, H_FILL, CENTER, BOX
    keys = [f["key"] for f in fields]
    k = 0
    for pk, pl in spec["products"].items():
        for rk, rl in spec["regions"].items():
            r = g0 + 1 + k
            k += 1
            label(ws, f"B{r}", f"{pl}, {rl}", bold=False)
            pr = top + 1 + keys.index(f"mkt.{pk}.{rk}.price")
            ad = top + 1 + keys.index(f"mkt.{pk}.{rk}.ads")
            for j in range(1, ny):
                cc = get_column_letter(5 + j)
                fx(ws, f"{cc}{r}", f'=IF(AND(ISNUMBER({cc}{pr}),ISNUMBER({cc}{ad})),IF(AND({cc}{pr}<0,{cc}{ad}<0),"Both cut",""),"")')
    ws.conditional_formatting.add(f"F{g0+1}:{lc}{g0+k}", FormulaRule(formula=[f'F{g0+1}="Both cut"'], fill=RED))
    note = g0 + k + 2
    for t_i, t in enumerate([
            "How to use: 1) plan the year in its column; 2) enter the same values in GLO-BUS and test the projections; "
            "3) record the projected KPIs; 4) after entering, run 'check our GLO-BUS entries against the plan' "
            "(GLO-BUS Capture), which reads the screens and flags any difference. Nothing is uploaded or entered for you.",
            "Labels follow the usual GLO-BUS screens; if your version differs, rename the Decision column but keep the "
            "Key column unchanged (the plan check uses it)."]):
        c = ws.cell(row=note + t_i, column=2, value=t)
        c.font, c.alignment = Font(name=F, size=9, italic=True), Alignment(wrap_text=False)
    ws.freeze_panes = "E6"


def _results_spec():
    return json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references",
                                       "globus-results.json"), encoding="utf-8"))


EXAMPLE_RESULTS = {
    6: {"kpis": {"eps": [1.85, 2.00], "roe": [0.142, 0.15], "stock": [22.4, 25.0], "credit": ["B+", "BB"], "image": [68, 70]},
        "company": {"score": 78, "rank": 3, "revenue": 412000, "net_profit": 18500, "cash": 14200},
        "product": {"camera": {"units": 1450, "price": 264, "pq": 4.0, "cost_unit": 182, "op_margin": 0.11, "ind_price": 276, "ind_pq": 4.0, "ind_cost_unit": 186,
                               "share": {"na": 12.0, "ea": 11.5, "ap": 12.4, "la": 13.0}},
                    "drone": {"units": 120, "price": 1237, "pq": 4.2, "cost_unit": 905, "op_margin": 0.09, "ind_price": 1195, "ind_pq": 4.1, "ind_cost_unit": 890,
                              "share": {"na": 12.0, "ea": 12.6, "ap": 11.1, "la": 12.2}}}},
    7: {"kpis": {"eps": [2.10, 2.15], "roe": [0.155, 0.155], "stock": [26.1, 27.0], "credit": ["BB-", "BB"], "image": [71, 72]},
        "company": {"score": 84, "rank": 2, "revenue": 455000, "net_profit": 21900, "cash": 19800},
        "product": {"camera": {"units": 1610, "price": 259, "pq": 4.2, "cost_unit": 176, "op_margin": 0.125, "ind_price": 271, "ind_pq": 4.1, "ind_cost_unit": 184,
                               "share": {"na": 13.1, "ea": 12.2, "ap": 13.0, "la": 13.6}},
                    "drone": {"units": 131, "price": 1229, "pq": 4.4, "cost_unit": 884, "op_margin": 0.105, "ind_price": 1188, "ind_pq": 4.2, "ind_cost_unit": 879,
                              "share": {"na": 12.8, "ea": 13.0, "ap": 11.9, "la": 12.5}}}},
    8: {"kpis": {"eps": [2.32, 2.30], "roe": [0.168, 0.16], "stock": [29.5, 29.0], "credit": ["BB", "BB"], "image": [74, 74]},
        "company": {"score": 89, "rank": 1, "revenue": 498000, "net_profit": 24800, "cash": 23500},
        "product": {"camera": {"units": 1720, "price": 255, "pq": 4.3, "cost_unit": 171, "op_margin": 0.135, "ind_price": 268, "ind_pq": 4.2, "ind_cost_unit": 181,
                               "share": {"na": 13.8, "ea": 12.9, "ap": 13.5, "la": 14.1}},
                    "drone": {"units": 142, "price": 1219, "pq": 4.6, "cost_unit": 870, "op_margin": 0.112, "ind_price": 1181, "ind_pq": 4.3, "ind_cost_unit": 871,
                              "share": {"na": 13.4, "ea": 13.6, "ap": 12.5, "la": 13.0}}}},
}


def sheet_year_results(wb, year, res, decisions, cir_rows, spec, fields, mode):
    """One tab per GLO-BUS year. Returns {metric_key: cell} for the Tracking sheet."""
    ws = wb.create_sheet(f"Y{year} Results")
    head(ws, f"GLO-BUS Year {year} results", ("Example values (illustrative)." if mode == "example" else
         "From the team's capture of this year's reports. Correct any value that was misread.") +
         " Figures in the units shown; edit the cream cells.", [34, 16, 16, 16, 14])
    cells = {}
    r = 5
    header(ws, r, ["Scored KPI", "Actual", "Investor expectation", "Gap", "Met?"])
    ws.freeze_panes = None
    kp = (res or {}).get("kpis", {})
    for k in spec["kpis"]:
        r += 1
        a, t = (kp.get(k["key"]) or [None, None]) if isinstance(kp.get(k["key"]), list) else \
            ((kp.get(k["key"]) or {}).get("actual"), (kp.get(k["key"]) or {}).get("target"))
        label(ws, f"A{r}", k["label"], bold=False)
        inp(ws, f"B{r}", a, None if k["fmt"] == "@" else k["fmt"])
        inp(ws, f"C{r}", t, None if k["fmt"] == "@" else k["fmt"])
        if k["key"] == "credit":
            fx(ws, f"D{r}", f'=IF(OR(B{r}="",C{r}=""),"",IFERROR(MATCH(C{r},CreditScale,0)-MATCH(B{r},CreditScale,0),""))', "+0;-0;0")
            fx(ws, f"E{r}", f'=IF(D{r}="","",IF(D{r}>=0,"Yes","No"))')
        else:
            fx(ws, f"D{r}", f'=IF(AND(ISNUMBER(B{r}),ISNUMBER(C{r})),B{r}-C{r},"")', k["fmt"])
            fx(ws, f"E{r}", f'=IF(D{r}="","",IF(D{r}>=0,"Yes","No"))')
        cells[f"kpi.{k['key']}"] = f"B{r}"
        cells[f"kpi.{k['key']}.target"] = f"C{r}"
    traffic(ws, f"E6:E{r}", f'E6="Yes"', "FALSE", f'E6="No"')
    ws[f"D5"].comment = Comment("Credit rating gap is in notches (positive = at or above expectation).", "StratOS")
    r += 2
    header(ws, r, ["Company result", "Value"])
    co = (res or {}).get("company", {})
    for k in spec["company"]:
        r += 1
        label(ws, f"A{r}", f"{k['label']} ({k['unit']})", bold=False)
        inp(ws, f"B{r}", co.get(k["key"]), k["fmt"])
        cells[f"co.{k['key']}"] = f"B{r}"
    r += 2
    header(ws, r, ["Product result", "Cameras", "Drones"])
    pr = (res or {}).get("product", {})
    top = r
    for k in spec["product"]:
        r += 1
        label(ws, f"A{r}", f"{k['label']} ({k['unit']})", bold=False)
        for j, p in enumerate(["camera", "drone"]):
            col = "BC"[j]
            inp(ws, f"{col}{r}", (pr.get(p) or {}).get(k["key"]), k["fmt"])
            cells[f"{p}.{k['key']}"] = f"{col}{r}"
    r += 1
    label(ws, f"A{r}", "Price vs industry average")
    for j, p in enumerate(["camera", "drone"]):
        col = "BC"[j]
        fx(ws, f"{col}{r}", f'=IF(AND(ISNUMBER({cells[p + ".price"]}),ISNUMBER({cells[p + ".ind_price"]})),'
                            f'{cells[p + ".price"]}/{cells[p + ".ind_price"]}-1,"")', "+0.0%;-0.0%;0.0%")
        cells[f"{p}.price_gap"] = f"{col}{r}"
    r += 1
    label(ws, f"A{r}", "Cost per unit vs industry average")
    for j, p in enumerate(["camera", "drone"]):
        col = "BC"[j]
        fx(ws, f"{col}{r}", f'=IF(AND(ISNUMBER({cells[p + ".cost_unit"]}),ISNUMBER({cells[p + ".ind_cost_unit"]})),'
                            f'{cells[p + ".cost_unit"]}/{cells[p + ".ind_cost_unit"]}-1,"")', "+0.0%;-0.0%;0.0%")
        cells[f"{p}.cost_gap"] = f"{col}{r}"
    r += 2
    header(ws, r, ["Market share (%)", "Cameras", "Drones"])
    s0 = r + 1
    for rk, rl in [("na", "North America"), ("ea", "Europe-Africa"), ("ap", "Asia-Pacific"), ("la", "Latin America")]:
        r += 1
        label(ws, f"A{r}", rl, bold=False)
        for j, p in enumerate(["camera", "drone"]):
            inp(ws, f"{'BC'[j]}{r}", ((pr.get(p) or {}).get("share") or {}).get(rk), "0.0")
    r += 1
    label(ws, f"A{r}", "Average across regions")
    for j, p in enumerate(["camera", "drone"]):
        col = "BC"[j]
        fx(ws, f"{col}{r}", f'=IF(COUNT({col}{s0}:{col}{r-1})=0,"",AVERAGE({col}{s0}:{col}{r-1}))', "0.0")
        cells[f"{p}.share_avg"] = f"{col}{r}"
    # decisions entered
    if decisions:
        r += 2
        header(ws, r, ["Decision entered this year", "Value", "Key"])
        labels = {f["key"]: f["label"] for f in fields}
        for k_, v in decisions.items():
            r += 1
            label(ws, f"A{r}", labels.get(k_, k_), bold=False)
            inp(ws, f"B{r}", v)
            ws[f"C{r}"] = k_
            ws[f"C{r}"].font = Font(name=F, size=8, color="888888")
    if cir_rows:
        r += 2
        header(ws, r, ["CIR: company", "Product", "Price", "P/Q", "Share (%)"])
        for row in cir_rows:
            r += 1
            for col, v in zip("ABCDE", [row.get("company"), (row.get("product") or "").title(), row.get("price"),
                                       row.get("pq"), row.get("share")]):
                inp(ws, f"{col}{r}", v)
    return ws.title, cells


TRACK_ROWS = [("EPS", "kpi.eps", "$0.00"), ("EPS expectation", "kpi.eps.target", "$0.00"),
              ("ROE", "kpi.roe", "0.0%"), ("ROE expectation", "kpi.roe.target", "0.0%"),
              ("Stock price", "kpi.stock", "$0.00"), ("Stock price expectation", "kpi.stock.target", "$0.00"),
              ("Credit rating", "kpi.credit", "@"), ("Credit rating score (AAA = 21)", "credit_score", "0"),
              ("Image rating", "kpi.image", "0"), ("Image rating expectation", "kpi.image.target", "0"),
              ("Overall score", "co.score", "0"), ("Rank", "co.rank", "0"),
              ("Net revenues ($000s)", "co.revenue", "#,##0"), ("Net profit ($000s)", "co.net_profit", "#,##0"),
              ("Ending cash ($000s)", "co.cash", "#,##0"),
              ("Cameras: market share (avg %)", "camera.share_avg", "0.0"), ("Drones: market share (avg %)", "drone.share_avg", "0.0"),
              ("Cameras: cost per unit ($)", "camera.cost_unit", "$#,##0"), ("Cameras: industry cost per unit ($)", "camera.ind_cost_unit", "$#,##0"),
              ("Drones: cost per unit ($)", "drone.cost_unit", "$#,##0"), ("Drones: industry cost per unit ($)", "drone.ind_cost_unit", "$#,##0"),
              ("Cameras: price ($)", "camera.price", "$#,##0"), ("Drones: price ($)", "drone.price", "$#,##0"),
              ("Cameras: P/Q", "camera.pq", "0.0"), ("Drones: P/Q", "drone.pq", "0.0"),
              ("Cameras: operating margin", "camera.op_margin", "0.0%"), ("Drones: operating margin", "drone.op_margin", "0.0%"),
              ("Cameras: industry price ($)", "camera.ind_price", "$#,##0"), ("Drones: industry price ($)", "drone.ind_price", "$#,##0"),
              ("Cameras: industry P/Q", "camera.ind_pq", "0.0"), ("Drones: industry P/Q", "drone.ind_pq", "0.0"),
              ("Cameras: price vs industry", "camera.price_gap", "+0.0%;-0.0%;0.0%"),
              ("Cameras: cost per unit vs industry", "camera.cost_gap", "+0.0%;-0.0%;0.0%"),
              ("Drones: price vs industry", "drone.price_gap", "+0.0%;-0.0%;0.0%"),
              ("Drones: cost per unit vs industry", "drone.cost_gap", "+0.0%;-0.0%;0.0%")]


def _public_by_company(caps):
    """Per year, per company: public scoreboard figures and CIR price / P/Q / share (averaged over regions)."""
    out = {}
    for c in sorted(caps or [], key=lambda c: c.get("year", 0)):
        y = c.get("year")
        d = out.setdefault(y, {})
        for r in c.get("scoreboard_rows") or []:
            d.setdefault(str(r.get("company")), {}).update({k: r.get(k) for k in ("score", "rank", "eps", "roe", "stock", "credit", "image")})
        agg = {}
        for r in c.get("cir_rows") or []:
            agg.setdefault((str(r.get("company")), r.get("product")), []).append(r)
        for (co, prod), rows in agg.items():
            g_ = [x for x in rows if (x.get("region") or "Global").lower() == "global"] or rows
            avg = lambda k: (sum(x.get(k) for x in g_ if x.get(k) is not None) / max(1, len([x for x in g_ if x.get(k) is not None]))
                             if any(x.get(k) is not None for x in g_) else None)
            d.setdefault(co, {}).update({f"{prod}.price": avg("price"), f"{prod}.pq": avg("pq"), f"{prod}.share": avg("share")})
    return out


def sheet_rivals(wb, caps, mode):
    """Rivals tab: the class-wide public reports only (scoreboard, CIR), year by year, with charts."""
    from openpyxl.chart import LineChart, Reference
    pub = _public_by_company(caps)
    if not pub and mode == "example":
        import random
        rnd = random.Random(3)
        pub = {}
        for y in (6, 7, 8):
            pub[y] = {}
            for i, co in enumerate("ABCDEFGH"):
                base = [80, 72, 78, 85, 70, 75, 82, 68][i] + (y - 6) * rnd.randint(-3, 5)
                pub[y][co] = {"score": base, "camera.price": 240 + i * 9 + rnd.randint(-6, 6),
                              "camera.pq": round(3.5 + i * 0.15 + rnd.uniform(-0.1, 0.1), 1),
                              "camera.share": round(12.5 + rnd.uniform(-3, 3), 1)}
            pub[y]["C"]["score"] = {6: 78, 7: 84, 8: 89}[y]
            ranked = sorted(pub[y], key=lambda k: -pub[y][k]["score"])
            for k in pub[y]:
                pub[y][k]["rank"] = ranked.index(k) + 1
    ws = wb.create_sheet("Rivals")
    years = sorted(pub)
    team = next((c.get("company") for c in (caps or []) if c.get("company")), "C" if mode == "example" else None)
    head(ws, "Where you stand: the rivals", "Only what the class-wide reports show every team (scoreboard, "
         "Competitive Intelligence Report). Nothing is taken from another team's screens. Rebuild after each round.",
         [26] + [11] * max(3, len(years)))
    if not years:
        label(ws, "A5", "Add capture files with scoreboard_rows and cir_rows to fill this tab.", bold=False)
        return
    comps = sorted({co for y in years for co in pub[y]})
    blocks = [("Overall score", "score", "0"), ("Rank", "rank", "0"), ("Cameras: price ($)", "camera.price", "$#,##0"),
              ("Cameras: P/Q", "camera.pq", "0.0"), ("Cameras: market share (%)", "camera.share", "0.0"),
              ("Drones: price ($)", "drone.price", "$#,##0"), ("Drones: P/Q", "drone.pq", "0.0"),
              ("Drones: market share (%)", "drone.share", "0.0")]
    r = 5
    starts = {}
    for title, key, fmt in blocks:
        if not any(pub[y].get(co, {}).get(key) is not None for y in years for co in comps):
            continue
        header(ws, r, [title] + [f"Year {y}" for y in years])
        starts[key] = r
        for i, co in enumerate(comps):
            rr = r + 1 + i
            c = ws.cell(row=rr, column=1, value=f"Company {co}" + ("  (you)" if co == team else ""))
            c.font = B_FONT if co == team else Font(name=F, size=10)
            for j, y in enumerate(years):
                inp(ws, f"{get_column_letter(2 + j)}{rr}", pub[y].get(co, {}).get(key), fmt)
                if co == team:
                    ws[f"{get_column_letter(2 + j)}{rr}"].fill = PatternFill("solid", fgColor="FBE9C9")
        r += len(comps) + 2
    ws.freeze_panes = None
    anchor = get_column_letter(len(years) + 3)
    n = 0
    for key, title in (("score", "Overall score by company"), ("camera.share", "Cameras: market share by company"),
                       ("drone.share", "Drones: market share by company")):
        if key not in starts:
            continue
        r0 = starts[key]
        ch = LineChart()
        ch.title, ch.height, ch.width = title, 7.5, 15
        ch.legend.position = "r"
        for i in range(len(comps)):
            ch.add_data(Reference(ws, min_col=1, max_col=1 + len(years), min_row=r0 + 1 + i, max_row=r0 + 1 + i),
                        from_rows=True, titles_from_data=True)
        ch.set_categories(Reference(ws, min_col=2, max_col=1 + len(years), min_row=r0, max_row=r0))
        for i, srs in enumerate(ch.series):
            mine = comps[i] == team
            srs.graphicalProperties.line.solidFill = "C9A55C" if mine else ["1D3557", "6C757D", "2D936C", "C44536", "457B9D", "8D6A9F", "A8DADC", "B5651D"][i % 8]
            srs.graphicalProperties.line.width = 42000 if mine else 15000
            srs.smooth = False
        ch.y_axis.majorGridlines = None
        ch.x_axis.delete = ch.y_axis.delete = False
        ws.add_chart(ch, f"{anchor}{5 + n * 17}")
        n += 1


def sheet_tracking(wb, year_tabs, spec):
    from openpyxl.chart import LineChart, Reference
    from openpyxl.workbook.defined_name import DefinedName
    ws = wb.create_sheet("Tracking")
    years = sorted(year_tabs)
    head(ws, "GLO-BUS trends", "Pulled by formula from the Year tabs. Rebuild the workbook after each round to add "
         "the new year. Charts update when a Year tab changes.", [36] + [12] * max(1, len(years)))
    # credit scale on a hidden column
    sc = spec["credit_scale"]
    colx = get_column_letter(3 + max(1, len(years)) + 6)
    for i, v in enumerate(sc):
        ws[f"{colx}{6+i}"] = v
        ws[f"{colx}{6+i}"].font = Font(name=F, size=8, color="BBBBBB")
    ws.column_dimensions[colx].hidden = True
    wb.defined_names["CreditScale"] = DefinedName("CreditScale", attr_text=f"Tracking!${colx}$6:${colx}${5+len(sc)}")
    header(ws, 5, ["Measure"] + [f"Year {y}" for y in years])
    rowof = {}
    for i, (lab, key, fmt) in enumerate(TRACK_ROWS):
        r = 6 + i
        rowof[key] = r
        label(ws, f"A{r}", lab, bold=not lab.endswith("expectation") and "industry" not in lab)
        for j, y in enumerate(years):
            col = get_column_letter(2 + j)
            tab, cells = year_tabs[y]
            if key == "credit_score":
                cr = f"{col}{rowof['kpi.credit']}"
                fx(ws, f"{col}{r}", f'=IF({cr}="","",IFERROR({len(sc)+1}-MATCH({cr},CreditScale,0),""))', fmt)
            else:
                ref = f"'{tab}'!{cells[key]}"
                fx(ws, f"{col}{r}", f'=IF({ref}="","",{ref})', None if fmt == "@" else fmt)
    last_col = get_column_letter(1 + len(years))
    charts = [("EPS vs investor expectation", ["kpi.eps", "kpi.eps.target"], "$"),
              ("ROE vs investor expectation", ["kpi.roe", "kpi.roe.target"], "%"),
              ("Stock price vs expectation", ["kpi.stock", "kpi.stock.target"], "$"),
              ("Image rating and credit score", ["kpi.image", "kpi.image.target", "credit_score"], ""),
              ("Market share (average of regions, %)", ["camera.share_avg", "drone.share_avg"], ""),
              ("Cost per unit vs industry", ["camera.cost_unit", "camera.ind_cost_unit", "drone.cost_unit", "drone.ind_cost_unit"], "$"),
              ("Net revenues and net profit ($000s)", ["co.revenue", "co.net_profit"], ""),
              ("Operating margin by product", ["camera.op_margin", "drone.op_margin"], "%"),
              ("Cameras: P/Q vs industry", ["camera.pq", "camera.ind_pq"], ""),
              ("Position vs industry: price premium and cost gap", ["camera.price_gap", "camera.cost_gap",
                                                                     "drone.price_gap", "drone.cost_gap"], "%")]
    anchor_row = 6 + len(TRACK_ROWS) + 2
    for n, (title, keys, unit) in enumerate(charts):
        ch = LineChart()
        ch.title = title
        ch.height, ch.width = 7.2, 13.5
        ch.legend.position = "b"
        for key in keys:
            r = rowof[key]
            data = Reference(ws, min_col=1, max_col=1 + len(years), min_row=r, max_row=r)
            ch.add_data(data, from_rows=True, titles_from_data=True)
        ch.set_categories(Reference(ws, min_col=2, max_col=1 + len(years), min_row=5, max_row=5))
        palette = ["1D3557", "C9A55C", "2D936C", "C44536"]
        for k_, srs in enumerate(ch.series):
            srs.graphicalProperties.line.solidFill = palette[k_ % 4]
            srs.graphicalProperties.line.width = 28000
            srs.smooth = False
            if "target" in keys[k_] or "ind_" in keys[k_] or "cost_gap" in keys[k_]:
                srs.graphicalProperties.line.dashStyle = "dash"
        if unit == "%":
            ch.y_axis.numFmt = "0%"
        ch.y_axis.majorGridlines = None
        ch.x_axis.delete = False
        ch.y_axis.delete = False
        col = "A" if n % 2 == 0 else get_column_letter(2 + max(5, len(years)) + 1)
        ws.add_chart(ch, f"{col}{anchor_row + (n // 2) * 16}")
    ws.freeze_panes = "B6"


def main():
    a = sys.argv
    ledger = a[a.index("--ledger") + 1] if "--ledger" in a else None
    out = a[a.index("--out") + 1] if "--out" in a else "StratOS_Workbook.xlsx"
    mode = "ledger" if ledger else ("blank" if "--blank" in a else "example")
    L = json.load(open(ledger, encoding="utf-8")) if ledger else {}
    caps = []
    for i, x in enumerate(a):
        if x == "--capture":
            caps.append(json.load(open(a[i + 1], encoding="utf-8")))
    y0 = int(a[a.index("--first-year") + 1]) if "--first-year" in a else 6
    years = list(range(y0, y0 + 10))
    title = a[a.index("--title") + 1] if "--title" in a else (
        f"{g(L, 'scope', 'industry', default='')} · base company {g(L, 'company_layer', 'focal_firm', default='')}"
        if ledger else "Strategy analysis worksheets")
    if mode == "ledger":
        LEGEND_TEXT[0] = ("Pre-filled from your StratOS ledger. Blue text on cream = inputs you can change.  "
                          "Black on grey = formulas (do not type over them).")
    elif mode == "blank":
        LEGEND_TEXT[0] = "Blue text on cream = your inputs.  Black on grey = formulas (do not type over them)."
    wb = Workbook()
    with tempfile.TemporaryDirectory() as tmp:
        sheet_start(wb, L, title, mode)
        sheet_pestel(wb, L, mode)
        sheet_forces(wb, L, mode)
        sheet_ksf(wb, L, mode)
        sheet_vrio(wb, L, mode)
        sheet_swot(wb, L, mode)
        sheet_matrix(wb, L, mode)
        sheet_ev(wb, L, mode)
        sheet_bc(wb, L, mode)
        sheet_risk(wb, L, mode)
        sheet_bsc(wb, L, mode)
        sheet_map(wb, L, mode, tmp)
        sheet_cir(wb, L, mode, caps)
        sheet_planner(wb, L, mode, caps, years)
        rspec = _results_spec()
        fspec = expand_fields(json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                                                          "references", "globus-fields.json"), encoding="utf-8")))
        year_tabs = {}
        if caps:
            for c in sorted(caps, key=lambda c: c.get("year", 0)):
                if c.get("results") or c.get("decisions"):
                    year_tabs[c.get("year")] = sheet_year_results(wb, c.get("year"), c.get("results"), c.get("decisions"),
                                                                  c.get("cir_rows"), rspec, fspec, mode)
        elif mode == "example":
            for y, res in EXAMPLE_RESULTS.items():
                year_tabs[y] = sheet_year_results(wb, y, res, None, None, rspec, fspec, mode)
        else:
            year_tabs[years[0]] = sheet_year_results(wb, years[0], None, None, None, rspec, fspec, mode)
        sheet_tracking(wb, year_tabs, rspec)
        sheet_rivals(wb, caps, mode)
        for ws in wb.worksheets:
            ws.sheet_properties.tabColor = GOLD if (ws.title.startswith("GLO-BUS") or ws.title in ("Start", "Tracking", "Rivals")
                                                    or ws.title.endswith(" Results")) else NAVY
        wb.save(out)
    print(json.dumps({"out": out, "mode": mode, "sheets": [ws.title for ws in wb.worksheets]}))


if __name__ == "__main__":
    main()
