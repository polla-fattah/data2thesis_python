# ------------------------------------------------------------------------------
# generate_wellbeing.R
#
# Generates the simulated Graduate Wellbeing Study used as the running case
# study in "FROM DATA TO THESIS: Using R for Non-Technical". Every file in data/ is created
# by this script from a fixed seed, so anyone can regenerate identical data.
#
# Specification: data/specification.md
# Check script:  data-raw/check_wellbeing.R
#
# Run from the project root:
#   Rscript data-raw/generate_wellbeing.R
# ------------------------------------------------------------------------------

suppressPackageStartupMessages({
  library(haven)    # SPSS file
  library(writexl)  # Excel file
})

dataset_version <- "1.1.0"
set.seed(20260924)

out_dir <- "data"
dir.create(out_dir, showWarnings = FALSE)
dir.create("data-raw", showWarnings = FALSE)

n_students    <- 600
n_supervisors <- 120

faculties       <- c("Education", "Health Sciences", "Humanities",
                     "Natural Sciences", "Social Sciences")
faculty_weights <- c(0.24, 0.22, 0.16, 0.18, 0.20)
emp_levels      <- c("None", "Part-time job", "Full-time job")
profiles        <- c("Balanced", "Overloaded", "Isolated", "Disengaged")

# Helpers ----------------------------------------------------------------------

clamp  <- function(x, lo, hi) pmin(pmax(x, lo), hi)
zscore <- function(x) as.numeric(scale(x))
fmt_id <- function(prefix, i, width) sprintf(paste0("%s%0", width, "d"), prefix, i)
yes_no <- function(x) ifelse(x, "Yes", "No")

# Turn a standard-normal score into a 1-5 answer
likert <- function(z, shift = 0) {
  findInterval(z + shift, c(-1.6, -0.6, 0.4, 1.4)) + 1L
}

# Build one questionnaire item from a latent trait
make_item <- function(latent, loading, shift = 0, reverse = FALSE) {
  z <- loading * latent + sqrt(1 - loading^2) * rnorm(length(latent))
  if (reverse) z <- -z
  likert(z, shift)
}

# 1. Supervisors ---------------------------------------------------------------

supervisors <- data.frame(
  supervisor_id = fmt_id("SUP", seq_len(n_supervisors), 3),
  faculty = sample(rep(faculties, times = round(faculty_weights * n_supervisors))),
  rank = sample(c("Lecturer", "Assistant Professor", "Professor"),
                n_supervisors, replace = TRUE, prob = c(0.35, 0.40, 0.25))
)

# Supervisor effects: some supervisors are more supportive, some students'
# wellbeing is higher simply because of who supervises them.
sup_eff_support   <- rnorm(n_supervisors, 0, 0.45)
sup_eff_wellbeing <- rnorm(n_supervisors, 0, 3)
sup_eff_meetings  <- rnorm(n_supervisors, 0, 0.25)
sup_popularity    <- rgamma(n_supervisors, shape = 3)

# 2. Students: background ------------------------------------------------------

# Every supervisor gets at least one student; the rest are spread unevenly,
# with no supervisor having more than 12.
sup_idx <- c(seq_len(n_supervisors),
             sample(seq_len(n_supervisors), n_students - n_supervisors,
                    replace = TRUE, prob = sup_popularity))
repeat {
  counts <- tabulate(sup_idx, n_supervisors)
  over <- which(counts > 12)
  if (length(over) == 0) break
  move <- sample(which(sup_idx == over[1]), 1)
  sup_idx[move] <- sample(which(counts < 12), 1)
}
sup_idx <- sample(sup_idx)
supervisors$n_students <- tabulate(sup_idx, n_supervisors)

n <- n_students
phd       <- runif(n) < 0.30
age       <- ifelse(phd, 27 + rgamma(n, 2, scale = 3.5), 23 + rgamma(n, 2, scale = 2.5))
age       <- round(clamp(age, 22, 55))
gender    <- sample(c("Female", "Male"), n, replace = TRUE, prob = c(0.55, 0.45))
part_time <- runif(n) < plogis(-1.0 + 0.08 * (age - 28))
employment <- ifelse(part_time,
                     sample(emp_levels, n, replace = TRUE, prob = c(0.15, 0.35, 0.50)),
                     sample(emp_levels, n, replace = TRUE, prob = c(0.65, 0.30, 0.05)))
