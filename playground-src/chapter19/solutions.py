# FROM DATA TO THESIS: Using Python for Non-Technical
# Playground, Chapter 19: Solutions
#
# One possible solution for the Python exercises in parts A and B, and model answers
# for part C. The project tasks are in exercises.txt, with hints and answers at
# its end. Part D has no solutions: the tasks are open.

import os
from pathlib import Path
import pandas as pd
import numpy as np
import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import pairwise_tukeyhsd

ROOT = Path(__file__).resolve().parent

# Run cleaning script if data/ does not exist yet:
if not (ROOT / "data" / "students.csv").exists():
    import subprocess
    subprocess.run(["python", str(ROOT / "scripts" / "01_clean_data.py")], check=True)

students = pd.read_csv(ROOT / "data" / "students.csv")
semesters = pd.read_csv(ROOT / "data" / "semesters.csv")
questionnaire = pd.read_csv(ROOT / "data" / "questionnaire.csv")

scores = questionnaire.copy()
scores["stress_4"] = 6 - scores["stress_4"]
scores["stress"] = scores.filter(like="stress_").mean(axis=1)
scores["support"] = scores.filter(like="support_").mean(axis=1)
scores = scores[["student_id", "stress", "support"]]

study = students.merge(scores, on="student_id").merge(semesters.query("semester == 1"), on="student_id")

def mean_sd(x):
    return f"{x.mean():.1f} ({x.std(ddof=1):.1f})"

def percent(x):
    return f"{100 * x.mean():.0f}%"

def format_p(p):
    return "p < .001" if p < 0.001 else f"p = {p:.3f}".replace(" 0.", " .")

def describe(d):
    return pd.Series({
        "Students": str(len(d)),
        "Age, mean (SD)": mean_sd(d["age"]),
        "Women": percent(d["gender"] == "Female"),
        "Part-time": percent(d["study_mode"] == "Part-time"),
        "Stress (1-5), mean (SD)": mean_sd(d["stress"]),
        "Support (1-5), mean (SD)": mean_sd(d["support"]),
        "Wellbeing in semester 1, mean (SD)": mean_sd(d["wellbeing"]),
        "Considered dropping out": percent(d["considering_dropout"] == "Yes")
    })


# ==============================================================================
# A. PRACTISE THE CHAPTER
# ==============================================================================

# Exercise 1: see exercises.txt (run the project; change a cleaning rule)


# Exercise 2: Students with children in Table 1
def describe_more(d):
    s = describe(d)
    s["Has children"] = percent(d["has_children"] == "Yes")
    return s

t1_more = pd.DataFrame({
    "Characteristic": describe_more(study).index,
    "Master's": describe_more(study[study["programme"] == "Master's"]).values,
    "PhD": describe_more(study[study["programme"] == "PhD"]).values,
    "All": describe_more(study).values
})
print("Table 1 with children row:")
print(t1_more.to_markdown(index=False))


# Exercise 3: A sentence for the effect of support on GPA
gpa_model = smf.ols("gpa ~ sleep_hours + study_hours + stress + support", data=study).fit()
estimate = gpa_model.params["support"]
ci_low = gpa_model.conf_int().loc["support", 0]
ci_high = gpa_model.conf_int().loc["support", 1]
p_val = gpa_model.pvalues["support"]

reporting_sentence = (
    f"Each one-point increase in supervisor support was associated with a GPA "
    f"{estimate:.2f} points higher (95% CI {ci_low:.2f} to {ci_high:.2f}, {format_p(p_val)}), "
    f"holding sleep, study hours, and stress constant."
)
print("\nReporting sentence:")
print(reporting_sentence)


# Exercise 4: see exercises.txt (a third panel for the thesis figure)


# Exercise 5: A method for a research question from your own field
# Model answer:
# 1. State the objective: e.g., "Determine whether regular physical activity reduces perceived burnout among doctoral students."
# 2. Identify the outcome: continuous numerical score (burnout inventory, 1 to 5).
# 3. Consider data hierarchy: single-timepoint survey (independent) vs. multi-semester tracking (repeated measures).
# 4. Map to method: multiple linear regression for cross-sectional; mixed-effects growth modeling for longitudinal data.


# Exercise 6: The chain of reasoning for RQ2 (sleep less than 7 hours?)
sleep_clean = study["sleep_hours"].dropna()
sleep_test = stats.ttest_1samp(sleep_clean, popmean=7, alternative="less")
sleep_mean = sleep_clean.mean()
sem_sleep = stats.sem(sleep_clean)
ci_sleep = stats.t.interval(0.95, df=len(sleep_clean)-1, loc=sleep_mean, scale=sem_sleep)

print(f"\nRQ2 Sleep Test: mean = {sleep_mean:.2f}, 95% CI = [{ci_sleep[0]:.2f}, {ci_sleep[1]:.2f}], p = {sleep_test.pvalue:.4f}, n = {len(sleep_clean)}")
# Chain of reasoning:
# - Question: Do students sleep less than the recommended 7 hours?
# - Hypothesis: Average sleep duration is significantly below 7.0 hours.
# - Design: Observational, baseline semester 1 survey.
# - Variables: Self-reported sleep hours (continuous).
# - Analysis: One-tailed one-sample t-test against mu = 7.0.
# - Result: Mean sleep was 6.48 hours (95% CI [6.40, 6.57], p < .001).
# - Conclusion: Students sleep approximately half an hour less than recommended; reject H0.
# - Limitation: Self-reported metric; single institution; unverified clinical sleep architecture.


