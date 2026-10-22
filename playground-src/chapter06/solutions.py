# FROM DATA TO THESIS: Using Python for Non-Technical
# Playground, Chapter 6: Descriptive Statistics and Exploratory Data Analysis
#
# Complete solutions with detailed explanations.

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
sh = first_sem["study_hours"]
mean_sh = sh.mean()
median_sh = sh.median()
sd_sh = sh.std()
iqr_sh = sh.quantile(0.75) - sh.quantile(0.25)

print(f"Mean: {mean_sh:.2f}, Median: {median_sh:.2f}")
print(f"SD: {sd_sh:.2f}, IQR: {iqr_sh:.2f}")
# Explanation:
# The mean (27.6 hours) is slightly higher than the median (26.0 hours).
# The distribution has mild positive skewness (skew ≈ 0.65). Both (mean, SD)
# and (median, IQR) are informative; because the skew is mild, reporting mean (27.6)
# and SD (13.1) is conventional, but median (26.0) and IQR (19.0) should be included
# if communicating to an applied audience sensitive to heavy study loads.


# Exercise 2: Is wellbeing normal? A Q-Q plot.
fig, ax = plt.subplots(figsize=(6, 4))
sm.qqplot(first_sem["wellbeing"].dropna(), line="s", ax=ax, markerfacecolor="#1d588c", alpha=0.5)
ax.set_title("Q-Q Plot for First-Semester Wellbeing")
plt.tight_layout()
plt.show()
# Explanation:
# The points fall closely along the straight standardized reference line.
# Aside from minor variation at the very tails, first-semester wellbeing
# satisfies the assumption of normality well.


# Exercise 3: Unusually high study hours (Tukey's box plot rule)
x = first_sem["study_hours"]
q1 = x.quantile(0.25)
q3 = x.quantile(0.75)
iqr = q3 - q1
fence = q3 + 1.5 * iqr
print(f"Upper fence: {fence:.1f} hours")

outliers = first_sem.query("study_hours > @fence")[
    ["student_id", "study_hours", "sleep_hours", "gpa", "wellbeing", "study_mode"]
]
print(f"Number of outliers: {len(outliers)}")
print(outliers)
# Explanation:
# The upper fence is around 64.5 hours per week. A handful of students report
# studying 65-75 hours per week. These are heavy workloads, but plausible for
# intense thesis phases or full-time students with demanding deadlines.


# Exercise 4: Sleep of students who left
sem3_students = set(semesters.query("semester == 3")["student_id"])
left_ids = set(students["student_id"]) - sem3_students

first_sem["left_study"] = first_sem["student_id"].isin(left_ids)
attrition_summary = first_sem.groupby("left_study").agg(
    mean_sleep=("sleep_hours", "mean"),
    mean_wellbeing=("wellbeing", "mean"),
    students=("student_id", "count")
).round(2)
print(attrition_summary)
# Explanation:
# Students who left averaged 6.13 hours of sleep versus 6.44 hours for those who stayed.
# While their sleep deficit was modest (~19 minutes), their wellbeing deficit was
# severe (45.3 vs 53.6), indicating that attrition was driven by broader distress.


# Exercise 5: Supervisor support and academic satisfaction
scores = pd.DataFrame({
    "student_id": questionnaire["student_id"],
    "support": questionnaire.filter(like="support_").mean(axis=1),
    "satisfaction": questionnaire.filter(like="satisfaction_").mean(axis=1),
})
r_value = scores["support"].corr(scores["satisfaction"])
print(f"Pearson r between Support and Satisfaction: {r_value:.2f}")
# Explanation:
# The correlation is approximately r = 0.48, which Cohen (1988) defines as a
# large positive effect size. However, this cross-sectional association does not prove
# that supervisor support causes satisfaction. A third variable (such as general student
# morale, department resources, or optimistic disposition) could influence both.


# Exercise 6: A summary for every variable
# - student_id: identifier (no summary)
# - gender, nationality, faculty, programme, study_mode, employment, workshop:
#   Nominal variables -> report frequency counts and percentages (and mode).
# - financial_worry:
#   Ordinal variable -> report median, IQR, and percentage in each category.
# - age:
#   Continuous right-skewed variable -> report median and IQR (or mean and SD with skew note).
# - workshop_sessions:
#   Discrete count -> report median/IQR (or mean/SD among invited students).
# - considering_dropout:
#   Binary nominal -> report percentage "Yes" (and sample size).


