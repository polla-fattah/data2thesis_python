# FROM DATA TO THESIS: Using Python for Non-Technical
# Playground, Chapter 9: Multivariate Statistical Methods
#
# Four parts, as on the playground page:
#   A. Practise the chapter       the book's exercises, with blanks (______) to fill
#   B. Go further                 new exercises beyond the book
#   C. Check your understanding   short questions; answers in solutions.py
#   D. Do it yourself             open tasks with no starter code and no answers
#
# Try each exercise yourself before you look at solutions.py.

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from statsmodels.multivariate.factor import Factor

semesters = pd.read_csv("semesters.csv")
questionnaire = pd.read_csv("questionnaire.csv")
items = questionnaire.drop(columns=["student_id"])

# Reverse stress_4 and calculate scale scores
q = questionnaire.copy()
q["stress_4"] = 6 - q["stress_4"]
scores = pd.DataFrame({
    "student_id": q["student_id"],
    "stress": q.filter(like="stress_").mean(axis=1),
    "burnout": q.filter(like="burnout_").mean(axis=1),
    "support": q.filter(like="support_").mean(axis=1),
    "satisfaction": q.filter(like="satisfaction_").mean(axis=1),
})

lifestyle = (
    semesters
    .groupby("student_id")[["sleep_hours", "study_hours", "caffeine_mg", "exercise_days"]]
    .mean()
    .reset_index()
)

profiles = lifestyle.merge(scores.drop(columns=["burnout"]), on="student_id").dropna()
profile_features = profiles.drop(columns=["student_id"])
scaler = StandardScaler()
profile_scaled = scaler.fit_transform(profile_features)


# ==============================================================================
# A. PRACTISE THE CHAPTER
# ==============================================================================

# Exercise 1: PCA of the support items
# How much variation does the first component capture? What does that suggest?
support_items = items.filter(like="support_").dropna()
scaler_sup = StandardScaler()
support_scaled = scaler_sup.fit_transform(support_items)
pca_support = PCA()
pca_support.______(support_scaled)
print("Explained variance ratio:", np.round(pca_support.explained_variance_ratio_, 3))


# Exercise 2: Three factors instead of four
# Which scales share a factor, and why?
items_complete = items.dropna()
fa3 = Factor(items_complete, n_factor=______, method="pa").fit()
fa3.rotate("promax")
loadings3 = pd.DataFrame(fa3.loadings, index=items.columns, columns=["F1", "F2", "F3"])
print(loadings3.mask(loadings3.abs() < 0.3, "").to_string())


# Exercise 3: Cronbach's alpha without reversing stress_4
def cronbach_alpha(df):
    data = df.dropna()
    k = data.shape[1]
    item_vars = data.var(axis=0, ddof=1).sum()
    total_var = data.sum(axis=1).var(ddof=1)
    return (k / (k - 1)) * (1 - item_vars / total_var)

stress_items = questionnaire.filter(like="stress_")
print("Raw alpha:", round(cronbach_alpha(stress_items), 2))

stress_reversed = stress_items.copy()
stress_reversed["stress_4"] = ______ - stress_reversed["stress_4"]
print("Reversed alpha:", round(cronbach_alpha(stress_reversed), 2))


# Exercise 4: Three clusters
# Describe the clusters; which profiles of the 4-cluster solution merged?
kmeans3 = KMeans(n_clusters=______, n_init=25, random_state=123)
profiles_k3 = profiles.copy()
profiles_k3["cluster_3"] = kmeans3.fit_predict(profile_scaled)
print(profiles_k3.groupby("cluster_3").mean().round(1))

kmeans4 = KMeans(n_clusters=4, n_init=25, random_state=123)
profiles_k3["cluster_4"] = kmeans4.fit_predict(profile_scaled)
print(pd.crosstab(profiles_k3["cluster_3"], profiles_k3["cluster_4"]))


# Exercise 5: Justifying the number of clusters
# Two or three sentences for a thesis methods section.
# Write your answer in comments below.


# Exercise 6: Noisier items
# With sd = 2, how many items are needed for a correlation of at least 0.8?
np.random.seed(42)
true_stress = np.random.normal(size=600)
simulated_items = np.column_stack([true_stress + np.random.normal(scale=______, size=600) for _ in range(20)])

corrs = {}
for k in range(1, 21):
    composite = simulated_items[:, :k].mean(axis=1)
    r = np.corrcoef(composite, true_stress)[0, 1]
    corrs[f"{k} items"] = round(r, 2)
print(corrs)


# ==============================================================================
# B. GO FURTHER
# ==============================================================================

