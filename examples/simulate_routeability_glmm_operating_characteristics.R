args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 3) {
  stop(
    "usage: Rscript examples/simulate_routeability_glmm_operating_characteristics.R ",
    "SCENARIOS.csv SUMMARY.csv REPLICATES.csv"
  )
}

scenario_path <- args[[1]]
summary_path <- args[[2]]
replicate_path <- args[[3]]

if (!requireNamespace("lme4", quietly = TRUE)) {
  stop(
    "R package 'lme4' is required for final GLMM operating-characteristic simulation"
  )
}

required_columns <- c(
  "scenario_id",
  "simulations",
  "individuals_per_cell",
  "trials_per_individual",
  "colony_count",
  "individual_sd_logit",
  "colony_sd_logit",
  "dropout_fraction",
  "timeout_fraction",
  "alpha_two_sided",
  "seed",
  "sesoi_provenance",
  "expected_h1_delta_b2",
  "expected_h2_localization",
  "p_KF_B1", "p_KC_B1", "p_RF_B1", "p_RC_B1",
  "p_KF_B2", "p_KC_B2", "p_RF_B2", "p_RC_B2",
  "p_KF_B3", "p_KC_B3", "p_RF_B3", "p_RC_B3"
)

scenarios <- read.csv(
  scenario_path,
  stringsAsFactors = FALSE,
  check.names = FALSE
)
missing <- setdiff(required_columns, names(scenarios))
if (length(missing) > 0) {
  stop(paste("scenario CSV missing required columns:", paste(missing, collapse = ", ")))
}
if (nrow(scenarios) == 0) {
  stop("scenario CSV is empty")
}
if (anyDuplicated(scenarios$scenario_id)) {
  stop("scenario_id values must be unique")
}

inv_logit <- function(x) {
  1 / (1 + exp(-x))
}

safe_logit <- function(p) {
  qlogis(pmin(pmax(p, 1e-8), 1 - 1e-8))
}

cell_probability <- function(row, architecture, access_mode, budget) {
  architecture_code <- if (architecture == "routeable") "R" else "K"
  access_code <- if (access_mode == "contingent") "C" else "F"
  column <- paste0("p_", architecture_code, access_code, "_B", budget)
  as.numeric(row[[column]])
}

build_cell_grid <- function() {
  grid <- expand.grid(
    architecture = c("bypass_control", "routeable"),
    access_mode = c("fixed", "contingent"),
    budget = c("B1", "B2", "B3"),
    KEEP.OUT.ATTRS = FALSE,
    stringsAsFactors = FALSE
  )
  grid$architecture <- factor(
    grid$architecture,
    levels = c("bypass_control", "routeable")
  )
  grid$access_mode <- factor(
    grid$access_mode,
    levels = c("fixed", "contingent")
  )
  grid$budget <- factor(
    grid$budget,
    levels = c("B1", "B2", "B3")
  )
  grid
}

delta_weights <- function(grid, budget_label) {
  weights <- rep(0, nrow(grid))
  weights[
    grid$architecture == "routeable" &
      grid$access_mode == "contingent" &
      grid$budget == budget_label
  ] <- 1
  weights[
    grid$architecture == "routeable" &
      grid$access_mode == "fixed" &
      grid$budget == budget_label
  ] <- -1
  weights[
    grid$architecture == "bypass_control" &
      grid$access_mode == "contingent" &
      grid$budget == budget_label
  ] <- -1
  weights[
    grid$architecture == "bypass_control" &
      grid$access_mode == "fixed" &
      grid$budget == budget_label
  ] <- 1
  weights
}

contrast_from_fit <- function(fit, grid, weights) {
  fixed_formula <- ~ architecture * access_mode * budget
  x <- model.matrix(fixed_formula, data = grid)
  beta <- lme4::fixef(fit)
  x <- x[, names(beta), drop = FALSE]
  vc <- as.matrix(vcov(fit))
  vc <- vc[names(beta), names(beta), drop = FALSE]

  eta <- as.vector(x %*% beta)
  probability <- inv_logit(eta)
  gradient_rows <- x * as.vector(probability * (1 - probability))

  estimate <- sum(weights * probability)
  gradient <- colSums(gradient_rows * weights)
  variance <- as.numeric(t(gradient) %*% vc %*% gradient)
  if (!is.finite(variance) || variance <= 0) {
    return(
      list(
        estimate = estimate,
        se = NA_real_,
        z = NA_real_,
        p_value = NA_real_
      )
    )
  }
  se <- sqrt(variance)
  z <- estimate / se
  p_value <- 2 * pnorm(-abs(z))
  list(
    estimate = estimate,
    se = se,
    z = z,
    p_value = p_value
  )
}

