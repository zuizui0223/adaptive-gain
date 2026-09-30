args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 3) {
  stop("usage: Rscript examples/dominguez2026_external_axis_cv.R INPUT.csv PREDICTIONS.csv FOLDS.csv")
}

input_path <- args[[1]]
prediction_path <- args[[2]]
fold_path <- args[[3]]

data <- read.csv(input_path, stringsAsFactors = FALSE, check.names = FALSE)

required <- c(
  "site",
  "risk_set",
  "outcome",
  "plant_phenology_days",
  "plant_abundance",
  "pollinator_otherplant_degree"
)
missing <- setdiff(required, names(data))
if (length(missing) > 0) {
  stop(paste("missing required columns:", paste(missing, collapse = ", ")))
}

model_sets <- list(
  primary_full = c("plant_phenology_days", "pollinator_otherplant_degree"),
  primary_plant_only = c("plant_phenology_days"),
  primary_pollinator_only = c("pollinator_otherplant_degree"),
  abundance_full = c("plant_abundance", "pollinator_otherplant_degree"),
  abundance_plant_only = c("plant_abundance"),
  abundance_pollinator_only = c("pollinator_otherplant_degree")
)

all_predictors <- c(
  "plant_phenology_days",
  "plant_abundance",
  "pollinator_otherplant_degree"
)

prepare_fold <- function(train, test) {
  for (name in all_predictors) {
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

sites <- sort(unique(data$site))
if (length(sites) < 2) {
  stop("need at least two sites for leave-one-site-out validation")
}

prediction_rows <- list()
fold_rows <- list()
prediction_index <- 1
fold_index <- 1

for (risk in c("gain", "loss")) {
  risk_data <- data[data$risk_set == risk, , drop = FALSE]

  for (held_out_site in sites) {
    train_raw <- risk_data[risk_data$site != held_out_site, , drop = FALSE]
    test_raw <- risk_data[risk_data$site == held_out_site, , drop = FALSE]
    if (nrow(test_raw) == 0) {
      stop(paste(risk, held_out_site, "has no held-out rows"))
    }
    if (length(unique(train_raw$outcome)) < 2) {
      stop(paste(risk, held_out_site, "training outcome is degenerate"))
    }

    prepared <- prepare_fold(train_raw, test_raw)
    train <- prepared$train
    test <- prepared$test
    null_probability <- clip_probability(
      rep(mean(train$outcome), nrow(test))
    )

    for (model_name in names(model_sets)) {
      model_predictors <- model_sets[[model_name]]
      formula <- as.formula(
        paste("outcome ~", paste(model_predictors, collapse = " + "))
      )
      fit <- suppressWarnings(
        glm(formula, data = train, family = binomial())
      )
      probability <- clip_probability(
        predict(fit, newdata = test, type = "response")
      )

      prediction_rows[[prediction_index]] <- data.frame(
        risk_set = risk,
        held_out_site = held_out_site,
        model = model_name,
        outcome = as.integer(test$outcome),
        model_probability = probability,
        null_probability = null_probability,
        stringsAsFactors = FALSE
      )
      prediction_index <- prediction_index + 1

      fold_rows[[fold_index]] <- data.frame(
        risk_set = risk,
        held_out_site = held_out_site,
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
