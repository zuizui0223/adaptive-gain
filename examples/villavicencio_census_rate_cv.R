args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 3) {
  stop("usage: Rscript examples/villavicencio_census_rate_cv.R INPUT.csv PREDICTIONS.csv FOLDS.csv")
}

input_path <- args[[1]]
prediction_path <- args[[2]]
fold_path <- args[[3]]

data <- read.csv(input_path, stringsAsFactors = FALSE, check.names = FALSE)

required <- c(
  "transition",
  "previous_rate_logit",
  "current_siteweek_opportunity_fraction",
  "current_success_censuses",
  "current_trials"
)
missing <- setdiff(required, names(data))
if (length(missing) > 0) {
  stop(paste("missing required columns:", paste(missing, collapse = ", ")))
}

transitions <- c(
  "2008_early->2008_mid",
  "2008_mid->2008_late",
  "2009_early->2009_mid",
  "2009_mid->2009_late",
  "2010_early->2010_mid",
  "2010_mid->2010_late"
)

if (!setequal(unique(data$transition), transitions)) {
  stop("census-rate table transition set disagrees with frozen primary scope")
}

predictors <- c(
  "previous_rate_logit",
  "current_siteweek_opportunity_fraction"
)

prepare_fold <- function(train, test) {
  for (name in predictors) {
    train_value <- as.numeric(train[[name]])
    test_value <- as.numeric(test[[name]])
    center <- mean(train_value)
    scale_value <- sd(train_value)
    if (!is.finite(scale_value) || scale_value == 0) {
      train[[name]] <- rep(0, length(train_value))
      test[[name]] <- rep(0, length(test_value))
    } else {
      train[[name]] <- (train_value - center) / scale_value
      test[[name]] <- (test_value - center) / scale_value
    }
  }
  list(train = train, test = test)
}

model_sets <- list(
  history_only = c("previous_rate_logit"),
  history_plus_opportunity = c(
    "previous_rate_logit",
    "current_siteweek_opportunity_fraction"
  )
)

clip_probability <- function(value) {
  pmin(pmax(as.numeric(value), 1e-8), 1 - 1e-8)
}

prediction_rows <- list()
fold_rows <- list()
prediction_index <- 1
fold_index <- 1

for (held_out in transitions) {
  train_raw <- data[data$transition != held_out, , drop = FALSE]
  test_raw <- data[data$transition == held_out, , drop = FALSE]

  prepared <- prepare_fold(train_raw, test_raw)
  train <- prepared$train
  test <- prepared$test

  for (model_name in names(model_sets)) {
    model_predictors <- model_sets[[model_name]]
    formula <- as.formula(
      paste(
        "cbind(current_success_censuses, current_trials - current_success_censuses) ~",
        paste(model_predictors, collapse = " + ")
      )
    )
    fit <- suppressWarnings(
      glm(formula, data = train, family = binomial())
    )
    probability <- clip_probability(
      predict(fit, newdata = test, type = "response")
    )

    prediction_rows[[prediction_index]] <- data.frame(
      transition = held_out,
      model = model_name,
      successes = as.integer(test$current_success_censuses),
      trials = as.integer(test$current_trials),
      probability = probability,
      stringsAsFactors = FALSE
    )
    prediction_index <- prediction_index + 1

    fold_rows[[fold_index]] <- data.frame(
      held_out_transition = held_out,
      model = model_name,
      train_rows = nrow(train),
      test_rows = nrow(test),
      train_successes = sum(train$current_success_censuses),
      train_trials = sum(train$current_trials),
      test_successes = sum(test$current_success_censuses),
      test_trials = sum(test$current_trials),
      converged = isTRUE(fit$converged),
      coefficient_count = length(coef(fit)),
      finite_coefficient_count = sum(is.finite(coef(fit))),
      stringsAsFactors = FALSE
    )
    fold_index <- fold_index + 1
  }
}

write.csv(
  do.call(rbind, prediction_rows),
  prediction_path,
  row.names = FALSE
)
write.csv(
  do.call(rbind, fold_rows),
  fold_path,
  row.names = FALSE
)
