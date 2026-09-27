args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 3) {
  stop("usage: Rscript examples/villavicencio_conventional_filter_cv.R INPUT.csv PREDICTIONS.csv FOLDS.csv")
}

input_path <- args[[1]]
prediction_path <- args[[2]]
fold_path <- args[[3]]

predictors <- c(
  "phenological_overlap",
  "flower_abundance",
  "corolla_length",
  "corolla_aperture",
  "height_mean",
  "body_length",
  "proboscis_length",
  "proboscis_width",
  "body_width",
  "body_thickness"
)

data <- read.csv(input_path, stringsAsFactors = FALSE, check.names = FALSE)
required <- c("transition", "risk_set", "outcome", "complete_case", predictors)
missing <- setdiff(required, names(data))
if (length(missing) > 0) {
  stop(paste("missing required columns:", paste(missing, collapse = ", ")))
}

complete_flag <- tolower(as.character(data$complete_case)) %in% c("true", "1", "yes", "y")
data <- data[complete_flag, , drop = FALSE]

prepare_fold <- function(train, test) {
  for (name in predictors) {
    train_value <- as.numeric(train[[name]])
    test_value <- as.numeric(test[[name]])

    if (name == "flower_abundance") {
      train_value <- log1p(train_value)
      test_value <- log1p(test_value)
    }

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

for (risk in c("gain", "loss")) {
  risk_data <- data[data$risk_set == risk, , drop = FALSE]
  transitions <- sort(unique(risk_data$transition))

  if (length(transitions) < 2) {
    stop(paste("risk set", risk, "has fewer than two transitions"))
  }

  for (held_out in transitions) {
    train <- risk_data[risk_data$transition != held_out, , drop = FALSE]
    test <- risk_data[risk_data$transition == held_out, , drop = FALSE]

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

    prediction_rows[[row_index]] <- data.frame(
      risk_set = risk,
      transition = held_out,
      outcome = as.integer(test$outcome),
      model_probability = model_probability,
      null_probability = null_probability,
      stringsAsFactors = FALSE
    )
    row_index <- row_index + 1

    fold_rows[[fold_index]] <- data.frame(
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
    fold_index <- fold_index + 1
  }
}

predictions <- do.call(rbind, prediction_rows)
folds <- do.call(rbind, fold_rows)

write.csv(predictions, prediction_path, row.names = FALSE)
write.csv(folds, fold_path, row.names = FALSE)
