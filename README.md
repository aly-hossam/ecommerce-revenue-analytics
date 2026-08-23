
# 🧸 Maven Fuzzy Factory - E-commerce Traffic, Conversion & Revenue Analytics

An executive-level data analytics project evaluating web traffic, conversion funnels, marketing channel performance, and monetization efficiency for **Maven Fuzzy Factory** (an e-commerce retailer). 

This project features an automated Python data pipeline, net revenue financial auditing (incorporating refunds), and a mobile-optimized **Interactive HTML Executive Dashboard** (`fuzzy_factory_report.html`).

---

## 📌 Executive Summary & Key KPIs

Over a 3-year operating period (**April 2012 – February 2015**), the platform scaled significantly across all primary commercial metrics:

- **Total Website Sessions:** `472,871`
- **Total Completed Orders:** `32,313`
- **Net Audited Revenue:** `$1,853,171` *(Gross Revenue: $1,938,510 less $85,338 refunds / 4.4% refund rate)*
- **Lifetime Conversion Rate (CVR):** `6.83%` *(Grew from 3.19% to peak at 8.7%)*
- **Net Average Order Value (AOV):** `$57.35` *(Evolved from $49.16 to $63.12)*
- **Net Revenue Per Session (RPS):** `$3.92` *(Scaled from $1.57 to $5.28)*

---

## 🎯 Key Business Questions & Strategic Insights

### 1. What is the trend in website sessions and order volume?
- **Insight:** Traffic and orders demonstrated exponential growth. Monthly sessions expanded from **1,879** to peak at **29,722**, while monthly orders grew from **60** to **2,314**. 
- **Methodology Note:** Data line trends exclude partial cutoff months (March 2012 & March 2015) to eliminate false "cliff drop" visualization effects.

### 2. What is the session-to-order conversion rate? How has it trended?
- **Insight:** CVR more than doubled over the platform lifecycle—rising from **3.19%** in early 2012 to **8.7%** in early 2015.
- **Drivers:** Continuous conversion funnel optimization, mobile UI improvements, and cross-selling product line expansions.

### 3. Which marketing channels have been most successful?
- **Volume Leader:** `gsearch (nonbrand)` is the primary acquisition engine, generating **$1,074,110 Net Revenue** (58.0% of total company revenue).
- **High-Intent Efficiency:** Brand search channels (`gsearch brand` and `bsearch brand`) achieved industry-leading conversion rates exceeding **8.5%**.
- **Compounding Brand Equity:** Unpaid channels (`Direct Type-In` and `Organic Search`) generated combined net revenues exceeding **$355,000**, reflecting strong brand retention.

### 4. How has revenue per order (AOV) and revenue per session (RPS) evolved?
- **AOV Growth:** Net Average Order Value grew from **$49.16** to **$63.12**, accelerated by adding product cross-sells and bundles.
- **RPS Growth:** Net Revenue Per Session surged from **$1.57** to **$5.28**, proving compounding monetization efficiency for every incoming site visitor.

---

## 🛠️ Project Architecture & File Structure

```text
.
├── extracted_files/
│   └── Maven+Fuzzy+Factory/
│       ├── orders.csv
│       ├── order_items.csv
│       ├── order_item_refunds.csv
│       ├── products.csv
│       ├── website_pageviews.csv
│       └── website_sessions.csv
├── a.py                             # CLI Tool: Scan, extract, & profile datasets
├── analyze_fuzzy_factory.py         # Main analytics pipeline & HTML dashboard generator
├── fuzzy_factory_report.html        # Interactive mobile-optimized HTML report
├── data_overview_report.md         # Auto-generated Markdown data profiling report
├── .gitignore                       # Git ignore configuration
└── README.md                        # Project documentation
```

---

## 🔍 Data Pipeline & Quality Auditing

1. **Net Revenue Financial Audit:** Integrates `order_item_refunds.csv` to deduct $85,338 in customer refunds from gross sales, giving leadership a true Net Revenue figure ($1,853,171).
2. **Dual-Axis Visualization Fix:** Solved scale flattening in Chart.js by placing AOV ($44-$64) and RPS ($1.5-$5.5) on separate, dual Y-axes.
3. **Partial Month Censoring Fix:** Isolates full operating months (`2012-04` through `2015-02`) for time-series trendlines to prevent distorted trend conclusions.
4. **Mobile UX Optimization:** Transformed channel charts into horizontal bar formats (`indexAxis: 'y'`) and formatted currency tables for clean mobile viewport browsing.

---

## ⚡ How to Run the Project

### 1. Prerequisites
Ensure Python 3.8+ and Pandas are installed:
```bash
pip install pandas
```

### 2. Execution Modes via `a.py` (CLI Tool)
- **Mode 1 (Scan Directory):**
  ```bash
  python a.py 1
  ```
- **Mode 2 (Extract Archives into Folders):**
  ```bash
  python a.py 2
  ```
- **Mode 3 (Automated Data Profiling):**
  ```bash
  python a.py 3
  ```

### 3. Generate Interactive HTML Dashboard
Run the main analytics engine:
```bash
python analyze_fuzzy_factory.py
```
Open `fuzzy_factory_report.html` in any web or mobile browser to view the interactive dashboard.

---

## 📜 License & Credits

- **Dataset Source:** [Maven Analytics](https://mavenanalytics.io/) (Public Domain).
- **Dashboard Stack:** Python, Pandas, Tailwind CSS, Chart.js.