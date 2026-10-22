# FROM DATA TO THESIS: Using Python for Non-Technical
# Playground, Chapter 1: Getting Started with Python
#
# Four parts, as on the playground page:
#   A. Practise the chapter       the book's exercises, with blanks (______) to fill
#   B. Go further                 new exercises beyond the book
#   C. Check your understanding   short questions; answers in solutions.py
#   D. Do it yourself             open tasks with no starter code and no answers
#
# Run a line with Shift+Enter in VS Code / interactive window.
# Try each exercise yourself before you look at solutions.py.

import pandas as pd

students  = pd.read_csv("students.csv")
semesters = pd.read_csv("semesters.csv")


# ==============================================================================
# A. PRACTISE THE CHAPTER
# ==============================================================================

# Exercise 1: A supervisor's sleep
# A supervisor sleeps 8, 7.5, 6, and 7 hours on four nights. Store the numbers in
# a list called supervisor_sleep and find the average, rounded to one decimal place.
supervisor_sleep = [8, 7.5, 6, 7]
average_sleep = sum(supervisor_sleep) / ______
round(average_sleep, ______)


# Exercise 2: Text and numbers
# Check the data types of "600" and 600 with type(), and explain the difference.
type("600")
type(______)


# Exercise 3: A missing value in pandas
# Show how pandas calculates the mean of a series while automatically handling
# missing values, and how to count missing values.
import numpy as np

sample_data = pd.Series([4, np.nan, 6])
sample_data.mean()
sample_data.______.sum()


# Exercise 4: The youngest and the oldest student
# Using students, find the minimum and maximum student age.
students['age'].______()
students['age'].______()


# Exercise 5: Part-time students
# Using .value_counts(), find how many students study part-time (variable study_mode).
students['study_mode'].______()


# Exercise 6: Decisions without a record
# Think of an analysis you have done, or read about, with a point-and-click
# program. List three decisions in it that a reader could not check without a
# written record.
# 1.
# 2.
# 3.


# ==============================================================================
# B. GO FURTHER
# ==============================================================================

# Exercise 7: Calculating with lists and series
# A student slept 6.5, 7, 5.5, 8, 7.5, 6, and 9 hours over a week.
# Convert the numbers to minutes (hours * 60), find the difference between
# the longest and shortest night in minutes, and count nights under 7 hours.
week = pd.Series([6.5, 7, 5.5, 8, 7.5, 6, 9])
minutes = week * ______
minutes
minutes.max() - minutes.min()
(week ______ 7).sum()


# Exercise 8: Master's and PhD students
# Find how many students are in each programme, and the percentage of PhD students.
counts = students['programme'].value_counts()
counts
phd_share = counts['PhD'] / counts.______()
print(f"PhD percentage: {phd_share * 100:.1f}%")


# Exercise 9: Reading Python error messages
# Each commented line below has one mistake. Remove the #, run it, read the error, and fix it.
sleep_week = [6.5, 7, 5.5, 8]
# round(sum(sleep_week) / len(sleep_week), 1
# print(sleep_wek)
# faculty = Education


# Exercise 10: Exploring a built-in dataset
# Using seaborn's built-in penguins dataset, find how many penguins are in the sample,
# their average body mass, and the count of each species.
import seaborn as sns

penguins = sns.load_dataset("penguins")
print(penguins.shape)
print(penguins['body_mass_g'].______())
print(penguins['species'].______())


# ==============================================================================
# C. CHECK YOUR UNDERSTANDING
# Answer in your own words, then compare with the answers in solutions.py.
# ==============================================================================

# 1. What is the difference between an integer (int) and a float in Python?
# 2. How does pandas handle missing values (NaN) when computing .mean()?
# 3. What is the difference between running code in an interactive terminal vs saving a script?
# 4. What is the difference between 'pip install' and 'import'?
# 5. Why is a Python script described as a reproducible record of research decisions?


# ==============================================================================
# D. DO IT YOURSELF
# Open tasks: no starter code, no hints, and no answers. Write your own code
# under each task, as you would for a thesis.
# ==============================================================================

# Task 1: Store your own hours of sleep for the last seven nights in a list, with
# a comment above each step, and report the average, the shortest night, and the
# count of nights under 7 hours.



# Task 2: Using students, report three descriptive facts about the sample (e.g.
# number of faculties, share of female students, and median age).



# Task 3: Load penguins from seaborn, check its column names, and calculate
# the average bill length for each species using .groupby('species')['bill_length_mm'].mean().



# Task 4: Set up a project folder for your thesis on your computer with a data/
# subfolder and an analysis.py script that loads students.csv and prints .shape and .info().
