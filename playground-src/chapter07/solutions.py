# FROM DATA TO THESIS: Using Python for Non-Technical
# Playground, Chapter 7: Hypothesis Testing and Statistical Inference
#
# Complete solutions with comprehensive statistical commentary.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.power import TTestIndPower

# Load datasets
students = pd.read_csv("students.csv")
semesters = pd.read_csv("semesters.csv")
questionnaire = pd.read_csv("questionnaire.csv")
sleep = pd.read_csv("sleep.csv")

first_sem = (
    semesters.query("semester == 1")
    .merge(students, on="student_id")
)


# ==============================================================================
# A. PRACTISE THE CHAPTER
# ==============================================================================

# Exercise 1: Two sampling distributions
study = first_sem["study_hours"].dropna().to_numpy()
rng = np.random.default_rng(1)

means_10 = np.array([rng.choice(study, size=10, replace=True).mean() for _ in range(1000)])
means_50 = np.array([rng.choice(study, size=50, replace=True).mean() for _ in range(1000)])

print(f"SE for n=10: {means_10.std(ddof=1):.2f}")
print(f"SE for n=50: {means_50.std(ddof=1):.2f}")

fig, ax = plt.subplots(figsize=(6, 3.5))
sns.histplot(means_50, bins=30, color="#1d588c", ax=ax)
ax.set_title("Sampling Distribution of Mean Study Hours (n=50)")
ax.set_xlabel("Sample Mean (hours/week)")
plt.tight_layout()
plt.show()
# Explanation:
# The standard error drops from ~4.13 hours for n=10 to ~1.85 hours for n=50,
# scaling strictly with 1/sqrt(n). Larger samples compress sampling error,
# yielding narrow, symmetrical, Gaussian-like sampling distributions.


# Exercise 2: A confidence interval for GPA
gpa_clean = first_sem["gpa"].dropna()
res_gpa = stats.ttest_1samp(gpa_clean, popmean=0)
ci_gpa = res_gpa.confidence_interval(0.95)
print(f"Mean GPA: {gpa_clean.mean():.2f}")
print(f"95% CI:   [{ci_gpa.low:.2f}, {ci_gpa.high:.2f}]")
# Explanation:
# The sample mean is 3.19. The 95% confidence interval is [3.15, 3.23].
# In words: based on our sample, the true mean first-semester GPA of all
# graduate students is plausibly between 3.15 and 3.23 grade points.


# Exercise 3: A one-sample test against 60
# H0: mu = 60 (wellbeing index equals 60)
# H1: mu != 60
test_wb = stats.ttest_1samp(first_sem["wellbeing"].dropna(), popmean=60)
ci_wb = test_wb.confidence_interval(0.95)
print(f"t-statistic: {test_wb.statistic:.2f}, df: {test_wb.df}, p-value: {test_wb.pvalue:.4e}")
print(f"Sample mean: {first_sem['wellbeing'].mean():.2f}, 95% CI: [{ci_wb.low:.2f}, {ci_wb.high:.2f}]")
# Conclusion:
# First-semester graduate student wellbeing (M = 52.88, SD = 11.23) is significantly
# below the neutral benchmark of 60, t(599) = -15.54, p < .001, 95% CI [51.98, 53.78].


# Exercise 4: Full-time and part-time students
ft_gpa = first_sem.query("study_mode == 'Full-time'")["gpa"].dropna().to_numpy()
pt_gpa = first_sem.query("study_mode == 'Part-time'")["gpa"].dropna().to_numpy()
observed_diff = ft_gpa.mean() - pt_gpa.mean()

all_gpa = np.concatenate([ft_gpa, pt_gpa])
n_ft = len(ft_gpa)
rng = np.random.default_rng(2026)

shuffled_diffs = []
for _ in range(5000):
    perm = rng.permutation(all_gpa)
    shuffled_diffs.append(perm[:n_ft].mean() - perm[n_ft:].mean())

shuffled_diffs = np.array(shuffled_diffs)
perm_p = (np.abs(shuffled_diffs) >= np.abs(observed_diff)).mean()
welch_res = stats.ttest_ind(ft_gpa, pt_gpa, equal_var=False)

