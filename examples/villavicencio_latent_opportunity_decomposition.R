args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 4) {
  stop("usage: Rscript examples/villavicencio_latent_opportunity_decomposition.R TABLE.csv BASE_FITS.csv MODELS.csv POSTERIORS.csv")
}

table_path <- args[[1]]
base_fit_path <- args[[2]]
model_path <- args[[3]]
posterior_path <- args[[4]]

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

if (sum(base_fits$identifiability_status == "IDENTIFIED") < 5) {
  stop("latent opportunity decomposition is blocked by the frozen detection gate")
}

inv_logit <- function(x) 1 / (1 + exp(-x))

log_sum_exp <- function(values) {
  finite <- values[is.finite(values)]
  if (length(finite) == 0) return(-Inf)
  m <- max(finite)
  m + log(sum(exp(finite - m)))
}

unpack_parameters <- function(theta, model, x) {
  if (model == "base") {
    psi <- inv_logit(theta[[1]])
    gamma <- rep(inv_logit(theta[[2]]), length(x))
    epsilon <- rep(inv_logit(theta[[3]]), length(x))
    p_previous <- rep(inv_logit(theta[[4]]), length(x))
    p_current <- rep(inv_logit(theta[[5]]), length(x))
    beta_gain <- beta_loss <- beta_detection <- 0
  } else if (model == "detection_only") {
    psi <- inv_logit(theta[[1]])
    gamma <- rep(inv_logit(theta[[2]]), length(x))
    epsilon <- rep(inv_logit(theta[[3]]), length(x))
    p_previous <- rep(inv_logit(theta[[4]]), length(x))
    p_current <- inv_logit(theta[[5]] + theta[[6]] * x)
    beta_gain <- beta_loss <- 0
    beta_detection <- theta[[6]]
  } else if (model == "state_only") {
    psi <- inv_logit(theta[[1]])
    gamma <- inv_logit(theta[[2]] + theta[[3]] * x)
    epsilon <- inv_logit(theta[[4]] + theta[[5]] * x)
    p_previous <- rep(inv_logit(theta[[6]]), length(x))
    p_current <- rep(inv_logit(theta[[7]]), length(x))
    beta_gain <- theta[[3]]
    beta_loss <- theta[[5]]
    beta_detection <- 0
  } else if (model == "state_plus_detection") {
    psi <- inv_logit(theta[[1]])
    gamma <- inv_logit(theta[[2]] + theta[[3]] * x)
    epsilon <- inv_logit(theta[[4]] + theta[[5]] * x)
    p_previous <- rep(inv_logit(theta[[6]]), length(x))
    p_current <- inv_logit(theta[[7]] + theta[[8]] * x)
    beta_gain <- theta[[3]]
    beta_loss <- theta[[5]]
    beta_detection <- theta[[8]]
  } else {
    stop(paste("unknown model", model))
  }
  list(
    psi = psi,
    gamma = gamma,
    epsilon = epsilon,
    p_previous = p_previous,
    p_current = p_current,
    beta_gain = beta_gain,
    beta_loss = beta_loss,
    beta_detection = beta_detection
  )
}

