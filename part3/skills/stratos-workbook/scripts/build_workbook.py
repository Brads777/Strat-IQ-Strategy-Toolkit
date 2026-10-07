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
    rows = [("How to use", "Each sheet is one StratOS step, in process order. Type only in the cream cells (blue text). Grey "
                           "cells are formulas: they score, rank and flag automatically. Every finding should name "
                           "its evidence, the same rule StratOS follows."),
            ("Colour key", "Blue on cream = input · black on grey = formula · green / amber / red = status."),
            ("Management Interviews", "Start here. What management told you: the decisions they need made, the goals you "
                                      "must reach, the questions they need answered, nine questions every team answers, "
                                      "your own questions, and the takeaways you hold yourselves to."),
            ("PART 1 · THE INDUSTRY", ""),
            ("Industry Overview", "Setup (scope, competitors, base company) and the industry introduction: market size side by side, a CAGR calculator, segments, top-4 share and HHI, history, life-cycle stage."),
            ("Competitive Analysis", "Each competitor's financials and moat against the peer median, margin rank, moat score, signals, and annual-report seeds for PESTEL."),
            ("PESTEL", "Macro findings with impact × certainty priority and the P&L line each one hits."),
            ("Five Forces", "Sub-factor scores roll up to each force and to an industry attractiveness score."),
            ("Trending Factors", "Candidate drivers through the four tests; Driver or Demoted, and a 3-5 driver check."),
            ("KSF Scorecard", "Weighted KSFs, every competitor scored, totals and rank; weights must sum to 100%."),
            ("Strategic Mapping", "Every company scored on two vectors, plotted on a map, and the white-space candidates with ERRC and a capability stamp."),
            ("PART 2 · THE COMPANY", ""),
            ("Value Chain", "Activities by cost share and value share; value minus cost reads as differentiating engine, in balance or value trap."),
            ("Unit Economics", "Contribution, break-even, margin of safety, LTV, LTV/CAC, CAC payback and a sensitivity table (J-1)."),
            ("Resources & Capabilities", "Resources, capabilities (threshold or distinctive) and core competencies."),
            ("VRIO", "Yes / No / ? for each test; the verdict and the KSF reality check are calculated."),
            ("Full Potential", "The profit gap to benchmark, driver by driver in sequence, with a bridge chart (K-1)."),
            ("Growth Barriers", "Six barriers marked binding, tight or slack; the binding constraint is named (K-2)."),
            ("SWOT-TOWS", "Four traced lists and the TOWS options that pair them."),
            ("PART 3 · THE STRATEGY", ""),
            ("Positioning", "The strategy you chose, in your words, and five fit tests including management fit."),
            ("Strategic Options", "SCQ framing and three or more options plus do nothing, each staged with a gate (P)."),
            ("Decision Matrix", "Criteria weights × option scores, with a weighted total and rank; do nothing included."),
            ("Business Case", "Driver-based cash flows, NPV, IRR and cumulative cash (Q-1)."),
            ("Expected Value", "Scenario probabilities × NPVs, expected NPV, worst case, maximin, value of information, and a Bayes' rule pilot check (Q-2)."),
            ("Risk Analysis", "A tornado chart and a 1,000-run Monte Carlo simulation over your low / likely / high ranges (Q-3)."),
            ("Pricing", "Optional: price points against expected volume; the profit-maximising price inside the acceptable range."),
            ("Stress Test", "Assumption audit with headroom, competitor war-game, and a risk register with owners and triggers (R)."),
            ("Go-to-Market", "Beachhead, ICP, a channel funnel worked back to CAC, CAC checked against LTV, launch phases (T)."),
            ("Initiatives", "RICE scores and rank; every initiative traces to a finding (S)."),
            ("Operating Model", "Decision rights (RAPID) and a stakeholder power-interest map."),
            ("Execution Roadmap", "First 100 days as bars by week, milestones and stage gates (S)."),
            ("Balanced Scorecard", "Objectives and measures in four perspectives, leading vs lagging, status vs target, balance check (U)."),
            ("Strategy Map", "Objectives by perspective and their cause-and-effect links (U)."),
            ("GLO-BUS", ""),
            ("GLO-BUS CIR", "Paste the CIR figures; each company is placed in a strategic group automatically."),
            ("GLO-BUS Planner", "Plan every decision for each year in screen order; flags big changes and years where price and "
                                "advertising are both cut. You enter the decisions in GLO-BUS yourself."),
            ("Season by Year", "All years on one tab: every decision entered (top) and every result (below), each year "
                               "followed by its change (▲ ▼, green = better). The first columns stay put as you scroll."),
            ("Competition by Year", "Every company's score, rank, KPIs, price, P/Q and share by year with the change, "
                                    "from the class-wide reports only, plus your rank on each measure."),
            ("KPI Charts", "Graphs of how you're doing: KPIs vs investor expectations, score by company, rank, share, "
                           "cost per unit and position vs the industry, revenue, profit and margins."),
            ("Findings & Questions", "Findings, watch items and questions to consider, year by year (filled from the "
                                     "weekly review), with the team's response and status."),
            ("Your work stays yours", "In graded work, the inputs, choices and every Impact Summary are the student's. "
                                      "The workbook calculates; it never decides.")]
    r = 6
    for k, v in rows:
        ws.cell(row=r, column=2, value=k).font = B_FONT
        if not v:
            ws.cell(row=r, column=2).font = Font(name=F, size=10, bold=True, color=GOLD)
        c = ws.cell(row=r, column=3, value=v)
        c.font, c.alignment = Font(name=F, size=10), WRAP
        r += 1
    ws.cell(row=r + 1, column=2, value="© 2026 Brad Scheller · StratOS Strategy Lab · Apache-2.0").font = S_FONT


MGMT_CORE = [
    ("Goals", "Which scored measures matter most to management: EPS, ROE, stock price, credit rating or image rating?"),
    ("Goals", "What would management call a successful season, and what would be a failure?"),
    ("Strategy", "What strategy does management favour for cameras, and for drones? Why?"),
    ("Markets", "Are there regions or segments management wants to lead in, or to avoid?"),
    ("Risk", "How much risk will management accept: debt, issuing stock, dividends, the lowest credit rating it will tolerate?"),
    ("Brand", "Are there minimum quality, warranty, image or CSR standards the company must keep?"),
    ("Operations", "What are management's views on capacity, workforce and pay?"),
    ("Rivals", "What does management expect competitors to do?"),
    ("Decision rights", "Which decisions must the team check with management before entering them?"),
]
MGMT_TOUCHES = ["EPS", "ROE", "Stock price", "Credit rating", "Image rating", "Product design", "Marketing",
                "Operations", "Compensation", "CSR", "Finance", "Whole strategy"]


def sheet_mgmt(wb, L, mode):
    ws = wb.create_sheet("Management Interviews")
    head(ws, "Management Interviews", "What management told you, in their words. It sets up everything after it: the "
         "memo's Key Issues and Exhibit B, the decision criteria, the strategy you choose, and the weekly check.",
         [6, 16, 46, 40, 30, 40, 18, 18, 34])
    mb = (g(L, "company_layer", "management_brief", default={}) or g(L, "globus", "management_brief", default={}) or {}) \
        if mode == "ledger" else {}
    ex = mode == "example"
    r = 5
    # ---- 1. Key issues (mirrors the memo's Key Issues section and Exhibit B) ----
    label(ws, f"A{r}", "1. Key issues from the interview  (these become your memo's Key Issues and Exhibit B)")
    ws.merge_cells(f"A{r}:I{r}")
    r += 1
    label(ws, f"A{r}", "Central problem: the decision management needs made", bold=False)
    ws.merge_cells(f"A{r}:B{r}")
    inp(ws, f"C{r}", mb.get("central_problem") or ("[e.g. How should Company C position cameras and drones to beat "
                                                   "investor expectations over the season?]" if ex else None))
    ws.merge_cells(f"C{r}:I{r}")
    ws.row_dimensions[r].height = 32
    r += 2
    blocks = [("Decisions management needs us to make", "decisions", "D", ["Decision", "By when", "Notes"]),
              ("Required goals (the decision criteria come from these)", "goals", "B",
               ["Goal", "Measure / KPI", "Target", "By when"]),
              ("Questions management needs answered", "questions", "Q", ["Question", "Why it matters to them", ""])]
    for title, key, prefix, cols in blocks:
        header(ws, r, ["#", title, ""] + [c for c in cols[1:] if c])
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
        items = mb.get(key) or []
        for i in range(5):
            rr = r + 1 + i
            c = ws.cell(row=rr, column=1, value=f"{prefix}{i + 1}")
            c.font, c.alignment = B_FONT, CENTER
            it = items[i] if i < len(items) else {}
            if isinstance(it, str):
                it = {"text": it}
            vals = {"decisions": [it.get("text") or it.get("decision"), it.get("by_when"), it.get("notes")],
                    "goals": [it.get("text") or it.get("goal"), it.get("kpi"), it.get("target"), it.get("by_when")],
                    "questions": [it.get("text") or it.get("question"), it.get("why"), None]}[key]
            if ex and i == 0:
                vals = {"decisions": ["[e.g. Choose a competitive strategy for each product line]", "Year 6", ""],
                        "goals": ["[e.g. Beat investor expectations for EPS every year]", "EPS", "[from the scoreboard]", "Every year"],
                        "questions": ["[e.g. Can we grow share without hurting the credit rating?]", "[their reason]", None]}[key]
            ws.merge_cells(start_row=rr, start_column=2, end_row=rr, end_column=3)
            inp(ws, f"B{rr}", vals[0])
            for j, v in enumerate(vals[1:]):
                if key == "questions" and j == 1:
                    continue
                inp(ws, f"{get_column_letter(4 + j)}{rr}", v)
            if key == "goals":
                dv_list(ws, ["EPS", "ROE", "Stock price", "Credit rating", "Image rating", "Market share",
                             "Cost per unit", "Other"], f"E{rr}")
        r += 7
    ws.freeze_panes = None
    # ---- 2. Core questions ----
    label(ws, f"A{r}", "2. Questions every team must answer")
    ws.merge_cells(f"A{r}:I{r}")
    r += 1
    cols = ["#", "Area", "Question", "What management said", "Their words (quote)", "What it means for our strategy",
            "Touches", "How sure", "Follow-up question"]
    header(ws, r, cols)
    ws.freeze_panes = None
    answers = {str(a.get("id")): a for a in (mb.get("answers") or [])}
    core0 = r + 1
    for i, (area, q) in enumerate(MGMT_CORE):
        rr = r + 1 + i
        a = answers.get(f"M{i+1}", {})
        ws.cell(row=rr, column=1, value=f"M{i+1}").font = B_FONT
        label(ws, f"B{rr}", area, bold=False)
        label(ws, f"C{rr}", q, bold=False)
        vals = [a.get("said"), a.get("quote"), a.get("meaning"), a.get("touches"), a.get("confidence"), a.get("follow_up")]
        if ex and i == 0:
            vals = ["[e.g. EPS and the credit rating come first]", "[\"We will not take on debt that risks our rating.\"]",
                    "[e.g. Growth must be funded mostly from earnings]", "Credit rating", "Stated", ""]
        for j, v in enumerate(vals):
            inp(ws, f"{get_column_letter(4 + j)}{rr}", v)
        ws.row_dimensions[rr].height = 42
    core1 = r + len(MGMT_CORE)
    r = core1 + 2
    # ---- 3. Team's own questions ----
    label(ws, f"A{r}", "3. Our own questions  (anything else the team asked)")
    ws.merge_cells(f"A{r}:I{r}")
    r += 1
    header(ws, r, cols)
    ws.freeze_panes = None
    own = mb.get("team_questions") or []
    own0 = r + 1
    for i in range(8):
        rr = r + 1 + i
        a = own[i] if i < len(own) else {}
        ws.cell(row=rr, column=1, value=f"T{i+1}").font = B_FONT
        for j, v in enumerate([a.get("area"), a.get("question"), a.get("said"), a.get("quote"), a.get("meaning"),
                               a.get("touches"), a.get("confidence"), a.get("follow_up")]):
            inp(ws, f"{get_column_letter(2 + j)}{rr}", v)
        ws.row_dimensions[rr].height = 30
    own1 = r + 8
    for rng_ in (f"G{core0}:G{core1}", f"G{own0}:G{own1}"):
        dv_list(ws, MGMT_TOUCHES, rng_)
    for rng_ in (f"H{core0}:H{core1}", f"H{own0}:H{own1}"):
        dv_list(ws, ["Stated", "Implied", "Our interpretation", "Not asked yet"], rng_)
    r = own1 + 2
    # ---- 4. Management brief ----
    label(ws, f"A{r}", "4. Management brief: the takeaways we hold ourselves to")
    ws.merge_cells(f"A{r}:I{r}")
    r += 1
    header(ws, r, ["#", "Takeaway", "", "From (row)", "How we'll check it each round", "", "", "", ""])
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
    ws.merge_cells(start_row=r, start_column=5, end_row=r, end_column=9)
    ws.freeze_panes = None
    tk = mb.get("takeaways") or []
    for i in range(5):
        rr = r + 1 + i
        t_ = tk[i] if i < len(tk) else {}
        if isinstance(t_, str):
            t_ = {"text": t_}
        ws.cell(row=rr, column=1, value=f"K{i+1}").font = B_FONT
        ws.merge_cells(start_row=rr, start_column=2, end_row=rr, end_column=3)
        inp(ws, f"B{rr}", t_.get("text"))
        inp(ws, f"D{rr}", t_.get("from"))
        ws.merge_cells(start_row=rr, start_column=5, end_row=rr, end_column=9)
        inp(ws, f"E{rr}", t_.get("check"))
    r += 7
    # ---- completeness ----
    label(ws, f"A{r}", "Completeness")
    ws.merge_cells(f"A{r}:B{r}")
    fx(ws, f"C{r}", f'=COUNTA(D{core0}:D{core1})&" of {len(MGMT_CORE)} required questions answered; "&'
                    f'COUNTA(C{own0}:C{own1})&" of the team\'s own questions recorded"')
    fx(ws, f"D{r}", f'=IF(COUNTA(D{core0}:D{core1})={len(MGMT_CORE)},"Complete",IF(COUNTA(D{core0}:D{core1})>=6,'
                    f'"Nearly there","Keep going"))', bold=True)
    traffic(ws, f"D{r}", f'D{r}="Complete"', f'D{r}="Nearly there"', f'D{r}="Keep going"')
    label(ws, f"A{r+1}", "Record what management said, not what you hoped they meant. Mark anything you are inferring "
                         "as 'Our interpretation'. This sheet stays with your team.", bold=False)
    ws.merge_cells(f"A{r+1}:I{r+1}")


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


