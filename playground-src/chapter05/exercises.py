# FROM DATA TO THESIS: Using Python for Non-Technical
# Playground, Chapter 5: From Research Question to Data
#
# Four parts, as on the playground page:
#   A. Practise the chapter       the book's exercises, with blanks (______) to fill
#   B. Go further                 new exercises beyond the book
#   C. Check your understanding   short questions; answers in solutions.py
#   D. Do it yourself             open tasks with no starter code and no answers
#
# Run a line or block with Shift+Enter in VS Code.
# Try each exercise yourself before you look at solutions.py.

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

# Exercise 1: Better research questions
# Improve these questions so that data could answer them, and state whether your
# version is descriptive, relational, or causal:
# (a) "Is exercise good for students?"
# (b) "What makes supervisors effective?"


# Exercise 2: A falsifiable hypothesis
# Research question: "Do students with children study fewer hours per week?"
# H1 (Alternative): Students with children report fewer weekly study hours than students without children.
# H0 (Null): The two groups have the same mean weekly study hours.
# What would count against H1: Students with children having equal or higher mean study hours.
study_by_children = (
    first_sem.groupby("has_children")["study_hours"]
    .agg(students="______", mean_study_hours="mean")
)
print(study_by_children.round(2))


# Exercise 3: Levels of measurement
# Classify each variable in students by its level of measurement (nominal, ordinal, interval, ratio).
# Then convert financial_worry into an ordered categorical with descriptive labels:
labels = ["Not at all", "A little", "Moderately", "Very", "Extremely"]
students["financial_worry_cat"] = pd.Categorical.from_codes(
    codes=students["financial_worry"] - 1,
    categories=______,
    ordered=______
)
print(students["financial_worry_cat"].value_counts(dropna=False).sort_index())


# Exercise 4: The null world with small groups
# Modify the simulation for two groups of 30 students (total 60) instead of 150.
# Between which bounds do 95% of the chance differences lie?
np.random.seed(2026)
n_sims = 5000
chance_diffs_small = np.empty(n_sims)
small_groups = np.repeat(["Invited", "Not invited"], ______)

for i in range(n_sims):
    wellbeing = np.random.normal(loc=60, scale=11, size=______)
    shuffled = np.random.permutation(small_groups)
    diff = (
        wellbeing[shuffled == "Invited"].mean()
        - wellbeing[shuffled == "Not invited"].mean()
    )
    chance_diffs_small[i] = diff

q_lower, q_upper = np.percentile(chance_diffs_small, [______, ______])
print(f"95% of chance differences fall between {q_lower:.2f} and {q_upper:.2f}")


# Exercise 5: Did the randomisation work?
# Check baseline equivalence between the two workshop conditions:
balance_check = students.groupby("workshop").agg(
    part_time=("study_mode", lambda x: 100 * (x == "Part-time").mean()),
    children=("has_children", lambda x: 100 * (x == "______").mean()),
    lives_away=("lives_away", lambda x: 100 * (x == "______").mean())
).round(1)
print(balance_check)


# Exercise 6: Statistical power and sample size
# Calculate the required sample size per group for a two-sample t-test to detect
# a standardised effect d = 0.30 with 80% power, and with 90% power:
power_analyzer = TTestIndPower()

n_80 = power_analyzer.solve_power(effect_size=______, power=0.80, alpha=0.05, alternative="two-sided")
n_90 = power_analyzer.solve_power(effect_size=______, power=______, alpha=0.05, alternative="two-sided")

print(f"Required per group for 80% power: {int(np.ceil(n_80))}")
print(f"Required per group for 90% power: {int(np.ceil(n_90))}")


# ==============================================================================
# B. GO FURTHER
# ==============================================================================

# Exercise 7: Kinds of questions
# Classify each as descriptive, relational, or causal:
# 1. What share of graduate students work in a paid job?
# 2. Is financial worry associated with considering dropping out?
# 3. Does a random invitation to a mindfulness course reduce stress?
# 4. How does average sleep change over four semesters?
# 5. Do students who meet their supervisor more often have higher GPAs?


