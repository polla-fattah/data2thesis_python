# FROM DATA TO THESIS: Using Python for Non-Technical
# Playground, Chapter 14: Advanced Clustering
#
# Four parts, as on the playground page:
#   A. Practise the chapter       the book's exercises, with GaussianMixture and DBSCAN
#   B. Go further                 new exercises beyond the book
#   C. Check your understanding   short questions; answers in solutions.py
#   D. Do it yourself             open tasks with no starter code and no answers
#
# Try each exercise yourself before you look at solutions.py.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.cluster.hierarchy import linkage, fcluster

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, adjusted_rand_score
from sklearn.neighbors import NearestNeighbors

# Load data
students = pd.read_csv("students.csv")
semesters = pd.read_csv("semesters.csv")
questionnaire = pd.read_csv("questionnaire.csv")

q = questionnaire.copy()
q['stress_4'] = 6 - q['stress_4']
q['stress'] = q[[f'stress_{i}' for i in range(1, 7)]].mean(axis=1)
q['support'] = q[[f'support_{i}' for i in range(1, 7)]].mean(axis=1)
q['satisfaction'] = q[[f'satisfaction_{i}' for i in range(1, 5)]].mean(axis=1)
scores = q[['student_id', 'stress', 'support', 'satisfaction']]

profiles = (
    semesters.groupby('student_id')[['sleep_hours', 'study_hours', 'caffeine_mg', 'exercise_days']]
    .mean()
    .reset_index()
    .merge(scores, on='student_id')
    .dropna()
)

features = ['sleep_hours', 'study_hours', 'caffeine_mg', 'exercise_days', 'stress', 'support', 'satisfaction']
scaler = StandardScaler()
profile_data = scaler.fit_transform(profiles[features])

profile_gmm = GaussianMixture(n_components=3, covariance_type='full', random_state=123).fit(profile_data)
kmeans_clusters = KMeans(n_clusters=4, n_init=25, random_state=123).fit(profile_data)
profiles['gmm_cluster'] = profile_gmm.predict(profile_data) + 1
profiles['kmeans_cluster'] = kmeans_clusters.labels_ + 1


# ==============================================================================
# A. PRACTISE THE CHAPTER
# ==============================================================================

# Exercise 1: Four mixture profiles
# Fit GaussianMixture with 4 components; describe the clusters and compare with k-means.
gmm4 = GaussianMixture(n_components=______, covariance_type='full', random_state=123).fit(profile_data)
profiles['gmm4_cluster'] = gmm4.predict(profile_data) + 1

summary4 = profiles.groupby('gmm4_cluster')[features].mean().round(1)
summary4['students'] = profiles['gmm4_cluster'].value_counts().sort_index()
print(summary4)

print("Crosstab 3 vs 4 GMM components:")
print(pd.crosstab(profiles['gmm_cluster'], profiles['gmm4_cluster']))
print("ARI GMM-4 vs K-means-4:", round(adjusted_rand_score(profiles['gmm4_cluster'], profiles['kmeans_cluster']), 2))


# Exercise 2: Clear members (probability above 0.95)
probs = profile_gmm.predict_proba(profile_data)
certainty = probs.max(axis=______)
print(f"Students with prob > 0.95: {np.sum(certainty > 0.95)} ({np.mean(certainty > 0.95)*100:.1f}%)")


# Exercise 3: DBSCAN with different eps (min_samples = 8)
for eps in [1.2, 1.6, 2.0, 2.4]:
    db = DBSCAN(eps=eps, min_samples=______).fit(profile_data)
    labels = db.labels_
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise = int(np.sum(labels == -1))
    print(f"eps={eps:.1f} -> Clusters: {n_clusters}, Noise points: {n_noise}")


# Exercise 4: The profiles without the noise students
db = DBSCAN(eps=2.0, min_samples=8).fit(profile_data)
keep = db.labels_ ______ -1
gmm_kept = GaussianMixture(n_components=3, covariance_type='full', random_state=123).fit(profile_data[keep])
profiles_kept = profiles[keep].copy()
profiles_kept['cluster_kept'] = gmm_kept.predict(profile_data[keep]) + 1

print("ARI before and after dropping noise:", round(adjusted_rand_score(profiles.loc[keep, 'gmm_cluster'], profiles_kept['cluster_kept']), 2))


# Exercise 5: Mixture model against hierarchical clustering (Ward, 3 clusters)
Z = linkage(profile_data, method='ward')
hierarchical = fcluster(Z, t=3, criterion='maxclust')

ari_hier = ______(profiles['gmm_cluster'], hierarchical)
print(f"ARI (GMM vs Hierarchical): {ari_hier:.2f}")
print(pd.crosstab(profiles['gmm_cluster'], hierarchical, rownames=['GMM'], colnames=['Hierarchical']))


# Exercise 6: Profiles and final GPA
final_gpa = semesters[(semesters['semester'] == 4) & semesters['gpa'].notna()][['student_id', 'gpa']].rename(columns={'gpa': 'final_gpa'})
prof_gpa = profiles.merge(final_gpa, on='student_id')
print(prof_gpa.groupby('gmm_cluster').agg(
    students=('student_id', 'count'),
    final_gpa=('final_gpa', lambda x: round(np.mean(x), 2)),
    study=('study_hours', lambda x: round(np.mean(x), 1)),
    stress=('stress', lambda x: round(np.mean(x), 1))
))


