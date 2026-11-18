args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 3) {
  stop("usage: Rscript examples/villavicencio_axis_robustness_audit.R WEEKLY.csv SITEWEEK.csv OUTPUT.csv")
}
weekly_path <- args[[1]]
siteweek_path <- args[[2]]
output_path <- args[[3]]

transitions <- c("2008->2009", "2009->2010", "2010->2011")
weekly <- read.csv(weekly_path, stringsAsFactors = FALSE, check.names = FALSE)
siteweek <- read.csv(siteweek_path, stringsAsFactors = FALSE, check.names = FALSE)

prepare_context <- function(data, threshold, plant_field, poll_field) {
  data <- data[data$transition %in% transitions, , drop = FALSE]
  previous_positive <- as.numeric(data$previous_weight) >= threshold
  current_positive <- as.numeric(data$current_weight) >= threshold
  list(
    data = data,
    previous_positive = previous_positive,
    current_positive = current_positive,
    plant_field = plant_field,
    poll_field = poll_field
  )
}

contexts <- list(
  weekly_k1 = prepare_context(
    weekly, 1L, "plant_flowering_weeks", "pollinator_otherplant_active_weeks"
  ),
  weekly_k2 = prepare_context(
    weekly, 2L, "plant_flowering_weeks", "pollinator_otherplant_active_weeks"
  ),
  weekly_k3 = prepare_context(
    weekly, 3L, "plant_flowering_weeks", "pollinator_otherplant_active_weeks"
  ),
  siteweek_k1 = prepare_context(
    siteweek, 1L, "plant_flowering_siteweeks", "pollinator_otherplant_active_siteweeks"
  )
)

clip_probability <- function(x) {
  pmin(pmax(as.numeric(x), 1e-8), 1 - 1e-8)
}
log_loss <- function(y, p) {
  p <- clip_probability(p)
  mean(-(y * log(p) + (1 - y) * log(1 - p)))
}

fit_predict <- function(train, test, fields) {
  for (field in unique(c(
    "plant_opportunity_axis",
    "pollinator_opportunity_axis"
  ))) {
    train_value <- log1p(as.numeric(train[[field]]))
    test_value <- log1p(as.numeric(test[[field]]))
    center <- mean(train_value)
    scale_value <- sd(train_value)
    if (!is.finite(scale_value) || scale_value == 0) {
      train[[field]] <- rep(0, length(train_value))
      test[[field]] <- rep(0, length(test_value))
    } else {
      train[[field]] <- (train_value - center) / scale_value
      test[[field]] <- (test_value - center) / scale_value
    }
  }
  formula <- as.formula(
    paste("outcome ~", paste(fields, collapse = " + "))
  )
  fit <- suppressWarnings(glm(formula, data = train, family = binomial()))
  if (!isTRUE(fit$converged) || any(!is.finite(coef(fit)))) {
    return(list(converged = FALSE, log_loss = NA_real_))
  }
  p <- predict(fit, newdata = test, type = "response")
  list(
    converged = TRUE,
    log_loss = log_loss(test$outcome, p)
  )
}

rows <- list()
index <- 1L
for (context_name in names(contexts)) {
  context <- contexts[[context_name]]
  data <- context$data
  data$plant_opportunity_axis <- as.numeric(data[[context$plant_field]])
  data$pollinator_opportunity_axis <- as.numeric(data[[context$poll_field]])

  for (risk in c("gain", "loss")) {
    if (risk == "gain") {
      risk_data <- data[!context$previous_positive, , drop = FALSE]
      risk_data$outcome <- as.integer(
        context$current_positive[!context$previous_positive]
      )
    } else {
      risk_data <- data[context$previous_positive, , drop = FALSE]
      risk_data$outcome <- as.integer(
        !context$current_positive[context$previous_positive]
      )
    }

    for (held_out in transitions) {
      train <- risk_data[risk_data$transition != held_out, , drop = FALSE]
      test <- risk_data[risk_data$transition == held_out, , drop = FALSE]
      if (length(unique(train$outcome)) < 2 || length(unique(test$outcome)) < 2) {
        stop(paste(context_name, risk, held_out, "degenerate outcome"))
      }

      full <- fit_predict(
        train, test,
        c("plant_opportunity_axis", "pollinator_opportunity_axis")
      )
      drop_plant <- fit_predict(
        train, test,
        c("pollinator_opportunity_axis")
      )
      drop_pollinator <- fit_predict(
        train, test,
        c("plant_opportunity_axis")
      )
      if (!all(c(full$converged, drop_plant$converged, drop_pollinator$converged))) {
        stop(paste(context_name, risk, held_out, "fit failure"))
      }

      plant_increment <- drop_plant$log_loss - full$log_loss
      pollinator_increment <- drop_pollinator$log_loss - full$log_loss
      expected_difference <- if (risk == "gain") {
        pollinator_increment - plant_increment
      } else {
        plant_increment - pollinator_increment
      }

      rows[[index]] <- data.frame(
        context = context_name,
        risk_set = risk,
        held_out_transition = held_out,
        test_n = nrow(test),
        test_events = sum(test$outcome == 1),
        full_log_loss = full$log_loss,
        plant_increment = plant_increment,
        pollinator_increment = pollinator_increment,
        expected_direction_difference = expected_difference,
        expected_direction_pass = expected_difference > 0,
        stringsAsFactors = FALSE
      )
      index <- index + 1L
    }
  }
}
write.csv(do.call(rbind, rows), output_path, row.names = FALSE)