full_job     <- employment == "Full-time job"
has_children <- runif(n) < plogis(-1.6 + 0.18 * (age - 28))
lives_away   <- runif(n) < 0.40

fw_latent <- 0.5 * has_children + 0.4 * lives_away - 0.4 * full_job +
  0.2 * (employment == "None") + rnorm(n)
financial_worry <- as.integer(cut(fw_latent,
                                  quantile(fw_latent, c(0, 0.15, 0.40, 0.70, 0.90, 1)),
                                  include.lowest = TRUE))

# The workshop invitation is random: exactly half the students are invited.
invited  <- sample(rep(c(TRUE, FALSE), each = n / 2))
sessions <- ifelse(invited,
                   sample(0:6, n, replace = TRUE,
                          prob = c(0.12, 0.08, 0.10, 0.12, 0.15, 0.18, 0.25)),
                   0L)

faculty <- supervisors$faculty[sup_idx]

# 3. Hidden student profiles (for the clustering chapters) ---------------------

profile <- vapply(lives_away, function(away) {
  p <- c(0.35, 0.30, 0.20, 0.15)
  p[3] <- p[3] * if (away) 1.6 else 0.6
  sample(profiles, 1, prob = p)
}, character(1))
unusual <- sample(n, 10)
profile[unusual] <- "Unusual"

profile_params <- data.frame(
  row.names    = profiles,
  sleep        = c(7.0, 5.8, 6.4, 6.8),
  study        = c(25, 42, 24, 12),
  caffeine     = c(120, 235, 150, 130),
  exercise     = c(3.5, 1.3, 2.0, 2.3),
  support      = c(0.5, 0.0, -1.3, -0.2),
  stress       = c(-0.6, 0.9, 0.3, 0.1),
  burnout      = c(-0.3, 0.4, 0.2, 0.4),
  satisfaction = c(0.6, 0.0, -0.7, -1.0)
)
P <- profile_params[ifelse(profile == "Unusual", "Balanced", profile), ]

# 4. Latent traits: stress, burnout, support, satisfaction ---------------------

faculty_stress <- c("Education" = 0, "Health Sciences" = 0.30, "Humanities" = -0.30,
                    "Natural Sciences" = 0, "Social Sciences" = 0)

support_lat <- P$support + sup_eff_support[sup_idx] + rnorm(n, 0, 0.8)
stress_lat  <- P$stress + faculty_stress[faculty] + 0.15 * zscore(financial_worry) -
  0.25 * support_lat + 0.3 * full_job + rnorm(n, 0, 0.8)
burnout_lat <- 0.55 * stress_lat + P$burnout + rnorm(n, 0, 0.75)
satisfaction_lat <- P$satisfaction + 0.3 * support_lat - 0.2 * stress_lat +
  rnorm(n, 0, 0.7)

support_lat      <- zscore(support_lat)
stress_lat       <- zscore(stress_lat)
burnout_lat      <- zscore(burnout_lat)
satisfaction_lat <- zscore(satisfaction_lat)

# 5. Questionnaire (22 items) --------------------------------------------------

item_text <- c(
  stress_1 = "I feel unable to control important things in my studies.",
  stress_2 = "I feel nervous and stressed about my studies.",
  stress_3 = "I feel that difficulties in my studies are piling up.",
  stress_4 = "I feel confident handling problems in my studies.",
  stress_5 = "I feel overwhelmed by what I have to do.",
  stress_6 = "I find it hard to relax because of my studies.",
  burnout_1 = "I feel emotionally drained by my studies.",
  burnout_2 = "I feel exhausted when I think about my thesis.",
  burnout_3 = "Deadlines make me feel overwhelmed.",
  burnout_4 = "I have become less interested in my research.",
  burnout_5 = "I doubt the value of my studies.",
  burnout_6 = "I feel used up at the end of a study day.",
  support_1 = "My supervisor gives me useful feedback.",
  support_2 = "My supervisor is available when I need help.",
  support_3 = "My supervisor cares about my wellbeing.",
  support_4 = "My supervisor helps me plan my work.",
  support_5 = "I can discuss problems openly with my supervisor.",
  support_6 = "My supervisor encourages me when I struggle.",
  satisfaction_1 = "I am satisfied with my progress in my programme.",
  satisfaction_2 = "I enjoy my studies.",
  satisfaction_3 = "My programme meets my expectations.",
  satisfaction_4 = "I would choose this programme again."
)

