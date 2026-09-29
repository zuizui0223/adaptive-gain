args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 3) {
  stop("usage: Rscript examples/villavicencio_two_season_detection_fit.R INPUT.csv FITS.csv POSTERIORS.csv")
}

input_path <- args[[1]]
fit_path <- args[[2]]
posterior_path <- args[[3]]

data <- read.csv(input_path, stringsAsFactors = FALSE, check.names = FALSE)

required <- c(
  "transition",
  "previous_success_censuses",
  "previous_trials",
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
  stop("transition set disagrees with frozen detection gate")
}

inv_logit <- function(x) {
  1 / (1 + exp(-x))
}

log_sum_exp <- function(values) {
  finite <- values[is.finite(values)]
  if (length(finite) == 0) {
    return(-Inf)
  }
  m <- max(finite)
  m + log(sum(exp(finite - m)))
}

row_log_terms <- function(theta, y1, n1, y2, n2) {
  psi <- inv_logit(theta[[1]])
  gamma <- inv_logit(theta[[2]])
  epsilon <- inv_logit(theta[[3]])
  p1 <- inv_logit(theta[[4]])
  p2 <- inv_logit(theta[[5]])

  state_logs <- c(
    log1p(-psi) + log1p(-gamma),
    log1p(-psi) + log(gamma),
    log(psi) + log(epsilon),
    log(psi) + log1p(-epsilon)
  )

  obs1_z0 <- if (y1 == 0) 0 else -Inf
  obs2_z0 <- if (y2 == 0) 0 else -Inf
  obs1_z1 <- dbinom(y1, size = n1, prob = p1, log = TRUE)
  obs2_z1 <- dbinom(y2, size = n2, prob = p2, log = TRUE)

  c(
    state_logs[[1]] + obs1_z0 + obs2_z0,
    state_logs[[2]] + obs1_z0 + obs2_z1,
    state_logs[[3]] + obs1_z1 + obs2_z0,
    state_logs[[4]] + obs1_z1 + obs2_z1
  )
}

negative_log_likelihood <- function(theta, frame) {
  total <- 0
  for (i in seq_len(nrow(frame))) {
    terms <- row_log_terms(
      theta,
      frame$previous_success_censuses[[i]],
      frame$previous_trials[[i]],
      frame$current_success_censuses[[i]],
      frame$current_trials[[i]]
    )
    value <- log_sum_exp(terms)
    if (!is.finite(value)) {
      return(1e100)
    }
    total <- total - value
  }
  total
}

posterior_probs <- function(theta, frame) {
  out <- matrix(NA_real_, nrow = nrow(frame), ncol = 4)
  colnames(out) <- c("p00", "p01", "p10", "p11")
  for (i in seq_len(nrow(frame))) {
    terms <- row_log_terms(
      theta,
      frame$previous_success_censuses[[i]],
      frame$previous_trials[[i]],
      frame$current_success_censuses[[i]],
      frame$current_trials[[i]]
    )
    norm <- log_sum_exp(terms)
    out[i, ] <- exp(terms - norm)
  }
  out
}

start_probabilities <- list(
  c(.10, .05, .10, .03, .03),
  c(.20, .10, .20, .05, .05),
  c(.30, .15, .30, .08, .08),
  c(.40, .20, .40, .12, .12),
  c(.50, .30, .30, .05, .15),
  c(.50, .30, .30, .15, .05),
  c(.60, .10, .50, .08, .20),
  c(.60, .50, .10, .20, .08),
  c(.70, .20, .50, .15, .15),
  c(.30, .50, .20, .20, .20),
  c(.80, .05, .60, .03, .20),
  c(.20, .60, .05, .20, .03)
)

fit_rows <- list()
posterior_rows <- list()
fit_index <- 1
posterior_index <- 1

