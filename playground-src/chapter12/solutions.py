# FROM DATA TO THESIS: Using Python for Non-Technical
# Playground, Chapter 12: Solutions
#
# One possible solution for each exercise in parts A and B, and model answers
# for part C. Part D has no solutions: the tasks are open, and there are many
# good ways to answer them.

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import (
    train_test_split,
    StratifiedKFold,
    cross_validate,
    cross_val_predict,
    GridSearchCV,
)
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    roc_auc_score,
    confusion_matrix,
    recall_score,
    precision_score,
    f1_score,
    roc_curve,
)

students = pd.read_csv("students.csv")
students["employment"] = students["employment"].fillna("None")
semesters = pd.read_csv("semesters.csv")
questionnaire = pd.read_csv("questionnaire.csv")

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

dropout_data["considering_dropout"] = (dropout_data["considering_dropout"] == "Yes").astype(int)

X = dropout_data.drop(columns=["considering_dropout"])
y = dropout_data["considering_dropout"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=2026
)

num_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
cat_cols = X.select_dtypes(include=["object", "category"]).columns.tolist()

dropout_recipe = ColumnTransformer([
    ("num", Pipeline([("imp", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]), num_cols),
    ("cat", OneHotEncoder(drop="first", sparse_output=False, handle_unknown="ignore"), cat_cols)
])

tree_recipe = ColumnTransformer([
    ("num", SimpleImputer(strategy="median"), num_cols),
    ("cat", OneHotEncoder(drop="first", sparse_output=False, handle_unknown="ignore"), cat_cols)
])

dropout_folds = StratifiedKFold(n_splits=10, shuffle=True, random_state=2026)

logistic_pipe = Pipeline([
    ("prep", dropout_recipe),
    ("model", LogisticRegression(random_state=2026))
])

cv_predictions = cross_val_predict(
    logistic_pipe, X_train, y_train, cv=dropout_folds, method="predict_proba"
)[:, 1]


# ==============================================================================
# A. PRACTISE THE CHAPTER
# ==============================================================================

# Exercise 1: support first (below ~2.55), then burnout or stress: poorly supported,
# burnt-out students are the primary group to watch.
tree2_pipe = Pipeline([
    ("prep", tree_recipe),
    ("model", DecisionTreeClassifier(max_depth=2, min_samples_leaf=10, random_state=2026))
])
tree2_pipe.fit(X_train, y_train)

feature_names = [f.split("__")[-1] for f in tree2_pipe.named_steps["prep"].get_feature_names_out()]
fig, ax = plt.subplots(figsize=(8, 4))
plot_tree(tree2_pipe.named_steps["model"], feature_names=feature_names, class_names=["No", "Yes"], filled=True, ax=ax)
plt.show()


# Exercise 2: Tuning the forest's max_features over [2, 5, 10]
forest_pipe = Pipeline([
    ("prep", tree_recipe),
    ("model", RandomForestClassifier(n_estimators=500, random_state=2026))
])

forest_grid = GridSearchCV(
    forest_pipe,
    param_grid={"model__max_features": [2, 5, 10]},
    cv=dropout_folds,
    scoring="roc_auc"
)
forest_grid.fit(X_train, y_train)

forest_tuning = pd.DataFrame({
    "max_features": [2, 5, 10],
    "mean_auc": forest_grid.cv_results_["mean_test_score"],
    "std_err": forest_grid.cv_results_["std_test_score"] / np.sqrt(10)
})
print("Forest tuning:\n", forest_tuning.round(3))


# Exercise 3: Very many neighbours in k-NN
knn_pipe = Pipeline([
    ("prep", dropout_recipe),
    ("knn", KNeighborsClassifier())
])

knn_grid = GridSearchCV(
    knn_pipe,
    param_grid={"knn__n_neighbors": [41, 81, 161, 301]},
    cv=dropout_folds,
    scoring="roc_auc"
)
knn_grid.fit(X_train, y_train)

knn_tuning = pd.DataFrame({
    "neighbors": [41, 81, 161, 301],
    "mean_auc": knn_grid.cv_results_["mean_test_score"],
    "std_err": knn_grid.cv_results_["std_test_score"] / np.sqrt(10)
})
print("k-NN tuning:\n", knn_tuning.round(3))


# Exercise 4: precision 0.67, recall 0.80, F1 0.73
precision_tiny = 8 / 12
recall_tiny    = 8 / 10
f1 = 2 * precision_tiny * recall_tiny / (precision_tiny + recall_tiny)
print(f"Precision: {precision_tiny:.3f}, Recall: {recall_tiny:.3f}, F1: {f1:.3f}")


# Exercise 5: Contacting only 10% of students: 0.5 flags 8.4% (recall 28.4%, precision 50.0%);
# 0.4 flags 12.4%. Threshold 0.5 is the one that stays strictly within the 10% limit.
threshold_rows = []
for t in [0.5, 0.4, 0.3, 0.2, 0.15, 0.1]:
    flags = (cv_predictions >= t).astype(int)
    tn_c, fp_c, fn_c, tp_c = confusion_matrix(y_train, flags, labels=[0, 1]).ravel()
    threshold_rows.append({
        "threshold": t,
        "flagged": flags.mean(),
        "recall": tp_c / (tp_c + fn_c),
        "precision": tp_c / (tp_c + fp_c) if (tp_c + fp_c) > 0 else 0,
        "specificity": tn_c / (tn_c + fp_c)
    })

threshold_table = pd.DataFrame(threshold_rows)
print("Threshold table:\n", threshold_table.round(3))


# Exercise 6: class_weight='balanced'
balanced_pipe = Pipeline([
    ("prep", dropout_recipe),
    ("model", LogisticRegression(class_weight="balanced", random_state=2026))
])

bal_res = cross_validate(
    balanced_pipe, X_train, y_train, cv=dropout_folds,
    scoring=["roc_auc", "recall", "precision"]
)
print("Balanced weighting - AUC:", round(bal_res["test_roc_auc"].mean(), 3),
      "Recall:", round(bal_res["test_recall"].mean(), 3),
      "Precision:", round(bal_res["test_precision"].mean(), 3))


# Exercise 7: cheapest threshold around 0.28-0.30, close to the decision-theory rule of 0.25 (1 / (1 + 3))
cost_miss        = 3
cost_false_alarm = 1

cost_rows = []
for t in np.arange(0.02, 0.62, 0.02):
    misses = np.sum((cv_predictions < t) & (y_train == 1))
    false_alarms = np.sum((cv_predictions >= t) & (y_train == 0))
    total_cost = cost_miss * misses + cost_false_alarm * false_alarms
    cost_rows.append({
        "threshold": round(t, 2),
        "total_cost": total_cost,
        "misses": misses,
        "false_alarms": false_alarms
    })

cost_df = pd.DataFrame(cost_rows)
best_cost_row = cost_df.loc[cost_df["total_cost"].idxmin()]
print("Cheapest threshold:", best_cost_row["threshold"])
print("Decision theory rule:", cost_false_alarm / (cost_false_alarm + cost_miss))


# ==============================================================================
# B. GO FURTHER
# ==============================================================================

# Exercise 8: Hand-calculated confusion matrices
prob  = np.array([0.90, 0.80, 0.70, 0.60, 0.45, 0.40, 0.30, 0.20, 0.15, 0.10])
truth = np.array([1,    1,    0,    1,    0,    1,    0,    0,    1,    0])

for t in [0.5, 0.35, 0.12]:
    flag = prob >= t
    tp = np.sum(flag & (truth == 1))
    fp = np.sum(flag & (truth == 0))
    fn = np.sum((~flag) & (truth == 1))
    tn = np.sum((~flag) & (truth == 0))
    rec = tp / np.sum(truth == 1)
    prec = tp / np.sum(flag) if np.sum(flag) > 0 else 0
    print(f"t={t:.2f} -> TP:{tp}, FP:{fp}, FN:{fn}, TN:{tn}, Recall:{rec:.2f}, Precision:{prec:.2f}")


# Exercise 9: False alarm cost 2; miss 10
cost_miss = 10
cost_false_alarm = 2

fa_costs = []
for t in np.arange(0.02, 0.62, 0.02):
    m = np.sum((cv_predictions < t) & (y_train == 1))
    fa = np.sum((cv_predictions >= t) & (y_train == 0))
    fa_costs.append({"threshold": round(t, 2), "total_cost": cost_miss * m + cost_false_alarm * fa})

fa_df = pd.DataFrame(fa_costs)
print("Cheapest threshold with cost_fa=2:", fa_df.loc[fa_df["total_cost"].idxmin()]["threshold"])
print("Decision theory rule:", cost_false_alarm / (cost_false_alarm + cost_miss))


# Exercise 10: Faculty breakdown at threshold 0.2
X_train_fac = X_train.copy()
X_train_fac["truth"] = y_train
X_train_fac["prob"] = cv_predictions
X_train_fac["flag"] = (cv_predictions >= 0.2).astype(int)

fac_summary = (
    X_train_fac.groupby("faculty")
    .apply(lambda g: pd.Series({
        "at_risk": np.sum(g["truth"] == 1),
        "found": np.sum((g["flag"] == 1) & (g["truth"] == 1)),
        "recall": np.sum((g["flag"] == 1) & (g["truth"] == 1)) / np.sum(g["truth"] == 1),
        "precision": np.sum((g["flag"] == 1) & (g["truth"] == 1)) / np.sum(g["flag"] == 1) if np.sum(g["flag"] == 1) > 0 else 0
    }))
)
print("Faculty breakdown:\n", fac_summary.round(3))


# Exercise 11: Palmer Penguins classification
penguins = pd.read_csv("penguins.csv").dropna(subset=["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"])
p_X = penguins[["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]]
p_y = penguins["species"]

p_X_tr, p_X_te, p_y_tr, p_y_te = train_test_split(p_X, p_y, test_size=0.25, stratify=p_y, random_state=1)
p_rf = RandomForestClassifier(n_estimators=500, random_state=1)
p_rf.fit(p_X_tr, p_y_tr)
p_pred = p_rf.predict(p_X_te)
print("Penguin confusion matrix:\n", pd.crosstab(p_y_te, p_pred, rownames=["Actual"], colnames=["Predicted"]))


# ==============================================================================
# C. CHECK YOUR UNDERSTANDING: model answers
# ==============================================================================

# 1. Recall (sensitivity) is the share of truly positive cases that the model flags:
#    how many students at risk are found. Precision is the share of flagged cases
#    that are truly positive: how often a contact is justified.
# 2. It sets how many errors of each kind the decisions produce; what those
#    errors cost is a value judgement about consequences for real people.
# 3. It averages the predictions of hundreds of trees grown on bootstrap samples
#    with random subsets of predictors; their individual overfitting errors cancel out.
# 4. It uses Euclidean distance, which predictors in large units (like caffeine in mg)
#    would dominate completely over small-scale variables.
# 5. Class weighting/upsampling shifts the predicted probabilities upwards (like a lower
#    threshold); it rarely improves the AUC, and uncalibrated probabilities lose their
#    direct percentage meaning.


# ==============================================================================
# D. DO IT YOURSELF
# No solutions: these tasks are open. Compare your approach with the methods of
# Chapter 12, and discuss your choices with a fellow student or your supervisor.
# ==============================================================================
