#!/usr/bin/env Rscript
# Stage81D. TRUE source Ohashi et al. 2015 28 taxon 300--700nm spectra.
# Apis D65/von-Kries green-foliage adapted receptor excitations from CRAN pavo.
# "far" = absolute green receptor contrast |E_l-0.5|; not actual flight distance.
# "near" = chromatic hexagon distance to foliage (r.vec); not actual behavior.
# This independently modeled 28-species subset does not reproduce the published
# 48/219 source classifications without full-author-method cross-validation.

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 3) stop("USAGE: Rscript quantify_...R <wide.csv> <manifest.csv> <outdir>")
outdir <- args[[3]]
dir.create(outdir, recursive=TRUE, showWarnings=FALSE)
if (!requireNamespace("pavo", quietly=TRUE)) stop("SOURCE_RECEPTOR_PACKAGE_PAVO_NOT_INSTALLED")
file <- read.csv(args[[1]], check.names=FALSE, stringsAsFactors=FALSE)
meta <- read.csv(args[[2]], stringsAsFactors=FALSE)
if (nrow(file) != 401 || ncol(file) != 1361 ||
    !identical(as.integer(file[["wl"]]), seq.int(300L,700L))) {
    stop("STAGE81D_AUTHENTIC_SOURCE_WAVELENGTH_MATRIX_NOT_401x1360")
}
if (nrow(meta)!=1360 || length(unique(meta[["source_species"]]))!=28)
    stop("STAGE81D_TRUE_SOURCE_28_TAXA_1360_RECORDS_CHANGED")
spectra_names <- names(file)[-1]
if (!identical(spectra_names,meta[["sample_id"]])) {
    stop("STAGE81D_ORIGINAL_SPECTROMETER_SAMPLE_ID_MANIFEST_MISMATCH")
}
if (any(!is.finite(as.matrix(file[-1])))) stop("STAGE81D_ORIGINAL_REFLECTANCE_MISSING")

vis <- pavo::vismodel(file,
  visual="apis",achromatic="l",illum="D65",trans="ideal",
  qcatch="Ei",bkg="green",vonkries=TRUE,relative=FALSE)
hex <- pavo::colspace(vis, space="hexagon")
if (nrow(vis)!=1360 || nrow(hex)!=1360 ||
    !all(c("s","m","l") %in% names(vis)) ||
    !all(c("x","y","r.vec") %in% names(hex))) {
    stop("STAGE81D_APIS_RECEPTOR_OR_HEXAGON_CHANNEL_NOT_AVAILABLE")
}
if (is.null(rownames(vis)) || !identical(rownames(vis),rownames(hex)) ||
    !identical(rownames(vis),meta[["sample_id"]])) {
    stop("STAGE81D_RECEPTOR_SPECTRA_ROW_IDS_NOT_IDENTICAL")
}
if (any(as.matrix(vis[,c("s","m","l")]) <= 0) ||
    any(as.matrix(vis[,c("s","m","l")]) >= 1)) {
    stop("STAGE81D_ADAPTED_APIS_RECEPTOR_EXCITATIONS_OUT_OF_BOUNDS")
}
sample_frame <- data.frame(
  meta,
  green_receptor_E=as.numeric(vis[["l"]]),
  hex_x=as.numeric(hex[["x"]]),
  hex_y=as.numeric(hex[["y"]]),
  hex_background_r=as.numeric(hex[["r.vec"]]),
  stringsAsFactors=FALSE
)
if (any(!is.finite(as.matrix(sample_frame[c("green_receptor_E","hex_x","hex_y","hex_background_r")]))))
   stop("STAGE81D_NONFINITE_RECEIVER_ORIGINAL_SOURCE_MODEL")

