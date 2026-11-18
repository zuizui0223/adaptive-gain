args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 3) {
  stop("usage: Rscript examples/villavicencio_link_frequency_threshold_audit.R INPUT.csv PREDICTIONS.csv FOLDS.csv")
}
input_path <- args[[1]]
prediction_path <- args[[2]]
fold_path <- args[[3]]

predictors <- c(
  "focal_excluded_overlap_weeks",
  "plant_flowering_weeks",
  "pollinator_otherplant_active_weeks"
)
thresholds <- c(2L, 3L)
transitions <- c("2008->2009", "2009->2010", "2010->2011")

data <- read.csv(input_path, stringsAsFactors = FALSE, check.names = FALSE)
required <- c(
  "transition", "previous_weight", "current_weight", predictors
)
missing <- setdiff(required, names(data))
if (length(missing) > 0) {
  stop(paste("missing required columns:", paste(missing, collapse = ", ")))
}
data <- data[data$transition %in% transitions, , drop = FALSE]

prepare_fold <- function(train, test) {
  for (name in predictors) {
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
clip_probability <- function(x) {
  pmin(pmax(as.numeric(x), 1e-8), 1 - 1e-8)
}

prediction_rows <- list()
fold_rows <- list()
pi <- 1L
fi <- 1L

for (threshold in thresholds) {
  previous_positive <- as.numeric(data$previous_weight) >= threshold
  current_positive <- as.numeric(data$current_weight) >= threshold

  for (risk in c("gain", "loss")) {
    if (risk == "gain") {
      risk_data <- data[!previous_positive, , drop = FALSE]
      risk_data$outcome <- as.integer(
        as.numeric(risk_data$current_weight) >= threshold
      )
    } else {
      risk_data <- data[previous_positive, , drop = FALSE]
      risk_data$outcome <- as.integer(
        as.numeric(risk_data$current_weight) < threshold
      )
    }

    for (held_out in transitions) {
      train <- risk_data[risk_data$transition != held_out, , drop = FALSE]
      test <- risk_data[risk_data$transition == held_out, , drop = FALSE]
      if (length(unique(train$outcome)) < 2 || length(unique(test$outcome)) < 2) {
        stop(paste(threshold, risk, held_out, "has a degenerate outcome"))
      }

      prepared <- prepare_fold(train, test)
      train <- prepared$train
      test <- prepared$test
      formula <- as.formula(
        paste("outcome ~", paste(predictors, collapse = " + "))
      )
      fit <- suppressWarnings(
        glm(formula, data = train, family = binomial())
      )
      model_probability <- clip_probability(
        predict(fit, newdata = test, type = "response")
      )
      null_probability <- clip_probability(
        rep(mean(train$outcome), nrow(test))
      )

      prediction_rows[[pi]] <- data.frame(
        threshold = threshold,
        risk_set = risk,
        transition = held_out,
        outcome = as.integer(test$outcome),
        model_probability = model_probability,
        null_probability = null_probability,
        stringsAsFactors = FALSE
      )
      pi <- pi + 1L

      fold_rows[[fi]] <- data.frame(
        threshold = threshold,
        risk_set = risk,
        held_out_transition = held_out,
        train_n = nrow(train),
        test_n = nrow(test),
        train_events = sum(train$outcome == 1),
        test_events = sum(test$outcome == 1),
        converged = isTRUE(fit$converged),
        coefficient_count = length(coef(fit)),
        finite_coefficient_count = sum(is.finite(coef(fit))),
        stringsAsFactors = FALSE
      )
      fi <- fi + 1L
    }
  }
}

write.csv(do.call(rbind, prediction_rows), prediction_path, row.names = FALSE)
write.csv(do.call(rbind, fold_rows), fold_path, row.names = FALSE)
