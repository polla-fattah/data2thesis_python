# FROM DATA TO THESIS: Using Python for Non-Technical
# Playground, Chapter 16: Time Series Forecasting
#
# Four parts, as on the playground page:
#   A. Practise the chapter       the book's exercises with pandas and statsmodels
#   B. Go further                 new exercises beyond the book
#   C. Check your understanding   short questions; answers in solutions.py
#   D. Do it yourself             open tasks with no starter code and no answers
#
# Run a line with Shift+Enter in your IDE or execute: python exercises.py
# Try each exercise yourself before you look at solutions.py.

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
fc_snaive = y_cl[-______:]   # weekly season: last 7 days

ex1_table = pd.DataFrame({
    'Day': range(15, 22),
    'Mean': fc_mean.round(1),
    'Naive': fc_naive,
    'Seasonal_Naive': fc_snaive
}).set_index('Day')
# print(ex1_table)


# Exercise 2: The seasonally adjusted series
stl_obj = STL(visits['visits'], period=52, robust=True).fit()
season_adjust = visits['visits'] - ______   # subtract the seasonal component
# print(season_adjust.head())


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
    print(f"Fourier K={K_val:2d}: MAE = {mae_of(y_te, pred):.2f}")


# Exercise 4: Train on three years, test on the fourth
train_3 = visits[visits.index < '______']  # first 3 academic years end Aug 2023
test_4  = visits[(visits.index >= '2023-09-01') & (visits.index < '2024-09-01')]
y_tr3 = train_3['visits'].values
y_te4 = test_4['visits'].values
h4 = len(y_te4)

stl_3 = STL(np.log(y_tr3), period=52, robust=True).fit()
sa_3 = np.log(y_tr3) - stl_3.seasonal
ets_3 = Holt(sa_3, initialization_method='estimated').fit()
fc_stl_ets3 = np.exp(ets_3.forecast(h4) + stl_3.seasonal[-52:])
# print("STL + ETS Year 4 MAE:", mae_of(y_te4, fc_stl_ets3))


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
    exam_totals.append(np.sum(sim_path[11:15]))

q_exam = np.quantile(exam_totals, [0.025, 0.5, 0.975]).round()
# print("Exam weeks (12-15) forecast:", q_exam)


# Exercise 6: Explaining a prediction interval
# Write a short paragraph for the counselling service explaining what a 95% interval means.


# Exercise 7: Twice the noise in the artificial series
for noise_sd in [3.0, 6.0]:
    np.random.seed(4)
    w = np.arange(1, 157)
    s = 30 + 0.05 * w + 12 * np.sin(2 * np.pi * w / 52) + np.random.normal(0, ______, 156)
    print(f"Noise SD {noise_sd} -> Total SD = {np.std(s):.2f}")


# ==============================================================================
# B. GO FURTHER
# ==============================================================================

# Exercise 8: Build a series and forecast with growth
np.random.seed(1)
w8 = np.arange(1, 209)
s8 = 50 + 0.1 * w8 + 15 * np.sin(2 * np.pi * w8 / 52) + np.random.normal(0, 4, 208)
act8 = s8[156:208]
last8 = s8[104:156]
growth_52 = 0.1 * ______   # growth over 52 weeks


# Exercise 9: Autocorrelation by hand vs acf()
x = visits['visits'].values
n = len(x)
r1  = np.corrcoef(x[1:], x[:-1])[0, 1]
r52 = np.corrcoef(x[______:], x[:-52])[0, 1]


# Exercise 10: Airline passengers and growing seasonal swings
flights = pd.read_csv("flights.csv")
f49 = flights[flights['year'] == 1949]['passengers'].values
f60 = flights[flights['year'] == 1960]['passengers'].values
raw_swing_49 = f49.max() - f49.min()
raw_swing_60 = f60.max() - f60.min()
log_swing_49 = np.log(f49).max() - np.log(f49).min()
log_swing_60 = np.log(f60).max() - np.log(f60).min()


# Exercise 11: Carbon dioxide and the missing trend
co2_df = pd.read_csv("co2.csv")
y_co2 = co2_df['co2'].values
n_tr = len(y_co2) - 24
tr_co2 = y_co2[:n_tr]
te_co2 = y_co2[n_tr:]
last_year_co2 = np.tile(tr_co2[-12:], 2)
annual_growth = tr_co2[-1] - tr_co2[-______]   # growth over the previous 12 months


# ==============================================================================
# C. CHECK YOUR UNDERSTANDING
# Answer in your own words, then compare with the answers in solutions.py.
# ==============================================================================

# 1. Why are the observations of a time series not independent?
# 2. What is the difference between trend, season, and noise?
# 3. Why must the test period come after the training period?
# 4. What is a prediction interval?
# 5. Why should every forecast be compared with benchmarks?


# ==============================================================================
# D. DO IT YOURSELF
# Open tasks: no starter code, no hints, and no answers. Write your own code
# under each task, as you would for a thesis.
# ==============================================================================

# Task 1: Fit ETS and SARIMAX on monthly CO2 or flight passengers, evaluate
# across a held-out test period, and report with prediction intervals.

# Task 2: Write a one-page summary for the university counselling service
# regarding next year's expected demand, with numbers derived from your code.

# Task 3: Identify three real-world changes that could violate the model's
# assumptions and cause next year's forecasts to deviate from reality.
