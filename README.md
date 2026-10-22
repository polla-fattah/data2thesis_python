# FROM DATA TO THESIS: Using Python for Non-Technical

<p align="left">
  <a href="https://github.com/polla-fattah/data2thesis_python"><img src="https://img.shields.io/badge/Open_Source-Project-181717?style=for-the-badge&logo=github&logoColor=white" alt="Open Source Project"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg?style=for-the-badge" alt="License: Apache 2.0"></a>
  <a href="https://github.com/polla-fattah/data2thesis_python"><img src="https://img.shields.io/badge/Amendments-Welcomed-2ea44f?style=for-the-badge&logo=github&logoColor=white" alt="Amendments Welcomed"></a>
</p>

A practical guide to analysing research data with Python, for researchers with no programming or statistics background. The book follows Elaf, a Master's student, through her thesis on graduate student wellbeing, introducing each method as the answer to one of her research questions.

**Read it online:** https://polla-fattah.github.io/data2thesis_python

## Repository layout

```text
data2thesis/
├── content/book/        chapter and appendix manuscript (.qmd)
├── content/playground/  practical chapter exercises and datasets
├── content/slides/      lecture decks for each chapter
├── styles/              custom styling (SCSS)
├── downloads/           case study datasets and data2thesis package
├── _freeze/             cached computational results for fast rendering
├── index.qmd            landing page
├── _quarto.yml          unified Quarto website configuration
└── build.ps1            unified build and serve script
```

| Folder / File | Contents |
|---|---|
| `content/book/` | The book chapters and appendices (`.qmd`) |
| `content/playground/` | Practical interactive exercises and datasets (`.qmd`, `.zip`, `.csv`) |
| `content/slides/` | Lecture presentation decks (`.md`, `.qmd`) |
| `styles/` | Custom SCSS styling (light and dark mode) |
| `downloads/` | Built case-study data files and `data2thesis` package |
| `_freeze/` | Cached execution results so rebuilding requires no R run |
| `index.qmd` | The landing page of the website |
| `_quarto.yml` | Unified Quarto configuration |
| `build.ps1` | The PowerShell build and preview script |
| `data/` | Case study raw datasets and specification |
| `data-raw/` | Scripts that generate data and build the packages/zips |
| `data2thesis/` | Source of the `data2thesis` Python package |

## Building and running the site locally

