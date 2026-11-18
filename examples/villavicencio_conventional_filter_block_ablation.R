args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 3) {
  stop("usage: Rscript examples/villavicencio_conventional_filter_block_ablation.R INPUT.csv PREDICTIONS.csv FOLDS.csv")
}

input_path <- args[[1]]
prediction_path <- args[[2]]
fold_path <- args[[3]]

blocks <- list(
  phenology = c("phenological_overlap"),
  abundance = c("flower_abundance"),
  plant_morphology = c("corolla_length", "corolla_aperture", "height_mean"),
  pollinator_morphology = c(
    "body_length",
    "proboscis_length",
    "proboscis_width",
    "body_width",
    "body_thickness"
  )
)

predictors <- unique(unlist(blocks, use.names = FALSE))

scopes <- list(
  strict_core_2008_2011 = c("2008->2009", "2009->2010", "2010->2011"),
  near_core_2007_2011 = c("2007->2008", "2008->2009", "2009->2010", "2010->2011"),
  all_annual_2006_2011 = c("2006->2007", "2007->2008", "2008->2009", "2009->2010", "2010->2011")
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

fit_predict <- function(train, test, names) {
  formula <- as.formula(
    paste("outcome ~", if (length(names) == 0) "1" else paste(names, collapse = " + "))
  )
  fit <- suppressWarnings(glm(formula, data = train, family = binomial()))
  list(
    probability = clip_probability(predict(fit, newdata = test, type = "response")),
    converged = isTRUE(fit$converged),
    coefficient_count = length(coef(fit)),
    finite_coefficient_count = sum(is.finite(coef(fit)))
  )
}

prediction_rows <- list()
fold_rows <- list()
prediction_index <- 1
fold_index <- 1

for (scope_name in names(scopes)) {
  scope_transitions <- scopes[[scope_name]]
  scope_data <- data[data$transition %in% scope_transitions, , drop = FALSE]

  for (risk in c("gain", "loss")) {
    risk_data <- scope_data[scope_data$risk_set == risk, , drop = FALSE]
    transitions <- scope_transitions[scope_transitions %in% unique(risk_data$transition)]

    if (length(transitions) < 2) {
      stop(paste("scope", scope_name, "risk set", risk, "has fewer than two transitions"))
    }

    for (held_out in transitions) {
      train <- risk_data[risk_data$transition != held_out, , drop = FALSE]
      test <- risk_data[risk_data$transition == held_out, , drop = FALSE]
      prepared <- prepare_fold(train, test)
      train <- prepared$train
      test <- prepared$test

      model_sets <- c(list(full = predictors), lapply(blocks, function(block) setdiff(predictors, block)))
      names(model_sets) <- c("full", paste0("drop_", names(blocks)))

      for (model_name in names(model_sets)) {
        fitted <- fit_predict(train, test, model_sets[[model_name]])

        prediction_rows[[prediction_index]] <- data.frame(
          analysis_scope = scope_name,
          risk_set = risk,
          transition = held_out,
          model = model_name,
          outcome = as.integer(test$outcome),
          probability = fitted$probability,
          stringsAsFactors = FALSE
        )
        prediction_index <- prediction_index + 1

        fold_rows[[fold_index]] <- data.frame(
          analysis_scope = scope_name,
          risk_set = risk,
          held_out_transition = held_out,
          model = model_name,
          train_n = nrow(train),
          test_n = nrow(test),
          train_events = sum(train$outcome == 1),
          test_events = sum(test$outcome == 1),
          converged = fitted$converged,
          coefficient_count = fitted$coefficient_count,
          finite_coefficient_count = fitted$finite_coefficient_count,
          stringsAsFactors = FALSE
        )
        fold_index <- fold_index + 1
      }
    }
  }
}

write.csv(do.call(rbind, prediction_rows), prediction_path, row.names = FALSE)
write.csv(do.call(rbind, fold_rows), fold_path, row.names = FALSE)
