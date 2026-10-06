# GLO-BUS capture checklist

Match by meaning: menu labels differ between GLO-BUS versions. `id` is the prefix `capture_check.py`
looks for. "Each product" = cameras and drones; "each region" = North America (NA), Europe-Africa (EA),
Asia-Pacific (AP), Latin America (LA).

## Class-wide reports (every company sees these)

| id | Screen | Split | Required |
|---|---|---|---|
| `scoreboard` | Scoreboard / overall standings and KPI scores (EPS, ROE, stock price, credit rating, image rating) | — | yes |
| `cir` | Competitive Intelligence Report (older: Comparative Competitive Efforts) | each product × each region | yes |
| `cdj` | Camera & Drone Journal: industry summary and benchmarks (cost per unit, marketing cost, margins) | — | yes |
| `highlights` | Performance highlights / investor expectations | — | yes |
| `industry-reports` | Other industry reports (market shares, sales by region, special contract bids) | as shown | if present |

## The team's own company

| id | Screen | Split | Required |
|---|---|---|---|
| `dec-product` | Product design decisions (P/Q, components, models) | each product | yes |
| `dec-marketing` | Marketing and pricing decisions (price, ads, retailer support, promotions, warranty) | each product × each region | yes |
| `dec-operations` | Assembly operations and facilities (workstations, capacity, overtime, training) | each product | yes |
| `dec-compensation` | Workforce compensation (wages, incentives, benefits) | — | yes |
| `dec-csr` | Corporate citizenship / social responsibility | — | yes |
| `dec-finance` | Finance and cash flow (loans, stock issues and buybacks, dividends) | — | yes |
| `projections` | Projected results / KPI projections for the decisions shown | — | yes |
| `company-reports` | Company operating reports: income statement, balance sheet, cash flow, cost reports | as shown | yes |
| `special-contracts` | Special contract bids (later years) | — | if present |

`capture_check.py` treats a page as thin when its text has fewer than 200 characters (often a
chart-only page: keep the screenshot and say so).
