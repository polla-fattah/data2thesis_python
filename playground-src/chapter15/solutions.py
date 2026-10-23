# FROM DATA TO THESIS: Using Python for Non-Technical
# Playground, Chapter 15: Neural Networks
# Solutions

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

# Chapter's data, split, pipeline, and folds
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
def neuron_ex1(stress, support):
    return sigmoid(-4 + 1.2 * stress - 1.6 * support)

p_high_stress = neuron_ex1(stress=4, support=2)
p_low_stress  = neuron_ex1(stress=2, support=4)
print(f"Ex 1 - High stress, low support: {p_high_stress:.3f}")
print(f"Ex 1 - Low stress, high support:  {p_low_stress:.4f}")
# A negative weight means that higher values of the input decrease the total,
# reducing the output probability: more support lowers the chance of considering dropout.


# Exercise 2: One hidden neuron, weight decay 1.0, against logistic regression
one_neuron_pipe = Pipeline([
    ('prep', dropout_recipe),
    ('mlp', MLPClassifier(hidden_layer_sizes=(1,), alpha=1.0, max_iter=500, random_state=2026, solver='lbfgs'))
])

one_neuron_scores = cross_val_score(one_neuron_pipe, X_train, y_train, cv=dropout_folds, scoring='roc_auc')

log_pipe = Pipeline([
    ('prep', dropout_recipe),
    ('clf', LogisticRegression(random_state=2026, max_iter=1000))
])
log_scores = cross_val_score(log_pipe, X_train, y_train, cv=dropout_folds, scoring='roc_auc')

print(f"Ex 2 - One hidden unit CV AUC: {one_neuron_scores.mean():.3f}")
print(f"Ex 2 - Logistic regression CV AUC: {log_scores.mean():.3f}")
# They are very similar because a single hidden unit with a logistic activation produces
# essentially a single non-linear projection, behaving much like logistic regression.


# Exercise 3: When the seed matters
for penalty in [3.16, 0.01]:
    seed_aucs = []
    for seed in [1, 2, 3]:
        net = Pipeline([
            ('prep', dropout_recipe),
            ('mlp', MLPClassifier(hidden_layer_sizes=(10,), alpha=penalty, max_iter=500, random_state=seed, solver='lbfgs'))
        ])
        net.fit(X_train, y_train)
        auc_val = roc_auc_score(y_test, net.predict_proba(X_test)[:, 1])
        seed_aucs.append(round(auc_val, 3))
    print(f"Ex 3 - Penalty (alpha) = {penalty}: Test AUC across seeds 1, 2, 3: {seed_aucs}")
# With little weight decay (0.01), starting weights determine which local minimum the network
# settles in, causing test AUC to fluctuate. With strong weight decay (3.16), the objective is
# regularized and smooth, giving consistent performance across seeds.


# Exercise 4: Epochs (20 neurons, no weight decay)
for epochs in [10, 100, 1000]:
    net = Pipeline([
        ('prep', dropout_recipe),
        ('mlp', MLPClassifier(hidden_layer_sizes=(20,), alpha=0.0, max_iter=epochs, random_state=2026, solver='lbfgs'))
    ])
    net.fit(X_train, y_train)
    tr_auc = roc_auc_score(y_train, net.predict_proba(X_train)[:, 1])
    te_auc = roc_auc_score(y_test, net.predict_proba(X_test)[:, 1])
    print(f"Ex 4 - Epochs {epochs:4d}: Train AUC = {tr_auc:.3f}, Test AUC = {te_auc:.3f}")
# As epochs increase from 10 to 1000, training AUC reaches 1.000 (memorisation), while test AUC
# stays around 0.77-0.78 without improving.


# Exercise 5: Explaining the choice to the research group
# "We evaluated a tuned multilayer perceptron neural network against logistic regression using
# rigorous 10-fold cross-validation. The neural network achieved a cross-validated ROC AUC of 0.835
# and test AUC of 0.826, which did not improve upon logistic regression (test AUC 0.843). Because
# the wellbeing data has smooth, additive structure, the neural network's ~500 uninterpretable
# weights added complexity and risk of overfitting without any gain in predictive accuracy."


# Exercise 6: The learning rate (0.1, 1.0, 10, 100)
six = pd.DataFrame({
    'stress':  np.array([2.0, 2.5, 3.0, 3.5, 4.0, 4.5]) - 3.25,
    'dropout': np.array([0,   0,   1,   0,   1,   1])
})

def log_loss(b0, b1):
    p = sigmoid(b0 + b1 * six['stress'])
    return -np.mean(six['dropout'] * np.log(p) + (1 - six['dropout']) * np.log(1 - p))

for lr in [0.1, 1.0, 10.0, 100.0]:
    b0, b1 = 0.0, 0.0
    for step in range(200):
        p = sigmoid(b0 + b1 * six['stress'])
        b0 -= lr * np.mean(p - six['dropout'])
        b1 -= lr * np.mean((p - six['dropout']) * six['stress'])
    print(f"Ex 6 - LR = {lr:5.1f}: b1 = {b1:7.4f}, Final loss = {log_loss(b0, b1):.4f}")
# At lr = 0.1, convergence is slow; at lr = 1.0, convergence is smooth;
# at lr = 100, updates overshoot and oscillate.


# ==============================================================================
# B. GO FURTHER (pure Python & scikit-learn)
# ==============================================================================

