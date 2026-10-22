# FROM DATA TO THESIS: Using Python for Non-Technical
# Playground, Chapter 4: Solutions
#
# One possible solution for each exercise in parts A and B, and model answers
# for part C. Part D has no solutions: the tasks are open, and there are many
# good ways to answer them.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", font_scale=1.1)

students = pd.read_csv("students.csv")
semesters = pd.read_csv("semesters.csv")

first_sem = (
    semesters[semesters["semester"] == 1]
    .merge(students, on="student_id")
)

# ==============================================================================
# A. PRACTISE THE CHAPTER
# ==============================================================================

# Exercise 1: a binwidth of 5 shows the shape best: a peak in the mid-twenties
# and a long tail to the right. 1 is too jagged, 10 hides the tail.
fig, ax = plt.subplots(figsize=(7, 4))
sns.histplot(
    data=first_sem,
    x="study_hours",
    binwidth=5,
    color="steelblue",
    edgecolor="white",
    ax=ax
)
ax.set_title("Distribution of Weekly Study Hours")
ax.set_xlabel("Weekly Study Hours")
ax.set_ylabel("Student Count")
plt.show()


# Exercise 2: 307 no job, 196 part-time, 97 full-time. The colour is set as a
# fixed string (e.g., 'steelblue'), so no unnecessary legend is generated.
emp_order = ["None", "Part-time job", "Full-time job"]
students["employment"] = pd.Categorical(students["employment"], categories=emp_order, ordered=True)

fig, ax = plt.subplots(figsize=(6, 4))
sns.countplot(
    data=students,
    x="employment",
    color="steelblue",
    ax=ax
)
ax.set_xlabel("Paid Employment Status")
ax.set_ylabel("Number of Students")
plt.show()


# Exercise 3: medians between 3.06 and 3.14; the boxes overlap almost completely
fig, ax = plt.subplots(figsize=(8, 4))
sns.boxplot(
    data=first_sem,
    x="faculty",
    y="gpa",
    color="skyblue",
    ax=ax
)
ax.set_xlabel("Faculty")
ax.set_ylabel("Grade Point Average (GPA, 0 to 4)")
plt.show()


# Exercise 4: more caffeine, less sleep (about half an hour less per extra 100 mg)
fig, ax = plt.subplots(figsize=(7, 4))
sns.regplot(
    data=first_sem,
    x="caffeine_mg",
    y="sleep_hours",
    scatter_kws={"alpha": 0.35, "color": "darkblue"},
    line_kws={"color": "darkred"},
    ax=ax
)
ax.set_xlabel("Daily Caffeine Consumption (mg)")
ax.set_ylabel("Sleep Duration (Hours per Night)")
plt.show()


# Exercise 5: Saving a figure
fig, ax = plt.subplots(figsize=(6.3, 3.9))
sns.histplot(data=first_sem, x="sleep_hours", binwidth=0.5, color="steelblue", edgecolor="white", ax=ax)
ax.set_xlabel("Hours of Sleep per Night")
ax.set_ylabel("Count")
fig.savefig("sleep.png", dpi=300, bbox_inches="tight")
plt.close(fig)


# Exercise 6: A bar chart of wellbeing by faculty whose axis starts at zero.
faculty_means = (
    first_sem.groupby("faculty", as_index=False)["wellbeing"]
    .mean()
    .sort_values("wellbeing")
)

fig, ax = plt.subplots(figsize=(7, 4))
sns.barplot(
    data=faculty_means,
    x="faculty",
    y="wellbeing",
    color="grey",
    ax=ax
)
ax.set_ylim(0, 100)
ax.set_xlabel("Faculty")
ax.set_ylabel("Average Wellbeing in Semester 1 (0 to 100)")
plt.show()


# ==============================================================================
# B. GO FURTHER
# ==============================================================================