# ==============================================================================
# B. GO FURTHER
# ==============================================================================

# Exercise 7: A helper for confidence intervals, used in three sentences
def format_ci(estimate, low, high, digits=2):
    return f"{estimate:.{digits}f} (95% CI {low:.{digits}f} to {high:.{digits}f})"

ci_sleep_gpa = gpa_model.conf_int().loc["sleep_hours"]
print("Sleep & GPA:", format_ci(gpa_model.params["sleep_hours"], ci_sleep_gpa[0], ci_sleep_gpa[1]))

mode_ft = study.query("study_mode == 'Full-time'")["wellbeing"].dropna()
mode_pt = study.query("study_mode == 'Part-time'")["wellbeing"].dropna()
diff_mode = mode_ft.mean() - mode_pt.mean()
ci_mode = stats.t.interval(0.95, df=len(mode_ft)+len(mode_pt)-2, loc=diff_mode,
                           scale=np.sqrt(mode_ft.var(ddof=1)/len(mode_ft) + mode_pt.var(ddof=1)/len(mode_pt)))
print("Study mode difference:", format_ci(diff_mode, ci_mode[0], ci_mode[1], digits=1))

dropout_model = smf.logit("I(considering_dropout == 'Yes') ~ stress + support + financial_worry + C(employment) + C(study_mode)", data=study).fit(disp=False)
or_stress = np.exp(dropout_model.params["stress"])
ci_or_stress = np.exp(dropout_model.conf_int().loc["stress"])
print("Dropout odds ratio:", format_ci(or_stress, ci_or_stress[0], ci_or_stress[1], digits=1))


# Exercise 8: The chain of reasoning for RQ4 (stress and faculties)
stress_model = smf.ols("stress ~ C(faculty)", data=study).fit()
anova_tab = anova_lm(stress_model, typ=2)
print("\nStress ANOVA:")
print(anova_tab)

eta_sq = anova_tab.loc["C(faculty)", "sum_sq"] / anova_tab["sum_sq"].sum()
print(f"Eta squared: {eta_sq:.3f}")

tukey = pairwise_tukeyhsd(study["stress"], study["faculty"], alpha=0.05)
print(tukey)


# Exercise 9: Table 1 by faculty
faculties = sorted(study["faculty"].unique())
t1_fac = pd.DataFrame({"Characteristic": describe(study).index})
for f in faculties:
    t1_fac[f] = describe(study[study["faculty"] == f]).values
print("\nTable 1 across all 5 faculties:")
print(t1_fac.to_markdown(index=False))


# Exercise 10: Choosing methods for five research questions
# 1. Nurse weekly hours (describe): Mean and 95% bootstrap/parametric CI, histogram (Ch 4, 6).
# 2. Hours and burnout, controlling for age and ward (explain): Multiple linear regression with ward fixed or random effects (Ch 8, 10).
# 3. Longitudinal quarterly burnout tracking: Mixed-effects random slope growth model (Ch 10).
# 4. Predicting nurse attrition within 12 months: Regularized classification (logistic regression, gradient boosting) with cross-validated ROC-AUC (Ch 11, 12, 13).
# 5. Nurse shift profiles: Unsupervised clustering (K-Means, GMM, or hierarchical) on shift metrics (Ch 9, 14).


# ==============================================================================
# C. CHECK YOUR UNDERSTANDING: model answers
# ==============================================================================

# 1. Why should every number in a thesis be traced to code?
#    So that every result can be independently audited, audited by examiners, updated
#    instantly when raw data changes, and protected against human copy-paste errors.
#
# 2. What is the difference between a result and a conclusion?
#    A result is the direct numerical output of a statistical procedure (e.g. p = .02, beta = 0.11).
#    A conclusion interprets what that number means conceptually in relation to the research
#    question, conditioned on the research design, construct validity, and methodological limits.
#
# 3. Why is the workshop conclusion the only causal one in the chapter?
#    Because workshop invitation was randomized by the researcher, ensuring exchangeability
#    between groups prior to treatment. GPA, sleep, and dropout were observed without experimental
#    random assignment, leaving room for unmeasured confounding.
#
# 4. What is a limitations section for?
#    To transparently delineate the boundaries of inference: potential confounders, measurement
#    error, sample generalizability constraints, and attrition biases.
#
# 5. What are reporting standards such as JARS, CONSORT, and STROBE for?
#    They establish comprehensive checklists of essential methodological, statistical,
#    and ethical disclosures required to evaluate the validity, replicability, and clinical/scientific
#    relevance of research studies.


# ==============================================================================
# D. DO IT YOURSELF
# Open tasks: no starter code, no hints, and no answers.
# ==============================================================================
