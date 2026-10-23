# Revision Plan: From Data to Thesis

Working plan for revising *FROM DATA TO THESIS: Using R for Non-Technical* (the repository and website address remain `R4NTR`). The chapter outline lives in [README.md](README.md); this file holds the instructions that apply across the book, the known defects, and the order of work.

Most chapters are first drafts from 2025, and many sections were generated with AI tools. Treat every chapter as a draft to be restructured, fact-checked, and updated, not as finished text.

---

## 0. Running case study

**Decided:** the book follows one research story: **Elaf's Master's thesis on graduate student wellbeing** (sleep, stress, study habits, supervisor support, GPA, burnout, and whether students consider dropping out). Each method is introduced as the answer to one of the student's research questions.

The story comes from the author's lecture notes *Data Analysis for Research* (2025), which follow a Master's student in Educational Psychology (called Sara in the notes, renamed Elaf for the book):
`UNi/Research/Books/R/Statics/StatisticsPresentation/` (`LectureNotesDataAnalysis.Rmd` and its PDF, the statistics notes `LectureNotes.Rmd`, and the data `graduate_student_wellbeing.csv`).

**"In your field" boxes:** so readers outside education and psychology see their own research in each method, chapters include short boxes showing the same method in another field, e.g. health (patients measured at clinic visits), agriculture (crop trials over seasons), or business (employee satisfaction and turnover). Each box is a few lines of explanation and code on a small dataset.

**Teaching pattern (decided):** Elaf's data is used from Chapter 1. Each new idea, data structure, or code block is first shown on a tiny example (a few values, close to the theme where possible), then applied to Elaf's data, as in the author's lecture notes. Real datasets appear in the "in your field" boxes.

**Dataset:** specified in [data/specification.md](data/specification.md); the author's decisions are in its section 9 (unnamed university, GPA 0-4, randomly invited workshop, counselling visits for time series, 600 students, five faculties, data as both files and an R package).

**Dataset specification:** approved by the author.

**Rewrite, not repair (decided):** each chapter is rewritten around Elaf's study, in the author's voice. The current chapter drafts and both sets of lecture notes are source material: correct explanations and code are reused, everything else is replaced. The defects in section 3 are fixed as part of each rewrite, not in a separate pass over the old text.

**Playground (decided):** an online section of the website, separate from the chapters, with one page per chapter for hands-on practice. Git is never required.
- **Try it in the browser:** exercises run directly on the page with webR (R running inside the browser), so readers need no installation. Best for Chapters 1-9; packages that cannot run in the browser (e.g. `keras`) are practised through the downloadable project instead.
- **Download the chapter project:** a zip file with an RStudio project, Elaf's data, a starter script with the exercises, and a solutions script. Readers either click a download link or type one line in R: `usethis::use_course("<link to the zip>")`, which downloads, unzips, and opens the project in RStudio.
- **Hidden solutions:** each exercise has an answer that expands when clicked, so readers try first and check afterwards.
- **Version control is optional:** git and GitHub are introduced only in Chapter 16 (reproducible research), as an extra for readers who want it.
- **Test first:** build one pilot page (Chapter 1) to confirm webR works on the GitHub Pages site before building the others.

---

## 1. Book structure (19 chapters)

