#!/usr/bin/env Rscript
# Stage85 50 genuine original Ohashi (2015) spectrometer taxa.
# 28 reference Apis D65/green von-Kries model source regression plus
# 22 additional original DoPI exact-name matched species. No observed
# Bombus cognition, flight-range, actual near-distance detection or wind.
args <- commandArgs(trailingOnly=TRUE)
if (length(args)!=5) {
  stop("USAGE <wide50.csv> <manifest50.csv> <old28species.csv> <old28parts.csv> <outdir>")
}
output <- args[[5]]
dir.create(output,recursive=TRUE,showWarnings=FALSE)
if (!requireNamespace("pavo",quietly=TRUE) ||
    !requireNamespace("jsonlite",quietly=TRUE)) {
  stop("STAGE85_REQUIRED_AUTHENTIC_R_VISUAL_MODEL_PACKAGES_MISSING")
}
raw <- read.csv(args[[1]],check.names=FALSE,stringsAsFactors=FALSE)
meta <- read.csv(args[[2]],stringsAsFactors=FALSE)
old_species <- read.csv(args[[3]],stringsAsFactors=FALSE)
old_parts <- read.csv(args[[4]],stringsAsFactors=FALSE)
if (nrow(raw)!=401L || !identical(as.integer(raw$wl),seq.int(300L,700L))) {
  stop("STAGE85_ORIGINAL_RAW_401_WAVELENGTHS_CHANGED")
}
if (nrow(meta)!=ncol(raw)-1L ||
    !identical(names(raw)[-1L],meta$sample_id) ||
    length(unique(meta$source_species))!=50L ||
    length(unique(old_species$source_species))!=28L ||
    nrow(old_parts)!=53L) {
  stop("STAGE85_INVALID_AUTHENTIC_50_SAMPLE_MANIFEST_OR_PRIOR_28_REFERENCE")
}
if (!all(meta$original_stage %in% c("e","m","l")) ||
    !all(meta$source_species_new_for_DOPI %in% c(0,1)) ||
    length(unique(meta$source_species[meta$source_species_new_for_DOPI==1]))!=22L ||
    length(unique(meta$source_species[meta$source_species_new_for_DOPI==0]))!=28L) {
  stop("STAGE85_REAL_DOPI_28_PLUS_22_SPECIES_SAMPLE_IDENTITY_CHANGED")
}
if (any(!is.finite(as.matrix(raw[-1])))) {
  stop("STAGE85_ORIGINAL_REFLECTANCE_NONFINITE")
}

# The EXACT SAME published pavo settings as Stage81D; no task-derived
# observer shift, nearest-pollen synoptic weather or unvalidated background.
vis <- pavo::vismodel(raw,visual="apis",achromatic="l",illum="D65",
                      trans="ideal",qcatch="Ei",bkg="green",
                      vonkries=TRUE,relative=FALSE)
hex <- pavo::colspace(vis,space="hexagon")
if (nrow(vis)!=nrow(meta) || nrow(hex)!=nrow(meta) ||
    !identical(rownames(vis),rownames(hex)) ||
    !identical(rownames(vis),meta$sample_id) ||
    !all(c("s","m","l")%in%names(vis)) ||
    !all(c("x","y","r.vec")%in%names(hex))) {
  stop("STAGE85_R_APIS_BEE_RECEPTOR_OUTPUT_SAMPLE_ID_MISMATCH")
}
if (any(as.matrix(vis[,c("s","m","l")])<=0) ||
    any(as.matrix(vis[,c("s","m","l")])>=1)) {
  stop("STAGE85_ADAPTED_RECEPTORS_OUTSIDE_0_1")
}
x <- data.frame(meta,green_receptor_E=as.numeric(vis$l),
                hex_x=as.numeric(hex$x),hex_y=as.numeric(hex$y),
                hex_background_r=as.numeric(hex$r.vec),
                stringsAsFactors=FALSE)
if (any(!is.finite(as.matrix(x[c("green_receptor_E","hex_x","hex_y",
                                "hex_background_r")])))) {
  stop("STAGE85_RECEPTOR_MODEL_DERIVED_NONFINITE")
}

