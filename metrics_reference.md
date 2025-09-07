# Pocket Guide to IPO & Financial Metrics

> **Units:** All amounts are normalized to **₹ crore** (2 decimals).
> **Nulls:** Missing/uncertain values are set to `null`—never guess.

---

## 1) Terms (IPO Basics)

### **open\_date**

* **What:** Start date for IPO applications.
* **Why it matters:** Defines when bids can be placed.
* **Example:** `2025-08-26`.

### **close\_date**

* **What:** Last date for IPO applications.
* **Why it matters:** After this, bids close.
* **Example:** `2025-08-29`.

### **price\_band**

* **What:** Indicative range investors can bid within.
* **Format:** e.g., `₹95–₹100` per share.
* **Why it matters:** Guides valuation and allocation price discovery.
* **If missing:** `null` (not finalized or not in source).

### **lot\_size**

* **What:** Minimum shares per application.
* **Why it matters:** Determines minimum investment.
* **Example:** Lot size `150`, final price `₹100` → min bid = `150 × 100 = ₹15,000`.
* **If missing:** `null`.

---

## 2) Core Financials (Yearly)

> Fields appear per fiscal year (e.g., `2023`, `2024`, `2025`).

### **revenue\_cr**

* **What:** Total sales before costs.
* **Example:** `120.29` → ₹120.29 crore.

### **ebitda\_cr**

* **What:** Earnings **before** interest, tax, depreciation, amortization (core operating profit proxy).
* **Example:** `32.38`.

### **pat\_cr**

* **What:** Profit After Tax (bottom line).
* **Example:** `20.52`.

### **networth\_cr**

* **What:** Shareholders’ equity = Assets − Liabilities.
* **Example:** `80.42`.

### **debt\_cr**

* **What:** Total borrowings outstanding.
* **Example:** `58.35`.

### **cfo\_cr**

* **What:** Cash flow from operations (actual cash from core business).
* **Example:** `-22.55` (negative indicates cash strain).

---

## 3) Derived Metrics (Computed)

### **window\_years**

* **What:** Count of periods used after sorting (max last 6).
* **Computation:** `len(rows)`.

### **fy\_range**

* **What:** First and last FY labels in window.
* **Computation:** `[fy_labels[0], fy_labels[-1]]`.

### **revenue\_cagr**

* **What:** Compound Annual Growth Rate of revenue across the window.
* **Formula:** $(\text{Rev}_{\text{last}} / \text{Rev}_{\text{first}})^{1/(n-1)} - 1$
* **Interpretation:** Higher = better long-term growth.
* **Edge cases:** If `first<=0`, `last<=0`, or <2 valid points → `null`.

### **pat\_cagr**

* **What:** CAGR of PAT (bottom-line growth).
* **Notes:** Big numbers can reflect margin expansion or one-offs.

### **ebitda\_cagr**

* **What:** CAGR of EBITDA (operating growth).
* **Why:** Reinforces quality of growth independent of financing/taxes.

### **pat\_margin**

* **What:** Latest PAT as a % of revenue.
* **Formula:** $\text{PAT} / \text{Revenue}$ (latest year).
* **Interpretation:** Efficiency after all costs/taxes.

### **ebitda\_margin**

* **What:** Latest EBITDA as a % of revenue.
* **Formula:** $\text{EBITDA} / \text{Revenue}$ (latest year).
* **Interpretation:** Operating efficiency; less affected by capital structure.

### **margin\_trend\_ebitda**

* **What:** Change in EBITDA margin from first to last year.
* **Formula:** $(\text{EBITDA}/\text{Rev})_{\text{last}} - (\text{EBITDA}/\text{Rev})_{\text{first}}$
* **Interpretation:** Positive = improving operating structure.

### **revenue\_volatility**

* **What:** Standard deviation of **YoY revenue growth** (predictability proxy).
* **Steps:**

  1. YoY growth: $g_t = \text{Rev}_t/\text{Rev}_{t-1} - 1$
  2. Volatility = `stdev(growth_series)` (sample stdev).
* **Interpretation:** Lower = steadier revenue.

### **debt\_to\_networth**

* **What:** Latest **Debt ÷ Net worth** (leverage proxy, akin to D/E).
* **Interpretation:** Lower = safer; more equity cushion.

### **net\_debt\_to\_ebitda**

* **What:** Latest **(Net) Debt ÷ EBITDA** (years of EBITDA to cover debt).
* **Note:** If cash is unknown, `Debt` used as a proxy for `Net Debt`.
* **Interpretation:**

  * \~1× or less = low leverage
  * \~1–3× = moderate
  * greater than 3× = elevated

### **cfo\_latest**

* **What:** Latest operating cash flow.
* **Interpretation:** Persistent negatives flag working-capital stress or weak cash conversion.

### **cfo\_to\_pat**

* **What:** Latest **CFO ÷ PAT** (cash conversion of earnings).
* **Interpretation:**

  * ≥ 0.9 = strong conversion
  * 0.5–0.9 = okay
  * 0–0.5 = weak
  * ≤ 0 = poor (profits not turning into cash)

### **cfo\_positive\_years\_ratio**

* **What:** Share of years with **CFO > 0**.
* **Interpretation:** Persistence of cash generation (closer to 1.0 is better).