simulate_one <- function(row, simulation_index) {
  simulations <- as.integer(row$simulations)
  individuals_per_cell <- as.integer(row$individuals_per_cell)
  trials_per_individual <- as.integer(row$trials_per_individual)
  colony_count <- as.integer(row$colony_count)
  individual_sd <- as.numeric(row$individual_sd_logit)
  colony_sd <- as.numeric(row$colony_sd_logit)
  dropout_fraction <- as.numeric(row$dropout_fraction)
  timeout_fraction <- as.numeric(row$timeout_fraction)
  alpha <- as.numeric(row$alpha_two_sided)

  if (simulations < 1 || individuals_per_cell < 1 ||
      trials_per_individual < 1 || colony_count < 1) {
    stop("scenario integer counts must be positive")
  }
  if (individual_sd < 0 || colony_sd < 0) {
    stop("random-intercept SDs must be non-negative")
  }
  if (dropout_fraction < 0 || dropout_fraction >= 1 ||
      timeout_fraction < 0 || timeout_fraction >= 1) {
    stop("dropout and timeout fractions must lie in [0,1)")
  }
  if (alpha <= 0 || alpha >= 1) {
    stop("alpha_two_sided must lie in (0,1)")
  }

  set.seed(as.integer(row$seed) + simulation_index - 1L)

  colony_effect <- rnorm(colony_count, mean = 0, sd = colony_sd)
  rows <- list()
  row_index <- 1L
  randomized_individual_count <- 0L
  retained_individual_count <- 0L
  timeout_count <- 0L

  for (budget in 1:3) {
    for (architecture in c("bypass_control", "routeable")) {
      for (access_mode in c("fixed", "contingent")) {
        p_primary <- cell_probability(
          row,
          architecture = architecture,
          access_mode = access_mode,
          budget = budget
        )
        if (!is.finite(p_primary) || p_primary <= 0 || p_primary >= 1) {
          stop("cell primary-success probabilities must lie in (0,1)")
        }
        if (p_primary > 1 - timeout_fraction + 1e-12) {
          stop(
            "cell primary-success probability exceeds 1-timeout_fraction"
          )
        }
        p_correct_given_response <- p_primary / (1 - timeout_fraction)
        base_logit <- safe_logit(p_correct_given_response)

        for (individual_index in seq_len(individuals_per_cell)) {
          randomized_individual_count <- randomized_individual_count + 1L
          individual_id <- paste(
            row$scenario_id,
            paste0("B", budget),
            architecture,
            access_mode,
            paste0("i", individual_index),
            sep = "__"
          )
          colony_index <- ((individual_index - 1L) %% colony_count) + 1L
          colony_id <- paste0("c", colony_index)

          if (runif(1) < dropout_fraction) {
            next
          }
          retained_individual_count <- retained_individual_count + 1L
          individual_effect <- rnorm(1, mean = 0, sd = individual_sd)
          conditional_correct <- inv_logit(
            base_logit + individual_effect + colony_effect[colony_index]
          )

          for (trial_index in seq_len(trials_per_individual)) {
            timeout <- rbinom(1, size = 1, prob = timeout_fraction)
            if (timeout == 1) {
              success <- 0L
              timeout_count <- timeout_count + 1L
            } else {
              success <- rbinom(
                1,
                size = 1,
                prob = conditional_correct
              )
            }

            rows[[row_index]] <- data.frame(
              success = success,
              timeout = timeout,
              architecture = architecture,
              access_mode = access_mode,
              budget = paste0("B", budget),
              individual = individual_id,
              colony = colony_id,
              stringsAsFactors = FALSE
            )
            row_index <- row_index + 1L
          }
        }
      }
    }
  }

  if (length(rows) == 0) {
    return(
      data.frame(
        scenario_id = row$scenario_id,
        simulation_index = simulation_index,
        fit_success = FALSE,
        converged = FALSE,
        singular = NA,
        h1_estimate = NA,
        h1_se = NA,
        h1_p_value = NA,
        h1_pass = FALSE,
        h2_estimate = NA,
        h2_se = NA,
        h2_p_value = NA,
        h2_raw_pass = FALSE,
        h2_hierarchical_pass = FALSE,
        randomized_individual_count = randomized_individual_count,
        retained_individual_count = retained_individual_count,
        observed_trial_count = 0,
        timeout_fraction_observed = NA,
        fit_error = "all randomized individuals dropped out",
        stringsAsFactors = FALSE
      )
    )
  }

  data <- do.call(rbind, rows)
  data$architecture <- factor(
    data$architecture,
    levels = c("bypass_control", "routeable")
  )
  data$access_mode <- factor(
    data$access_mode,
    levels = c("fixed", "contingent")
  )
  data$budget <- factor(
    data$budget,
    levels = c("B1", "B2", "B3")
  )
  data$individual <- factor(data$individual)
  data$colony <- factor(data$colony)

  observed_cells <- interaction(
    data$architecture,
    data$access_mode,
    data$budget,
    drop = TRUE
  )
  if (length(unique(observed_cells)) < 12) {
    return(
      data.frame(
        scenario_id = row$scenario_id,
        simulation_index = simulation_index,
        fit_success = FALSE,
        converged = FALSE,
        singular = NA,
        h1_estimate = NA,
        h1_se = NA,
        h1_p_value = NA,
        h1_pass = FALSE,
        h2_estimate = NA,
        h2_se = NA,
        h2_p_value = NA,
        h2_raw_pass = FALSE,
        h2_hierarchical_pass = FALSE,
        randomized_individual_count = randomized_individual_count,
        retained_individual_count = retained_individual_count,
        observed_trial_count = nrow(data),
        timeout_fraction_observed = mean(data$timeout),
        fit_error = "one or more randomized cells lost all retained individuals",
        stringsAsFactors = FALSE
      )
    )
  }

  formula <- if (colony_count > 1) {
    success ~ architecture * access_mode * budget +
      (1 | individual) + (1 | colony)
  } else {
    success ~ architecture * access_mode * budget +
      (1 | individual)
  }

  fit_error <- NULL
  fit <- tryCatch(
    suppressWarnings(
      lme4::glmer(
        formula,
        data = data,
        family = binomial(),
        nAGQ = 1,
        control = lme4::glmerControl(
          optimizer = "bobyqa",
          calc.derivs = TRUE
        )
      )
    ),
    error = function(error) {
      fit_error <<- conditionMessage(error)
      NULL
    }
  )

  if (is.null(fit)) {
    return(
      data.frame(
        scenario_id = row$scenario_id,
        simulation_index = simulation_index,
        fit_success = FALSE,
        converged = FALSE,
        singular = NA,
        h1_estimate = NA,
        h1_se = NA,
        h1_p_value = NA,
        h1_pass = FALSE,
        h2_estimate = NA,
        h2_se = NA,
        h2_p_value = NA,
        h2_raw_pass = FALSE,
        h2_hierarchical_pass = FALSE,
        randomized_individual_count = randomized_individual_count,
        retained_individual_count = retained_individual_count,
        observed_trial_count = nrow(data),
        timeout_fraction_observed = mean(data$timeout),
        fit_error = fit_error,
        stringsAsFactors = FALSE
      )
    )
  }

  convergence_messages <- fit@optinfo$conv$lme4$messages
  converged <- is.null(convergence_messages)
  singular <- lme4::isSingular(fit, tol = 1e-4)

  grid <- build_cell_grid()
  w_b1 <- delta_weights(grid, "B1")
  w_b2 <- delta_weights(grid, "B2")
  w_b3 <- delta_weights(grid, "B3")
  w_h2 <- w_b2 - 0.5 * (w_b1 + w_b3)

  h1 <- tryCatch(
    contrast_from_fit(fit, grid, w_b2),
    error = function(error) {
      fit_error <<- paste(
        "contrast failure:",
        conditionMessage(error)
      )
      NULL
    }
  )
  h2 <- tryCatch(
    contrast_from_fit(fit, grid, w_h2),
    error = function(error) {
      fit_error <<- paste(
        "contrast failure:",
        conditionMessage(error)
      )
      NULL
    }
  )

  if (is.null(h1) || is.null(h2)) {
    return(
      data.frame(
        scenario_id = row$scenario_id,
        simulation_index = simulation_index,
        fit_success = FALSE,
        converged = converged,
        singular = singular,
        h1_estimate = NA,
        h1_se = NA,
        h1_p_value = NA,
        h1_pass = FALSE,
        h2_estimate = NA,
        h2_se = NA,
        h2_p_value = NA,
        h2_raw_pass = FALSE,
        h2_hierarchical_pass = FALSE,
        randomized_individual_count = randomized_individual_count,
        retained_individual_count = retained_individual_count,
        observed_trial_count = nrow(data),
        timeout_fraction_observed = mean(data$timeout),
        fit_error = fit_error,
        stringsAsFactors = FALSE
      )
    )
  }

  h1_pass <- (
    is.finite(h1$p_value) &&
      h1$p_value < alpha &&
      is.finite(h1$estimate) &&
      h1$estimate > 0
  )
  h2_raw_pass <- (
    is.finite(h2$p_value) &&
      h2$p_value < alpha &&
      is.finite(h2$estimate) &&
      h2$estimate > 0
  )

  data.frame(
    scenario_id = row$scenario_id,
    simulation_index = simulation_index,
    fit_success = TRUE,
    converged = converged,
    singular = singular,
    h1_estimate = h1$estimate,
    h1_se = h1$se,
    h1_p_value = h1$p_value,
    h1_pass = h1_pass,
    h2_estimate = h2$estimate,
    h2_se = h2$se,
    h2_p_value = h2$p_value,
    h2_raw_pass = h2_raw_pass,
    h2_hierarchical_pass = h1_pass && h2_raw_pass,
    randomized_individual_count = randomized_individual_count,
    retained_individual_count = retained_individual_count,
    observed_trial_count = nrow(data),
    timeout_fraction_observed = mean(data$timeout),
    fit_error = if (is.null(fit_error)) "" else fit_error,
    stringsAsFactors = FALSE
  )
}