Requires [Quarto](https://quarto.org) and Python. On Windows, the script `build.ps1` in the project root does everything. Open a PowerShell terminal in the project folder and run:

```powershell
.\build.ps1
```

It renders the entire website (landing page, book, playground, and slides) in a single unified pass, and serves the result at <http://localhost:4300>. Leave the terminal open while you browse; press Ctrl+C to stop the server. If Windows refuses to run the script, use `powershell -ExecutionPolicy Bypass -File .\build.ps1`.

| Command | What it does |
|---|---|
| `.\build.ps1` | Build the entire site (book, playground, slides) and serve |
| `.\build.ps1 -NoBuild` | Serve what is already built |
| `.\build.ps1 -NoServe` | Build only |
| `.\build.ps1 -Package` | Synchronize and build the `data2thesis` Python wheel |
| `.\build.ps1 -Chapter 07-hypothesis-testing.qmd` | Render one book chapter only, then serve |
| `.\build.ps1 -Playground` | Also rebuild the playground download zips (after changing `playground-src/`) |
| `.\build.ps1 -Port 4400` | Serve on another port |

Chapters whose code has not changed are not re-executed: their results are stored in `_freeze/`, so a full build takes seconds. Commit `_freeze/` after changing code, so the site can be published by GitHub Actions (`.github/workflows/publish.yml`).

## Outline

*Every chapter ends with a chapter review: a short summary and a list of key terms, which are collected in the glossary (Appendix B).*

## **Part 1: Foundations of Python Programming and Data Handling**

### **Chapter 1: Getting Started with Python**

- Why researchers use Python; installing Python and VS Code (Positron and Jupyter as alternatives).
- A tour of VS Code: Editor, Interactive Window / Terminal, Extensions, and File Explorer.
- Python as a calculator, variables and assignment, and the basic types of data (`int`, `float`, `str`, `bool`), including missing values (`None`, `NaN`).
- Functions, methods, arguments, docstrings, and getting help.
- Writing scripts (`.py`); organizing work with project folders and virtual environments.
- Installing packages with `pip` and importing them, including the `data2thesis` companion package.
- A first look at Elaf's data with Pandas.

### **Chapter 2: Data Structures in Python**

- Pandas Series: working with 1D vectors, vectorization, boolean indexing, and updating values.
- Categoricals for discrete groups, with ordered levels (`pd.Categorical`).
- DataFrames: structure, selecting rows and columns with `.loc` and `.iloc`, and adding columns.
- Matrices and Dictionaries, met as results (correlation matrices, statistical test objects).
- Importing CSV (`read_csv`), Excel (`read_excel`), and SPSS (`read_spss` / `pyreadstat`) files, keeping question and value labels; exporting data with `.to_csv()`.
- Coming from SPSS or Excel: how familiar tasks map to Python and Pandas.
- Reading common error tracebacks (`NameError`, `KeyError`, `TypeError`); rapid descriptive summaries (`.describe()`).

### **Chapter 3: Data Manipulation and Cleaning with Pandas**

- Tidy data principles in Python and method chaining with Pandas.
- Core Pandas methods: `.query()`, `[]` filtering, `.filter()`, `.sort_values()`, `.assign()`, `.replace()`, and `.groupby()` with `.agg()`.
- Reshaping tables with `.melt()` (long) and `.pivot()` / `.pivot_table()` (wide).
- Joining tables with `pd.merge()` (`how="left"`, `how="inner"`, `how="outer"`).
- Case study: cleaning Elaf's survey export (`wellbeing_raw.xlsx`: removing test and duplicate rows, standardizing names, recoding categories, handling missing codes, converting text to numbers, fixing impossible values), computing scale scores with reverse-coded items, and reshaping semester records; verified against canonical data.


### **Chapter 4: Data Visualization with Seaborn and Matplotlib**

- Visual perception and graphical hierarchy (Cleveland & McGill): why position and length outperform angle and area.
- Visualizing distributions and categories with Seaborn: `sns.histplot()`, `sns.countplot()`, and `sns.boxplot()`.
- Bivariate relationships: scatter plots, opacity (`alpha`), and regression trend lines with `sns.regplot()`.
- Longitudinal change over time: `sns.lineplot()` with marker aesthetics and custom palettes.
- Data mapping (`hue`) versus fixed styling (`color`).
- Explanatory graphics: custom labels, theoretical limits, zero baselines, annotations with `ax.axvline()` and `ax.text()`.
- Small multiples (`sns.FacetGrid`, `sns.lmplot`), kernel density estimation (`sns.kdeplot`), and correlation matrices with `sns.heatmap()`.
- Exporting publication-ready raster (PNG at 300 DPI) and vector (PDF, SVG) graphics with `plt.savefig(bbox_inches="tight")`.

## **Part 2: Statistical Analysis for Research**

### **Chapter 5: From Research Question to Data**

- Why research questions come first, and what makes a question answerable with data.
- From a research question to a testable, falsifiable hypothesis, and to the null hypothesis a test will check.
- Variables, constructs, and levels of measurement, shown in Elaf's data.
- Reliability and validity: does a measure measure consistently, and does it measure the right thing?
- Study designs: descriptive, correlational, experimental, and longitudinal, and what each can claim.
- Populations, samples, and sampling, with a simulation.
- Planning the analysis in advance: sample size, power, and preregistration.

### **Chapter 6: Descriptive Statistics and Exploratory Data Analysis (EDA)**

- Exploratory, inferential, and predictive analysis, and the analysis workflow.
- Centre (mean, median, mode) and spread (SD, variance, IQR), and when to report which.
- Shape: skewness, modality, the normal distribution and the 68-95-99.7 rule, z-scores, and Q-Q plots.
- Unusual values: the box plot and z-score rules, and what (not) to do with outliers.
- Missing data: how much, and why (missing completely at random, at random, not at random); attrition in Elaf's study.
- Correlation, scatter plot matrices, and why correlation is not causation.
- Describing the sample in a thesis.

### **Chapter 7: Hypothesis Testing and Statistical Inference**

- Populations and samples; sampling distributions by simulation, the standard error, and the central limit theorem.
- Confidence intervals, including bootstrap confidence intervals.
- The logic of hypothesis testing: null and alternative hypotheses, p-values, Type I and II errors, one- and two-tailed tests, statistical versus practical significance.
- One-sample, two-sample (Welch), and paired t-tests, with Cohen's *d*.
- Checking assumptions (and the trap of normality tests in large samples).
- Chi-square tests of goodness of fit and independence.
- Non-parametric tests: Mann-Whitney U and Wilcoxon signed-rank.
- Choosing the right test, and reporting results in a thesis.

### **Chapter 8: ANOVA and Regression**

- One-way ANOVA, eta squared, Tukey post-hoc tests, Levene's test, and Kruskal-Wallis.
- Two-way ANOVA: main effects, interactions, and interaction plots.
- Simple and multiple linear regression; reading `summary()`; R-squared; categorical predictors.
- Separating an effect from a confounder (caffeine and sleep); curved relationships; interactions with centred predictors.
- Diagnostic plots, and tidy reporting with broom.
- Logistic regression: odds, odds ratios, and predicted probabilities for considering dropout.

### **Chapter 9: Multivariate Statistical Methods**

- Exploring many correlations at once (sorted correlation plots).
- Principal component analysis: components, eigenvalues, scree plots, the Kaiser rule, and parallel analysis.
- PCA versus factor analysis; exploratory factor analysis of Elaf's questionnaire (loadings, oblique rotation, a reversed item, a cross-loading).
- Reliability with Cronbach's alpha.
- Cluster analysis: scaling, k-means, choosing the number of clusters (elbow, silhouette), describing clusters, and hierarchical clustering with dendrograms.

### **Chapter 10: Mixed-Effects Models**

- Repeated measures and nested data, and why ordinary regression gets the uncertainty wrong (in either direction).
- Random intercepts and random slopes with `lme4`, starting from the real `sleepstudy` data; the intraclass correlation (ICC).
- Confidence intervals, likelihood ratio tests, and p-values with `lmerTest`.
- Change over time in Elaf's study: the decline in wellbeing, the fading workshop effect, and stable GPA (and what a singular fit means).
- Students within supervisors: variance at each level.
- Generalised linear mixed models for counts (supervisor meetings) and binary outcomes.
- Reporting a mixed-effects model.

## **Part 3: Machine Learning with Python**

### **Chapter 11: Introduction to Machine Learning in Python**

- Supervised and unsupervised learning; prediction versus explanation.
- The tidymodels framework: splitting (rsample), recipes, model specifications (parsnip), workflows, tuning, and yardstick.
- Predicting which students will consider dropout: a stratified split, a recipe (imputation, dummy variables, normalisation), and data leakage.
- Evaluating a classifier: why accuracy misleads for imbalanced outcomes, and the ROC AUC.
- Overfitting, cross-validation, hyperparameter tuning (tree depth), and the final test with `last_fit()`.
- Fairness and responsible use of predictions about people.

### **Chapter 12: Classification Models**

- Decision trees (how splits are chosen, reading a tree) and random forests (bootstrap samples, `mtry`, permutation importance).
- k-nearest neighbours (distances, why normalisation matters, tuning k) and support vector machines (margins, linear and RBF kernels).
- Comparing models fairly with workflow sets: on Elaf's data, logistic regression predicts as well as any flexible model.
- The confusion matrix: sensitivity (recall), specificity, precision, and the F1 score.
- Choosing the classification threshold with the ROC curve and cross-validated predictions, and reporting it.
- Imbalanced outcomes: upsampling, downsampling, SMOTE, and class weights with themis, and what they do (and do not) change.

### **Chapter 13: Predictive Regression**

- Predicting Elaf's final GPA from year-one information: wide-format predictors with `pivot_wider()`, and the limits of a model trained only on students who stayed.
- Measuring numeric predictions: MAE, RMSE, and R², always against a baseline that predicts the mean.
- Why ordinary regression overfits with many correlated predictors (a 60-student experiment).
- Regularised regression with glmnet: ridge, lasso, and elastic net; tuning the penalty; coefficient paths; why selected predictors are not causes.
- Boosting: building a model from many small trees, and tuning XGBoost.
- Comparing models with cross-validation, the final test, and what year-one GPA alone achieves.

### **Chapter 14: Advanced Clustering**

- What k-means assumes: hard assignments, round clusters of similar size, and no room for outliers.
- Gaussian mixture models with mclust: membership probabilities, covariance structures, and choosing the number of clusters with BIC; three student profiles and the students who fit none clearly.
- DBSCAN: clusters as dense regions, core points and noise, and choosing `eps` with the k-nearest-neighbour distance plot; finding students who fit no profile.
- Evaluating a clustering: silhouette, BIC, agreement between methods (adjusted Rand index), stability, and relevance to outcomes such as considering dropout.
- Reporting clustering choices in a thesis.

### **Chapter 15: Neural Networks**

- How a neural network works: neurons, layers, weights, and activation functions.
- Fitting and tuning a neural network with tidymodels (`mlp()` with the `nnet` engine) on the dropout question.
- Comparing it fairly with the models of Chapters 11 and 12.
- Deep learning: what it is, when it helps, and where to go next (`keras3`, `torch`).

### **Chapter 16: Time Series Forecasting**

- Time series data in R with `tsibble`, and time plots.
- Trend and seasonality: decomposition and seasonal plots with `feasts`.
- Simple benchmark forecasts, exponential smoothing (ETS), and ARIMA with `fable`.
- Judging forecasts: training and test periods, accuracy measures, and prediction intervals.
- Case study: forecasting next year's weekly visits to the university counselling service.

## **Part 4: Reproducible Research and Applications**

### **Chapter 17: Reproducible Research**

- What reproducible research is, and why copying results by hand goes wrong.
- Quarto documents: YAML header, Markdown text, code chunks, inline code, chunk options, numbered tables and figures, citations from a BibTeX file, and LaTeX equations; rendering to HTML, Word, and PDF; parameterised reports. A note on R Markdown for older projects.
- Keeping package versions with renv, and reporting and citing software.
- Shiny: inputs, outputs, and reactivity, with a complete wellbeing dashboard.
- Open science: sharing data and code with a DOI and a licence, protecting participants (small cells), preregistration and registered reports.
- Optional: keeping a project's history with git and GitHub.

### **Chapter 18: Using AI with Python**

- How large language models work, and why they make confident mistakes (hallucinations, outdated knowledge).
- Using AI assistants to write, explain, and debug R code, and checking what they produce; AI inside RStudio and Positron.
- Coding Elaf's open-ended answers: a keyword dictionary as a baseline, then a language model called from R with `ellmer` (system prompt with a codebook, structured output, `parallel_chat_structured()`).
- Validating AI coding against human coding: accuracy, confusion matrix, Cohen's kappa, reading disagreements, and consistency between runs.
- Responsible use: checking, data privacy and local models, reproducibility (models, prompts, saved outputs), disclosure, and bias.

### **Chapter 19: Putting It All Together**

- The path of a research project, and how to organise one: read-only raw data, numbered scripts, relative paths, a README, and a Quarto results document.
- Elaf's complete pipeline, from the raw survey export to clean data (checked against the package), a sample table, and three research questions answered with the methods of the book.
- Reporting: helper functions for means, percentages, and p-values; broom for model tables; reporting sentences with inline numbers; combined figures with patchwork.
- Choosing a method: a decision guide and a map of Elaf's research questions to the chapters.
- Challenges every researcher meets, and where to go next (further methods, free books, and the R community).

### **Appendices:**

- **Appendix A:** Installation and Setup: R on Windows, macOS, and Linux; RStudio (and Positron); recommended settings; the book's packages and the data2thesis package; common problems and keeping R up to date.
- **Appendix B:** Glossary: every key term from the chapter reviews with a plain-language definition and chapter references, and a table of frequently used R functions.
- **Appendix C:** Python Packages: every package used in the book, what it is for, the chapters that use it, and its version; finding, judging, and citing packages.
- **Appendix D:** Common Errors and How to Fix Them: real messages (errors, warnings, and silent mistakes) from starting out, files, data, plots, tests and models, and machine learning, with what each means and how to fix it; what to do when stuck.
- **Appendix E:** Further Learning Resources: free books by topic (including Tyson Barrett's *R for Researchers*), courses and practice, and communities.
