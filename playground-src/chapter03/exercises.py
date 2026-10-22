# FROM DATA TO THESIS: Using Python for Non-Technical
# Playground, Chapter 3: Data Manipulation and Cleaning with Pandas
#
# Four parts, as on the playground page:
#   A. Practise the chapter       the book's exercises, with blanks (______) to fill
#   B. Go further                 new exercises beyond the book
#   C. Check your understanding   short questions; answers in solutions.py
#   D. Do it yourself             open tasks with no starter code and no answers
#
# Run line by line in VS Code using Shift+Enter (Send to Interactive Window).
# Try each exercise yourself before checking solutions.py.

import pandas as pd
import numpy as np

students      = pd.read_csv("students.csv")
semesters     = pd.read_csv("semesters.csv")
supervisors   = pd.read_csv("supervisors.csv")
questionnaire = pd.read_csv("questionnaire.csv")


# ==============================================================================
# A. PRACTISE THE CHAPTER
# ==============================================================================

# Exercise 1: Average age by faculty, sorted from oldest to youngest
faculty_age = (
    students
    .groupby("______")["age"]
    .mean()
    .sort_values(ascending=______)
    .reset_index()
)
print(faculty_age)


# Exercise 2: Sleep in three categories
# "Short" under 6 hours, "Recommended" 7 or more, "Moderate" otherwise. Count
# records in each category (keeping missing values as NaN).
conditions = [
    semesters["sleep_hours"].isna(),
    semesters["sleep_hours"] < 6,
    semesters["sleep_hours"] ______ 7
]
choices = [np.nan, "Short", "Recommended"]

semesters["sleep_group"] = np.select(conditions, choices, default="Moderate")
print(semesters["sleep_group"].value_counts(dropna=False))


# Exercise 3: One column per semester
# A table of GPA with one row per student and one column per semester.
gpa_wide = (
    semesters[["student_id", "semester", "gpa"]]
    .pivot(index="______", columns="______", values="gpa")
    .reset_index()
)
print(gpa_wide.head())


# Exercise 4: GPA by study mode
# Merge semesters with students and compare average GPA between study modes.
study_mode_gpa = (
    semesters
    .merge(students[["student_id", "study_mode"]], on="______", how="left")
    .groupby("______")["gpa"]
    .mean()
    .reset_index()
)
print(study_mode_gpa)


# Exercise 5: A reversed item
# Explain in your own words why stress_4 must be reverse-coded before computing
# the composite stress score, and what would happen if it were left unreversed.


# Exercise 6: Clean data in your own field
# For each quality of clean data (valid, accurate, complete, consistent, unique),
# give one example of a data issue from your own field and the required cleaning step.


# ==============================================================================
# B. GO FURTHER
# ==============================================================================

# Exercise 7: The missing-code trap
# Two skipped answers were recorded as 99. Compare the mean and median with
# and without replacing 99 with NaN.
answers = pd.Series([4, 3, 5, 99, 2, 99, 1])
print("With 99 - Mean:", answers.mean(), "Median:", answers.median())

clean_answers = answers.replace(______, np.nan)
print("With NaN - Mean:", clean_answers.mean(), "Median:", clean_answers.median())


# Exercise 8: Checking two tables against each other
# Count each supervisor's students from semester 1 data, merge with supervisors,
# and check whether the counted students equal n_students.
sem1 = semesters[semesters["semester"] == 1]
check = (
    sem1
    .merge(students[["student_id", "supervisor_id"]], on="student_id", how="left")
    .groupby("supervisor_id")
    .agg(n_counted=("student_id", "______"))
    .reset_index()
    .merge(supervisors, on="supervisor_id", how="left")
)
print(check.head())
discrepancies = check[check["n_counted"] ______ check["n_students"]]
print("Discrepancies found:", len(discrepancies))


# Exercise 9: The questionnaire in long format
# Reshape the 22 questionnaire items from wide to long, and compute the mean
# answer for each item.
long_q = pd.melt(
    questionnaire,
    id_vars=["______"],
    var_name="item",
    value_name="answer"
)
print("Long table shape:", long_q.shape)
item_means = (
    long_q
    .groupby("item")["answer"]
    .mean()
    .reset_index()
)
print(item_means.head(10))


# Exercise 10: Cleaning a small messy DataFrame
# Fix faculty text variations and decimal commas in sleep values.
messy = pd.DataFrame({
    "faculty": ["Education", "education ", "EDUCATION", "Health Sciences", "health sci."],
    "sleep":   ["6,5", "7 hrs", "8", "5.5", "7,5"]
})

clean = messy.assign(
    faculty = np.where(messy["faculty"].str.lower().str.contains("educ"), "Education", "Health Sciences"),
    sleep   = (messy["sleep"]
               .str.replace("______", ".")
               .str.extract(r"([\d\.]+)", expand=False)
               .astype(float))
)
print(clean)
print("Mean sleep:", clean["sleep"].mean())


# ==============================================================================
# C. CHECK YOUR UNDERSTANDING
# Answer in your own words, then compare with solutions.py.
# ==============================================================================

# 1. Clean data is valid, accurate, complete, consistent, and unique. What does
#    each quality guard against?
# 2. Why is the raw primary data file never edited by hand in Excel?
# 3. What is tidy data, and why does analysis become simpler when data is tidy?
# 4. What is the difference between a left join and an anti-join?
# 5. Why should a 99 not be replaced with NaN globally across an entire dataset?


# ==============================================================================
# D. DO IT YOURSELF
# Open tasks: write your own code under each task, as you would for a thesis.
# ==============================================================================

# Task 1: Which faculty has the largest proportion of students who moved away
# from their family (lives_away == 'Yes'), and how does that proportion differ
# between Master's and PhD students across faculties? Generate one grouped summary table.



# Task 2: Calculate each student's burnout score as the average of burnout_1..6,
# merge it with the first-semester records, and compare the average burnout of
# students who have versus have not considered dropping out.



# Task 3: Load the raw Excel export (wellbeing_raw.xlsx) using pd.read_excel().
# Identify all test accounts and duplicate rows, remove them, and report how many
# genuine participants remain.



# Task 4: Write a python function clean_survey_data() that executes the full
# survey cleaning pipeline from start to finish, outputting clean DataFrames for
# students, semesters, and questionnaire items.
