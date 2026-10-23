# FROM DATA TO THESIS: Using Python for Non-Technical
# Playground, Chapter 10: Mixed-Effects Models
#
# Four parts, as on the playground page:
#   A. Practise the chapter       the book's exercises, with blanks (______) to fill
#   B. Go further                 new exercises beyond the book
#   C. Check your understanding   short questions; answers in solutions.py
#   D. Do it yourself             open tasks with no starter code and no answers
#
# Try each exercise yourself before you look at solutions.py.

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf

students = pd.read_csv("students.csv")
students["employment"] = students["employment"].fillna("None")
semesters = pd.read_csv("semesters.csv")
sleepstudy = pd.read_csv("sleepstudy.csv")
chickweight = pd.read_csv("chickweight.csv")

panel = (
    semesters
    .merge(students, on="student_id")
    .assign(time=lambda d: d["semester"] - 1)
)


# ==============================================================================
# A. PRACTISE THE CHAPTER
# ==============================================================================

# Exercise 1: Sleep over the semesters
# Random intercept model; ICC; does sleep change?
sleep_ri = smf.______( "sleep_hours ~ time", panel, groups=panel["student_id"]).fit()
var_between = sleep_ri.cov_re.iloc[0, 0]
var_within = sleep_ri.scale
icc = var_between / (var_between + var_within)
print(f"ICC: {icc:.3f}")
print("95% CI for slope:\n", sleep_ri.conf_int().loc["time"])


# Exercise 2: Is a random slope worth keeping?
sleep_rs = smf.mixedlm("sleep_hours ~ time", panel, groups=panel["student_id"], re_formula="~______").fit()
lr_stat = -2 * (sleep_ri.llf - sleep_rs.llf)
p_val = stats.chi2.sf(lr_stat, df=2)
print(f"LR Chi2(2): {lr_stat:.2f}, p-value: {p_val:.4f}")
print("Random effects cov:\n", sleep_rs.cov_re)


# Exercise 3: Do part-time students change differently?
wb_mode = smf.mixedlm("wellbeing ~ time ______ study_mode", panel, groups=panel["student_id"], re_formula="~time").fit()
print(wb_mode.summary().tables[1].round(2))
print("Confidence intervals:\n", wb_mode.conf_int().round(2))


# Exercise 4: Supervisors and study hours
# How much of the variation lies between supervisors?
study_levels = smf.mixedlm(
    "study_hours ~ time",
    panel,
    groups=panel["supervisor_id"],
    re_formula="1",
    vc_formula={"student": "0 + C(student_id)"}
).fit()
var_sup = study_levels.cov_re.iloc[0, 0]
var_stu = study_levels.vcomp[0]
var_res = study_levels.scale
var_tot = var_sup + var_stu + var_res
print(pd.DataFrame({
    "level": ["supervisor", "student", "residual"],
    "share": [round(var_sup / var_tot, 3), round(var_stu / var_tot, 3), round(var_res / var_tot, 3)]
}))


# Exercise 5: Supervisors who differ more
# scale = 10 for style: what happens to the false alarm rate of the ordinary
# regression, and why?
def simulate_clustered(style_sd):
    supervisor = np.repeat(np.arange(20), 10)
    trained = np.repeat(np.tile([0, 1], 10), 10)
    style = np.random.normal(scale=style_sd, size=20)[supervisor]
    wellbeing = 60 + style + np.random.normal(scale=10, size=200)
    df = pd.DataFrame({"supervisor": supervisor, "trained": trained, "wellbeing": wellbeing})
    
    p_ord = smf.ols("wellbeing ~ trained", df).fit().pvalues["trained"]
    m = smf.mixedlm("wellbeing ~ trained", df, groups=df["supervisor"]).fit(disp=False)
    p_mix = m.pvalues["trained"]
    return (p_ord < 0.05, p_mix < 0.05)

np.random.seed(12)
runs = [simulate_clustered(style_sd=______) for _ in range(100)]
ord_rate = np.mean([r[0] for r in runs])
mix_rate = np.mean([r[1] for r in runs])
print(f"Ordinary false alarms: {ord_rate:.1%}, Mixed false alarms: {mix_rate:.1%}")


# Exercise 6: Explaining it to a fellow student
# Why would an ordinary regression of all the semester records be wrong?
# Write your answer in comments below.


# ==============================================================================
# B. GO FURTHER
# ==============================================================================

# Exercise 7: How much information is in the records?
# The design effect for GPA (then change gpa to sleep_hours).
records_per_student = len(panel) / panel["student_id"].nunique()

panel_gpa = panel.dropna(subset=["gpa"])
gpa_null = smf.mixedlm("gpa ~ 1", panel_gpa, groups=panel_gpa["student_id"]).fit()
icc_gpa = gpa_null.cov_re.iloc[0, 0] / (gpa_null.cov_re.iloc[0, 0] + gpa_null.scale)
design_effect = 1 + (records_per_student - 1) * ______
print(f"ICC: {icc_gpa:.2f}, Design Effect: {design_effect:.2f}, Equivalent records: {len(panel_gpa) / design_effect:.0f}")


# Exercise 8: Averaging first, or a mixed model
averages = panel.groupby(["student_id", "study_mode"])["wellbeing"].mean().reset_index()

m_avg = smf.ols("wellbeing ~ study_mode", averages).fit()
m_mix = smf.mixedlm("wellbeing ~ study_mode", panel, groups=panel["student_id"]).fit()
m_naive = smf.ols("wellbeing ~ study_mode", panel).fit()

print("Averages OLS:\n", m_avg.summary().tables[1])
print("Mixed Model:\n", m_mix.summary().tables[1])
print("Naive OLS:\n", m_naive.summary().tables[1])


# Exercise 9: How long a study needs to run (sleepstudy, days 0 to 4 vs all 10)
full = smf.mixedlm("Reaction ~ Days", sleepstudy, groups=sleepstudy["Subject"], re_formula="~Days").fit()
early_data = sleepstudy.query("Days ______ 4")
early = smf.mixedlm("Reaction ~ Days", early_data, groups=early_data["Subject"], re_formula="~Days").fit()

print("Full (10 days):\n", full.summary().tables[1])
print("Early (5 days):\n", early.summary().tables[1])


# Exercise 10: Growth curves for chicks
chick_model = smf.mixedlm("weight ~ Time", chickweight, groups=chickweight["Chick"], re_formula="~______").fit()
print(chick_model.summary())


# ==============================================================================
# C. CHECK YOUR UNDERSTANDING
# Answer in your own words, then compare with the answers in solutions.py.
# ==============================================================================

# 1. Why are repeated records of the same student not independent?
# 2. What does the intraclass correlation (ICC) measure?
# 3. What is the difference between a fixed effect and a random effect?
# 4. What does near-zero variance / singular fit mean, and what should you do?
# 5. In the chapter's simulation, why did ordinary regression produce so many false alarms?


# ==============================================================================
# D. DO IT YOURSELF
# Open tasks: no starter code, no hints, and no answers. Write your own code
# under each task, as you would for a thesis.
# ==============================================================================

# Task 1: Model the change in exercise_days over the semesters, choose the
# random effects with a likelihood ratio test, calculate the ICC, and report.

# Task 2: Does the workshop effect over time differ between Master's and PhD
# students? A three-way interaction, described with predicted wellbeing for the
# four groups in semester 2.

# Task 3: The reporting paragraph for a mixed model of GPA over the semesters,
# with random effects and numbers of observations and students, all by code.

# Task 4: Explore chick growth curves with dietary interactions using chickweight.
