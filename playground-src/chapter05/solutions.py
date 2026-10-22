# FROM DATA TO THESIS: Using Python for Non-Technical
# Playground, Chapter 5: Solutions
#
# One possible solution for each exercise in parts A and B, and model answers
# for part C. Part D has no solutions: the tasks are open, and there are many
# good ways to answer them.

import pandas as pd
import numpy as np
from scipy import stats
from scipy.special import expit
from statsmodels.stats.power import TTestIndPower

students = pd.read_csv("students.csv")
semesters = pd.read_csv("semesters.csv")
questionnaire = pd.read_csv("questionnaire.csv")

first_sem = (
    semesters[semesters["semester"] == 1]
    .merge(students, on="student_id")
)

# ==============================================================================
# A. PRACTISE THE CHAPTER
# ==============================================================================

# Exercise 1: Model answers
# (a) "Do graduate students who report regular weekly aerobic exercise achieve
#     higher semester wellbeing scores than sedentary students?" (Relational)
#     or: "Does random assignment to a structured 8-week physical activity
#     programme improve graduate student psychological wellbeing?" (Causal)
# (b) "Is the frequency of monthly supervisor advisory meetings associated
#     with graduate students' self-reported research progress satisfaction?" (Relational)


# Exercise 2: Both groups study approximately 27.6 hours; no support for H1.
study_by_children = (
    first_sem.groupby("has_children")["study_hours"]
    .agg(students="count", mean_study_hours="mean")
)
print(study_by_children.round(2))


# Exercise 3: Levels of measurement
# Nominal: student_id, supervisor_id, gender, faculty, programme, study_mode,
#          has_children, lives_away, workshop, considering_dropout
# Ordinal: employment, financial_worry, Likert survey items
# Ratio:   age, workshop_sessions, sleep_hours, study_hours, caffeine_mg
labels = ["Not at all", "A little", "Moderately", "Very", "Extremely"]
students["financial_worry_cat"] = pd.Categorical.from_codes(
    codes=students["financial_worry"].fillna(0).astype(int) - 1,
    categories=labels,
    ordered=True
)
print(students["financial_worry_cat"].value_counts(dropna=False).sort_index())


# Exercise 4: With n = 30 per group, 95% of chance differences fall roughly
# between -5.5 and +5.5 points (more than double the interval for n = 150).
# A genuine 5-point intervention effect is easily masked by chance in a small pilot.
np.random.seed(2026)
n_sims = 5000
chance_diffs_small = np.empty(n_sims)
small_groups = np.repeat(["Invited", "Not invited"], 30)

for i in range(n_sims):
    wellbeing = np.random.normal(loc=60, scale=11, size=60)
    shuffled = np.random.permutation(small_groups)
    diff = (
        wellbeing[shuffled == "Invited"].mean()
        - wellbeing[shuffled == "Not invited"].mean()
    )
    chance_diffs_small[i] = diff

q_lower, q_upper = np.percentile(chance_diffs_small, [2.5, 97.5])
print(f"95% bounds for n=30 per group: [{q_lower:.2f}, {q_upper:.2f}]")


# Exercise 5: The two randomised conditions show closely matched proportions;
# the small differences (e.g., living away 39.3% vs 46.0%) reflect normal chance variation.
balance_check = students.groupby("workshop").agg(
    part_time=("study_mode", lambda x: 100 * (x == "Part-time").mean()),
    children=("has_children", lambda x: 100 * (x == "Yes").mean()),
    lives_away=("lives_away", lambda x: 100 * (x == "Yes").mean())
).round(1)
print(balance_check)


# Exercise 6: 176 students per group for 80% power, 235 for 90% power
power_analyzer = TTestIndPower()
n_80 = power_analyzer.solve_power(effect_size=0.30, power=0.80, alpha=0.05, alternative="two-sided")
n_90 = power_analyzer.solve_power(effect_size=0.30, power=0.90, alpha=0.05, alternative="two-sided")
print(f"Required for 80% power (d=0.3): {int(np.ceil(n_80))} students per group")
print(f"Required for 90% power (d=0.3): {int(np.ceil(n_90))} students per group")


# ==============================================================================
# B. GO FURTHER
# ==============================================================================

# Exercise 7 (Model answers):
# 1. Descriptive (frequency distribution in a single cohort)
# 2. Relational (association between two observed measures)
# 3. Causal (investigates treatment effect via random assignment)
# 4. Descriptive / Longitudinal (describes temporal trajectory of one variable)
# 5. Relational (observational association; meeting frequency was not randomised)

