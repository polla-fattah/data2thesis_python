# Dataset Specification: The Graduate Wellbeing Study

**Status:** approved by the author. **Version 1.1.0 generated** by `data-raw/generate_wellbeing.R` (1.1.0 rewrote the open-ended answers with a much larger phrase bank, `data-raw/answer_bank.R`; every other value is identical to 1.0.0); all 72 checks in `data-raw/check_wellbeing.R` pass (results in `data-raw/check_results.txt`). Numbers in section 5 are the values in the generated data.

This document specifies the simulated dataset that runs through the book as its case study. It is based on the 2025 lecture notes *Data Analysis for Research* (where the student was called Sara; `graduate_student_wellbeing.csv`) and extends them so the data supports every chapter.

The author's decisions are listed in section 9. Everything else is a proposal to accept, change, or reject.

---

## 1. Principles

1. **Simulated, and said so.** The book states clearly that the data is simulated for teaching, that no real students are described, and why simulation was used (every method can be shown, and readers can regenerate the data themselves).
2. **Realistic.** Values, distributions, and relationships should look like real survey and academic data: skewed variables, correlated measures, missing answers, messy entries.
3. **Designed effects.** Each chapter's research question has an answer built into the data, with realistic effect sizes (mostly small to moderate), so analyses find something and the numbers are worth interpreting.
4. **Honest null results.** Some hypotheses are *not* supported, so readers learn that "no effect" is a finding too.
5. **Teaching traps on purpose.** A few classic pitfalls are built in deliberately (confounding, attrition, imbalanced classes, a reverse-coded item), each one discussed in the chapter where it appears.
6. **Not about computers.** All content concerns students' lives, studies, and wellbeing.
7. **Reproducible.** Documented scripts generate every file from a fixed seed, and a check script confirms the designed effects are present.

---

## 2. The study

### 2.1 The story
**Elaf** is a Master's student in Educational Psychology. Her thesis asks how lifestyle, stress, and supervisor support relate to graduate students' wellbeing, academic performance, and thoughts of dropping out, and whether a short wellbeing workshop helps.

### 2.2 Design
A two-year **longitudinal study** at one university. The university and country are **not named**, so readers anywhere can picture their own.

| Stage | When | What is collected |
|---|---|---|
| Baseline survey | Start of year 1 | Background information and a 22-item questionnaire |
| Semester records | End of each of 4 semesters | GPA, sleep, study hours, exercise, caffeine, wellbeing, supervisor meetings |
| Workshop | Between semesters 1 and 2 | Half the students are **randomly invited** to a six-week wellbeing workshop |
| Year-1 survey | End of semester 2 | Whether the student has considered dropping out |
| Final survey | End of semester 4 | One open-ended question about their biggest challenge |

