# FROM DATA TO THESIS: Using Python for Non-Technical
# Playground, Chapter 13: Solutions
#
# One possible solution for each exercise in parts A and B, and model answers
# for part C. Part D has no solutions: the tasks are open, and there are many
# good ways to answer them.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, KFold, GridSearchCV
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import root_mean_squared_error, mean_absolute_error, r2_score

# Load data
students = pd.read_csv("students.csv")
students["employment"] = students["employment"].fillna("None")
semesters = pd.read_csv("semesters.csv")
questionnaire = pd.read_csv("questionnaire.csv")

# Year one pivot
s12 = semesters[semesters['semester'] <= 2]
year_one = s12.pivot(
    index='student_id',
    columns='semester',
    values=['gpa', 'sleep_hours', 'study_hours', 'exercise_days', 'caffeine_mg', 'supervisor_meetings', 'wellbeing']
)
year_one.columns = [f"{col[0]}_s{col[1]}" for col in year_one.columns]
year_one = year_one.reset_index()

final_gpa = (
    semesters[(semesters['semester'] == 4) & semesters['gpa'].notna()][['student_id', 'gpa']]
    .rename(columns={'gpa': 'final_gpa'})
)

gpa_data = (
    students
    .merge(questionnaire, on='student_id')
    .merge(year_one, on='student_id')
    .merge(final_gpa, on='student_id')
    .drop(columns=['student_id', 'supervisor_id', 'considering_dropout'])
)

X = gpa_data.drop(columns=['final_gpa'])
y = gpa_data['final_gpa']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=2026
)
gpa_folds = KFold(n_splits=10, shuffle=True, random_state=2026)

numeric_cols = X_train.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = X_train.select_dtypes(exclude=[np.number]).columns.tolist()