part_keys <- unique(sample_frame[,c("source_species","original_flower_part")])
part_keys <- part_keys[order(part_keys$source_species,part_keys$original_flower_part),,drop=FALSE]
if (nrow(part_keys)!=53) stop("STAGE81D_TRUE_SOURCE_53_AGE_PARTS_CHANGED")
permutation_count <- 999L
metrics <- vector("list", nrow(part_keys))
for (ii in seq_len(nrow(part_keys))) {
    key <- part_keys[ii,,drop=FALSE]
    one <- sample_frame[sample_frame$source_species==key$source_species &
                        sample_frame$original_flower_part==key$original_flower_part,,drop=FALSE]
    e <- one[one$original_stage=="e",,drop=FALSE]
    l <- one[one$original_stage=="l",,drop=FALSE]
    if (nrow(e)!=10 || nrow(l)!=10)
        stop("STAGE81D_REAL_STAGE_10_EARLY_10_LATE_NOT_MET")
    dxy <- c(mean(l$hex_x)-mean(e$hex_x),mean(l$hex_y)-mean(e$hex_y))
    dist <- sqrt(sum(dxy*dxy))
    pool <- rbind(e,l)
    set.seed(20261118L + ii)
    exceed <- 0L
    for (jj in seq_len(permutation_count)) {
        perm <- sample.int(20L)
        a <- pool[perm[seq_len(10L)],,drop=FALSE]
        b <- pool[perm[11L:20L],,drop=FALSE]
        u <- c(mean(b$hex_x)-mean(a$hex_x),
               mean(b$hex_y)-mean(a$hex_y))
        exceed <- exceed + (sqrt(sum(u*u))>=dist-1e-12)
    }
    metrics[[ii]] <- data.frame(
      source_species=key$source_species,
      original_flower_part=key$original_flower_part,
      n_early_samples=nrow(e),
      n_late_samples=nrow(l),
      source_has_custom_part_specifications=as.integer(any(one$has_author_part_specifications==1)),
      bee_hex_early_to_late_dist=dist,
      bee_hex_colour_shift_permutation_p=(1+exceed)/(1+permutation_count),
      early_green_receptor_background_abs=mean(abs(e$green_receptor_E-.5)),
      late_green_receptor_background_abs=mean(abs(l$green_receptor_E-.5)),
      delta_far_green_abs_late_minus_early=mean(abs(l$green_receptor_E-.5))-mean(abs(e$green_receptor_E-.5)),
      early_near_hex_background_r=mean(e$hex_background_r),
      late_near_hex_background_r=mean(l$hex_background_r),
      delta_near_hex_chroma_late_minus_early=mean(l$hex_background_r)-mean(e$hex_background_r),
      stringsAsFactors=FALSE
    )
}
parts <- do.call(rbind, metrics)
parts$bee_hex_colour_shift_BH_q_53 <- p.adjust(parts$bee_hex_colour_shift_permutation_p, method="BH")
parts$independent_model_bee_visibly_changing_part_threshold_0_09 <- (
    parts$bee_hex_early_to_late_dist >= .09 & parts$bee_hex_colour_shift_BH_q_53 < .05)
if (nrow(parts)!=53 ||
    any(!is.finite(parts$bee_hex_early_to_late_dist)) ||
    any(!is.finite(parts$early_green_receptor_background_abs))) {
    stop("STAGE81D_TRUE_SOURCE_PART_BEERECEPTOR_RESULTS_INVALID")
}
write.csv(parts,file.path(outdir,"stage81d_original_28_apis_far_green_near_hex_age_parts.csv"),row.names=FALSE)

species_names <- sort(unique(parts$source_species))
species <- vector("list",length(species_names))
for (k in seq_along(species_names)) {
    src <- species_names[[k]]
    pp <- parts[parts$source_species==src,,drop=FALSE]
    species[[k]] <- data.frame(
        source_species=src,
        original_age_parts=nrow(pp),
        independent_model_significant_hex_part_count=sum(pp$bee_hex_colour_shift_BH_q_53<.05),
        independent_model_visible_0_09_part_count=sum(pp$independent_model_bee_visibly_changing_part_threshold_0_09),
        independent_model_any_visible_hex_shift=any(pp$independent_model_bee_visibly_changing_part_threshold_0_09),
        median_delta_far_green_abs=median(pp$delta_far_green_abs_late_minus_early),
        median_delta_near_hex_chroma=median(pp$delta_near_hex_chroma_late_minus_early),
        median_age_colour_shift_hex=median(pp$bee_hex_early_to_late_dist),
        author_exact_positive_negative_per_species_not_originally_confirmed=TRUE
    )
}
species <- do.call(rbind,species)
write.csv(species,file.path(outdir,"stage81d_original_28_apis_far_near_species.csv"),row.names=FALSE)

