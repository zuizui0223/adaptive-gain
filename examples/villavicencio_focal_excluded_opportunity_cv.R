args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 3) {
  stop("usage: Rscript examples/villavicencio_focal_excluded_opportunity_cv.R INPUT.csv PREDICTIONS.csv FOLDS.csv")
}

input_path <- args[[1]]
prediction_path <- args[[2]]
fold_path <- args[[3]]

full_predictors <- c(
  "focal_excluded_overlap_weeks",
  "plant_flowering_weeks",
  "pollinator_otherplant_active_weeks"
)
model_sets <- list(
  full = full_predictors,
  drop_pairwise_overlap = c(
    "plant_flowering_weeks",
    "pollinator_otherplant_active_weeks"
  )
)

scopes <- list(
  strict_core_2008_2011 = c("2008->2009", "2009->2010", "2010->2011"),
  near_core_2007_2011 = c("2007->2008", "2008->2009", "2009->2010", "2010->2011"),
  all_annual_2006_2011 = c("2006->2007", "2007->2008", "2008->2009", "2009->2010", "2010->2011")
)

data <- read.csv(input_path, stringsAsFactors = FALSE, check.names = FALSE)
required <- c("transition", "risk_set", "outcome", full_predictors)
missing <- setdiff(required, names(data))
if (length(missing) > 0) {
  stop(paste("missing required columns:", paste(missing, collapse = ", ")))
}

prepare_fold <- function(train, test) {
  for (name in full_predictors) {
    train_value <- log1p(as.numeric(train[[name]]))
    test_value <- log1p(as.numeric(test[[name]]))
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

clip_probability <- function(value) {
  pmin(pmax(as.numeric(value), 1e-8), 1 - 1e-8)
}

prediction_rows <- list()
fold_rows <- list()
row_index <- 1
fold_index <- 1

for (scope_name in names(scopes)) {
  scope_transitions <- scopes[[scope_name]]
  scope_data <- data[data$transition %in% scope_transitions, , drop = FALSE]

  for (risk in c("gain", "loss")) {
    risk_data <- scope_data[scope_data$risk_set == risk, , drop = FALSE]
    transitions <- scope_transitions[
      scope_transitions %in% unique(risk_data$transition)
    ]
    if (length(transitions) < 2) {
      stop(paste(scope_name, risk, "has fewer than two transitions"))
    }

    for (held_out in transitions) {
      train_raw <- risk_data[risk_data$transition != held_out, , drop = FALSE]
      test_raw <- risk_data[risk_data$transition == held_out, , drop = FALSE]
      prepared <- prepare_fold(train_raw, test_raw)
      train <- prepared$train
      test <- prepared$test
      null_probability <- clip_probability(
        rep(mean(train$outcome), nrow(test))
      )

      for (model_name in names(model_sets)) {
        predictors <- model_sets[[model_name]]
        formula <- as.formula(
          paste("outcome ~", paste(predictors, collapse = " + "))
        )
        fit <- suppressWarnings(
          glm(formula, data = train, family = binomial())
        )
        model_probability <- clip_probability(
          predict(fit, newdata = test, type = "response")
        )

        prediction_rows[[row_index]] <- data.frame(
          analysis_scope = scope_name,
          risk_set = risk,
          transition = held_out,
          model = model_name,
          outcome = as.integer(test$outcome),
          model_probability = model_probability,
          null_probability = null_probability,
          stringsAsFactors = FALSE
        )
        row_index <- row_index + 1

        fold_rows[[fold_index]] <- data.frame(
          analysis_scope = scope_name,
          risk_set = risk,
          held_out_transition = held_out,
          model = model_name,
          train_n = nrow(train),
          test_n = nrow(test),
          train_events = sum(train$outcome == 1),
          test_events = sum(test$outcome == 1),
          converged = isTRUE(fit$converged),
          coefficient_count = length(coef(fit)),
          finite_coefficient_count = sum(is.finite(coef(fit))),
          stringsAsFactors = FALSE
        )
        fold_index <- fold_index + 1
      }
    }
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
