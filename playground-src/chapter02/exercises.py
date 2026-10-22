# FROM DATA TO THESIS: Using Python for Non-Technical
# Playground, Chapter 2: Data Structures in Python
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

students = pd.read_csv("students.csv")
semesters = pd.read_csv("semesters.csv")


# ==============================================================================
# A. PRACTISE THE CHAPTER
# ==============================================================================

# Exercise 1: Ages over 30
# Show only the ages over 30 with boolean indexing, and count them.
ages = pd.Series([24, 31, 28, 45, 26])
print(ages[ages ______ 30])
print((ages ______ 30).sum())


# Exercise 2: Ordered categories
# Make the categories run from "Disagree" through "Neutral" to "Agree", and check
# the order with value_counts().
answers = pd.Series(
    pd.Categorical(
        ["Agree", "Disagree", "Neutral", "Agree"],
        categories=______,
        ordered=True
    )
)
print(answers.value_counts(sort=False))


# Exercise 3: Part-time students with children
# Combine two boolean conditions with & (remember parentheses around each condition!)
part_time_parents = (students["study_mode"] == "Part-time") ______ (students["has_children"] == "Yes")
print(part_time_parents.sum())


# Exercise 4: A new column
# Add over_30, True for students older than 30. Count them, and inspect missing values.
students["over_30"] = students["age"] ______ 30
print(students["over_30"].sum())
print(students["over_30"].isna().sum())


# Exercise 5: The question behind a variable
# Read the SPSS file with pyreadstat and find the question behind support_3.
import pyreadstat
spss_df, meta = pyreadstat.read_sav("wellbeing.sav")
print(meta.column_names_to_labels["______"])


# Exercise 6: Units of analysis
# State the unit of analysis of students, semesters, questionnaire, and
# supervisors. For each, name one research question it could answer on its own.
# students:
# semesters:
# questionnaire:
# supervisors:


# ==============================================================================
# B. GO FURTHER
# ==============================================================================

# Exercise 7: A DataFrame of every kind
# Five invented students, with a nominal category, an ordered category, a
# number, and a boolean flag. Check the architecture with .info().
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
print(five.______())


# Exercise 8: The student with no age
# Show the ID, faculty, and programme of the students whose age is missing (isna).
print(students.loc[students["age"].______(), ["student_id", "faculty", "programme"]])


# Exercise 9: Rows and students
# Show the rows of student S0001, count all the rows, count distinct students,
# and check counts per semester.
print(semesters[semesters["student_id"] == "S0001"])
print("Total rows:", len(semesters))
print("Unique students:", semesters["student_id"].______())
print(semesters["semester"].value_counts())


# Exercise 10: Building a codebook DataFrame
# Build a codebook for a sample dataset: variable name, question meaning, and data type.
codebook = pd.DataFrame({
    "variable": ["student_id", "age", "faculty"],
    "meaning": ["Unique student code", "Age at baseline", "Academic faculty"],
    "type": [str(students[col].dtype) for col in ["student_id", "age", "faculty"]]
})
print(codebook)


# ==============================================================================
# C. CHECK YOUR UNDERSTANDING
# Answer in your own words, then compare with solutions.py.
# ==============================================================================

# 1. Why does pd.Series([6.5, "seven"]) become a Series with object/string dtype?
# 2. In Python, what is the difference between df.iloc[0] and df.iloc[1]?
# 3. What is the advantage of setting ordered=True on a pd.Categorical Series?
# 4. Why must an analysis of student demographics count each student once, even
#    when the semesters table has four rows per student?
# 5. What crucial information does an automated codebook provide that raw CSV
#    column headers omit?


# ==============================================================================
# D. DO IT YOURSELF
# Open tasks: write your own code under each task, as you would for a thesis.
# ==============================================================================

# Task 1: Import the semester data twice: from semesters.csv using pd.read_csv(),
# and from the Excel file wellbeing_raw.xlsx using pd.read_excel(). Inspect
# .info() for both, and compare row counts and column data types.



# Task 2: Choose three variables from students (for example gender, employment,
# and financial_worry). Convert each to its appropriate measurement type
# (category, ordered category, or float), inspect with .dtypes, and justify each choice.



# Task 3: Load the built-in penguins dataset from seaborn (sns.load_dataset("penguins")).
# Identify the unit of analysis, check missing values across columns, and compute
# the mean body mass for each penguin species.



# Task 4: Read wellbeing.sav with pyreadstat. Extract meta.column_names and
# meta.column_labels into a clean codebook DataFrame, add an empty 'notes' column,
# and export the result to codebook.csv with index=False.