| Part | Ch | Title | File | Status |
|---|---|---|---|---|
| 1 | 1 | Getting Started with R | `book/01-getting-started.qmd` | **Rewritten** (first full draft, 2026-09-24); awaiting the author's review |
| 1 | 2 | Data Structures in R | `book/02-data-structures.qmd` | **Rewritten** (first full draft, 2026-09-24), with playground page; awaiting the author's review |
| 1 | 3 | Data Manipulation | `book/03-data-manipulation.qmd` | **Rewritten** (first full draft, 2026-09-24), with playground page; awaiting the author's review |
| 1 | 4 | Data Visualization | `book/04-data-visualization.qmd` | **Rewritten** (first full draft, 2026-09-24), with playground page; awaiting the author's review |
| 2 | 5 | From Research Question to Data | `book/05-research-question.qmd` | **In progress** (new chapter, 2026-09-25) |
| 2 | 6 | Descriptive Statistics and EDA | `book/06-descriptive-statistics.qmd` | **Rewritten** (first full draft, 2026-09-24), with playground page; awaiting the author's review |
| 2 | 7 | Hypothesis Testing and Statistical Inference | `book/07-hypothesis-testing.qmd` | **Rewritten** (first full draft, 2026-09-24), with playground page; awaiting the author's review |
| 2 | 8 | ANOVA and Regression | `book/08-anova-regression.qmd` | **Rewritten** (first full draft, 2026-09-24), with playground page; awaiting the author's review |
| 2 | 9 | Multivariate Statistical Methods | `book/09-multivariate.qmd` | **Rewritten** (first full draft, 2026-09-24), with playground page; awaiting the author's review |
| 2 | 10 | Mixed-Effects Models | `book/10-mixed-models.qmd` | **Written** (new chapter, first full draft, 2026-09-24), with playground page; awaiting the author's review |
| 3 | 11 | Introduction to Machine Learning in R | `book/11-machine-learning.qmd` | **Rewritten** (first full draft, 2026-09-24), with playground page; awaiting the author's review |
| 3 | 12 | Classification Models | `book/12-classification.qmd` | **Rewritten** (first full draft, 2026-09-24), with playground page; awaiting the author's review |
| 3 | 13 | Predictive Regression | `book/13-predictive-regression.qmd` | **Rewritten** (first full draft, 2026-09-24), with playground page; awaiting the author's review |
| 3 | 14 | Advanced Clustering | `book/14-advanced-clustering.qmd` | **Rewritten** (first full draft, 2026-09-24), with playground page; awaiting the author's review |
| 3 | 15 | Neural Networks | `book/15-neural-networks.qmd` | **Written** (split from the old Ch 14; first full draft, 2026-09-24), with playground page; awaiting the author's review |
| 3 | 16 | Time Series Forecasting | `book/16-time-series.qmd` | **Written** (split from the old Ch 14; first full draft, 2026-09-24), with playground page; awaiting the author's review |
| 4 | 17 | Reproducible Research | `book/17-reproducible-research.qmd` | **Rewritten** (first full draft, 2026-09-24), with playground page and a Quarto project download; awaiting the author's review |
| 4 | 18 | Using AI with R | `book/18-ai.qmd` | **Written** (new chapter, first full draft, 2026-09-24), with playground page; language-model results produced locally with Gemma 4 through Ollama (2026-09-24); awaiting the author's review |
| 4 | 19 | Putting It All Together | `book/19-putting-it-together.qmd` | **Written** (new chapter, first full draft, 2026-09-24), with playground page and a complete project download; awaiting the author's review |
| - | A | Installation and Setup | `book/a-installation.qmd` | **Rewritten** (first full draft, 2026-09-24), without screenshots (steps described in words); awaiting the author's review |
| - | B | Glossary | `book/b-glossary.qmd` | **Written** (first full draft, 2026-09-24): definitions in `book/glossary.txt`, functions in `book/functions.txt`; chapter references are added automatically, and rendering stops if a chapter's key term has no definition; awaiting the author's review |
| - | C | R Packages | `book/c-packages.qmd` | **Written** (first full draft, 2026-09-24): packages in `book/packages.txt`; chapters found automatically and versions read when the book is built; awaiting the author's review |
| - | D | Common Errors | `book/d-common-errors.qmd` | **Written** (first full draft, 2026-09-24): every message is produced live when the book is built; awaiting the author's review |
| - | E | Further Resources | `book/e-resources.qmd` | **Written** (first full draft, 2026-09-24); Arabic resources removed at the author's request; awaiting the author's review |

Chapter order and parts are set in `book/_quarto.yml`. The earlier Jekyll drafts are in `archive/jekyll/_chapters/` and are source material for the rewrites.

---

## 2. Instructions for every chapter