shift <- function() runif(1, -0.4, 0.4)
questionnaire <- data.frame(
  stress_1 = make_item(stress_lat, 0.75, shift()),
  stress_2 = make_item(stress_lat, 0.72, shift()),
  stress_3 = make_item(stress_lat, 0.70, shift()),
  stress_4 = make_item(stress_lat, 0.62, shift(), reverse = TRUE),
  stress_5 = make_item(stress_lat, 0.78, shift()),
  stress_6 = make_item(stress_lat, 0.65, shift()),
  burnout_1 = make_item(burnout_lat, 0.78, shift()),
  burnout_2 = make_item(burnout_lat, 0.75, shift()),
  # burnout_3 also reflects stress: it loads on both factors
  burnout_3 = likert(0.45 * burnout_lat + 0.40 * stress_lat +
                       sqrt(1 - 0.45^2 - 0.40^2 - 2 * 0.45 * 0.40 * 0.6) * rnorm(n),
                     shift()),
  burnout_4 = make_item(burnout_lat, 0.68, shift()),
  burnout_5 = make_item(burnout_lat, 0.62, shift()),
  burnout_6 = make_item(burnout_lat, 0.72, shift()),
  support_1 = make_item(support_lat, 0.80, shift()),
  support_2 = make_item(support_lat, 0.72, shift()),
  support_3 = make_item(support_lat, 0.70, shift()),
  support_4 = make_item(support_lat, 0.68, shift()),
  support_5 = make_item(support_lat, 0.76, shift()),
  support_6 = make_item(support_lat, 0.66, shift()),
  satisfaction_1 = make_item(satisfaction_lat, 0.75, shift()),
  satisfaction_2 = make_item(satisfaction_lat, 0.72, shift()),
  satisfaction_3 = make_item(satisfaction_lat, 0.68, shift()),
  satisfaction_4 = make_item(satisfaction_lat, 0.70, shift())
)

# 6. Semester records ----------------------------------------------------------

nondrinker <- runif(n) < 0.08
p_sleep    <- P$sleep + 0.08 + rnorm(n, 0, 0.5)
p_study    <- P$study + rnorm(n, 0, 6)
p_caff_log <- log(P$caffeine) + rnorm(n, 0, 0.42) + 0.14 * (gender == "Male")
p_exercise <- P$exercise * exp(rnorm(n, 0, 0.3))

# A few unusual students who fit no profile (outliers for Chapters 5 and 13)
half <- seq_along(unusual) <= length(unusual) / 2
p_sleep[unusual]    <- ifelse(half, 5.2, 9.4)
p_study[unusual]    <- ifelse(half, 62, 3)
p_caff_log[unusual] <- log(ifelse(half, 780, 20))
p_exercise[unusual] <- ifelse(half, 0.2, 6.0)
nondrinker[unusual] <- FALSE

gpa_int   <- rnorm(n, 0, 0.22)
wb_int    <- rnorm(n, 0, 6)
wb_slope  <- rnorm(n, 0, 1.0)
time_eff  <- c(0, -0.3, -1.5, -3.0)   # wellbeing dips as the thesis nears
ws_full   <- c(0, 8, 6.5, 5)          # workshop effect for full attendance

sem <- expand.grid(semester = 1:4, i = seq_len(n))[, c("i", "semester")]
i <- sem$i
t <- sem$semester
N <- nrow(sem)

caffeine <- ifelse(nondrinker[i], 0, exp(p_caff_log[i] + rnorm(N, 0, 0.2)))
caffeine <- round(clamp(caffeine, 0, 900) / 5) * 5

# Caffeine reduces sleep; it does not affect GPA directly (the confounding lesson)
sleep <- p_sleep[i] - 0.0025 * (caffeine - 160) + rnorm(N, 0, 0.40)
sleep <- round(clamp(sleep, 3.5, 10), 1)

study    <- round(clamp(p_study[i] + rnorm(N, 0, 4), 2, 70))
exercise <- as.integer(clamp(rpois(N, p_exercise[i]), 0, 7))
meetings <- as.integer(clamp(rpois(N, exp(1.3 + 0.35 * support_lat[i] + 0.2 * phd[i] +
                                           sup_eff_meetings[sup_idx[i]])), 0, 15))

workshop_eff <- ifelse(invited[i], ws_full[t] * sessions[i] / 6, 0)
wellbeing <- 62 + wb_int[i] + sup_eff_wellbeing[sup_idx[i]] + time_eff[t] +
  wb_slope[i] * (t - 1) + workshop_eff + 3 * (sleep - 6.4) - 4 * stress_lat[i] -
  2 * burnout_lat[i] + 2.5 * support_lat[i] - 4 * part_time[i] + rnorm(N, 0, 5)