replicate_rows <- list()
replicate_index <- 1L

for (scenario_index in seq_len(nrow(scenarios))) {
  row <- scenarios[scenario_index, , drop = FALSE]
  simulations <- as.integer(row$simulations)

  for (simulation_index in seq_len(simulations)) {
    replicate_rows[[replicate_index]] <- simulate_one(
      row,
      simulation_index = simulation_index
    )
    replicate_index <- replicate_index + 1L
  }
}

replicates <- do.call(rbind, replicate_rows)
write.csv(replicates, replicate_path, row.names = FALSE)

summary_rows <- list()
summary_index <- 1L

for (scenario_index in seq_len(nrow(scenarios))) {
  row <- scenarios[scenario_index, , drop = FALSE]
  observed <- replicates[
    replicates$scenario_id == row$scenario_id,
    ,
    drop = FALSE
  ]
  fit_success <- observed$fit_success %in% TRUE
  converged <- observed$converged %in% TRUE
  singular <- observed$singular %in% TRUE

  mean_or_na <- function(values, keep) {
    values <- values[keep & is.finite(values)]
    if (length(values) == 0) {
      return(NA_real_)
    }
    mean(values)
  }

  summary_rows[[summary_index]] <- data.frame(
    scenario_id = row$scenario_id,
    simulations = nrow(observed),
    fit_success_fraction = mean(fit_success),
    converged_fraction = mean(converged),
    singular_fraction = mean(singular, na.rm = TRUE),
    h1_directional_rejection_fraction = mean(observed$h1_pass %in% TRUE),
    h2_raw_directional_rejection_fraction = mean(
      observed$h2_raw_pass %in% TRUE
    ),
    h2_hierarchical_pass_fraction = mean(
      observed$h2_hierarchical_pass %in% TRUE
    ),
    mean_h1_estimate_fit_success = mean_or_na(
      observed$h1_estimate,
      fit_success
    ),
    mean_h2_estimate_fit_success = mean_or_na(
      observed$h2_estimate,
      fit_success
    ),
    expected_h1_delta_b2 = as.numeric(row$expected_h1_delta_b2),
    expected_h2_localization = as.numeric(row$expected_h2_localization),
    mean_retained_individuals = mean(observed$retained_individual_count),
    mean_observed_trials = mean(observed$observed_trial_count),
    mean_timeout_fraction_observed = mean(
      observed$timeout_fraction_observed,
      na.rm = TRUE
    ),
    stringsAsFactors = FALSE
  )
  summary_index <- summary_index + 1L
}

summary <- do.call(rbind, summary_rows)
write.csv(summary, summary_path, row.names = FALSE)