- **Participants:** 600 graduate students (Master's and PhD) from 5 faculties, supervised by 120 supervisors.
- **Why randomise the workshop:** random invitation lets the book discuss causal conclusions properly. **Decided.** (Voluntary attendance was considered; the book still teaches confounding through the caffeine example in section 5.3.)

### 2.3 Elaf's research questions
| # | Research question | Main chapters |
|---|---|---|
| RQ1 | What does graduate student life look like: sleep, study, stress, wellbeing? | 4, 6 |
| RQ2 | Do students sleep less than the recommended 7 hours? | 7 |
| RQ3 | Does the wellbeing workshop improve wellbeing? | 7, 10 |
| RQ4 | Do stress and wellbeing differ between faculties and study modes? | 7, 8 |
| RQ5 | What explains students' GPA? | 8, 13 |
| RQ6 | Do the questionnaire items measure stress, burnout, supervisor support, and satisfaction as intended? | 9 |
| RQ7 | Are there distinct groups (profiles) of students? | 9, 14 |
| RQ8 | How do wellbeing and GPA change over the two years, and how much do supervisors matter? | 10 |
| RQ9 | Which students are at risk of considering dropout, and can we predict them? | 8, 12 |
| RQ10 | Can we predict final GPA from year-1 information? | 13 |
| RQ11 | What challenges do students describe in their own words? | 18 |
| RQ12 | *(Internal analysis for the counselling service, not part of the thesis)* How does demand for the counselling service vary through the year, and how many visits should it expect next year? | 16 |

---

## 3. Files

| File | Rows | Contents | Used for |
|---|---|---|---|
| `students.csv` | 600 | One row per student: background, workshop group, year-1 dropout answer | Most chapters |
| `questionnaire.csv` | 600 | One row per student: the 22 baseline questionnaire items | Ch 9, scale scores elsewhere |
| `semesters.csv` | about 2,330 | One row per student per semester (long format); fewer than 2,400 because some students leave | Ch 3, 7, 8, 10, 13 |
| `supervisors.csv` | 120 | One row per supervisor | Ch 3 (joins), Ch 10 |
| `open_responses.csv` | about 540 | One row per student who answered the final survey | Ch 18 |
| `open_responses_coded.csv` | 200 | A subset hand-coded into themes, to check AI coding against | Ch 18 |
| `counselling_visits.csv` | 260 | Weekly visits to the university counselling service over 5 years, analysed for the service as an internal analysis | Ch 16 |
| `wellbeing_raw.xlsx` | 615 | The messy "survey export": one wide sheet as it came from the online survey tool | Ch 2, 3 |
| `wellbeing.sav` | 600 | SPSS version of `students` and `questionnaire`, with variable and value labels | Ch 2 |

- The clean CSV files are what most chapters use; the raw Excel file is cleaned into them in Chapter 3.
- **Distributed both ways:** as files in the `data/` folder on the book's website, and as the installable Python package `data2thesis` (source in `data2thesis/`, installation instructions in `data2thesis/README.md`). The book teaches both: loading files teaches file paths and importing; installing the package teaches how packages work.

---

## 4. Codebook

### 4.1 `students.csv`
| Variable | Type | Values | Description |
|---|---|---|---|
| `student_id` | ID | `S0001`-`S0600` | Student identifier |
| `supervisor_id` | ID | `SUP001`-`SUP120` | The student's supervisor |
| `age` | Numeric | 22-55 | Age in years at baseline (right-skewed, median about 28) |
| `gender` | Categorical | Female, Male | Gender (about 55% female) |
| `faculty` | Categorical | Education, Health Sciences, Humanities, Natural Sciences, Social Sciences | Faculty |
| `programme` | Categorical | Master's, PhD | Degree programme (about 70% Master's) |
| `study_mode` | Categorical | Full-time, Part-time | Study mode (about 30% part-time) |
| `employment` | Ordinal | None, Part-time job, Full-time job | Paid work alongside study |
| `has_children` | Binary | Yes, No | Has children (about 25%) |
| `lives_away` | Binary | Yes, No | Moved away from family to study |
| `financial_worry` | Ordinal | 1-5 | "How worried are you about money?" (1 = not at all, 5 = extremely) |
| `workshop` | Binary | Invited, Not invited | Randomly invited to the wellbeing workshop (50/50) |
| `workshop_sessions` | Numeric | 0-6 | Sessions attended (0 for the not-invited group; many invited students attend only some) |
| `considering_dropout` | Binary | Yes, No | At the end of year 1: "Have you seriously considered leaving your programme?" (about 15% Yes) |

### 4.2 `questionnaire.csv`: 22 items
All items use a 1-5 scale (1 = strongly disagree, 5 = strongly agree). The wording is written for this book (not copied from published, copyrighted scales).

| Scale | Items | Example items | Notes |
|---|---|---|---|
| Stress | `stress_1`-`stress_6` | "I feel unable to control important things in my studies." | `stress_4` is **reverse-worded**: "I feel confident handling problems in my studies." |
| Burnout | `burnout_1`-`burnout_6` | "I feel emotionally drained by my studies." | `burnout_3` ("Deadlines make me feel overwhelmed") **also relates to stress**, so it loads on both factors |
| Supervisor support | `support_1`-`support_6` | "My supervisor gives me useful feedback." | |
| Academic satisfaction | `satisfaction_1`-`satisfaction_4` | "I am satisfied with my progress in my programme." | |