wellbeing <- round(clamp(wellbeing, 0, 100))

# GPA: sleep helps; study hours help with diminishing returns; supervisor
# support matters more for PhD students; gender and caffeine have no effect.
gpa <- 2.62 + gpa_int[i] + 0.10 * (sleep - 6.4) + 0.6 * (1 - exp(-study / 15)) -
  0.08 * stress_lat[i] + (0.05 + 0.09 * phd[i]) * support_lat[i] + rnorm(N, 0, 0.17)
gpa <- round(clamp(gpa, 0, 4), 2)

semesters <- data.frame(
  student_id = fmt_id("S", i, 4),
  semester = t,
  gpa = gpa,
  sleep_hours = sleep,
  study_hours = study,
  exercise_days = exercise,
  caffeine_mg = caffeine,
  supervisor_meetings = meetings,
  wellbeing = wellbeing
)

# 7. Considering dropout (end of year 1) ---------------------------------------

lp0 <- log(2.6) * stress_lat + log(1.8) * (financial_worry - 3) + log(0.45) * support_lat +
  0.9 * full_job + 0.4 * part_time + 0.45 * burnout_lat
b0 <- uniroot(function(b) mean(plogis(b + lp0)) - 0.15, c(-8, 4))$root
dropout <- runif(n) < plogis(b0 + lp0)

# 8. Attrition and missing data ------------------------------------------------

# Leaving after year 1 is much more common among students who considered it,
# so the missing semester 3-4 rows are not missing at random.
left <- runif(n) < ifelse(dropout, 0.26, 0.025)
semesters <- semesters[!(left[i] & t > 2), ]

# Item non-response (about 2%) and a more sensitive question (about 5%)
for (v in names(questionnaire)) {
  questionnaire[[v]][runif(n) < 0.02] <- NA
}
fw_observed <- financial_worry
fw_observed[runif(n) < 0.05] <- NA

# Occasional missing self-reports in semester records (about 1%)
for (v in c("sleep_hours", "study_hours", "exercise_days", "caffeine_mg")) {
  semesters[[v]][runif(nrow(semesters)) < 0.01] <- NA
}

# 9. Assemble the clean tables -------------------------------------------------

students <- data.frame(
  student_id = fmt_id("S", seq_len(n), 4),
  supervisor_id = supervisors$supervisor_id[sup_idx],
  age = age,
  gender = gender,
  faculty = faculty,
  programme = ifelse(phd, "PhD", "Master's"),
  study_mode = ifelse(part_time, "Part-time", "Full-time"),
  employment = employment,
  has_children = yes_no(has_children),
  lives_away = yes_no(lives_away),
  financial_worry = fw_observed,
  workshop = ifelse(invited, "Invited", "Not invited"),
  workshop_sessions = sessions,
  considering_dropout = yes_no(dropout)
)
questionnaire <- cbind(student_id = students$student_id, questionnaire)

# Entry errors that the raw file shows and a careful cleaner turns into NA.
# They are NA in the clean files, because the true value cannot be known.
entry_errors <- list(
  age   = list(row = sample(n, 1), value = 250),
  sleep = list(row = sample(nrow(semesters), 1), value = 26),
  study = list(row = sample(nrow(semesters), 1), value = 700),
  gpa   = list(row = sample(nrow(semesters), 1), value = 34.5)
)
students$age[entry_errors$age$row] <- NA
semesters$sleep_hours[entry_errors$sleep$row] <- NA
semesters$study_hours[entry_errors$study$row] <- NA
semesters$gpa[entry_errors$gpa$row] <- NA

# 10. Open-ended answers -------------------------------------------------------

