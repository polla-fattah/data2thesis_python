# Slide Architecture & Development Plan: From Data to Thesis (R4NTR)

This document establishes the pedagogical design, slide anatomy, depth targets, and chapter-by-chapter blueprint for the lecture slide decks of **FROM DATA TO THESIS: Using R for Non-Technical**.

It is directly modeled on the depth, cadence, and architectural standards of the companion engineering book (`new-lectures`), adapting its proven slide engineering practices to graduate research methodology, biostatistics, and data science with R.

---

## 1. Benchmark Analysis from the Reference Project (`new-lectures`)

An audit of the 18 slide decks in `new-lectures/content/slides/` reveals the following structural parameters:

| Metric | Reference Project Benchmark | R4NTR Slide Standard |
|---|---|---|
| **Average Slide Count** | 80–120 slides per chapter | 60–100 slides per chapter |
| **Pacing & Density** | 1 core concept per slide; no walls of text | 1 concept/finding per slide; 2–4 concise points |
| **Visual Artifacts** | ASCII dependency graphs, tables, code comparisons | ASCII flow diagrams, ggplot2 figures, syntax vs. output tables |
| **Concrete Case Study** | Consistent ecommerce platform problem | Consistent graduate study: Elaf’s 600 students, 4 semesters |
| **Output Format** | Standard Markdown (`---` slide delimiters) | Quarto RevealJS (`.qmd`) + Marp compatible Markdown |

---

## 2. The 7-Phase Pedagogical Slide Arc

Every chapter slide deck in R4NTR follows a strict, repeatable 7-phase sequence:

```text
Phase 1: The Thesis Hook (Elaf's dilemma & research question)
   │
Phase 2: What We Will Explain (Explicit roadmap & learning objectives)
   │
Phase 3: The Minimal Example (Handful of numbers: vectors/toy tibble)
   │
Phase 4: Theoretical & Methodological Mechanics (Intuition, assumptions, formulas)
   │
Phase 5: The Case-Study Analysis (Elaf's data: R code, tidy outputs, plots)
   │
Phase 6: In Your Field (Cross-disciplinary box: Health, Agriculture, Business)
   │
Phase 7: Reporting in a Thesis (APA/thesis wording, table design, checklist)
```

### Slide Anatomy Guidelines
1. **Title & Headline**: Every slide has a descriptive, assertive headline (e.g., `## Unequal Variances Distort the p-value`, not `## Levene's Test`).
2. **Text Constraint**: Maximum 3–4 bullet points or 35–45 words per slide.
3. **Paired Comparison Slides**: Use two sequential slides for `Problem` vs `Solution`, or side-by-side columns for `Old Way (SPSS/Base)` vs `Tidyverse Way`.
4. **Code Precision**: Keep R code blocks focused on 4–8 lines highlighting the exact verbs and pipes (`|>`).

---

## 3. Chapter-by-Chapter Slide Specifications (Chapters 1 to 19)

### Part 1: Foundations of R Programming and Data Handling

#### Chapter 1: Getting Started with R
* **Target Count**: 50–65 slides
* **Research Context**: Elaf's first day; 600 students across 5 faculties.
* **Core Modules**:
  1. *The Thesis Dilemma*: Why point-and-click analysis creates reproducibility crises in thesis examinations.
  2. *The R & RStudio Environment*: Four panes, console vs. script, working directory, RStudio projects.
  3. *Core Language Primitives*: Objects, `<-`, data types (`numeric`, `character`, `logical`, `NA`), vectors with `c()`.
  4. *Functions & Arguments*: `mean()`, `max()`, `round()`, `na.rm = TRUE`.
  5. *Package Ecosystem*: Buying the book (`install.packages`) vs. taking it off the shelf (`library`).
  6. *First Touch on Case Data*: Loading `data2thesis`, examining `students` (`nrow`, `ncol`, `head`).
  7. *In Your Field*: Agricultural crop yields (`PlantGrowth`).
  8. *Thesis Checkpoint*: Documenting R versions and computational environment.