partkeys <- unique(x[,c("source_species","original_flower_part")])
partkeys <- partkeys[order(partkeys$source_species,partkeys$original_flower_part),]
parts <- list()
unresolved <- list()
for (ii in seq_len(nrow(partkeys))) {
  sp <- partkeys$source_species[[ii]]
  part <- partkeys$original_flower_part[[ii]]
  g <- x[x$source_species==sp & x$original_flower_part==part,,drop=FALSE]
  e <- g[g$original_stage=="e",,drop=FALSE]
  l <- g[g$original_stage=="l",,drop=FALSE]
  if (nrow(e)!=10L || nrow(l)!=10L) {
    unresolved[[length(unresolved)+1L]] <- data.frame(
      source_species=sp,original_flower_part=part,
      actual_early_samples=nrow(e),actual_late_samples=nrow(l),
      reason="INSUFFICIENT_AUTHENTIC_ORIGINAL_EARLY_LATE_GROUP_NOT_NEGATIVE")
    next
  }
  d <- c(mean(l$hex_x)-mean(e$hex_x),mean(l$hex_y)-mean(e$hex_y))
  observed <- sqrt(sum(d*d))
  full <- rbind(e,l)
  set.seed(20261118L+ii)
  exceed <- 0L
  for (k in seq_len(999L)) {
    ix <- sample.int(20L)
    a <- full[ix[1:10],,drop=FALSE]
    b <- full[ix[11:20],,drop=FALSE]
    del <- c(mean(b$hex_x)-mean(a$hex_x),mean(b$hex_y)-mean(a$hex_y))
    exceed <- exceed + (sqrt(sum(del*del))>=observed-1e-12)
  }
  parts[[length(parts)+1L]] <- data.frame(
    source_species=sp,original_flower_part=part,
    source_species_new_for_DOPI=as.integer(g$source_species_new_for_DOPI[1]),
    n_early_samples=nrow(e),n_late_samples=nrow(l),
    source_has_custom_part_specifications=as.integer(any(g$has_author_part_specifications==1)),
    bee_hex_early_to_late_dist=observed,
    bee_hex_colour_shift_permutation_p=(exceed+1)/1000,
    early_green_receptor_background_abs=mean(abs(e$green_receptor_E-0.5)),
    late_green_receptor_background_abs=mean(abs(l$green_receptor_E-0.5)),
    delta_far_green_abs_late_minus_early=
      mean(abs(l$green_receptor_E-0.5))-mean(abs(e$green_receptor_E-0.5)),
    early_near_hex_background_r=mean(e$hex_background_r),
    late_near_hex_background_r=mean(l$hex_background_r),
    delta_near_hex_chroma_late_minus_early=
      mean(l$hex_background_r)-mean(e$hex_background_r),
    stringsAsFactors=FALSE)
}
if (!length(parts))stop("STAGE85_NO_VALID_ORIGINAL_AGE_COMPARISONS")
parts <- do.call(rbind,parts)
parts$bee_hex_colour_shift_BH_q_full_50_comparison_family <-
  p.adjust(parts$bee_hex_colour_shift_permutation_p,method="BH")
parts$independent_model_visible_0_09_BH50 <- (
  parts$bee_hex_early_to_late_dist>=0.09 &
  parts$bee_hex_colour_shift_BH_q_full_50_comparison_family<0.05
)

# Verify the 28 previously modelled taxa with the actual 28-source output.
# The new 50-family BH threshold is intentionally different, but CONTINUOUS
# contrast physics and identical flower part mappings MUST agree.
prev <- parts[parts$source_species_new_for_DOPI==0,,drop=FALSE]
if (nrow(prev)!=53L ||
    length(unique(prev$source_species))!=28L ||
    nrow(old_parts)!=53L) {
  stop("STAGE85_PREVIOUS_28_53_PARTS_DROPPED_OR_EXTRA")
}
sort_key <- function(df) order(df$source_species,df$original_flower_part)
ref <- old_parts[sort_key(old_parts),,drop=FALSE]
current <- prev[sort_key(prev),,drop=FALSE]
if (!identical(ref$source_species,current$source_species) ||
    !identical(ref$original_flower_part,current$original_flower_part)) {
  stop("STAGE85_OLD_28_SOURCE_PART_IDENTITIES_DONT_MATCH")
}
check <- c("bee_hex_early_to_late_dist",
 "early_green_receptor_background_abs",
 "late_green_receptor_background_abs",
 "delta_far_green_abs_late_minus_early",
 "early_near_hex_background_r",
 "late_near_hex_background_r",
 "delta_near_hex_chroma_late_minus_early")
diff <- sapply(check,function(cn) max(abs(ref[[cn]]-current[[cn]])))
if (any(!is.finite(diff))||any(diff>1e-7)) {
  print(diff)
  stop("STAGE85_PREVIOUS_28_BEE_RECEIVER_MEASURES_NOT_REPRODUCED")
}
write.csv(parts,file.path(output,"stage85_50_original_apis_green_hex_age_part_metrics.csv"),
          row.names=FALSE)
if (length(unresolved)) write.csv(do.call(rbind,unresolved),
  file.path(output,"stage85_true_original_incomplete_age_parts.csv"),row.names=FALSE)

