# 02_analysis.py
# Fits the models for the results chapter and saves the results and figures
# to output/. Run after 01_clean_data.py.

import warnings
warnings.filterwarnings("ignore")
from pathlib import Path
import pickle
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

navy = "#1d588c"
copper = "#b4762e"

students = pd.read_csv(DATA_DIR / "students.csv")
questionnaire = pd.read_csv(DATA_DIR / "questionnaire.csv")
semesters = pd.read_csv(DATA_DIR / "semesters.csv")

# 1. Scale scores and the study analysis table -------------------------------
scores = questionnaire.copy()
scores["stress_4"] = 6 - scores["stress_4"]
scores["stress"] = scores.filter(like="stress_").mean(axis=1)
scores["burnout"] = scores.filter(like="burnout_").mean(axis=1)
scores["support"] = scores.filter(like="support_").mean(axis=1)
scores = scores[["student_id", "stress", "burnout", "support"]]

study = students.merge(scores, on="student_id").merge(semesters.query("semester == 1"), on="student_id")

# 2. RQ3: Workshop trajectory (Mixed-effects model) --------------------------
panel = semesters.merge(students, on="student_id").assign(time=lambda d: d["semester"] - 1)

workshop_model = smf.mixedlm(
    "wellbeing ~ C(semester) * workshop",
    panel,
    groups=panel["student_id"],
    re_formula="~time"
).fit(method=["lbfgs", "powell"])

pred_grid = pd.MultiIndex.from_product(
    [[1, 2, 3, 4], ["Invited", "Not invited"]],
    names=["semester", "workshop"]
).to_frame().reset_index(drop=True)
pred_grid["time"] = pred_grid["semester"] - 1
pred_grid["predicted_wellbeing"] = workshop_model.predict(pred_grid)

piv = pred_grid.pivot(index="semester", columns="workshop", values="predicted_wellbeing")
gaps = (piv["Invited"] - piv["Not invited"]).to_dict()

# 3. RQ5: GPA multiple regression -------------------------------------------
gpa_model = smf.ols("gpa ~ sleep_hours + study_hours + stress + support", data=study).fit()
gpa_table = pd.DataFrame({
    "estimate": gpa_model.params,
    "std_err": gpa_model.bse,
    "t_value": gpa_model.tvalues,
    "p_value": gpa_model.pvalues,
    "conf_low": gpa_model.conf_int()[0],
    "conf_high": gpa_model.conf_int()[1]
})
gpa_fit = {
    "r_squared": gpa_model.rsquared,
    "nobs": int(gpa_model.nobs)
}

# 4. RQ9: Considering dropout (logistic regression) -------------------------
study["dropout_bool"] = (study["considering_dropout"] == "Yes").astype(int)
dropout_model = smf.logit(
    "dropout_bool ~ stress + support + financial_worry + C(employment) + C(study_mode)",
    data=study
).fit(disp=False)

dropout_table = pd.DataFrame({
    "odds_ratio": np.exp(dropout_model.params),
    "conf_low": np.exp(dropout_model.conf_int()[0]),
    "conf_high": np.exp(dropout_model.conf_int()[1]),
    "p_value": dropout_model.pvalues
})

# 5. Figure 1 (Multi-panel) -------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4))

for w_label, color in [("Invited", navy), ("Not invited", copper)]:
    sub = pred_grid[pred_grid["workshop"] == w_label]
    ax1.plot(sub["semester"], sub["predicted_wellbeing"], marker="o", color=color, linewidth=2, label=w_label)

ax1.set_xlabel("Semester")
ax1.set_ylabel("Predicted wellbeing (0-100)")
ax1.set_xticks([1, 2, 3, 4])
ax1.legend(title="Workshop")
ax1.set_title("A", loc="left", fontweight="bold", fontsize=12)

sns.regplot(
    data=study, x="sleep_hours", y="gpa",
    ax=ax2,
    scatter_kws={"alpha": 0.3, "color": "black", "s": 20},
    line_kws={"color": navy, "linewidth": 2}
)
ax2.set_xlabel("Sleep (hours a night)")
ax2.set_ylabel("GPA (semester 1)")
ax2.set_title("B", loc="left", fontweight="bold", fontsize=12)

for ax in (ax1, ax2):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

plt.tight_layout()
fig.savefig(OUTPUT_DIR / "figure-1.png", dpi=300, bbox_inches="tight")
plt.close(fig)

# 6. Save results dictionary ------------------------------------------------
results = {
    "study": study,
    "gaps": gaps,
    "gpa_table": gpa_table,
    "gpa_fit": gpa_fit,
    "dropout_table": dropout_table
}

with open(OUTPUT_DIR / "results.pkl", "wb") as f:
    pickle.dump(results, f)

print(f"Results saved to {OUTPUT_DIR}/ (results.pkl, figure-1.png).")