# ---------- GLO-BUS season sheets (all years on one tab) ----------
UNIT_FMT = {"$": "$#,##0.00", "$000s": "#,##0", "stars": "0.0", "count": "0", "%": "0.0%", "days": "0",
            "per screen": "0.0", "$ per worker": "$#,##0", "$ per unit": "$#,##0.00", "000s shares": "#,##0",
            "score": "0", "text": "@"}
CHG_FMT = {"$#,##0.00": '"▲ "$#,##0.00;"▼ "$#,##0.00;"–"', "#,##0": '"▲ "#,##0;"▼ "#,##0;"–"',
           "0.0": '"▲ "0.0;"▼ "0.0;"–"', "0": '"▲ "0;"▼ "0;"–"', "0.0%": '"▲ "0.0%;"▼ "0.0%;"–"',
           "$#,##0": '"▲ "$#,##0;"▼ "$#,##0;"–"', "+0.0%;-0.0%;0.0%": '"▲ "0.0%;"▼ "0.0%;"–"', "@": "@",
           "$0.00": '"▲ "$0.00;"▼ "$0.00;"–"'}
# (section, label, key, fmt, better) ; better: up | down | None.  key "=..." means a formula row.
RESULT_ROWS = [
    ("Scored KPIs", "EPS", "kpis.eps.actual", "$0.00", "up"),
    ("Scored KPIs", "EPS: investor expectation", "kpis.eps.target", "$0.00", None),
    ("Scored KPIs", "ROE", "kpis.roe.actual", "0.0%", "up"),
    ("Scored KPIs", "ROE: investor expectation", "kpis.roe.target", "0.0%", None),
    ("Scored KPIs", "Stock price", "kpis.stock.actual", "$0.00", "up"),
    ("Scored KPIs", "Stock price: investor expectation", "kpis.stock.target", "$0.00", None),
    ("Scored KPIs", "Credit rating", "kpis.credit.actual", "@", None),
    ("Scored KPIs", "Credit rating: investor expectation", "kpis.credit.target", "@", None),
    ("Scored KPIs", "Credit rating score (AAA = 21)", "=credit", "0", "up"),
    ("Scored KPIs", "Image rating", "kpis.image.actual", "0", "up"),
    ("Scored KPIs", "Image rating: investor expectation", "kpis.image.target", "0", None),
    ("Company", "Overall score", "company.score", "0", "up"),
    ("Company", "Rank in the industry", "company.rank", "0", "down"),
    ("Company", "Net revenues ($000s)", "company.revenue", "#,##0", "up"),
    ("Company", "Net profit ($000s)", "company.net_profit", "#,##0", "up"),
    ("Company", "Ending cash ($000s)", "company.cash", "#,##0", "up"),
]
for _p, _pl in (("camera", "Cameras"), ("drone", "Drones")):
    RESULT_ROWS += [
        (_pl, f"{_pl}: units sold (000s)", f"product.{_p}.units", "#,##0", "up"),
        (_pl, f"{_pl}: average price ($)", f"product.{_p}.price", "$#,##0", None),
        (_pl, f"{_pl}: industry average price ($)", f"product.{_p}.ind_price", "$#,##0", None),
        (_pl, f"{_pl}: price vs industry", f"=gap:{_p}.price", "+0.0%;-0.0%;0.0%", None),
        (_pl, f"{_pl}: P/Q rating", f"product.{_p}.pq", "0.0", "up"),
        (_pl, f"{_pl}: industry average P/Q", f"product.{_p}.ind_pq", "0.0", None),
        (_pl, f"{_pl}: cost per unit ($)", f"product.{_p}.cost_unit", "$#,##0", "down"),
        (_pl, f"{_pl}: industry cost per unit ($)", f"product.{_p}.ind_cost_unit", "$#,##0", None),
        (_pl, f"{_pl}: cost per unit vs industry", f"=gap:{_p}.cost_unit", "+0.0%;-0.0%;0.0%", "down"),
        (_pl, f"{_pl}: operating margin", f"product.{_p}.op_margin", "0.0%", "up"),
        (_pl, f"{_pl}: share, North America (%)", f"product.{_p}.share.na", "0.0", "up"),
        (_pl, f"{_pl}: share, Europe-Africa (%)", f"product.{_p}.share.ea", "0.0", "up"),
        (_pl, f"{_pl}: share, Asia-Pacific (%)", f"product.{_p}.share.ap", "0.0", "up"),
        (_pl, f"{_pl}: share, Latin America (%)", f"product.{_p}.share.la", "0.0", "up"),
        (_pl, f"{_pl}: share, average of regions (%)", f"=avg:{_p}", "0.0", "up"),
    ]


def _dig(d, path):
    for k in path.split("."):
        if not isinstance(d, dict):
            return None
        d = d.get(k)
    return d


def _example_results_as_capture(y, res):
    kp = {k: {"actual": v[0], "target": v[1]} for k, v in res["kpis"].items()}
    return {"year": y, "results": {"kpis": kp, "company": res["company"], "product": res["product"]}}


def _season_years(caps, y0, mode):
    got = sorted({c.get("year") for c in caps if c.get("year") is not None})
    if mode == "example" and not got:
        got = sorted(EXAMPLE_RESULTS)
    last = max([y0 + 4] + got)
    return list(range(min([y0] + got), last + 1))


def _chg(ws, cell_now, cell_prev, ref, fmt, better):
    if fmt == "@":
        return
    fx(ws, ref, f'=IF(AND(ISNUMBER({cell_now}),ISNUMBER({cell_prev})),{cell_now}-{cell_prev},"")', CHG_FMT.get(fmt, fmt))
    c = ws[ref]
    c.font = Font(name=F, size=9, color="5F6B76")


def _color_changes(ws, refs, better):
    if not better or not refs:
        return
    rng = " ".join(refs)
    first = refs[0]
    good = f'AND(ISNUMBER({first}),{first}{">" if better == "up" else "<"}0)'
    bad = f'AND(ISNUMBER({first}),{first}{"<" if better == "up" else ">"}0)'
    ws.conditional_formatting.add(rng, FormulaRule(formula=[good], fill=GREEN))
    ws.conditional_formatting.add(rng, FormulaRule(formula=[bad], fill=RED))


def sheet_season(wb, L, mode, caps, fields, spec, years):
    """Season by Year: every decision (top) and result (below), one pair of columns per year."""
    from openpyxl.workbook.defined_name import DefinedName
    ws = wb.create_sheet("Season by Year")
    byyear = {c.get("year"): c for c in caps}
    if mode == "example" and not caps:
        byyear = {y: _example_results_as_capture(y, r) for y, r in EXAMPLE_RESULTS.items()}
    plans = {int(k): v for k, v in (g(L, "globus", "plans", default={}) or {}).items()} if mode == "ledger" else {}
    head(ws, "GLO-BUS season by year", "Every decision and result, one pair of columns per year: the value, then the "
         "change from the year before (▲ up, ▼ down; green = better, red = worse). The first three columns stay put "
         "as you scroll right. Rebuild after each round to add the new year.", [22, 40, 11] + [12, 10] * len(years))
    vcol = {y: get_column_letter(4 + 2 * i) for i, y in enumerate(years)}
    ccol = {y: get_column_letter(5 + 2 * i) for i, y in enumerate(years)}
    hdr = ["Area", "Decision or result", "Unit"]
    for y in years:
        hdr += [f"Year {y}", "Change"]
    header(ws, 5, hdr)
    ws.freeze_panes = "D6"
    r = 6
    # credit scale for the score row
    sc = spec["credit_scale"]
    sx = get_column_letter(6 + 2 * len(years) + 2)
    for i, v in enumerate(sc):
        ws[f"{sx}{6+i}"] = v
        ws[f"{sx}{6+i}"].font = Font(name=F, size=8, color="BBBBBB")
    ws.column_dimensions[sx].hidden = True
    wb.defined_names["CreditScale"] = DefinedName("CreditScale", attr_text=f"'Season by Year'!${sx}$6:${sx}${5+len(sc)}")
    rows_of = {}

    def band(text):
        nonlocal r
        c = ws.cell(row=r, column=1, value=text)
        c.font, c.fill = Font(name=F, size=11, bold=True, color=NAVY), PatternFill("solid", fgColor=BAND)
        for j in range(2, 4 + 2 * len(years)):
            ws.cell(row=r, column=j).fill = PatternFill("solid", fgColor=BAND)
        r += 1

    band("DECISIONS ENTERED  (from your captures; planned values in grey italics where nothing was captured)")
    for f_ in fields:
        if f_["area"].startswith("Projected KPIs"):
            continue
        fmt = UNIT_FMT.get(f_["unit"], "General")
        label(ws, f"A{r}", f_["area"], bold=False)
        label(ws, f"B{r}", f_["label"], bold=False)
        label(ws, f"C{r}", f_["unit"], bold=False)
        refs = []
        for i, y in enumerate(years):
            v = (byyear.get(y) or {}).get("decisions", {}).get(f_["key"]) if byyear.get(y) else None
            planned = False
            if v is None and plans.get(y, {}).get(f_["key"]) is not None:
                v, planned = plans[y][f_["key"]], True
            c = inp(ws, f"{vcol[y]}{r}", v, None if fmt == "@" else fmt)
            if planned:
                c.font = Font(name=F, size=10, italic=True, color="8A949E")
            if i:
                _chg(ws, f"{vcol[y]}{r}", f"{vcol[years[i-1]]}{r}", f"{ccol[y]}{r}", fmt, None)
                refs.append(f"{ccol[y]}{r}")
        rows_of[f_["key"]] = r
        r += 1
    r += 1
    band("RESULTS  (from your captures: the scorecard, company and product reports)")
    for sec, lab, key, fmt, better in RESULT_ROWS:
        label(ws, f"A{r}", sec, bold=False)
        label(ws, f"B{r}", lab, bold=better is not None and not lab.endswith("expectation"))
        rows_of[key] = r
        refs = []
        for i, y in enumerate(years):
            cell = f"{vcol[y]}{r}"
            if key == "=credit":
                cr = f"{vcol[y]}{rows_of['kpis.credit.actual']}"
                fx(ws, cell, f'=IF({cr}="","",IFERROR({len(sc)+1}-MATCH({cr},CreditScale,0),""))', fmt)
            elif key.startswith("=gap:"):
                p, k = key[5:].split(".", 1)
                a, b = f"{vcol[y]}{rows_of[f'product.{p}.{k}']}", f"{vcol[y]}{rows_of[f'product.{p}.ind_{k}']}"
                fx(ws, cell, f'=IF(AND(ISNUMBER({a}),ISNUMBER({b})),{a}/{b}-1,"")', fmt)
            elif key.startswith("=avg:"):
                p = key[5:]
                rs = [rows_of[f"product.{p}.share.{x}"] for x in ("na", "ea", "ap", "la")]
                rng = f"{vcol[y]}{rs[0]}:{vcol[y]}{rs[-1]}"
                fx(ws, cell, f'=IF(COUNT({rng})=0,"",AVERAGE({rng}))', fmt)
            else:
                v = _dig((byyear.get(y) or {}).get("results") or {}, key)
                inp(ws, cell, v, None if fmt == "@" else fmt)
            if i:
                _chg(ws, cell, f"{vcol[years[i-1]]}{r}", f"{ccol[y]}{r}", fmt, better)
                if fmt != "@":
                    refs.append(f"{ccol[y]}{r}")
        _color_changes(ws, refs, better)
        r += 1
    # KPI vs expectation flags
    for k in ("eps", "roe", "stock", "image"):
        ra, rt = rows_of[f"kpis.{k}.actual"], rows_of[f"kpis.{k}.target"]
        for y in years:
            ws.conditional_formatting.add(f"{vcol[y]}{ra}", FormulaRule(
                formula=[f'AND(ISNUMBER({vcol[y]}{ra}),ISNUMBER({vcol[y]}{rt}),{vcol[y]}{ra}>={vcol[y]}{rt})'], fill=GREEN))
            ws.conditional_formatting.add(f"{vcol[y]}{ra}", FormulaRule(
                formula=[f'AND(ISNUMBER({vcol[y]}{ra}),ISNUMBER({vcol[y]}{rt}),{vcol[y]}{ra}<{vcol[y]}{rt})'], fill=AMBER))
    data_years = [y for y in years if (byyear.get(y) or {}).get("results")]
    return {"rows": rows_of, "vcol": vcol, "years": years, "data_years": data_years}


