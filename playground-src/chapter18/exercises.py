# FROM DATA TO THESIS: Using Python for Non-Technical
# Playground, Chapter 18: Using AI with Python
#
# Four parts, as on the playground page:
#   A. Practise the chapter       the book's exercises, with blanks (______) to fill
#   B. Go further                 new exercises beyond the book
#   C. Check your understanding   short questions; answers in solutions.py
#   D. Do it yourself             open tasks with no starter code and no answers
#
# Try each exercise yourself before you look at solutions.py.

import pandas as pd
import numpy as np
import re
from sklearn.metrics import accuracy_score, cohen_kappa_score

students = pd.read_csv("students.csv")
semesters = pd.read_csv("semesters.csv")
open_responses = pd.read_csv("open_responses.csv")
open_responses_coded = pd.read_csv("open_responses_coded.csv")
ai_coding = pd.read_csv("ai_coding_results.csv")

keywords = {
    "Supervision": r"\b(supervis|feedback|guidance|meeting)",
    "Workload": r"\b(time|deadline|workload|too much|assignment|reading|busy)",
    "Finances": r"\b(money|fee|scholarship|rent|afford|salary|income|funding|stipend|loan)",
    "Family": r"\b(famil|child|kid|son\b|daughter|baby|parent|mother|father|husband|wife)",
    "Health": r"\b(sleep|tired|stress|anxi|health|ill\b|burnout|headache|coffee|exhaust)",
    "Isolation": r"\b(lonel|alone|friends|outsider|miss (home|my)|far from|know no one)",
    "Other": r"\b(ethic|participant|statistic|library|procedure|english|power cut|laptop|internet|software)"
}
themes = list(keywords.keys())

def code_by_keywords(text, dictionary=keywords):
    text_lower = str(text).lower()
    hits = {theme: len(re.findall(pat, text_lower)) for theme, pat in dictionary.items()}
    max_hits = max(hits.values())
    if max_hits == 0:
        return "Other"
    for theme, count in hits.items():
        if count == max_hits:
            return theme


# ==============================================================================
# A. PRACTISE THE CHAPTER
# ==============================================================================

# Exercise 1: Checking an assistant's code
# Plausible suggestion for average sleep by faculty and semester:
avg_sleep = (
    semesters.merge(students, on="student_id")
    .groupby(["faculty", "semester"])["sleep_hours"]
    .mean()
    .reset_index()
)
print("Average sleep (pandas skips NaN automatically):")
print(avg_sleep.head())

# In numpy or custom calculations, check NaN handling:
print("np.mean([6, 7, np.nan]):", np.mean([6, 7, np.nan]))
print("np.nanmean([6, 7, np.nan]):", np.______([6, 7, np.nan]))


# Exercise 2: Three more keywords
check = open_responses_coded.copy()
check["keyword_theme"] = check["biggest_challenge"].apply(code_by_keywords)

print(f"Original Agreement: {accuracy_score(check['theme'], check['keyword_theme']):.3f}")
print(f"Original Kappa:     {cohen_kappa_score(check['theme'], check['keyword_theme']):.3f}")

new_keywords = dict(keywords)
new_keywords["Workload"] = r"\b(time|deadline|workload|too much|assignment|reading|busy|thesis|work|______)"
new_keywords["Isolation"] = r"\b(lonel|alone|friends|outsider|miss (home|my)|far from|know no one|isolat|on my own)"

check["keyword_theme_new"] = check["biggest_challenge"].apply(lambda t: code_by_keywords(t, new_keywords))
print(f"New Agreement:      {accuracy_score(check['theme'], check['keyword_theme_new']):.3f}")
print(f"New Kappa:          {cohen_kappa_score(check['theme'], check['keyword_theme_new']):.3f}")


# Exercise 3: Reading the disagreements
disagreements = check[check["theme"] != check["keyword_theme"]]
print(f"Number of disagreements: {len(disagreements)}")
np.random.seed(18)
sample_dis = disagreements.sample(10, random_state=18)[["biggest_challenge", "theme", "keyword_theme"]]
print(sample_dis)


