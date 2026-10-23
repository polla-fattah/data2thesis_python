# FROM DATA TO THESIS: Using Python for Non-Technical
# Playground, Chapter 11: Introduction to Machine Learning in Python
# Solutions

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd

from sklearn.model_selection import (
    train_test_split,
    StratifiedKFold,
    cross_val_score,
    GridSearchCV,
)
from sklearn.preprocessing import StandardScaler, OneHotEncoder, PolynomialFeatures
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_selection import VarianceThreshold
from sklearn.metrics import accuracy_score, roc_auc_score, root_mean_squared_error

students = pd.read_csv("students.csv")
students["employment"] = students["employment"].fillna("None")
semesters = pd.read_csv("semesters.csv")
questionnaire = pd.read_csv("questionnaire.csv")
titanic = pd.read_csv("titanic.csv")

scores = pd.DataFrame({
    "student_id": questionnaire["student_id"],
    "stress": questionnaire[["stress_1", "stress_2", "stress_3", "stress_5", "stress_6"]]
              .assign(stress_4=6 - questionnaire["stress_4"]).mean(axis=1),
    "burnout": questionnaire.filter(like="burnout_").mean(axis=1),
    "support": questionnaire.filter(like="support_").mean(axis=1),
    "satisfaction": questionnaire.filter(like="satisfaction_").mean(axis=1),
})

sem1 = semesters[semesters["semester"] == 1].drop(columns=["semester"])

dropout_data = (
    students
    .merge(scores, on="student_id")
    .merge(sem1, on="student_id")
    .drop(columns=["student_id", "supervisor_id", "workshop", "workshop_sessions"])
)

X = dropout_data.drop(columns=["considering_dropout"])
y = (dropout_data["considering_dropout"] == "Yes").astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=2026
)

num_cols = X.select_dtypes(include=[np.number]).columns.tolist()
cat_cols = X.select_dtypes(exclude=[np.number]).columns.tolist()

preprocessor = ColumnTransformer([
    ("num", Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ]), num_cols),
    ("cat", Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("ohe", OneHotEncoder(drop="first", sparse_output=False, handle_unknown="ignore"))
    ]), cat_cols)
])

logistic_pipe = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(max_iter=1000, random_state=2026))
])

cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=2026)


# ==============================================================================
# A. PRACTISE THE CHAPTER
# ==============================================================================

# Exercise 1: The model without the questionnaire
full_auc = cross_val_score(logistic_pipe, X_train, y_train, cv=cv, scoring="roc_auc").mean()

X_train_no_q = X_train.drop(columns=["stress", "burnout", "support", "satisfaction"])
num_cols_no_q = [c for c in num_cols if c not in ["stress", "burnout", "support", "satisfaction"]]

preprocessor_no_q = ColumnTransformer([
    ("num", Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ]), num_cols_no_q),
    ("cat", Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("ohe", OneHotEncoder(drop="first", sparse_output=False, handle_unknown="ignore"))
    ]), cat_cols)
])

pipe_no_q = Pipeline([
    ("preprocessor", preprocessor_no_q),
    ("classifier", LogisticRegression(max_iter=1000, random_state=2026))
])

no_q_auc = cross_val_score(pipe_no_q, X_train_no_q, y_train, cv=cv, scoring="roc_auc").mean()
print(f"Full CV AUC: {full_auc:.3f}, Without Questionnaire: {no_q_auc:.3f}")
# Removing the questionnaire drops the cross-validated AUC from ~0.806 to ~0.735:
# psychological indicators carry substantial predictive signal over demographics alone.


# Exercise 2: A different split (80/20, seed 7)
X_tr80, X_te80, y_tr80, y_te80 = train_test_split(
    X, y, test_size=0.20, stratify=y, random_state=7
)
logistic_pipe.fit(X_tr80, y_tr80)
prob_80 = logistic_pipe.predict_proba(X_te80)[:, 1]
auc_80 = roc_auc_score(y_te80, prob_80)