species <- lapply(sort(unique(parts$source_species)),function(sp){
  a <- parts[parts$source_species==sp,,drop=FALSE]
  data.frame(source_species=sp,
    source_species_new_for_DOPI=as.integer(a$source_species_new_for_DOPI[1]),
    source_verified_comparable_age_parts=nrow(a),
    independent_model_visible_0_09_BH50_any=any(a$independent_model_visible_0_09_BH50),
    independent_model_visible_0_09_BH50_parts=sum(a$independent_model_visible_0_09_BH50),
    median_delta_far_green_abs=median(a$delta_far_green_abs_late_minus_early),
    median_delta_near_hex_chroma=median(a$delta_near_hex_chroma_late_minus_early),
    median_age_colour_shift_hex=median(a$bee_hex_early_to_late_dist),
    descriptive_far_maintained_near_reduced=as.integer(
       median(a$delta_far_green_abs_late_minus_early)>=0 &&
       median(a$delta_near_hex_chroma_late_minus_early)<0),
    source_no_functional_guide_or_distant_detection_distance_measured=TRUE,
    source_author_exact_taxon_48_of_219_group_status_unverified=TRUE)
})
species<-do.call(rbind,species)
write.csv(species,file.path(output,"stage85_50_original_apis_far_near_species.csv"),
          row.names=FALSE)

old_coh <- old_species[order(old_species$source_species),,drop=FALSE]
new_coh <- species[species$source_species_new_for_DOPI==0,,drop=FALSE]
new_coh <- new_coh[order(new_coh$source_species),,drop=FALSE]
if (!identical(old_coh$source_species,new_coh$source_species)) {
  stop("STAGE85_OLD_28_SPECIES_RECEPTOR_ROSTER_CHANGED")
}
diff_species=sapply(c("median_delta_far_green_abs",
 "median_delta_near_hex_chroma","median_age_colour_shift_hex"),
  function(cn) max(abs(old_coh[[cn]]-new_coh[[cn]])))
if (any(!is.finite(diff_species))||any(diff_species>1e-7)) {
  print(diff_species)
  stop("STAGE85_28_SOURCE_SPECIES_CONTINUOUS_RECEPTOR_REGRESSION")
}
new22 <- species[species$source_species_new_for_DOPI==1,,drop=FALSE]
old28 <- species[species$source_species_new_for_DOPI==0,,drop=FALSE]
status <- list(
  schema="stage85_true_original_50_early_late_Ohashi_Apis_D65_green_hex",
  original_source_spectrometer_species=50L,
  original_source_complete_age_species=nrow(species),
  source_previous_28_species_in_full_50=length(unique(prev$source_species)),
  source_additional_22_species_comparable_age_parts=nrow(new22),
  original_source_complete_flower_age_parts=nrow(parts),
  original_source_new_22_flower_age_parts=nrow(parts[parts$source_species_new_for_DOPI==1,,drop=FALSE]),
  original_source_unpaired_or_incomplete_parts=length(unresolved),
  source_28_old_continuous_physics_max_absolute_diff=max(diff_species,diff),
  previous_28_model_visible_BH53_species_source=5L,
  new_50_family_model_visible_species=sum(species$independent_model_visible_0_09_BH50_any),
  new_50_family_model_visible_old_28=sum(old28$independent_model_visible_0_09_BH50_any),
  new_50_family_model_visible_additional_22=sum(new22$independent_model_visible_0_09_BH50_any),
  new_22_species_far_green_contrast_lower_late=sum(new22$median_delta_far_green_abs<0),
  new_22_species_near_chromatic_contrast_lower_late=sum(new22$median_delta_near_hex_chroma<0),
  new_22_species_descriptive_far_maintained_near_reduced=sum(new22$descriptive_far_maintained_near_reduced),
  new_50_species_descriptive_far_maintained_near_reduced=sum(species$descriptive_far_maintained_near_reduced),
  pavo_version=as.character(packageVersion("pavo")),
  modeled_visual_system="Apis_mellifera_pavo_D65_green_foliage_vonKries_Ei_hexagon",
  original_part_sample_permutation_n=999L,
  original_perceptual_colour_hex_threshold=0.09,
  BH_multiple_test_family_size=nrow(parts),
  source_original_author_visible_classification_219_not_recomputed=TRUE,
  not_plant_native_Europe_or_actual_Bombus_choice_measurement=TRUE,
  source_no_scent_wind_learning_or_landing_measurement=TRUE
)
writeLines(jsonlite::toJSON(status,pretty=TRUE,auto_unbox=TRUE),
  file.path(output,"stage85_50_apis_true_original_source_receipt.json"))
cat("STAGE85_ORIGINAL_50_HONEYBEE_VISUAL_RECEPTOR_SOURCE",
  jsonlite::toJSON(status,auto_unbox=TRUE),"\n")
