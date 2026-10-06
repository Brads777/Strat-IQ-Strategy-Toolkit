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
            ("Expected Value", "Scenario probabilities × NPVs, expected NPV, worst case, maximin, value of information."),
            ("Business Case", "Driver-based cash flows, NPV, IRR and cumulative cash."),
            ("Balanced Scorecard", "Objectives and measures in four perspectives, leading vs lagging, status vs target, balance check."),
            ("Strategy Map", "Objectives by perspective and their cause-and-effect links; picture included when built from a ledger."),
            ("GLO-BUS CIR", "Paste the CIR figures; each company is placed in a strategic group automatically."),
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
        sheet_bsc(wb, L, mode)
        sheet_map(wb, L, mode, tmp)
        sheet_cir(wb, L, mode, caps)
        sheet_planner(wb, L, mode, caps, years)
        for ws in wb.worksheets:
            ws.sheet_properties.tabColor = GOLD if ws.title in ("Start", "GLO-BUS CIR", "GLO-BUS Planner") else NAVY
        wb.save(out)
    print(json.dumps({"out": out, "mode": mode, "sheets": [ws.title for ws in wb.worksheets]}))


if __name__ == "__main__":
    main()
