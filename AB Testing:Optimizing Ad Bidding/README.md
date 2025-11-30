# 📊 A/B Testing: Optimizing Ad Bidding Strategy

## 🛑 Final Recommendation: DO NOT IMPLEMENT TEST VARIANT

The new bidding strategy (Test Group) **significantly underperformed** the existing strategy (Control Group) on both the **Purchase Rate** and **Click-Through Rate (CTR)**, which are the primary user engagement and conversion metrics.

| Metric | Control Rate | Test Rate | Result | Significance ($p$-value) |
| :--- | :--- | :--- | :--- | :--- |
| **Purchase Rate** | $\approx 0.54\%$ | $\approx 0.48\%$ | **Control WINS** | $< 0.05$ (Significant) |
| **Click-Through Rate (CTR)** | $\approx 5.01\%$ | $\approx 3.29\%$ | **Control WINS** | $\approx 0.0$ (Highly Significant) |
| **Earnings per Impression (EPI)** | $\approx 0.020$ | $\approx 0.021$ | Test is $\uparrow$ | $0.062$ (Not Significant at $\alpha=0.05$) |

---

## 🎯 Project Goal & Hypothesis

| Item | Description |
| :--- | :--- |
| **Objective** | Evaluate whether a new ad bidding strategy improves key performance metrics compared to the existing one. |
| **Hypothesis** | The new bidding strategy (Test Group) is expected to have higher Purchase Rate, Click-Through Rate, and Earnings Per Impression. |

### Metric Definitions

| Metric | Formula | Description |
| :--- | :--- | :--- |
| **Purchase Rate** | $\frac{Purchases}{Impressions}$ | Measures how often impressions convert to purchases (Primary Metric) |
| **Click-Through Rate (CTR)** | $\frac{Clicks}{Impressions}$ | Indicates user engagement with the ad (Driver Metric) |
| **Earnings per Impression (EPI)** | $\frac{Earnings}{Impressions}$ | Tracks revenue efficiency per ad impression (Safety/Secondary Metric) |

---

## ⚙️ A/B Test Design & Analysis

The experiment was set up as a two-sample **A/B Test**, with the ad bidding strategy randomized across 40 units (likely unique users or accounts) in each group.

| Design Parameter | Value |
| :--- | :--- |
| **Randomized Units** | 40 (Control) / 40 (Test) |
| **Baseline Purchase Rate** | $\approx 0.54\%$ |
| **Minimum Detectable Effect (MDE)** | $1\%$ |
| **Required Sample Size (Impressions)** | 846 (per group) |
| **Test Performed** | Two-Sample Z-Test (for Rates) and T-Test (for EPI) |

---

## 💡 Detailed Findings

### 1. Purchase Rate (Primary Metric)
* **Result:** The **Control Group** had a significantly higher purchase rate.
* **Statistical Test:** The Z-test yielded a very low $p$-value ($p \ll 0.05$), indicating the difference is **highly statistically significant**. The confidence intervals for the two rates do not overlap, confirming the control group's superiority in driving conversions.

### 2. Click-Through Rate (CTR)
* **Result:** The **Control Group** had a much higher click-through rate.
* **Statistical Test:** The $p$-value was $\approx 0.0$, demonstrating an extremely **statistically significant** drop in user engagement in the test group. The new bidding strategy seems to select ads or placements that users are far less likely to click.

### 3. Earnings Per Impression (EPI)
* **Result:** The **Test Group** showed a slightly higher point estimate for EPI, but this result is **not statistically significant** at the $\alpha=0.05$ level.
* **Statistical Test:** The T-test resulted in a $p$-value of **$0.062$**. This is right on the boundary, but traditionally, we would fail to reject the null hypothesis, meaning we cannot confidently say the test variant increased earnings due to the new strategy (it could be due to chance).

---

## 🛠️ Technology Stack

* **Python**
* **Pandas** (Data Manipulation)
* **NumPy** (Numerical Operations)
* **Matplotlib / Seaborn** (Visualization, Histograms)
* **Statsmodels** (Statistical Tests, Power Analysis)
* **SciPy** (Statistical Tests)
