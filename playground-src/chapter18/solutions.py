# FROM DATA TO THESIS: Using Python for Non-Technical
# Playground, Chapter 18: Solutions
#
# One possible solution for each exercise in parts A and B, and model answers
# for part C. Part D has no solutions: the tasks are open. Exercise 4 calls a
# language model only if one is available; otherwise it uses the saved run.

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
# In pandas groupby().mean(), missing values (NaN) are skipped automatically:
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
print("np.nanmean([6, 7, np.nan]):", np.nanmean([6, 7, np.nan]))


# Exercise 2: Three more keywords
check = open_responses_coded.copy()
check["keyword_theme"] = check["biggest_challenge"].apply(code_by_keywords)

print(f"Original Agreement: {accuracy_score(check['theme'], check['keyword_theme']):.3f}")
print(f"Original Kappa:     {cohen_kappa_score(check['theme'], check['keyword_theme']):.3f}")

new_keywords = dict(keywords)
new_keywords["Workload"] = r"\b(time|deadline|workload|too much|assignment|reading|busy|thesis|work|course)"
new_keywords["Isolation"] = r"\b(lonel|alone|friends|outsider|miss (home|my)|far from|know no one|isolat|on my own)"

check["keyword_theme_new"] = check["biggest_challenge"].apply(lambda t: code_by_keywords(t, new_keywords))
print(f"New Agreement:      {accuracy_score(check['theme'], check['keyword_theme_new']):.3f}")
print(f"New Kappa:          {cohen_kappa_score(check['theme'], check['keyword_theme_new']):.3f}")


# Exercise 3: Reading the disagreements
disagreements = check[check["theme"] != check["keyword_theme"]]
print(f"Number of disagreements: {len(disagreements)}")
sample_dis = disagreements.sample(10, random_state=18)[["biggest_challenge", "theme", "keyword_theme"]]
print(sample_dis)


# Exercise 4: Evaluating the language model's coding
model_check = open_responses_coded.merge(ai_coding, on="student_id")
print(f"Model Agreement: {accuracy_score(model_check['theme'], model_check['ai_theme']):.3f}")
print(f"Model Kappa:     {cohen_kappa_score(model_check['theme'], model_check['ai_theme']):.3f}")

cm = pd.crosstab(model_check["theme"], model_check["ai_theme"], rownames=["Hand"], colnames=["Model"])
print("Confusion Matrix:")
print(cm)


# Exercise 5: A methods paragraph for AI coding in your thesis
# Model answer:
# "Qualitative responses to the open-ended survey question were coded into seven
# predetermined thematic categories using a local large language model (Gemma 4 e4b,
# via Ollama, temperature = 0.0) guided by a structured codebook and Pydantic schema.
# To validate the automated coding, a random sample of 200 responses was independently
# hand-coded by the researcher. Inter-coder agreement between hand coding and the model
# was 90.0% (Cohen's kappa = 0.874), indicating almost perfect agreement. All prompt
# templates, temperature settings, and raw response tables are archived in the online
# supplementary materials."


# Exercise 6: A coder who always says Workload
coder_a = ["Workload"] * 16 + ["Family"] * 4
coder_b = ["Workload"] * 20
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
    print(f"Workload: {n_workload:<2} Agreement: {acc:.3f} Kappa: {kap:.3f}")


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
# 1. Handling missing values:
print("Age mean (pandas skips NaN):", students["age"].mean().round(1))
# 2. Case sensitivity in category filters:
print("Education (lowercase):", len(students[students["faculty"] == "education"]))
print("Education (proper case):", len(students[students["faculty"] == "Education"]))
# 3. Within-group vs global percentages:
pt_pct = (
    students.groupby("faculty")["study_mode"]
    .value_counts(normalize=True)
    .unstack()
    .round(3) * 100
)
print("Part-time percentage within each faculty:")
print(pt_pct["Part-time"])


# ==============================================================================
# C. CHECK YOUR UNDERSTANDING: model answers
# ==============================================================================

# 1. Why can raw agreement between two coders be misleading?
#    Some agreement happens purely by chance, especially when one category or theme
#    is disproportionately common. Cohen's kappa adjusts for this by subtracting
#    expected chance agreement.
#
# 2. What is a hallucination?
#    A confident, fluent, but factually false statement generated by a language model,
#    such as an invented Python library function, non-existent parameter, or fabricated citation.
#
# 3. Why is a temperature of 0 used when a model codes research data?
#    At temperature 0, the model acts deterministically, picking the token with the highest
#    probability, which ensures reproducible and consistent thematic coding across runs.
#
# 4. What must be recorded so that AI coding can be reproduced and checked?
#    Provider, exact model name and version hash, date of access, system prompts, codebook,
#    temperature, parameter configurations, and the full raw output log.
#
# 5. When must data not be sent to an online model?
#    When data contains identifiable personal information, confidential institutional records,
#    or sensitive participant responses, unless explicit ethics committee approval and consent
#    have cleared commercial third-party cloud processing. A local model (e.g. Ollama) avoids this.


# ==============================================================================
# D. DO IT YOURSELF
# Open tasks: no starter code, no hints, and no answers.
# ==============================================================================
