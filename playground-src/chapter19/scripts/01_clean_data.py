# 01_clean_data.py
# Reads the raw survey export and writes clean tables to data/.
# Run from the project root. The raw file in data-raw/ is never changed;
# everything in data/ is recreated by this script.

import os
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = ROOT / "data-raw" / "wellbeing_raw.xlsx"
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

raw = pd.read_excel(DATA_RAW)

item_names = [f"stress_{i}" for i in range(1, 7)] + \
             [f"burnout_{i}" for i in range(1, 7)] + \
             [f"support_{i}" for i in range(1, 7)] + \
             [f"satisfaction_{i}" for i in range(1, 5)]

# 1. Remove test responses and duplicates ------------------------------------
responses = raw[~raw["Q1_Student ID"].str.upper().str.startswith("TEST")].copy()
responses = responses.drop(columns=["Response ID"]).drop_duplicates()

# 2. Usable column names -----------------------------------------------------
rename_map = {
    "Q1_Student ID": "student_id",
    "Q2_Age": "age",
    "Q3_Gender": "gender",
    "Q4_Faculty": "faculty",
    "Q5_Programme": "programme",
    "Q6_Study mode": "study_mode",
    "Q7_Paid work": "employment",
    "Q8_Children": "has_children",
    "Q9_Moved away from family": "lives_away",
    "Q10_How worried are you about money? (1-5)": "financial_worry",
    "Workshop group": "workshop",
    "Workshop sessions attended": "workshop_sessions",
    "Y1_Considered leaving?": "considering_dropout"
}
q11_cols = [f"Q11_{i}" for i in range(1, 23)]
rename_map.update(dict(zip(q11_cols, item_names)))
responses = responses.rename(columns=rename_map)

# 3. Consistent categories ---------------------------------------------------
def clean_gender(g):
    s = str(g).strip().lower()
    return "Female" if s.startswith("f") else "Male"

def clean_faculty(f):
    s = str(f).lower()
    if "educ" in s: return "Education"
    if "health" in s: return "Health Sciences"
    if "humanit" in s: return "Humanities"
    if "social" in s: return "Social Sciences"
    return "Natural Sciences"

responses["gender"] = responses["gender"].apply(clean_gender)
responses["faculty"] = responses["faculty"].apply(clean_faculty)
responses["programme"] = responses["programme"].apply(lambda p: "PhD" if "ph" in str(p).lower() else "Master's")
responses["study_mode"] = responses["study_mode"].apply(lambda m: "Part-time" if "part" in str(m).lower() else "Full-time")
responses["employment"] = responses["employment"].apply(lambda e: "None" if str(e).lower() in ["none", "no job"] else e)

for col in ["has_children", "lives_away", "considering_dropout"]:
    responses[col] = responses[col].apply(lambda x: "Yes" if str(x).lower().startswith("y") else "No")

# 4. Missing codes, numbers stored as text, impossible values ----------------
def parse_number(s):
    return pd.to_numeric(s.astype(str).str.replace(",", ".").str.extract(r"(\d+(?:\.\d+)?)")[0], errors="coerce")

responses["financial_worry"] = pd.to_numeric(responses["financial_worry"].replace([99, "99", -9, "-9"], np.nan), errors="coerce")
for col in item_names:
    responses[col] = pd.to_numeric(responses[col].replace([99, "99"], np.nan), errors="coerce")

responses["workshop_sessions"] = pd.to_numeric(responses["workshop_sessions"], errors="coerce")
responses["age"] = parse_number(responses["age"])
responses.loc[responses["age"] > 100, "age"] = np.nan

# 5. Three clean tables ------------------------------------------------------
student_cols = [
    "student_id", "age", "gender", "faculty", "programme", "study_mode",
    "employment", "has_children", "lives_away", "financial_worry",
    "workshop", "workshop_sessions", "considering_dropout"
]
students_clean = responses[student_cols].copy()
questionnaire_clean = responses[["student_id"] + item_names].copy()

long_records = []
for sem in [1, 2, 3, 4]:
    sub = pd.DataFrame({
        "student_id": responses["student_id"],
        "semester": sem,
        "gpa": parse_number(responses[f"GPA_S{sem}"]),
        "sleep_hours": parse_number(responses[f"Sleep_S{sem}"]),
        "study_hours": parse_number(responses[f"Study_S{sem}"]),
        "exercise_days": parse_number(responses[f"Exercise_S{sem}"]),
        "caffeine_mg": parse_number(responses[f"Caffeine_S{sem}"]),
        "supervisor_meetings": parse_number(responses[f"Meetings_S{sem}"]),
        "wellbeing": parse_number(responses[f"Wellbeing_S{sem}"])
    })
    long_records.append(sub)

semesters_clean = pd.concat(long_records, ignore_index=True)
semesters_clean.loc[semesters_clean["sleep_hours"] > 24, "sleep_hours"] = np.nan
semesters_clean.loc[semesters_clean["study_hours"] > 168, "study_hours"] = np.nan
semesters_clean.loc[semesters_clean["gpa"] > 4, "gpa"] = np.nan

metric_cols = ["gpa", "sleep_hours", "study_hours", "exercise_days", "caffeine_mg", "supervisor_meetings", "wellbeing"]
semesters_clean = semesters_clean.dropna(subset=metric_cols, how="all")
semesters_clean["supervisor_meetings"] = semesters_clean["supervisor_meetings"].astype(int)
semesters_clean["wellbeing"] = semesters_clean["wellbeing"].astype(int)

# 6. Quality assertions ------------------------------------------------------
assert len(students_clean) == students_clean["student_id"].nunique(), "student_id must be unique"
assert set(students_clean["gender"]).issubset({"Female", "Male"}), "invalid gender"
assert not students_clean["faculty"].isna().any(), "missing faculty"
assert (semesters_clean["sleep_hours"].dropna() <= 24).all(), "impossible sleep"
assert (semesters_clean["study_hours"].dropna() <= 168).all(), "impossible study"
assert (semesters_clean["gpa"].dropna() <= 4).all(), "impossible gpa"

students_clean.to_csv(DATA_DIR / "students.csv", index=False)
questionnaire_clean.to_csv(DATA_DIR / "questionnaire.csv", index=False)
semesters_clean.to_csv(DATA_DIR / "semesters.csv", index=False)

print(f"Done. Clean tables written to {DATA_DIR}/ (students: {len(students_clean)}, questionnaire: {len(questionnaire_clean)}, semesters: {len(semesters_clean)}).")
