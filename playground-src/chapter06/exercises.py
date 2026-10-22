# FROM DATA TO THESIS: Using Python for Non-Technical
# Playground, Chapter 6: Descriptive Statistics and Exploratory Data Analysis
#
# Four parts, as on the playground page:
#   A. Practise the chapter       the book's exercises, with blanks (______) to fill
#   B. Go further                 new exercises beyond the book
#   C. Check your understanding   short questions; answers in solutions.py
#   D. Do it yourself             open tasks with no starter code and no answers
#
# Run a line with Shift+Enter in VS Code / interactive window.
# Try each exercise yourself before you look at solutions.py.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm

# Load datasets
students = pd.read_csv("students.csv")
semesters = pd.read_csv("semesters.csv")
questionnaire = pd.read_csv("questionnaire.csv")

first_sem = (
    semesters.query("semester == 1")
    .merge(students, on="student_id")
)


# ==============================================================================
# A. PRACTISE THE CHAPTER
# ==============================================================================

# Exercise 1: Four summaries of study hours
# Symmetrical or skewed? Which pair of summaries would you report?
sh = first_sem["study_hours"]
mean_sh = sh.mean()
median_sh = sh.______()
sd_sh = sh.______()
iqr_sh = sh.quantile(0.75) - sh.quantile(______)

print(f"Mean: {mean_sh:.2f}, Median: {median_sh:.2f}")
print(f"SD: {sd_sh:.2f}, IQR: {iqr_sh:.2f}")


# Exercise 2: Is wellbeing normal? A Q-Q plot.
fig, ax = plt.subplots(figsize=(6, 4))
sm.______(first_sem["wellbeing"].dropna(), line="s", ax=ax)
ax.set_title("Q-Q Plot for First-Semester Wellbeing")
plt.tight_layout()
plt.show()


# Exercise 3: Unusually high study hours (Tukey's box plot rule)
x = first_sem["study_hours"]
q1 = x.quantile(0.25)
q3 = x.quantile(0.75)
iqr = q3 - q1
fence = q3 + ______ * iqr
print(f"Upper fence: {fence:.1f} hours")

outliers = first_sem.query("study_hours > @fence")[
    ["student_id", "study_hours", "sleep_hours", "gpa", "wellbeing", "study_mode"]
]
print(f"Number of outliers: {len(outliers)}")
print(outliers.head())


# Exercise 4: Sleep of students who left
# Do they differ in sleep as they did in wellbeing?
sem3_students = set(semesters.query("semester == 3")["student_id"])
left_ids = set(students["student_id"]) - sem3_students

first_sem["left_study"] = first_sem["student_id"].______(left_ids)
attrition_summary = first_sem.groupby("left_study").agg(
    mean_sleep=("sleep_hours", "mean"),
    mean_wellbeing=("wellbeing", "mean"),
    students=("student_id", "count")
).round(2)
print(attrition_summary)


# Exercise 5: Supervisor support and academic satisfaction
# The correlation, classified with Cohen's guidelines.
scores = pd.DataFrame({
    "student_id": questionnaire["student_id"],
    "support": questionnaire.filter(like="support_").______(axis=1),
    "satisfaction": questionnaire.filter(like="satisfaction_").______(axis=1),
})
r_value = scores["support"].______(scores["satisfaction"])
print(f"Pearson r: {r_value:.2f}")


# Exercise 6: A summary for every variable
# For each variable in students, choose the summary you would report, and
# justify each choice in one sentence. (See solutions.py for discussion).


# ==============================================================================
# B. GO FURTHER
# ==============================================================================

# Exercise 7: The standard deviation by hand
# Compute deviations, squared deviations, and unbiased sample variance
sleep_five = pd.Series([4.0, 6.0, 7.0, 8.0, 10.0])
deviations = sleep_five - sleep_five.mean()
print("Deviations:", deviations.values)

squared_devs = deviations ** 2
# Divide by (n - 1) for sample variance (Bessel's correction)
variance = squared_devs.sum() / (len(sleep_five) - ______)
sd_manual = np.______(variance)
sd_pandas = sleep_five.std()
print(f"Manual SD: {sd_manual:.4f}, Pandas SD: {sd_pandas:.4f}")


# Exercise 8: Mean and median of age, with a histogram
mean_age = students["age"].mean()
median_age = students["age"].______()
skew_age = students["age"].______()

print(f"Age Mean: {mean_age:.1f}, Median: {median_age:.1f}, Skewness: {skew_age:.2f}")

fig, ax = plt.subplots(figsize=(6, 3.5))
sns.histplot(students["age"].dropna(), bins=20, color="#1d588c", ax=ax)
ax.axvline(mean_age, color="red", linestyle="-", label="Mean")
ax.axvline(median_age, color="orange", linestyle="--", label="Median")
ax.set_xlabel("Age (years)")
ax.legend()
plt.tight_layout()
plt.show()


# Exercise 9: Missing values in every column of semesters, grouped by semester
missing_by_sem = semesters.groupby("semester").apply(
    lambda df: df.______.sum()
)
print(missing_by_sem)


# Exercise 10: When one mean misleads (bimodal distribution)
# In seaborn or data2thesis, load geyser/faithful dataset
from data2thesis import faithful

mean_wait = faithful["waiting"].mean()
print(f"Overall mean waiting time: {mean_wait:.1f} minutes")

# Split into short and long waits using a cutoff of 67 minutes
faithful_grouped = faithful.copy()
faithful_grouped["wait_type"] = np.where(faithful_grouped["waiting"] < ______, "short", "long")
print(faithful_grouped.groupby("wait_type")["waiting"].agg(["count", "mean"]))


# ==============================================================================
# C. CHECK YOUR UNDERSTANDING
# Answer in your own words, then compare with solutions.py.
# ==============================================================================

# 1. Which summary suits an ordinal variable, such as the five answers to a
#    question about money worries?
# 2. Sleep has a mean of 6.5 hours and an SD of 1.1 hours. What does the SD
#    mean in words?
# 3. Why is an outlier not simply deleted?
# 4. What is the difference between data missing at random and data missing
#    not at random?
# 5. Two variables have a correlation of 0. Does that mean they are unrelated?


# ==============================================================================
# D. DO IT YOURSELF
# Open tasks: no starter code and no hints. Write your code below.
# ==============================================================================

# Task 1: A complete "Table 1" describing the sample (percentages for categories,
# mean and SD for normal numeric, median and IQR for skewed, with valid N and missing).

# Task 2: Describe supervisor_meetings in the first semester: centre, spread,
# shape, and unusual values. Which summaries would you report?

# Task 3: Compare students sleeping < 6 hours vs >= 7 hours on first-semester GPA
# and wellbeing. Report mean, SD, and median for both groups.
