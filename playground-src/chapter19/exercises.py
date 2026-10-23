# FROM DATA TO THESIS: Using Python for Non-Technical
# Playground, Chapter 19: Putting It All Together
#
# This script holds the Python parts of the playground page. The project tasks
# (running the scripts, changing a cleaning rule, the thesis figure) are in
# exercises.txt.
#   A. Practise the chapter       the book's exercises, with blanks (______) to fill
#   B. Go further                 new exercises beyond the book
#   C. Check your understanding   short questions; answers in solutions.py
#   D. Do it yourself             open tasks with no starter code and no answers
#
# Try each exercise yourself before you look at solutions.py.

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
    s["Has children"] = ______(d["has_children"] == "Yes")
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
    f"{estimate:.2f} points higher (95% CI {ci_low:.2f} to {ci_high:.2f}, {______(p_val)}), "
    f"holding sleep, study hours, and stress constant."
)
print("\nReporting sentence:")
print(reporting_sentence)


# Exercise 4: see exercises.txt (a third panel for the thesis figure)


# Exercise 5: A method for a research question from your own field
# (Write your reflections as comments)


# Exercise 6: The chain of reasoning for RQ2 (sleep less than 7 hours?)
sleep_clean = study["sleep_hours"].dropna()
sleep_test = stats.ttest_1samp(sleep_clean, popmean=______, alternative="less")
sleep_mean = sleep_clean.mean()
# 95% two-sided confidence interval for mean sleep
sem_sleep = stats.sem(sleep_clean)
ci_sleep = stats.t.interval(0.95, df=len(sleep_clean)-1, loc=sleep_mean, scale=sem_sleep)

print(f"\nRQ2 Sleep Test: mean = {sleep_mean:.2f}, 95% CI = [{ci_sleep[0]:.2f}, {ci_sleep[1]:.2f}], p = {sleep_test.pvalue:.4f}, n = {len(sleep_clean)}")


# ==============================================================================
# B. GO FURTHER
# ==============================================================================

# Exercise 7: A helper for confidence intervals, used in three sentences
def format_ci(estimate, low, high, digits=2):
    return f"{estimate:.{digits}f} (95% CI {low:.{digits}f} to {______:.{digits}f})"

ci_sleep_gpa = gpa_model.conf_int().loc["sleep_hours"]
print("Sleep & GPA:", format_ci(gpa_model.params["sleep_hours"], ci_sleep_gpa[0], ci_sleep_gpa[1]))

mode_ft = study.query("study_mode == 'Full-time'")["wellbeing"].dropna()
mode_pt = study.query("study_mode == 'Part-time'")["wellbeing"].dropna()
diff_mode = mode_ft.mean() - mode_pt.mean()
ci_mode = stats.t.interval(0.95, df=len(mode_ft)+len(mode_pt)-2, loc=diff_mode,
                           scale=np.sqrt(mode_ft.var(ddof=1)/len(mode_ft) + mode_pt.var(ddof=1)/len(mode_pt)))
print("Study mode difference:", format_ci(diff_mode, ci_mode[0], ci_mode[1], digits=1))


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
    t1_fac[f] = describe(study[study["faculty"] == ______]).values
print("\nTable 1 across all 5 faculties:")
print(t1_fac.to_markdown(index=False))


# Exercise 10: Choosing methods for five research questions (as comments)
# 1. How many hours a week do nurses in a hospital work, on average?
# 2. Is the number of hours worked related to burnout, allowing for age and ward?
# 3. Burnout measured every three months for two years: does it rise?
# 4. Can nurses who will leave within a year be identified from their records?
# 5. Are there groups of nurses with similar shifts, overtime, and sick days?


# ==============================================================================
# C. CHECK YOUR UNDERSTANDING
# Answer in your own words, then compare with solutions.py.
# ==============================================================================

# 1. Why should every number in a thesis be traced to code?
# 2. What is the difference between a result and a conclusion?
# 3. Why is the workshop conclusion the only causal one in the chapter?
# 4. What is a limitations section for?
# 5. What are reporting standards such as JARS, CONSORT, and STROBE for?


# ==============================================================================
# D. DO IT YOURSELF
# Open tasks: no starter code, no hints, and no answers.
# ==============================================================================

# Task 1: The capstone. A research question the book did not answer (for
# example, exercise and wellbeing, allowing for sleep), carried through the
# whole chain, then written as a Quarto report like results.qmd.

# Task 2: Check your report against the JARS items for participants, measures,
# and results, and add anything missing.

# Task 3: Review a fellow student's report with the chain of reasoning, and
# write three constructive comments.
