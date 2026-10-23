# FROM DATA TO THESIS: Using Python for Non-Technical
# Playground, Chapter 17: Reproducible Research
#
# This script holds the Python exercises for Chapter 17. The Quarto and Shiny
# tasks (Exercises 2, 3, 4, and 8) are described in exercises.txt.
#   A. Practise the chapter       the book's exercises, with blanks (______) to fill
#   B. Go further                 new exercises beyond the book
#   C. Check your understanding   short questions; answers in solutions.py
#   D. Do it yourself             open tasks with no starter code and no answers
#
# Try each exercise yourself before you look at solutions.py.

import pandas as pd
import numpy as np
import scipy.stats as stats
import statsmodels.api as sm

students = pd.read_csv("students.csv")
semesters = pd.read_csv("semesters.csv")


# ==============================================================================
# A. PRACTISE THE CHAPTER
# ==============================================================================

# Exercise 1: A sentence that writes itself (as inline code would)
sleep = [6.5, 7.0, 5.5]
print(f"My three friends slept {np.mean(sleep):.______} hours on average last night.")
sleep[1] = 8.0
print(f"My three friends slept {np.mean(sleep):.______} hours on average last night.")


# Exercises 2 to 4: see exercises.txt


# Exercise 5: The smallest cells
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
    print(f"Removed: {drop:<14} Smallest cell: {______}")


# Exercise 6: A sixth analysis (excluding the five highest scores)
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
        "any_analysis": any(p < 0.05 for p in ______)
    }

np.random.seed(17)
sim_results = pd.DataFrame([forking_paths() for _ in range(1000)])
print("Forking paths simulation results:")
print(sim_results.mean())


# ==============================================================================
# B. GO FURTHER
# ==============================================================================

# Exercise 7: How many forking paths? (1, 2, 5, and 10 analyses)
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
    print(f"Analyses tried: {k:<2} False positive rate: {any_sig:.3f} (If independent: {______:.3f})")


# Exercise 9: Grouping instead of removing
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
print("Small cells (< 5) remaining:", (grouped["n"] < ______).sum())


# Exercise 10: Recording the software
import sys
import statsmodels
py_ver = sys.version.split()[0]
sm_ver = statsmodels.______
print(f"Analyses were carried out in Python version {py_ver}, with modeling in statsmodels version {sm_ver}.")


# ==============================================================================
# C. CHECK YOUR UNDERSTANDING
# Answer in your own words, then compare with the answers in solutions.py.
# ==============================================================================

# 1. What is the difference between a reproducible result and a replicable one?
# 2. Why should numbers in the text of a thesis not be typed by hand?
# 3. What does requirements.txt / lockfile record, and why does it matter?
# 4. Why is removing names and student numbers not enough to anonymise data?
# 5. What does preregistration protect against?


# ==============================================================================
# D. DO IT YOURSELF
# Open tasks: no starter code, no hints, and no answers.
# ==============================================================================

# Task 1: Write a reporting sentence as code, with every number (means,
# difference, test statistic, p-value, sample sizes) calculated and formatted
# using f-strings, rounded as a journal would print them.

# Task 2: see exercises.txt (a Quarto report and a second dashboard input).

# Task 3: Write a preregistration for a study of your own with the AsPredicted
# headings: hypotheses, dependent variable, conditions, analyses, exclusions,
# sample size, and anything else.
