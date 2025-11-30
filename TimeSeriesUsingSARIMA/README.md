

# 📈 Time Series Forecasting: Beer Sales Prediction

## 🚀 Key Results: Future Trend Prediction

This project implements a **Seasonal ARIMA (SARIMA)** model to forecast future beer sales based on historical data. The model successfully captures the underlying trend and seasonality, enabling accurate projections for future time periods.

| Metric | Result | Interpretation |
| :--- | :--- | :--- |
| **Model Type** | **SARIMA** | Handles both non-stationary trends and seasonal cycles. |
| **Seasonality** | **Detected** | The data exhibits clear recurring patterns (seasonality) which were incorporated into the model. |
| **Forecasting** | **Future Projection** | Successfully generated sales forecasts for upcoming months, visualized alongside historical data. |

-----
## 📊 Forecast Visualization
<img width="994" height="659" alt="image" src="https://github.com/user-attachments/assets/a188e0a3-2df4-40f0-af13-4c9de930cc29" />


## 🎯 Project Goal & Methodology

The primary goal is to analyze historical sales data and build a predictive model that can anticipate future demand.

| Area | Approach |
| :--- | :--- |
| **Problem Type** | Time Series Forecasting (Univariate) |
| **Data Source** | `BeerWineLiquor.csv` (Historical Beer Sales Data) |
| **Core Technique** | **SARIMA** (Seasonal AutoRegressive Integrated Moving Average) |
| **Objective** | Analyze stationarity and seasonality to configure a robust forecasting model. |

### Methodology Pipeline

1.  **Exploratory Data Analysis (EDA):**
      * Visualized the time series to identify **Trend** and **Seasonality**.
      * Performed **Decomposition** to separate the series into trend, seasonal, and residual components.
2.  **Stationarity Check:**
      * Utilized the **Augmented Dickey-Fuller (ADF) Test** to check if the data was stationary (a requirement for ARIMA models).
      * Applied differencing (`d` and `D` parameters) to stabilize the mean and variance.
3.  **Model Configuration:**
      * Selected SARIMA parameters: `Order=(1, 1, 1)` and `Seasonal Order=(1, 1, 1, 6)`.
      * **p, d, q:** Auto-regressive, Integrated (differencing), Moving Average terms.
      * **P, D, Q, s:** Seasonal counterparts with a periodicity of **6**.
4.  **Forecasting:**
      * **Validation:** Predicted values on a hold-out set (recent history) to visually verify model accuracy.
      * **Future Prediction:** Generated a new timeframe (`future_dates`) and forecasted sales into the unknown future.

-----

## ⚙️ Model Architecture

The project utilizes `statsmodels` to implement the SARIMA architecture:

```python
# Model Configuration Used
model = sm.tsa.statespace.SARIMAX(
    df['beer'],
    order=(1, 1, 1),          # (p, d, q)
    seasonal_order=(1, 1, 1, 6) # (P, D, Q, s)
)
```

  * **AR (Auto-Regressive):** Uses past values to predict future ones.
  * **I (Integrated):** Differencing applied to make the series stationary.
  * **MA (Moving Average):** Uses past forecast errors to correct future predictions.
  * **S (Seasonality):** accounts for regular pattern repeats (e.g., higher sales in summer).

-----

## 🛠️ Technology Stack

| Category | Tools/Libraries |
| :--- | :--- |
| **Language** | Python |
| **Modeling** | **Statsmodels** (SARIMAX) |
| **Data Manipulation** | **Pandas** (Time series indexing, Date parsing) |
| **Numerical Computing** | NumPy |
| **Visualization** | Matplotlib (Plotting trends and forecasts) |
