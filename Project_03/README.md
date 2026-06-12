# Project 3: SQL Data Analysis


---

## 📌 Project Overview

This project demonstrates end-to-end **SQL Data Analysis** on a real-world e-commerce transaction dataset using Python and SQLite. Rather than simply viewing data in a spreadsheet, we load the dataset into a relational database and write structured SQL queries to extract actionable business intelligence — exactly as a professional Data Analyst would in an enterprise environment.

The notebook contains **30 SQL queries** across all required clauses, paired with business interpretations that connect each result to a real decision a company would make.

---

## 🎯 Objectives

- Load and explore a structured transactional dataset
- Simulate a relational database using Python's built-in `sqlite3`
- Write professional SQL queries covering `SELECT`, `WHERE`, `ORDER BY`, `GROUP BY`, `COUNT`, `SUM`, and `AVG`
- Combine multiple clauses for advanced analytical queries
- Generate 15 actionable business insights from query outputs

---

## 📁 Project Structure

```
project-3-sql-analysis/
│
├── Data Analytics Project 3.ipynb             ← Main Jupyter Notebook
├── Dataset_for_Data_Analytics.xlsx            ← Source dataset (place here)
├── requirements.txt                           ← Python dependencies
└── README.md                                  ← This file
```

---

## 📊 Dataset

| Attribute       | Detail                                                  |
|-----------------|---------------------------------------------------------|
| File            | `Dataset_for_Data_Analytics.xlsx`                       |
| Records         | 1,200 rows                                              |
| Columns         | 14                                                      |
| Time Range      | 2023 – 2024                                             |
| Products        | Laptop, Phone, Tablet, Monitor, Printer, Chair, Desk    |
| Payment Methods | Credit Card, Debit Card, Online, Gift Card, Cash        |
| Order Statuses  | Delivered, Shipped, Pending, Cancelled, Returned        |
| Referral Sources| Google, Facebook, Instagram, Email, Referral            |

---

## 🛠️ Setup & Installation

### 1. Clone or download the project folder

Place both `SQL_Business_Intelligence_Analysis.ipynb` and `Dataset_for_Data_Analytics.xlsx` in the same directory.

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# Activate — Windows
venv\Scripts\activate

# Activate — macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch Jupyter Notebook

```bash
jupyter notebook
```

Open `SQL_Business_Intelligence_Analysis.ipynb` and run all cells from top to bottom (**Kernel → Restart & Run All**).

---

## 🧩 SQL Concepts Covered

| SQL Feature     | Queries | Purpose                              |
|-----------------|---------|--------------------------------------|
| `SELECT`        | All     | Data retrieval & column projection   |
| `DISTINCT`      | Q3–Q5   | Unique value enumeration             |
| `WHERE`         | Q6–Q11  | Row-level filtering & segmentation   |
| `ORDER BY`      | Q12–Q15 | Sorting, ranking, top-N analysis     |
| `GROUP BY`      | Q16–Q23 | Categorical bucketing                |
| `COUNT()`       | Q16–Q18 | Volume & frequency metrics           |
| `SUM()`         | Q19–Q20 | Revenue totals                       |
| `AVG()`         | Q21–Q22 | Performance benchmarking             |
| `HAVING`        | Q30     | Post-aggregation filtering           |
| `CASE WHEN`     | Q27     | Conditional aggregation              |
| `STRFTIME`      | Q28     | Date-based time-series grouping      |
| Combined clauses| Q24–Q30 | Executive-level BI queries           |

---

## 💡 Key Business Insights

1. **Laptops** generate the highest Average Order Value of all product categories
2. **Google** referral channel drives the highest-value customer orders
3. **Credit Card & Debit Card** dominate payment method preferences
4. **Delivered order rate** is the primary fulfilment health KPI
5. **Repeat customers** identified via `HAVING` represent the highest lifetime value segment
6. **Monthly revenue trends** reveal seasonality patterns for demand forecasting
7. **Coupon codes** act as basket-building tools, not just margin reducers

*Full insights with supporting query outputs are documented in Section 10 of the notebook.*

---

## 🔑 SQL Execution Order (Key Concept)

One of the most important concepts demonstrated in this project is that **the order you write SQL is not the order the database executes it**:

```
Write order:   SELECT → FROM → WHERE → GROUP BY
Execute order: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY
```

This explains why `WHERE` cannot reference aliases defined in `SELECT` (they don't exist yet at execution step 2), and why `HAVING` is required to filter on aggregated results.

---

## 🧰 Tech Stack

| Tool       | Purpose                         | Version  |
|------------|---------------------------------|----------|
| Python     | Runtime environment             | 3.10+    |
| pandas     | Data loading & display          | 2.0+     |
| sqlite3    | In-memory relational database   | stdlib   |
| openpyxl   | Excel file reading engine       | 3.1+     |
| Jupyter    | Interactive notebook interface  | 7.0+     |

---

## 📝 Notes

- `sqlite3` is part of Python's standard library — no separate installation required
- All queries use standard SQL syntax compatible with **SQLite, MySQL, and PostgreSQL** (minor adjustments needed for `STRFTIME` in non-SQLite engines)
- The notebook is fully self-contained — no external API calls or internet connection required after setup

---

*Completed as part of DecodeLabs Data Analytics Industrial Training Program — Batch 2026*