for (transition in transitions) {
  frame <- data[data$transition == transition, , drop = FALSE]
  if (nrow(frame) < 1) {
    stop(paste("empty transition", transition))
  }

  optim_results <- list()
  for (start_index in seq_along(start_probabilities)) {
    start <- qlogis(start_probabilities[[start_index]])
    fit <- tryCatch(
      optim(
        par = start,
        fn = negative_log_likelihood,
        frame = frame,
        method = "L-BFGS-B",
        lower = rep(-8, 5),
        upper = rep(8, 5),
        control = list(maxit = 5000, factr = 1e7)
      ),
      error = function(e) NULL
    )
    if (!is.null(fit) && is.finite(fit$value)) {
      optim_results[[length(optim_results) + 1]] <- list(
        start_index = start_index,
        fit = fit
      )
    }
  }

  if (length(optim_results) == 0) {
    stop(paste("no finite optimization result for", transition))
  }

  values <- vapply(
    optim_results,
    function(x) x$fit$value,
    numeric(1)
  )
  best_index <- which.min(values)
  best <- optim_results[[best_index]]$fit
  best_theta <- best$par

  # Recompute numerical Hessian at the selected optimum with unconstrained BFGS
  # initialized exactly at the bounded solution. If BFGS cannot improve, its
  # Hessian still supplies the local curvature diagnostic.
  hessian_fit <- tryCatch(
    optim(
      par = best_theta,
      fn = negative_log_likelihood,
      frame = frame,
      method = "BFGS",
      control = list(maxit = 1),
      hessian = TRUE
    ),
    error = function(e) NULL
  )

  hessian_ok <- FALSE
  finite_se <- FALSE
  min_hessian_eigenvalue <- NA_real_
  max_hessian_eigenvalue <- NA_real_
  hessian_condition_number <- NA_real_
  se_values <- rep(NA_real_, 5)

  if (!is.null(hessian_fit) && all(is.finite(hessian_fit$hessian))) {
    hessian <- (hessian_fit$hessian + t(hessian_fit$hessian)) / 2
    eigenvalues <- tryCatch(
      eigen(hessian, symmetric = TRUE, only.values = TRUE)$values,
      error = function(e) rep(NA_real_, 5)
    )
    if (all(is.finite(eigenvalues))) {
      min_hessian_eigenvalue <- min(eigenvalues)
      max_hessian_eigenvalue <- max(eigenvalues)
      hessian_ok <- min_hessian_eigenvalue > 1e-8
      if (hessian_ok) {
        inverse <- tryCatch(solve(hessian), error = function(e) NULL)
        if (!is.null(inverse)) {
          diagonal <- diag(inverse)
          if (all(is.finite(diagonal)) && all(diagonal >= 0)) {
            se_values <- sqrt(diagonal)
            finite_se <- all(is.finite(se_values))
          }
        }
        hessian_condition_number <- (
          max_hessian_eigenvalue / min_hessian_eigenvalue
        )
      }
    }
  }

  probs <- inv_logit(best_theta)
  names(probs) <- c(
    "psi",
    "gamma",
    "epsilon",
    "p_previous",
    "p_current"
  )

  nll_range <- max(values) - min(values)
  optim_converged <- best$convergence == 0
  all_starts_converged <- all(vapply(
    optim_results,
    function(x) x$fit$convergence == 0,
    logical(1)
  ))
  detection_interior <- (
    probs[["p_previous"]] > 0.01
    && probs[["p_previous"]] < 0.99
    && probs[["p_current"]] > 0.01
    && probs[["p_current"]] < 0.99
  )

  identified <- (
    optim_converged
    && all_starts_converged
    && nll_range <= 1e-6
    && hessian_ok
    && finite_se
    && detection_interior
  )

  posterior <- posterior_probs(best_theta, frame)

  observed_previous <- frame$previous_success_censuses > 0
  observed_current <- frame$current_success_censuses > 0
  observed_state <- ifelse(
    observed_previous,
    ifelse(observed_current, "stable_present", "loss"),
    ifelse(observed_current, "gain", "stable_absent")
  )

  for (i in seq_len(nrow(frame))) {
    posterior_rows[[posterior_index]] <- data.frame(
      transition = transition,
      plant = frame$plant[[i]],
      pollinator = frame$pollinator[[i]],
      observed_state = observed_state[[i]],
      previous_success_censuses = frame$previous_success_censuses[[i]],
      previous_trials = frame$previous_trials[[i]],
      current_success_censuses = frame$current_success_censuses[[i]],
      current_trials = frame$current_trials[[i]],
      p00 = posterior[i, "p00"],
      p01 = posterior[i, "p01"],
      p10 = posterior[i, "p10"],
      p11 = posterior[i, "p11"],
      stringsAsFactors = FALSE
    )
    posterior_index <- posterior_index + 1
  }

  observed_gain <- observed_state == "gain"
  observed_loss <- observed_state == "loss"

  fit_rows[[fit_index]] <- data.frame(
    transition = transition,
    n_rows = nrow(frame),
    optim_result_count = length(optim_results),
    best_start_index = optim_results[[best_index]]$start_index,
    best_nll = min(values),
    multi_start_nll_range = nll_range,
    best_convergence = best$convergence,
    all_starts_converged = all_starts_converged,
    hessian_positive_definite = hessian_ok,
    min_hessian_eigenvalue = min_hessian_eigenvalue,
    max_hessian_eigenvalue = max_hessian_eigenvalue,
    hessian_condition_number = hessian_condition_number,
    finite_logit_standard_errors = finite_se,
    psi = probs[["psi"]],
    gamma = probs[["gamma"]],
    epsilon = probs[["epsilon"]],
    p_previous = probs[["p_previous"]],
    p_current = probs[["p_current"]],
    se_logit_psi = se_values[[1]],
    se_logit_gamma = se_values[[2]],
    se_logit_epsilon = se_values[[3]],
    se_logit_p_previous = se_values[[4]],
    se_logit_p_current = se_values[[5]],
    expected_latent_stable_absent = sum(posterior[, "p00"]),
    expected_latent_gain = sum(posterior[, "p01"]),
    expected_latent_loss = sum(posterior[, "p10"]),
    expected_latent_stable_present = sum(posterior[, "p11"]),
    observed_gain_count = sum(observed_gain),
    observed_loss_count = sum(observed_loss),
    mean_true_gain_posterior_among_observed_gains = (
      if (sum(observed_gain) > 0)
        mean(posterior[observed_gain, "p01"])
      else NA_real_
    ),
    mean_true_loss_posterior_among_observed_losses = (
      if (sum(observed_loss) > 0)
        mean(posterior[observed_loss, "p10"])
      else NA_real_
    ),
    detection_probability_interior = detection_interior,
    identifiability_status = (
      if (identified) "IDENTIFIED" else "WEAK_OR_NONIDENTIFIED"
    ),
    stringsAsFactors = FALSE
  )
  fit_index <- fit_index + 1
}

write.csv(
  do.call(rbind, fit_rows),
  fit_path,
  row.names = FALSE
)
write.csv(
  do.call(rbind, posterior_rows),
  posterior_path,
  row.names = FALSE
)
