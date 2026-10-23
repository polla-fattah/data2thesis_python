# FROM DATA TO THESIS: Using Python for Non-Technical
# Playground, Chapter 16: Time Series Forecasting
# Solutions

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import STL
from statsmodels.tsa.api import Holt, ExponentialSmoothing
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import acf
from sklearn.metrics import mean_squared_error, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

counselling = pd.read_csv("counselling_visits.csv")
counselling['week_start'] = pd.to_datetime(counselling['week_start'])
visits = counselling.set_index('week_start').sort_index()

def mae_of(actual, forecast):
    return np.mean(np.abs(actual - forecast))

def rmse_of(actual, forecast):
    return np.sqrt(np.mean((actual - forecast)**2))


# ==============================================================================
# A. PRACTISE THE CHAPTER
# ==============================================================================

# Exercise 1: Benchmarks for a series with a trend
clinic = pd.DataFrame({
    'day': range(1, 15),
    'visits': np.array([12, 10, 9, 11, 7, 3, 2,  14, 11, 10, 12, 8, 4, 2]) + np.arange(1, 15)
}).set_index('day')

y_cl = clinic['visits'].values
fc_mean   = np.repeat(np.mean(y_cl), 7)
fc_naive  = np.repeat(y_cl[-1], 7)
fc_snaive = y_cl[-7:]

ex1_table = pd.DataFrame({
    'Day': range(15, 22),
    'Mean': fc_mean.round(1),
    'Naive': fc_naive,
    'Seasonal_Naive': fc_snaive
}).set_index('Day')
print("Ex 1 - Clinic 7-day ahead forecasts with trend:")
print(ex1_table)
# For a series with both trend and seasonality, standard seasonal naive reproduces the
# weekly cycle but ignores the upward trend; naive captures the higher recent level
# but ignores the weekly cycle. A drift/growth seasonal model combines both.


# Exercise 2: The seasonally adjusted series
stl_obj = STL(visits['visits'], period=52, robust=True).fit()
season_adjust = visits['visits'] - stl_obj.seasonal

# Plotting reveals the underlying trajectory without 52-week swings
print("Ex 2 - Seasonally adjusted series summary:")
print(f"Mean: {season_adjust.mean():.1f}, Min: {season_adjust.min():.1f}, Max: {season_adjust.max():.1f}")
# The seasonally adjusted series removes the large exam peaks and summer lows,
# clearly highlighting the gradual upward trend and the extreme October 2023 spike.


# Exercise 3: Fourier models with K = 2, K = 6, and K = 12
train_df = visits[visits.index < '2024-09-01']
test_df  = visits[visits.index >= '2024-09-01']
y_tr = train_df['visits'].values
y_te = test_df['visits'].values
log_y_tr = np.log(y_tr)
h = len(y_te)

t_tr = np.arange(len(y_tr))
t_te = np.arange(len(y_tr), len(y_tr) + h)

for K_val in [2, 6, 12]:
    X_tr = np.column_stack([fn(2 * np.pi * k * t_tr / 52) for k in range(1, K_val + 1) for fn in (np.sin, np.cos)])
    X_te = np.column_stack([fn(2 * np.pi * k * t_te / 52) for k in range(1, K_val + 1) for fn in (np.sin, np.cos)])
    
    m = ARIMA(log_y_tr, order=(1, 0, 0), exog=X_tr).fit()
    pred = np.exp(m.forecast(h, exog=X_te))
    print(f"Ex 3 - Fourier K={K_val:2d}: RMSE = {rmse_of(y_te, pred):.2f}, MAE = {mae_of(y_te, pred):.2f}")
# K=2 produces overly smooth waves; K=6 captures the main peaks; K=12 adds fine detail but
# risks fitting noise. In all cases, smooth sinusoidal waves struggle with the sharp summer step.


# Exercise 4: Train on three years, test on the fourth
train_3 = visits[visits.index < '2023-09-01']
test_4  = visits[(visits.index >= '2023-09-01') & (visits.index < '2024-09-01')]
y_tr3 = train_3['visits'].values
y_te4 = test_4['visits'].values
h4 = len(y_te4)