theme_bank <- list(
  Supervision = c(
    "My supervisor is hard to reach, and I often feel stuck for weeks.",
    "I wait a long time for feedback on my chapters, sometimes more than a month.",
    "My supervisor and I don't agree on the direction of my research.",
    "I rarely get clear guidance, so I am never sure if I am on the right track.",
    "Meetings with my supervisor are short and I leave with more questions than answers.",
    "My supervisor changed the focus of my thesis twice, which set me back.",
    "I feel nervous asking my supervisor for help.",
    "My supervisor is very busy with other students and administration."),
  Workload = c(
    "Balancing coursework, teaching duties and my thesis leaves me no time to rest.",
    "There is simply too much to do and not enough hours in the week.",
    "Deadlines pile up at the end of every semester.",
    "I work late most nights just to keep up with the reading.",
    "Writing the literature review took far longer than I expected.",
    "The amount of data collection for my project is overwhelming.",
    "I study every weekend and still feel behind.",
    "Managing several assignments at once is exhausting."),
  Finances = c(
    "Paying tuition fees while supporting myself is a constant worry.",
    "My scholarship does not cover my living costs.",
    "I had to take a second job to pay for my studies.",
    "Transport and rent take most of my income.",
    "I worry about money more than about my research.",
    "Buying books and paying for conferences is expensive.",
    "My salary was delayed several times, which made everything harder.",
    "I cannot afford to travel for data collection."),
  Family = c(
    "Looking after my children while studying is very difficult.",
    "My family needs me at home and I feel guilty spending time on my thesis.",
    "Caring for a sick parent took a lot of my time this year.",
    "It is hard to find a quiet place to study at home.",
    "Balancing family responsibilities with research is my biggest challenge.",
    "My family does not really understand why a postgraduate degree takes so long.",
    "After my baby was born, I struggled to keep my study routine.",
    "Family events and obligations often interrupt my plans."),
  Health = c(
    "I have trouble sleeping, especially before deadlines.",
    "Stress has affected my health and I get headaches often.",
    "I feel tired all the time and find it hard to concentrate.",
    "I stopped exercising and I can feel the difference.",
    "Anxiety about my progress keeps me awake at night.",
    "I was ill for several weeks and fell behind.",
    "I drink too much coffee to stay awake.",
    "Burnout made me lose interest in my research for a while."),
  Isolation = c(
    "I moved to a new city for my studies and I feel lonely.",
    "Research can be a lonely process, and I miss working with others.",
    "I don't know many people in my department.",
    "Being far from my family makes the hard days harder.",
    "There are few chances to meet other postgraduate students.",
    "I work alone most of the time and have no one to discuss ideas with.",
    "I feel like an outsider in my research group.",
    "I miss home, especially during exam periods."),
  Other = c(
    "Getting ethical approval for my study took much longer than planned.",
    "Finding participants for my data collection was a real problem.",
    "Learning statistics for my analysis was harder than I expected.",
    "The library does not have many of the journals I need.",
    "Administrative procedures at the university are slow and confusing.",
    "Writing in academic English is my biggest challenge.",
    "Frequent power cuts made it hard to work in the evenings.",
    "Finding reliable sources in my own language was difficult.")
)
themes <- names(theme_bank)

# Lower-case the first letter unless the sentence starts with "I"
decap <- function(x) {
  ifelse(grepl("^I[ ']", x), x, paste0(tolower(substr(x, 1, 1)), substring(x, 2)))
}
typos <- c("difficult" = "dificult", "because" = "becuase", "research" = "reserch",
           "family" = "familly", "different" = "diffrent", "feedback" = "feed back")

respondent <- which(!left & runif(n) < 0.95)

theme_weights <- cbind(
  Supervision = exp(1.0 - 1.1 * support_lat),
  Workload    = exp(0.6 + 0.9 * zscore(p_study)),
  Finances    = exp(-0.4 + 0.5 * (financial_worry - 3)),
  Family      = exp(-1.0 + 1.6 * has_children),
  Health      = exp(-0.3 - 0.8 * zscore(p_sleep) + 0.5 * burnout_lat),
  Isolation   = exp(-0.8 + 1.2 * lives_away + 0.8 * (profile == "Isolated")),
  Other       = 0.35
)

write_answer <- function(k) {
  w <- theme_weights[k, ]
  main <- sample(themes, 1, prob = w)
  text <- sample(theme_bank[[main]], 1)
  second <- ""
  opener <- sample(c("", "", "", "Honestly, ", "To be honest, ", "For me, "), 1)
  if (opener != "") text <- paste0(opener, decap(text))
  if (runif(1) < 0.30) {
    second <- sample(setdiff(themes, main), 1, prob = w[setdiff(themes, main)])
    joiner <- sample(c(" Also, ", " On top of that, ", " And "), 1)
    text <- paste0(text, joiner, decap(sample(theme_bank[[second]], 1)))
  }
  closers <- c("", "", "", " It has been a difficult year.",
               " I hope things get better next year.",
               " Otherwise the programme is good.")
  if (dropout[k]) closers <- c(closers, " Some days I think about quitting.")
  if (invited[k] && sessions[k] >= 3) closers <- c(closers, " The workshop helped a little.")
  text <- paste0(text, sample(closers, 1))
  # Variation found in real answers: typos, lower case, missing full stop
  if (runif(1) < 0.06) {
    hit <- names(typos)[vapply(names(typos), grepl, logical(1), x = text)]
    if (length(hit) > 0) {
      word <- hit[1]
      text <- sub(word, typos[[word]], text)
    }
  }
  if (runif(1) < 0.10) text <- decap(text)
  if (runif(1) < 0.10) text <- sub("\\.$", "", text)
  c(theme = main, second = second, text = text)
}

