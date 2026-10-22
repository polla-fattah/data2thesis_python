# FROM DATA TO THESIS: Using Python for Non-Technical
# Playground, Chapter 4: Data Visualization with Seaborn and Matplotlib
#
# Four parts, as on the playground page:
#   A. Practise the chapter       the book's exercises, with blanks (______) to fill
#   B. Go further                 new exercises beyond the book
#   C. Check your understanding   short questions; answers in solutions.py
#   D. Do it yourself             open tasks with no starter code and no answers
#
# Run a line or block with Shift+Enter in VS Code.
# Try each exercise yourself before you look at solutions.py.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set clean scientific styling
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

# Exercise 1: Choosing a binwidth
# Try binwidths of 1, 5, and 10 with sns.histplot. Which shows the distribution best?
fig, ax = plt.subplots(figsize=(7, 4))
sns.histplot(
    data=first_sem,
    x="study_hours",
    binwidth=______,
    color="steelblue",
    edgecolor="white",
    ax=ax
)
ax.set_title("Distribution of Study Hours per Week")
ax.set_xlabel("Weekly Study Hours")
ax.set_ylabel("Student Count")
plt.show()


# Exercise 2: Employment in order, in one colour
# Order the categorical levels from no job to full-time job; use one single colour.
emp_order = ["None", "Part-time job", "Full-time job"]
students["employment"] = pd.Categorical(students["employment"], categories=______, ordered=True)

fig, ax = plt.subplots(figsize=(6, 4))
sns.countplot(
    data=students,
    x="employment",
    color=______,
    ax=ax
)
ax.set_xlabel("Paid Employment Status")
ax.set_ylabel("Number of Students")
plt.show()


# Exercise 3: GPA by faculty, with clear axis labels
fig, ax = plt.subplots(figsize=(8, 4))
sns.______(
    data=first_sem,
    x="faculty",
    y="gpa",
    color="skyblue",
    ax=ax
)
ax.set_xlabel("______")
ax.set_ylabel("______")
plt.show()


# Exercise 4: Caffeine and sleep, with a trend line
fig, ax = plt.subplots(figsize=(7, 4))
sns.regplot(
    data=first_sem,
    x="caffeine_mg",
    y="sleep_hours",
    scatter_kws={"alpha": ______},
    line_kws={"color": "darkred"},
    ax=ax
)
ax.set_xlabel("Daily Caffeine Consumption (mg)")
ax.set_ylabel("Sleep Duration (Hours)")
plt.show()


# Exercise 5: Saving a publication-ready graph
# Create and save a figure to a high-resolution PNG file (300 DPI).
fig, ax = plt.subplots(figsize=(6.3, 3.9))  # ~16 cm x 10 cm
sns.histplot(data=first_sem, x="sleep_hours", binwidth=0.5, color="steelblue", edgecolor="white", ax=ax)
ax.set_xlabel("Hours of Sleep per Night")
ax.set_ylabel("Count")

fig.savefig("sleep.png", dpi=______, bbox_inches="tight")
plt.close(fig)


# Exercise 6: The misleading graph, redrawn
# Redraw the faculty wellbeing comparison with a true zero-baseline (0 to 100).
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
ax.set_ylim(______, 100)
ax.set_xlabel("Faculty")
ax.set_ylabel("Average Wellbeing in Semester 1 (0 to 100)")
plt.show()


# ==============================================================================
# B. GO FURTHER
# ==============================================================================

# Exercise 7: The same numbers three ways (Dot plot vs Bar plot)
# Compare a horizontal dot plot (Lollipop / scatter) with a bar plot.
fig, ax = plt.subplots(figsize=(7, 3.5))
ax.scatter(faculty_means["wellbeing"], faculty_means["faculty"], color="navy", s=60)
ax.set_xlim(55, 65)
ax.set_xlabel("Average Wellbeing")
ax.set_ylabel("Faculty")
ax.set_title("Dot Plot: Zoomed scale is honest because points denote position, not length")
plt.show()


# Exercise 8: A longitudinal line chart, zoomed vs full scale
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
axes[1].set_ylim(______, ______)
axes[1].set_title("Full Theoretical Scale (0 to 100)")
plt.tight_layout()
plt.show()


# Exercise 9: Anscombe's quartet yourself
anscombe = sns.load_dataset("anscombe")

# Check summary statistics per dataset
summary = anscombe.groupby("dataset").agg(
    mean_x=("x", "mean"),
    std_x=("x", "std"),
    mean_y=("y", "mean"),
    std_y=("y", "std")
)
print(summary)

# Faceted scatter plot with regression line across the 4 datasets
g = sns.lmplot(
    data=anscombe,
    x="x",
    y="y",
    col="______",
    ci=None,
    scatter_kws={"s": 50, "alpha": 0.8},
    line_kws={"color": "crimson"}
)
plt.show()


# Exercise 10: Exercise days and wellbeing (Jitter + Regression)
# Exercise days take integer values 0 to 7: add horizontal jitter to resolve overplotting.
fig, ax = plt.subplots(figsize=(7, 4))
sns.regplot(
    data=first_sem,
    x="exercise_days",
    y="wellbeing",
    x_jitter=______,
    scatter_kws={"alpha": 0.3, "color": "teal"},
    line_kws={"color": "darkred"},
    ax=ax
)
ax.set_xlabel("Days of Exercise per Week")
ax.set_ylabel("Wellbeing Score (0 to 100)")
plt.show()


# ==============================================================================
# C. CHECK YOUR UNDERSTANDING
# Answer in your own words, then compare with the answers in solutions.py.
# ==============================================================================

# 1. Why do researchers prefer a bar chart or dot plot to a pie chart?
# 2. When is a y axis that does not start at zero acceptable?
# 3. What is the difference between mapping a color to data and setting a fixed color?
# 4. Which kind of palette suits categories, and which suits continuous quantities?
# 5. What is an exploratory graph for, and how does it differ from an explanatory graph?


# ==============================================================================
# D. DO IT YOURSELF
# Open tasks: no starter code, no hints, and no answers. Write your own code
# under each task, as you would for a thesis.
# ==============================================================================

# Task 1: Choose a question about two variables of the study that the chapter
# did not graph. Make an explanatory version ready for a thesis, and write its caption.


# Task 2: The code below draws a deliberately poor graph. Improve it, and write
# down each change you made and why:
bad_data = first_sem.groupby("faculty", as_index=False)["sleep_hours"].mean()
fig, ax = plt.subplots()
sns.barplot(data=bad_data, x="faculty", y="sleep_hours", hue="faculty", ax=ax)
ax.set_ylim(6.3, 6.7)
plt.show()


# Task 3: Load seaborn's built-in 'mpg' dataset (sns.load_dataset('mpg')).
# Make three exploratory plots of engine displacement ('displacement') against
# highway efficiency ('mpg' or 'weight'), then polish the clearest one into an
# explanatory thesis figure.


# Task 4: Make a faceted grid comparing wellbeing across semesters faceted by
# faculty, using sns.FacetGrid or sns.relplot.


# Task 5: Save your polished figure as a PDF file (vector) and as a 300 DPI PNG,
# and inspect the crispness of text when zoomed in.
