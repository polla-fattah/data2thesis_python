# FROM DATA TO THESIS: Using Python for Non-Technical
# Playground, Chapter 8: ANOVA and Regression
#
# Four parts, as on the playground page:
#   A. Practise the chapter       the book's exercises, with blanks (______) to fill
#   B. Go further                 new exercises beyond the book
#   C. Check your understanding   short questions; answers in solutions.py
#   D. Do it yourself             open tasks with no starter code and no answers
#
# Try each exercise yourself before you look at solutions.py.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from patsy.contrasts import Treatment

students = pd.read_csv("students.csv")
students["employment"] = students["employment"].fillna("None")
semesters = pd.read_csv("semesters.csv")
questionnaire = pd.read_csv("questionnaire.csv")

q = questionnaire.copy()
q["stress_4"] = 6 - q["stress_4"]
scores = pd.DataFrame({
    "student_id": q["student_id"],
    "stress": q.filter(like="stress_").mean(axis=1),
    "support": q.filter(like="support_").mean(axis=1),
})

study = (
    students
    .merge(scores, on="student_id")
    .merge(semesters.query("semester == 1"), on="student_id")
)


# ==============================================================================
# A. PRACTISE THE CHAPTER
# ==============================================================================

# Exercise 1: Wellbeing across faculties
# One-way ANOVA and eta squared; Tukey's test only if the ANOVA is significant.
wellbeing_anova = smf.______( "wellbeing ~ C(faculty)", data=study).fit()
aov_table = sm.stats.anova_lm(wellbeing_anova, typ=1)
print(aov_table)

ss_between = aov_table.loc["C(faculty)", "sum_sq"]
ss_total = aov_table["sum_sq"].______()
eta_sq = ss_between / ss_total
print(f"Eta squared: {eta_sq:.4f}")


# Exercise 2: Wellbeing and sleep
# Fit simple regression; interpret the slope and R-squared.
wb_simple = smf.ols("wellbeing ~ sleep_hours", data=study).______()
print(wb_simple.summary())


# Exercise 3: Adding stress and support
# What happens to the slope of sleep, and to R-squared?
wb_simple = smf.ols("wellbeing ~ sleep_hours", data=study).fit()
wb_multiple = smf.ols("wellbeing ~ sleep_hours + stress + support", data=study).fit()

print("Simple slope for sleep:  ", wb_simple.params["sleep_hours"])
print("Multiple slope for sleep:", wb_multiple.______["sleep_hours"])
print("Simple R-squared:        ", wb_simple.rsquared)
print("Multiple R-squared:      ", wb_multiple.rsquared)


# Exercise 4: A categorical predictor
# Name the reference category and explain its coefficient; then make part-time
# the reference category.
wb_mode = smf.ols("wellbeing ~ sleep_hours + stress + support + C(study_mode)", data=study).fit()
print(wb_mode.summary().tables[1])

wb_mode_ref = smf.ols(
    "wellbeing ~ sleep_hours + stress + support + C(study_mode, Treatment(reference=______))",
    data=study
).fit()
print(wb_mode_ref.summary().tables[1])


# Exercise 5: Burnout and dropout
# Odds ratio, and predicted probabilities for burnout scores of 2 and 4.
q_burnout = questionnaire.filter(like="burnout_").mean(axis=1)
study_b = study.copy()
study_b["burnout"] = q_burnout
study_b["dropout"] = (study_b["considering_dropout"] == "Yes").astype(int)

burnout_model = smf.logit("dropout ~ burnout", data=study_b).fit()
print("Odds ratio:\n", np.exp(burnout_model.params))
print("95% CI of Odds Ratio:\n", np.exp(burnout_model.conf_int()))

new_cases = pd.DataFrame({"burnout": [2.0, 4.0]})
probs = burnout_model.predict(______)
print("Predicted probabilities:", probs.round(3).tolist())


# Exercise 6: A confounder in your own field
# Draw a diagram of a confounder that might explain an association in your field,
# and describe how a regression could separate the two explanations.


# ==============================================================================
# B. GO FURTHER
# ==============================================================================

