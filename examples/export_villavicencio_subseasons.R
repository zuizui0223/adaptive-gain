args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 2) {
  stop("usage: Rscript examples/export_villavicencio_subseasons.R INPUT.RData OUTPUT_DIR")
}

input_path <- args[[1]]
output_dir <- args[[2]]
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

loaded <- load(input_path)
required <- c("bipartite.networks", "plant.id", "pollinator.id")
missing <- setdiff(required, loaded)
if (length(missing) > 0) {
  stop(paste("missing required RData objects:", paste(missing, collapse = ", ")))
}

nets <- get("bipartite.networks")
plant_id <- get("plant.id")
pollinator_id <- get("pollinator.id")

if (!is.list(nets) || length(nets) != 18) {
  stop("expected bipartite.networks to contain exactly 18 matrices")
}

as_id_frame <- function(x, guild) {
  if (is.data.frame(x)) {
    out <- x
  } else if (is.matrix(x)) {
    out <- as.data.frame(x, stringsAsFactors = FALSE)
  } else {
    out <- data.frame(code = as.character(x), stringsAsFactors = FALSE)
  }
  out$guild <- guild
  out
}

plant_frame <- as_id_frame(plant_id, "plant")
pollinator_frame <- as_id_frame(pollinator_id, "pollinator")
write.csv(plant_frame, file.path(output_dir, "plant_id.csv"), row.names = FALSE)
write.csv(pollinator_frame, file.path(output_dir, "pollinator_id.csv"), row.names = FALSE)

id_codes <- function(x, expected_n, prefix) {
  if (is.data.frame(x) || is.matrix(x)) {
    candidates <- as.character(x[, 1])
  } else {
    candidates <- as.character(x)
  }
  if (length(candidates) != expected_n) {
    candidates <- paste0(prefix, seq_len(expected_n))
  }
  candidates
}

period_names <- names(nets)
if (is.null(period_names) || any(period_names == "")) {
  period_names <- sprintf("period_%02d", seq_along(nets))
}
write.csv(
  data.frame(
    source_index = seq_along(nets),
    period = period_names,
    stringsAsFactors = FALSE
  ),
  file.path(output_dir, "period_index.csv"),
  row.names = FALSE
)

interaction_rows <- list()
axis_rows <- list()

for (i in seq_along(nets)) {
  mat <- as.matrix(nets[[i]])
  if (length(dim(mat)) != 2) {
    stop(paste("network", i, "is not a matrix"))
  }

  has_row_names <- !is.null(rownames(mat)) && all(rownames(mat) != "")
  has_col_names <- !is.null(colnames(mat)) && all(colnames(mat) != "")

  full_normal <- nrow(mat) == nrow(plant_frame) && ncol(mat) == nrow(pollinator_frame)
  full_reversed <- nrow(mat) == nrow(pollinator_frame) && ncol(mat) == nrow(plant_frame)

  if (full_reversed && !full_normal) {
    mat <- t(mat)
    has_row_names <- !is.null(rownames(mat)) && all(rownames(mat) != "")
    has_col_names <- !is.null(colnames(mat)) && all(colnames(mat) != "")
    full_normal <- TRUE
  }

  if (has_row_names) {
    plant_codes <- rownames(mat)
  } else if (full_normal) {
    plant_codes <- id_codes(plant_id, nrow(mat), "plant_")
  } else {
    stop(
      paste(
        "network", i,
        "has no row names and row count cannot be mapped to plant.id:",
        nrow(mat)
      )
    )
  }

  if (has_col_names) {
    pollinator_codes <- colnames(mat)
  } else if (full_normal) {
    pollinator_codes <- id_codes(pollinator_id, ncol(mat), "pollinator_")
  } else {
    stop(
      paste(
        "network", i,
        "has no column names and column count cannot be mapped to pollinator.id:",
        ncol(mat)
      )
    )
  }

  idx <- which(mat > 0, arr.ind = TRUE)
  if (nrow(idx) > 0) {
    interaction_rows[[length(interaction_rows) + 1]] <- data.frame(
      period = period_names[[i]],
      plant = plant_codes[idx[, 1]],
      pollinator = pollinator_codes[idx[, 2]],
      weight = as.numeric(mat[idx]),
      stringsAsFactors = FALSE
    )
  }

  axis_rows[[length(axis_rows) + 1]] <- rbind(
    data.frame(
      period = period_names[[i]],
      guild = "plant",
      species = plant_codes,
      basis = "matrix_axis_not_verified_presence",
      stringsAsFactors = FALSE
    ),
    data.frame(
      period = period_names[[i]],
      guild = "pollinator",
      species = pollinator_codes,
      basis = "matrix_axis_not_verified_presence",
      stringsAsFactors = FALSE
    )
  )
}

if (length(interaction_rows) == 0) {
  interactions <- data.frame(
    period = character(),
    plant = character(),
    pollinator = character(),
    weight = numeric()
  )
} else {
  interactions <- do.call(rbind, interaction_rows)
}
axes <- do.call(rbind, axis_rows)

write.csv(
  interactions,
  file.path(output_dir, "subseason_interactions_long.csv"),
  row.names = FALSE
)
write.csv(
  axes,
  file.path(output_dir, "subseason_matrix_axes.csv"),
  row.names = FALSE
)

manifest <- data.frame(
  key = c(
    "source_object",
    "network_count",
    "positive_interaction_rows",
    "axis_semantics"
  ),
  value = c(
    "bipartite.networks",
    as.character(length(nets)),
    as.character(nrow(interactions)),
    "matrix axes exported for QC only; do not treat as independent species presence until verified"
  ),
  stringsAsFactors = FALSE
)
write.csv(manifest, file.path(output_dir, "export_manifest.csv"), row.names = FALSE)