logistic_pipe.fit(X_train, y_train)
auc_75 = roc_auc_score(y_test, logistic_pipe.predict_proba(X_test)[:, 1])
print(f"80/20 Test AUC: {auc_80:.3f} vs 75/25 Test AUC: {auc_75:.3f}")
# The test AUC changes slightly (from ~0.843 to ~0.835) due to sample composition in the test set.


# Exercise 3: Tuning k-nearest neighbours
knn_pipe = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", KNeighborsClassifier())
])

param_grid = {"classifier__n_neighbors": [5, 11, 21, 41]}
knn_grid = GridSearchCV(knn_pipe, param_grid=param_grid, cv=cv, scoring="roc_auc")
knn_grid.fit(X_train, y_train)

print("Best k:", knn_grid.best_params_)
print(f"Best KNN CV AUC: {knn_grid.best_score_:.3f} vs Logistic CV AUC: {full_auc:.3f}")
# k=21 or k=41 achieves highest AUC (~0.79), slightly below logistic regression (~0.81).


# Exercise 4: Zero-variance predictors
X_prep = preprocessor.fit_transform(X_train)
zv_selector = VarianceThreshold(threshold=0.0)
X_zv = zv_selector.fit_transform(X_prep)

print("Columns before VarianceThreshold:", X_prep.shape[1])
print("Columns after VarianceThreshold: ", X_zv.shape[1])
# A zero-variance predictor is a column that takes exactly the same value for every row.
# Such features carry zero information and can cause numerical instability in models.


# Exercise 5: Explaining accuracy to an administrator
# In an imbalanced problem where only 15% of students consider dropping out, a naive baseline
# model that simply predicts "No" for every single student achieves 85% accuracy.
# However, this model identifies exactly zero students at risk, making it completely useless
# for proactive student support.


# Exercise 6: More training points (50 instead of 15)
true_curve = lambda x: np.sin(2 * x)

def make_points(n, seed=3):
    np.random.seed(seed)
    x = np.random.uniform(0, 3, n)
    y = true_curve(x) + np.random.normal(0, 0.3, n)
    return pd.DataFrame({"x": x, "y": y})

train_50 = make_points(50, seed=3)
test_points = make_points(1000, seed=4)
test_points = (
    test_points[
        (test_points["x"] >= train_50["x"].min()) &
        (test_points["x"] <= train_50["x"].max())
    ]
    .iloc[:300]
    .reset_index(drop=True)
)

errors_50 = []
for d in range(1, 13):
    m = make_pipeline(PolynomialFeatures(d), LinearRegression())
    m.fit(train_50[["x"]], train_50["y"])
    err = root_mean_squared_error(test_points["y"], m.predict(test_points[["x"]]))
    errors_50.append({"degree": d, "new_data_rmse": err})

errors_50_df = pd.DataFrame(errors_50)
print(errors_50_df.round(3))
print("Best degree with N=50:", errors_50_df.loc[errors_50_df["new_data_rmse"].idxmin(), "degree"])
# With 50 observations, the curve has enough support to fit degree 4 or 5 without exploding in variance.


# ==============================================================================
# B. GO FURTHER
# ==============================================================================

# Exercise 7: Data leakage
np.random.seed(1)
noise = np.random.normal(size=(len(X), 200))
tr_idx, te_idx = train_test_split(np.arange(len(X)), test_size=0.25, random_state=1)

# Leaky selection on all data:
corrs_all = np.array([np.corrcoef(noise[:, j], y)[0, 1] for j in range(200)])
top_leaky = np.argsort(-np.abs(corrs_all))[:5]
lr_leaky = LogisticRegression().fit(noise[tr_idx][:, top_leaky], y.iloc[tr_idx])
leaky_auc = roc_auc_score(y.iloc[te_idx], lr_leaky.predict_proba(noise[te_idx][:, top_leaky])[:, 1])

