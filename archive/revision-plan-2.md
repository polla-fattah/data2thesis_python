# Second revision plan

**Status:** proposal for the author's review, 2026-09-25, updated the same day with the author's guidance and decisions (below). Nothing in this plan has been carried out yet. Decisions marked **(decide)** are the author's.

**The author's guidance on code (2026-09-25):** keep the code, and add more where it helps; do not turn the book into a mostly theoretical text. What is missing is the academic framing and the intuition *before* the code. The code then carries out an idea the reader already understands. Where the code itself is the subject (for example a new R construct), it can come first and be explained after.

**Decisions so far:** the new chapter goes at the start of Part 2 as a new **Chapter 5** (option (a) below); the pilot chapter is **Chapter 6**, hypothesis testing; the heading renames and the styling prototype are to be decided later.

**Chapter numbers** in this plan are the current ones. Once the new Chapter 5 is added, the current Chapters 5 to 18 become 6 to 19.

The first revision (plan.md) rewrote every chapter around one case study. This second revision addresses four points raised by the author:

1. The name Elaf is repeated too often, especially in headings.
2. Code and results do not stand out enough from the text.
3. The book reads like an R manual in the order of a thesis: it needs more academic framing and intuition for each idea before the code, while keeping (and adding to) the code.
4. The book does not teach how to turn a research question into testable hypotheses.

Point 3 is the largest and shapes the rest, so it is planned in most detail (Section 3). Point 4 is part of it (Section 4).

---

## 1. Fewer mentions of Elaf

### What the book does now

- Elaf is named **207 times** in the 18 chapters, between 2.3 and 6.1 times per 1,000 words (most in Chapters 1, 17, 3, and 2).
- **17 headings** contain her name, for example "Elaf's data: a first look", "Elaf's data" (four times), "Elaf's model", "Cleaning Elaf's survey export", "Coding Elaf's open-ended answers", "How well does it agree with Elaf?".
- Many sentences use "Elaf's data" or "Elaf's students" where "the data" or "the students" would do.

### Rules for the revision

- **No names in headings.** Headings name the idea or the task (see the renaming table below).
- **Elaf appears where the story needs a person:** the opening question of each chapter, the moment the chapter moves from the tiny example to the study data (once), decisions a researcher must make ("Elaf decides to…"), and the "Writing it up" box. Everywhere else: "the study", "the students", "the data", "the questionnaire".
- **Target:** about 1 mention per 1,000 words, no more than 5 to 6 per chapter (Chapters 1 and 18 may have a few more, because they frame the story).
- The glossary, appendices, and figure captions do not name her unless necessary.

### Headings to rename (proposal)

| Chapter | Current heading | Proposed heading |
|---|---|---|
| 1 | Elaf's data: a first look | A first look at the study data |
| 1 | About Elaf's data (callout) | About the data in this book |
| 2 | Elaf's data (subsections) | The study data |
| 3 | Putting the verbs together on Elaf's data | Putting the steps together |
| 3 | Cleaning Elaf's survey export | Cleaning a real survey export |
| 6, 7 | Elaf's data (several subsections) | The study data / With the study data |
| 7 | Elaf's model | The dropout model |
| 9 | Elaf's data: change over two years | Change over two years |
| 14 | A neural network for Elaf's dropout question | A neural network for the dropout question |
| 15 | Elaf's counselling data | The counselling records |
| 16 | Elaf's thesis results in Quarto | A results chapter in Quarto |
| 16 | Elaf's wellbeing dashboard | A wellbeing dashboard |
| 17 | Coding Elaf's open-ended answers | Coding open-ended answers |
| 17 | How well does it agree with Elaf? | How well does the model agree with the human coder? |
| A | Elaf's data: the data2thesis package | The book's data: the data2thesis package |

**Effort:** small. A script lists every mention; each is kept or rewritten by hand, so the prose still reads naturally.

---

## 2. Making code and results stand out

### What the author's other book does (polla.dev/ssg-book)