# Data preparation for pure matrix/array exercises
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
    grad = X_mat.T @ (p - y_vec) / len(y_vec)
    b -= lr * grad

lr_model = LogisticRegression(penalty=None, solver='lbfgs')
lr_model.fit(train_df[['stress', 'support']], train_df['dropout'])

print("Ex 7 - Gradient descent coefficients:", b.round(4))
print("Ex 7 - Logistic regression coefficients:", [lr_model.intercept_[0], lr_model.coef_[0, 0], lr_model.coef_[0, 1]])


# Exercise 8: A hidden layer by hand
students_3 = pd.DataFrame({'stress': [4.0, 2.0, 3.5], 'support': [2.0, 4.0, 1.5]})
h1 = sigmoid(-3.0 + 1.5 * students_3['stress'] - 0.5 * students_3['support'])
h2 = sigmoid( 2.0 - 0.2 * students_3['stress'] - 1.0 * students_3['support'])
output = sigmoid(-2.0 + 3.0 * h1 + 2.0 * h2)
res_ex8 = students_3.copy()
res_ex8['h1'] = h1
res_ex8['h2'] = h2
res_ex8['output'] = output
print("Ex 8 - Hidden layer forward pass:")
print(res_ex8.round(3))


# Exercise 9: Weight decay with a small sample (60 students)
np.random.seed(7)
small_idx = np.random.choice(len(train_df), size=60, replace=False)
small = train_df.iloc[small_idx]

for alpha_val in [0.0, 0.1, 1.0, 10.0]:
    aucs = []
    for seed in [1, 2, 3]:
        net = MLPClassifier(hidden_layer_sizes=(5,), alpha=alpha_val, max_iter=1000, random_state=seed, solver='lbfgs')
        net.fit(small[features], small['dropout'])
        aucs.append(round(roc_auc_score(test_df['dropout'], net.predict_proba(test_df[features])[:, 1]), 3))
    print(f"Ex 9 - Small sample alpha={alpha_val:4.1f}: Test AUC across seeds = {aucs}")

lr_small = LogisticRegression(max_iter=1000)
lr_small.fit(small[features], small['dropout'])
print("Ex 9 - Small sample Logistic test AUC:", round(roc_auc_score(test_df['dropout'], lr_small.predict_proba(test_df[features])[:, 1]), 3))


# Exercise 10: A neural network for timber volume (trees.csv)
trees = pd.read_csv("trees.csv")
X_tr = trees[['Girth', 'Height']]
y_tr = trees['Volume']

loo = LeaveOneOut()

# Linear model LOO RMSE
lm_pipe = Pipeline([('scaler', StandardScaler()), ('lm', LinearRegression())])
lm_err = []
for tr, te in loo.split(X_tr):
    lm_pipe.fit(X_tr.iloc[tr], y_tr.iloc[tr])
    pred = lm_pipe.predict(X_tr.iloc[te])
    lm_err.append(y_tr.iloc[te].values[0] - pred[0])
print("Ex 10 - Trees Linear Model LOO RMSE:", round(np.sqrt(np.mean(np.array(lm_err)**2)), 3))

# MLP LOO RMSE
mlp_pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('mlp', MLPRegressor(hidden_layer_sizes=(3,), alpha=0.1, max_iter=2000, random_state=1, solver='lbfgs'))
])
mlp_err = []
for tr, te in loo.split(X_tr):
    mlp_pipe.fit(X_tr.iloc[tr], y_tr.iloc[tr])
    pred = mlp_pipe.predict(X_tr.iloc[te])
    mlp_err.append(y_tr.iloc[te].values[0] - pred[0])
print("Ex 10 - Trees Neural Network LOO RMSE:", round(np.sqrt(np.mean(np.array(mlp_err)**2)), 3))


# ==============================================================================
# C. CHECK YOUR UNDERSTANDING (Model answers)
# ==============================================================================

# 1. Why is a single neuron with a sigmoid activation the same as a logistic regression?
# A single neuron multiplies each input x_i by a weight w_i, adds a bias b, and passes the
# sum z = b + sum(w_i * x_i) into a sigmoid function 1 / (1 + exp(-z)). This is mathematically
# identical to logistic regression, where the bias is the intercept, weights are coefficients,
# and the sigmoid maps the linear predictor (log odds) to a predicted probability.

# 2. What does the learning rate control?
# The learning rate controls the step size taken along the negative gradient during each epoch
# of gradient descent. If it is too small, convergence requires an excessive number of steps;
# if it is too large, the updates overshoot the minimum, causing oscillation or divergence.

# 3. What does weight decay prevent?
# Weight decay adds an L2 penalty on large weights (proportional to sum(w_i^2)). This prevents
# neurons from fitting noise and memorising individual training cases, producing simpler,
# smoother decision boundaries that generalize better to unseen data.

# 4. Why must the seed be set, and reported, when training a neural network?
# Neural networks initialize their weights randomly. Because the loss surface has multiple local
# minima, different initializations can lead to different final models. Setting and reporting
# random_state ensures reproducibility across runs and research reporting.

# 5. When are neural networks worth using?
# Neural networks excel on unstructured data (images, audio, natural language), on very large
# datasets (tens of thousands to millions of observations), and when the true relationship
# involves strong non-linearities and complex interactions that linear models cannot represent.
# For moderate-sized tabular research data, regression, random forests, or gradient boosting
# are usually faster, more interpretable, and perform just as well.
