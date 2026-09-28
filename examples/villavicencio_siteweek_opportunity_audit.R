args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 3) {
  stop("usage: Rscript examples/villavicencio_siteweek_opportunity_audit.R INPUT.csv PREDICTIONS.csv FOLDS.csv")
}
input_path <- args[[1]]
prediction_path <- args[[2]]
fold_path <- args[[3]]

predictors <- c(
  "siteweek_focal_excluded_overlap_cells",
  "plant_flowering_siteweeks",
  "pollinator_otherplant_active_siteweeks"
)
scopes <- list(
  strict_core_2008_2011 = c("2008->2009", "2009->2010", "2010->2011"),
  near_core_2007_2011 = c("2007->2008", "2008->2009", "2009->2010", "2010->2011"),
  all_annual_2006_2011 = c("2006->2007", "2007->2008", "2008->2009", "2009->2010", "2010->2011")
)

data <- read.csv(input_path, stringsAsFactors = FALSE, check.names = FALSE)
required <- c("transition", "risk_set", "outcome", predictors)
missing <- setdiff(required, names(data))
if (length(missing) > 0) stop(paste("missing columns:", paste(missing, collapse=", ")))

prepare_fold <- function(train, test) {
  for (name in predictors) {
    xtr <- log1p(as.numeric(train[[name]]))
    xte <- log1p(as.numeric(test[[name]]))
    center <- mean(xtr)
    scale_value <- sd(xtr)
    if (!is.finite(scale_value) || scale_value == 0) {
      train[[name]] <- rep(0, length(xtr))
      test[[name]] <- rep(0, length(xte))
    } else {
      train[[name]] <- (xtr - center) / scale_value
      test[[name]] <- (xte - center) / scale_value
    }
  }
  list(train=train, test=test)
}
clip <- function(x) pmin(pmax(as.numeric(x), 1e-8), 1 - 1e-8)

pred_rows <- list()
fold_rows <- list()
pi <- 1
fi <- 1

for (scope_name in names(scopes)) {
  transitions <- scopes[[scope_name]]
  scope_data <- data[data$transition %in% transitions, , drop=FALSE]
  for (risk in c("gain","loss")) {
    risk_data <- scope_data[scope_data$risk_set == risk, , drop=FALSE]
    for (held_out in transitions) {
      train <- risk_data[risk_data$transition != held_out, , drop=FALSE]
      test <- risk_data[risk_data$transition == held_out, , drop=FALSE]
      prepared <- prepare_fold(train, test)
      train <- prepared$train
      test <- prepared$test
      formula <- as.formula(paste("outcome ~", paste(predictors, collapse=" + ")))
      fit <- suppressWarnings(glm(formula, data=train, family=binomial()))
      model_p <- clip(predict(fit, newdata=test, type="response"))
      null_p <- clip(rep(mean(train$outcome), nrow(test)))

      pred_rows[[pi]] <- data.frame(
        analysis_scope=scope_name,
        risk_set=risk,
        transition=held_out,
        outcome=as.integer(test$outcome),
        model_probability=model_p,
        null_probability=null_p,
        stringsAsFactors=FALSE
      )
      pi <- pi + 1

      fold_rows[[fi]] <- data.frame(
        analysis_scope=scope_name,
        risk_set=risk,
        held_out_transition=held_out,
        train_n=nrow(train),
        test_n=nrow(test),
        train_events=sum(train$outcome==1),
        test_events=sum(test$outcome==1),
        converged=isTRUE(fit$converged),
        coefficient_count=length(coef(fit)),
        finite_coefficient_count=sum(is.finite(coef(fit))),
        stringsAsFactors=FALSE
      )
      fi <- fi + 1
    }
  }
}
write.csv(do.call(rbind,pred_rows), prediction_path, row.names=FALSE)
write.csv(do.call(rbind,fold_rows), fold_path, row.names=FALSE)
