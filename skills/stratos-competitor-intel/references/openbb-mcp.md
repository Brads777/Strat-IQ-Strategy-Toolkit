# OpenBB MCP: the default data source

Read this in step 2, before you collect any financials.

## Setup (once per environment)

```bash
pip install openbb-mcp-server
openbb-mcp --transport streamable-http --default-categories admin   # default transport; stdio and sse also supported
```

- Put provider API keys in `~/.openbb_platform/user_settings.json` under `credentials`. Some providers need keys, such as `fmp_api_key`, `intrinio_api_key`, or `polygon_api_key`. Never write keys into the skill or into its outputs.
- If the server isn't reachable, say so once and go straight to the fallback chain in SKILL.md step 2. Don't retry in a loop.

## Tool activation

Start with only the discovery tools loaded, then activate what you need:

1. `available_categories`, then `available_tools` with `category=equity` and `subcategory=fundamental`
2. `activate_tools` with `tool_names="equity_fundamental_income,equity_fundamental_balance,equity_fundamental_cash,equity_fundamental_ratios,equity_fundamental_metrics,equity_compare_peers,equity_profile"`
3. If you need them: `equity_estimates_*` (consensus estimates), `news_company` (recent strategic moves), `economy_*` (macro indicators for the PESTEL links in step 5)
4. When you're finished, `deactivate_tools` to keep context small

Tool names depend on which extensions are installed. Confirm them with `available_tools` rather than assuming they exist.

## What each tool is for

| Need | Tool | Notes |
|---|---|---|
| Income statement, balance sheet, cash flow | `equity_fundamental_income` / `_balance` / `_cash` | Request `period=annual` with `limit=4`, then `period=quarter` to build LTM |
| Ratios (margins, ROE, turnover) | `equity_fundamental_ratios` | Recompute ROIC yourself using the formula in `financial-metrics.md` |
| Valuation multiples, market cap, EV | `equity_fundamental_metrics` | |
| Peer set suggestions | `equity_compare_peers` | Use this only to suggest candidates. The industry boundary from step 1 decides who's in |
| Business description, sector, employees | `equity_profile` | Feeds step 4 profiles and revenue per employee |
| Segment data | `equity_fundamental_revenue_per_segment` (if installed) | Otherwise, take segment data from 10-K notes |

## Provider order

1. `fmp` or `intrinio` if you have keys (the most consistent standardized fundamentals)
2. `yfinance` (free; good for public-company snapshots, weaker on history)
3. `sec` (free; the authoritative source for US filings. Use it to spot-check at least one figure per competitor)

Use a single provider for each metric across the whole peer set. If you have to mix providers, add a footnote saying which competitors got which provider, because definitions differ (for example, adjusted vs. reported EBITDA).

## What OpenBB doesn't cover

OpenBB mostly covers public equities. For private competitors and for segments that aren't disclosed, use the finance connector, filings, press, or proxies. Label those figures "est." and give them confidence = Low.