### 2.1 Restructure
- Each chapter follows the same template:
  1. Short introduction: why this matters to a researcher.
  2. Learning objectives (3-5 bullets).
  3. Main sections, numbered `N.1`, `N.2`, … (sub-sections `N.1.1`).
  4. A worked case study or hands-on project.
  5. **Chapter review**: a short summary and a list of **key terms** (key terms are also added to the glossary in Appendix B).
  6. Exercises: a few short ones in the chapter, with longer practice on the chapter's playground page.
  7. References / further reading.
- Remove repetition between chapters (see section 4); teach each idea once and refer back to it.
- Keep chapters a manageable length; split material that has grown beyond the chapter's topic.

### 2.2 Check the information
- Many passages were auto-generated. Check every factual claim, statistical explanation, function name, argument, and printed result.
- Run every code block in a clean R session and confirm that the output shown matches.
- Replace the auto-generated reference lists (541 entries, all "accessed on July 30, 2025") with sources suitable for an academic book: textbooks, peer-reviewed papers, official package documentation, and CRAN vignettes. Avoid GeeksforGeeks, Medium, Reddit, Stack Overflow, and similar sites as citations.
- Remove the stray citation numbers attached to words (e.g. "graphics.1 As…"); use a consistent citation style instead.

### 2.3 Update the information
- Bring content up to date with current R (4.5+) and current package versions.
- Prefer current tools and idioms:
  - Native pipe `|>` instead of `%>%` (mention `%>%` once, for reading older code).
  - `pivot_longer()` / `pivot_wider()`, not `gather()` / `spread()`.
  - dplyr 1.1+ features: `.by =`, `join_by()`.
  - **tidymodels** throughout Part 3, not caret (caret is in maintenance mode).
  - `bake(new_data = NULL)` instead of `juice()`.
  - `keras3` instead of `keras`; check installation steps.
  - Replace or reduce Prophet (no longer actively developed); consider `fable` / `forecast`.
  - Check all ggplot2 code against ggplot2 4.x.
  - Quarto alongside, or instead of, R Markdown in Chapter 16.
  - Mention Positron as an alternative editor to RStudio.

### 2.4 Diagrams and figures
- Convert any ASCII diagrams to **Mermaid** (built into Quarto: use a ```` ```{mermaid} ```` block).
- The book currently has no diagrams or figures. Add diagrams where they explain a process, for example:
  - The data analysis workflow (Ch 5).
  - Choosing the right statistical test (Ch 6).
  - The machine learning pipeline: split → recipe → fit → tune → evaluate (Ch 10).
  - Cross-validation folds (Ch 10).
  - The `.Rmd` / Quarto rendering pipeline and Shiny reactivity (Ch 16).
- Add plot images to the visualization and analysis chapters, so readers can see what the code produces. Every image needs alt text.

### 2.5 Code standards
- Code that should run is written as Quarto code chunks (```` ```{r} ````), so outputs and plots are produced by the code itself. Code that is only shown uses ```` ```r ````. Never paste output by hand.
- No Markdown escape characters inside code (`\<-`, `\=`, `\_`, `\#`).
- Load packages at the start of each chapter in one setup block; list installation commands in Appendix A rather than scattered through the text.
- Use `set.seed()` before every random step (sampling, splitting, resampling, clustering, model fitting).
- Use RStudio Projects and `here::here()` for file paths; never assume a working directory.

### 2.6 Datasets
- Use Elaf's dataset ([data/specification.md](data/specification.md)) for the case study in every chapter, from Chapter 1.
- Tiny examples before each tool use a few typed-in values, close to the theme where possible.
- "In your field" boxes and small real examples (e.g. `lme4::sleepstudy`) use datasets that ship with R or install as packages, so readers need no downloads or accounts.
- Remove the Kaggle datasets that need a login (Titanic, WHO life expectancy, retail sales) and the `Boston` housing dataset (it contains a race-based variable and has been dropped by many textbooks).