s_pooled = np.sqrt((ft_gpa.var(ddof=1) + pt_gpa.var(ddof=1)) / 2)
cohens_d = (ft_gpa.mean() - pt_gpa.mean()) / s_pooled

print(f"Observed Difference: {observed_diff:.3f}")
print(f"Permutation p-value: {perm_p:.3f}")
print(f"Welch t p-value:     {welch_res.pvalue:.3f}")
print(f"Cohen's d:           {cohens_d:.3f}")
# Explanation:
# The difference in mean GPA between full-time (3.20) and part-time (3.17)
# students is tiny (0.03 grade points), d = 0.06. Both the permutation test
# (p = 0.44) and Welch's t-test (t = 0.77, p = 0.44) confirm that study mode
# does not significantly differentiate academic performance.


# Exercise 5: Statistical power by simulation
def simulate_study(n_per_group, effect=3.0, sd=11.0, reps=2000):
    rng = np.random.default_rng(3)
    p_vals = []
    for _ in range(reps):
        inv = rng.normal(loc=60 + effect, scale=sd, size=n_per_group)
        ctrl = rng.normal(loc=60, scale=sd, size=n_per_group)
        p_vals.append(stats.ttest_ind(inv, ctrl, equal_var=False).pvalue)
    return (np.array(p_vals) < 0.05).mean()

power_40 = simulate_study(40, effect=3.0)
print(f"Power with 40 students per group: {power_40:.2f}")
# Explanation:
# Power is only about 0.22 (22%). If a researcher designs a study with only 40
# participants per group to detect a 3-point effect, they have a 78% risk of
# failing to detect the true intervention effect (Type II error).


# Exercise 6: Living away and dropout
cont_tab = pd.crosstab(students["lives_away"], students["considering_dropout"])
print("Contingency table:")
print(cont_tab)

chi2_out = stats.chi2_contingency(cont_tab)
print(f"Chi-square: {chi2_out.statistic:.2f}, df: {chi2_out.dof}, p-value: {chi2_out.pvalue:.4f}")
print("Expected frequencies:")
print(np.round(chi2_out.expected_freq, 1))
# Explanation:
# All expected counts exceed 40 (well above the required minimum of 5).
# The chi-square test yields chi2(1) = 2.45, p = 0.117. There is no statistically
# significant association between living away from family and considering dropout.


# ==============================================================================
# B. GO FURTHER
# ==============================================================================

# Exercise 7: Confidence interval coverage
pop = first_sem["wellbeing"].to_numpy()
true_param = pop.mean()
rng = np.random.default_rng(4)

covered_count = 0
for _ in range(100):
    sample_draw = rng.choice(pop, size=30, replace=False)
    ci = stats.ttest_1samp(sample_draw, popmean=0).confidence_interval(0.95)
    if ci.low <= true_param <= ci.high:
        covered_count += 1

print(f"Coverage out of 100 samples: {covered_count}%")
# Explanation:
# Out of 100 independently generated 95% confidence intervals, approximately 94-96
# contain the true parameter. This demonstrates that '95% confidence' is a long-run
# property of the estimation procedure over repeated sampling.


# Exercise 8: Permutation test for medians
fem_sleep = first_sem.query("gender == 'Female'")["sleep_hours"].dropna().to_numpy()
male_sleep = first_sem.query("gender == 'Male'")["sleep_hours"].dropna().to_numpy()
obs_median_diff = np.median(fem_sleep) - np.median(male_sleep)

all_sleep = np.concatenate([fem_sleep, male_sleep])
n_f = len(fem_sleep)
rng = np.random.default_rng(2026)

shuffled_median_diffs = []
for _ in range(5000):
    perm = rng.permutation(all_sleep)
    shuffled_median_diffs.append(np.median(perm[:n_f]) - np.median(perm[n_f:]))

perm_median_p = (np.abs(shuffled_median_diffs) >= np.abs(obs_median_diff)).mean()
print(f"Observed Median Difference: {obs_median_diff:.2f} hours")
print(f"Permutation p-value:        {perm_median_p:.3f}")