# Benchmarks
fc_m3  = np.repeat(np.mean(y_tr3), h4)
fc_n3  = np.repeat(y_tr3[-1], h4)
fc_sn3 = y_tr3[-52:]

# STL + ETS
stl_3 = STL(np.log(y_tr3), period=52, robust=True).fit()
sa_3 = np.log(y_tr3) - stl_3.seasonal
ets_3 = Holt(sa_3, initialization_method='estimated').fit()
fc_stl_ets3 = np.exp(ets_3.forecast(h4) + stl_3.seasonal[-52:])

# Fourier K=6
t_tr3 = np.arange(len(y_tr3))
t_te4 = np.arange(len(y_tr3), len(y_tr3) + h4)
X_tr3 = np.column_stack([fn(2 * np.pi * k * t_tr3 / 52) for k in range(1, 7) for fn in (np.sin, np.cos)])
X_te4 = np.column_stack([fn(2 * np.pi * k * t_te4 / 52) for k in range(1, 7) for fn in (np.sin, np.cos)])
ar_3 = ARIMA(np.log(y_tr3), order=(1, 0, 0), exog=X_tr3).fit()
fc_fourier3 = np.exp(ar_3.forecast(h4, exog=X_te4))

ex4_models = {
    'Mean': fc_m3,
    'Naive': fc_n3,
    'Seasonal Naive': fc_sn3,
    'STL + ETS': fc_stl_ets3,
    'Fourier ARIMA': fc_fourier3
}
print("Ex 4 - Year 4 test accuracy (trained on years 1-3):")
for name, preds in ex4_models.items():
    print(f"  {name:15s}: RMSE = {rmse_of(y_te4, preds):.2f}, MAE = {mae_of(y_te4, preds):.2f}")


# Exercise 5: Visits in the four weeks before the first exam period
y_all = visits['visits'].values
stl_all = STL(np.log(y_all), period=52, robust=True).fit()
sa_all = np.log(y_all) - stl_all.seasonal
ets_all = Holt(sa_all, initialization_method='estimated').fit()
fc_log_all = ets_all.forecast(52) + stl_all.seasonal[-52:]

np.random.seed(2026)
resid = stl_all.resid
exam_totals = []
for _ in range(1000):
    sim_noise = np.random.choice(resid, size=52, replace=True)
    sim_path = np.exp(fc_log_all + sim_noise)
    # weeks 12 to 15 (0-indexed 11:15)
    exam_totals.append(np.sum(sim_path[11:15]))

q_exam = np.quantile(exam_totals, [0.025, 0.5, 0.975]).round()
print(f"Ex 5 - 4-week pre-exam total forecast: {int(q_exam[1])} visits (95% interval: {int(q_exam[0])} to {int(q_exam[2])})")


# Exercise 6: Explaining a prediction interval
# "A 95% prediction interval is a range of numbers within which next year's visits are expected
# to fall 95 times out of 100, based on our statistical model. A forecast can never be a single
# exact number because real demand always includes unpredictable weekly noise and unexpected
# events. The interval tells the service how much extra capacity to keep in reserve for peak
# weeks and what minimum workload to plan for during quiet periods."


# Exercise 7: Twice the noise in the artificial series
for noise_sd in [3.0, 6.0]:
    np.random.seed(4)
    w = np.arange(1, 157)
    s = 30 + 0.05 * w + 12 * np.sin(2 * np.pi * w / 52) + np.random.normal(0, noise_sd, 156)
    print(f"Ex 7 - Noise SD = {noise_sd:.1f} -> Total series SD = {np.std(s):.2f}")
# Doubling the noise SD makes the series visibly jagged. Because forecast uncertainty is
# governed by the variance of the unexplained noise, prediction intervals become twice as wide.


# ==============================================================================
# B. GO FURTHER
# ==============================================================================

# Exercise 8: Build a series and forecast with growth
np.random.seed(1)
w8 = np.arange(1, 209)
s8 = 50 + 0.1 * w8 + 15 * np.sin(2 * np.pi * w8 / 52) + np.random.normal(0, 4, 208)
act8 = s8[156:208]
last8 = s8[104:156]

