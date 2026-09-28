args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 2) {
  stop("usage: Rscript examples/villavicencio_gain_loss_matched_audit.R INPUT.csv OUTPUT.csv [REPLICATES]")
}

input_path <- args[[1]]
output_path <- args[[2]]
replicates <- if (length(args) >= 3) as.integer(args[[3]]) else 100L
if (!is.finite(replicates) || replicates < 1) {
  stop("REPLICATES must be a positive integer")
}

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
drop_phenology_predictors <- setdiff(predictors, "phenological_overlap")

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
data$outcome <- as.integer(data$outcome)

auc <- function(y, probability) {
  positives <- sum(y == 1)
  negatives <- sum(y == 0)
  if (positives == 0 || negatives == 0) {
    return(NA_real_)
  }
  ranks <- rank(as.numeric(probability), ties.method = "average")
  (sum(ranks[y == 1]) - positives * (positives + 1) / 2) /
    (positives * negatives)
}

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

fit_auc <- function(train, test, model_predictors) {
  prepared <- prepare_fold(train, test)
  train <- prepared$train
  test <- prepared$test
  formula <- as.formula(
    paste("outcome ~", paste(model_predictors, collapse = " + "))
  )
  fit <- tryCatch(
    suppressWarnings(glm(formula, data = train, family = binomial())),
    error = function(e) NULL
  )
  if (is.null(fit) || !isTRUE(fit$converged) || any(!is.finite(coef(fit)))) {
    return(list(auc = NA_real_, converged = FALSE))
  }
  probability <- tryCatch(
    as.numeric(predict(fit, newdata = test, type = "response")),
    error = function(e) rep(NA_real_, nrow(test))
  )
  if (any(!is.finite(probability))) {
    return(list(auc = NA_real_, converged = FALSE))
  }
  list(auc = auc(test$outcome, probability), converged = TRUE)
}

balanced_sample <- function(train, per_class) {
  positive <- which(train$outcome == 1)
  negative <- which(train$outcome == 0)
  if (length(positive) < per_class || length(negative) < per_class) {
    stop("per_class exceeds available rows")
  }
  index <- c(
    sample(positive, per_class, replace = FALSE),
    sample(negative, per_class, replace = FALSE)
  )
  train[index, , drop = FALSE]
}

set.seed(20260928L)
rows <- list()
row_index <- 1L

for (scope_name in names(scopes)) {
  transitions <- scopes[[scope_name]]
  scope_data <- data[data$transition %in% transitions, , drop = FALSE]

  for (held_out in transitions) {
    train_gain <- scope_data[
      scope_data$transition != held_out & scope_data$risk_set == "gain",
      ,
      drop = FALSE
    ]
    train_loss <- scope_data[
      scope_data$transition != held_out & scope_data$risk_set == "loss",
      ,
      drop = FALSE
    ]
    test_gain <- scope_data[
      scope_data$transition == held_out & scope_data$risk_set == "gain",
      ,
      drop = FALSE
    ]
    test_loss <- scope_data[
      scope_data$transition == held_out & scope_data$risk_set == "loss",
      ,
      drop = FALSE
    ]

    class_counts <- c(
      sum(train_gain$outcome == 1),
      sum(train_gain$outcome == 0),
      sum(train_loss$outcome == 1),
      sum(train_loss$outcome == 0)
    )
    per_class <- min(class_counts)
    if (per_class < 1) {
      stop(paste(scope_name, held_out, "has an empty matched training class"))
    }
    if (length(unique(test_gain$outcome)) < 2 || length(unique(test_loss$outcome)) < 2) {
      stop(paste(scope_name, held_out, "has a degenerate held-out endpoint"))
    }

    for (replicate_id in seq_len(replicates)) {
      sampled_gain <- balanced_sample(train_gain, per_class)
      sampled_loss <- balanced_sample(train_loss, per_class)

      gain_full <- fit_auc(sampled_gain, test_gain, predictors)
      gain_drop <- fit_auc(sampled_gain, test_gain, drop_phenology_predictors)
      loss_full <- fit_auc(sampled_loss, test_loss, predictors)
      loss_drop <- fit_auc(sampled_loss, test_loss, drop_phenology_predictors)

      fits_ok <- all(c(
        gain_full$converged,
        gain_drop$converged,
        loss_full$converged,
        loss_drop$converged
      ))

      gain_phenology_delta <- gain_full$auc - gain_drop$auc
      loss_phenology_delta <- loss_full$auc - loss_drop$auc

      rows[[row_index]] <- data.frame(
        analysis_scope = scope_name,
        held_out_transition = held_out,
        replicate = replicate_id,
        matched_per_class = per_class,
        matched_training_n_per_endpoint = 2L * per_class,
        fits_ok = fits_ok,
        gain_full_auc = gain_full$auc,
        loss_full_auc = loss_full$auc,
        gain_minus_loss_auc = gain_full$auc - loss_full$auc,
        gain_drop_phenology_auc = gain_drop$auc,
        loss_drop_phenology_auc = loss_drop$auc,
        gain_phenology_auc_delta = gain_phenology_delta,
        loss_phenology_auc_delta = loss_phenology_delta,
        gain_minus_loss_phenology_auc_delta = (
          gain_phenology_delta - loss_phenology_delta
        ),
        stringsAsFactors = FALSE
      )
      row_index <- row_index + 1L
    }
  }
}

result <- do.call(rbind, rows)
write.csv(result, output_path, row.names = FALSE)
