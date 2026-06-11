# 🧹 Project 1: Data Cleaning & Preparation
**DecodeLabs Industrial Training | Data Analytics Batch 2026**

---

## 📌 Overview

A complete data cleaning pipeline for a 1,200-record e-commerce transactions dataset.  
Run **one script** → get **one Excel file** with everything inside.

---

## 🎯 Project Goal

> Clean a raw dataset by handling missing values, duplicates, and incorrect data.

| Requirement | Status |
|---|---|
| Identify missing or null values | ✅ |
| Remove duplicate records | ✅ |
| Correct data formats (dates, numbers, text) | ✅ |
| Prepare clean dataset for analysis | ✅ |

---

## 📁 Folder Structure

```
Project_01/
├── Dataset_for_Data_Analytics.xlsx   ← raw input dataset
├── data_cleaning.py                  ← run this
├── requirements.txt                  ← dependencies
└── Project1_Cleaned.xlsx             ← output (auto-generated)
```

---

## ⚙️ How to Run

```bash
# Step 1 — Install dependencies
pip install -r requirements.txt

# Step 2 — Run the script
python data_cleaning.py
```

That's it. `Project1_Cleaned.xlsx` will appear in the same folder.

---

## 📊 Output — Project1_Cleaned.xlsx

One Excel file with 3 sheets:

| Sheet | Contents |
|---|---|
| **Cleaned Dataset** | All 1,200 rows, fully cleaned and formatted |
| **Cleaning Report** | Missing values, duplicates, format changes, validation checks, before/after comparison, summary stats, key insights |
| **Charts** | Missing value heatmap, revenue by product, order status distribution, monthly revenue trend |

---

## 🔍 What Was Cleaned

### Missing Values
- `CouponCode` had **309 null values (25.75%)**
- Filled with `NO_COUPON` — absence of coupon is a valid business state
- All other 13 columns were fully populated

### Duplicates
- Full-row duplicates: **0 found**
- Duplicate OrderIDs: **0 found**
- DecodeLabs verification gate: **PASSED ✅**

### Format Corrections
| Field | Before | After |
|---|---|---|
| Date | datetime64 / mixed | `YYYY-MM-DD` |
| Text columns | Mixed / inconsistent case | Title Case |
| OrderID, CustomerID | Mixed | UPPERCASE |
| UnitPrice, TotalPrice | Variable decimals | 2 decimal places |
| Quantity, ItemsInCart | float64 | int64 |

---

## 📈 Key Findings

- **Total Revenue:** Rs. 12,64,761.96
- **Avg Order Value:** Rs. 1,053.97
- **Top Product:** Chair
- **Top Referral Channel:** Instagram
- **⚠️ Cancel + Return Rate: 41.42%** — critical, industry benchmark is 8–12%

---

## 🛠️ Tech Stack

| Tool | Use |
|---|---|
| Python 3.x | Core language |
| pandas | Data cleaning & manipulation |
| numpy | Numerical operations |
| matplotlib / seaborn | Charts |
| openpyxl | Excel output |

---

## 💼 Resume Bullet Points

- Built an end-to-end Python data cleaning pipeline (Pandas, openpyxl) on a 1,200-record e-commerce dataset, achieving a Data Quality Score of 100/100
- Implemented strategic missing value imputation, duplicate detection, ISO 8601 date standardization, and 7-rule business validation — all outputs consolidated into a single Excel workbook
- Identified a critical 41.42% cancellation + return rate through post-cleaning EDA, surfacing an actionable business insight for stakeholder review

---

*DecodeLabs Industrial Training | Data Analytics | Batch 2026*