# Exercise 4: Evaluating the language model's coding
model_check = open_responses_coded.merge(ai_coding, on="student_id")
print(f"Model Agreement: {accuracy_score(model_check['theme'], model_check['ai_theme']):.3f}")
print(f"Model Kappa:     {cohen_kappa_score(model_check['theme'], model_check['______']):.3f}")

cm = pd.crosstab(model_check["theme"], model_check["ai_theme"], rownames=["Hand"], colnames=["Model"])
print("Confusion Matrix:")
print(cm)


# Exercise 5: A methods paragraph for AI coding in your thesis
# (write it as comments)


# Exercise 6: A coder who always says Workload
coder_a = ["Workload"] * 16 + ["Family"] * 4
coder_b = ["______"] * 20
print(f"Agreement: {accuracy_score(coder_a, coder_b):.2f}")
print(f"Kappa:     {cohen_kappa_score(coder_a, coder_b):.2f}")


# ==============================================================================
# B. GO FURTHER
# ==============================================================================

# Exercise 7: Kappa with three themes as Workload becomes more common
for n_workload in [10, 20, 40, 80]:
    c_a = ["Workload"] * n_workload + ["Family"] * 6 + ["Finances"] * 4
    c_b = (
        ["Workload"] * (n_workload - 2) + ["Family", "Finances"] +
        ["Family"] * 5 + ["Workload"] +
        ["Finances"] * 3 + ["Workload"]
    )
    acc = accuracy_score(c_a, c_b)
    kap = cohen_kappa_score(c_a, c_b)
    print(f"Workload: {n_workload:<2} Agreement: {acc:.3f} Kappa: {______:.3f}")


# Exercise 8: The dictionary's most common confusion
errors = check[check["theme"] != check["keyword_theme"]]
confusion_top = (
    errors.groupby(["theme", "keyword_theme"])
    .size()
    .reset_index(name="count")
    .sort_values("count", ascending=False)
)
print("Top 3 confusions:")
print(confusion_top.head(3))


# Exercise 9: Long answers and short answers
check["words"] = check["biggest_challenge"].str.split().str.len()
print("Mean words by theme:")
print(check.groupby("theme")["words"].agg(["count", "mean"]).round(1).sort_values("mean", ascending=False))

check["correct"] = check["theme"] == check["keyword_theme"]
print("Mean words by accuracy:")
print(check.groupby("correct")["words"].mean().round(1))


# Exercise 10: Three mistakes an assistant might make
# 1. Handling missing values
print("Age mean:", students["age"].mean())
# 2. Case sensitivity in category filters
print("Education (lowercase):", len(students[students["faculty"] == "education"]))
print("Education (proper case):", len(students[students["faculty"] == "Education"]))
# 3. Within-group vs global percentages
pt_pct = (
    students.groupby("faculty")["study_mode"]
    .value_counts(normalize=True)
    .unstack()
    .round(3) * 100
)
print("Part-time percentage within each faculty:")
print(pt_pct["Part-time"])


# ==============================================================================
# C. CHECK YOUR UNDERSTANDING
# Answer in your own words, then compare with solutions.py.
# ==============================================================================

# 1. Why can raw agreement between two coders be misleading?
# 2. What is a hallucination?
# 3. Why is a temperature of 0 used when a model codes research data?
# 4. What must be recorded so that AI coding can be reproduced and checked?
# 5. When must data not be sent to an online model?


# ==============================================================================
# D. DO IT YOURSELF
# Open tasks: no starter code, no hints, and no answers.
# ==============================================================================

# Task 1: Invent an open question and ten answers, write a codebook of four or
# five themes, code the answers yourself, have a peer or model code them, and
# calculate Cohen's kappa.

# Task 2: Code 20 answers with a local model (Ollama), refine one theme definition,
# and observe how agreement changes.

# Task 3: Write the disclosure paragraph for using AI in your own thesis.