### **cfo\_cumulative**

* **What:** Sum of CFO over the window (multi-year cash generation).
* **Interpretation:** Negative totals strengthen concerns about cash quality.

### **yoy\_revenue\_growth**

* **What:** List of consecutive YoY revenue growth rates (feeds volatility).
* **Formula:** For each adjacent pair, $\text{Rev}_t/\text{Rev}_{t-1} - 1$.
* **Use:** Transparent trail of year-to-year swings.

---

## 4) Decision Engine (Scoring Cheatsheet)

> The engine weights five buckets to produce a label: **Apply / Neutral / Avoid**.

**Weights**

* Growth **30%**
* Profitability **25%**
* Cashflow **20%**
* Leverage **15%**
* Volatility **10%**

**Key Thresholds (summarized)**

* **Revenue CAGR:**

  * ≥20%: Strong (100) · 10–20%: Moderate (70) · 0–10%: Low (40) · <0: Declining (15)
  * **Bonus:** EBITDA CAGR >10% → +10 to growth
* **EBITDA margin:**

  * ≥20%: Strong (55) · 12–20%: Moderate (40) · 5–12%: Thin (25) · <5%: Weak (10)
* **PAT margin:**

  * ≥12%: Healthy (35) · 7–12%: Moderate (25) · 0–7%: Thin (15) · <0: Negative (5)
* **EBITDA margin trend:**

  * greter than 0: Improving (+10)
* **Cashflow:**

  * CFO latest >0 → +45, else +15
  * CFO/PAT: ≥0.9 (35), 0.5–0.9 (25), >0–0.5 (15), ≤0 (5)
  * CFO positive years ratio: ≥0.66 (20), 0.33–0.66 (10), else (5)
* **Leverage:**

  * Debt/Net worth: ≤0.5 (50), ≤1.0 (35), ≤2.0 (20), >2.0 (10)
  * (Net) Debt/EBITDA: ≤1.0 (50), ≤3.0 (35), ≤5.0 (20), >5.0 (10)
* **Revenue volatility:**

  * ≤0.10 (100), ≤0.20 (70), >0.20 (35)

**Labeling**

* Score ≥ 70 → **Apply**
* 55–69.99 → **Neutral**
* < 55 → **Avoid**
  **Confidence:** Tightness to thresholds (55, 70) reduces confidence.

---

## 5) Data Handling & Sorting

* **FY parsing:** Extracts year from labels like `"FY2025"` or `"2025"`; sorts ascending.
* **Windowing:** Uses **last 6** years max (if available).
* **Normalization:** All amounts in **₹ crore**, rounded to 2 decimals.
* **Safety:** Non-numeric or invalid values → `null`, metrics skip gracefully.

---

## 6) Quick Interpretation Rules of Thumb

* **Growth:** Prefer high **revenue\_cagr**; **ebitda\_cagr** supports quality of growth.
* **Profitability:** High **ebitda\_margin** and **pat\_margin**, with positive **margin\_trend\_ebitda**.
* **Cash Quality:** Positive **cfo\_latest**, **cfo\_to\_pat** ≈ 1.0 or higher, healthy **cfo\_cumulative**, decent **cfo\_positive\_years\_ratio**.
* **Leverage:** Low **debt\_to\_networth** and **net\_debt\_to\_ebitda**.
* **Stability:** Low **revenue\_volatility**, reasonable **yoy\_revenue\_growth** swings.

---

### Example Snippet (Structure Only)

```json
{
  "terms_and_financials": {
    "company": "ANLON HEALTHCARE LIMITED",
    "terms": {
      "price_band": null,
      "lot_size": null,
      "open_date": "2025-08-26",
      "close_date": "2025-08-29"
    },
    "financials": [
      {"fy": "2023", "revenue_cr": 112.88, "ebitda_cr": 12.66, "pat_cr": 5.82, "networth_cr": 7.37, "debt_cr": 66.39, "cfo_cr": -2.85},
      {"fy": "2024", "revenue_cr": 66.58, "ebitda_cr": 15.57, "pat_cr": 9.66, "networth_cr": 21.03, "debt_cr": 74.56, "cfo_cr": -3.23},
      {"fy": "2025", "revenue_cr": 120.29, "ebitda_cr": 32.38, "pat_cr": 20.52, "networth_cr": 80.42, "debt_cr": 58.35, "cfo_cr": -22.55}
    ]
  },
  "financial_quality": {
    "window_years": 3,
    "fy_range": ["2023", "2025"],
    "revenue_cagr": 0.0323,
    "pat_cagr": 0.8777,
    "ebitda_cagr": 0.5993,
    "pat_margin": 0.1706,
    "ebitda_margin": 0.2692,
    "margin_trend_ebitda": 0.1570,
    "revenue_volatility": 0.8605,
    "debt_to_networth": 0.7256,
    "net_debt_to_ebitda": 1.8020,
    "cfo_latest": -22.55,
    "cfo_to_pat": -1.0989,
    "cfo_positive_years_ratio": 0.0,
    "cfo_cumulative": -28.63,
    "yoy_revenue_growth": [-0.4102, 0.8067]
  }
}
```

---