#### Chapter 2: Data Structures and Data Import
* **Target Count**: 65–80 slides
* **Research Context**: Survey exports, questionnaires, and multi-table records.
* **Core Modules**:
  1. *Measurement Levels*: Nominal, ordinal, interval, ratio, and how R represents them (factors vs numbers).
  2. *Data Structures*: Vectors, factors, data frames, tibbles, lists.
  3. *Import Toolchain*: Reading CSV (`readr`), Excel (`readxl`), SPSS (`haven`).
  4. *Data Dictionaries & Codebooks*: Variable labels, value labels, question wording preservation.
  5. *Common Import Traps*: String encoding, trailing spaces, decimal commas, silent type conversions.
  6. *In Your Field*: Medical diagnostic datasets and clinical trial exports.
  7. *Thesis Checkpoint*: Preparing the methodology chapter data provenance appendix.

#### Chapter 3: Data Manipulation with dplyr and tidyr
* **Target Count**: 75–90 slides
* **Research Context**: Cleaning the raw, messy survey export (`wellbeing_raw.xlsx`).
* **Core Modules**:
  1. *What Clean Data Means*: Validity, accuracy, completeness, consistency, uniqueness.
  2. *Tidy Data Principles*: Observations as rows, variables as columns, values in cells.
  3. *The Modern Pipe*: `|>` as "and then".
  4. *The Five Core dplyr Verbs*: `filter()`, `select()`, `arrange()`, `mutate()`, `summarise()`.
  5. *Grouping Mechanics*: Modern `.by` syntax vs legacy `group_by()`.
  6. *Reshaping Data*: `pivot_longer()` and `pivot_wider()`.
  7. *Relational Joins*: `left_join()`, `anti_join()`, linking students to supervisor rankings and semesters.
  8. *Case Study Deep-Dive*: Handling duplicate submissions, cleaning typos with `stringr`, handling `-99` codes.
  9. *Thesis Checkpoint*: Sample attrition flowchart and data cleaning log.

#### Chapter 4: Data Visualization with ggplot2
* **Target Count**: 80–95 slides
* **Research Context**: Visualizing graduate student wellbeing distributions and semester changes.
* **Core Modules**:
  1. *Grammar of Graphics*: Data, aesthetics (`aes`), geometric objects (`geom`), scales, facets, themes.
  2. *Univariate Visualizations*: Histograms (`geom_histogram`), density plots (`geom_density`), bar charts.
  3. *Bivariate & Multivariate*: Scatter plots (`geom_point`), boxplots (`geom_boxplot`), violin plots.
  4. *Faceting for Subgroups*: `facet_wrap()` by faculty, `facet_grid()` by study mode and workshop.
  5. *Aesthetic Mapping vs Fixed Attributes*: Color mapping vs setting `color = "darkblue"`.
  6. *Publication-Ready Styling*: APA theme customization, typography, color-blind friendly palettes (`viridis`).
  7. *Thesis Checkpoint*: Figure caption standards, resolving raster vs vector formats (PNG vs PDF/SVG).

---

### Part 2: Statistical Analysis for Research

#### Chapter 5: From Research Question to Analysis Plan
* **Target Count**: 60–75 slides
* **Research Context**: Elaf's 12 research questions and study operationalization.
* **Core Modules**:
  1. *Formulating Answerable Questions*: Specific, measurable, feasible, novel.
  2. *Confirmatory vs Exploratory Research*: Pre-registration, hypothesis testing vs pattern finding.
  3. *Operationalizing Psychological Constructs*: Turning "wellbeing" and "stress" into measurable indices.
  4. *Study Designs*: Cross-sectional, longitudinal, experimental vs observational.
  5. *Power Analysis*: Sample size determination, effect size estimation, Type I and Type II errors.
  6. *Constructing the Analysis Plan*: Mapping each RQ to a specific statistical model.
  7. *Thesis Checkpoint*: Drafting Chapter 3 (Methodology) of the thesis.