negative_log_likelihood <- function(theta, frame, model) {
  x <- frame$opportunity_z
  par <- unpack_parameters(theta, model, x)
  total <- 0

  for (i in seq_len(nrow(frame))) {
    psi <- par$psi
    gamma <- par$gamma[[i]]
    epsilon <- par$epsilon[[i]]
    p1 <- par$p_previous[[i]]
    p2 <- par$p_current[[i]]

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
    obs1_z1 <- dbinom(y1, size = n1, prob = p1, log = TRUE)
    obs2_z1 <- dbinom(y2, size = n2, prob = p2, log = TRUE)

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

make_starts <- function(base_row, model) {
  base_theta <- c(
    qlogis(base_row$psi),
    qlogis(base_row$gamma),
    qlogis(base_row$epsilon),
    qlogis(base_row$p_previous),
    qlogis(base_row$p_current)
  )

  if (model == "base") {
    return(list(base_theta))
  }
  if (model == "detection_only") {
    return(lapply(
      c(-1, 0, 1),
      function(beta) c(base_theta[1:4], base_theta[5], beta)
    ))
  }
  if (model == "state_only") {
    beta_pairs <- list(
      c(0, 0),
      c(0.5, -0.5),
      c(1, -1),
      c(-0.5, 0.5),
      c(1, 0),
      c(0, -1)
    )
    return(lapply(
      beta_pairs,
      function(beta) c(
        base_theta[1],
        base_theta[2], beta[[1]],
        base_theta[3], beta[[2]],
        base_theta[4],
        base_theta[5]
      )
    ))
  }
  if (model == "state_plus_detection") {
    triples <- list(
      c(0, 0, 0),
      c(0.5, -0.5, 0),
      c(1, -1, 0),
      c(0, 0, 1),
      c(0.5, -0.5, 1),
      c(1, -1, 1),
      c(-0.5, 0.5, 1),
      c(0.5, -0.5, -1)
    )
    return(lapply(
      triples,
      function(beta) c(
        base_theta[1],
        base_theta[2], beta[[1]],
        base_theta[3], beta[[2]],
        base_theta[4],
        base_theta[5], beta[[3]]
      )
    ))
  }
  stop("unknown model")
}

model_names <- c(
  "base",
  "detection_only",
  "state_only",
  "state_plus_detection"
)

model_rows <- list()
posterior_rows <- list()
mi <- 1
pi <- 1

for (transition in transitions) {
  frame <- data[data$transition == transition, , drop = FALSE]
  base_row <- base_fits[base_fits$transition == transition, , drop = FALSE]
  if (nrow(base_row) != 1) stop("base fit row mismatch")

  x_raw <- as.numeric(frame$current_siteweek_opportunity_fraction)
  x_mean <- mean(x_raw)
  x_sd <- sd(x_raw)
  if (!is.finite(x_sd) || x_sd <= 0) {
    stop(paste("zero opportunity variance in", transition))
  }
  frame$opportunity_z <- (x_raw - x_mean) / x_sd

  best_by_model <- list()

  for (model in model_names) {
    starts <- make_starts(base_row, model)
    results <- list()

    for (start_index in seq_along(starts)) {
      fit <- tryCatch(
        optim(
          par = starts[[start_index]],
          fn = negative_log_likelihood,
          frame = frame,
          model = model,
          method = "L-BFGS-B",
          lower = rep(-8, length(starts[[start_index]])),
          upper = rep(8, length(starts[[start_index]])),
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
      stop(paste("no finite fit for", transition, model))
    }

    values <- vapply(results, function(x) x$fit$value, numeric(1))
    best_index <- which.min(values)
    best <- results[[best_index]]$fit
    best_by_model[[model]] <- best

    pars <- unpack_parameters(
      best$par,
      model,
      rep(0, nrow(frame))
    )

    model_rows[[mi]] <- data.frame(
      transition = transition,
      model = model,
      n_rows = nrow(frame),
      parameter_count = length(best$par),
      best_nll = best$value,
      aic = 2 * best$value + 2 * length(best$par),
      best_convergence = best$convergence,
      all_starts_converged = all(vapply(
        results,
        function(x) x$fit$convergence == 0,
        logical(1)
      )),
      multi_start_nll_range = max(values) - min(values),
      opportunity_mean = x_mean,
      opportunity_sd = x_sd,
      beta_gain = pars$beta_gain,
      beta_loss = pars$beta_loss,
      beta_detection = pars$beta_detection,
      stringsAsFactors = FALSE
    )
    mi <- mi + 1
  }

  # Posterior states under the most flexible model are exported only as a
  # diagnostic surface; model comparison decides whether state effects deserve
  # interpretation.
  best <- best_by_model[["state_plus_detection"]]
  par <- unpack_parameters(
    best$par,
    "state_plus_detection",
    frame$opportunity_z
  )

  for (i in seq_len(nrow(frame))) {
    psi <- par$psi
    gamma <- par$gamma[[i]]
    epsilon <- par$epsilon[[i]]
    p1 <- par$p_previous[[i]]
    p2 <- par$p_current[[i]]

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
    obs1_z1 <- dbinom(y1, n1, p1, log = TRUE)
    obs2_z1 <- dbinom(y2, n2, p2, log = TRUE)
    logs <- c(
      state_logs[[1]] + obs1_z0 + obs2_z0,
      state_logs[[2]] + obs1_z0 + obs2_z1,
      state_logs[[3]] + obs1_z1 + obs2_z0,
      state_logs[[4]] + obs1_z1 + obs2_z1
    )
    norm <- log_sum_exp(logs)
    probs <- exp(logs - norm)

    posterior_rows[[pi]] <- data.frame(
      transition = transition,
      plant = frame$plant[[i]],
      pollinator = frame$pollinator[[i]],
      opportunity_z = frame$opportunity_z[[i]],
      p00 = probs[[1]],
      p01 = probs[[2]],
      p10 = probs[[3]],
      p11 = probs[[4]],
      stringsAsFactors = FALSE
    )
    pi <- pi + 1
  }
}

write.csv(do.call(rbind, model_rows), model_path, row.names = FALSE)
write.csv(do.call(rbind, posterior_rows), posterior_path, row.names = FALSE)
