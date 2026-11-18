args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 2) {
  stop("usage: Rscript examples/fit_routeability_pilot_nuisance_glmm.R PILOT_B.csv OUTPUT.csv")
}

input_path <- args[[1]]
output_path <- args[[2]]

suppressPackageStartupMessages(library(lme4))

data <- read.csv(input_path, stringsAsFactors = FALSE, check.names = FALSE)

required <- c(
  "individual_id",
  "colony_id",
  "correct_within_window",
  "timeout",
  "block"
)
missing <- setdiff(required, names(data))
if (length(missing) > 0) {
  stop(paste("missing required columns:", paste(missing, collapse = ", ")))
}

forbidden <- c("architecture", "access_mode", "budget", "H1", "H2")
leaked <- intersect(forbidden, names(data))
if (length(leaked) > 0) {
  stop(paste("forbidden focal columns:", paste(leaked, collapse = ", ")))
}

as_bool <- function(value, name) {
  text <- tolower(trimws(as.character(value)))
  out <- rep(NA, length(text))
  out[text %in% c("1", "true", "yes", "y")] <- TRUE
  out[text %in% c("0", "false", "no", "n")] <- FALSE
  if (any(is.na(out))) {
    stop(paste(name, "contains non-boolean values"))
  }
  out
}

data$correct_within_window <- as_bool(
  data$correct_within_window,
  "correct_within_window"
)
data$timeout <- as_bool(data$timeout, "timeout")
if (any(data$timeout & data$correct_within_window)) {
  stop("timeout trials cannot be correct_within_window")
}

data$individual_id <- factor(trimws(data$individual_id))
if (any(nchar(as.character(data$individual_id)) == 0)) {
  stop("individual_id cannot be empty")
}

colony_text <- trimws(data$colony_id)
if (any(colony_text == "") && any(colony_text != "")) {
  stop("colony_id must be either fully populated or fully empty")
}
colony_available <- all(colony_text != "")
if (colony_available) {
  data$colony_id <- factor(colony_text)
  colony_count <- nlevels(data$colony_id)
} else {
  colony_count <- 0L
}

if (nlevels(data$individual_id) < 2) {
  stop("at least two individuals are required")
}
if (length(unique(data$correct_within_window)) < 2) {
  stop("pooled pilot outcome must contain both successes and failures")
}

if (colony_available && colony_count > 1) {
  formula <- correct_within_window ~ 1 + (1 | individual_id) + (1 | colony_id)
} else {
  formula <- correct_within_window ~ 1 + (1 | individual_id)
}

fit <- suppressWarnings(
  glmer(
    formula,
    data = data,
    family = binomial(),
    control = glmerControl(
      optimizer = "bobyqa",
      optCtrl = list(maxfun = 200000)
    )
  )
)

messages <- fit@optinfo$conv$lme4$messages
optimizer_code <- fit@optinfo$conv$opt
optimizer_converged <- (
  is.null(optimizer_code)
  || all(as.integer(optimizer_code) == 0L)
)

# lme4 may report a boundary/singular fit through the same message channel
# used for genuine convergence warnings. Singularity is a separate nuisance
# diagnostic below and must not be mislabeled as optimizer non-convergence.
if (is.null(messages)) {
  non_singular_messages <- character(0)
} else {
  non_singular_messages <- messages[
    !grepl("boundary \\(singular\\) fit", messages)
  ]
}
converged <- optimizer_converged && length(non_singular_messages) == 0
singular <- isSingular(fit, tol = 1e-4)

vc <- as.data.frame(VarCorr(fit))
individual_rows <- vc[vc$grp == "individual_id" & is.na(vc$var2), , drop = FALSE]
if (nrow(individual_rows) != 1) {
  stop("could not extract one individual random-intercept SD")
}
individual_sd <- individual_rows$sdcor[[1]]

if (colony_available && colony_count > 1) {
  colony_rows <- vc[vc$grp == "colony_id" & is.na(vc$var2), , drop = FALSE]
  if (nrow(colony_rows) != 1) {
    stop("could not extract one colony random-intercept SD")
  }
  colony_sd <- colony_rows$sdcor[[1]]
} else {
  colony_sd <- 0
}

intercept <- unname(fixef(fit)[["(Intercept)"]])
if (!all(is.finite(c(intercept, individual_sd, colony_sd)))) {
  stop("non-finite nuisance GLMM estimate")
}

output <- data.frame(
  pooled_intercept_logit = intercept,
  individual_sd_logit = individual_sd,
  colony_sd_logit = colony_sd,
  colony_count_in_fit = colony_count,
  individual_count_in_fit = nlevels(data$individual_id),
  trial_count_in_fit = nrow(data),
  converged = converged,
  singular = singular,
  stringsAsFactors = FALSE
)
write.csv(output, output_path, row.names = FALSE)