#### Chapter 6: Descriptive Statistics and Exploratory Data Analysis
* **Target Count**: 70–85 slides
* **Research Context**: Describing the 600 graduate students across faculties and semesters.
* **Core Modules**:
  1. *Central Tendency*: Mean vs median vs trimmed mean; when skewness makes the mean deceptive.
  2. *Dispersion*: Standard deviation, variance, IQR, MAD.
  3. *Testing Normality*: Skewness/kurtosis, Q-Q plots, Shapiro-Wilk test limitations on large N.
  4. *Cross-Tabulations*: Contingency tables, row/column percentages, chi-square test of independence.
  5. *Missing Data Patterns*: MCAR, MAR, MNAR; detecting selective dropout in semester 3.
  6. *Case Study Table 1*: Building the canonical participant demographics table.
  7. *Thesis Checkpoint*: APA formatted sample characteristics table.

#### Chapter 7: Hypothesis Testing and Comparing Groups
* **Target Count**: 85–100 slides
* **Research Context**: RQ1: "Does the wellbeing workshop improve student scores?"
* **Core Modules**:
  1. *The Logic of Significance Testing*: Sampling distributions, null hypotheses, p-values.
  2. *Comparing Two Independent Groups*: Independent two-sample t-test, Welch's correction.
  3. *Paired Comparisons*: Paired t-test for within-subject change over time.
  4. *Assumptions & Diagnostics*: Normality of residuals, homogeneity of variance (Levene's test).
  5. *Non-Parametric Fallbacks*: Mann-Whitney U / Wilcoxon rank-sum test, Wilcoxon signed-rank test.
  6. *Effect Sizes*: Cohen's d, Hedges' g, confidence intervals around effect sizes.
  7. *Case Study Analysis*: Workshop vs control group wellbeing comparison.
  8. *Thesis Checkpoint*: Reporting t-test results in standard academic format ($t(df) = ..., p = ..., d = ...$).

#### Chapter 8: ANOVA and Linear Regression
* **Target Count**: 90–110 slides
* **Research Context**: RQ2 & RQ3: Comparing faculties (ANOVA) and predicting wellbeing from sleep and stress (Regression).
* **Core Modules**:
  1. *One-Way ANOVA*: Partitioning variance ($SS_{between}$ vs $SS_{within}$), F-distribution.
  2. *Post-Hoc Tests*: Tukey's HSD, Bonferroni adjustments, controlling Family-Wise Error Rate.
  3. *Two-Way Factorial ANOVA*: Main effects, interaction effects, interaction plots.
  4. *Simple Linear Regression*: Ordinary Least Squares (OLS), slope ($\beta_1$), intercept ($\beta_0$), $R^2$.
  5. *Multiple Linear Regression*: Confounding, partial slopes, multicollinearity (VIF).
  6. *Regression Diagnostics*: Residuals vs fitted, Q-Q residuals, scale-location, Cook's distance.
  7. *Case Study Execution*: Predicting wellbeing from sleep hours, financial worry, and supervisor support.
  8. *Thesis Checkpoint*: Regression summary tables with unstandardized $B$, $SE$, standardized $\beta$, and $p$.

#### Chapter 9: Questionnaire Scales and Factor Analysis
* **Target Count**: 75–90 slides
* **Research Context**: Analysing the 22 survey items (stress, burnout, support, satisfaction).
* **Core Modules**:
  1. *Measurement Theory*: Observed indicators vs latent constructs.
  2. *Reliability Analysis*: Internal consistency, Cronbach's alpha ($\alpha$), McDonald's omega ($\omega$).
  3. *Item Analysis*: Corrected item-total correlations, alpha-if-item-deleted.
  4. *Exploratory Factor Analysis (EFA)*: Factorability (KMO, Bartlett's test), extraction methods.
  5. *Determining Number of Factors*: Scree plot, parallel analysis, Kaiser's rule.
  6. *Factor Rotations*: Orthogonal (Varimax) vs Oblique (Promax, Oblimin).
  7. *Factor Loadings & Scale Construction*: Building composite sum and mean scores.
  8. *Thesis Checkpoint*: Factor loading matrix reporting and scale reliability tables.

#### Chapter 10: Change Over Time and Mixed Models
* **Target Count**: 85–105 slides
* **Research Context**: Tracking students across 4 consecutive semesters; clustered within supervisors.
* **Core Modules**:
  1. *The Challenge of Repeated Measures*: Non-independence of observations, correlated errors.
  2. *Repeated Measures ANOVA*: Mauchly's sphericity, Greenhouse-Geisser corrections, missing data drawbacks.
  3. *Linear Mixed-Effects Models (LMM)*: Fixed effects vs random effects (`lme4::lmer`).
  4. *Random Intercept Models*: Allowing student baselines to vary.
  5. *Random Slope Models*: Allowing student trajectories over time to vary.
  6. *Handling Multilevel Nesting*: Students nested within supervisors, nested within faculties.
  7. *Model Comparison*: AIC, BIC, Likelihood Ratio Tests (`anova()`).
  8. *Thesis Checkpoint*: Multilevel table reporting: fixed parameter estimates, variance components, intraclass correlation (ICC).

---

### Part 3: Machine Learning with R

#### Chapter 11: Machine Learning with R: Principles
* **Target Count**: 60–75 slides
* **Research Context**: Transitioning from explanation (p-values) to prediction (dropout prevention).
* **Core Modules**:
  1. *Inference vs Prediction*: Why a high $R^2$ or significant $p$-value fails out-of-sample.
  2. *The Bias-Variance Tradeoff*: Underfitting, overfitting, model complexity.
  3. *Data Splitting Strategies*: Train/test splits, stratification.
  4. *Resampling & Cross-Validation*: K-fold CV, repeated CV, preventing data leakage.
  5. *The Tidymodels Framework*: Recipes, model specifications (`parsnip`), workflows.
  6. *Evaluation Metrics*: RMSE, MAE, $R^2$ for regression; Accuracy, ROC-AUC for classification.
  7. *Thesis Checkpoint*: Justifying ML approaches in academic empirical research.

#### Chapter 12: Classification Models
* **Target Count**: 80–100 slides
* **Research Context**: Predicting graduate student dropout risk (`considering_dropout`).
* **Core Modules**:
  1. *Binary Classification*: Logistic regression as an ML classifier.
  2. *K-Nearest Neighbors (KNN)*: Distance metrics, scaling requirements.
  3. *Decision Trees*: Splitting criteria (Gini, entropy), pruning, interpretability.
  4. *Ensemble Methods: Random Forests*: Bagging, out-of-bag error, feature importance (`vip`).
  5. *Support Vector Machines (SVM)*: Hyperplanes, soft margins, radial basis kernels.
  6. *Evaluating Classifiers*: Confusion matrices, sensitivity, specificity, precision, recall, F1-score, ROC curves.
  7. *Class Imbalance*: Synthetic minority oversampling (SMOTE, `themis`), threshold tuning.
  8. *Thesis Checkpoint*: Reporting classifier performance curves and confusion matrices.

#### Chapter 13: Predictive Regression and Regularization
* **Target Count**: 70–85 slides
* **Research Context**: Predicting final semester GPA from survey variables and attendance.
* **Core Modules**:
  1. *Overfitting in High-Dimensional Data*: When predictors approach sample size.
  2. *Shrinkage & Regularization*: Penalized loss functions.
  3. *Ridge Regression (L2 penalty)*: Handling multicollinearity, shrinking coefficients toward zero.
  4. *Lasso Regression (L1 penalty)*: Automatic feature selection, sparse models.
  5. *Elastic Net*: Balancing L1 and L2 penalties (`glmnet`).
  6. *Hyperparameter Tuning*: Tuning $\lambda$ and $\alpha$ with cross-validation grids.
  7. *Gradient Boosting Machines (XGBoost)*: Sequential tree boosting, learning rates, tree depth.
  8. *Thesis Checkpoint*: Visualizing regularization coefficient paths and reporting tuned hyperparameters.

#### Chapter 14: Clustering and Unsupervised Learning
* **Target Count**: 75–90 slides
* **Research Context**: Discovering natural student wellbeing and engagement profiles.
* **Core Modules**:
  1. *Unsupervised Learning Philosophy*: Finding latent structure without labels.
  2. *Data Preprocessing for Clustering*: Standardizing variables, distance metrics (Euclidean, Manhattan).
  3. *K-Means Clustering*: Centroid updates, WCSS, elbow method, silhouette analysis.
  4. *Hierarchical Clustering*: Agglomerative methods (Ward's, complete, average), dendrograms.
  5. *Model-Based Clustering*: Gaussian Mixture Models (GMM, `mclust`), BIC criteria.
  6. *Density-Based Clustering*: DBSCAN, handling arbitrary cluster shapes and noise.
  7. *Validating & Profiling Clusters*: Visualizing clusters with PCA / t-SNE, demographic profiling.
  8. *Thesis Checkpoint*: Interpreting student profiles in a thesis discussion chapter.

#### Chapter 15: Neural Networks and Deep Learning
* **Target Count**: 70–85 slides
* **Research Context**: Modeling complex non-linear interactions in student behavioral patterns.
* **Core Modules**:
  1. *Biological vs Artificial Neurons*: Perceptrons, inputs, weights, biases.
  2. *Activation Functions*: Sigmoid, Tanh, ReLU, Softmax.
  3. *Network Architecture*: Input layer, hidden layers, output layer, width vs depth.
  4. *Training Mechanics*: Forward propagation, loss functions, backpropagation, gradient descent.
  5. *Optimization & Regularization*: Learning rates, momentum, Adam optimizer, dropout, early stopping.
  6. *Implementation in R*: Multi-layer perceptrons with `tidymodels` and `nnet`.
  7. *Interpreting Black-Box Models*: Partial dependence plots, VIP.
  8. *Thesis Checkpoint*: Critical academic evaluation of deep learning vs traditional statistical models.

#### Chapter 16: Time Series Analysis and Forecasting
* **Target Count**: 75–90 slides
* **Research Context**: Forecasting monthly university counselling service visits.
* **Core Modules**:
  1. *Time Series Characteristics*: Temporal ordering, autocorrelation, stationarity.
  2. *The Tidy Time Series Ecosystem*: `tsibble`, `feasts`, `fable`.
  3. *Time Series Decomposition*: Trend, seasonal, irregular components (STL decomposition).
  4. *Exponential Smoothing*: Simple, Holt's linear trend, Holt-Winters seasonal (ETS).
  5. *ARIMA Modeling*: Autoregressive ($p$), Integrated ($d$), Moving Average ($q$), unit root tests.
  6. *Evaluating Forecast Accuracy*: Train/test horizons, MASE, RMSE, prediction intervals.
  7. *Case Study Forecast*: Projecting counselling resource demands for future semesters.
  8. *Thesis Checkpoint*: Communicating forecasts, uncertainty ribbons, and seasonal implications.

---

### Part 4: Reproducible Research and Applications

#### Chapter 17: Reproducible Research and Thesis Reporting
* **Target Count**: 80–95 slides
* **Research Context**: Converting scripts and data into an automated Master's thesis chapter and dashboard.
* **Core Modules**:
  1. *The Reproducibility Crisis*: File versions (`thesis_v2_final_FINAL.docx`), irreproducible tables.
  2. *Literate Programming*: Weaving text, math, code, and figures in Quarto (`.qmd`).
  3. *Computational Freeze*: Managing execution cache with `freeze: auto`.
  4. *Automating Thesis Tables*: `knitr::kable`, `gt`, `tinytable` with APA formatting.
  5. *Cross-Referencing*: Figures (`@fig-`), tables (`@tbl-`), and equations (`@eq-`).
  6. *Bibliographic Management*: BibTeX (`references.bib`), citation keys, CSL styles.
  7. *Interactive Dashboards*: Building research dissemination tools with Shiny and `bslib`.
  8. *Project Environment Management*: Dependency locking with `renv`.
  9. *Thesis Checkpoint*: The complete reproducible submission bundle.

#### Chapter 18: Using AI Responsibly in Research Data Analysis
* **Target Count**: 70–85 slides
* **Research Context**: Qualitative coding of 600 open survey responses using LLMs (`ellmer`).
* **Core Modules**:
  1. *AI in Academic Research*: Opportunities, boundaries, and ethical mandates.
  2. *How LLMs Work (and Why They Hallucinate)*: Token prediction, temperature, context windows.
  3. *AI as Coding Assistant*: Prompting for R code, verifying packages, avoiding obsolete syntax.
  4. *Qualitative Thematic Coding with R*: Hand-coding benchmarks vs AI assistance.
  5. *Calling Models with `ellmer`*: Structured outputs, system prompts, API safety.
  6. *Measuring Inter-Rater Reliability*: Cohen's kappa ($\kappa$), confusion matrix between human and LLM.
  7. *University & Publisher Disclosure Guidelines*: Acknowledging AI use, data privacy policies.
  8. *Thesis Checkpoint*: Drafting an AI methodology disclosure statement for examiners.

#### Chapter 19: The Complete Thesis Project
* **Target Count**: 80–100 slides
* **Research Context**: The synthesis: from raw messy survey to the defended thesis results chapter.
* **Core Modules**:
  1. *The Complete Arc*: Tracing Elaf's full journey across all 18 chapters.
  2. *Answering the 12 Research Questions*: The comprehensive findings matrix.
  3. *The Chain of Reasoning*: Hypotheses $\rightarrow$ operationalization $\rightarrow$ statistical test $\rightarrow$ thesis claim $\rightarrow$ limitations.
  4. *Synthesis Visualizations*: Multi-panel executive figures using `patchwork`.
  5. *Integrating Quantitative Findings into the Discussion*: Theoretical implications and institutional recommendations.
  6. *Examiner Defense Preparation*: The top 10 statistical questions examiners ask and how to answer them with code.
  7. *Thesis Checkpoint*: The final submission checklist.

---

## 4. Execution Plan: Sequential One-by-One Authoring

To ensure exceptional depth and pedagogical consistency, slide decks will be authored sequentially in individual milestones:

```text
[Sprint 1] Phase 1: Foundations (Chapters 1–4)
   ├── 01-getting-started
   ├── 02-data-structures
   ├── 03-data-manipulation
   └── 04-data-visualization

[Sprint 2] Phase 2: Statistical Core (Chapters 5–10)
   ├── 05-research-question
   ├── 06-descriptive-statistics
   ├── 07-hypothesis-testing
   ├── 08-anova-regression
   ├── 09-multivariate
   └── 10-mixed-models

[Sprint 3] Phase 3: Machine Learning (Chapters 11–16)
   ├── 11-machine-learning
   ├── 12-classification
   ├── 13-predictive-regression
   ├── 14-advanced-clustering
   ├── 15-neural-networks
   └── 16-time-series

[Sprint 4] Phase 4: Synthesis & Reporting (Chapters 17–19)
   ├── 17-reproducible-research
   ├── 18-ai
   └── 19-putting-it-together
```

### Next Immediate Action:
Author the comprehensive slide deck for **Chapter 1: Getting Started with R** (target 50–65 slides) following the verified template and integrating it directly into `content/slides/01-getting-started.qmd`.
