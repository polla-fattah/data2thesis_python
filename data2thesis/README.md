# data2thesis: Python Companion Package

Datasets and utilities for the book and course **"FROM DATA TO THESIS: Using Python for Non-Technical"** by Dr. Polla Fattah.

The package contains the **Graduate Wellbeing Study**, the running case study used throughout the book. It follows Elaf, a Master's student in Educational Psychology, who studies 600 graduate students over four semesters to understand how lifestyle, stress, supervisor support, and a wellbeing workshop relate to grades, mental health, and dropout risk.

> **Note**: Elaf and her data are simulated for teaching purposes. The patterns were built in by the author to teach real-world data science, cleaning, exploratory data analysis, inferential statistics, machine learning, and AI coding. It describes no real individuals and should not be cited as empirical evidence.

---

## Installation

### From Local Clone / Repository:
```bash
pip install ./data2thesis
```

Or in editable development mode:
```bash
pip install -e ./data2thesis
```

### From GitHub:
```bash
pip install git+https://github.com/polla-fattah/data2thesis_python.git#subdirectory=data2thesis
```

---

## Quickstart

### 1. Direct Attribute Access
Datasets are lazily loaded into Pandas DataFrames on demand:

```python
import data2thesis as dt

# Inspect students baseline data
print(dt.students.head())
print(dt.students.shape)  # (600, 14)

# Longitudinal semester records
print(dt.semesters.describe())

# Survey questionnaire (22 Likert items)
print(dt.questionnaire.info())
```

### 2. Explicit Loader Functions
Each dataset has a dedicated loader with rich documentation of all columns and variables:

```python
import data2thesis as dt

students = dt.load_students()
questionnaire = dt.load_questionnaire()
semesters = dt.load_semesters()
supervisors = dt.load_supervisors()
open_responses = dt.load_open_responses()
open_responses_coded = dt.load_open_responses_coded()
counselling_visits = dt.load_counselling_visits()  # parses dates by default
```

### 3. Raw Example Files (Excel, SPSS, CSV)
For chapters teaching file import and data cleaning:

```python
import pandas as pd
import data2thesis as dt

# List all available files
print(dt.list_example_files())

# Read the messy Excel export (Chapter 3)
excel_path = dt.example_file("wellbeing_raw.xlsx")
df_raw = pd.read_excel(excel_path)

# Read the SPSS file with value labels
sav_path = dt.example_file("wellbeing.sav")
df_spss = pd.read_spss(sav_path)
```

---

## Available Datasets

| Dataset | Rows | Columns | Description |
|---|---|---|---|
| `students` | 600 | 14 | Baseline demographics, faculty, study mode, workshop invitation, and year-1 dropout thoughts |
| `questionnaire` | 600 | 23 | 22 baseline Likert items measuring Stress, Burnout, Supervisor Support, and Satisfaction |
| `semesters` | 2,326 | 9 | Longitudinal semester records: GPA, sleep, study hours, exercise, caffeine, and wellbeing score |
| `supervisors` | 120 | 4 | Supervisor IDs, faculty, academic rank, and count of supervised students |
| `open_responses` | 535 | 2 | Qualitative responses to "What has been your biggest challenge during your studies?" |
| `open_responses_coded` | 200 | 3 | Subset of 200 open answers with ground-truth thematic coding |
| `counselling_visits` | 260 | 2 | Weekly student counselling clinic visits over 5 academic years |

---

## License

Apache License 2.0. See [LICENSE](LICENSE) for details.