Scale scores (the average of each scale's items, after reversing `stress_4`) are computed by readers in Chapter 3 and used in later chapters: `stress_score`, `burnout_score`, `support_score`, `satisfaction_score`.

### 4.3 `semesters.csv` (long format)
| Variable | Type | Values | Description |
|---|---|---|---|
| `student_id` | ID | | Student identifier |
| `semester` | Numeric | 1-4 | Semester number |
| `gpa` | Numeric | 0.00-4.00 | Semester GPA on a 0-4 scale (**decided**) |
| `sleep_hours` | Numeric | 3.5-10 | Average hours of sleep per night (roughly normal, mean about 6.4) |
| `study_hours` | Numeric | 2-70 | Hours of study per week |
| `exercise_days` | Count | 0-7 | Days per week with at least 30 minutes of exercise |
| `caffeine_mg` | Numeric | 0-900 | Average daily caffeine (strongly right-skewed; some zeros) |
| `supervisor_meetings` | Count | 0-15 | Meetings with the supervisor this semester |
| `wellbeing` | Numeric | 0-100 | Wellbeing index (higher is better) |

### 4.4 `supervisors.csv`
| Variable | Type | Values | Description |
|---|---|---|---|
| `supervisor_id` | ID | | Supervisor identifier |
| `faculty` | Categorical | 5 faculties | Supervisor's faculty |
| `rank` | Ordinal | Lecturer, Assistant Professor, Professor | Academic rank |
| `n_students` | Count | 1-12 | Number of students supervised in the study |

### 4.5 `open_responses.csv` and `open_responses_coded.csv`
| Variable | Description |
|---|---|
| `student_id` | Student identifier |
| `biggest_challenge` | Free-text answer (1-3 sentences) to "What has been your biggest challenge during your studies?" |
| `theme` | *(coded file only)* Hand-coded theme: Supervision, Workload, Finances, Family, Health, Isolation, Other |

Answers are written to reflect each student's data (a student with low supervisor support is more likely to mention supervision), so text themes connect to the numbers. They vary in length, tone, and spelling, like real answers: each is built from a large phrase bank (about 90 core statements with interchangeable details, follow-up sentences, mentions of a second theme, openers, and closers), and about 7% are very short ("Money.", "no time"). The hand-coded theme is the main theme of the answer.

### 4.6 `counselling_visits.csv`
| Variable | Description |
|---|---|
| `week_start` | Date of the Monday starting each week, over 5 academic years |
| `visits` | Number of student visits to the counselling service that week |

---

## 5. Designed effects

Effect sizes below are targets; the check script (section 8) confirms the generated data comes close to them.

### 5.1 Descriptive picture (RQ1; Ch 4-6)
- Sleep is roughly normal (mean about 6.4 h, SD about 1.0); caffeine is strongly right-skewed with some very high values (outliers); age is right-skewed.
- Stress and burnout scores correlate moderately (r ≈ 0.6); support correlates negatively with both (r ≈ −0.35).
- A handful of genuine extreme cases (e.g. 3.5 h sleep with 800 mg caffeine) for the outlier discussion.

### 5.2 Group comparisons (RQ2-RQ4; Ch 7-8)
| Test | Comparison | Built-in result |
|---|---|---|
| One-sample t-test | Mean sleep vs. 7 hours | Clearly below 7 (mean about 6.4) |
| Two-sample t-test | Wellbeing in semester 2: invited vs. not invited | Invited higher by about 5 points (Cohen's d ≈ 0.45) |
| Paired t-test | Wellbeing, semester 1 vs. 2, invited group | Increases by about 5 points |
| Mann-Whitney U | Caffeine (skewed) by gender | Small difference; used to show why a non-parametric test fits skewed data |
| Wilcoxon signed-rank | One satisfaction item, semester-level comparison **[or drop]** | Small change |
| Chi-square | Employment × considering dropout | Dropout thoughts more common with a full-time job (about 25% vs. 12%) |
| One-way ANOVA | Stress score by faculty | Small differences (η² ≈ 0.03); post-hoc tests show only Health Sciences differs from Humanities |
| Two-way ANOVA | Wellbeing by programme × study mode | Main effect of study mode (part-time lower); **no interaction** (an honest null) |
| Null result | GPA by gender | No meaningful difference |

### 5.3 Explaining GPA (RQ5; Ch 8, 13)
Semester GPA depends on:
- **Sleep** (positive): about +0.10 GPA per extra hour.
- **Study hours** (positive, with **diminishing returns**: little gain beyond about 35 hours/week; shown with a quadratic term in Chapter 8). In Chapter 13's prediction of final GPA, tree-based models do *not* beat regularised regression, because year-one GPA already carries this effect; Chapter 13 shows boosting winning on the concrete data instead. (Updated 2026-09-24 to match the generated data.)
- **Stress score** (negative) and **support score** (positive): small to moderate.
- **Caffeine: a confounding lesson.** Caffeine correlates negatively with GPA on its own, but only because high-caffeine students sleep less; once sleep is in the model, caffeine has no effect.
- **Interaction:** supervisor support matters more for PhD students than for Master's students (for Chapter 8's interaction section).
- Overall, a model with these predictors explains about 25% of GPA variance (R² ≈ 0.25): realistic, not perfect.
- For Chapter 13's regularisation, the prediction task includes all 22 items and background variables, several of which are irrelevant or strongly correlated with each other, so Lasso has something to remove.

### 5.4 Questionnaire structure (RQ6; Ch 9)
- Four underlying factors (stress, burnout, support, satisfaction), with stress and burnout correlated (about 0.6), so factor analysis has to separate related constructs.
- Item loadings mostly 0.6-0.8; `burnout_3` cross-loads on stress; `stress_4` is reverse-worded and loads negatively until reversed.
- Reliability (Cronbach's alpha) about 0.76-0.85 per scale. (An earlier version of the check script wrongly included the scale score among the items, which inflated alpha to 0.86-0.89; fixed.)

### 5.5 Student profiles (RQ7; Ch 9, 14)
Four profiles are built in, with overlap between them (as in real data):

| Profile | Share | Pattern |
|---|---|---|
| Balanced | about 35% | Good sleep, moderate study, low stress, good support |
| Overloaded | about 30% | High study hours, short sleep, high caffeine, high stress |
| Isolated | about 20% | Low supervisor support and meetings, low satisfaction, lives away |
| Disengaged | about 15% | Low study hours, low satisfaction, moderate stress |

- The profiles are not perfectly round or equal in size. **In the generated data, with the profile variables used in Chapters 9 and 14, no method separates the isolated and disengaged profiles**: a Gaussian mixture model (Ch 14) finds three clear profiles (balanced, overloaded, and disengaged or isolated), and k-means with four clusters (Ch 9) splits the overloaded students instead. The chapters report three profiles. (Updated 2026-09-24 to match the generated data.)
- About 10 unusual students do not fit any profile, so DBSCAN (Ch 14) can flag them as noise.

### 5.6 Change over time and supervisors (RQ8; Ch 10)
- Wellbeing declines slightly over the two years on average, but students differ in their starting level and in how fast they change (random intercepts and slopes).
- The workshop raises wellbeing from semester 2, and the effect fades gradually (about +5 in semester 2, about +3 by semester 4), giving a workshop × semester interaction.
- **Supervisors matter:** students of the same supervisor are more alike (intraclass correlation ≈ 0.10 for wellbeing).
- `supervisor_meetings` is a count, for a Poisson mixed model (Ch 10's section on count outcomes).

### 5.7 Considering dropout (RQ9; Ch 8, 12)
- About 15% answer Yes: an **imbalanced outcome**, handled deliberately (accuracy is misleading; precision, recall, and AUC are needed).
- Odds of considering dropout increase with stress (odds ratio ≈ 1.8 per SD), financial worry (≈ 1.5 per point), a full-time job, and part-time study; they decrease with supervisor support (≈ 0.6 per SD).
- A realistic ceiling: good models reach an AUC of about 0.78 on test data, not near-perfect, so model comparison is meaningful.
- Models are trained and tested on separate data (fixing the 2025 notes, which tested on the training data).

### 5.8 Attrition and missing data (Ch 2, 3, 6)
- **Attrition:** about 6% of students leave after year 1, so their semester 3-4 rows are missing. Leaving is much more common among students who considered dropout, so the missing data is **not random**: a built-in lesson on why dropping incomplete cases can bias results.
- **Item non-response:** about 2% of questionnaire answers are missing at random. Semester self-reports (sleep, study hours, exercise, caffeine) are missing about 1% of the time.
- Sensitive items (`financial_worry`) are skipped more often (about 5%).

### 5.9 The messy raw file (Ch 2-3)
`wellbeing_raw.xlsx` imitates a real survey export and needs cleaning:
- Unfriendly column names (e.g. `Q3_How many hours do you sleep?`).
- Inconsistent category coding (`F`, `female`, `Female `).
- Numbers stored as text (`"7 hrs"`, `"6,5"`).
- Missing values coded as `99`, `-9`, or blank.
- A few impossible values (age 250, sleep 26 hours, 700 study hours, GPA 34.5) and 12 duplicate rows. In the clean files these cells are empty (NA), because the true value cannot be known.
- Semester measurements in wide format (`gpa_s1`, `gpa_s2`, …), to reshape to long format.
- Test responses at the start of the file (e.g. `student_id` = `TEST`).

### 5.10 Counselling visits (RQ12; Ch 16)
- **Story:** the doctors at the university counselling service hear about Elaf's wellbeing study and ask her to analyse their weekly visit records as an **internal analysis**, to help them plan staffing. It is not part of her thesis, which is why it is a time series while her thesis data is a survey. It also shows readers a common situation: being asked to analyse someone else's data because you know how.
- Weekly visits over 5 academic years with a clear **seasonal pattern** (peaks before exams, drops during breaks), a gentle upward **trend**, and random noise.
- This keeps time series inside the case study (**decided**, instead of a built-in dataset such as `AirPassengers`).

---

## 6. Data used outside the case study
Elaf's data is used **from Chapter 1**. Every new idea, data structure, or code block follows the pattern of the author's lecture notes:

1. **A tiny example first:** a few values, close to the theme where possible (e.g. three friends' sleep hours, `c(6.5, 7, 5.5)`), so readers see exactly what the tool does.
2. **Then Elaf's data:** the same tool applied to the full case study.

In Chapters 1-2, the case study data is introduced gradually (a few students and variables first) so beginners are not faced with four tables and 600 students at once.

Other data supports the case rather than replacing it:

| Data | Purpose |
|---|---|
| Real datasets in the "in your field" boxes | So readers regularly meet real data: e.g. a health example (patients measured at visits), an agriculture example (crop trials), a business example (employee turnover); from standard open datasets or packages where possible |
| `sleepstudy` | A small real example before the case study in Chapter 10 |

---

## 7. Mapping to chapters

| Ch | Case study use |
|---|---|
| 1 | Open the data; first look at a few variables |
| 2 | Import CSV, Excel, and the SPSS file (with labels); data structures |
| 3 | Clean the raw file; compute scale scores; reshape semesters wide → long; join students, semesters, and supervisors |
| 4 | Plot distributions, relationships, change over semesters |
| 5 | Turn the research questions into hypotheses; variables, levels of measurement, constructs, and the study's design |
| 6 | Describe the sample; skewness and outliers; missing data and attrition |
| 7 | Sampling distributions (treating the 600 students as a population and drawing samples); one-sample, two-sample, and paired t-tests; chi-square; non-parametric tests |
| 8 | ANOVA by faculty and study mode; regression for GPA; logistic regression for dropout |
| 9 | Factor analysis and PCA of the questionnaire; k-means and hierarchical clustering into profiles |
| 10 | Mixed models for wellbeing and GPA over semesters, students within supervisors |
| 11 | Machine learning workflow on the dropout question: splitting, recipes, cross-validation |
| 12 | Classification models for dropout risk |
| 13 | Predicting final GPA; regularisation; boosting |
| 14 | Gaussian mixtures and DBSCAN on student profiles |
| 15 | A neural network on dropout risk |
| 16 | Time series of counselling visits |
| 17 | Elaf's reproducible thesis report; a Shiny wellbeing dashboard |
| 18 | AI coding of open-ended answers, validated against the hand-coded subset |
| 19 | The complete project from raw data to thesis chapter |

---

## 8. Generation and checks

- **Script:** `data-raw/generate_wellbeing.R` builds all files from `set.seed()`, in this order: supervisors → students → questionnaire → semesters → dropout → attrition and missingness → open responses → raw messy file → SPSS file.
- **Check script:** `data-raw/check_wellbeing.R` re-runs each chapter's key analysis and confirms the result is close to its target in section 5 (e.g. the workshop effect, the caffeine confounding, the four factors, AUC about 0.80). If a target is missed, the generator is adjusted, not the book.
- **Open text:** answers are generated from templates and phrase banks tied to each student's data, then reviewed by hand; the 200 "hand-coded" themes are checked by the author.
- **Versioning:** the dataset has a version number; the book states which version it uses, so printed results stay consistent.
- **Packages:** base R plus `haven` (SPSS file) and `writexl` (Excel file).

---

## 9. Author's decisions

| Question | Decision |
|---|---|
| Student's name | **Elaf** (chosen by coin toss between Sidra and Elaf) |
| Setting | University and country **not named** |
| Grading scale | GPA on a **0-4** scale |
| Workshop | **Random invitation** |
| Time series | **Counselling visits** inside the case study |
| Chapters 1-4 | **Elaf's data from Chapter 1**, with each tool shown first on a tiny example (section 6) |
| Distribution | **Both:** files in `data/` and an installable Python package |
| Size | **600 students** |
| Faculties | The **five proposed faculties** |

The specification as a whole has been approved by the author.