# Exercise 7: When alpha misleads
# Add the same "mood" noise to every item: compare alpha, and the correlation
# with the true stress level, with and without it.
np.random.seed(42)
true_stress = np.random.normal(size=600)
items_clean = np.column_stack([true_stress + np.random.normal(size=600) for _ in range(6)])
mood = np.random.normal(size=600)
items_mood = items_clean + ______[:, np.newaxis]

df_clean = pd.DataFrame(items_clean)
df_mood = pd.DataFrame(items_mood)

alpha_clean = cronbach_alpha(df_clean)
alpha_mood = cronbach_alpha(df_mood)
r_clean = np.corrcoef(items_clean.mean(axis=1), true_stress)[0, 1]
r_mood = np.corrcoef(items_mood.mean(axis=1), true_stress)[0, 1]

print(f"Clean: alpha = {alpha_clean:.2f}, r = {r_clean:.2f}")
print(f"Mood:  alpha = {alpha_mood:.2f}, r = {r_mood:.2f}")


# Exercise 8: PCA of the four scale scores
scale_scores = scores.drop(columns=["student_id"]).dropna()
scores_scaled = StandardScaler().fit_transform(scale_scores)
scores_pca = PCA()
scores_pca.fit(scores_scaled)
print("Explained variance ratio:", np.round(scores_pca.explained_variance_ratio_, 2))
rot_df = pd.DataFrame(
    scores_pca.components_.T,
    index=scale_scores.columns,
    columns=[f"PC{i+1}" for i in range(4)]
)
print(rot_df.round(2))


# Exercise 9: Clusters in random data
np.random.seed(1)
random_mat = np.random.uniform(size=profile_scaled.shape)
random_scaled = StandardScaler().fit_transform(random_mat)

km_rand = KMeans(n_clusters=4, n_init=25, random_state=1).fit(random_scaled)
km_real = KMeans(n_clusters=4, n_init=25, random_state=123).fit(profile_scaled)

totss_rand = ((random_scaled - random_scaled.mean(axis=0)) ** 2).sum()
totss_real = ((profile_scaled - profile_scaled.mean(axis=0)) ** 2).sum()

between_rand = totss_rand - km_rand.inertia_
between_real = totss_real - km_real.inertia_

print(f"Random explained variance: {between_rand / totss_rand:.2%}")
print(f"Real explained variance:   {between_real / totss_real:.2%}")


# Exercise 10: Why PCA scales the variables (USArrests)
usarrests = pd.read_csv("usarrests.csv")
arrests_data = usarrests.drop(columns=["State"], errors="ignore")
print("Variances:\n", arrests_data.var())

# Unscaled PCA
pca_unscaled = PCA().fit(arrests_data)
unscaled_loadings = pd.DataFrame(
    pca_unscaled.components_[:2].T,
    index=arrests_data.columns,
    columns=["PC1", "PC2"]
)
print("\nUnscaled Loadings:\n", unscaled_loadings.round(2))

# Scaled PCA
pca_scaled = PCA().fit(StandardScaler().fit_transform(arrests_data))
scaled_loadings = pd.DataFrame(
    pca_scaled.components_[:2].T,
    index=arrests_data.columns,
    columns=["PC1", "PC2"]
)
print("\nScaled Loadings:\n", scaled_loadings.round(2))
print("Scaled Explained Variance:", np.round(pca_scaled.explained_variance_ratio_, 2))


# ==============================================================================
# C. CHECK YOUR UNDERSTANDING
# Answer in your own words, then compare with the answers in solutions.py.
# ==============================================================================

# 1. Why does a questionnaire use several items for each construct?
# 2. What is the difference between PCA and factor analysis?
# 3. An item loads 0.45 on one factor and 0.40 on another. What does this
#    cross-loading mean?
# 4. A scale has a Cronbach's alpha of 0.93. Does that show that it is valid?
# 5. Why should clusters not be described as natural groups of people?


# ==============================================================================
# D. DO IT YOURSELF
# Open tasks: no starter code, no hints, and no answers. Write your own code
# under each task, as you would for a thesis.
# ==============================================================================

# Task 1: Check the burnout scale fully: item correlations, Cronbach's alpha,
# and alpha with each item dropped. Write the one-sentence report.

# Task 2: Cluster the students on a different set of variables of your choice,
# choose the number of clusters, describe them, and argue whether they would be
# useful to a university.

# Task 3: Write the methods paragraph describing one scale: number of items, an
# example item, answer scale, scoring (with reversed items), and reliability,
# with the numbers calculated by code.

# Task 4: Run a PCA on USArrests or other multivariate datasets, decide how many
# components to keep, and interpret them.
