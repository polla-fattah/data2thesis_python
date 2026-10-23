# FROM DATA TO THESIS: Using Python for Non-Technical
# Playground, Chapter 15: Neural Networks
#
# Four parts, as on the playground page:
#   A. Practise the chapter       the book's exercises, with scikit-learn
#   B. Go further                 new exercises beyond the book
#   C. Check your understanding   short questions; answers in solutions.py
#   D. Do it yourself             open tasks with no starter code and no answers
#
# Run a line with Shift+Enter in your IDE or execute: python exercises.py
# Try each exercise yourself before you look at solutions.py.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score, LeaveOneOut
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import roc_auc_score, root_mean_squared_error
import warnings
warnings.filterwarnings('ignore')

# Load data
students = pd.read_csv("students.csv")
semesters = pd.read_csv("semesters.csv")
questionnaire = pd.read_csv("questionnaire.csv")

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# The chapter's data, split, pipeline, and folds
questionnaire['stress_4'] = 6 - questionnaire['stress_4']
scores = pd.DataFrame({
    'student_id': questionnaire['student_id'],
    'stress': questionnaire[['stress_1', 'stress_2', 'stress_3', 'stress_4', 'stress_5', 'stress_6']].mean(axis=1),
    'burnout': questionnaire[[f'burnout_{i}' for i in range(1, 7)]].mean(axis=1),
    'support': questionnaire[[f'support_{i}' for i in range(1, 7)]].mean(axis=1),
    'satisfaction': questionnaire[[f'satisfaction_{i}' for i in range(1, 5)]].mean(axis=1),
})

sem1 = semesters[semesters['semester'] == 1].drop(columns=['semester'])
dropout_data = (
    students.merge(scores, on='student_id')
    .merge(sem1, on='student_id')
    .drop(columns=['student_id', 'supervisor_id', 'workshop', 'workshop_sessions'])
)
dropout_data['considering_dropout'] = (dropout_data['considering_dropout'] == 'Yes').astype(int)

X = dropout_data.drop(columns=['considering_dropout'])
y = dropout_data['considering_dropout']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=2026
)

num_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
cat_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()