# Growth over 52 weeks is 0.1 * 52 = 5.2
growth_52 = 0.1 * 52
print(f"Ex 8 - Mean MAE:                 {mae_of(act8, np.mean(s8[:156])):.2f}")
print(f"Ex 8 - SNaive MAE:               {mae_of(act8, last8):.2f}")
print(f"Ex 8 - SNaive + Growth (52) MAE: {mae_of(act8, last8 + growth_52):.2f}")


# Exercise 9: Autocorrelation by hand vs acf()
x = visits['visits'].values
n = len(x)
r1 = np.corrcoef(x[1:], x[:-1])[0, 1]
r52 = np.corrcoef(x[52:], x[:-52])[0, 1]
acf_vals = acf(x, nlags=52)
print(f"Ex 9 - Lag 1:  Manual = {r1:.3f}, acf() = {acf_vals[1]:.3f}")
print(f"Ex 9 - Lag 52: Manual = {r52:.3f}, acf() = {acf_vals[52]:.3f}")


# Exercise 10: Airline passengers and growing seasonal swings
flights = pd.read_csv("flights.csv")
f49 = flights[flights['year'] == 1949]['passengers'].values
f60 = flights[flights['year'] == 1960]['passengers'].values
print("Ex 10 - Airline passengers raw annual swing (max - min):")
print(f"  1949: {f49.max() - f49.min()} thousand passengers")
print(f"  1960: {f60.max() - f60.min()} thousand passengers")
print("Ex 10 - Log annual swing (ln(max) - ln(min)):")
print(f"  1949: {np.log(f49).max() - np.log(f49).min():.2f}")
print(f"  1960: {np.log(f60).max() - np.log(f60).min():.2f}")
# On the raw scale, the seasonal swing increases from 44 to 232 thousand passengers as the
# overall volume quadruples. On the logarithmic scale, the swing is roughly constant (0.35 to 0.47).


# Exercise 11: Carbon dioxide and the missing trend
co2_df = pd.read_csv("co2.csv")
y_co2 = co2_df['co2'].values
n_tr = len(y_co2) - 24
tr_co2 = y_co2[:n_tr]
te_co2 = y_co2[n_tr:]

last_year_co2 = np.tile(tr_co2[-12:], 2)
# Growth over last 12 months
annual_growth = tr_co2[-1] - tr_co2[-13]
growth_adj = last_year_co2 + annual_growth * np.repeat([1, 2], 12)

print("Ex 11 - Mauna Loa 2-year forecast MAE:")
print(f"  Mean MAE:                 {mae_of(te_co2, np.mean(tr_co2)):.2f} ppm")
print(f"  Seasonal Naive MAE:       {mae_of(te_co2, last_year_co2):.2f} ppm")
print(f"  SNaive + Growth MAE:      {mae_of(te_co2, growth_adj):.2f} ppm")
print(f"  Estimated annual growth:  {annual_growth:.2f} ppm/year")


# ==============================================================================
# C. CHECK YOUR UNDERSTANDING (Model answers)
# ==============================================================================

# 1. Why are the observations of a time series not independent?
# Because observations close in time are influenced by common underlying factors. A busy week
# of student visits tends to be followed by another busy week because the term schedule, exam
# pressures, and weather persist over time. Time order carries essential information.

# 2. What is the difference between trend, season, and noise?
# - Trend: the long-term, slow progression of the series (rising, falling, or constant).
# - Season: a periodic, repeating pattern linked to a fixed calendar cycle (e.g., 52 weeks).
# - Noise: irregular, unpredictable random fluctuations that cannot be forecast.

# 3. Why must the test period come after the training period?
# In real life, a forecast can only use past data to predict the future. Selecting a random
# subset of time series observations as a test set would allow models to "leak" future
# information backwards in time, giving misleadingly optimistic accuracy scores.

# 4. What is a prediction interval?
# A range of values within which the future observation is expected to fall with a specified
# probability (e.g. 95%). It explicitly quantifies forecasting uncertainty.

# 5. Why should every forecast be compared with benchmarks?
# Complex models (like ETS and ARIMA) require estimation and tuning effort. Comparing them
# against naive, seasonal naive, and mean baselines proves whether the added complexity
# actually yields superior forecast accuracy.
