args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 3) {
  stop("usage: Rscript examples/villavicencio_detection_overdispersion_fit.R TABLE.csv BINOMIAL_FITS.csv OUTPUT.csv")
}

table_path <- args[[1]]
base_fit_path <- args[[2]]
output_path <- args[[3]]

data <- read.csv(table_path, stringsAsFactors = FALSE, check.names = FALSE)
base_fits <- read.csv(base_fit_path, stringsAsFactors = FALSE, check.names = FALSE)

transitions <- c(
  "2008_early->2008_mid",
  "2008_mid->2008_late",
  "2009_early->2009_mid",
  "2009_mid->2009_late",
  "2010_early->2010_mid",
  "2010_mid->2010_late"
)

inv_logit <- function(x) 1 / (1 + exp(-x))

log_sum_exp <- function(values) {
  finite <- values[is.finite(values)]
  if (length(finite) == 0) return(-Inf)
  m <- max(finite)
  m + log(sum(exp(finite - m)))
}

dbetabinom_log <- function(y, n, mu, kappa) {
  alpha <- mu * kappa
  beta <- (1 - mu) * kappa
  lchoose(n, y) + lbeta(y + alpha, n - y + beta) - lbeta(alpha, beta)
}

negative_log_likelihood <- function(theta, frame) {
  psi <- inv_logit(theta[[1]])
  gamma <- inv_logit(theta[[2]])
  epsilon <- inv_logit(theta[[3]])
  p1 <- inv_logit(theta[[4]])
  p2 <- inv_logit(theta[[5]])
  kappa1 <- exp(theta[[6]])
  kappa2 <- exp(theta[[7]])

  total <- 0
  for (i in seq_len(nrow(frame))) {
    y1 <- frame$previous_success_censuses[[i]]
    n1 <- frame$previous_trials[[i]]
    y2 <- frame$current_success_censuses[[i]]
    n2 <- frame$current_trials[[i]]

    state_logs <- c(
      log1p(-psi) + log1p(-gamma),
      log1p(-psi) + log(gamma),
      log(psi) + log(epsilon),
      log(psi) + log1p(-epsilon)
    )

    obs1_z0 <- if (y1 == 0) 0 else -Inf
    obs2_z0 <- if (y2 == 0) 0 else -Inf
    obs1_z1 <- dbetabinom_log(y1, n1, p1, kappa1)
    obs2_z1 <- dbetabinom_log(y2, n2, p2, kappa2)

    terms <- c(
      state_logs[[1]] + obs1_z0 + obs2_z0,
      state_logs[[2]] + obs1_z0 + obs2_z1,
      state_logs[[3]] + obs1_z1 + obs2_z0,
      state_logs[[4]] + obs1_z1 + obs2_z1
    )
    value <- log_sum_exp(terms)
    if (!is.finite(value)) return(1e100)
    total <- total - value
  }
  total
}

make_starts <- function(base_row) {
  base <- c(
    qlogis(base_row$psi),
    qlogis(base_row$gamma),
    qlogis(base_row$epsilon),
    qlogis(base_row$p_previous),
    qlogis(base_row$p_current)
  )
  state_shifts <- list(
    c(0, 0),
    c(-1, -1),
    c(-2, -2),
    c(-2, 0),
    c(0, -2),
    c(1, -1)
  )
  kappas <- c(5, 20, 100)
  out <- list()
  index <- 1
  for (shift in state_shifts) {
    for (kappa in kappas) {
      candidate <- base
      candidate[[2]] <- candidate[[2]] + shift[[1]]
      candidate[[3]] <- candidate[[3]] + shift[[2]]
      out[[index]] <- c(candidate, log(kappa), log(kappa))
      index <- index + 1
    }
  }
  out
}

rows <- list()
ri <- 1

for (transition in transitions) {
  frame <- data[data$transition == transition, , drop = FALSE]
  base_row <- base_fits[base_fits$transition == transition, , drop = FALSE]
  if (nrow(base_row) != 1) stop("base fit row mismatch")

  starts <- make_starts(base_row)
  results <- list()

  for (start_index in seq_along(starts)) {
    fit <- tryCatch(
      optim(
        par = starts[[start_index]],
        fn = negative_log_likelihood,
        frame = frame,
        method = "L-BFGS-B",
        lower = c(rep(-8, 5), rep(log(0.1), 2)),
        upper = c(rep(8, 5), rep(log(10000), 2)),
        control = list(maxit = 5000, factr = 1e7)
      ),
      error = function(e) NULL
    )
    if (!is.null(fit) && is.finite(fit$value)) {
      results[[length(results) + 1]] <- list(
        start_index = start_index,
        fit = fit
      )
    }
  }

  if (length(results) == 0) {
    stop(paste("no finite beta-binomial fit for", transition))
  }

  values <- vapply(results, function(x) x$fit$value, numeric(1))
  best_index <- which.min(values)
  best <- results[[best_index]]$fit
  probs <- inv_logit(best$par[1:5])
  names(probs) <- c(
    "psi",
    "gamma",
    "epsilon",
    "p_previous",
    "p_current"
  )
  kappas <- exp(best$par[6:7])

  binomial_nll <- as.numeric(base_row$best_nll)
  binomial_aic <- 2 * binomial_nll + 2 * 5
  beta_binomial_aic <- 2 * best$value + 2 * 7

  rows[[ri]] <- data.frame(
    transition = transition,
    n_rows = nrow(frame),
    binomial_nll = binomial_nll,
    binomial_aic = binomial_aic,
    beta_binomial_nll = best$value,
    beta_binomial_aic = beta_binomial_aic,
    delta_aic_beta_minus_binomial = beta_binomial_aic - binomial_aic,
    beta_binomial_preferred = beta_binomial_aic <= binomial_aic - 2,
    optim_result_count = length(results),
    all_starts_converged = all(vapply(
      results,
      function(x) x$fit$convergence == 0,
      logical(1)
    )),
    multi_start_nll_range = max(values) - min(values),
    psi = probs[["psi"]],
    gamma = probs[["gamma"]],
    epsilon = probs[["epsilon"]],
    p_previous = probs[["p_previous"]],
    p_current = probs[["p_current"]],
    kappa_previous = kappas[[1]],
    kappa_current = kappas[[2]],
    gamma_logit_at_boundary = abs(best$par[[2]]) >= 7.9,
    epsilon_logit_at_boundary = abs(best$par[[3]]) >= 7.9,
    any_state_transition_boundary = (
      abs(best$par[[2]]) >= 7.9 || abs(best$par[[3]]) >= 7.9
    ),
    stringsAsFactors = FALSE
  )
  ri <- ri + 1
}

write.csv(do.call(rbind, rows), output_path, row.names = FALSE)
