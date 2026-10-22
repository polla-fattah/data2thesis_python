# FROM DATA TO THESIS: Using Python for Non-Technical
# Playground, Chapter 1: Getting Started with Python
# Complete Model Solutions

import pandas as pd
import numpy as np
import seaborn as sns

students  = pd.read_csv("students.csv")
semesters = pd.read_csv("semesters.csv")


# ==============================================================================
# A. PRACTISE THE CHAPTER: SOLUTIONS
# ==============================================================================

# Exercise 1: A supervisor's sleep
supervisor_sleep = [8, 7.5, 6, 7]
average_sleep = sum(supervisor_sleep) / len(supervisor_sleep)
print("Exercise 1:", round(average_sleep, 1))  # 7.1


# Exercise 2: Text and numbers
print("Exercise 2 type '600':", type("600"))  # <class 'str'>
print("Exercise 2 type 600:", type(600))      # <class 'int'>
# '600' is text (str); 600 is an integer (int). Python will not allow "600" + 1.


# Exercise 3: A missing value in pandas
sample_data = pd.Series([4, np.nan, 6])
print("Exercise 3 mean:", sample_data.mean())         # 5.0 (skips NaN by default)
print("Exercise 3 missing:", sample_data.isna().sum()) # 1


# Exercise 4: The youngest and the oldest student
print("Youngest age:", students['age'].min())  # 23
print("Oldest age:", students['age'].max())    # 52


# Exercise 5: Part-time students
print("Exercise 5 study mode counts:\n", students['study_mode'].value_counts())
# Full-time: 423, Part-time: 177


# Exercise 6: Decisions without a record
# Model answer:
# 1. Which cases were excluded (e.g. participants who dropped out or had incomplete answers).
# 2. How missing values were treated (imputed, dropped, or ignored).
# 3. Which survey items were reverse-coded prior to computing aggregate scale scores.


# ==============================================================================
# B. GO FURTHER: SOLUTIONS
# ==============================================================================

# Exercise 7: Calculating with lists and series
week = pd.Series([6.5, 7, 5.5, 8, 7.5, 6, 9])
minutes = week * 60
print("Minutes per night:\n", minutes)
print("Difference in minutes:", minutes.max() - minutes.min())  # 210.0
print("Nights under 7 hours:", (week < 7).sum())               # 3


# Exercise 8: Master's and PhD students
counts = students['programme'].value_counts()
print("Programme counts:\n", counts)
phd_share = counts['PhD'] / counts.sum()
print(f"PhD percentage: {phd_share * 100:.1f}%")  # 29.0%


# Exercise 9: Reading Python error messages
sleep_week = [6.5, 7, 5.5, 8]
print(round(sum(sleep_week) / len(sleep_week), 1))  # Fixed: added closing parenthesis
print(sleep_week)                                   # Fixed: corrected variable spelling
faculty = "Education"                               # Fixed: enclosed string in quotes
print(faculty)


# Exercise 10: Exploring a built-in dataset
penguins = sns.load_dataset("penguins")
print("Penguins dimensions:", penguins.shape)
print("Average body mass (g):", round(penguins['body_mass_g'].mean(), 1))
print("Species counts:\n", penguins['species'].value_counts())


# ==============================================================================
# C. CHECK YOUR UNDERSTANDING: MODEL ANSWERS
# ==============================================================================

# 1. An int is a whole number (e.g. 600); a float has decimal points (e.g. 6.5).
# 2. In pandas, .mean() automatically ignores NaN values by default (skipna=True),
#    calculating the average across all valid recorded values.
# 3. The interactive window/REPL executes code line-by-line for quick tests, but
#    leaves no permanent record. A script (.py) saves instructions permanently in
#    order, making your analysis reproducible and shareable.
# 4. 'pip install' downloads and installs a package onto your hard drive once.
#    'import' loads that package into your active Python session so you can use it.
# 5. A script records every step of data preparation, cleaning, modeling, and plotting
#    explicitly. Anyone reading the script can trace exactly how every figure and
#    statistic in your thesis was calculated.