# Exercise 7: Dot plot for honest differences in position
fig, ax = plt.subplots(figsize=(7, 3.5))
ax.scatter(faculty_means["wellbeing"], faculty_means["faculty"], color="navy", s=60)
ax.set_xlim(55, 65)
ax.set_xlabel("Average Wellbeing")
ax.set_ylabel("Faculty")
ax.set_title("Dot Plot: Zoomed scale is honest because points denote position, not length")
plt.show()


# Exercise 8: Zoomed vs unzoomed line chart
wellbeing_by_sem = (
    semesters.merge(students[["student_id", "workshop"]], on="student_id")
    .groupby(["semester", "workshop"], as_index=False)["wellbeing"]
    .mean()
)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Left: zoomed in
sns.lineplot(data=wellbeing_by_sem, x="semester", y="wellbeing", hue="workshop", marker="o", ax=axes[0])
axes[0].set_title("Zoomed View (Exaggerated visual slope)")

# Right: full 0-100 scale
sns.lineplot(data=wellbeing_by_sem, x="semester", y="wellbeing", hue="workshop", marker="o", ax=axes[1])
axes[1].set_ylim(0, 100)
axes[1].set_title("Full Theoretical Scale (0 to 100)")
plt.tight_layout()
plt.show()


# Exercise 9: Anscombe's quartet
anscombe = sns.load_dataset("anscombe")
g = sns.lmplot(
    data=anscombe,
    x="x",
    y="y",
    col="dataset",
    ci=None,
    scatter_kws={"s": 50, "alpha": 0.8},
    line_kws={"color": "crimson"}
)
plt.show()


# Exercise 10: Exercise days and wellbeing with jitter
fig, ax = plt.subplots(figsize=(7, 4))
sns.regplot(
    data=first_sem,
    x="exercise_days",
    y="wellbeing",
    x_jitter=0.2,
    scatter_kws={"alpha": 0.3, "color": "teal"},
    line_kws={"color": "darkred"},
    ax=ax
)
ax.set_xlabel("Days of Exercise per Week")
ax.set_ylabel("Wellbeing Score (0 to 100)")
plt.show()


# ==============================================================================
# C. CHECK YOUR UNDERSTANDING: model answers
# ==============================================================================

# 1. Why do researchers prefer a bar chart or dot plot to a pie chart?
#    People judge positions and lengths on a common scale far more accurately
#    than angles, arcs, and 2D areas (Cleveland & McGill, 1984).
#
# 2. When is a y axis that does not start at zero acceptable?
#    For positional encodings (lines, scatter points, dot plots) where the reader
#    is informed and the full range is known. Never for bar charts, where visual
#    ink/bar height directly encodes physical magnitude from the baseline.
#
# 3. What is the difference between mapping a color to data and setting a fixed color?
#    Mapping (e.g. hue='faculty') assigns distinct colors according to variable
#    values and automatically creates a legend. Setting a fixed color (e.g.
#    color='steelblue') applies a uniform aesthetic without cluttering the plot
#    with redundant legends.
#
# 4. Which kind of palette suits categories, and which suits quantities?
#    Categories: Qualitative/discrete palettes (e.g. 'Set2', 'tab10') with equal
#    perceived luminance.
#    Continuous quantities: Sequential palettes (e.g. 'Blues', 'viridis') or
#    diverging palettes around a neutral midpoint (e.g. 'vlag', 'coolwarm').
#
# 5. What is an exploratory graph for, and how does it differ from an explanatory graph?
#    Exploratory graphs are fast, private, and plentiful; they allow the analyst
#    to spot outliers, distributions, and coding errors.
#    Explanatory graphs are polished, singularly focused public artifacts crafted
#    for the reader, with clear labels, honest scales, and informative captions.


# ==============================================================================
# D. DO IT YOURSELF
# No solutions: these tasks are open. Compare your approach with the methods of
# Chapter 4, and discuss your choices with a fellow student or your supervisor.
# ==============================================================================
