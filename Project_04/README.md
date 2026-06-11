# Project 4: Data Visualization and Storytelling

**DecodeLabs Industrial Training | Data Analytics Batch 2026**

## Objective

Transform the supplied e-commerce order data into an honest, concise, and
boardroom-ready visual narrative. The project follows the brief's three
principles:

1. Choose the chart based on the business question.
2. Remove visual clutter and preserve axis integrity.
3. Use action titles and finish with a clear recommendation.

## Executive Finding

Revenue momentum is weakening while order outcomes remain the main risk.
Comparable H1 gross order value declined from 2023 through 2025, and cancelled
plus returned orders represent more than two in five records.

> Important: `TotalPrice` is described as **gross order value**, not recognized
> revenue, because the source includes cancelled, returned, pending, and shipped
> orders.

## Files

```text
Project_04/
|-- Data Analytics Project 4.pdf
|-- Dataset for Data Analytics.xlsx
|-- Project4_Data_Visualization.ipynb
|-- data_visualization.py
|-- requirements.txt
|-- README.md
`-- outputs/
    |-- 00_executive_dashboard.png
    |-- 01_h1_gross_order_value.png
    |-- 02_product_performance.png
    |-- 03_order_status_distribution.png
    |-- 04_referral_source_performance.png
    |-- 05_coupon_average_order_value.png
    |-- executive_report.html
    |-- analysis_ready_orders.csv
    |-- key_metrics.csv
    `-- table_*.csv
```

## How to Run

```bash
cd Project_04
pip install -r requirements.txt
python data_visualization.py
```

Open `outputs/executive_report.html` in any browser for the self-contained
executive report. The notebook provides a submission-friendly walkthrough.

## Data Validation

The pipeline checks:

- Required columns are present.
- `OrderID` is unique and key fields are complete.
- Date and numeric fields parse correctly.
- Numeric order values are non-negative.
- `TotalPrice = Quantity x UnitPrice` for every row.
- Missing coupon values are labeled `NO_COUPON`, since no coupon is a valid
  business state.

## Visual Story

| Visual | Business question | Design choice |
|---|---|---|
| Executive dashboard | What must leadership know now? | Four KPIs and three focused charts |
| H1 trend | Is performance improving over comparable periods? | Line chart; avoids partial-year distortion |
| Product performance | Which products drive order value? | Sorted horizontal bars with direct labels |
| Order status | Where is operational exposure concentrated? | Zero-baseline bars; risk categories highlighted |
| Referral source | Which source combines scale and quality? | Gross value bars annotated with issue rates |
| Coupon AOV | Do offers materially change basket value? | Zero-baseline bars and direct currency labels |

Pie charts and 3D effects are intentionally excluded because they would reduce
comparison accuracy without adding information.

## Key Findings

- 1,200 unique orders total **$1,264,761.96** in gross order value.
- Average order value is **$1,053.97**.
- H1 gross order value fell from **$286,501.52 in 2023** to **$231,882.85 in
  2025**, a **19.1% decline**.
- Cancelled and returned orders account for **41.42%** of order volume.
- Chair leads product gross value at **$195,620.11**, but Printer is only
  **$7.50** behind; the portfolio is diversified rather than dependent on one
  item.
- Instagram is the largest referral source at **$275,285.45** and has the
  lowest cancellation/return issue rate at **37.07%**.
- Coupon average order values differ by only **$34.50** from highest to lowest.

## Recommendations

1. Diagnose cancellation and return causes before increasing acquisition spend.
2. Protect and selectively scale Instagram while monitoring completed-order
   quality.
3. Judge coupons on incremental margin and completed-order conversion, not
   gross order value alone.
4. Continue comparable-period reporting; never compare half-year 2025 with a
   complete prior year.

## Tools

- Python
- pandas
- matplotlib
- openpyxl
- Jupyter Notebook