# The answers above fix each student's themes (and use the same random draws as
# version 1.0.0). Version 1.1.0 rewrites the text from a much larger phrase bank
# (answer_bank.R), using a separate random stream, so every other value in the
# dataset stays exactly the same.
answers <- t(vapply(respondent, write_answer, character(3)))
saved_seed <- .Random.seed
set.seed(20261101)
source(file.path("data-raw", "answer_bank.R"))
answers[, "text"] <- vapply(seq_along(respondent), function(i) {
  k <- respondent[i]
  write_varied(answers[i, "theme"], answers[i, "second"],
               dropout = dropout[k], workshop = invited[k] && sessions[k] >= 3)
}, character(1))
assign(".Random.seed", saved_seed, envir = globalenv())
open_responses <- data.frame(
  student_id = students$student_id[respondent],
  biggest_challenge = answers[, "text"]
)
coded_rows <- sort(sample(nrow(open_responses), 200))
open_responses_coded <- data.frame(
  student_id = open_responses$student_id[coded_rows],
  biggest_challenge = open_responses$biggest_challenge[coded_rows],
  theme = answers[coded_rows, "theme"]
)

# 11. Counselling service: weekly visits over five academic years --------------

# Requested by the counselling doctors as an internal analysis (not the thesis).
week_start <- seq(as.Date("2020-09-07"), by = "week", length.out = 260)
week_of_year <- ((seq_along(week_start) - 1) %% 52) + 1   # week 1 = early September
academic_year <- ((seq_along(week_start) - 1) %/% 52) + 1

season <- rep(1.0, 52)
season[1:2]   <- 0.7    # first weeks of the year
season[16:17] <- 1.45   # before semester 1 exams
season[18:19] <- 1.30   # semester 1 exams
season[20]    <- 0.50   # mid-year break
season[29]    <- 0.60   # spring break
season[37:38] <- 1.45   # before semester 2 exams
season[39:40] <- 1.30   # semester 2 exams
season[41:52] <- 0.25   # summer: reduced service
level <- 35 * 1.06^((seq_along(week_start) - 1) / 52)   # about 6% growth per year
lambda <- level * season[week_of_year]
awareness_week <- 3 * 52 + 8                             # one unusual week in year 4
lambda[awareness_week] <- lambda[awareness_week] * 1.9
counselling_visits <- data.frame(week_start = week_start, visits = rpois(260, lambda))

# 12. The messy raw survey export ----------------------------------------------

vary <- function(x, map) {
  out <- x
  for (value in names(map)) {
    hit <- which(x == value)
    out[hit] <- sample(map[[value]]$labels, length(hit), replace = TRUE,
                       prob = map[[value]]$prob)
  }
  out
}
variants <- function(labels, prob) list(labels = labels, prob = prob)

wide <- reshape(semesters, idvar = "student_id", timevar = "semester",
                direction = "wide", sep = "_S")
wide <- merge(data.frame(student_id = students$student_id), wide,
              by = "student_id", all.x = TRUE, sort = FALSE)
wide <- wide[match(students$student_id, wide$student_id), ]

missing_code <- function(x, codes = c("", "99", "-9"), prob = c(0.5, 0.3, 0.2)) {
  out <- as.character(x)
  hit <- which(is.na(x))
  out[hit] <- sample(codes, length(hit), replace = TRUE, prob = prob)
  out
}

sleep_text <- function(x) {
  out <- as.character(x)
  u <- runif(length(x))
  ok <- !is.na(x)
  hrs <- ok & u < 0.10
  out[hrs] <- paste(x[hrs], sample(c("hrs", "hours", "h"), sum(hrs), replace = TRUE))
  comma <- ok & u >= 0.10 & u < 0.16 & x != round(x)
  out[comma] <- sub(".", ",", as.character(x[comma]), fixed = TRUE)
  out[!ok] <- ""
  out
}

