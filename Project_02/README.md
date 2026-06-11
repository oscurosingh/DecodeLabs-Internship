# Project 2: Exploratory Data Analysis

## Overview

This portfolio project presents an end-to-end exploratory analysis of 1,200 e-commerce orders recorded between January 1, 2023 and June 30, 2025. It moves beyond basic charting to assess data quality, transaction economics, product and customer performance, order-status risk, acquisition channels, time trends, and statistically unusual purchases.

The analysis was completed as part of the **DecodeLabs Data Analytics Industrial Training Program**. All findings are calculated from the supplied workbook; no observations are fabricated or based on external data.

## Business Problem

Raw transaction data cannot support sound decisions until its quality, distributions, anomalies, and business relationships are understood. Management needs a defensible view of what drives gross order value, which products and channels matter, whether customers return, and how much booked value is exposed to cancellation or return.

## Objectives

- Assess data completeness, uniqueness, validity, and consistency.
- Understand order size, price, cart, and transaction-value distributions.
- Identify unusual transactions without automatically treating them as errors.
- Rank products, customers, payment methods, and referral sources.
- Measure repeat purchasing and approximate customer lifetime value.
- Analyze daily, weekly, and monthly revenue patterns.
- Translate evidence into practical revenue, retention, marketing, and product actions.

## Dataset Information

| Attribute | Value |
|---|---:|
| Source | `Dataset for Data Analytics.xlsx` |
| Rows | 1,200 orders |
| Columns | 14 |
| Date range | 2023-01-01 to 2025-06-30 |
| Unique customers | 1,189 |
| Gross order value | $1,264,761.96 |
| Average order value | $1,053.97 |
| Products | 7 |

The workbook contains order identifiers, dates, customer and product information, quantities, prices, shipping and payment attributes, fulfillment status, cart size, coupon usage, referral source, and total price.

## Methodology

1. **Data Cleaning** - Parsed dates, standardized text, interpreted blank coupon codes, and tested key business rules.
2. **Descriptive Statistics** - Calculated central tendency, dispersion, quartiles, skewness, and kurtosis.
3. **EDA** - Examined numeric and categorical distributions with business interpretation.
4. **Outlier Analysis** - Compared IQR and Z-score detection and classified unusual cases by business meaning.
5. **Customer Analysis** - Measured customer value, order frequency, repeat rate, and revenue concentration.
6. **Product Analysis** - Ranked products by units, gross order value, average order value, and contribution.
7. **Revenue Analysis** - Compared payment, referral, order-status, coupon, and time-based performance.
8. **Correlation Analysis** - Assessed relationships among quantity, unit price, cart size, and total price.

## Key Insights

- The dataset passes core integrity checks: all 1,200 order IDs and tracking numbers are unique, no complete duplicates exist, numeric business fields are positive, and every `TotalPrice` equals `Quantity × UnitPrice`.
- Gross order value is **$1.265M**, with a **$1,053.97** average order value. The median is lower at **$823.62**, reflecting a right-skewed transaction-value distribution.
- **Chair** is the leading product by gross order value at **$195,620.11 (15.47%)**, narrowly ahead of Printer; **Phone** is lowest at **$151,722.39 (12.00%)**.
- Product revenue is diversified: the top three products contribute approximately **46.12%**, so the business is not dependent on a single product.
- Cancelled and returned orders represent **$519,673.91 (41.09%)** of gross order value. This is the largest commercial risk surfaced by the analysis.
- Only **11 of 1,189 customers (0.93%)** made more than one purchase, and repeat customers generated just **1.54%** of gross order value. Retention is a much larger opportunity than customer concentration.
- The top 10 customers contribute only **2.85%** of gross order value, while the top 20% contribute **45.42%**, indicating a broad customer base rather than dependence on a few accounts.
- Instagram leads referral sources with **$275,285.45 (21.77%)** of gross order value; Facebook has the highest referral-source average order value at **$1,098.29**.
- Credit Card has the highest payment-method average order value at **$1,127.55**, while Online produces the most orders.
- Eight `TotalPrice` observations are IQR outliers, but none exceed an absolute Z-score of 3. Their valid arithmetic and high quantity/price combinations support treating them as premium transactions, not automatic data errors.
- Quantity and unit price both influence total price, with correlations of **0.615** and **0.717**, respectively. Unit price is the stronger linear driver.
- Full-year gross order value declined **13.10%** in 2024 versus 2023; H1 2025 was **9.79%** below H1 2024. Because the dataset ends in June 2025, annual 2025 totals are not compared with complete prior years.

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- SciPy
- Jupyter Notebook

## Repository Structure

```text
Project_02/
├── Dataset for Data Analytics.xlsx
├── EDA_Project.ipynb
├── README.md
└── requirements.txt
```

## How to Run

1. Open a terminal in `Project_02`.
2. Create and activate a virtual environment.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start Jupyter:

   ```bash
   jupyter notebook
   ```

5. Open `EDA_Project.ipynb` and select **Run All**.

The notebook resolves the workbook from either the project directory or the repository root and can be run from top to bottom without editing paths.

## Future Improvements

- Add net revenue, refund amount, shipping cost, margin, and delivery timestamps to distinguish booked value from realized profitability.
- Introduce customer geography and demographic attributes for market segmentation.
- Add product category and cost data for category-level margin analysis.
- Build cohort retention and RFM segmentation when more repeat-purchase history becomes available.
- Apply formal time-series forecasting after collecting a longer, consistently sampled history.
- Run controlled campaign tests to measure whether coupon and referral-channel differences are causal.