# Exercise 7: F by hand, compared with anova_lm()
group_scores = pd.DataFrame({
    "group": ["A"] * 4 + ["B"] * 4 + ["C"] * 4,
    "stress": [2.5, 3.0, 2.8, 3.1,   3.4, 3.8, 3.5, 3.9,   2.9, 3.3, 3.0, 3.4]
})
group_means = group_scores.groupby("group")["stress"].transform("mean")
grand_mean = group_scores["stress"].mean()

ss_between = ((group_means - grand_mean) ** 2).sum()
ss_within = ((group_scores["stress"] - group_means) ** 2).sum()

# df_between = k - 1 = 2; df_within = N - k = 12 - 3 = 9
F_value = (ss_between / ______) / (ss_within / ______)
print("Manual F value:", F_value)

fit_group = smf.ols("stress ~ C(group)", data=group_scores).fit()
print(sm.stats.anova_lm(fit_group, typ=1))


# Exercise 8: Regression as conditional means
# Average wellbeing per whole hour of sleep, beside the line's predictions.
bands = (
    study.dropna(subset=["sleep_hours"])
    .assign(sleep_band=lambda d: d["sleep_hours"].round())
    .groupby("sleep_band")
    .agg(students=("student_id", "count"), mean_wellbeing=("wellbeing", "mean"))
    .reset_index()
    .sort_values("sleep_band")
)

wb_line = smf.ols("wellbeing ~ sleep_hours", data=study).fit()
bands["line_prediction"] = wb_line.predict(pd.DataFrame({"sleep_hours": bands[______]}))
print(bands)


# Exercise 9: Simpson's paradox
# Admission rates of men and women at Berkeley in 1973, overall and by department.
admissions = pd.read_csv("ucbadmissions.csv")
print(admissions.head())

# Overall admission rate by Gender
admit_admitted = admissions.query("Admit == 'Admitted'")
overall = (
    admissions.groupby("Gender")["Freq"].sum().rename("total")
    .to_frame()
    .join(admit_admitted.groupby("Gender")["Freq"].sum().rename("admitted"))
)
overall["rate"] = overall["admitted"] / overall[______]
print("Overall admission rates:\n", overall)

# Admission rate by Department and Gender
dept_total = admissions.groupby(["Dept", "Gender"])["Freq"].sum().rename("total")
dept_admit = admit_admitted.groupby(["Dept", "Gender"])["Freq"].sum().rename("admitted")
dept = dept_total.to_frame().join(dept_admit).fillna(0)
dept["rate"] = dept["admitted"] / dept["total"]
print("Admission rates by department:\n", dept)


# Exercise 10: A missed curve in the residuals
straight = smf.ols("gpa ~ study_hours", data=study).fit()
curved = smf.ols("gpa ~ study_hours + np.power(study_hours, ______)", data=study).fit()

print(f"Straight R-squared: {straight.rsquared:.4f}")
print(f"Curved R-squared:   {curved.rsquared:.4f}")


# ==============================================================================
# C. CHECK YOUR UNDERSTANDING
# Answer in your own words, then compare with the answers in solutions.py.
# ==============================================================================

# 1. What does the F statistic of an ANOVA compare?
# 2. In a multiple regression, what does "holding the other predictors
#    constant" mean?
# 3. What is a confounder?
# 4. A residual plot shows a funnel. What does it mean?
# 5. An odds ratio of 2 does not mean that the probability doubles. Why not?


# ==============================================================================
# D. DO IT YOURSELF
# Open tasks: no starter code, no hints, and no answers. Write your own code
# under each task, as you would for a thesis.
# ==============================================================================

# Task 1: A regression model for first-semester wellbeing with predictors of
# your choice, justified by a research question; check the residual plot, and
# write the reporting paragraph with every number calculated by code.



# Task 2: Does the effect of support on wellbeing differ between full-time and
# part-time students? Centre support, fit an interaction, interpret it, and
# draw an interaction plot.



# Task 3: A logistic regression for another yes-or-no variable (such as
# lives_away) with two or three justified predictors: odds ratios with
# confidence intervals, and predicted probabilities for two contrasting
# students.



# Task 4: trees: predict Volume from Girth and Height, check whether a straight
# line is adequate, and explain what you would change if it is not.