gpa_recipe = ColumnTransformer([
    ('num', Pipeline([
        ('impute', SimpleImputer(strategy='median')),
        ('scale', StandardScaler())
    ]), numeric_cols),
    ('cat', Pipeline([
        ('impute', SimpleImputer(strategy='most_frequent')),
        ('dummy', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'))
    ]), categorical_cols)
])


# ==============================================================================
# A. PRACTISE THE CHAPTER
# ==============================================================================

# Exercise 1: MAE 0.22, RMSE 0.25; with one miss of 1.0, MAE 0.34 but RMSE
# 0.48: squaring gives the big miss far more weight
tiny = pd.DataFrame({
    'actual': [3.2, 2.8, 3.6, 3.0, 2.5],
    'predicted': [3.0, 2.9, 3.3, 3.1, 2.9]
})
errors = tiny['actual'] - tiny['predicted']
mae_hand = np.mean(np.abs(errors))
rmse_hand = np.sqrt(np.mean(errors**2))
print(f"Hand: MAE={mae_hand:.3f}, RMSE={rmse_hand:.3f}")
print(f"Sklearn: MAE={mean_absolute_error(tiny['actual'], tiny['predicted']):.3f}, RMSE={root_mean_squared_error(tiny['actual'], tiny['predicted']):.3f}")

tiny.loc[4, 'predicted'] = 3.5
print(f"After outlier: MAE={mean_absolute_error(tiny['actual'], tiny['predicted']):.3f}, RMSE={root_mean_squared_error(tiny['actual'], tiny['predicted']):.3f}")


# Exercise 2: 60 students: ordinary ~0.66, lasso 0.22; 150 students: ordinary ~0.26, lasso 0.21.
# The gap shrinks as sample size grows.
lm_pipe = Pipeline([('prep', gpa_recipe), ('model', LinearRegression())])
lasso_pipe = Pipeline([('prep', gpa_recipe), ('model', Lasso(alpha=0.03, random_state=2026))])

for n in [60, 150]:
    small_idx = X_train.sample(n=n, random_state=3).index
    X_small, y_small = X_train.loc[small_idx], y_train.loc[small_idx]
    
    lm_pipe.fit(X_small, y_small)
    lasso_pipe.fit(X_small, y_small)
    
    lm_rmse = root_mean_squared_error(y_test, lm_pipe.predict(X_test))
    lasso_rmse = root_mean_squared_error(y_test, lasso_pipe.predict(X_test))
    print(f"n={n:3d} | Ordinary LM Test RMSE: {lm_rmse:.3f} | Lasso Test RMSE: {lasso_rmse:.3f}")


# Exercise 3: Ridge keeps all coefficients; lasso sets most to zero
alphas = np.logspace(-4, 0, 20)
ridge_cv = GridSearchCV(
    Pipeline([('prep', gpa_recipe), ('model', Ridge())]),
    param_grid={'model__alpha': alphas},
    cv=gpa_folds, scoring='neg_root_mean_squared_error'
).fit(X_train, y_train)

best_ridge = ridge_cv.best_estimator_
best_ridge_coefs = best_ridge.named_steps['model'].coef_
ridge_zero = np.sum(best_ridge_coefs == 0)

lasso_cv = GridSearchCV(
    Pipeline([('prep', gpa_recipe), ('model', Lasso(random_state=2026, max_iter=5000))]),
    param_grid={'model__alpha': alphas},
    cv=gpa_folds, scoring='neg_root_mean_squared_error'
).fit(X_train, y_train)

best_lasso = lasso_cv.best_estimator_
best_lasso_coefs = best_lasso.named_steps['model'].coef_
lasso_zero = np.sum(best_lasso_coefs == 0)

print(f"Ridge zero coefficients: {ridge_zero} / {len(best_ridge_coefs)}")
print(f"Lasso zero coefficients: {lasso_zero} / {len(best_lasso_coefs)}")


# Exercise 4: Scale scores instead of items
scale_scores = questionnaire.copy()
scale_scores['stress_4'] = 6 - scale_scores['stress_4']
scale_scores['stress'] = scale_scores[[f'stress_{i}' for i in range(1, 7)]].mean(axis=1)
scale_scores['burnout'] = scale_scores[[f'burnout_{i}' for i in range(1, 7)]].mean(axis=1)
scale_scores['support'] = scale_scores[[f'support_{i}' for i in range(1, 7)]].mean(axis=1)
scale_scores['satisfaction'] = scale_scores[[f'satisfaction_{i}' for i in range(1, 5)]].mean(axis=1)
scale_scores = scale_scores[['student_id', 'stress', 'burnout', 'support', 'satisfaction']]

scores_data = (
    students
    .merge(scale_scores, on='student_id')
    .merge(year_one, on='student_id')
    .merge(final_gpa, on='student_id')
    .drop(columns=['student_id', 'supervisor_id', 'considering_dropout'])
)

Xs = scores_data.drop(columns=['final_gpa'])
ys = scores_data['final_gpa']

Xs_train, Xs_test, ys_train, ys_test = train_test_split(
    Xs, ys, test_size=0.25, random_state=2026
)
s_num = Xs_train.select_dtypes(include=[np.number]).columns.tolist()
s_cat = Xs_train.select_dtypes(exclude=[np.number]).columns.tolist()
scores_recipe = ColumnTransformer([
    ('num', Pipeline([('impute', SimpleImputer(strategy='median')), ('scale', StandardScaler())]), s_num),
    ('cat', Pipeline([('impute', SimpleImputer(strategy='most_frequent')), ('dummy', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'))]), s_cat)
])

scores_lasso_cv = GridSearchCV(
    Pipeline([('prep', scores_recipe), ('model', Lasso(random_state=2026, max_iter=5000))]),
    param_grid={'model__alpha': alphas},
    cv=gpa_folds, scoring='neg_root_mean_squared_error'
).fit(Xs_train, ys_train)

print(f"Lasso CV RMSE with 4 scale scores: {-scores_lasso_cv.best_score_:.3f}")


# Exercise 5: More trees for Gradient Boosting (learning rate 0.03)
gb_trees_cv = GridSearchCV(
    Pipeline([('prep', gpa_recipe), ('model', GradientBoostingRegressor(learning_rate=0.03, max_depth=1, random_state=2026))]),
    param_grid={'model__n_estimators': [100, 500, 1000]},
    cv=gpa_folds, scoring='neg_root_mean_squared_error'
).fit(X_train, y_train)

for trees, score in zip(gb_trees_cv.cv_results_['param_model__n_estimators'], -gb_trees_cv.cv_results_['mean_test_score']):
    print(f"Trees: {trees} -> CV RMSE: {score:.3f}")


# Exercise 6 (model answer):
# "Predictions are typically about 0.2 grade points from the GPA a student achieves:
# a student predicted at 3.0 will usually end between about 2.8 and 3.2.
# The prediction starts an advising conversation; it is not a verdict."


# ==============================================================================
# B. GO FURTHER (pure Python & NumPy)
# ==============================================================================

gpa_simple = (
    students[['student_id', 'age', 'financial_worry']]
    .merge(questionnaire, on='student_id')
    .merge(year_one, on='student_id')
    .merge(final_gpa, on='student_id')
    .drop(columns=['student_id'])
)
gpa_simple = gpa_simple.fillna(gpa_simple.median())
np.random.seed(12)
train_mask = np.random.rand(len(gpa_simple)) < 0.75
train_df = gpa_simple[train_mask].reset_index(drop=True)
test_df = gpa_simple[~train_mask].reset_index(drop=True)


# Exercise 7: Ridge regression by hand
X_ridge = train_df[['gpa_s1', 'gpa_s2']].values
X_ridge = (X_ridge - X_ridge.mean(axis=0)) / X_ridge.std(axis=0, ddof=0)
y_ridge = (train_df['final_gpa'] - train_df['final_gpa'].mean()).values

r = np.corrcoef(train_df['gpa_s1'], train_df['gpa_s2'])[0, 1]
print(f"Correlation between gpa_s1 and gpa_s2: {r:.3f}")

for lam in [0, 10, 100, 1000, 10000]:
    I = np.eye(X_ridge.shape[1])
    b = np.linalg.solve(X_ridge.T @ X_ridge + lam * I, X_ridge.T @ y_ridge)
    print(f"lambda={lam:5d} -> b_s1={b[0]:.4f}, b_s2={b[1]:.4f}")


# Exercise 8: One sample of 60, or ten?
results = []
for s in range(1, 11):
    small = train_df.sample(n=60, random_state=s)
    lm_all = LinearRegression().fit(small.drop(columns=['final_gpa']), small['final_gpa'])
    lm_two = LinearRegression().fit(small[['gpa_s1', 'gpa_s2']], small['final_gpa'])
    
    rmse_all = root_mean_squared_error(test_df['final_gpa'], lm_all.predict(test_df.drop(columns=['final_gpa'])))
    rmse_two = root_mean_squared_error(test_df['final_gpa'], lm_two.predict(test_df[['gpa_s1', 'gpa_s2']]))
    results.append({'seed': s, 'all_predictors': rmse_all, 'two_gpas': rmse_two})

results_df = pd.DataFrame(results)
print(results_df.round(3))
print("SD across seeds:")
print(results_df[['all_predictors', 'two_gpas']].std().round(3))


# Exercise 9: Boosting by hand (100 rounds, one-split trees)
learn_rate = 0.3
pred_train = np.full(len(train_df), train_df['final_gpa'].mean())
pred_test = np.full(len(test_df), train_df['final_gpa'].mean())

train_rmse = []
test_rmse = []

X_b_train = train_df.drop(columns=['final_gpa'])
y_b_train = train_df['final_gpa'].values
X_b_test = test_df.drop(columns=['final_gpa'])
y_b_test = test_df['final_gpa'].values

for i in range(100):
    error = y_b_train - pred_train
    tree = DecisionTreeRegressor(max_depth=1, random_state=i)
    tree.fit(X_b_train, error)
    
    pred_train += learn_rate * tree.predict(X_b_train)
    pred_test += learn_rate * tree.predict(X_b_test)
    
    train_rmse.append(root_mean_squared_error(y_b_train, pred_train))
    test_rmse.append(root_mean_squared_error(y_b_test, pred_test))

print(f"Best round: {np.argmin(test_rmse) + 1}, Best test RMSE: {np.min(test_rmse):.3f}")


# Exercise 10: The shape of a tree (cherry trees, leave-one-out cross-validation)
cherry = pd.read_csv("trees.csv")
n = len(cherry)
loo_sq_err_lin = []
loo_sq_err_log = []

for i in range(n):
    train_c = cherry.drop(index=i)
    test_c = cherry.iloc[[i]]
    
    # linear
    m_lin = LinearRegression().fit(train_c[['Girth', 'Height']], train_c['Volume'])
    p_lin = m_lin.predict(test_c[['Girth', 'Height']])[0]
    loo_sq_err_lin.append((test_c['Volume'].values[0] - p_lin)**2)
    
    # log-log
    m_log = LinearRegression().fit(np.log(train_c[['Girth', 'Height']]), np.log(train_c['Volume']))
    p_log = np.exp(m_log.predict(np.log(test_c[['Girth', 'Height']]))[0])
    loo_sq_err_log.append((test_c['Volume'].values[0] - p_log)**2)

print(f"LOO RMSE Linear: {np.sqrt(np.mean(loo_sq_err_lin)):.3f}")
print(f"LOO RMSE Log-Log: {np.sqrt(np.mean(loo_sq_err_log)):.3f}")


# ==============================================================================
# C. CHECK YOUR UNDERSTANDING: model answers
# ==============================================================================

# 1. Each predictor adds a coefficient that can fit the sample; with many
#    coefficients and few cases, they fit noise, and correlated predictors make
#    the coefficients unstable.
# 2. Ridge shrinks every coefficient and keeps all predictors; the lasso also
#    sets some to exactly zero, selecting predictors.
# 3. It sets how much large coefficients cost (0 = ordinary regression; very
#    large = the mean for everyone). Chosen by cross-validation.
# 4. A forest averages many deep, independent trees (less variance); boosting
#    adds small trees in sequence, each fitted to the errors so far (less bias).
# 5. Part of every outcome is unpredictable luck; the model predicts only the
#    predictable part, so extremes are pulled towards the mean.


# ==============================================================================
# D. DO IT YOURSELF
# No solutions: these tasks are open. Compare your approach with the methods of
# Chapter 13, and discuss your choices with a fellow student or your supervisor.
# ==============================================================================