# Exercise 8 (Model answers):
# 1. "Students with higher baseline academic stress report lower semester GPAs";
#    against H1: zero or positive correlation between stress and GPA.
# 2. "Invited students who attend at least 4 workshop sessions exhibit higher
#    semester 2 wellbeing than uninvited students"; against H1: equal or lower mean wellbeing.
# 3. "Daily screen hours on social media correlate negatively with sleep duration";
#    against H1: zero or positive correlation between screen time and sleep.


# Exercise 9: Simple random sampling yields variable part-time representation
# (5 to 25 students), whereas stratified sampling guarantees exactly 15.
# Because study mode accounts for little total wellbeing variance, estimate standard
# errors are virtually identical (~1.62 vs ~1.63).
np.random.seed(5)
full_time = first_sem[first_sem["study_mode"] == "Full-time"]
part_time = first_sem[first_sem["study_mode"] == "Part-time"]

simple_means = []
stratified_means = []

for _ in range(2000):
    s_simple = first_sem.sample(n=50, replace=False)
    simple_means.append(s_simple["wellbeing"].mean())

    s_strat = pd.concat([
        full_time.sample(n=35, replace=False),
        part_time.sample(n=15, replace=False)
    ])
    stratified_means.append(s_strat["wellbeing"].mean())

print(f"Simple sample SD of estimates:     {np.std(simple_means):.3f}")
print(f"Stratified sample SD of estimates: {np.std(stratified_means):.3f}")


# Exercise 10: Estimated power for r = 0.20:
# n=100 (~0.51), n=150 (~0.71), n=200 (~0.83), n=250 (~0.87).
# Approximately 190 to 200 participants are required for 80% power.
def simulate_correlation_power(n, r=0.20, n_sims=1000):
    significant_count = 0
    for _ in range(n_sims):
        x = np.random.normal(size=n)
        y = r * x + np.sqrt(1 - r**2) * np.random.normal(size=n)
        r_val, p_val = stats.pearsonr(x, y)
        if p_val < 0.05:
            significant_count += 1
    return significant_count / n_sims

for sample_n in [100, 150, 200, 250]:
    power_est = simulate_correlation_power(sample_n, r=0.20)
    print(f"Sample size {sample_n}: Estimated power = {power_est:.2f}")


# Exercise 11: True mean is 60.5; even with n = 400, the voluntary survey estimate
# converges tightly around 63.9 with standard error ~0.30. Increasing sample size
# sharpens the precision around a biased estimate.
pop_wellbeing = first_sem["wellbeing"].dropna().to_numpy()
true_mean = pop_wellbeing.mean()
p_answer = expit((pop_wellbeing - true_mean) / 10)
p_answer /= p_answer.sum()

np.random.seed(5)
voluntary_estimates_400 = [
    np.random.choice(pop_wellbeing, size=400, replace=True, p=p_answer).mean()
    for _ in range(2000)
]

print(f"True population mean:             {true_mean:.2f}")
print(f"Biased sample (n=400) mean:       {np.mean(voluntary_estimates_400):.2f}")
print(f"Standard error of estimate:       {np.std(voluntary_estimates_400):.3f}")


# ==============================================================================
# C. CHECK YOUR UNDERSTANDING: model answers
# ==============================================================================

# 1. Why must a hypothesis be stated before the data is analysed?
#    A hypothesis formed after observing the data merely redescribes empirical
#    patterns (HARKing) and cannot fail. An a priori hypothesis ensures the
#    empirical test genuinely risks refutation.
#
# 2. A statistical test rejects the null hypothesis. What has it NOT shown?
#    It has NOT proven that the substantive hypothesis (H1) is uniquely true,
#    that the effect is practically large, or that the relationship is causal
#    (in an observational study where confounding remains).
#
# 3. What is the difference between reliability and validity?
#    Reliability is measurement consistency/precision. Validity is accuracy
#    relative to the intended construct. A miscalibrated scale can be highly
#    reliable (reproducible) while completely invalid (systematically biased).
#
# 4. Why is a larger biased sample still biased?
#    Increasing sample size reduces sampling variance (random standard error),
#    tightening the confidence interval around a systematically shifted estimate.
#    It does not eliminate recruitment or self-selection bias.
#
# 5. What does random assignment balance that post-hoc statistical adjustment cannot?
#    Random assignment balances both measured AND unmeasured/unknown confounders
#    across treatment arms. Statistical adjustment can only control for variables
#    that were explicitly measured and included in the model.


# ==============================================================================
# D. DO IT YOURSELF
# No solutions: these tasks are open. Compare your approach with the methods of
# Chapter 5, and discuss your choices with a fellow student or your supervisor.
# ==============================================================================