# Exercise 8: Hypotheses that could be wrong
# Rewrite each vague statement into a falsifiable directional hypothesis:
# 1. "Stress affects students in various ways."
# 2. "The workshop works for students who engage with it properly."
# 3. "Social media use may be related to wellbeing."


# Exercise 9: Stratified vs Simple Random Sampling simulation
# Draw 2,000 samples of size 50 using simple random sampling vs stratified
# sampling (35 full-time, 15 part-time). Compare stability of estimates:
np.random.seed(5)
full_time = first_sem[first_sem["study_mode"] == "Full-time"]
part_time = first_sem[first_sem["study_mode"] == "Part-time"]

simple_means = []
stratified_means = []

for _ in range(2000):
    # Simple random sample of 50
    s_simple = first_sem.sample(n=50, replace=False)
    simple_means.append(s_simple["wellbeing"].mean())

    # Stratified sample: 35 full-time + 15 part-time
    s_strat = pd.concat([
        full_time.sample(n=35, replace=False),
        part_time.sample(n=______, replace=False)
    ])
    stratified_means.append(s_strat["wellbeing"].mean())

print(f"Simple sample SD of estimates:     {np.std(simple_means):.3f}")
print(f"Stratified sample SD of estimates: {np.std(stratified_means):.3f}")


# Exercise 10: Power for a correlation via Monte Carlo simulation
# Estimate the power of detecting a true Pearson correlation r = 0.20 at alpha = 0.05
# for sample sizes n in [100, 150, 200, 250]:
def simulate_correlation_power(n, r=0.20, n_sims=1000):
    significant_count = 0
    for _ in range(n_sims):
        x = np.random.normal(size=n)
        y = r * x + np.sqrt(1 - r**2) * np.random.normal(size=n)
        r_val, p_val = stats.pearsonr(x, y)
        if p_val < ______:
            significant_count += 1
    return significant_count / n_sims

for sample_n in [100, 150, 200, 250]:
    power_est = simulate_correlation_power(sample_n, r=0.20)
    print(f"Sample size {sample_n}: Estimated power = {power_est:.2f}")


# Exercise 11: A larger biased sample remains biased
# Voluntary response simulation with 400 students:
pop_wellbeing = first_sem["wellbeing"].dropna().to_numpy()
true_mean = pop_wellbeing.mean()
p_answer = expit((pop_wellbeing - true_mean) / 10)
p_answer /= p_answer.sum()

np.random.seed(5)
voluntary_estimates_400 = [
    np.random.choice(pop_wellbeing, size=______, replace=True, p=p_answer).mean()
    for _ in range(2000)
]

print(f"True population mean:             {true_mean:.2f}")
print(f"Biased sample (n=400) mean:       {np.mean(voluntary_estimates_400):.2f}")
print(f"Standard error of estimate:       {np.std(voluntary_estimates_400):.3f}")


# ==============================================================================
# C. CHECK YOUR UNDERSTANDING
# Answer in your own words, then compare with the answers in solutions.py.
# ==============================================================================

# 1. Why must a hypothesis be stated before the data is analysed?
# 2. A statistical test rejects the null hypothesis. What has it NOT shown?
# 3. What is the difference between reliability and validity?
# 4. Why is a larger biased sample still biased?
# 5. What does random assignment balance that post-hoc statistical adjustment cannot?


# ==============================================================================
# D. DO IT YOURSELF
# Open tasks: no starter code, no hints, and no answers. Write your own code
# under each task, as you would for a thesis.
# ==============================================================================

# Task 1: For a research topic in your own field, state:
# - Research topic & problem
# - Specific research question (descriptive, relational, or causal)
# - Falsifiable alternative hypothesis (H1) and corresponding null hypothesis (H0)
# - Specific empirical finding that would count against H1.


# Task 2: Create an analysis plan DataFrame for two hypotheses with columns:
# ['hypothesis', 'outcome', 'predictors', 'statistical_test', 'decision_rule']


# Task 3: Check the balance of the workshop invitation across ALL baseline variables
# in students in a single clean summary table.


# Task 4: In an experiment with 10 participants per group, find the smallest effect
# size (Cohen's d) detectable with 80% power at alpha = 0.05 using TTestIndPower.
# What limitation does this impose on small pilot studies?
