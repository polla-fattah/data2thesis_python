# FROM DATA TO THESIS: Using Python for Non-Technical
# Playground, Chapter 8: Solutions
#
# One possible solution for each exercise in parts A and B, and model answers
# for part C. Part D has no solutions: the tasks are open, and there are many
# good ways to answer them.

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

# Exercise 1: F = 2.02, p = 0.09, eta squared 0.013: not significant (p > .05),
# so no post-hoc Tukey test is warranted.
wellbeing_anova = smf.ols("wellbeing ~ C(faculty)", data=study).fit()
aov_table = sm.stats.anova_lm(wellbeing_anova, typ=1)
print("ANOVA table for wellbeing across faculties:\n", aov_table)

ss_between = aov_table.loc["C(faculty)", "sum_sq"]
ss_total = aov_table["sum_sq"].sum()
eta_sq = ss_between / ss_total
print(f"Eta squared: {eta_sq:.4f}")


# Exercise 2: slope 5.3 points per hour of sleep; R-squared 0.21
wb_simple = smf.ols("wellbeing ~ sleep_hours", data=study).fit()
print(wb_simple.summary())


# Exercise 3: the slope of sleep falls from 5.3 to 3.9 (stress and support share
# explanatory variance); R-squared doubles, from 0.21 to 0.43
wb_simple = smf.ols("wellbeing ~ sleep_hours", data=study).fit()
wb_multiple = smf.ols("wellbeing ~ sleep_hours + stress + support", data=study).fit()

print("Simple slope for sleep:  ", wb_simple.params["sleep_hours"])
print("Multiple slope for sleep:", wb_multiple.params["sleep_hours"])
print("Simple R-squared:        ", wb_simple.rsquared)
print("Multiple R-squared:      ", wb_multiple.rsquared)


# Exercise 4: reference Full-time; part-time students about 3.0 points lower,
# holding the rest constant. With Part-time as reference: Full-time is +3.0.
wb_mode = smf.ols("wellbeing ~ sleep_hours + stress + support + C(study_mode)", data=study).fit()
print(wb_mode.summary().tables[1])

wb_mode_ref = smf.ols(
    "wellbeing ~ sleep_hours + stress + support + C(study_mode, Treatment(reference='Part-time'))",
    data=study
).fit()
print(wb_mode_ref.summary().tables[1])


# Exercise 5: odds ratio 3.7 (95% CI 2.5 to 5.4); predicted probabilities 3%
# (burnout 2) and 31% (burnout 4)
q_burnout = questionnaire.filter(like="burnout_").mean(axis=1)
study_b = study.copy()
study_b["burnout"] = q_burnout
study_b["dropout"] = (study_b["considering_dropout"] == "Yes").astype(int)

burnout_model = smf.logit("dropout ~ burnout", data=study_b).fit(disp=False)
print("Odds ratio:\n", np.exp(burnout_model.params))
print("95% CI of Odds Ratio:\n", np.exp(burnout_model.conf_int()))

new_cases = pd.DataFrame({"burnout": [2.0, 4.0]})
probs = burnout_model.predict(new_cases)
print("Predicted probabilities for burnout 2 and 4:", probs.round(3).tolist())


# Exercise 6 (model answer): fast-food outlets and heart disease, with poverty
# as a possible common cause. Regress disease on outlets and income: if the
# outlet coefficient stays clearly above zero, the direct explanation survives;
# if it shrinks towards zero, poverty was confounding. Unmeasured confounders
# remain possible.


# ==============================================================================
# B. GO FURTHER
# ==============================================================================

# Exercise 7: SS between 1.31, SS within 0.55, F = 10.7, as anova_lm reports
group_scores = pd.DataFrame({
    "group": ["A"] * 4 + ["B"] * 4 + ["C"] * 4,
    "stress": [2.5, 3.0, 2.8, 3.1,   3.4, 3.8, 3.5, 3.9,   2.9, 3.3, 3.0, 3.4]
})
group_means = group_scores.groupby("group")["stress"].transform("mean")
grand_mean = group_scores["stress"].mean()

ss_between = ((group_means - grand_mean) ** 2).sum()
ss_within = ((group_scores["stress"] - group_means) ** 2).sum()

F_value = (ss_between / 2) / (ss_within / 9)
print("Manual F value:", F_value)

fit_group = smf.ols("stress ~ C(group)", data=group_scores).fit()
print(sm.stats.anova_lm(fit_group, typ=1))


# Exercise 8: the line and the band averages agree within a point where most
# students are (6 and 7 hours); tiny groups at the edges bounce around it
bands = (
    study.dropna(subset=["sleep_hours"])
    .assign(sleep_band=lambda d: d["sleep_hours"].round())
    .groupby("sleep_band")
    .agg(students=("student_id", "count"), mean_wellbeing=("wellbeing", "mean"))
    .reset_index()
    .sort_values("sleep_band")
)

wb_line = smf.ols("wellbeing ~ sleep_hours", data=study).fit()
bands["line_prediction"] = wb_line.predict(pd.DataFrame({"sleep_hours": bands["sleep_band"]}))
print(bands)


# Exercise 9: overall, 45% of men and 30% of women admitted; within
# departments, women's rate is higher in four of six. The department is a
# confounder: women applied mostly to departments that admitted few applicants.
admissions = pd.read_csv("ucbadmissions.csv")
print(admissions.head())

admit_admitted = admissions.query("Admit == 'Admitted'")
overall = (
    admissions.groupby("Gender")["Freq"].sum().rename("total")
    .to_frame()
    .join(admit_admitted.groupby("Gender")["Freq"].sum().rename("admitted"))
)
overall["rate"] = overall["admitted"] / overall["total"]
print("Overall admission rates:\n", overall)

dept_total = admissions.groupby(["Dept", "Gender"])["Freq"].sum().rename("total")
dept_admit = admit_admitted.groupby(["Dept", "Gender"])["Freq"].sum().rename("admitted")
dept = dept_total.to_frame().join(dept_admit).fillna(0)
dept["rate"] = dept["admitted"] / dept["total"]
print("Admission rates by department:\n", dept)


# Exercise 10: the straight line's residuals form an arch; with the squared
# term they scatter evenly. R-squared 0.004 vs 0.036; the curve peaks at about
# 32 hours.
straight = smf.ols("gpa ~ study_hours", data=study).fit()
curved = smf.ols("gpa ~ study_hours + np.power(study_hours, 2)", data=study).fit()

print(f"Straight R-squared: {straight.rsquared:.4f}")
print(f"Curved R-squared:   {curved.rsquared:.4f}")


# ==============================================================================
# C. CHECK YOUR UNDERSTANDING: model answers
# ==============================================================================

# 1. Variation between group averages against variation within groups, each per
#    degree of freedom. Near 1: no more than chance; large: more.
# 2. The difference in the outcome between cases that differ by one unit in
#    that predictor but have the same values of the other predictors in the
#    model. A statistical comparison, limited to measured predictors.
# 3. A variable that affects both the predictor and the outcome, creating or
#    distorting an association (sleep, for caffeine and GPA).
# 4. The spread is not constant: coefficients are unbiased, but standard
#    errors, p-values, and intervals are unreliable. Transform the outcome or
#    use robust standard errors.
# 5. Odds are p / (1 - p). Doubling small odds nearly doubles the probability,
#    but odds of 1 (50%) doubled give 67%. Report predicted probabilities too.


# ==============================================================================
# D. DO IT YOURSELF
# No solutions: these tasks are open. Compare your approach with the methods of
# Chapter 8, and discuss your choices with a fellow student or your supervisor.
# ==============================================================================
