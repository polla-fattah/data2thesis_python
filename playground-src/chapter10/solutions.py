# FROM DATA TO THESIS: Using Python for Non-Technical
# Playground, Chapter 10: Solutions
#
# One possible solution for each exercise in parts A and B, and model answers
# for part C. Part D has no solutions: the tasks are open, and there are many
# good ways to answer them.

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

# Exercise 1: ICC ~0.83; slope of time is almost exactly zero (-0.000, CI -0.015 to 0.016):
# sleep does not change across semesters
sleep_ri = smf.mixedlm("sleep_hours ~ time", panel, groups=panel["student_id"]).fit()
var_between = sleep_ri.cov_re.iloc[0, 0]
var_within = sleep_ri.scale
icc = var_between / (var_between + var_within)
print(f"ICC: {icc:.3f}")
print("95% CI for slope:\n", sleep_ri.conf_int().loc["time"])


# Exercise 2: the test favours the random slope (Chi2 = 7.8, p = 0.02),
# but the slopes' SD is only 0.05 hours per semester: statistically detectable,
# practically negligible
sleep_rs = smf.mixedlm("sleep_hours ~ time", panel, groups=panel["student_id"], re_formula="~time").fit()
lr_stat = -2 * (sleep_ri.llf - sleep_rs.llf)
p_val = stats.chi2.sf(lr_stat, df=2)
print(f"LR Chi2(2): {lr_stat:.2f}, p-value: {p_val:.4f}")
print("Random effects cov:\n", sleep_rs.cov_re)


# Exercise 3: part-time students start ~3.9 points lower (CI -5.9 to -1.9); the
# slope difference (0.14, CI -0.34 to 0.61) includes zero: same rate of change
wb_mode = smf.mixedlm("wellbeing ~ time * study_mode", panel, groups=panel["student_id"], re_formula="~time").fit()
print(wb_mode.summary().tables[1].round(2))
print("Confidence intervals:\n", wb_mode.conf_int().round(2))


# Exercise 4: supervisor share ~0 (boundary/near zero); 91% between students
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


# Exercise 5: the ordinary regression's false alarms rise to about 46% (vs ~26% with sd = 5);
# the mixed model stays near 8-10%. Larger differences between supervisors make their
# students more alike, so the data holds even less independent information.
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
runs = [simulate_clustered(style_sd=10) for _ in range(100)]
ord_rate = np.mean([r[0] for r in runs])
mix_rate = np.mean([r[1] for r in runs])
print(f"Ordinary false alarms: {ord_rate:.1%}, Mixed false alarms: {mix_rate:.1%}")


# Exercise 6 (model answer):
# A student's records are far more alike than records of different students,
# so 2,326 records of 600 students carry about as much information as ~700
# independent ones. An ordinary regression counts them all as independent, so
# its standard errors and p-values are spuriously small.


# ==============================================================================
# B. GO FURTHER
# ==============================================================================

# Exercise 7: GPA: ICC 0.71, design effect 3.0, worth about 767 records.
# Sleep: ICC 0.83, design effect 3.4, worth about 679.
records_per_student = len(panel) / panel["student_id"].nunique()

panel_gpa = panel.dropna(subset=["gpa"])
gpa_null = smf.mixedlm("gpa ~ 1", panel_gpa, groups=panel_gpa["student_id"]).fit()
icc_gpa = gpa_null.cov_re.iloc[0, 0] / (gpa_null.cov_re.iloc[0, 0] + gpa_null.scale)
design_effect = 1 + (records_per_student - 1) * icc_gpa
print(f"ICC: {icc_gpa:.2f}, Design Effect: {design_effect:.2f}, Equivalent records: {len(panel_gpa) / design_effect:.0f}")


# Exercise 8: averages and mixed model agree (-3.7, SE 0.98); the naive
# regression of all records gives SE 0.54, which is artificially narrow.
averages = panel.groupby(["student_id", "study_mode"])["wellbeing"].mean().reset_index()

m_avg = smf.ols("wellbeing ~ study_mode", averages).fit()
m_mix = smf.mixedlm("wellbeing ~ study_mode", panel, groups=panel["student_id"]).fit()
m_naive = smf.ols("wellbeing ~ study_mode", panel).fit()

print("Averages OLS:\n", m_avg.summary().tables[1])
print("Mixed Model:\n", m_mix.summary().tables[1])
print("Naive OLS:\n", m_naive.summary().tables[1])


# Exercise 9: five days give a slope of ~8.2 ms per day (SE 2.4), against 10.5
# (SE 1.5) for ten days; a slope describes only the period observed.
full = smf.mixedlm("Reaction ~ Days", sleepstudy, groups=sleepstudy["Subject"], re_formula="~Days").fit()
early_data = sleepstudy.query("Days <= 4")
early = smf.mixedlm("Reaction ~ Days", early_data, groups=early_data["Subject"], re_formula="~Days").fit()

print("Full (10 days):\n", full.summary().tables[1])
print("Early (5 days):\n", early.summary().tables[1])


# Exercise 10: average growth ~8.5 g per day, SD of growth rates ~3.8 g per day;
# the intercept (29 g, below the real 41 g) reflects slight non-linearity.
chick_model = smf.mixedlm("weight ~ Time", chickweight, groups=chickweight["Chick"], re_formula="~Time").fit()
print(chick_model.summary())


# ==============================================================================
# C. CHECK YOUR UNDERSTANDING: model answers
# ==============================================================================

# 1. Why are repeated records of the same student not independent?
#    Each student brings stable personal traits to every record, so a subsequent
#    record partly repeats the information of previous ones.
#
# 2. What does the intraclass correlation (ICC) measure?
#    The proportion of total outcome variance that lies between clusters rather
#    than within them; a higher ICC means ignoring clustering is more erroneous.
#
# 3. What is the difference between a fixed effect and a random effect?
#    Fixed effects describe population-average relationships (single numbers).
#    Random effects describe how groups or subjects vary around those averages
#    (estimated as variances/standard deviations).
#
# 4. What does near-zero variance / singular fit mean, and what should you do?
#    The random effects structure is over-parameterised for the data's variation.
#    Simplify the model by dropping unnecessary random slopes.
#
# 5. In the chapter's simulation, why did ordinary regression produce so many false alarms?
#    The training was assigned to 20 supervisors, not 200 independent students.
#    Treating 200 clustered observations as independent understates standard errors.


# ==============================================================================
# D. DO IT YOURSELF
# No solutions: these tasks are open. Compare your approach with the methods of
# Chapter 10, and discuss your choices with a fellow student or your supervisor.
# ==============================================================================
