# FROM DATA TO THESIS: Using Python for Non-Technical
# Playground, Chapter 3: Solutions
#
# Model solutions for parts A and B, and reference answers for part C.
# Part D has no single answer: tasks are open-ended for independent practice.

import pandas as pd
import numpy as np

students      = pd.read_csv("students.csv")
semesters     = pd.read_csv("semesters.csv")
supervisors   = pd.read_csv("supervisors.csv")
questionnaire = pd.read_csv("questionnaire.csv")


# ==============================================================================
# A. PRACTISE THE CHAPTER
# ==============================================================================

# Exercise 1: Natural Sciences oldest (30.7), Humanities youngest (29.2)
faculty_age = (
    students
    .groupby("faculty")["age"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)
print("Mean age by faculty:\n", faculty_age)


# Exercise 2: Short 682, Recommended 762, Moderate 861, NaN 21
conditions = [
    semesters["sleep_hours"].isna(),
    semesters["sleep_hours"] < 6,
    semesters["sleep_hours"] >= 7
]
choices = [np.nan, "Short", "Recommended"]

semesters["sleep_group"] = np.select(conditions, choices, default="Moderate")
print("Sleep group frequency:\n", semesters["sleep_group"].value_counts(dropna=False))


# Exercise 3: Wide GPA table (one row per student, columns 1 to 4)
gpa_wide = (
    semesters[["student_id", "semester", "gpa"]]
    .pivot(index="student_id", columns="semester", values="gpa")
    .reset_index()
)
print("GPA Wide head:\n", gpa_wide.head())


# Exercise 4: full-time 3.09, part-time 3.10
study_mode_gpa = (
    semesters
    .merge(students[["student_id", "study_mode"]], on="student_id", how="left")
    .groupby("study_mode")["gpa"]
    .mean()
    .reset_index()
)
print("GPA by study mode:\n", study_mode_gpa)


# Exercise 5 (model answer):
# Item stress_4 ("I feel confident handling problems in my studies") is worded
# in the opposite direction from the other items: agreeing reflects lower stress.
# If averaged without reverse-coding, it cancels out the other items, artificially
# pulling scores toward the neutral midpoint, compressing true variance, and
# weakening correlations with other constructs like burnout or GPA. On a 1-5 scale,
# reverse-coding is achieved by computing 6 - stress_4.


# Exercise 6 (model answer from health research):
# - Valid: A systolic blood pressure recorded as 1,200 mmHg (set to NaN).
# - Accurate: Laboratory assay reading 'below detection limit' encoded as 0.
# - Complete: A participant who missed semester 2 follow-up recorded as NaN, not 0.
# - Consistent: Body weight entered in lbs in one hospital and kg in another (convert).
# - Unique: A patient admitted under two duplicate clinical IDs (merge into one).


# ==============================================================================
# B. GO FURTHER
# ==============================================================================

# Exercise 7: With 99, mean is 30.4 (impossible on 1-5 scale) and median is 4;
# with NaN, mean is 3.0 and median is 3.0.
answers = pd.Series([4, 3, 5, 99, 2, 99, 1])
print("With 99 - Mean:", answers.mean(), "Median:", answers.median())

clean_answers = answers.replace(99, np.nan)
print("With NaN - Mean:", clean_answers.mean(), "Median:", clean_answers.median())


# Exercise 8: No discrepancies found across all 120 supervisors
sem1 = semesters[semesters["semester"] == 1]
check = (
    sem1
    .merge(students[["student_id", "supervisor_id"]], on="student_id", how="left")
    .groupby("supervisor_id")
    .agg(n_counted=("student_id", "count"))
    .reset_index()
    .merge(supervisors, on="supervisor_id", how="left")
)
discrepancies = check[check["n_counted"] != check["n_students"]]
print("Discrepancies found:", len(discrepancies))


# Exercise 9: 13,200 rows (600 students x 22 items). stress_4 has the lowest
# raw mean (2.90) because it is worded inversely.
long_q = pd.melt(
    questionnaire,
    id_vars=["student_id"],
    var_name="item",
    value_name="answer"
)
print("Long questionnaire shape:", long_q.shape)
item_means = long_q.groupby("item")["answer"].mean().reset_index()
print(item_means.head(10))


# Exercise 10: 3 Education, 2 Health Sciences; average sleep is 6.9 hours.
# Without the comma fix, 6,5 becomes 65.0, distorting the mean to 32.1.
messy = pd.DataFrame({
    "faculty": ["Education", "education ", "EDUCATION", "Health Sciences", "health sci."],
    "sleep":   ["6,5", "7 hrs", "8", "5.5", "7,5"]
})

clean = messy.assign(
    faculty = np.where(messy["faculty"].str.lower().str.contains("educ"), "Education", "Health Sciences"),
    sleep   = (messy["sleep"]
               .str.replace(",", ".")
               .str.extract(r"([\d\.]+)", expand=False)
               .astype(float))
)
print(clean)
print("Mean sleep:", clean["sleep"].mean())


# ==============================================================================
# C. CHECK YOUR UNDERSTANDING: model answers
# ==============================================================================

# 1. Valid guards against out-of-range impossible values. Accurate guards against
#    misinterpreting codes as genuine scores. Complete guards against unrecorded
#    missingness. Consistent guards against fragmented category labels. Unique
#    guards against double-counting observations.
# 2. Hand edits in Excel destroy the audit trail. Code-based data cleaning keeps
#    the raw file untouched, ensuring any step can be audited, adjusted, or re-run.
# 3. In tidy data, each variable is a column, each observation is a row, and each
#    cell is a value. This structure allows seamless vectorized operations and
#    grouped aggregation in Pandas.
# 4. A left join keeps all rows of the left table and appends matching columns;
#    an anti-join filters the left table to identify cases that have NO match in
#    the right table (useful for tracking study attrition).
# 5. 99 is not always a missing code. In a 0-100 scale (like wellbeing), 99 is an
#    authentic measurement. Codes must only be replaced in columns where the
#    codebook explicitly defines 99 as missing.


# ==============================================================================
# D. DO IT YOURSELF
# Open-ended practical applications.
# ==============================================================================