# Exercise 7: A gap between the groups (long group moved to y = 3)
for long_y in [1.4, ______]:
    np.random.seed(8)
    r_pts = np.random.normal(loc=[0, 0], scale=[0.4, 0.4], size=(100, 2))
    l_pts = np.random.normal(loc=[3, long_y], scale=[2.0, 0.2], size=(100, 2))
    s_pts = np.random.uniform(low=[-2, -2], high=[7, 4], size=(15, 2))
    sim_xy = np.vstack([r_pts, l_pts, s_pts])
    sim_truth = np.array(['Round'] * 100 + ['Long'] * 100 + ['Scattered'] * 15)
    real = sim_truth != 'Scattered'
    
    km = KMeans(n_clusters=2, n_init=25, random_state=123).fit(sim_xy).labels_
    gm = GaussianMixture(n_components=2, covariance_type='full', random_state=123).fit(sim_xy).predict(sim_xy)
    db = DBSCAN(eps=0.5, min_samples=5).fit(sim_xy).labels_
    
    n_db_c = len(set(db[real])) - (1 if -1 in db[real] else 0)
    print(f"long_y={long_y} | KMeans ARI: {adjusted_rand_score(sim_truth[real], km[real]):.2f} | GMM ARI: {adjusted_rand_score(sim_truth[real], gm[real]):.2f} | DBSCAN ARI: {adjusted_rand_score(sim_truth[real], db[real]):.2f} | DBSCAN clusters: {n_db_c}")


# ==============================================================================
# B. GO FURTHER (pure Python & NumPy)
# ==============================================================================

# Exercise 8: Membership probabilities by hand (Old Faithful)
wait = np.array([50, 67, 85])
short = 0.36 * norm.pdf(wait, loc=54.6, scale=5.9)
long_ = 0.64 * norm.pdf(wait, loc=______, scale=5.9)
p_short = short / (short + ______)
print("Hand membership probability for short wait:", np.round(p_short, 3))


# Exercise 9: Groups of different sizes and densities
np.random.seed(4)
g_large = np.random.normal(loc=[0, 0], scale=[1.2, 1.2], size=(300, 2))
g_small = np.random.normal(loc=[3, 0], scale=[0.3, 0.3], size=(30, 2))
g_medium = np.random.normal(loc=[0, 4.5], scale=[0.5, 0.5], size=(60, 2))
g_xy = np.vstack([g_large, g_small, g_medium])
g_truth = np.array(['large'] * 300 + ['small'] * 30 + ['medium'] * 60)

km_g = KMeans(n_clusters=3, n_init=25, random_state=123).fit(g_xy).labels_
print("Different densities - KMeans ARI:", round(adjusted_rand_score(g_truth, km_g), 2))

for eps in [0.3, 0.4, 0.5, 0.6]:
    db_g = DBSCAN(eps=eps, min_samples=5).fit(g_xy).labels_
    print(f"eps={eps} -> DBSCAN ARI: {adjusted_rand_score(g_truth, db_g):.2f}")

gmm_g = GaussianMixture(n_components=3, covariance_type='full', random_state=123).fit(g_xy).predict(g_xy)
print("Different densities - GMM ARI:", round(adjusted_rand_score(g_truth, gmm_g), 2))


# Exercise 10: DBSCAN on Old Faithful
faithful = pd.read_csv("faithful.csv") if "faithful.csv" in dt.EXAMPLE_FILES else dt.load_faithful()
geyser_scaled = StandardScaler().fit_transform(faithful[['eruptions', 'waiting']])

for eps in [0.1, 0.2, 0.3, 0.5]:
    db = DBSCAN(eps=eps, min_samples=5).fit(geyser_scaled).labels_
    n_c = len(set(db)) - (1 if -1 in db else 0)
    print(f"Geyser eps={eps} -> clusters: {n_c}, noise: {np.sum(db == -1)}")

db_geyser = DBSCAN(eps=0.3, min_samples=5).fit(geyser_scaled).labels_
print(faithful.groupby(db_geyser)['waiting'].agg(['count', 'mean']).round(1))


# Exercise 11: Earthquakes near Fiji
quakes = pd.read_csv("quakes.csv") if "quakes.csv" in dt.EXAMPLE_FILES else dt.load_quakes()
quake_coords = StandardScaler().fit_transform(quakes[['long', 'lat']])

km_q = KMeans(n_clusters=2, n_init=25, random_state=1).fit(quake_coords).labels_
db_q = DBSCAN(eps=0.3, min_samples=10).fit(quake_coords).labels_

print("Quakes crosstab KMeans vs DBSCAN:")
print(pd.crosstab(km_q, db_q, rownames=['KMeans'], colnames=['DBSCAN']))
print("Quakes ARI:", round(adjusted_rand_score(km_q, ______), 2))


# ==============================================================================
# C. CHECK YOUR UNDERSTANDING
# Answer in your own words, then compare with the answers in solutions.py.
# ==============================================================================

# 1. What are the three definitions of a group used by k-means, mixture
#    models, and DBSCAN?
# 2. What is the difference between hard and soft membership?
# 3. What does BIC compare when choosing the number of clusters?
# 4. Why did DBSCAN find only one cluster of students in the chapter?
# 5. How can a clustering be judged when there is no answer key?


# ==============================================================================
# D. DO IT YOURSELF
# Open tasks: no starter code, no hints, and no answers. Write your own code
# under each task, as you would for a thesis.
# ==============================================================================

# Task 1: Find profiles with a mixture model on variables of your choice;
# report the share of clear members, and describe the uncertain students.



# Task 2: Check the stability of the three profiles on 20 bootstrap samples,
# comparing each with the full-data profiles with adjusted_rand_score().



# Task 3: Write the clustering paragraph of a methods section, reporting every
# choice (variables, scaling, method, number of clusters, validation).