- Code blocks sit in a clearly separate panel: a slightly different background, a thin 1-pixel border, rounded corners (12 px), generous space above and below (24 px), a monospace font a little smaller than the text, and a copy button.
- Inline code (`like this`) has its own tint and colour, so it is visible inside a sentence.
- Section numbers (1.1, 1.2) and short "Pause and check" boxes break up the text.
- The 2025 lecture notes do something similar for R: code and its output each sit in their own bordered, rounded box, so a reader always sees where code ends and results begin.

### What this book does now

- Code: a flat grey box with square corners.
- **Output: no box at all**, only monospace text directly on the page, so results blend into the paragraphs. This is the main problem.
- Long plotting code (10 to 20 lines of `labs()`, `theme()`, colours) interrupts the explanation.

### Proposal (styling only, no change to the text)

1. **Code blocks:** a soft background, a thin border, 8 px rounded corners, and a little more space around them; a small "R" label at the top right.
2. **Output blocks:** directly below the code, in their own lighter box (white or very light background, a thin left accent line in the book's teal colour), with a small "Output" label. Visibly different from code, and from paragraphs, without being loud.
3. **Inline code:** a light tint and a slightly different colour, as in the SSG book.
4. **Figures:** a little more space, and the caption in a smaller, muted style, so the figure reads as a result.
5. The same design in dark mode.

All code stays visible, as the author prefers; the styling only makes it easier to tell code, output, and text apart.

**Process:** prototype on one chapter (Chapter 5), show before-and-after screenshots at desktop and phone width for approval, then apply to the whole book through `site/styles/theme.scss`. **(decide)** after the prototype.

---

## 3. From an R manual to a research methods book

### Diagnosis

The book was written tool-first: each chapter introduces R functions in the order a thesis needs them, and explains ideas through the output of those functions. The code itself is not the problem (it stays, and grows); the problem is what comes before it. Signs of this:

- **Headings name tools, not ideas:** "The tidyverse", "The pipe", "`%>%` in older code", "Working with rows and columns: dplyr", "`group_by()`", "The tidymodels framework", "Preparing the data with a recipe", "Two functions called `alpha()`".
- **The idea arrives through the code:** 445 code chunks in 18 chapters (up to about 200 lines of code in Chapters 3 and 11), often introduced after only a sentence or two about the idea behind them, so the reader learns what a function does before knowing why the method exists.
- **Core research-methods ideas are missing or only implied:**

| Idea | In the book now |
|---|---|
| From research problem to research question to hypothesis | Research questions are given ready-made; never taught |
| Falsifiable, testable hypotheses; stating H0 and H1 before seeing the data | H0 and H1 appear only at test time (Chapter 6) |
| Variables and their roles (outcome, predictor, confounder, moderator) | Only in passing |
| Levels of measurement (nominal, ordinal, interval, ratio) | Not taught |
| Constructs, operationalisation, reliability, validity | Reliability via Cronbach's alpha only; validity not taught |
| Study design (experiment, quasi-experiment, observational, longitudinal, cross-sectional) | Not taught (randomisation mentioned in Chapters 6 and 7) |
| Sampling and generalisation | Sampling distributions yes; sampling methods and who the results apply to, no |
| Planning: effect size, power, and sample size before collecting data | Effect sizes yes; power only named |
| Why and how graphs work (perception, choosing a chart for a question) | Not taught; Chapter 4 is a ggplot2 tutorial |
| Principles of data quality and cleaning decisions | The steps are shown; the principles are not |
| Causation and confounding, with diagrams | Confounding shown once (caffeine and sleep), without a general framework |

### Principles for the rewrite

Every chapter moves from **idea, to intuition, to decision, to R, to interpretation**. The additions are *before and after* the code; the code stays:

1. **The idea in plain words:** what problem it solves for a researcher, and why it matters.
2. **Intuition before formulas and code:** a tiny example worked by hand, a picture or diagram, an analogy, often a simulation (shuffle, resample, repeat) that lets readers *see* the idea.
3. **The decision:** when to use it, what it assumes, and what to choose instead. Decision tables and flowcharts.
4. **R, in full:** the code that carries out the idea, explained step by step, with more code where it builds understanding (for example small simulations, or checking an assumption). Where the code is the subject itself, code first and explanation after.
5. **Interpretation and reporting:** what the result means, what it does not mean, and how to write it in a thesis.
6. **Common misconceptions:** a short list at the end of the main sections.

Practical rules:

- **Headings name ideas and tasks,** never packages or functions ("Choosing the cases you need", not "`filter()`").
- **Learning objectives** start with concepts ("Explain…", "Decide…", "Interpret…") and end with the R skill.
- A **"Think before you analyse"** box before each analysis: What is the question? What is the unit of analysis? Which variables, of what type? What pattern would support the hypothesis, and what would count against it?
- **Intuition code:** new code whose purpose is understanding rather than analysis, such as simulating many samples, shuffling group labels, or drawing what an assumption means, placed before the analysis code.
- **Concept figures,** not only data plots: diagrams of sampling, of the null distribution, of the two kinds of error, of confounding, of overfitting.

### A new opening chapter: from research question to data **(decide)**

The biggest missing piece is the research logic that comes before any analysis. The plan proposes a new chapter at the start of Part 2, provisionally titled **"From Research Question to Data"**. It is more conceptual than the others, but uses R wherever it helps: looking at how each construct is measured in the data, checking the level of measurement of each variable, and small simulations of sampling. Its sections:

1. **What data analysis is for in research:** describing, explaining, predicting; validating claims and testing theories (following the 2025 lecture notes, Part 1).
2. **From a problem to a research question:** narrowing a topic; good and weak questions; descriptive, relational, and causal questions.
3. **From a question to a hypothesis:** a hypothesis as a precise, testable prediction; falsifiability (a hypothesis must say what result would prove it wrong); directional and non-directional hypotheses; the null hypothesis as the "nothing is going on" world that the data may or may not contradict. Worked for every research question of the case study (see Section 4).
4. **Variables and measurement:** constructs and their operationalisation (how "wellbeing" or "stress" becomes a number); levels of measurement and what each allows; variable roles (outcome, predictor, confounder, moderator, mediator).
5. **Reliability and validity:** consistent measurement versus measuring the right thing, with the classic target diagram.
6. **Study designs:** experiments and randomisation (the workshop), observational, cross-sectional and longitudinal designs (the semesters), and what each design can and cannot show about cause.
7. **Samples and populations:** who the results apply to; sampling methods; non-response and attrition.
8. **Planning the analysis:** matching each hypothesis to an analysis before collecting data; effect sizes and sample size; preregistration (link to Chapter 16).

Placement options (**decided: option (a)**, 2026-09-25):

- **(a) A new Chapter 5, "From Research Question to Data"**, opening Part 2, before descriptive statistics. Chapters 5 to 18 become 6 to 19. This fits the book's path: tools in Part 1, research logic at the start of the statistics part. *(Recommended.)*
- **(b) A new Chapter 1**, before any R. Strong framing, but readers wait longer for their first R code, and every chapter number changes.
- **(c) No new chapter**: spread the material over Chapters 1, 2, 5, and 6. No renumbering, but the ideas stay scattered and easy to miss.

Renumbering was done once before (the Chapter 14 split) and is mostly mechanical; the frozen results make it safe.

### Chapter by chapter

For each chapter: what to add or strengthen, and what to rename, and how much work it is. Existing code is kept everywhere unless it is replaced by better code. **Effort:** S = a few sections touched, M = several sections rewritten, L = most of the chapter rewritten.

**Chapter 1, Getting Started (S).** Keep as the practical start. Add a short opening on why research is done in code (a record of every decision). Move "Coming from SPSS or Excel" material that is really about workflow into one place.

**Chapter 2, Data Structures (M).** Reframe around *data as measurement*: the data matrix (cases × variables), the unit of analysis, variables and their types, and how levels of measurement map to R (nominal → factor, ordinal → ordered factor, interval and ratio → numeric). Headings such as "Vectors: the building block" become "Variables and their values", "Categories", "A table of cases". A codebook as the bridge between the questionnaire and the data.

**Chapter 3, Data Manipulation (M).** Put **data quality and cleaning decisions** first: what "clean" means (valid, accurate, complete, consistent, unique), why cleaning is part of the analysis, and why every decision is recorded. Tidy data explained with a picture before any code. Headings by task: "Choosing the cases you need", "Creating new variables", "Summarising by group", "Reshaping between wide and long", "Combining tables". Before each cleaning step, the reason for it (what problem it fixes, and what would go wrong without it); then the code.

**Chapter 4, Data Visualisation (L).** Rebuild around **how graphs communicate**:
- What a graph is for: exploring versus explaining.
- Choosing a graph from the question and the variable types (a decision table: one numeric variable → histogram or box plot; numeric by group → box plots; two numeric → scatter plot; change over time → line chart).
- How people read graphs: position is read most accurately, then length, angle, area, and colour (Cleveland and McGill); so bar charts and dot plots beat pie charts.
- Honest graphs: axis ranges, aspect ratio, clutter, colour for categories versus quantities, colour-blind palettes.
- A before-and-after critique of a poor graph of the study data.
- ggplot2 taught as the tool that follows from the grammar of graphics; the polishing code stays, now explained as design decisions (why this colour, this scale, this label).

**Chapter 5, Descriptive Statistics (S to M).** Already the most conceptual. Add: the level of measurement decides which summary is meaningful; intuition for the standard deviation (the typical distance from the mean, shown on a plot); every number needs its spread and its *n*; outliers as information before they are problems.

**Chapter 6, Hypothesis Testing (L).** Build the logic before the tests:
- Start from the hypotheses written in the new chapter (the workshop, sleep) and restate them as H0 and H1 before looking at the data.
- **A permutation test first:** shuffle the workshop labels many times to build the "no effect" distribution, and see where the real difference falls. The p-value then has a picture before it has a formula; the t-test follows as the shortcut.
- Falsification in practice: what result would count against the hypothesis, decided in advance.
- Type I and II errors and **power, by simulation:** how often a study of a given size would detect an effect of a given size; planning a sample size.
- Statistical versus practical significance (already present), and the dangers of many tests and flexible analyses (link to preregistration).
- The tests themselves (one-sample, two-sample, paired, chi-square, non-parametric) keep their code, each introduced by the question it answers and the hypothesis it tests; the decision table (already present) ties them together.

**Chapter 7, ANOVA and Regression (M).** Intuition for **partitioning variation** (a picture of between-group and within-group spread) before the F test; regression as "the average outcome for given predictor values", shown on a scatter plot with conditional means; **confounding with a simple diagram** (caffeine, sleep, GPA) and the general rule it illustrates; assumptions shown with pictures of when they fail. After `summary()`, more space for what each number means for the research question.

**Chapter 8, Multivariate Methods (M).** Open with **constructs and latent variables**: why a questionnaire uses many items for one idea; reliability versus validity (link to the new chapter); what factor analysis assumes. Clustering as a *description* of the data, not a discovery of natural groups (already in a warning; make it the frame). Rename "Two functions called `alpha()`" into a short note inside the reliability section.

**Chapter 9, Mixed-Effects Models (S to M).** Strengthen the intuition for **non-independence**: why repeated measurements of one person are not new information, shown with a simulation where ignoring the structure gives the wrong uncertainty; the ICC as "how much people differ from each other compared with how much they change".

**Chapter 10, Introduction to Machine Learning (M).** Frame prediction as a different kind of research question with a different standard of evidence (performance on new data). **Generalisation and overfitting** by picture (a curve that fits the training points perfectly and new points badly), and the bias-variance trade-off in plain words. The tidymodels steps kept in full, introduced as the design of a fair test.

**Chapter 11, Classification (M).** More on **judging predictions**: the confusion matrix, costs of errors, and thresholds as a research and ethical decision. Each model family introduced by its idea and the picture of its decision boundary (already present), before its code.

**Chapter 12, Predictive Regression (S to M).** Lead with the idea of **too many predictors for the data** and shrinkage as a remedy, with the 60-student experiment (already present) as the central example; boosting explained by the step-by-step picture before the tuning code.

**Chapter 13, Advanced Clustering (S).** Frame around "what is a group?"; soft versus hard membership; judging a clustering without an answer key.

**Chapter 14, Neural Networks (S).** Already concept-first (the neuron is a logistic regression). Keep the code; add a short explanation of what training does, with a small hand-worked example of one gradient-descent step.

**Chapter 15, Time Series Forecasting (S to M).** Open with **time series thinking**: dependence over time, trend and seasonality as parts of a pattern, and forecasts as ranges rather than numbers, before the fable code.

**Chapter 16, Reproducible Research (S to M).** Frame reproducibility as **research integrity and credibility** (why results must be checkable), before the tools. Keep the Shiny app code in full, introduced by the ideas of inputs, outputs, and reactivity.

**Chapter 17, Using AI with R (S).** Already concept-led (validation of coding, kappa, responsible use). Keep the code; open with the research question of qualitative coding (how do we know a coder is reliable?) before any AI.

**Chapter 18, Putting It All Together (S to M).** Add a closing **chain of reasoning** for each research question: question → hypothesis → design → variables → analysis → result → conclusion → limitation. Link to reporting standards (for example the APA's Journal Article Reporting Standards) for how quantitative results are reported.

### Throughout the book

- A short **"In one sentence"** statement at the start of each main section: the idea the section teaches.
- **"Think before you analyse"** boxes before each analysis (Section 3 principles).
- **"Common misconceptions"** at the end of each chapter's main content.
- Exercises: add conceptual questions ("Which graph would you choose, and why?", "Write the null hypothesis for…", "What result would count against…?") alongside the coding exercises, which stay; the playground gets matching exercises.
- Glossary: add the new terms (falsifiability, operationalisation, construct, validity, level of measurement, study design, power, and others).

---

## 4. Question: does the book teach how to form hypotheses?

**Answer: no, not properly.** What the book does now:

- The research questions (RQ1 to RQ12) are given to Elaf ready-made in each chapter's opening; the book never shows how they were developed or how to write a good one. The complete list appears only at the end, in Chapter 18.
- The null and alternative hypotheses first appear in Chapter 6, at the moment of testing (for example "the workshop has no effect on wellbeing"). They are defined correctly, but as part of the test's mechanics, not as the planned, testable statements that a study is designed around.
- Falsifiability, operationalisation, directional hypotheses, and stating the hypotheses (and the result that would count against them) *before* seeing the data are not taught. Preregistration is mentioned only in Chapter 16.

**Proposal** (part of the new chapter in Section 3, and carried through the book):

1. Teach the path **research problem → research question → hypothesis → prediction → test**, with examples of weak and good questions and hypotheses.
2. Define a good hypothesis: specific, about a stated population, **testable with available data, and falsifiable** (it names the result that would count against it); directional or non-directional, decided in advance.
3. Show how each hypothesis is **operationalised**: which variables, measured how, compared how.
4. Write the **null hypothesis** for each, as the "nothing is going on" world the data is compared with, and explain what rejecting it does and does not mean.
5. Give a table for the case study, used throughout the book, for example:

| Research question | Hypothesis (H1) | Null hypothesis (H0) | What would count against H1 | Chapter |
|---|---|---|---|---|
| RQ2: Do graduate students sleep less than 7 hours? | Mean sleep is below 7 hours | Mean sleep is 7 hours or more | An average of 7 hours or more, or a confidence interval that includes 7 | 6 |
| RQ3: Does the workshop improve wellbeing? | Invited students have higher wellbeing in semester 2 than students not invited | No difference in wellbeing between the groups | A difference near zero or negative, with a narrow interval | 6, 9 |
| RQ5: What explains GPA? | More sleep is associated with higher GPA, holding study hours, stress, and support constant | The sleep coefficient is zero | A coefficient near zero or negative | 7 |
| RQ9: Who considers dropping out? | Higher stress raises the odds of considering dropout | The odds ratio for stress is 1 | An odds ratio of 1 or below | 7, 11 |

6. Each later chapter restates the relevant hypothesis **before** its analysis and returns to it in the conclusion ("the data contradict / do not contradict H0, so…").
7. Exploratory questions (profiles, prediction) are labelled as such: no hypothesis is tested, and the results suggest hypotheses for future work.

---

## 5. Order of work and decisions

| Step | Work | Effort | Decision needed |
|---|---|---|---|
| 1 | Fewer mentions of Elaf; rename headings (Section 1) | Small | Approve the heading names |
| 2 | Code and output styling: prototype on one chapter, then the whole book (Section 2) | Small | **Done** (2026-09-25): the look of the author's front-end book, in light and dark |
| 3 | New Chapter 5 "From Research Question to Data", including hypotheses (Sections 3 and 4); renumber Chapters 5 to 18 | Large | **Done** (2026-09-25) |
| 4 | Pilot rewrite of Chapter 6 (hypothesis testing; Chapter 7 after renumbering), for the author to judge the new balance before the rest | Medium | **Done** (2026-09-25), reviewed by the author; his comments became Section 6 |
| 5 | Conceptual rewrite of the remaining chapters, in the order of the book, each followed by a fresh render, fact check, and the checklist in Section 6 | Large | Review each chapter |
| 6 | Glossary, playground exercises, README outline, and plan.md updated for the new content | Medium | - |

Each step keeps the working rules of the first revision: every number computed from the data, every claim checked, tiny examples before the study data, and no commit or push without the author's instruction.


---

## 6. Checklist for every chapter in the second round

The Chapter 7 pilot produced two sets of lessons: the author's comments on its writing, and the faults found when the rewritten chapter was reviewed again. Both apply to every chapter. Each chapter is revised with part A in mind and then checked against part B before it is handed to the author.

### A. Writing (the author's rules, from his review of Chapter 7)

1. **Open with the idea, not with Elaf.** A chapter begins with the research problem or the concept; the case study enters afterwards.
2. **No paragraph starts with code.** A function or object name never opens a paragraph. Write a word-led sentence ("The line `set.seed(2026)` fixes…"), or at least "The function `set.seed()`…".
3. **No questions as headings or paragraph openers.** "How big is the difference?" becomes "Effect size"; "What does 95% mean?" becomes a statement.
4. **Prose before lists.** No numbered or bulleted list directly after a heading or a one-line introduction. Connected paragraphs are the default; a list is kept only where it genuinely helps (objectives, summaries, exercises, a list of misconceptions after a proper introduction).
5. **Precise, academic headings.** No casual words ("Goodness of fit" became "Test of expected proportions"); the common name can be given in the text.
6. **Short headings, rarely with a colon.** A heading names one idea and does not carry extra information ("When assumptions fail: non-parametric tests" became "Non-parametric tests").

### B. Review pass (generalised from the second review of Chapter 7)

1. **Consistency with earlier chapters.** Every hypothesis, definition, and number that another chapter also states must agree with it, or the difference must be explained. *(Chapter 7 tested RQ2 two-tailed although Chapter 5 stated it with a direction; the text now explains the choice.)* Check especially against Chapter 5's hypothesis table and Chapter 19's map.
2. **Precise definitions.** Statistical definitions are checked word by word, because small slips teach wrong ideas. *(The p-value callout said "a difference this large" instead of "at least this large".)* Typical places: p-values, confidence intervals, power, effect sizes, "significant", "cause".
3. **No oversimplified claims.** A simplification is acceptable only if it stays true. *(Power was said to be "not controlled by the significance level"; it depends on effect size, sample size, and the significance level.)* Check every "only", "never", "always", and "not … but".
4. **Results that readers will meet in practice.** Where the code produces an edge case (a p-value of 0, a warning, a singular fit, an empty group), the text says what it means and how to report it. *(A permutation p-value of 0 is reported as p < .001.)*
5. **No hard-coded numbers.** Every number in the prose that comes from the data is written as inline R, so it cannot drift out of step with the code. *(Three numbers in Chapter 7, such as the sleep interval, were typed by hand.)* Rounded descriptions ("about a quarter") are acceptable when the exact value is shown nearby.
6. **Text that describes code must match the code.** Descriptions such as "the first line", "the function below", "the output shows three parts" are checked against the chunk and its output. *(`set.seed()` was called "the first line" of a chunk that begins with `library()`.)*
7. **Logical order of sections.** Each section should follow from the one before it; a section that answers a problem comes directly after the section that raises it. *(Non-parametric tests, the answer to failed assumptions, was separated from the assumptions section by chi-square tests.)*

The review pass is kept proportionate: it looks for faults that would mislead a reader or embarrass the book, not for every possible improvement. Improvements that would add new material (for example a simulation of what "95% confidence" means, suggested for Chapter 7 and not yet added) are listed for the author to decide, not added silently.
