args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 3) {
  stop("usage: Rscript examples/dominguez2026_measurement_mapping_sensitivity.R INPUT.csv PREDICTIONS.csv FOLDS.csv")
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
  "published_pollinator_abundance",
  "published_pollinator_phenology"
)
missing <- setdiff(required, names(data))
if (length(missing) > 0) {
  stop(paste("missing required columns:", paste(missing, collapse = ", ")))
}

model_sets <- list(
  pheno_pollabund_full = c("plant_phenology_days", "published_pollinator_abundance"),
  pheno_pollabund_plant_only = c("plant_phenology_days"),
  pheno_pollabund_poll_only = c("published_pollinator_abundance"),
  pheno_pollpheno_full = c("plant_phenology_days", "published_pollinator_phenology"),
  pheno_pollpheno_plant_only = c("plant_phenology_days"),
  pheno_pollpheno_poll_only = c("published_pollinator_phenology"),
  abund_pollabund_full = c("plant_abundance", "published_pollinator_abundance"),
  abund_pollabund_plant_only = c("plant_abundance"),
  abund_pollabund_poll_only = c("published_pollinator_abundance")
)

all_predictors <- c(
  "plant_phenology_days",
  "plant_abundance",
  "published_pollinator_abundance",
  "published_pollinator_phenology"
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
prediction_rows <- list()
fold_rows <- list()
pi <- 1
fi <- 1

for (risk in c("gain", "loss")) {
  risk_data <- data[data$risk_set == risk, , drop = FALSE]

  for (held_out_site in sites) {
    train_raw <- risk_data[risk_data$site != held_out_site, , drop = FALSE]
    test_raw <- risk_data[risk_data$site == held_out_site, , drop = FALSE]
    prepared <- prepare_fold(train_raw, test_raw)
    train <- prepared$train
    test <- prepared$test

    for (model_name in names(model_sets)) {
      predictors <- model_sets[[model_name]]
      formula <- as.formula(
        paste("outcome ~", paste(predictors, collapse = " + "))
      )
      fit <- suppressWarnings(
        glm(formula, data = train, family = binomial())
      )
      probability <- clip_probability(
        predict(fit, newdata = test, type = "response")
      )

      prediction_rows[[pi]] <- data.frame(
        risk_set = risk,
        held_out_site = held_out_site,
        model = model_name,
        outcome = as.integer(test$outcome),
        probability = probability,
        stringsAsFactors = FALSE
      )
      pi <- pi + 1

      fold_rows[[fi]] <- data.frame(
        risk_set = risk,
        held_out_site = held_out_site,
        model = model_name,
        converged = isTRUE(fit$converged),
        coefficient_count = length(coef(fit)),
        finite_coefficient_count = sum(is.finite(coef(fit))),
        stringsAsFactors = FALSE
      )
      fi <- fi + 1
    }
  }
}

write.csv(do.call(rbind, prediction_rows), prediction_path, row.names = FALSE)
write.csv(do.call(rbind, fold_rows), fold_path, row.names = FALSE)