age_raw <- students$age
age_raw[entry_errors$age$row] <- entry_errors$age$value

raw <- data.frame(
  "Q1_Student ID" = students$student_id,
  "Q2_Age" = missing_code(age_raw, "", 1),
  "Q3_Gender" = vary(students$gender, list(
    Female = variants(c("Female", "female", "F", "Female "), c(0.6, 0.2, 0.12, 0.08)),
    Male   = variants(c("Male", "male", "M", "Male "), c(0.6, 0.2, 0.12, 0.08)))),
  "Q4_Faculty" = vary(students$faculty, list(
    "Education"        = variants(c("Education", "education", "Faculty of Education"), c(0.7, 0.15, 0.15)),
    "Health Sciences"  = variants(c("Health Sciences", "Health Sci.", "health sciences"), c(0.7, 0.15, 0.15)),
    "Humanities"       = variants(c("Humanities", "humanities", "Faculty of Humanities"), c(0.7, 0.15, 0.15)),
    "Natural Sciences" = variants(c("Natural Sciences", "Natural Sci.", "Sciences"), c(0.7, 0.15, 0.15)),
    "Social Sciences"  = variants(c("Social Sciences", "Social Sci.", "social sciences"), c(0.7, 0.15, 0.15)))),
  "Q5_Programme" = vary(students$programme, list(
    "Master's" = variants(c("Master's", "Masters", "MSc", "master's"), c(0.6, 0.2, 0.1, 0.1)),
    "PhD"      = variants(c("PhD", "Ph.D.", "phd"), c(0.7, 0.2, 0.1)))),
  "Q6_Study mode" = vary(students$study_mode, list(
    "Full-time" = variants(c("Full-time", "Full time", "full-time"), c(0.7, 0.2, 0.1)),
    "Part-time" = variants(c("Part-time", "Part time", "part-time"), c(0.7, 0.2, 0.1)))),
  "Q7_Paid work" = vary(students$employment, list(
    "None" = variants(c("None", "none", "No job"), c(0.7, 0.15, 0.15)),
    "Part-time job" = variants("Part-time job", 1),
    "Full-time job" = variants("Full-time job", 1))),
  "Q8_Children" = vary(students$has_children, list(
    Yes = variants(c("Yes", "yes", "Y"), c(0.7, 0.2, 0.1)),
    No  = variants(c("No", "no", "N"), c(0.7, 0.2, 0.1)))),
  "Q9_Moved away from family" = vary(students$lives_away, list(
    Yes = variants(c("Yes", "yes", "Y"), c(0.7, 0.2, 0.1)),
    No  = variants(c("No", "no", "N"), c(0.7, 0.2, 0.1)))),
  "Q10_How worried are you about money? (1-5)" = missing_code(students$financial_worry),
  "Workshop group" = students$workshop,
  "Workshop sessions attended" = students$workshop_sessions,
  "Y1_Considered leaving?" = vary(students$considering_dropout, list(
    Yes = variants(c("Yes", "yes", "Y"), c(0.7, 0.2, 0.1)),
    No  = variants(c("No", "no", "N"), c(0.7, 0.2, 0.1)))),
  check.names = FALSE
)

# Questionnaire items as Q11_1 ... Q11_22, missing as blank or 99
items_raw <- as.data.frame(lapply(questionnaire[-1], missing_code,
                                  codes = c("", "99"), prob = c(0.8, 0.2)))
names(items_raw) <- paste0("Q11_", seq_along(items_raw))
raw <- cbind(raw, items_raw)

# Semester measurements, wide: GPA_S1 ... Wellbeing_S4
sem_vars <- c(gpa = "GPA", sleep_hours = "Sleep", study_hours = "Study",
              exercise_days = "Exercise", caffeine_mg = "Caffeine",
              supervisor_meetings = "Meetings", wellbeing = "Wellbeing")
error_cell <- function(var, s) {
  key <- c(sleep_hours = "sleep", study_hours = "study", gpa = "gpa")[var]
  if (is.na(key)) return(NULL)
  e <- entry_errors[[key]]
  row <- semesters[e$row, ]
  if (row$semester != s) return(NULL)
  list(student = row$student_id, value = e$value)
}
for (s in 1:4) {
  for (v in names(sem_vars)) {
    x <- wide[[paste0(v, "_S", s)]]
    col <- if (v == "sleep_hours") sleep_text(x) else ifelse(is.na(x), "", as.character(x))
    err <- error_cell(v, s)
    if (!is.null(err)) col[students$student_id == err$student] <- as.character(err$value)
    raw[[paste0(sem_vars[[v]], "_S", s)]] <- col
  }
}

