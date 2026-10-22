# FROM DATA TO THESIS: Using Python for Non-Technical
# Playground, Chapter 7: Hypothesis Testing and Statistical Inference
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
# Draw 1,000 samples of 10 students' study hours, and 1,000 samples of 50.
# Compare the standard errors and plot the distribution for n=50.
study = first_sem["study_hours"].dropna().to_numpy()
rng = np.random.default_rng(1)

means_10 = np.array([rng.choice(study, size=10, replace=True).mean() for _ in range(1000)])
means_50 = np.array([rng.choice(study, size=______, replace=True).mean() for _ in range(1000)])

print(f"SE for n=10: {means_10.std(ddof=1):.2f}")
print(f"SE for n=50: {means_50.std(ddof=1):.2f}")

fig, ax = plt.subplots(figsize=(6, 3.5))
sns.histplot(means_50, bins=30, color="#1d588c", ax=ax)
ax.set_title("Sampling Distribution of Mean Study Hours (n=50)")
ax.set_xlabel("Sample Mean (hours/week)")
plt.tight_layout()
plt.show()


# Exercise 2: A confidence interval for GPA
# Calculate a 95% confidence interval for average first-semester GPA.
gpa_clean = first_sem["gpa"].dropna()
res_gpa = stats.______(gpa_clean, popmean=0)
ci_gpa = res_gpa.confidence_interval(0.95)
print(f"Mean GPA: {gpa_clean.mean():.2f}")
print(f"95% CI:   [{ci_gpa.low:.2f}, {ci_gpa.high:.2f}]")


# Exercise 3: A one-sample test against 60
# Test whether average first-semester wellbeing differs from 60.
# State H0: mu = 60, H1: mu != 60.
test_wb = stats.ttest_1samp(first_sem["wellbeing"].dropna(), popmean=______)
print(f"t-statistic: {test_wb.statistic:.2f}, df: {test_wb.df}, p-value: {test_wb.pvalue:.4f}")


# Exercise 4: Full-time and part-time students
# Compare first-semester GPA with a permutation test (5,000 shuffles), then
# with a Welch two-sample t-test. Calculate Cohen's d.
ft_gpa = first_sem.query("study_mode == 'Full-time'")["gpa"].dropna().to_numpy()
pt_gpa = first_sem.query("study_mode == 'Part-time'")["gpa"].dropna().to_numpy()
observed_diff = ft_gpa.mean() - pt_gpa.mean()

all_gpa = np.concatenate([ft_gpa, pt_gpa])
n_ft = len(ft_gpa)
rng = np.random.default_rng(2026)

shuffled_diffs = []
for _ in range(5000):
    perm = rng.______(all_gpa)
    shuffled_diffs.append(perm[:n_ft].mean() - perm[n_ft:].mean())

perm_p = (np.abs(shuffled_diffs) >= np.abs(observed_diff)).mean()
welch_res = stats.ttest_ind(ft_gpa, pt_gpa, equal_var=______)

# Cohen's d
s_pooled = np.sqrt((ft_gpa.var(ddof=1) + pt_gpa.var(ddof=1)) / 2)
cohens_d = (ft_gpa.mean() - pt_gpa.mean()) / s_pooled

print(f"Observed Difference: {observed_diff:.3f}")
print(f"Permutation p-value: {perm_p:.3f}")
print(f"Welch t p-value:     {welch_res.pvalue:.3f}")
print(f"Cohen's d:           {cohens_d:.3f}")


# Exercise 5: Statistical power by simulation
# Simulate power with 40 students per group when true workshop effect is 3 points (sd = 11).
def simulate_study(n_per_group, effect=3.0, sd=11.0, reps=2000):
    rng = np.random.default_rng(3)
    p_vals = []
    for _ in range(reps):
        inv = rng.normal(loc=60 + effect, scale=sd, size=n_per_group)
        ctrl = rng.normal(loc=60, scale=sd, size=n_per_group)
        p_vals.append(stats.ttest_ind(inv, ctrl, equal_var=False).pvalue)
    return (np.array(p_vals) < 0.05).mean()

power_40 = simulate_study(______, effect=______)
print(f"Power with 40 students per group: {power_40:.2f}")


# Exercise 6: Living away and dropout
# Test whether living away from family is associated with considering dropout.
cont_tab = pd.crosstab(students["lives_away"], students["considering_dropout"])
print("Contingency table:")
print(cont_tab)

chi2_out = stats.chi2_contingency(______)
print(f"Chi-square: {chi2_out.statistic:.2f}, df: {chi2_out.dof}, p-value: {chi2_out.pvalue:.4f}")
print("Expected frequencies:")
print(chi2_out.expected_freq)


# ==============================================================================
# B. GO FURTHER
# ==============================================================================

# Exercise 7: How often a confidence interval covers the true mean
# Treat first-semester wellbeing as population. Draw 100 samples of 30,
# compute 95% CIs, and count coverage.
pop = first_sem["wellbeing"].to_numpy()
true_param = pop.mean()
rng = np.random.default_rng(4)

covered_count = 0
for _ in range(100):
    sample_draw = rng.choice(pop, size=30, replace=False)
    ci = stats.ttest_1samp(sample_draw, popmean=0).confidence_interval(______)
    if ci.low <= true_param <= ci.high:
        covered_count += 1

print(f"Coverage out of 100 samples: {covered_count}%")


# Exercise 8: Permutation test for medians
# Test whether median sleep differs between female and male students using 5,000 shuffles.
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
# Compare wellbeing between all 5 faculties pairwise. Apply Bonferroni correction.
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
# 10 patients, each given two soporific drugs.
d1 = sleep.query("group == 1")["extra"].to_numpy()
d2 = sleep.query("group == 2")["extra"].to_numpy()

paired_result = stats.ttest_rel(d2, d1)
independent_result = stats.ttest_ind(d2, d1, equal_var=False)

print(f"Paired t-test:      t = {paired_result.statistic:.2f}, p = {paired_result.pvalue:.4f}")
print(f"Independent t-test: t = {independent_result.statistic:.2f}, p = {independent_result.pvalue:.4f}")


# ==============================================================================
# C. CHECK YOUR UNDERSTANDING
# Answer in your own words, then compare with solutions.py.
# ==============================================================================

# 1. What does the standard error of a mean measure, and how does it differ
#    from the standard deviation?
# 2. What is the correct interpretation of a 95% confidence interval?
# 3. What is a permutation test, and why does it need no normality assumption?
# 4. Explain why a study with power = 0.20 is dangerous for science.
# 5. Why should Welch's t-test be preferred over Student's original t-test?


# ==============================================================================
# D. DO IT YOURSELF
# Open tasks: no starter code and no answers.
# ==============================================================================

# Task 1: Compare sleep between invited and control students in semester 2.
# Conduct both a Welch t-test and a Mann-Whitney U test. Report M, SD, t, p, and d.

# Task 2: Calculate a 95% bootstrap confidence interval for the 75th percentile
# (Q3) of first-semester caffeine intake.

# Task 3: Test whether faculty affiliation is related to considering dropout
# using a chi-square test of independence. Check expected counts.
