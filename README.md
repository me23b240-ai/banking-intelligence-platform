# Banking Intelligence Platform

End-to-end customer analytics project covering customer segmentation, churn prediction,
and cross-sell propensity for a banking dataset.

## Business Questions
- Who are the most valuable customers, and which segments are growing?
- Which customers are highly vs. poorly engaged?
- Who is likely to churn, and what drives it?
- Which customers are likely to adopt another product?

## Dataset
Credit Card Customers (BankChurners), Kaggle: https://www.kaggle.com/datasets/sakshigoyal7/credit-card-customers
10,127 rows, 21 columns. Real anonymized bank customer data with a churn label (Attrition_Flag).

Download the CSV and place it at `data/raw/BankChurners.csv` before running the notebooks.

## Structure
- `sql/` - business analytics queries
- `notebooks/` - EDA, segmentation, modeling
- `src/` - reusable Python functions
- `dashboard/` - Streamlit app
- `docs/` - data dictionary, model card, decision memo

## Status
In progress. See docs/ for current phase.