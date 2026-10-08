# Strat-IQ v3 demo kit

Files for screen-recording the nine live demos in the Strat-IQ v3 process video. Start with
**Demo_Run_Sheet.docx** (or `.md` / `.pdf`): setup, the exact prompts, the results you should see, and
what to point at.

Everything here is **illustrative demo data** (BYD as the base company in global EVs; GLO-BUS company C),
labelled as such in each file. It shows what the tools do; it is not research to cite.

Rebuild the demo workbook:

```
python ../part3/skills/stratiq-workbook/scripts/build_workbook.py --ledger strategy-ledger-ev-demo.json \
  --capture globus/globus-capture-C-Y6.json --capture globus/globus-capture-C-Y7.json --out StratIQ_Workbook_demo.xlsx
```
