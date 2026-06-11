# Project 1: Data Cleaning & Preparation

**DecodeLabs Data Analytics Industrial Training | Batch 2026**

## Overview

This project converts a raw 1,200-row e-commerce workbook into an analysis-ready Pandas DataFrame through a fully documented Jupyter Notebook workflow.

The notebook follows the requirements in `DATA ANALYTICS p1.pdf`:

- identify missing or null values;
- remove duplicate records when present;
- correct date, numeric, identifier, and text formats;
- prove there are zero duplicate order IDs;
- prove there are zero incorrectly formatted dates.

All cleaning logic, evidence, outputs, validation checks, and conclusions are contained in `Project1_Data_Cleaning.ipynb`. The workflow does not generate a separate cleaned workbook.

## Dataset

| Attribute | Value |
|---|---:|
| File | `Dataset_for_Data_Analytics.xlsx` |
| Records | 1,200 |
| Columns | 14 |
| Date range | 2023-01-01 to 2025-06-30 |
| Unique order IDs | 1,200 |
| Unique tracking numbers | 1,200 |

The source contains order, customer, product, pricing, fulfillment, payment, coupon, referral, and shipping fields.

## Data Quality Findings

- `CouponCode` contains 309 blank values, or 25.75% of records.
- Coupon blanks are a valid business state and are standardized to `NO_COUPON`.
- All 13 other columns are complete.
- No full-row duplicates are present.
- No duplicate `OrderID` values are present.
- No duplicate `TrackingNumber` values are present.
- All 1,200 dates parse successfully and fall between January 1, 2023 and June 30, 2025.
- All quantities, cart sizes, unit prices, and total prices are positive.
- Every `TotalPrice` matches `Quantity × UnitPrice` within a one-cent tolerance.
- All order, customer, and tracking identifiers match their expected patterns.

No source records are removed because the duplicate checks find no duplicate rows or order IDs.

## Cleaning Workflow

1. Load the source workbook without modifying it.
2. Audit shape, schema, missingness, uniqueness, and sample values.
3. Standardize optional coupon blanks as `NO_COUPON`.
4. Remove exact and `OrderID` duplicates defensively.
5. Parse dates as `datetime64[ns]`.
6. Normalize text whitespace and categorical capitalization.
7. Normalize identifiers to uppercase.
8. enforce numeric types and two-decimal monetary precision.
9. Validate dates, identifiers, positivity, allowed categories, and revenue arithmetic.
10. Run assertions for the DecodeLabs acceptance gate.

## Mandatory Verification

The executed notebook proves:

```text
Duplicate OrderID values after cleaning: 0
Incorrectly formatted dates after cleaning: 0
```

It also verifies that all 1,200 source records are retained.

## Repository Structure

```text
Project_01/
├── DATA ANALYTICS p1.pdf
├── Dataset_for_Data_Analytics.xlsx
├── Project1_Data_Cleaning.ipynb
├── README.md
└── requirements.txt
```

## How to Run

1. Open a terminal in `Project_01`.
2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Start Jupyter:

   ```bash
   jupyter notebook
   ```

4. Open `Project1_Data_Cleaning.ipynb`.
5. Select **Run All**.

The notebook resolves the dataset from either the project directory or the repository root, so no path edits are required.

## Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- OpenPyXL
- Jupyter Notebook

## Portfolio Value

This project demonstrates reproducible data profiling, semantic missing-value treatment, defensive deduplication, type normalization, business-rule validation, audit reporting, and assertion-based quality control. It treats cleaning as an evidence-driven process rather than claiming corrections that the raw dataset did not require.