COMP_METRICS = [("Overall score", "score", "0", "up"), ("Rank", "rank", "0", "down"), ("EPS ($)", "eps", "$0.00", "up"),
                ("ROE", "roe", "0.0%", "up"), ("Stock price ($)", "stock", "$0.00", "up"), ("Image rating", "image", "0", "up"),
                ("Credit rating", "credit", "@", None),
                ("Cameras: price ($)", "camera.price", "$#,##0", None), ("Cameras: P/Q", "camera.pq", "0.0", "up"),
                ("Cameras: market share (%)", "camera.share", "0.0", "up"),
                ("Drones: price ($)", "drone.price", "$#,##0", None), ("Drones: P/Q", "drone.pq", "0.0", "up"),
                ("Drones: market share (%)", "drone.share", "0.0", "up")]


def _example_public(years):
    import random
    rnd = random.Random(3)
    pub = {}
    for y in years[:3]:
        pub[y] = {}
        for i, co in enumerate("ABCDEFGH"):
            base = [80, 72, 78, 85, 70, 75, 82, 68][i] + (y - years[0]) * rnd.randint(-3, 5)
            pub[y][co] = {"score": base, "eps": round(1.3 + base / 100 + rnd.uniform(-.2, .2), 2),
                          "camera.price": 240 + i * 9 + rnd.randint(-6, 6),
                          "camera.pq": round(3.5 + i * 0.15 + rnd.uniform(-0.1, 0.1), 1),
                          "camera.share": round(12.5 + rnd.uniform(-3, 3), 1)}
        pub[y]["C"]["score"] = {0: 78, 1: 84, 2: 89}[y - years[0]]
        ranked = sorted(pub[y], key=lambda k: -pub[y][k]["score"])
        for k in pub[y]:
            pub[y][k]["rank"] = ranked.index(k) + 1
    return pub


def sheet_competition(wb, caps, mode, years):
    ws = wb.create_sheet("Competition by Year")
    pub = _public_by_company(caps)
    if not pub and mode == "example":
        pub = _example_public(years)
    team = next((str(c.get("company")) for c in (caps or []) if c.get("company")), "C" if mode == "example" else None)
    head(ws, "Competition by year", "Every company on the measures that decide the contest, from the class-wide reports "
         "only (scoreboard and Competitive Intelligence Report). Each year: the value, then the change (▲ ▼). Your row "
         "is highlighted; the last row of each block is your rank on that measure.", [26] + [11, 9] * len(years))
    vcol = {y: get_column_letter(2 + 2 * i) for i, y in enumerate(years)}
    ccol = {y: get_column_letter(3 + 2 * i) for i, y in enumerate(years)}
    comps = sorted({co for y in pub for co in pub[y]}) or (list("ABCDEFGH") if mode != "blank" else [])
    if not comps:
        comps = list("ABCDE")
    ws.freeze_panes = "B5"
    r = 5
    blocks = {}
    for title, key, fmt, better in COMP_METRICS:
        if pub and not any(pub[y].get(co, {}).get(key) is not None for y in pub for co in comps):
            continue
        hdr = [title]
        for y in years:
            hdr += [f"Year {y}", "Change"]
        header(ws, r, hdr)
        ws.freeze_panes = "B5"
        r0 = r + 1
        for i, co in enumerate(comps):
            rr = r0 + i
            c = ws.cell(row=rr, column=1, value=f"Company {co}" + ("  (you)" if co == team else ""))
            c.font = B_FONT if co == team else Font(name=F, size=10)
            refs = []
            for j, y in enumerate(years):
                cell = inp(ws, f"{vcol[y]}{rr}", (pub.get(y) or {}).get(co, {}).get(key), None if fmt == "@" else fmt)
                if co == team:
                    cell.fill = PatternFill("solid", fgColor="FBE9C9")
                if j:
                    _chg(ws, f"{vcol[y]}{rr}", f"{vcol[years[j-1]]}{rr}", f"{ccol[y]}{rr}", fmt, better)
                    if fmt != "@":
                        refs.append(f"{ccol[y]}{rr}")
            _color_changes(ws, refs, better)
        r1 = r0 + len(comps) - 1
        me = r0 + comps.index(team) if team in comps else None
        rr = r1 + 1
        if fmt != "@":
            label(ws, f"A{rr}", "Industry average", bold=False)
            for y in years:
                fx(ws, f"{vcol[y]}{rr}", f'=IF(COUNT({vcol[y]}{r0}:{vcol[y]}{r1})=0,"",AVERAGE({vcol[y]}{r0}:{vcol[y]}{r1}))', fmt)
            rr += 1
            if me and key != "rank" and better:
                label(ws, f"A{rr}", "Your rank on this measure")
                refs = []
                for j, y in enumerate(years):
                    c_ = f"{vcol[y]}{me}"
                    fx(ws, f"{vcol[y]}{rr}", f'=IF(ISNUMBER({c_}),RANK({c_},{vcol[y]}{r0}:{vcol[y]}{r1},{0 if better == "up" else 1}),"")',
                       "0", bold=True)
                    if j:
                        _chg(ws, f"{vcol[y]}{rr}", f"{vcol[years[j-1]]}{rr}", f"{ccol[y]}{rr}", "0", "down")
                        refs.append(f"{ccol[y]}{rr}")
                _color_changes(ws, refs, "down")
                rr += 1
        blocks[key] = (r0, r1, me)
        r = rr + 1
    sv = [v.get("score") for y in pub for v in pub[y].values() if isinstance(v.get("score"), (int, float))]
    return {"blocks": blocks, "vcol": vcol, "years": years, "comps": comps, "team": team,
            "score_range": (min(sv), max(sv)) if sv else None}