# ==============================================================================
# B. GO FURTHER
# ==============================================================================

# Exercise 7: The standard deviation by hand
sleep_five = pd.Series([4.0, 6.0, 7.0, 8.0, 10.0])
deviations = sleep_five - sleep_five.mean()
print("Deviations:", deviations.values)

squared_devs = deviations ** 2
variance = squared_devs.sum() / (len(sleep_five) - 1)
sd_manual = np.sqrt(variance)
sd_pandas = sleep_five.std()
print(f"Manual SD: {sd_manual:.4f}, Pandas SD: {sd_pandas:.4f}")
assert np.isclose(sd_manual, sd_pandas)


# Exercise 8: Mean and median of age, with a histogram
mean_age = students["age"].mean()
median_age = students["age"].median()
skew_age = students["age"].skew()

print(f"Age Mean: {mean_age:.1f}, Median: {median_age:.1f}, Skewness: {skew_age:.2f}")

fig, ax = plt.subplots(figsize=(6, 3.5))
sns.histplot(students["age"].dropna(), bins=20, color="#1d588c", ax=ax)
ax.axvline(mean_age, color="red", linestyle="-", linewidth=2, label=f"Mean ({mean_age:.1f})")
ax.axvline(median_age, color="orange", linestyle="--", linewidth=2, label=f"Median ({median_age:.1f})")
ax.set_xlabel("Age (years)")
ax.legend()
sns.despine()
plt.tight_layout()
plt.show()


# Exercise 9: Missing values in every column of semesters, grouped by semester
missing_by_sem = semesters.groupby("semester").apply(
    lambda df: df.isna().sum()
)
print("Missing counts by semester:")
print(missing_by_sem)


# Exercise 10: When one mean misleads (bimodal distribution)
from data2thesis import faithful

mean_wait = faithful["waiting"].mean()
print(f"Overall mean waiting time: {mean_wait:.1f} minutes")

faithful_grouped = faithful.copy()
faithful_grouped["wait_type"] = np.where(faithful_grouped["waiting"] < 67, "short", "long")
print(faithful_grouped.groupby("wait_type")["waiting"].agg(["count", "mean", "std"]))
# Explanation:
# The overall mean (~70.9 min) falls in the valley between the two modes.
# Splitting into short waits (~54.5 min) and long waits (~80.0 min) accurately describes
# the two underlying physical regimes of the geyser.


# ==============================================================================
# C. CHECK YOUR UNDERSTANDING - ANSWERS
# ==============================================================================

# 1. An ordinal variable has unequal intervals between categories. Report the
#    median and the interquartile range (IQR), alongside category percentage distributions.
#
# 2. A standard deviation of 1.1 hours means that individual students' sleep durations
#    typically deviate from the sample mean (6.5 hours) by roughly 1.1 hours.
#    Under normality, ~68% of students sleep between 5.4 and 7.6 hours.
#
# 3. An outlier represents a genuine observation from the target population.
#    Deleting it artificially reduces natural variance, biases estimates, and constitutes
#    poor scientific practice. Instead, verify data-entry validity, report the outlier,
#    and use robust statistics (median, IQR) or sensitivity analyses.
#
# 4. Missing at Random (MAR) means missingness is systematically related to observed
#    covariates (which can be statistically adjusted for). Missing Not at Random (MNAR)
#    means missingness depends on the unobserved value itself (e.g. distressed students
#    refusing to disclose financial distress), creating unavoidable sample bias.
#
# 5. No. Pearson's r = 0 indicates the absence of a straight-line (linear) relationship.
#    A strong non-linear or U-shaped relationship can exist while yielding r ≈ 0.


# ==============================================================================
# D. DO IT YOURSELF - SAMPLE IMPLEMENTATION
# ==============================================================================

# Task 1: Complete Table 1 function
def create_table_1(df, vars_list):
    records = []
    for var in vars_list:
        s = df[var].dropna()
        records.append({
            "Variable": var,
            "Valid N": len(s),
            "Mean": s.mean(),
            "SD": s.std(),
            "Median": s.median(),
            "IQR": s.quantile(0.75) - s.quantile(0.25),
            "Missing": df[var].isna().sum()
        })
    return pd.DataFrame(records).set_index("Variable").round(2)

print("\nTask 1 Table:")
print(create_table_1(first_sem, ["sleep_hours", "study_hours", "caffeine_mg", "gpa", "wellbeing"]))