# Duplicated submissions and test responses
dups <- raw[sample(n, 12), ]
raw <- rbind(raw, dups)
raw <- raw[sample(nrow(raw)), ]
tests <- raw[1:3, ]
tests[] <- ""
tests[["Q1_Student ID"]] <- c("TEST", "test", "TEST2")
tests[["Q2_Age"]] <- c("99", "", "30")
tests[["Q3_Gender"]] <- c("Female", "", "Male")
raw <- rbind(tests, raw)
raw <- cbind("Response ID" = fmt_id("R", seq_len(nrow(raw)), 4), raw)
rownames(raw) <- NULL

# 13. SPSS file with labels ----------------------------------------------------

lab <- function(x, labels, label) {
  codes <- setNames(seq_along(labels), labels)
  labelled(unname(codes[x]), codes, label = label)
}
lab01 <- function(x, labels, label) {
  codes <- setNames(c(0, 1), labels)
  labelled(unname(codes[x]), codes, label = label)
}
agree <- c("Strongly disagree" = 1, "Disagree" = 2, "Neutral" = 3,
           "Agree" = 4, "Strongly agree" = 5)

spss <- data.frame(student_id = students$student_id)
attr(spss$student_id, "label") <- "Student identifier"
spss$supervisor_id <- students$supervisor_id
attr(spss$supervisor_id, "label") <- "Supervisor identifier"
spss$age <- labelled(students$age, label = "Age in years at baseline")
spss$gender <- lab(students$gender, c("Female", "Male"), "Gender")
spss$faculty <- lab(students$faculty, faculties, "Faculty")
spss$programme <- lab(students$programme, c("Master's", "PhD"), "Degree programme")
spss$study_mode <- lab(students$study_mode, c("Full-time", "Part-time"), "Study mode")
spss$employment <- labelled(match(students$employment, emp_levels) - 1,
                            setNames(0:2, emp_levels), label = "Paid work alongside study")
spss$has_children <- lab01(students$has_children, c("No", "Yes"), "Has children")
spss$lives_away <- lab01(students$lives_away, c("No", "Yes"), "Moved away from family to study")
spss$financial_worry <- labelled(students$financial_worry,
                                 c("Not at all" = 1, "Slightly" = 2, "Moderately" = 3,
                                   "Very" = 4, "Extremely" = 5),
                                 label = "How worried are you about money?")
spss$workshop <- lab01(students$workshop, c("Not invited", "Invited"),
                       "Randomly invited to the wellbeing workshop")
spss$workshop_sessions <- labelled(students$workshop_sessions,
                                   label = "Workshop sessions attended (0-6)")
spss$considering_dropout <- lab01(students$considering_dropout, c("No", "Yes"),
                                  "Seriously considered leaving the programme (end of year 1)")
for (v in names(item_text)) {
  spss[[v]] <- labelled(questionnaire[[v]], agree, label = item_text[[v]])
}

# 14. Write the files ----------------------------------------------------------

write_csv <- function(x, file) {
  write.csv(x, file.path(out_dir, file), row.names = FALSE, na = "", fileEncoding = "UTF-8")
}
write_csv(students, "students.csv")
write_csv(questionnaire, "questionnaire.csv")
write_csv(semesters, "semesters.csv")
write_csv(supervisors, "supervisors.csv")
write_csv(open_responses, "open_responses.csv")
write_csv(open_responses_coded, "open_responses_coded.csv")
write_csv(counselling_visits, "counselling_visits.csv")
write_xlsx(list(responses = raw), file.path(out_dir, "wellbeing_raw.xlsx"))
write_sav(spss, file.path(out_dir, "wellbeing.sav"))
writeLines(dataset_version, file.path(out_dir, "VERSION"))

# The hidden "truth" behind the data, used only by the check script
saveRDS(list(profile = profile, left = left, respondent = respondent,
             theme = answers[, "theme"], unusual = unusual,
             entry_errors = entry_errors),
        file.path("data-raw", "truth.rds"))

cat("Graduate Wellbeing Study, version", dataset_version, "\n")
cat("  students:", nrow(students), " semesters:", nrow(semesters),
    " open responses:", nrow(open_responses), " raw rows:", nrow(raw), "\n")
