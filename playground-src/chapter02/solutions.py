# FROM DATA TO THESIS: Using Python for Non-Technical
# Playground, Chapter 2: Solutions
#
# Model solutions for parts A and B, and reference answers for part C.
# Part D has no single answer: tasks are open-ended for independent practice.

import pandas as pd
import numpy as np

students = pd.read_csv("students.csv")
semesters = pd.read_csv("semesters.csv")


# ==============================================================================
# A. PRACTISE THE CHAPTER
# ==============================================================================

# Exercise 1: two ages, 31 and 45, are over 30
ages = pd.Series([24, 31, 28, 45, 26])
print(ages[ages > 30])
print((ages > 30).sum())


# Exercise 2: Disagree 1, Neutral 1, Agree 2, in explicit ordinal scale
answers = pd.Series(
    pd.Categorical(
        ["Agree", "Disagree", "Neutral", "Agree"],
        categories=["Disagree", "Neutral", "Agree"],
        ordered=True
    )
)
print(answers.value_counts(sort=False))


# Exercise 3: 51 students are part-time and have children
part_time_parents = (students["study_mode"] == "Part-time") & (students["has_children"] == "Yes")
print("Part-time students with children:", part_time_parents.sum())


# Exercise 4: 205 students are older than 30; exactly 1 age is missing
students["over_30"] = students["age"] > 30
print("Students over 30:", students["over_30"].sum())
print("Missing age values:", students["age"].isna().sum())


# Exercise 5: "My supervisor cares about my wellbeing."
import pyreadstat
spss_df, meta = pyreadstat.read_sav("wellbeing.sav")
print("Prompt:", meta.column_names_to_labels["support_3"])


# Exercise 6 (model answer):
# students: an individual graduate student (600 rows). Example Q: Are part-time
#   students more likely to report intention to discontinue studies?
# semesters: one student observed in one semester (2,326 rows). Example Q: Does
#   average sleep duration decline between semester 1 and semester 4?
# questionnaire: baseline survey response per student (600 rows, 22 items).
#   Example Q: What is the correlation between baseline stress and burnout?
# supervisors: a faculty supervisor (120 rows). Example Q: Does supervisory
#   workload differ significantly by faculty or academic rank?


# ==============================================================================
# B. GO FURTHER
# ==============================================================================

# Exercise 7: A DataFrame holding nominal, ordered ordinal, numeric, and boolean types
five = pd.DataFrame({
    "faculty": pd.Categorical(["Science", "Education", "Science", "Engineering", "Education"]),
    "exercise": pd.Categorical(
        ["Rarely", "Often", "Sometimes", "Rarely", "Often"],
        categories=["Rarely", "Sometimes", "Often"],
        ordered=True
    ),
    "age": [26, 34, 29, 41, 25],
    "works": [True, False, False, True, True]
})
print(five.info())
print("Students who exercise more than rarely:")
print(five[five["exercise"] > "Rarely"])


# Exercise 8: Exactly one student (S0007), a Master's student in Health Sciences
missing_age_students = students.loc[students["age"].isna(), ["student_id", "faculty", "programme"]]
print(missing_age_students)


# Exercise 9: S0001 has 4 rows; 2,326 total rows across 600 unique students;
# 37 students have incomplete follow-up (no records in semesters 3 or 4)
print(semesters[semesters["student_id"] == "S0001"])
print("Total rows:", len(semesters))
print("Unique students:", semesters["student_id"].nunique())
print(semesters["semester"].value_counts())


# Exercise 10: Building a codebook DataFrame
codebook = pd.DataFrame({
    "variable": ["student_id", "age", "faculty"],
    "meaning": ["Unique student code", "Age at baseline", "Academic faculty"],
    "type": [str(students[col].dtype) for col in ["student_id", "age", "faculty"]]
})
print(codebook)


# ==============================================================================
# C. CHECK YOUR UNDERSTANDING: model answers
# ==============================================================================

# 1. A Pandas Series requires a homogeneous data type. Since text cannot be
#    converted to a number without information loss, Pandas coerces the entire
#    collection to 'object' (string) dtype.
# 2. Python is 0-indexed: df.iloc[0] returns the very first row (offset 0),
#    while df.iloc[1] returns the second row (offset 1).
# 3. Setting ordered=True enforces an explicit ordinal ranking. It ensures that
#    value_counts(), summary tables, and plots display categories in logical order
#    rather than alphabetical order, and allows comparisons like cat > 'Disagree'.
# 4. The research question is about individuals. Counting rows in a multi-wave
#    table would count student-semesters, artificially weighting students who
#    remained in the study longer and violating the assumption of independence.
# 5. A codebook provides the semantic foundation: the verbatim survey item text,
#    the measurement scale (e.g., 1-5 Likert anchors), value label encodings,
#    and conventions used for missing observations.


# ==============================================================================
# D. DO IT YOURSELF
# Open-ended practical applications.
# ==============================================================================
