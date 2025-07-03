# 📊 Sales Data Analysis – Online Retail II

This mini-project analyzes the **Online Retail II dataset** from the UCI Machine Learning Repository. It automates a 3-level reporting pipeline to generate clean, insightful **PDF reports** with visualizations and KPIs using **Python**.

---

## 🔍 Project Overview

This project performs a structured analysis of 2 years of e-commerce sales data. The analysis is broken into 3 levels:

### ✅ Level 1 – Basic Data Overview
- Dataset description
- Column metadata
- Data types
- Key Performance Indicators (KPIs)
- Interesting facts

### ✅ Level 2 – Visual Analysis
- Top 10 countries by revenue
- Monthly revenue trends
- Top 10 products by quantity sold

### ✅ Level 3 – Advanced Insights
- Correlation heatmap of key features
- Revenue distribution (KDE plot)
- Revenue trends for top 3 countries
- Top 10 customers by total revenue

Each level builds on the previous one and is exported as a styled PDF using `ReportLab`.

## 🧰 Tools & Libraries Used

| Tool/Library       | Purpose                 |
|--------------------|-------------------------|
| pandas             | Data manipulation       |
| matplotlib, seaborn | Data visualization      |
| reportlab          | Build PDF reports       |
| datetime, os       | Utilities               |


---

## 📁 Project Structure

```bash
DataVisualizationAssignment/
├── assets/                     # Generated plots and PDFs
├── logic/
│   ├── __init__.py
│   ├── data_processor.py       # Data cleaning and plotting logic
│   └── report_generator.py     # PDF generation logic
├── main.py                     # CLI to select analysis level
├── requirements.txt
└── README.md