dropout_recipe = ColumnTransformer([
    ('num', Pipeline([('imp', SimpleImputer(strategy='median')), ('scaler', StandardScaler())]), num_cols),
    ('cat', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'), cat_cols)
])

dropout_folds = StratifiedKFold(n_splits=10, shuffle=True, random_state=2026)


# ==============================================================================
# A. PRACTISE THE CHAPTER
# ==============================================================================

# Exercise 1: A neuron with new weights (support twice as important: weight = -1.6)
def neuron(stress, support):
    return sigmoid(-4 + 1.2 * stress + ______ * support)

# print(round(neuron(4, 2), 3))
# print(round(neuron(2, 4), 4))


# Exercise 2: One hidden neuron, weight decay 1.0, against logistic regression
one_neuron_pipe = Pipeline([
    ('prep', dropout_recipe),
    ('mlp', MLPClassifier(hidden_layer_sizes=(______), alpha=1.0, max_iter=500, random_state=2026, solver='lbfgs'))
])
# one_scores = cross_val_score(one_neuron_pipe, X_train, y_train, cv=dropout_folds, scoring='roc_auc')

log_pipe = Pipeline([
    ('prep', dropout_recipe),
    ('clf', LogisticRegression(random_state=2026, max_iter=1000))
])
# log_scores = cross_val_score(log_pipe, X_train, y_train, cv=dropout_folds, scoring='roc_auc')


# Exercise 3: When the seed matters
# The chapter's tuned network (10 hidden units, alpha 3.16), three seeds, then
# the same with an alpha of 0.01.
for penalty in [3.16, 0.01]:
    test_aucs = []
    for seed in [1, 2, 3]:
        net = Pipeline([
            ('prep', dropout_recipe),
            ('mlp', MLPClassifier(hidden_layer_sizes=(10,), alpha=penalty, max_iter=500, random_state=______, solver='lbfgs'))
        ])
        net.fit(X_train, y_train)
        auc_val = roc_auc_score(y_test, net.predict_proba(X_test)[:, 1])
        test_aucs.append(round(auc_val, 3))
    print(f"Penalty {penalty}: test AUC across seeds:", test_aucs)


# Exercise 4: Epochs (20 neurons, no weight decay)
for epochs in [10, 100, 1000]:
    net = Pipeline([
        ('prep', dropout_recipe),
        ('mlp', MLPClassifier(hidden_layer_sizes=(20,), alpha=0.0, max_iter=______, random_state=2026, solver='lbfgs'))
    ])
    net.fit(X_train, y_train)
    tr_auc = roc_auc_score(y_train, net.predict_proba(X_train)[:, 1])
    te_auc = roc_auc_score(y_test, net.predict_proba(X_test)[:, 1])
    print(f"Epochs {epochs:4d} -> Train AUC: {tr_auc:.3f}, Test AUC: {te_auc:.3f}")


# Exercise 5: Explaining the choice to the research group
# Write two or three sentences explaining why the thesis retains logistic regression.


# Exercise 6: The learning rate (0.1, 1.0, 10, 100)
six = pd.DataFrame({
    'stress':  np.array([2.0, 2.5, 3.0, 3.5, 4.0, 4.5]) - 3.25,
    'dropout': np.array([0,   0,   1,   0,   1,   1])
})

def log_loss(b0, b1):
    p = sigmoid(b0 + b1 * six['stress'])
    return -np.mean(six['dropout'] * np.log(p) + (1 - six['dropout']) * np.log(1 - p))

for lr in [0.1, ______, 10.0, 100.0]:
    b0, b1 = 0.0, 0.0
    for step in range(200):
        p = sigmoid(b0 + b1 * six['stress'])
        b0 -= lr * np.mean(p - six['dropout'])
        b1 -= lr * np.mean((p - six['dropout']) * six['stress'])
    print(f"LR: {lr} -> b1: {b1:.4f}, final loss: {log_loss(b0, b1):.4f}")


# ==============================================================================
# B. GO FURTHER (pure Python & scikit-learn)
# ==============================================================================

nn_data = students.merge(scores, on='student_id').merge(sem1, on='student_id')
nn_data['dropout'] = (nn_data['considering_dropout'] == 'Yes').astype(int)
features = ['stress', 'burnout', 'support', 'financial_worry', 'sleep_hours',
            'study_hours', 'caffeine_mg', 'wellbeing', 'gpa']
nn_clean = nn_data[['dropout'] + features].dropna()

np.random.seed(10)
train_idx = np.random.choice(len(nn_clean), size=int(0.75 * len(nn_clean)), replace=False)
test_idx = np.setdiff1d(np.arange(len(nn_clean)), train_idx)

train_df = nn_clean.iloc[train_idx].copy()
test_df  = nn_clean.iloc[test_idx].copy()

scaler_b = StandardScaler()
train_df[features] = scaler_b.fit_transform(train_df[features])
test_df[features]  = scaler_b.transform(test_df[features])


# Exercise 7: Gradient descent with two predictors, against LogisticRegression
X_mat = np.column_stack([np.ones(len(train_df)), train_df['stress'], train_df['support']])
y_vec = train_df['dropout'].values
b = np.array([0.0, 0.0, 0.0])
lr = 1.0
for step in range(2000):
    p = sigmoid(X_mat @ b)
    grad = X_mat.T @ (p - ______) / len(y_vec)
    b -= lr * grad


# Exercise 8: A hidden layer by hand
students_3 = pd.DataFrame({'stress': [4.0, 2.0, 3.5], 'support': [2.0, 4.0, 1.5]})
h1 = sigmoid(-3.0 + 1.5 * students_3['stress'] - 0.5 * students_3['support'])
h2 = sigmoid( 2.0 - 0.2 * students_3['stress'] - 1.0 * students_3['support'])
output = ______( -2.0 + 3.0 * h1 + 2.0 * h2 )


# Exercise 9: Weight decay with a small sample (60 students)
np.random.seed(7)
small_idx = np.random.choice(len(train_df), size=60, replace=False)
small = train_df.iloc[small_idx]

for alpha_val in [0.0, 0.1, 1.0, 10.0]:
    aucs = []
    for seed in [1, 2, 3]:
        net = MLPClassifier(hidden_layer_sizes=(5,), alpha=______, max_iter=1000, random_state=seed, solver='lbfgs')
        net.fit(small[features], small['dropout'])
        aucs.append(round(roc_auc_score(test_df['dropout'], net.predict_proba(test_df[features])[:, 1]), 3))
    print(f"Alpha {alpha_val}: Test AUC across seeds: {aucs}")


# Exercise 10: A neural network for timber volume (trees.csv)
trees = pd.read_csv("trees.csv")
X_tr = trees[['Girth', 'Height']]
y_tr = trees['Volume']

loo = LeaveOneOut()

# Fit LinearRegression and MLPRegressor inside leave-one-out cross validation:
# mlp_pipe = Pipeline([
#     ('scaler', StandardScaler()),
#     ('mlp', MLPRegressor(hidden_layer_sizes=(3,), alpha=0.1, max_iter=2000, random_state=1, solver='lbfgs'))
# ])


# ==============================================================================
# C. CHECK YOUR UNDERSTANDING
# Answer in your own words, then compare with the answers in solutions.py.
# ==============================================================================

# 1. Why is a single neuron with a sigmoid activation the same as a logistic
#    regression?
# 2. What does the learning rate control?
# 3. What does weight decay prevent?
# 4. Why must the seed be set, and reported, when training a neural network?
# 5. When are neural networks worth using?


# ==============================================================================
# D. DO IT YOURSELF
# Open tasks: no starter code, no hints, and no answers. Write your own code
# under each task, as you would for a thesis.
# ==============================================================================

# Task 1: Tune a neural network for a numeric outcome (such as final_gpa or
# wellbeing) using GridSearchCV on MLPRegressor, compare its test RMSE fairly
# with Ridge or Linear Regression, and decide which to use.

# Task 2: Explain to a non-specialist, as comments above your own
# gradient-descent loop, what training a network means.

# Task 3: Is a neural network worth trying? Consider:
# (a) Diagnosing skin lesions from 20,000 labelled photographs.
# (b) Predicting which of 300 survey respondents change jobs from 12 questionnaire scores.
# (c) Forecasting next week's hospital admissions from ten years of daily records.
