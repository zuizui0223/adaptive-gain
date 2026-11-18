args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 4) {
  stop("usage: Rscript examples/villavicencio_subseason_effort_only_cv.R DYADS.csv PLANT_EFFORT.csv PREDICTIONS.csv FOLDS.csv")
}

dyad_path <- args[[1]]
effort_path <- args[[2]]
prediction_path <- args[[3]]
fold_path <- args[[4]]

dyads <- read.csv(dyad_path, stringsAsFactors = FALSE, check.names = FALSE)
effort <- read.csv(effort_path, stringsAsFactors = FALSE, check.names = FALSE)

scopes <- list(
  strict_dated_core_2008_2010 = c(
    "2008_early->2008_mid",
    "2008_mid->2008_late",
    "2009_early->2009_mid",
    "2009_mid->2009_late",
    "2010_early->2010_mid",
    "2010_mid->2010_late"
  ),
  core_sites_2008_2011 = c(
    "2008_early->2008_mid",
    "2008_mid->2008_late",
    "2009_early->2009_mid",
    "2009_mid->2009_late",
    "2010_early->2010_mid",
    "2010_mid->2010_late",
    "2011_early->2011_mid",
    "2011_mid->2011_late"
  ),
  all_2007_2011 = c(
    "2007_early->2007_mid",
    "2007_mid->2007_late",
    "2008_early->2008_mid",
    "2008_mid->2008_late",
    "2009_early->2009_mid",
    "2009_mid->2009_late",
    "2010_early->2010_mid",
    "2010_mid->2010_late",
    "2011_early->2011_mid",
    "2011_mid->2011_late"
  )
)

dyads <- dyads[dyads$role == "primary", , drop = FALSE]
dyads$transition <- paste(dyads$previous_period, dyads$current_period, sep = "->")
dyads$risk_set <- ifelse(
  tolower(as.character(dyads$previous_link)) %in% c("true", "1", "yes", "y"),
  "loss",
  "gain"
)
dyads$outcome <- ifelse(
  dyads$risk_set == "loss",
  as.integer(!(tolower(as.character(dyads$current_link)) %in% c("true", "1", "yes", "y"))),
  as.integer(tolower(as.character(dyads$current_link)) %in% c("true", "1", "yes", "y"))
)

prev_effort <- effort
names(prev_effort) <- c("previous_period", "plant", "previous_censuses", "previous_minutes")
curr_effort <- effort
names(curr_effort) <- c("current_period", "plant", "current_censuses", "current_minutes")

dyads <- merge(
  dyads,
  prev_effort,
  by = c("previous_period", "plant"),
  all.x = TRUE,
  sort = FALSE
)
dyads <- merge(
  dyads,
  curr_effort,
  by = c("current_period", "plant"),
  all.x = TRUE,
  sort = FALSE
)

if (any(is.na(dyads$previous_censuses)) || any(is.na(dyads$current_censuses))) {
  stop("at least one eligible dyad lacks focal-plant census effort")
}

predictors <- c("previous_censuses", "current_censuses")

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

clip_probability <- function(value) {
  pmin(pmax(as.numeric(value), 1e-8), 1 - 1e-8)
}

prediction_rows <- list()
fold_rows <- list()
pi <- 1
fi <- 1

for (scope_name in names(scopes)) {
  scope_transitions <- scopes[[scope_name]]
  scope_data <- dyads[dyads$transition %in% scope_transitions, , drop = FALSE]

  for (risk in c("gain", "loss")) {
    risk_data <- scope_data[scope_data$risk_set == risk, , drop = FALSE]
    transitions <- scope_transitions[
      scope_transitions %in% unique(risk_data$transition)
    ]

    for (held_out in transitions) {
      train_raw <- risk_data[risk_data$transition != held_out, , drop = FALSE]
      test_raw <- risk_data[risk_data$transition == held_out, , drop = FALSE]

      # A held-out fold must contain both endpoint classes to contribute AUC,
      # but the strict/core scopes were chosen to avoid degenerate folds.
      if (length(unique(test_raw$outcome)) < 2) {
        stop(paste(scope_name, risk, held_out, "held-out outcome is degenerate"))
      }
      if (length(unique(train_raw$outcome)) < 2) {
        stop(paste(scope_name, risk, held_out, "training outcome is degenerate"))
      }

      prepared <- prepare_fold(train_raw, test_raw)
      train <- prepared$train
      test <- prepared$test

      fit <- suppressWarnings(
        glm(
          outcome ~ previous_censuses + current_censuses,
          data = train,
          family = binomial()
        )
      )
      probability <- clip_probability(
        predict(fit, newdata = test, type = "response")
      )
      null_probability <- clip_probability(
        rep(mean(train$outcome), nrow(test))
      )

      prediction_rows[[pi]] <- data.frame(
        analysis_scope = scope_name,
        risk_set = risk,
        transition = held_out,
        outcome = as.integer(test$outcome),
        model_probability = probability,
        null_probability = null_probability,
        stringsAsFactors = FALSE
      )
      pi <- pi + 1

      fold_rows[[fi]] <- data.frame(
        analysis_scope = scope_name,
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
      fi <- fi + 1
    }
  }
}

write.csv(do.call(rbind, prediction_rows), prediction_path, row.names = FALSE)
write.csv(do.call(rbind, fold_rows), fold_path, row.names = FALSE)