# Exercise 9: Multiple testing correction
faculties = first_sem["faculty"].unique()
p_raw = []
pairs = []
for i in range(len(faculties)):
    for j in range(i + 1, len(faculties)):
        f1, f2 = faculties[i], faculties[j]
        s1 = first_sem.query("faculty == @f1")["wellbeing"].dropna()
        s2 = first_sem.query("faculty == @f2")["wellbeing"].dropna()
        p_raw.append(stats.ttest_ind(s1, s2, equal_var=False).pvalue)
        pairs.append(f"{f1} vs {f2}")

reject, p_bonf, _, _ = multipletests(p_raw, alpha=0.05, method="bonferroni")
print(f"Significant uncorrected: {sum(np.array(p_raw) < 0.05)} of {len(p_raw)}")
print(f"Significant Bonferroni:  {sum(reject)} of {len(p_raw)}")


# Exercise 10: Paired vs independent t-test on Student's sleep data
d1 = sleep.query("group == 1")["extra"].to_numpy()
d2 = sleep.query("group == 2")["extra"].to_numpy()

paired_result = stats.ttest_rel(d2, d1)
independent_result = stats.ttest_ind(d2, d1, equal_var=False)

print(f"Paired t-test:      t = {paired_result.statistic:.2f}, p = {paired_result.pvalue:.4f}")
print(f"Independent t-test: t = {independent_result.statistic:.2f}, p = {independent_result.pvalue:.4f}")
# Explanation:
# The paired t-test compares each patient with themselves, subtracting baseline
# patient sleep variability, yielding t = 4.06, p = 0.0028 (significant).
# An independent t-test mistakenly pools across individuals, treating between-person
# variability as noise, yielding t = 1.86, p = 0.079 (non-significant).
# Using the correct paired design uncovers the genuine pharmacological effect!


# ==============================================================================
# C. CHECK YOUR UNDERSTANDING - ANSWERS
# ==============================================================================

# 1. Standard error (SE = s / sqrt(n)) measures the dispersion of sample estimates
#    around the true population parameter across repeated sampling. Standard deviation
#    (s) measures the dispersion of individual data points around the sample mean.
#
# 2. A 95% confidence interval means that across hypothetical infinite replications of
#    the identical sampling and estimation process, 95% of computed intervals will bracket
#    the fixed, unknown population parameter.
#
# 3. A permutation test simulates the null hypothesis directly by randomly shuffling
#    group assignment labels across observed data points. Because it generates the
#    exact empirical null distribution from the sample itself, it relies on zero
#    parametric distribution assumptions (such as normality).
#
# 4. A study with power = 0.20 has an 80% Type II error rate (it will fail to detect
#    a genuine effect 4 times out of 5). Furthermore, any effect that happens to pass
#    the p < .05 threshold is subject to 'the winner's curse'—massively inflating the
#    apparent effect size.
#
# 5. Welch's t-test adjusts the degrees of freedom using the Welch-Satterthwaite equation,
#    robustly controlling the Type I error rate when group variances or sample sizes differ.
#    Standard Student's t-test experiences severe false-alarm inflation when variances are unequal.


# ==============================================================================
# D. DO IT YOURSELF - SAMPLE IMPLEMENTATION
# ==============================================================================

# Task 1: Sleep differences in semester 2 by workshop invitation
sem2 = semesters.query("semester == 2").merge(students, on="student_id")
s_inv = sem2.query("workshop == 'Invited'")["sleep_hours"].dropna()
s_ctrl = sem2.query("workshop == 'Not invited'")["sleep_hours"].dropna()

t_res = stats.ttest_ind(s_inv, s_ctrl, equal_var=False)
u_res = stats.mannwhitneyu(s_inv, s_ctrl, alternative="two-sided")
d_val = (s_inv.mean() - s_ctrl.mean()) / np.sqrt((s_inv.var(ddof=1) + s_ctrl.var(ddof=1)) / 2)

print("\nTask 1 Sleep Comparison:")
print(f"Invited: M = {s_inv.mean():.2f}, SD = {s_inv.std():.2f}")
print(f"Control: M = {s_ctrl.mean():.2f}, SD = {s_ctrl.std():.2f}")
print(f"Welch t({t_res.df:.1f}) = {t_res.statistic:.2f}, p = {t_res.pvalue:.4f}, d = {d_val:.2f}")
print(f"Mann-Whitney U = {u_res.statistic:.1f}, p = {u_res.pvalue:.4f}")