def sheet_kpi_charts(wb, season, comp):
    """KPI Charts: a contiguous chart-data table (formulas) at the bottom, charts on top."""
    from openpyxl.chart import LineChart, Reference
    ws = wb.create_sheet("KPI Charts")
    years = season.get("data_years") or season["years"][:1]
    head(ws, "Key performance indicators", "Charts update from Season by Year and Competition by Year for the years "
         "captured so far; rebuild the workbook after each round to add the new year. The chart data below the charts "
         "is formulas; do not type over it.", [34] + [11] * len(years))
    series = [  # (label, source, key)
        ("EPS", "s", "kpis.eps.actual"), ("EPS expectation", "s", "kpis.eps.target"),
        ("ROE", "s", "kpis.roe.actual"), ("ROE expectation", "s", "kpis.roe.target"),
        ("Stock price", "s", "kpis.stock.actual"), ("Stock price expectation", "s", "kpis.stock.target"),
        ("Image rating", "s", "kpis.image.actual"), ("Image rating expectation", "s", "kpis.image.target"),
        ("Credit rating score (AAA = 21)", "s", "=credit"),
        ("Overall score", "s", "company.score"), ("Rank", "s", "company.rank"),
        ("Net revenues ($000s)", "s", "company.revenue"), ("Net profit ($000s)", "s", "company.net_profit"),
        ("Cameras: share (%)", "s", "=avg:camera"), ("Drones: share (%)", "s", "=avg:drone"),
        ("Cameras: cost per unit", "s", "product.camera.cost_unit"), ("Cameras: industry cost per unit", "s", "product.camera.ind_cost_unit"),
        ("Drones: cost per unit", "s", "product.drone.cost_unit"), ("Drones: industry cost per unit", "s", "product.drone.ind_cost_unit"),
        ("Cameras: price vs industry", "s", "=gap:camera.price"), ("Cameras: cost vs industry", "s", "=gap:camera.cost_unit"),
        ("Drones: price vs industry", "s", "=gap:drone.price"), ("Drones: cost vs industry", "s", "=gap:drone.cost_unit"),
        ("Cameras: operating margin", "s", "product.camera.op_margin"), ("Drones: operating margin", "s", "product.drone.op_margin"),
    ]
    for co in comp["comps"]:
        if "score" in comp["blocks"]:
            series.append((f"Company {co}" + (" (you)" if co == comp["team"] else ""), "c", ("score", co)))
    fmts = {"ROE": "0.0%", "ROE expectation": "0.0%"}
    data0 = 60
    label(ws, f"A{data0 - 2}", "Chart data (formulas)")
    header(ws, data0 - 1, ["Series"] + [f"Y{y}" for y in years])
    ws.freeze_panes = None
    rowof = {}
    for i, (lab, src, key) in enumerate(series):
        rr = data0 + i
        rowof[lab] = rr
        label(ws, f"A{rr}", lab, bold=False)
        for j, y in enumerate(years):
            col = get_column_letter(2 + j)
            if src == "s":
                ref = f"'Season by Year'!{season['vcol'][y]}{season['rows'][key]}"
            else:
                r0, r1, me = comp["blocks"]["score"]
                ref = f"'Competition by Year'!{comp['vcol'][y]}{r0 + comp['comps'].index(key[1])}"
            fx(ws, f"{col}{rr}", f'=IF(ISNUMBER({ref}),{ref},"")',
               fmts.get(lab, "+0.0%;-0.0%;0.0%" if "vs industry" in lab else ("0.0%" if "margin" in lab else "General")))
    charts = [("EPS vs investor expectation", ["EPS", "EPS expectation"], "$0.00"),
              ("ROE vs investor expectation", ["ROE", "ROE expectation"], "0%"),
              ("Stock price vs investor expectation", ["Stock price", "Stock price expectation"], "$0"),
              ("Image rating vs investor expectation", ["Image rating", "Image rating expectation"], "0"),
              ("Credit rating score (AAA = 21, higher is better)", ["Credit rating score (AAA = 21)"], "0"),
              ("Overall score by company (scoreboard)", [s[0] for s in series if s[1] == "c"], "0"),
              ("Your rank (1 = top)", ["Rank"], "0"),
              ("Market share (average of regions, %)", ["Cameras: share (%)", "Drones: share (%)"], "0.0"),
              ("Cost per unit vs industry", ["Cameras: cost per unit", "Cameras: industry cost per unit",
                                             "Drones: cost per unit", "Drones: industry cost per unit"], "$0"),
              ("Position vs industry: price and cost", ["Cameras: price vs industry", "Cameras: cost vs industry",
                                                         "Drones: price vs industry", "Drones: cost vs industry"], "0%"),
              ("Net revenues and net profit ($000s)", ["Net revenues ($000s)", "Net profit ($000s)"], "#,##0"),
              ("Operating margin by product", ["Cameras: operating margin", "Drones: operating margin"], "0%")]
    palette = ["1D3557", "C9A55C", "2D936C", "C44536", "457B9D", "8D6A9F", "6C757D", "B5651D", "A8DADC"]
    for n, (title, labs, nf) in enumerate(charts):
        labs = [l for l in labs if l in rowof]
        if not labs:
            continue
        ch = LineChart()
        ch.title, ch.height, ch.width = title, 7.0, 12.5
        ch.legend.position = "b"
        for l in labs:
            ch.add_data(Reference(ws, min_col=1, max_col=1 + len(years), min_row=rowof[l], max_row=rowof[l]),
                        from_rows=True, titles_from_data=True)
        ch.set_categories(Reference(ws, min_col=2, max_col=1 + len(years), min_row=data0 - 1, max_row=data0 - 1))
        for k_, srs in enumerate(ch.series):
            l = labs[k_]
            mine = "(you)" in l
            srs.graphicalProperties.line.solidFill = GOLD if mine else palette[k_ % len(palette)]
            srs.graphicalProperties.line.width = 38000 if mine else 22000
            srs.smooth = False
            if "expectation" in l or "industry" in l and "vs" not in l or "cost vs" in l:
                srs.graphicalProperties.line.dashStyle = "dash"
        ch.y_axis.numFmt = nf
        if title.startswith("Your rank"):
            ch.y_axis.scaling.orientation = "maxMin"
            ch.y_axis.scaling.min = 1
        if title.startswith("Overall score") and comp.get("score_range"):
            lo, hi = comp["score_range"]
            ch.y_axis.scaling.min = max(0, int(lo // 5 * 5) - 5)
            ch.y_axis.scaling.max = int(hi // 5 * 5) + 10
        ch.y_axis.majorGridlines = None
        ch.x_axis.delete = ch.y_axis.delete = False
        ws.add_chart(ch, f"{'A' if n % 2 == 0 else 'H'}{5 + (n // 2) * 15}")
    # push the data table below the charts
    return ws


FINDING_TYPES = ["Finding", "Watch item", "Question to consider", "Management goal"]


def sheet_findings(wb, mode, reports):
    ws = wb.create_sheet("Findings & Questions")
    head(ws, "Findings and questions to consider", "One row per finding, watch item or question, year by year. "
         "Rows from the weekly report are filled in; add your own. The 'Our response' column is the team's.",
         [8, 18, 22, 48, 44, 44, 40, 14])
    header(ws, 5, ["Year", "Type", "Area", "What we see", "Evidence", "General lesson", "Our response or decision", "Status"])
    rows = []
    for rep in sorted(reports, key=lambda x: x.get("year", 0)):
        y = rep.get("year")
        for p, d in (rep.get("products") or {}).items():
            rows.append([y, "Finding", d.get("label"), f"Apparent position: {d.get('apparent')} ({d.get('confidence')})",
                         f"Price {d.get('price_gap') and f'{d['price_gap']:+.1%}'} vs industry; P/Q "
                         f"{d.get('pq_gap') and f'{d['pq_gap']:+.1f}'} stars; cost {d.get('cost_gap') and f'{d['cost_gap']:+.1%}'}",
                         "", None, "Open"])
        for w in rep.get("watch") or []:
            mg = w["title"].startswith("Management goal")
            area = (w.get("evidence") or "").split(":")[0] if mg else (w["title"].split(":")[0] if ":" in w["title"] else "")
            rows.append([y, "Management goal" if mg else "Watch item", area, w["title"], w.get("evidence"),
                         w.get("lesson"), None, "Open"])
        for q in rep.get("questions") or []:
            rows.append([y, "Question to consider", "", q, "", "", None, "Open"])
    if not rows and mode == "example":
        rows = [[7, "Watch item", "Drones", "The position your inputs show differs from the strategy you chose",
                 "Chose differentiation; price +3.5% and P/Q +0.2 stars look like best-cost",
                 "Teams that drift between positions usually pay for both and get credit for neither.", None, "Open"],
                [7, "Question to consider", "", "Which input did you change most this year, and did the result move the way "
                 "the projections said?", "", "", None, "Open"]]
    n = max(40, len(rows) + 15)
    for i in range(n):
        rr = 6 + i
        row = rows[i] if i < len(rows) else [None] * 8
        for j, v in enumerate(row):
            c = ws.cell(row=rr, column=1 + j)
            if j in (6, 7) or i >= len(rows):
                inp(ws, c.coordinate, v)
            else:
                c.value = v
                c.font, c.alignment, c.border = Font(name=F, size=10), WRAP, BOX
        ws.row_dimensions[rr].height = 44 if i < len(rows) else 20
    dv_list(ws, FINDING_TYPES, f"B6:B{5 + n}")
    dv_list(ws, ["Open", "Discussed", "Acted on", "Closed"], f"H6:H{5 + n}")
    traffic(ws, f"H6:H{5 + n}", 'OR(H6="Acted on",H6="Closed")', 'H6="Discussed"', 'H6="Open"')


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


# ---------- process-step sheets (one per StratOS step) ----------
def _grid(ws, r, headers, data, n, fmts=None, heights=None):
    """Header at row r, then n input rows filled from data (list of lists). Returns (first, last) data rows."""
    header(ws, r, headers)
    ws.freeze_panes = None
    fmts = fmts or [None] * len(headers)
    for i in range(n):
        rr = r + 1 + i
        row = data[i] if i < len(data) else [None] * len(headers)
        for j in range(len(headers)):
            v = row[j] if j < len(row) else None
            inp(ws, f"{get_column_letter(1 + j)}{rr}", v, fmts[j] if j < len(fmts) else None)
        if heights:
            ws.row_dimensions[rr].height = heights
    return r + 1, r + n


def _sec(ws, r, text, span="H"):
    c = ws.cell(row=r, column=1, value=text)
    c.font = Font(name=F, size=11, bold=True, color=NAVY)
    return r + 1


def _ids(xs):
    return ", ".join(xs) if isinstance(xs, list) else (xs or "")


def sheet_overview(wb, L, mode):
    ws = wb.create_sheet("Industry Overview")
    head(ws, "Setup and Industry Overview", "Part 1, steps 1-2. The scope every later step uses, and the business-plan-style "
         "introduction to the industry. Cite a source for every figure.", [30, 18, 14, 22, 30, 14, 14, 14])
    ex = mode == "example"
    sc = g(L, "scope", default={}) or {}
    ov = g(L, "industry_layer", "overview", default={}) or {}
    r = _sec(ws, 5, "Scope (from setup)")
    items = [("Industry", sc.get("industry") or ("[e.g. Global passenger electric vehicles]" if ex else None)),
             ("In scope / out of scope", sc.get("boundary_note") or ("[e.g. BEV + PHEV cars; excludes trucks]" if ex else None)),
             ("Geography", sc.get("geography") or ("Global" if ex else None)),
             ("Horizon", sc.get("horizon") or ("2026-2030" if ex else None)),
             ("Competitor set", _ids(sc.get("competitor_set")) or ", ".join(c.get("name", "") for c in (g(L, "competitors", default=[]) or [])) or ("[e.g. BYD, Tesla, VW Group]" if ex else None)),
             ("Base company", g(L, "company_layer", "focal_firm", default=None) or ("[e.g. BYD]" if ex else None))]
    for k, v in items:
        label(ws, f"A{r}", k, bold=False)
        inp(ws, f"B{r}", v)
        ws.merge_cells(f"B{r}:H{r}")
        r += 1
    r = _sec(ws, r + 1, "Market size (estimates differ by definition: show them side by side)")
    ms = [[m.get("value"), m.get("unit"), m.get("year"), m.get("publisher"), m.get("definition"),
           "Yes" if m.get("matches_scope") else ("No" if m.get("matches_scope") is False else None)]
          for m in (ov.get("market_size") or [])]
    if ex and not ms:
        ms = [[21, "million units", 2025, "[publisher]", "BEV + PHEV car sales", "Yes"]]
    a, b = _grid(ws, r, ["Value", "Unit", "Year", "Publisher", "Definition", "Matches scope?"], ms, 5)
    dv_list(ws, ["Yes", "No"], f"F{a}:F{b}")
    r = b + 2
    r = _sec(ws, r, "Growth: compound annual growth rate calculator")
    for k, v, f_ in (("Start value", 10 if ex else None, "#,##0.0"), ("End value", 21 if ex else None, "#,##0.0"),
                     ("Number of years", 5 if ex else None, "0")):
        label(ws, f"A{r}", k, bold=False)
        inp(ws, f"B{r}", v, f_)
        r += 1
    label(ws, f"A{r}", "CAGR")
    fx(ws, f"B{r}", f'=IFERROR((B{r-2}/B{r-3})^(1/B{r-1})-1,"")', "0.0%", bold=True)
    r += 2
    fc = [[x.get("publisher"), x.get("cagr"), x.get("to_year"), x.get("published")] for x in ((ov.get("growth") or {}).get("forecasts") or [])]
    a, b = _grid(ws, r, ["Forecast: publisher", "CAGR", "To year", "Published"], fc, 4, [None, "0.0%", "0", None])
    r = b + 2
    r = _sec(ws, r, "Segments and customers")
    sg = [[s.get("name"), s.get("share"), s.get("growth"), s.get("buyers")] for s in (ov.get("segments") or [])]
    a, b = _grid(ws, r, ["Segment", "Share", "Growth", "Who buys, and why"], sg, 5)
    r = b + 2
    r = _sec(ws, r, "Key players and concentration")
    pl = [[p.get("name"), p.get("share")] for p in ((ov.get("players") or {}).get("leaders") or [])]
    if ex and not pl:
        pl = [["[Leader 1]", 0.22], ["[Leader 2]", 0.12], ["[Leader 3]", 0.07], ["[Leader 4]", 0.05]]
    a, b = _grid(ws, r, ["Company", "Market share"], pl, 8, [None, "0.0%"])
    label(ws, f"D{a}", "Top-4 share")
    fx(ws, f"E{a}", f'=IF(COUNT(B{a}:B{b})<4,"",LARGE(B{a}:B{b},1)+LARGE(B{a}:B{b},2)+LARGE(B{a}:B{b},3)+LARGE(B{a}:B{b},4))',
       "0.0%", bold=True)
    label(ws, f"D{a+1}", "HHI (shares listed)")
    fx(ws, f"E{a+1}", f'=IF(COUNT(B{a}:B{b})=0,"",SUMPRODUCT(B{a}:B{b}*100,B{a}:B{b}*100))', "#,##0", bold=True)
    label(ws, f"D{a+2}", "Below 1,500 unconcentrated; above 2,500 highly concentrated.", bold=False)
    r = b + 2
    r = _sec(ws, r, "Recent history: the events that explain today's structure")
    tl = [[t.get("year"), t.get("event"), t.get("why_it_mattered")] for t in (ov.get("timeline") or [])]
    a, b = _grid(ws, r, ["Year", "Event", "Why it mattered"], tl, 8, ["0", None, None])
    for rr in range(a, b + 1):
        ws.merge_cells(f"C{rr}:H{rr}")
    r = b + 2
    r = _sec(ws, r, "Life-cycle stage")
    lc = ov.get("lifecycle") or {}
    label(ws, f"A{r}", "Stage", bold=False)
    inp(ws, f"B{r}", lc.get("stage") or ("growth" if ex else None))
    dv_list(ws, ["emerging", "growth", "shakeout", "mature", "declining"], f"B{r}")
    label(ws, f"C{r}", "What it implies", bold=False)
    inp(ws, f"D{r}", lc.get("implication"))
    ws.merge_cells(f"D{r}:H{r}")


def sheet_competitive(wb, L, mode):
    ws = wb.create_sheet("Competitive Analysis")
    head(ws, "Competitive Analysis", "Part 1, step 3. Each competitor's financials, moat and signals, benchmarked against the "
         "peer median. Same fiscal year for all; note the currency.", [20, 10, 9, 13, 11, 11, 11, 12, 12, 12, 12, 30])
    comps = g(L, "competitors", default=[]) or []
    rows = []
    for c in comps[:10]:
        f_ = c.get("financials") or {}
        m = c.get("moat") or {}
        num_ = lambda v: v if isinstance(v, (int, float)) else None
        rows.append([c.get("name"), f_.get("fiscal_year"), f_.get("currency"), num_(f_.get("revenue")),
                     num_(f_.get("gross_margin")), num_(f_.get("operating_margin")), num_(f_.get("rnd_pct")),
                     m.get("network"), m.get("switching"), m.get("scale"), m.get("intangibles"), c.get("apparent_strategy")])
    if mode == "example" and not rows:
        rows = [["[Firm A]", "FY2025", "USD", 120000, 0.18, 0.05, 0.07, "weak", "moderate", "strong", "moderate", "[cost leader at scale]"],
                ["[Firm B]", "FY2025", "USD", 40000, 0.24, 0.08, 0.10, "moderate", "moderate", "weak", "strong", "[premium tech brand]"]]
    r = _sec(ws, 5, "Financial benchmark and moat")
    hd = ["Company", "Fiscal year", "Currency", "Revenue (m)", "Gross margin", "Op. margin", "R&D % rev.",
          "Moat: network", "Moat: switching", "Moat: scale", "Moat: intangibles", "Apparent strategy"]
    a, b = _grid(ws, r, hd, rows, 10, [None, None, None, "#,##0", "0.0%", "0.0%", "0.0%"] + [None] * 5)
    dv_list(ws, ["weak", "moderate", "strong"], f"H{a}:K{b}")
    label(ws, f"A{b+1}", "Peer median")
    for col in "DEFG":
        fx(ws, f"{col}{b+1}", f'=IF(COUNT({col}{a}:{col}{b})=0,"",MEDIAN({col}{a}:{col}{b}))', ws[f"{col}{a}"].number_format, bold=True)
    r2 = b + 4
    header(ws, r2, ["Company", "Op. margin vs median", "Margin rank", "Moat score (0-8)"])
    ws.freeze_panes = None
    for i in range(10):
        rr, src = r2 + 1 + i, a + i
        fx(ws, f"A{rr}", f'=IF(A{src}="","",A{src})')
        fx(ws, f"B{rr}", f'=IF(OR(F{src}="",$F${b+1}=""),"",F{src}-$F${b+1})', "+0.0%;-0.0%;0.0%")
        fx(ws, f"C{rr}", f'=IF(F{src}="","",RANK(F{src},$F${a}:$F${b}))', "0")
        sc = "+".join(f'IF({c}{src}="strong",2,IF({c}{src}="moderate",1,0))' for c in "HIJK")
        fx(ws, f"D{rr}", f'=IF(A{src}="","",{sc})', "0")
    traffic(ws, f"B{r2+1}:B{r2+10}", f"AND(ISNUMBER(B{r2+1}),B{r2+1}>0.01)", f"AND(ISNUMBER(B{r2+1}),ABS(B{r2+1})<=0.01)",
            f"AND(ISNUMBER(B{r2+1}),B{r2+1}<-0.01)")
    r = r2 + 12
    r = _sec(ws, r, "Signals: what competitors are doing (hiring, patents, launches, capex, pricing)")
    sig = [[c.get("name"), s.get("kind"), s.get("observation"), s.get("inference")] for c in comps for s in (c.get("signals") or [])]
    header(ws, r, ["Company", "Kind", "Observation", "", "", "", "", "What it suggests", "", "", "", ""])
    ws.merge_cells(f"C{r}:G{r}")
    ws.merge_cells(f"H{r}:L{r}")
    ws.freeze_panes = None
    a, b = r + 1, r + 10
    for i in range(10):
        rr = a + i
        d = sig[i] if i < len(sig) else [None] * 4
        inp(ws, f"A{rr}", d[0]); inp(ws, f"B{rr}", d[1]); inp(ws, f"C{rr}", d[2]); inp(ws, f"H{rr}", d[3])
        ws.merge_cells(f"C{rr}:G{rr}")
        ws.merge_cells(f"H{rr}:L{rr}")
    dv_list(ws, ["hiring", "patents", "launch", "capex", "pricing", "partnership", "exit", "other"], f"B{a}:B{b}")
    r = b + 2
    r = _sec(ws, r, "Annual-report seeds for PESTEL (risk factors and management discussion)")
    seeds = [[s.get("dimension"), s.get("kind"), s.get("text"), s.get("pl_line"), len(s.get("firms") or [])]
             for s in (g(L, "ci", "pestel_seeds", default=[]) or [])]
    a, b = _grid(ws, r, ["PESTEL", "Kind", "Text", "P&L line", "Firms citing it"], seeds, 8, [None, None, None, None, "0"])
    dv_list(ws, ["P", "E", "S", "T", "Env", "L"], f"A{a}:A{b}")
    dv_list(ws, ["risk_factor", "mdna_trend"], f"B{a}:B{b}")


def sheet_drivers(wb, L, mode):
    ws = wb.create_sheet("Trending Factors")
    head(ws, "Trending Influence Factors", "Part 1, step 6. Candidates from PESTEL and Competitive Analysis; a driver must pass "
         "all four tests. Keep 3-5.", [8, 28, 14, 34, 16, 16, 10, 10, 10, 10, 13, 16])
    dr = g(L, "industry_layer", "drivers", default=[]) or []
    rows = [[d.get("id"), d.get("name"), _ids(d.get("from_pestel")), d.get("transmission"), d.get("pl_line"),
             _ids(d.get("forces_moved")), "Yes", "Yes", "Yes", "Yes", None, d.get("profit_pool")] for d in dr]
    if mode == "example" and not rows:
        rows = [["D1", "[Battery cost curve]", "P1", "[cheaper cells → lower input cost]", "cogs.inputs", "suppliers", "Yes", "Yes", "Yes", "Yes", None, "redistributing"],
                ["D2", "[Fuel-price spike]", "P7", "[one-off demand pull]", "revenue.volume", "substitutes", "No", "Yes", "Yes", "No", None, "expanding"]]
    hd = ["ID", "Candidate driver", "From (PESTEL / CI ids)", "Mechanism → P&L", "P&L line", "Forces moved",
          "Moves a force ≥1 pt?", "Moves P&L for most firms?", "Acts within horizon?", "Two source types?", "Verdict", "Profit pool"]
    a, b = _grid(ws, 5, hd, rows, 12, heights=30)
    dv_list(ws, ["Yes", "No"], f"G{a}:J{b}")
    dv_list(ws, ["expanding", "compressing", "redistributing"], f"L{a}:L{b}")
    for rr in range(a, b + 1):
        fx(ws, f"K{rr}", f'=IF(B{rr}="","",IF(COUNTIF(G{rr}:J{rr},"Yes")=4,"Driver","Demoted"))', bold=True)
    traffic(ws, f"K{a}:K{b}", f'K{a}="Driver"', "FALSE", f'K{a}="Demoted"')
    label(ws, f"A{b+2}", "Drivers kept")
    fx(ws, f"C{b+2}", f'=COUNTIF(K{a}:K{b},"Driver")&" of "&COUNTA(B{a}:B{b})&" candidates"', bold=True)
    fx(ws, f"D{b+2}", f'=IF(COUNTA(B{a}:B{b})=0,"",IF(AND(COUNTIF(K{a}:K{b},"Driver")>=3,COUNTIF(K{a}:K{b},"Driver")<=5),"OK: 3-5 drivers","Aim for 3-5 drivers"))')


def sheet_mapping(wb, L, mode):
    from openpyxl.chart import ScatterChart, Reference, Series
    ws = wb.create_sheet("Strategic Mapping")
    head(ws, "Strategic Mapping", "Part 1, step 8. Score each company on two vectors (0-10), see the map, then list the "
         "white space and stamp each candidate after VRIO.", [22, 12, 12, 14, 30, 26, 26, 26, 26, 14, 16])
    s6 = g(L, "company_layer", "s6_disruption", default={}) or g(L, "company_layer", "s5_conventional", default={}) or {}
    axes = s6.get("axes") or []
    comps = g(L, "competitors", default=[]) or []
    ax_names = [f"v{a}" for a in axes] if axes else []
    label(ws, "A5", "Horizontal axis (vector)")
    inp(ws, "B5", ax_names[0] if ax_names else ("[e.g. Ecosystem integration]" if mode == "example" else None))
    ws.merge_cells("B5:E5")
    label(ws, "A6", "Vertical axis (vector)")
    inp(ws, "B6", ax_names[1] if len(ax_names) > 1 else ("[e.g. Resale value]" if mode == "example" else None))
    ws.merge_cells("B6:E6")
    rows = []
    for c in comps[:10]:
        p = c.get("positions") or {}
        x = p.get(ax_names[0]) if ax_names else None
        y = p.get(ax_names[1]) if len(ax_names) > 1 else None
        sc = lambda v: v * 10 if isinstance(v, (int, float)) and v <= 1 else v
        rows.append([c.get("name"), sc(x), sc(y), None])
    if mode == "example" and not rows:
        rows = [["[Firm A]", 3, 4, 5], ["[Firm B]", 8, 6, 2], ["[Firm C]", 5, 3, 3]]
    a, b = _grid(ws, 8, ["Company", "X score (0-10)", "Y score (0-10)", "Size (share or revenue)"], rows, 10, [None, "0.0", "0.0", "0.0"])
    ch = ScatterChart()
    ch.title, ch.height, ch.width = "Strategic map", 9, 14
    ch.scatterStyle = "marker"
    ch.x_axis.title, ch.y_axis.title = "X vector", "Y vector"
    ch.x_axis.scaling.min = ch.y_axis.scaling.min = 0
    ch.x_axis.scaling.max = ch.y_axis.scaling.max = 10
    for i in range(10):
        rr = a + i
        s = Series(Reference(ws, min_col=3, min_row=rr), Reference(ws, min_col=2, min_row=rr), title_from_data=False)
        from openpyxl.chart.series import SeriesLabel
        from openpyxl.chart.data_source import StrRef
        s.tx = SeriesLabel(strRef=StrRef(f"'Strategic Mapping'!$A${rr}"))
        s.marker.symbol, s.marker.size = "circle", 11
        s.marker.graphicalProperties.solidFill = ["1D3557", "C9A55C", "2D936C", "C44536", "457B9D", "8D6A9F", "6C757D", "B5651D", "A8DADC", "264653"][i]
        s.marker.graphicalProperties.line.noFill = True
        s.graphicalProperties.line.noFill = True
        ch.series.append(s)
    ch.x_axis.delete = ch.y_axis.delete = False
    ch.legend.position = "r"
    ws.add_chart(ch, "F5")
    r = b + 12
    r = _sec(ws, r, "White space and blue-ocean candidates")
    cand = [[c.get("rank"), (c.get("at") or [None, None])[0], (c.get("at") or [None, None])[1], c.get("demand"), c.get("thesis"),
             _ids((c.get("errc") or {}).get("eliminate")), _ids((c.get("errc") or {}).get("reduce")),
             _ids((c.get("errc") or {}).get("raise")), _ids((c.get("errc") or {}).get("create")), c.get("capability")]
            for c in (g(L, "company_layer", "candidates", default=[]) or [])]
    if mode == "example" and not cand:
        cand = [[1, 8.5, 2, "unpriced", "[the empty corner and who it serves]", "[…]", "[…]", "[…]", "[…]", "UNVALIDATED"]]
    a, b = _grid(ws, r, ["Rank", "X", "Y", "Demand", "Thesis", "Eliminate", "Reduce", "Raise", "Create", "Capability (after VRIO)"],
                 cand, 5, ["0", "0.0", "0.0"] + [None] * 7, heights=36)
    dv_list(ws, ["UNVALIDATED", "supported", "gap"], f"J{a}:J{b}")
    dv_list(ws, ["unpriced", "evidence of demand", "tested"], f"D{a}:D{b}")
    traffic(ws, f"J{a}:J{b}", f'J{a}="supported"', f'J{a}="UNVALIDATED"', f'J{a}="gap"')


def sheet_value_chain(wb, L, mode):
    ws = wb.create_sheet("Value Chain")
    head(ws, "Value Chain", "Part 2, step 9. Each activity's share of cost and of the value customers pay for. Value minus "
         "cost shows where the firm earns its margin.", [8, 30, 18, 14, 14, 12, 12, 12, 24, 16])
    vc = g(L, "company_layer", "internal", "value_chain", default=[]) or []
    rows = [[v.get("id"), v.get("activity"), v.get("porter_category"), v.get("stage"), v.get("sourcing"),
             v.get("cost_share"), v.get("value_share")] for v in vc]
    if mode == "example" and not rows:
        rows = [["A1", "[Battery cells and packs]", "Operations", "product", "in-house", 0.35, 0.25],
                ["A2", "[Software and connected services]", "Technology", "custom", "in-house", 0.08, 0.20]]
    hd = ["ID", "Activity", "Porter category", "Stage", "Sourcing", "Cost share", "Value share", "Value − cost", "Reading", "Delivers KSF"]
    a, b = _grid(ws, 5, hd, [r_ + [None, None, _ids(v.get("delivers_ksf")) if i < len(vc) and (v := vc[i]) else None]
                              for i, r_ in enumerate(rows)], 12, [None, None, None, None, None, "0%", "0%", "+0%;-0%;0%"])
    dv_list(ws, ["Inbound logistics", "Operations", "Outbound logistics", "Marketing and sales", "Service",
                 "Procurement", "Technology", "HR", "Firm infrastructure"], f"C{a}:C{b}")
    dv_list(ws, ["commodity", "product", "custom", "genesis"], f"D{a}:D{b}")
    dv_list(ws, ["in-house", "outsourced", "mixed"], f"E{a}:E{b}")
    for rr in range(a, b + 1):
        fx(ws, f"H{rr}", f'=IF(OR(F{rr}="",G{rr}=""),"",G{rr}-F{rr})', "+0%;-0%;0%")
        fx(ws, f"I{rr}", f'=IF(B{rr}="","",IF(H{rr}="","No figures",IF(H{rr}>0.05,"Differentiating engine",'
                         f'IF(H{rr}<-0.05,"Value trap","In balance"))))')
    traffic(ws, f"I{a}:I{b}", f'I{a}="Differentiating engine"', f'I{a}="In balance"', f'I{a}="Value trap"')
    label(ws, f"A{b+1}", "Totals")
    fx(ws, f"F{b+1}", f"=SUM(F{a}:F{b})", "0%", bold=True)
    fx(ws, f"G{b+1}", f"=SUM(G{a}:G{b})", "0%", bold=True)
    fx(ws, f"H{b+1}", f'=IF(AND(ABS(F{b+1}-1)<0.02,ABS(G{b+1}-1)<0.02),"Both sum to 100%","Cost and value shares should each sum to 100%")')


def sheet_unit_econ(wb, L, mode):
    ws = wb.create_sheet("Unit Economics")
    head(ws, "Unit Economics (Exhibit J-1)", "Part 2, step 10. Does one more unit make money, and what does a customer cost? "
         "Matches unit_economics.py.", [34, 16, 16, 34, 16])
    ue = g(L, "company_layer", "internal", "unit_economics", default={}) or {}
    lines = {l.get("line", "").lower(): l.get("value") for l in (ue.get("lines") or [])}
    ex = mode == "example"
    ins = [("Unit", ue.get("unit") or ("one vehicle" if ex else None), None),
           ("Price per unit", lines.get("asp") or lines.get("price") or (32000 if ex else None), "$#,##0"),
           ("Variable cost per unit", lines.get("variable_cost") or (20000 if ex else None), "$#,##0"),
           ("Fixed costs per period", lines.get("fixed_costs") or (180000000 if ex else None), "$#,##0"),
           ("Volume per period", lines.get("volume") or (32400 if ex else None), "#,##0"),
           ("Customer acquisition cost (CAC)", lines.get("cac") or (1500 if ex else None), "$#,##0"),
           ("Units per customer per year", lines.get("units_per_customer_year") or (0.2 if ex else None), "0.00"),
           ("Retention (share kept each year)", lines.get("retention") or (0.6 if ex else None), "0%"),
           ("Discount rate", lines.get("discount_rate") or (0.10 if ex else None), "0.0%"),
           ("Service margin per customer per year", lines.get("service_margin_year") or (300 if ex else None), "$#,##0")]
    label(ws, "A5", "Inputs")
    for i, (k, v, f_) in enumerate(ins):
        label(ws, f"A{6+i}", k, bold=False)
        inp(ws, f"B{6+i}", v, f_)
    P, V, Fx, Q, CAC, U, RET, DR, SM = "B7", "B8", "B9", "B10", "B11", "B12", "B13", "B14", "B15"
    label(ws, "D5", "Results")
    res = [("Contribution per unit", f'=IF(OR({P}="",{V}=""),"",{P}-{V})', "$#,##0"),
           ("Contribution margin", f'=IFERROR(E6/{P},"")', "0.0%"),
           ("Break-even volume", f'=IFERROR(IF(E6>0,{Fx}/E6,"never"),"")', "#,##0"),
           ("Margin of safety", f'=IFERROR(({Q}-E8)/{Q},"")', "0.0%"),
           ("Operating profit", f'=IFERROR(E6*{Q}-{Fx},"")', "$#,##0"),
           ("Annual contribution per customer", f'=IFERROR(E6*{U}+N({SM}),"")', "$#,##0"),
           ("Customer lifetime (years, max 10)", f'=IFERROR(IF({RET}>=1,10,MIN(10,1/(1-{RET}))),"")', "0.0"),
           ("Lifetime value (LTV)", "LTV", "$#,##0"),
           ("LTV / CAC", f'=IFERROR(E13/{CAC},"")', "0.0"),
           ("CAC payback (months)", f'=IFERROR({CAC}/(E11/12),"")', "0.0")]
    # helper years for LTV
    for yv in range(10):
        ws[f"H{6+yv}"] = yv
        ws[f"H{6+yv}"].font = Font(name=F, size=8, color="BBBBBB")
        fx(ws, f"I{6+yv}", f'=IFERROR(IF($E$12-H{6+yv}<=0,0,$E$11*MIN(1,$E$12-H{6+yv})/(1+{DR})^H{6+yv}),0)', "#,##0")
        ws[f"I{6+yv}"].font = Font(name=F, size=8, color="BBBBBB")
    ws.column_dimensions["H"].hidden = True
    ws.column_dimensions["I"].hidden = True
    for i, (k, f_, nf) in enumerate(res):
        label(ws, f"D{6+i}", k, bold=k in ("Contribution per unit", "Break-even volume", "LTV / CAC"))
        fx(ws, f"E{6+i}", '=IF(E11="","",SUM(I6:I15))' if f_ == "LTV" else f_, nf, bold=k in ("Break-even volume", "LTV / CAC"))
    traffic(ws, "E14", "AND(ISNUMBER(E14),E14>=3)", "AND(ISNUMBER(E14),E14>=1)", "AND(ISNUMBER(E14),E14<1)")
    r = 18
    label(ws, f"A{r}", "Sensitivity: operating profit when one input moves")
    header(ws, r + 1, ["Input", "−10%", "Plan", "+10%"])
    ws.freeze_panes = None
    for i, (k, expr) in enumerate([("Price", "(({P}*(1+x))-{V})*{Q}-{Fx}"), ("Variable cost", "({P}-{V}*(1+x))*{Q}-{Fx}"),
                                    ("Volume", "({P}-{V})*{Q}*(1+x)-{Fx}"), ("Fixed costs", "({P}-{V})*{Q}-{Fx}*(1+x)")]):
        rr = r + 2 + i
        label(ws, f"A{rr}", k, bold=False)
        for col, x in zip("BCD", ("-0.1", "0", "0.1")):
            fx(ws, f"{col}{rr}", "=IFERROR(" + expr.format(P=P, V=V, Q=Q, Fx=Fx).replace("x", x) + ',"")', "$#,##0;($#,##0)")


def sheet_rc(wb, L, mode):
    ws = wb.create_sheet("Resources & Capabilities")
    head(ws, "Resources and Capabilities", "Part 2, step 11. What the firm owns, what it does well, and which capabilities "
         "might be core competencies (VRIO tests them next).", [8, 32, 16, 30, 16, 16, 14])
    I_ = g(L, "company_layer", "internal", default={}) or {}
    ex = mode == "example"
    res = [[x.get("id"), x.get("name"), x.get("type"), x.get("measure")] for x in (I_.get("resources") or [])]
    if ex and not res:
        res = [["R1", "[In-house cell plants]", "tangible", "[GWh of capacity]"], ["R2", "[Brand in home market]", "intangible", "[NPS / share]"]]
    r = _sec(ws, 5, "Resources")
    a, b = _grid(ws, r, ["ID", "Resource", "Type", "Measure or evidence"], res, 8)
    dv_list(ws, ["tangible", "intangible", "human", "organisational"], f"C{a}:C{b}")
    cap = [[x.get("id"), x.get("name"), _ids(x.get("combines")), x.get("performance"), _ids(x.get("from_activity")), x.get("class")]
           for x in (I_.get("capabilities") or [])]
    if ex and not cap:
        cap = [["C1", "[Vertical battery integration]", "R1", "[cost per kWh below peers]", "A1", "distinctive"]]
    r = _sec(ws, b + 2, "Capabilities")
    a2, b2 = _grid(ws, r, ["ID", "Capability", "Combines (resources)", "Performance evidence", "From activity", "Class"], cap, 8)
    dv_list(ws, ["threshold", "distinctive"], f"F{a2}:F{b2}")
    cc = [[x.get("capability"), x.get("customer_benefit"), x.get("hard_to_imitate"), x.get("extendable"), x.get("status")]
          for x in (I_.get("core_competencies") or [])]
    r = _sec(ws, b2 + 2, "Core competencies (Prahalad and Hamel: customer benefit, hard to imitate, extendable)")
    a3, b3 = _grid(ws, r, ["Capability", "Customer benefit (KSF)", "Hard to imitate because", "Extends to", "Status"], cc, 5)
    dv_list(ws, ["candidate", "confirmed", "removed"], f"E{a3}:E{b3}")
    label(ws, f"A{b3+2}", "Counts")
    fx(ws, f"B{b3+2}", f'=COUNTA(B{a}:B{b})&" resources · "&COUNTA(B{a2}:B{b2})&" capabilities ("&COUNTIF(F{a2}:F{b2},"distinctive")&" distinctive) · "&COUNTIF(E{a3}:E{b3},"confirmed")&" confirmed core competencies"')
    ws.merge_cells(f"B{b3+2}:G{b3+2}")


def sheet_full_potential(wb, L, mode):
    from openpyxl.chart import BarChart, Reference
    ws = wb.create_sheet("Full Potential")
    head(ws, "Full Potential (Exhibit K-1)", "Part 2, step 14. The profit gap to a benchmark, driver by driver, applied in "
         "sequence so overlaps count once. A ceiling, not a forecast. Matches full_potential.py.",
         [22, 14, 14, 26, 18, 16, 16])
    fp = {d.get("driver"): d for d in ((g(L, "company_layer", "internal", "full_potential", default={}) or {}).get("drivers") or [])}
    ex = {"price": (30000, 32000), "mix_premium": (0, 800), "volume": (300000, 360000), "variable_cost": (24000, 22500),
          "fixed_cost": (1.8e9, 1.7e9)} if mode == "example" else {}
    order = [("price", "Price per unit"), ("mix_premium", "Mix premium per unit"), ("volume", "Volume"),
             ("variable_cost", "Variable cost per unit"), ("fixed_cost", "Fixed costs")]
    header(ws, 5, ["Driver", "Today", "Benchmark", "Benchmark source", "Controllability", "Value after step", "Gap captured"])
    ws.freeze_panes = None
    for i, (k, lab) in enumerate(order):
        r = 6 + i
        d = fp.get(k, {})
        label(ws, f"A{r}", lab, bold=False)
        inp(ws, f"B{r}", d.get("today", (ex.get(k) or (None, None))[0]), "#,##0")
        inp(ws, f"C{r}", d.get("benchmark", (ex.get(k) or (None, None))[1]), "#,##0")
        inp(ws, f"D{r}", d.get("benchmark_source") or ("peer median" if ex else None))
        inp(ws, f"E{r}", d.get("controllability") or ("controllable" if ex else None))
        lower = k in ("variable_cost", "fixed_cost")
        fx(ws, f"F{r}", f'=IF(B{r}="","",IF(C{r}="",B{r},{"MIN" if lower else "MAX"}(B{r},C{r})))', "#,##0")
    dv_list(ws, ["controllable", "capability-bound", "structural"], "E6:E10")
    prof = lambda p, m, v, c, f: f"(({p}+N({m})-{c})*{v}-{f})"
    T = ["B6", "B7", "B8", "B9", "B10"]
    A = ["F6", "F7", "F8", "F9", "F10"]
    states = []
    for i in range(6):
        cur = [A[j] if j < i else T[j] for j in range(5)]
        states.append(prof(*cur))
    for i in range(5):
        fx(ws, f"G{6+i}", f'=IFERROR({states[i+1]}-{states[i]},"")', "#,##0;(#,##0)", bold=True)
    label(ws, "A12", "Operating profit today")
    fx(ws, "B12", f'=IFERROR({states[0]},"")', "#,##0;(#,##0)", bold=True)
    label(ws, "A13", "Full-potential operating profit")
    fx(ws, "B13", f'=IFERROR({states[5]},"")', "#,##0;(#,##0)", bold=True)
    label(ws, "A14", "Uplift")
    fx(ws, "B14", '=IFERROR(B13-B12,"")', "#,##0;(#,##0)", bold=True)
    fx(ws, "C14", '=IFERROR(B14/ABS(B12),"")', "0%")
    label(ws, "A15", "Largest gap")
    fx(ws, "B15", '=IFERROR(INDEX(A6:A10,MATCH(MAX(G6:G10),G6:G10,0)),"")', bold=True)
    ch = BarChart()
    ch.type, ch.title, ch.height, ch.width = "col", "Profit gap captured by driver", 7, 13
    ch.add_data(Reference(ws, min_col=7, min_row=5, max_row=10), titles_from_data=True)
    ch.set_categories(Reference(ws, min_col=1, min_row=6, max_row=10))
    ch.legend = None
    ch.series[0].graphicalProperties.solidFill = NAVY
    ch.y_axis.majorGridlines = None
    ch.x_axis.delete = ch.y_axis.delete = False
    ws.add_chart(ch, "A18")


def sheet_growth_barriers(wb, L, mode):
    ws = wb.create_sheet("Growth Barriers")
    head(ws, "Growth Barriers (Exhibit K-2)", "Part 2, step 15. Which constraint binds growth now? Exactly one should be "
         "binding; lifting it is what unlocks the next stage.", [26, 14, 44, 40])
    gb = g(L, "company_layer", "internal", "growth_barriers", default={}) or {}
    given = {b_.get("barrier"): b_ for b_ in (gb.get("barriers") or [])}
    kinds = [("demand", "Demand: enough customers want it"), ("supply", "Supply / capacity"), ("capability", "Capability / talent"),
             ("capital", "Capital / funding"), ("access", "Distribution / market access"), ("regulation", "Regulation / licences")]
    header(ws, 5, ["Barrier", "Status", "Evidence", "What lifting it unlocks"])
    ws.freeze_panes = None
    for i, (k, lab) in enumerate(kinds):
        r = 6 + i
        d = given.get(k, {})
        label(ws, f"A{r}", lab, bold=False)
        st = d.get("status") or (k == gb.get("binding") and "binding") or None
        if mode == "example" and not st:
            st = {"access": "binding", "capital": "tight"}.get(k, "slack")
        inp(ws, f"B{r}", st)
        inp(ws, f"C{r}", d.get("evidence") if isinstance(d.get("evidence"), str) else None)
        inp(ws, f"D{r}", gb.get("unlocked") if k == gb.get("binding") else None)
        ws.row_dimensions[r].height = 30
    dv_list(ws, ["binding", "tight", "slack"], "B6:B11")
    traffic(ws, "B6:B11", 'B6="slack"', 'B6="tight"', 'B6="binding"')
    label(ws, "A13", "Binding constraint")
    fx(ws, "B13", '=IF(COUNTIF(B6:B11,"binding")=1,INDEX(A6:A11,MATCH("binding",B6:B11,0)),IF(COUNTIF(B6:B11,"binding")=0,"None marked","More than one: choose the one that binds first"))', bold=True)
    ws.merge_cells("B13:D13")


def sheet_positioning(wb, L, mode):
    ws = wb.create_sheet("Positioning")
    head(ws, "Positioning (Strategy Interview)", "Part 3, step 17. The strategy you chose, in your words, and the four fit "
         "tests. The workbook records; it never chooses.", [26, 60, 18, 40])
    p = g(L, "strategy_layer", "positioning", default={}) or {}
    ex = mode == "example"
    rows = [("Generic strategy", p.get("strategy") or ("[your choice]" if ex else None)),
            ("Target customers", p.get("target")), ("Source of advantage", p.get("advantage")),
            ("Why now", p.get("why_now")), ("What we will not do", p.get("not_doing")),
            ("Positioning statement (your words)", p.get("statement"))]
    for i, (k, v) in enumerate(rows):
        r = 5 + i
        label(ws, f"A{r}", k, bold=False)
        inp(ws, f"B{r}", v)
        ws.merge_cells(f"B{r}:D{r}")
        ws.row_dimensions[r].height = 30 if i < 5 else 48
    dv_list(ws, ["Low-cost provider", "Broad differentiation", "Best-cost provider", "Focused low-cost",
                 "Focused differentiation", "[your choice]"], "B5")
    header(ws, 12, ["Fit test", "Question", "Verdict", "Evidence"])
    ws.freeze_panes = None
    fit = p.get("fit") or {}
    tests = [("market", "Market fit", "Is there demand where you are aiming (maps, segments, trends)?"),
             ("competitive", "Competitive fit", "Can you hold the position against the rivals near it?"),
             ("capability", "Capability fit", "Do VRIO and the capability stamps support it?"),
             ("economic", "Economic fit", "Do unit economics and the business case work?"),
             ("management", "Management fit", "Does it fit the goals and limits from your management interview?")]
    for i, (k, lab, q) in enumerate(tests):
        r = 13 + i
        label(ws, f"A{r}", lab, bold=False)
        label(ws, f"B{r}", q, bold=False)
        inp(ws, f"C{r}", fit.get(k))
        inp(ws, f"D{r}", None)
    dv_list(ws, ["supported", "open question", "conflicts"], "C13:C17")
    traffic(ws, "C13:C17", 'C13="supported"', 'C13="open question"', 'C13="conflicts"')
    label(ws, "A19", "Fit summary")
    fx(ws, "B19", '=COUNTIF(C13:C17,"supported")&" supported · "&COUNTIF(C13:C17,"open question")&" open · "&COUNTIF(C13:C17,"conflicts")&" conflicts"', bold=True)


def sheet_options(wb, L, mode):
    ws = wb.create_sheet("Strategic Options")
    head(ws, "Strategic Options (Exhibit P)", "Part 3, step 18. Frame the decision, then three or more distinct options plus "
         "do nothing, each with a staged first step and a gate.", [8, 30, 14, 18, 36, 36, 12])
    o = g(L, "strategy_layer", "options", default={}) or {}
    scq = o.get("scq") or {}
    ex = mode == "example"
    for i, (k, lab) in enumerate((("situation", "Situation"), ("complication", "Complication"), ("question", "Question"))):
        label(ws, f"A{5+i}", lab, bold=False)
        inp(ws, f"B{5+i}", scq.get(k))
        ws.merge_cells(f"B{5+i}:G{5+i}")
    rows = [[x.get("id"), x.get("name"), x.get("route"), _ids(x.get("exploits")), x.get("staged_step"), x.get("gate"),
             "Yes" if x.get("suggested") else "No"] for x in (o.get("options") or [])]
    if ex and not rows:
        rows = [["O-A", "[Build an EU plant]", "build", "ST1", "[pilot line first]", "[orders > X by Q4]", "No"],
                ["O-0", "Do nothing", "do nothing", "", "", "", "No"]]
    a, b = _grid(ws, 9, ["ID", "Option", "Route", "Exploits (TOWS ids)", "Staged first step", "Gate to the next stage", "Suggested?"], rows, 8, heights=30)
    dv_list(ws, ["build", "buy", "partner", "license", "focus", "exit", "do nothing"], f"C{a}:C{b}")
    dv_list(ws, ["Yes", "No"], f"G{a}:G{b}")
    label(ws, f"A{b+2}", "Checks")
    fx(ws, f"B{b+2}", f'=IF(COUNTIF(C{a}:C{b},"do nothing")=0,"Add do nothing as the baseline",IF(COUNTA(B{a}:B{b})-1<3,"Add options: aim for three or more plus do nothing","OK"))', bold=True)
    ws.merge_cells(f"B{b+2}:G{b+2}")


def sheet_pricing(wb, L, mode):
    ws = wb.create_sheet("Pricing")
    head(ws, "Pricing (optional)", "Part 3. Only when price is a lever. Test price points against the volume you expect at "
         "each; the sheet finds the profit-maximising point inside the acceptable range.", [18, 16, 16, 16, 18, 14])
    ex = mode == "example"
    label(ws, "A5", "Variable cost per unit", bold=False)
    inp(ws, "B5", 20000 if ex else None, "$#,##0")
    label(ws, "A6", "Fixed costs", bold=False)
    inp(ws, "B6", 180000000 if ex else None, "$#,##0")
    label(ws, "A7", "Acceptable range: low", bold=False)
    inp(ws, "B7", 28000 if ex else None, "$#,##0")
    label(ws, "A8", "Acceptable range: high", bold=False)
    inp(ws, "B8", 36000 if ex else None, "$#,##0")
    data = [[28000, 42000], [30000, 39000], [32000, 36000], [34000, 31000], [36000, 26000]] if ex else []
    header(ws, 10, ["Price point", "Expected volume", "Revenue", "Contribution", "Operating profit", "In range?"])
    ws.freeze_panes = None
    for i in range(8):
        r = 11 + i
        d = data[i] if i < len(data) else [None, None]
        inp(ws, f"A{r}", d[0], "$#,##0")
        inp(ws, f"B{r}", d[1], "#,##0")
        fx(ws, f"C{r}", f'=IF(OR(A{r}="",B{r}=""),"",A{r}*B{r})', "$#,##0")
        fx(ws, f"D{r}", f'=IF(C{r}="","",(A{r}-$B$5)*B{r})', "$#,##0")
        fx(ws, f"E{r}", f'=IF(D{r}="","",D{r}-$B$6)', "$#,##0;($#,##0)")
        fx(ws, f"F{r}", f'=IF(A{r}="","",IF(AND(A{r}>=$B$7,A{r}<=$B$8),"Yes","No"))')
    label(ws, "A20", "Best price in range")
    fx(ws, "B20", '=IFERROR(INDEX(A11:A18,MATCH(_xlfn.MAXIFS(E11:E18,F11:F18,"Yes"),E11:E18,0)),"")', "$#,##0", bold=True)
    label(ws, "C20", "Profit there", bold=False)
    fx(ws, "D20", '=IFERROR(_xlfn.MAXIFS(E11:E18,F11:F18,"Yes"),"")', "$#,##0;($#,##0)", bold=True)


def sheet_stress(wb, L, mode):
    ws = wb.create_sheet("Stress Test")
    head(ws, "Stress Test (Exhibit R)", "Part 3, step 22. Attack the leading option before anyone plans: the assumptions it "
         "rests on, how rivals respond, and a risk register with owners and triggers.", [30, 16, 16, 12, 12, 10, 12, 18, 30, 30])
    st = g(L, "strategy_layer", "stress_test", default={}) or {}
    ex = mode == "example"
    asm = [[x.get("assumption"), x.get("value"), x.get("break_even"), x.get("evidence"), x.get("danger")] for x in (st.get("assumptions") or []) if isinstance(x, dict)]
    if ex and not asm:
        asm = [["[Units in year 3]", 97200, 92000, "[source]", None]]
    r = _sec(ws, 5, "Assumption audit")
    header(ws, r, ["Assumption", "Value used", "Break-even value", "Evidence", "Headroom", "Danger zone?"])
    ws.freeze_panes = None
    for i in range(8):
        rr = r + 1 + i
        d = asm[i] if i < len(asm) else [None] * 5
        inp(ws, f"A{rr}", d[0]); inp(ws, f"B{rr}", d[1], "#,##0.##"); inp(ws, f"C{rr}", d[2], "#,##0.##"); inp(ws, f"D{rr}", d[3])
        fx(ws, f"E{rr}", f'=IF(OR(B{rr}="",C{rr}="",B{rr}=0),"",ABS(B{rr}-C{rr})/ABS(B{rr}))', "0%")
        fx(ws, f"F{rr}", f'=IF(E{rr}="","",IF(E{rr}<0.1,"Yes","No"))', bold=True)
    traffic(ws, f"F{r+1}:F{r+8}", f'F{r+1}="No"', "FALSE", f'F{r+1}="Yes"')
    r = r + 10
    r = _sec(ws, r, "Competitor war-game")
    wg = [[x.get("rival"), x.get("response"), x.get("effect"), x.get("counter")] for x in (st.get("war_game") or []) if isinstance(x, dict)]
    a, b = _grid(ws, r, ["Rival", "Most likely response", "Effect on us", "Our counter"], wg, 5, heights=30)
    r = b + 2
    r = _sec(ws, r, "Risk register")
    rk = [[x.get("risk"), x.get("likelihood"), x.get("impact"), None, None, x.get("owner"), x.get("mitigation"), x.get("trigger")]
          for x in (st.get("risks") or []) if isinstance(x, dict)]
    if ex and not rk:
        rk = [["[Price war in the target segment]", 4, 4, None, None, "[CMO]", "[hold price; add value]", "[rival cuts > 5%]"]]
    header(ws, r, ["Risk", "Likelihood (1-5)", "Impact (1-5)", "Score", "Rating", "Owner", "Mitigation", "Early-warning trigger"])
    ws.freeze_panes = None
    for i in range(10):
        rr = r + 1 + i
        d = rk[i] if i < len(rk) else [None] * 8
        inp(ws, f"A{rr}", d[0]); inp(ws, f"B{rr}", d[1], "0"); inp(ws, f"C{rr}", d[2], "0")
        fx(ws, f"D{rr}", f'=IF(OR(B{rr}="",C{rr}=""),"",B{rr}*C{rr})', "0")
        fx(ws, f"E{rr}", f'=IF(D{rr}="","",IF(D{rr}>=15,"High",IF(D{rr}>=8,"Medium","Low")))', bold=True)
        for col, v in zip("FGH", d[5:]):
            inp(ws, f"{col}{rr}", v)
    dv_whole(ws, 1, 5, f"B{r+1}:C{r+10}")
    traffic(ws, f"E{r+1}:E{r+10}", f'E{r+1}="Low"', f'E{r+1}="Medium"', f'E{r+1}="High"')
    label(ws, f"A{r+12}", "High risks without an owner")
    fx(ws, f"B{r+12}", f'=COUNTIFS(E{r+1}:E{r+10},"High",F{r+1}:F{r+10},"")', "0", bold=True)


def sheet_gtm(wb, L, mode):
    ws = wb.create_sheet("Go-to-Market")
    head(ws, "Go-to-Market (Exhibit T)", "Part 3, step 23. One named beachhead, the funnel worked back to spend and CAC, and "
         "launch gates. CAC must fit the unit economics.", [24, 14, 14, 12, 12, 14, 14, 14, 16])
    gm = g(L, "strategy_layer", "gtm", default={}) or {}
    ex = mode == "example"
    for i, (k, lab) in enumerate((("beachhead", "Beachhead segment"), ("icp", "Ideal customer profile"), ("value_prop", "Value proposition"))):
        label(ws, f"A{5+i}", lab, bold=False)
        inp(ws, f"B{5+i}", gm.get(k))
        ws.merge_cells(f"B{5+i}:I{5+i}")
    ch = [[c.get("channel"), c.get("spend"), c.get("reach"), c.get("lead_rate"), c.get("close_rate")] for c in (gm.get("channels") or []) if isinstance(c, dict)]
    if ex and not ch:
        ch = [["[Dealer partners]", 2000000, 400000, 0.02, 0.10], ["[Online direct]", 1500000, 900000, 0.01, 0.05]]
    header(ws, 9, ["Channel", "Spend", "Reach", "Lead rate", "Close rate", "Leads", "Customers", "CAC", "CAC vs LTV"])
    ws.freeze_panes = None
    for i in range(8):
        r = 10 + i
        d = ch[i] if i < len(ch) else [None] * 5
        inp(ws, f"A{r}", d[0]); inp(ws, f"B{r}", d[1], "$#,##0"); inp(ws, f"C{r}", d[2], "#,##0")
        inp(ws, f"D{r}", d[3], "0.0%"); inp(ws, f"E{r}", d[4], "0.0%")
        fx(ws, f"F{r}", f'=IF(OR(C{r}="",D{r}=""),"",C{r}*D{r})', "#,##0")
        fx(ws, f"G{r}", f'=IF(OR(F{r}="",E{r}=""),"",F{r}*E{r})', "#,##0")
        fx(ws, f"H{r}", f'=IFERROR(IF(G{r}>0,B{r}/G{r},""),"")', "$#,##0")
        fx(ws, f"I{r}", f"=IFERROR(IF(H{r}=\"\",\"\",IF('Unit Economics'!$E$13=\"\",\"set LTV on Unit Economics\",IF(H{r}<='Unit Economics'!$E$13/3,\"Fits (LTV/CAC ≥ 3)\",IF(H{r}<='Unit Economics'!$E$13,\"Thin\",\"Burns value\")))),\"\")")
    traffic(ws, "I10:I17", 'LEFT(I10,4)="Fits"', 'I10="Thin"', 'I10="Burns value"')
    label(ws, "A18", "Blended")
    fx(ws, "B18", "=SUM(B10:B17)", "$#,##0", bold=True)
    fx(ws, "G18", "=SUM(G10:G17)", "#,##0", bold=True)
    fx(ws, "H18", '=IFERROR(B18/G18,"")', "$#,##0", bold=True)
    ph = [[p.get("phase"), p.get("when"), p.get("goal"), p.get("gate")] for p in (gm.get("phases") or []) if isinstance(p, dict)]
    r = _sec(ws, 20, "Launch phases and gates")
    _grid(ws, r, ["Phase", "When", "Goal", "Gate to the next phase"], ph, 4)


def sheet_initiatives(wb, L, mode):
    ws = wb.create_sheet("Initiatives")
    head(ws, "Initiative Prioritizer (Exhibit S)", "Part 3, step 24. RICE score = reach × impact × confidence ÷ effort. "
         "The binding constraint goes first; every initiative traces to a finding.", [8, 34, 16, 12, 12, 13, 12, 12, 8, 14, 12])
    ini = g(L, "strategy_layer", "initiatives", default=[]) or []
    rows = [[x.get("id"), x.get("initiative"), x.get("traces_to"), x.get("reach"), x.get("impact"), x.get("confidence"),
             x.get("effort")] for x in ini]
    if mode == "example" and not rows:
        rows = [["I1", "[Secure dealer partners in Germany]", "GB:access", 5000, 2, 0.8, 4],
                ["I2", "[Cut cell cost 8%]", "K1", 20000, 1, 0.5, 6]]
    hd = ["ID", "Initiative", "Traces to", "Reach", "Impact (0.25-3)", "Confidence", "Effort (person-months)", "RICE", "Rank", "Depends on", "Status"]
    a, b = _grid(ws, 5, hd, [r_ + [None, None, None, None] for r_ in rows], 12, [None, None, None, "#,##0", "0.00", "0%", "0.0"])
    for rr in range(a, b + 1):
        fx(ws, f"H{rr}", f'=IF(OR(D{rr}="",E{rr}="",F{rr}="",G{rr}="",G{rr}=0),"",D{rr}*E{rr}*F{rr}/G{rr})', "#,##0", bold=True)
        fx(ws, f"I{rr}", f'=IF(H{rr}="","",RANK(H{rr},$H${a}:$H${b}))', "0")
        inp(ws, f"J{rr}", None)
        inp(ws, f"K{rr}", None)
    dv_list(ws, ["now", "next", "later", "dropped"], f"K{a}:K{b}")
    label(ws, f"A{b+2}", "Initiatives with nothing to trace to")
    fx(ws, f"C{b+2}", f'=COUNTIFS(B{a}:B{b},"<>",C{a}:C{b},"")', "0", bold=True)


def sheet_operating(wb, L, mode):
    from openpyxl.chart import ScatterChart, Reference, Series
    ws = wb.create_sheet("Operating Model")
    head(ws, "Operating Model and Stakeholders", "Part 3, steps 25-26. Who decides what (RAPID), and who must say yes: power "
         "and interest place each stakeholder in a quadrant.", [26, 16, 16, 16, 16, 16, 12, 12, 12, 20, 30])
    om = g(L, "strategy_layer", "operating_model", default={}) or {}
    rap = [[x.get("decision"), x.get("recommend"), x.get("agree"), x.get("perform"), x.get("input"), x.get("decide")]
           for x in (om.get("decision_rights") or []) if isinstance(x, dict)]
    if mode == "example" and not rap:
        rap = [["[Enter Germany]", "[Strategy lead]", "[CFO]", "[EU GM]", "[Sales, Legal]", "[CEO]"]]
    r = _sec(ws, 5, "Decision rights (RAPID)")
    a, b = _grid(ws, r, ["Decision", "Recommend", "Agree", "Perform", "Input", "Decide"], rap, 6)
    sh = g(L, "strategy_layer", "stakeholders", default={}) or {}
    st = [[x.get("name"), None, None, None, None, None, x.get("power"), x.get("interest"), x.get("stance"), None, x.get("action")]
          for x in (sh.get("list") or sh.get("stakeholders") or []) if isinstance(x, dict)]
    if mode == "example" and not st:
        st = [["[EU regulators]", None, None, None, None, None, 5, 3, -1, None, "[early dialogue]"],
              ["[Dealer groups]", None, None, None, None, None, 3, 5, 1, None, "[co-design terms]"]]
    r = _sec(ws, b + 2, "Stakeholder map")
    header(ws, r, ["Stakeholder", "", "", "", "", "", "Power (1-5)", "Interest (1-5)", "Stance (−2..+2)", "Quadrant", "Action"])
    ws.merge_cells(f"A{r}:F{r}")
    ws.freeze_panes = None
    s0 = r + 1
    for i in range(10):
        rr = s0 + i
        d = st[i] if i < len(st) else [None] * 11
        inp(ws, f"A{rr}", d[0])
        ws.merge_cells(f"A{rr}:F{rr}")
        inp(ws, f"G{rr}", d[6], "0"); inp(ws, f"H{rr}", d[7], "0"); inp(ws, f"I{rr}", d[8], "+0;-0;0")
        fx(ws, f"J{rr}", f'=IF(OR(G{rr}="",H{rr}=""),"",IF(G{rr}>=3,IF(H{rr}>=3,"Manage closely","Keep satisfied"),IF(H{rr}>=3,"Keep informed","Monitor")))', bold=True)
        inp(ws, f"K{rr}", d[10])
    dv_whole(ws, 1, 5, f"G{s0}:H{s0+9}")
    dv_whole(ws, -2, 2, f"I{s0}:I{s0+9}")
    ch = ScatterChart()
    ch.title, ch.height, ch.width = "Power and interest", 8, 12
    ch.scatterStyle = "marker"
    ch.x_axis.title, ch.y_axis.title = "Interest", "Power"
    ch.x_axis.scaling.min = ch.y_axis.scaling.min = 0
    ch.x_axis.scaling.max = ch.y_axis.scaling.max = 5.5
    s = Series(Reference(ws, min_col=7, min_row=s0, max_row=s0 + 9), Reference(ws, min_col=8, min_row=s0, max_row=s0 + 9),
               title="Stakeholders")
    s.marker.symbol, s.marker.size = "circle", 10
    s.marker.graphicalProperties.solidFill = NAVY
    s.marker.graphicalProperties.line.noFill = True
    s.graphicalProperties.line.noFill = True
    ch.series.append(s)
    ch.legend = None
    ch.x_axis.delete = ch.y_axis.delete = False
    ws.add_chart(ch, f"A{s0 + 12}")


def sheet_roadmap(wb, L, mode):
    ws = wb.create_sheet("Execution Roadmap")
    head(ws, "Execution Roadmap (Exhibit S)", "Part 3, step 27. The first 100 days by workstream (the bars fill in from the "
         "start and end weeks), milestones and stage gates.", [30, 16, 8, 8] + [3.2] * 15 + [4])
    rm = g(L, "strategy_layer", "roadmap", default={}) or {}
    ws_ = [[x.get("action") or x.get("workstream"), x.get("owner"), x.get("start_week"), x.get("end_week")]
           for x in (rm.get("first_100_days") or []) if isinstance(x, dict)]
    if mode == "example" and not ws_:
        ws_ = [["[Sign two dealer groups]", "[EU GM]", 1, 8], ["[Pilot line ready]", "[COO]", 4, 14]]
    header(ws, 5, ["Workstream / action", "Owner", "Start wk", "End wk"] + [str(w) for w in range(1, 16)])
    ws.freeze_panes = None
    for i in range(12):
        r = 6 + i
        d = ws_[i] if i < len(ws_) else [None] * 4
        inp(ws, f"A{r}", d[0]); inp(ws, f"B{r}", d[1]); inp(ws, f"C{r}", d[2], "0"); inp(ws, f"D{r}", d[3], "0")
        for w in range(1, 16):
            col = get_column_letter(4 + w)
            ws[f"{col}{r}"].border = BOX
        rng = f"E{r}:S{r}"
        ws.conditional_formatting.add(rng, FormulaRule(
            formula=[f'AND(ISNUMBER($C{r}),ISNUMBER($D{r}),E$5*1>=$C{r},E$5*1<=$D{r})'],
            fill=PatternFill("solid", fgColor=GOLD)))
    dv_whole(ws, 1, 15, "C6:D17")
    ms = [[x.get("milestone"), x.get("date"), x.get("kpi"), x.get("target")] for x in (rm.get("milestones") or []) if isinstance(x, dict)]
    r = _sec(ws, 20, "Milestones")
    a, b = _grid(ws, r, ["Milestone", "Date", "KPI", "Target"], ms, 6)
    gt = [[x.get("gate"), x.get("criteria"), x.get("evidence"), x.get("decision_date")] for x in (rm.get("gates") or []) if isinstance(x, dict)]
    r = _sec(ws, b + 2, "Stage gates (go / no-go)")
    _grid(ws, r, ["Gate", "Criteria to pass", "Evidence we will use", "Decision date"], gt, 4)


def main():
    a = sys.argv
    ledger = a[a.index("--ledger") + 1] if "--ledger" in a else None
    out = a[a.index("--out") + 1] if "--out" in a else "StratOS_Workbook.xlsx"
    mode = "ledger" if ledger else ("blank" if "--blank" in a else "example")
    L = json.load(open(ledger, encoding="utf-8")) if ledger else {}
    caps, reports = [], []
    for i, x in enumerate(a):
        if x == "--capture":
            caps.append(json.load(open(a[i + 1], encoding="utf-8")))
        if x == "--report":
            reports.append(json.load(open(a[i + 1], encoding="utf-8")))
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
        sheet_mgmt(wb, L, mode)
        # Part 1
        sheet_overview(wb, L, mode)
        sheet_competitive(wb, L, mode)
        sheet_pestel(wb, L, mode)
        sheet_forces(wb, L, mode)
        sheet_drivers(wb, L, mode)
        sheet_ksf(wb, L, mode)
        sheet_mapping(wb, L, mode)
        # Part 2
        sheet_value_chain(wb, L, mode)
        sheet_unit_econ(wb, L, mode)
        sheet_rc(wb, L, mode)
        sheet_vrio(wb, L, mode)
        sheet_full_potential(wb, L, mode)
        sheet_growth_barriers(wb, L, mode)
        sheet_swot(wb, L, mode)
        # Part 3
        sheet_positioning(wb, L, mode)
        sheet_options(wb, L, mode)
        sheet_matrix(wb, L, mode)
        sheet_bc(wb, L, mode)
        sheet_ev(wb, L, mode)
        sheet_risk(wb, L, mode)
        sheet_pricing(wb, L, mode)
        sheet_stress(wb, L, mode)
        sheet_gtm(wb, L, mode)
        sheet_initiatives(wb, L, mode)
        sheet_operating(wb, L, mode)
        sheet_roadmap(wb, L, mode)
        sheet_bsc(wb, L, mode)
        sheet_map(wb, L, mode, tmp)
        sheet_cir(wb, L, mode, caps)
        sheet_planner(wb, L, mode, caps, years)
        rspec = _results_spec()
        fspec = expand_fields(json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                                                          "references", "globus-fields.json"), encoding="utf-8")))
        syears = _season_years(caps, y0, mode)
        season = sheet_season(wb, L, mode, caps, fspec, rspec, syears)
        comp = sheet_competition(wb, caps, mode, syears)
        sheet_kpi_charts(wb, season, comp)
        sheet_findings(wb, mode, reports)
        part = {"Start": "C9A55C", "Management Interviews": "C9A55C"}
        p1 = ["Industry Overview", "Competitive Analysis", "PESTEL", "Five Forces", "Trending Factors", "KSF Scorecard", "Strategic Mapping"]
        p2 = ["Value Chain", "Unit Economics", "Resources & Capabilities", "VRIO", "Full Potential", "Growth Barriers", "SWOT-TOWS"]
        for ws in wb.worksheets:
            t = ws.title
            ws.sheet_properties.tabColor = part.get(t) or ("457B9D" if t in p1 else "2D936C" if t in p2 else
                                                         "C44536" if (t.startswith("GLO-BUS") or t in ("Season by Year", "Competition by Year", "KPI Charts", "Findings & Questions"))
                                                         else NAVY)
        wb.save(out)
    print(json.dumps({"out": out, "mode": mode, "sheets": [ws.title for ws in wb.worksheets]}))


if __name__ == "__main__":
    main()