# Central vs outer spatial differences: only for parts c/o, no custom Specs.
# This does not prove the natural pattern is a functional nectar guide.
spatial <- list()
for (src in species_names) {
    z <- sample_frame[sample_frame$source_species==src,,drop=FALSE]
    if (any(z$has_author_part_specifications==1)) next
    for (stage in c("e","l")) {
        a <- z[z$original_stage==stage & z$original_flower_part=="c",,drop=FALSE]
        b <- z[z$original_stage==stage & z$original_flower_part=="o",,drop=FALSE]
        if (nrow(a)!=10 || nrow(b)!=10) next
        diff <- c(mean(b$hex_x)-mean(a$hex_x),mean(b$hex_y)-mean(a$hex_y))
        spatial[[length(spatial)+1L]] <- data.frame(
            source_species=src, original_flower_stage=stage,
            original_author_part_codes="c_vs_o_no_custom_spec",
            early_or_late_center_outer_hexagon_distance=sqrt(sum(diff*diff)),
            not_demonstrated_functional_nectar_guide=TRUE)
    }
}
if (length(spatial)>0) {
    write.csv(do.call(rbind,spatial),
       file.path(outdir,"stage81d_original_28_candidate_center_outer_hexagon_spatial.csv"),
       row.names=FALSE)
}
readout <- list(
  schema="stage81d_real_original_Ohashi_28_species_53_parts_apis_d65_green_early_late_receptor_metrics",
  original_28_species=length(species_names),
  original_source_age_parts=nrow(parts),
  original_spectra_n=1360,
  fitted_visual_system="pavo_APIS_HONEYBEE_D65_GREEN_VON_KRIES_Ei_colour_hexagon",
  pavo_package_version=as.character(packageVersion("pavo")),
  source_28_species_with_model_detectable_hex_change=sum(species$independent_model_any_visible_hex_shift),
  source_parts_with_model_detectable_hex_change=sum(parts$independent_model_bee_visibly_changing_part_threshold_0_09),
  source_28_species_with_near_chroma_lower_at_late_median=sum(species$median_delta_near_hex_chroma<0),
  source_28_species_with_green_contrast_lower_at_late_median=sum(species$median_delta_far_green_abs<0),
  source_28_species_both_late_far_green_and_near_chroma_lower=sum(
     species$median_delta_far_green_abs<0 & species$median_delta_near_hex_chroma<0),
  source_spatial_center_outer_candidate_rows=length(spatial),
  source_2015_published_bee_visible_all219=48L,
  do_not_transfer_published_48_of_219_to_this_28=TRUE,
  original_author_source_species_classifications_not_independently_recovered=TRUE,
  author_original_shuffle_and_test_area_selection_may_differ_from_this_53part_subanalysis=TRUE,
  source_European_field_visitors_not_same_spectrometer_population_or_flower=TRUE,
  no_wind_odor_learning_or_landing_observations_in_2015_source=TRUE,
  no_causal_pollinator_preference_or_fitness_estimated=TRUE
)
if (!requireNamespace("jsonlite",quietly=TRUE)) stop("SOURCE_JSON_PACKAGE_NOT_INSTALLED")
writeLines(jsonlite::toJSON(readout,pretty=TRUE,auto_unbox=TRUE),
           file.path(outdir,"stage81d_original_28_apis_d65_far_near_source_receipt.json"))
cat("STAGE81D_SOURCE_OHASHI_REAL_BEE_RECEPTOR_FAR_GREEN_NEAR_HEX ",
    jsonlite::toJSON(readout,auto_unbox=TRUE),"\n")