# Honest selection on training data only:
corrs_tr = np.array([np.corrcoef(noise[tr_idx, j], y.iloc[tr_idx])[0, 1] for j in range(200)])
top_honest = np.argsort(-np.abs(corrs_tr))[:5]
lr_honest = LogisticRegression().fit(noise[tr_idx][:, top_honest], y.iloc[tr_idx])
honest_auc = roc_auc_score(y.iloc[te_idx], lr_honest.predict_proba(noise[te_idx][:, top_honest])[:, 1])

print(f"Leaky Test AUC: {leaky_auc:.3f} (false confidence!)")
print(f"Honest Test AUC: {honest_auc:.3f} (correctly recognizes pure noise)")


# Exercise 8: Cross-validation by hand
kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=2026)
fold_scores = []

for train_idx, val_idx in kf.split(X_train, y_train):
    m = logistic_pipe.fit(X_train.iloc[train_idx], y_train.iloc[train_idx])
    val_probs = m.predict_proba(X_train.iloc[val_idx])[:, 1]
    fold_scores.append(roc_auc_score(y_train.iloc[val_idx], val_probs))

print("Fold AUCs:", np.round(fold_scores, 3))
print(f"Mean manual CV AUC: {np.mean(fold_scores):.3f}")


# Exercise 9: Noisier data, simpler model
def make_noisy(n, sd):
    np.random.seed(3)
    x = np.random.uniform(0, 3, n)
    y = true_curve(x) + np.random.normal(0, sd, n)
    return pd.DataFrame({"x": x, "y": y})

train_noisy = make_noisy(15, sd=0.6)
test_noisy = make_noisy(300, sd=0.6)
test_noisy = test_noisy[
    (test_noisy["x"] >= train_noisy["x"].min()) &
    (test_noisy["x"] <= train_noisy["x"].max())
]

noisy_errors = []
for d in range(1, 13):
    m = make_pipeline(PolynomialFeatures(d), LinearRegression()).fit(train_noisy[["x"]], train_noisy["y"])
    noisy_errors.append(root_mean_squared_error(test_noisy["y"], m.predict(test_noisy[["x"]])))

print("Best degree under high noise:", np.argmin(noisy_errors) + 1)
# High noise masks subtle non-linearities, penalizing flexible models earlier.


# Exercise 10: Who survived the Titanic?
y_titanic = (titanic["Survived"] == "Yes").astype(int)
X_titanic = titanic[["Class", "Sex", "Age"]]

X_tr_t, X_te_t, y_tr_t, y_te_t = train_test_split(
    X_titanic, y_titanic, test_size=0.25, stratify=y_titanic, random_state=4
)

titanic_pipe = Pipeline([
    ("ohe", OneHotEncoder(drop="first", sparse_output=False, handle_unknown="ignore")),
    ("classifier", LogisticRegression())
])
titanic_pipe.fit(X_tr_t, y_tr_t)

prob_titanic = titanic_pipe.predict_proba(X_te_t)[:, 1]
pred_titanic = titanic_pipe.predict(X_te_t)

print(f"Titanic Test AUC:      {roc_auc_score(y_te_t, prob_titanic):.3f}")
print(f"Titanic Test Accuracy: {accuracy_score(y_te_t, pred_titanic):.3f}")
print(f"Majority Class Base:   {(y_te_t == 0).mean():.3f}")


# ==============================================================================
# C. CHECK YOUR UNDERSTANDING - MODEL ANSWERS
# ==============================================================================

# 1. An explanatory model tests why an outcome happens by estimating sensible,
#    unconfounded causal coefficients. A predictive model is judged solely by how
#    accurately its predictions generalize to unseen cases.
# 2. The test set is a measure of generalization. If used repeatedly to adjust
#    hyperparameters or feature subsets, it becomes an informal training set,
#    producing data leakage and overoptimistic performance estimates.
# 3. Cross-validation estimates the expected out-of-sample performance of the
#    modeling pipeline on new data, using solely the training partition.
# 4. Overfitting occurs when a model fits sample-specific noise rather than the
#    underlying population signal, performing well on training data but poorly on new data.
# 5. Data leakage is when information from outside the training partition (such as test
#    features, future outcomes, or target distributions) inadvertently contaminates
#    model estimation or preprocessing.