### 2.7 Style
- One consistent voice across the book, written for non-technical researchers: plain language, explain terms when first used.
- Headings without bold markup (`## N.1 Title`, not `## **Title**`).
- Consistent section and table numbering (`Table N.1`, in order of appearance).
- Remove leftover reviewer notes in HTML comments (`<!-- … -->`) after acting on them.

---

## 3. Known defects

These are fixed as part of each chapter's rewrite (section 0). They are listed so nothing is carried over into the new text.

### Critical
- [ ] **Chapters 4-15: code is not formatted as code.** About 180 code blocks are plain paragraphs under a lone `R` line, with escaped characters and output pasted as text. Inline code formatting was lost, leaving broken sentences (e.g. Ch 5: "mean() function performs this calculation.").
- [x] **Chapter 4 contains the chapter twice.** (Resolved by the rewrite.) Lines 10-202 are an older, garbled copy (R comments render as headings); the real chapter starts at line 208 after a dashed separator.

### Chapter-specific
- [x] Ch 2 (fixed in the rewrite): import/export comes before vectors; move it after data frames. Remove duplicated "Exporting Data" and "Aggregating Data" sections. Reduce the "Basic Exploratory Analysis" and missing-data sections, which overlap Chapters 3 and 5.
- [x] Ch 2-3: act on, then delete, 9 reviewer notes in HTML comments. (Ch 2 rewritten without them; its notes were covered: e.g. simpler matrices, one summary section.)
- [ ] Ch 1-3: 255 code fences have no language label.
- [x] Ch 8: first section numbered "1." instead of "8.1". (Resolved by the rewrite; Quarto numbers sections automatically.)
- [ ] Ch 11: Table 11.2 appears before Table 11.1.
- [x] Ch 12: add a plain linear model as a baseline in the life expectancy project. (Done in the rewrite: the chapter now uses Elaf's final GPA, with a mean baseline and a plain linear model; the concrete data replaces life expectancy in the "In your field" box.)
- [x] Ch 14: section 14.1 (ensembles) repeats bagging (Ch 11.2) and boosting (Ch 12). Remove or reduce it, then retitle the chapter (e.g. "Neural Networks and Time Series Forecasting"), or split it into two chapters. (The author chose to split: Ch 14 Neural Networks, Ch 15 Time Series Forecasting; the ensembles section is dropped.)
- [x] Ch 16 (formerly 15): no chapter summary. (Resolved by the rewrite.)
- [x] Unused Jekyll stub `005-chapter00.md` ("Tempo") left behind in `archive/jekyll/`; not part of the Quarto book.
- [ ] Part index pages have no titles, and Parts 2-4 are `published: false`; check whether this is intended.

---

## 4. Repetition to resolve

| Topic | Appears in | Keep in |
|---|---|---|
| Exploratory analysis | Ch 2, Ch 5 | Ch 5 |
| Missing data | Ch 2, Ch 3, Ch 5 | Recognising `NA` in Ch 2; handling in Ch 3/5 |
| Clustering basics | Ch 8, Ch 13 | Basics in Ch 8, advanced methods in Ch 13 (as planned) |
| Ensembles (bagging, boosting) | Ch 11, Ch 12, old Ch 14 | Ch 11 (random forests), Ch 12 (boosting) |
| Classification metrics | Ch 7, Ch 11 | Ch 11; brief mention in Ch 7 |

---

## 5. Content to add

Already in the README outline:
- **Ch 1:** RStudio Projects and file paths (`here`).
- **Ch 2:** importing Excel (`readxl`) and SPSS (`haven`) with labels; a "coming from SPSS or Excel" guide.
- **Ch 6:** sampling distributions by simulation and bootstrap confidence intervals, before the tests.
- **Ch 9:** Mixed-Effects Models (new chapter).
- **Ch 17:** Using AI with R (new chapter).
- **Every chapter:** chapter review with summary and key terms.
- **Appendix E:** further learning resources (Arabic-language resources were planned, then removed at the author's request on 2026-09-24). Include Tyson Barrett's free book *R for Researchers: An Introduction* (2019, https://tysonbarrett.com/Rstats/) as a shorter companion for the same audience.

Proposed, not yet in the outline:
- Ch 1: Positron; the native pipe.
- Ch 2 or 3: writing your own functions (not taught anywhere).
- Ch 3: duckdb / arrow for data too large for memory.
- Ch 4: combining plots with `patchwork`.
- Ch 5: publication "Table 1" with `gtsummary`.
- Ch 6: effect sizes, power analysis and sample size (`pwr`), multiple-testing corrections.
- Ch 7: model tables (`gtsummary`, `broom`) and `marginaleffects`.
- Ch 16: Quarto, `targets`, open-science practices (data and code sharing, preregistration, ethics).
- Optional chapters depending on readers: text analysis (`tidytext`), survival analysis, Bayesian statistics (`brms`), meta-analysis (`metafor`), spatial data (`sf`).

---

## 6. Order of work

1. [x] **Write the dataset specification** ([data/specification.md](data/specification.md)). Approved.
2. [x] **Generate the dataset**: `data-raw/generate_wellbeing.R` produces all files (version 1.0.0); `data-raw/check_wellbeing.R` confirms all 72 designed effects. **Follow-up (done 2026-09-24):** the open-ended answers were rewritten from a much larger phrase bank (`data-raw/answer_bank.R`) as version 1.1.0; every other value is identical to 1.0.0, and all 72 checks still pass.
3. [x] **Build the data package**: `data2thesis/` (version 1.0.0) passes `R CMD check` with no warnings or notes. `data-raw/build_package.R` copies the data into it; the built file `data/data2thesis_1.0.0.tar.gz` lets readers install from the website. Package name `data2thesis` chosen so a future Python book could share it.
4. [x] **Build the playground pilot**: `playground/chapter01.md` (7 browser exercises with hidden solutions) and `playground/chapter01.zip` (RStudio project), built by `data-raw/build_playground.R` from `playground-src/`. Tested on a local Jekyll server without cross-origin headers (the GitHub Pages situation): R starts, all exercises run, plots draw, errors display. **Still to confirm:** the same on the live GitHub Pages site after pushing.
4b. [x] **Quarto prototype** (`quarto/`): a Quarto website (`quarto/site/`: landing page, playground with quarto-live) and a Quarto book (`quarto/book/`: welcome page and a sample chapter) rendered together into `quarto/_site/`. Build: render `site` first, then `book`. Verified: landing page sections and links, the sample chapter (code runs, figure numbering and cross-reference, Mermaid diagram, citation and reference list, callouts, numbers in the text taken from the code). **Still to verify:** the quarto-live exercises in a visible browser (they do not start in a hidden browser pane).
4c. [ ] **Move the book to Quarto**. Done: the Jekyll site is archived in `archive/jekyll/`; the website is in `site/` and the book in `book/` (17 chapter and 5 appendix placeholders, each with Elaf's question and an outline; Chapter 6 starts with the written *Comparing two groups* section); the pre-render script is TypeScript (`site/copy_resources.ts`) and code results are frozen, so `.github/workflows/publish.yml` publishes without R (checked: a whole-project build runs no R code). **Checked 2026-09-24:** layout has no horizontal overflow at desktop or phone width; quarto-live exercises run in a visible browser (Chapters 3, 9, and 14: dplyr, lme4, and nnet, with results matching the book). **Still to do:** push, then switch GitHub Pages to "GitHub Actions" (Settings > Pages) and check the live site.
5. [x] **Rewrite each chapter** around Elaf's study (section 0), using the template in 2.1 and following sections 2.2-2.7: tiny example first, then Elaf's data; fact-checked content and proper references; figures, diagrams, "in your field" boxes, exercises, and chapter reviews. Each chapter also gets its playground page. (First drafts of all 18 chapters and their playground pages done 2026-09-24; awaiting the author's review.)
6. [x] **Write the new chapters** (9, 17, 18) and appendices B-E. (Done 2026-09-24; Chapter 17's language-model results produced with a local model on 2026-09-24.)
7. [ ] **Unify style** across the whole book. First pass done 2026-09-24: every chapter follows the template (objectives, In your field box, review, key terms, exercises, playground link, further reading); spelling is consistently British except titles of cited works and the Ch 4 title "Data Visualization"; callout types unified (tip = practical advice and write-ups, important = rules, warning = pitfalls); all cross-chapter references checked after the renumbering. A fresh render of every chapter (2026-09-24, R 4.4.3, ggplot2 4.0.3) changed no number in the text; figures in Chapters 4-8 were redrawn by the newer ggplot2.
8. [ ] **Publish**: set `published: true` chapter by chapter as each one is finished.

---

## 7. Decisions log

- **Chapter titles** (short form where it fits): Ch 1 "Getting Started with R", Ch 7 "ANOVA and Regression", Ch 12 "Predictive Regression", Ch 13 "Advanced Clustering". Abstracts rewritten to match content.
- **Mixed-Effects Models** placed as Ch 9, at the end of Part 2 (after Multivariate Methods), so Chapters 1-8 keep their numbers.
- **Using AI with R** placed as Ch 16 (Ch 17 since the split of Chapter 14), before the final chapter, because its section on disclosing AI use builds on Reproducible Research.
- **Notice that the data is fictional** (2026-09-25, the author's request): a clear statement that Elaf, her study, and her data are fictional, generated by a program with patterns built in by the author, describe no real people, and must not be cited or used as findings about real students. It appears in full in a callout where the data is first loaded in Chapter 1, in the book's preface, and in the landing-page FAQ; and in a short form in the landing page's "Get the data" section, the data2thesis package description and help, and every playground project README.
- **Chapter 17 uses a local model** (2026-09-24, the author's choice, replacing the earlier plan of an online model with an API key): the language-model results come from Google's Gemma 4 (`gemma4:e4b`), run locally through Ollama on the author's laptop (RTX 4060 GPU), with no key and no cost, so the answers never leave the computer. The model does not reliably follow ellmer's structured-output format, so the script asks for the theme name as text and checks each reply against the list of themes. The chapter, its download project, and `data-raw/run_ai_coding.R` describe both options (local and online).
- **Specification updated to match the data** (2026-09-24, the author's choice): Chapter 12's trees do not beat a straight line for final GPA, and Chapter 13 finds three profiles rather than four; the specification now says so, and the chapters are unchanged. **Arabic resources** removed from Appendix E at the author's request.
- **Chapter 17 data and AI results** (2026-09-24, the author's choices): the open-ended answers are regenerated with much more varied text as dataset version 1.1.0, keeping every other value identical (same random draws, themes, and coded subset); the chapter's language-model results come from a script that the author runs once with his own API key through `ellmer`, and the results are saved to a file that the chapter reads, so the book renders without a key; `ellmer` installed with the author's permission.
- **Chapter 16 content** (2026-09-24, the author's choices): Quarto is taught first, with a short box on R Markdown for older projects; the chapter includes renv, git and GitHub as an optional section, and open science practices (sharing data and code, preregistration, ethics and anonymisation, citing software); `targets` is left out; Shiny is covered with a small, complete wellbeing dashboard.
- **Chapter 14 split** (2026-09-24, the author's choice): the old "Advanced Machine Learning Techniques" became Ch 14 *Neural Networks* and Ch 15 *Time Series Forecasting*; its ensembles section was dropped (covered in Ch 11 and 12). Chapters 15-17 became 16-18, and files, section labels, cross-references, the landing page, README, and the dataset specification were updated in one pass.
- **Renumbering** of files, slugs, section numbers, table numbers, and cross-references was done in one pass (chapters 9+ were unpublished, so no live links broke).
- **Outside material** (the "Internet Links" bookmarks folder, EPIB607 course notes, YouTube channels) is used as suggestions, not as instructions.
- **Running case study:** graduate student wellbeing (from the author's lecture notes), with "in your field" boxes for other fields. Alternatives considered: a diabetes clinic programme, a school reading programme, a wheat farming trial, employee wellbeing, and air quality and hospital visits. The student wellbeing study was chosen because nearly every reader is or was a graduate student, and the author's notes already exist.
- **Student's name:** Elaf, chosen by a coin toss between Sidra and Elaf (the author's daughters' names). The 2025 lecture notes called her Sara.
- **Dataset specification approved** ([data/specification.md](data/specification.md)), including the author's decisions in its section 9.
- **Rewrite rather than repair:** chapters are rewritten around Elaf's study; existing drafts and lecture notes are source material.
- **Time series:** counselling-service visits, kept after considering alternatives (survey answer timestamps, supervisor meetings, Elaf's research diary, daily check-ins, university withdrawal records). Story: the counselling doctors ask Elaf for an internal analysis, separate from her thesis.
- **Book title:** *From Data to Thesis: Research Data Analysis with R* (replacing *R for Non-Technical Researchers*). Chosen because it describes the reader's goal rather than what they lack, matches the thesis case study, and does not clash with existing books. "R for Researchers" was ruled out: Tyson Barrett's *R for Researchers: An Introduction* (2019) already uses it for a similar audience. That book is shorter (about 28,000 words), not updated since 2019, and has no running case study, machine learning part, or AI chapter, so this book remains worth writing.
- **Future, not in the current plan:** a sibling book, *From Data to Thesis: Research Data Analysis with Python*, may follow later.
- **Package name:** `data2thesis` (replacing the working name `r4ntrdata`), valid for both R and Python packages so a future Python book could share it. Its helper function is `data2thesis_example()`.
- **Playground:** an online practice section with browser exercises (webR), downloadable chapter projects (`usethis::use_course()`), and hidden solutions; no git required. Replaces the idea of borrowing the downloadable "Apply It" projects from Barrett's book.
- **Packages for Part 3** (installed 2026-09-24 with the author's permission): tidymodels, kknn, ranger, kernlab, themis, glmnet, xgboost, mclust, dbscan, and lmerTest. `vip` is no longer available on CRAN for R 4.4, so variable importance is plotted with the model's own output and ggplot2. Chapters 14 and 15: the author chose `nnet` through tidymodels (`mlp()`) for neural networks, with deep learning (`keras3`, `torch`) described but not installed, and `fable`, `tsibble`, and `feasts` for forecasting (installed 2026-09-24 with the author's permission; `feasts` and `ggtime` as Windows binaries, because the newest `ggtime` needs compilation, plus `urca`, which `ARIMA()` needs for its unit-root tests).
- **Follow-up:** the cover images (`assets/img/front-cover.png`, `back-cover.png`) still show the old title; to be redone later.
- **Publishing system: Quarto** (replacing Jekyll and the jekyll-chapterbook theme). Code runs when the book is built, so outputs and plots always match the code; built-in Mermaid, callouts, cross-references, citations, search, dark mode, and PDF/EPUB output; the quarto-live extension provides the playground exercises; the same tools suit the future Python book. A Quarto website holds the landing page and playground, with the Quarto book at `/book/`.
- **New Chapter 5, From Research Question to Data** (2026-09-25, the author's choice): a new chapter at the start of Part 2 on research questions, hypotheses and falsifiability, variables and measurement, reliability and validity, designs, sampling, and planning. Chapters 5-18 became 6-19; files, section labels, cross-references, playground pages and downloads, the landing page, README, and the dataset specification were updated in one pass. The second revision plan is in [revision-plan-2.md](revision-plan-2.md).
- **Visual style** (2026-09-25, the author's request): the site and book take their look from the author's front-end book (`WebApp/new-lectures`): a pale blue-grey canvas (deep navy in dark mode), navy links, copper as a second accent, Inter for text, Chakra Petch for display titles, and IBM Plex Mono for code and small labels (from Google Fonts). Code sits in a white card; results sit below it in a quieter tinted box with a copper edge and an "Output" label; inline code is crimson on a light chip. The landing page has the same faint grid, hero, and card styles. Colours are in `site/styles/light.scss` and `dark.scss`; the shared rules are in `site/styles/theme.scss`.
