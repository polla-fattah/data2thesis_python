# FROM DATA TO THESIS: Using Python for Non-Technical
# Playground, Chapter 17: Solutions
#
# One possible solution for the Python exercises in parts A and B, and model answers
# for part C. The Quarto and Shiny tasks have finished versions in the
# solutions folder. Part D has no solutions: the tasks are open.

import pandas as pd
import numpy as np
import scipy.stats as stats
import statsmodels.api as sm

students = pd.read_csv("students.csv")
semesters = pd.read_csv("semesters.csv")


# ==============================================================================
# A. PRACTISE THE CHAPTER
# ==============================================================================

# Exercise 1: 6.3 hours, then 6.7 after the change
sleep = [6.5, 7.0, 5.5]
print(f"My three friends slept {np.mean(sleep):.1f} hours on average last night.")
sleep[1] = 8.0
print(f"My three friends slept {np.mean(sleep):.1f} hours on average last night.")


# Exercise 5: five cells below 5 (all part-time students with children; the
# smallest have 3). Smallest cell without faculty 21, without children 11,
# without study mode 10, without gender 7.
cells = (
    students.groupby(["faculty", "study_mode", "gender", "has_children"], observed=False)
    .size()
    .reset_index(name="n")
    .sort_values("n")
)
print("Smallest demographic cells:")
print(cells.head(6))
print("Cells with n < 5:", (cells["n"] < 5).sum())

demographics = ["faculty", "study_mode", "gender", "has_children"]
for drop in demographics:
    kept = [col for col in demographics if col != drop]
    smallest = students.groupby(kept, observed=False).size().min()
    print(f"Removed: {drop:<14} Smallest cell: {smallest}")


# Exercise 6: first analysis ~5.4%; any of six ~12.5% (10.9% with five)
def forking_paths():
    group = np.array(["A"] * 30 + ["B"] * 30)
    score = np.random.exponential(scale=10, size=60)
    covariate = np.random.normal(size=60)
    
    score_a = score[group == "A"]
    score_b = score[group == "B"]
    
    # 1. Standard t-test
    p_ttest = stats.ttest_ind(score_a, score_b).pvalue
    
    # 2. Outliers trimmed (|z| < 2)
    z = np.abs((score - np.mean(score)) / np.std(score, ddof=1))
    p_no_outliers = stats.ttest_ind(
        score[(z < 2) & (group == "A")], 
        score[(z < 2) & (group == "B")]
    ).pvalue
    
    # 3. Log scale
    p_log = stats.ttest_ind(np.log(score_a), np.log(score_b)).pvalue
    
    # 4. Rank test
    p_rank = stats.mannwhitneyu(score_a, score_b).pvalue
    
    # 5. With covariate
    X = sm.add_constant(np.column_stack([(group == "B").astype(int), covariate]))
    p_cov = sm.OLS(score, X).fit().pvalues[1]
    
    # 6. Exclude top five scores
    top_5_cutoff = np.sort(score)[-6]
    keep_mask = score <= top_5_cutoff
    p_no_top5 = stats.ttest_ind(
        score[keep_mask & (group == "A")], 
        score[keep_mask & (group == "B")]
    ).pvalue
    
    p_vals = [p_ttest, p_no_outliers, p_log, p_rank, p_cov, p_no_top5]
    return {
        "first_analysis": p_ttest < 0.05,
        "any_analysis": any(p < 0.05 for p in p_vals)
    }

np.random.seed(17)
sim_results = pd.DataFrame([forking_paths() for _ in range(1000)])
print("Forking paths simulation results:")
print(sim_results.mean())


# ==============================================================================
# B. GO FURTHER
# ==============================================================================

# Exercise 7: ~5.5%, 7.7%, 10.9%, 14% for 1, 2, 5, 10 analyses; independent
# tests would give 5%, 10%, 23%, 40%: related analyses add less each
def ten_paths():
    group = np.array(["A"] * 30 + ["B"] * 30)
    score = np.random.exponential(scale=10, size=60)
    covariate = np.random.normal(size=60)
    
    score_a = score[group == "A"]
    score_b = score[group == "B"]
    
    z = np.abs((score - np.mean(score)) / np.std(score, ddof=1))
    top_5_cutoff = np.sort(score)[-6]
    bot_5_cutoff = np.sort(score)[5]
    
    X = sm.add_constant(np.column_stack([(group == "B").astype(int), covariate]))
    p_cov = sm.OLS(score, X).fit().pvalues[1]
    
    return [
        stats.ttest_ind(score_a, score_b).pvalue,
        stats.mannwhitneyu(score_a, score_b).pvalue,
        stats.ttest_ind(np.log(score_a), np.log(score_b)).pvalue,
        stats.ttest_ind(score[(z < 2) & (group == "A")], score[(z < 2) & (group == "B")]).pvalue,
        p_cov,
        stats.ttest_ind(np.sqrt(score_a), np.sqrt(score_b)).pvalue,
        stats.ttest_ind(score[(z < 2.5) & (group == "A")], score[(z < 2.5) & (group == "B")]).pvalue,
        stats.ttest_ind(score[(score <= top_5_cutoff) & (group == "A")], score[(score <= top_5_cutoff) & (group == "B")]).pvalue,
        stats.ttest_ind(score[(score >= bot_5_cutoff) & (group == "A")], score[(score >= bot_5_cutoff) & (group == "B")]).pvalue,
        stats.ttest_ind(score_a, score_b, equal_var=True).pvalue
    ]

np.random.seed(17)
p_matrix = np.array([ten_paths() for _ in range(1000)])

tried = [1, 2, 5, 10]
for k in tried:
    any_sig = (p_matrix[:, :k] < 0.05).any(axis=1).mean()
    indep = 1 - (0.95 ** k)
    print(f"Analyses tried: {k:<2} False positive rate: {any_sig:.3f} (If independent: {indep:.3f})")


# Exercise 9: Grouping instead of removing (no cells < 5; smallest is 8)
students["faculty_group"] = np.where(
    students["faculty"].isin(["Natural Sciences", "Health Sciences"]),
    "Sciences",
    "Humanities and Social Sciences"
)
grouped = (
    students.groupby(["faculty_group", "study_mode", "gender", "has_children"], observed=False)
    .size()
    .reset_index(name="n")
    .sort_values("n")
)
print("Grouped demographic cells:")
print(grouped.head(4))
print("Small cells (< 5) remaining:", (grouped["n"] < 5).sum())


# Exercise 10: Recording the software
import sys
import statsmodels
py_ver = sys.version.split()[0]
sm_ver = statsmodels.__version__
print(f"Analyses were carried out in Python version {py_ver}, with modeling in statsmodels version {sm_ver}.")


# ==============================================================================
# C. CHECK YOUR UNDERSTANDING: model answers
# ==============================================================================

# 1. Reproducible: same data and code give the same result. Replicable: a new
#    study with new data finds the same thing.
# 2. Typed numbers go out of date when the data or analysis changes; inline
#    code recalculates them at every render.
# 3. requirements.txt / lockfile records exact package versions and dependencies,
#    so the environment can be faithfully restored on any computer.
# 4. Combinations of ordinary demographic variables can uniquely identify people;
#    small cells must be protected within the boundaries of ethical consent.
# 5. Preregistration prevents post-hoc analytical flexibility (the garden of
#    forking paths), clearly separating confirmatory testing from exploratory analysis.


# ==============================================================================
# D. DO IT YOURSELF
# No solutions: these tasks are open.
# ==============================================================================
