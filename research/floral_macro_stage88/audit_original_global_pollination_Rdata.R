#!/usr/bin/env Rscript
# Stage88B audit genuine Wang et al (2025) global mode Rdata, not inferred wind.
# Dryad DOI 10.5061/dryad.73n5tb35w, original file #4049686,
# original source SHA256 dfb34e3ce42bb07bdae6e2dea71de3653155670bc3032bc11e5f2d58303759e6
args <- commandArgs(trailingOnly=TRUE)
if(length(args)!=2L)stop("usage: audit_original...R <original.Rdata> <outdir>")
dir.create(args[[2]],recursive=TRUE,showWarnings=FALSE)
env<-new.env(parent=baseenv())
objects<-load(args[[1]],envir=env)
if(!length(objects))stop("STAGE88_ORIGINAL_RDATA_HAS_NO_NAMED_OBJECTS")
json<-function(x) jsonlite::toJSON(x,auto_unbox=TRUE,pretty=TRUE,na="null",null="null")
listed<-lapply(objects,function(nm){
  obj<-get(nm,envir=env)
  cls<-class(obj)
  cols<-if(is.data.frame(obj))names(obj) else character(0)
  list(name=nm,class=cls,rows=if(is.data.frame(obj))nrow(obj) else NA_integer_,
       columns=cols[seq_len(min(length(cols),100L))])
})
print(paste("STAGE88_REAL_RDATA_OBJECT_NAMES",paste(objects,collapse="|")))
print(json(listed))
frames<-lapply(objects,function(nm) get(nm,envir=env))
valid<-which(vapply(frames,function(x) {
    is.data.frame(x) &&
      any(grepl("polmod|pollination|polmodbinary",names(x),ignore.case=TRUE)) &&
      any(grepl("genus_species|species|scientific",names(x),ignore.case=TRUE))
  },logical(1)))
if(length(valid)!=1L){
  writeLines(json(list(schema="stage88_Wang2025_Rdata_original_probe",
        source_objects=listed,source_species_pollination_join_ready=FALSE)),
      file.path(args[[2]],"stage88_original_Rdata_schema_diagnostic.json"))
  stop("STAGE88_REQUIRED_UNAMBIGUOUS_ORIGINAL_SPECIES_MODE_DATA_FRAME_NOT_FOUND")
}
x<-frames[[valid[[1]]]]
p_candidates<-names(x)[grepl("^PolModbinary$",names(x),ignore.case=TRUE)]
s_candidates<-names(x)[grepl("^Genus_species$",names(x),ignore.case=TRUE)]
if(length(p_candidates)!=1L||length(s_candidates)!=1L){
  print(names(x))
  stop("STAGE88_AUTHOR_EXACT_PolModbinary_Genus_species_COLUMN_NOT_FOUND")
}
m<-p_candidates[[1]];s<-s_candidates[[1]]
modecounts<-sort(table(ifelse(is.na(x[[m]]),"SOURCE_NA",trimws(as.character(x[[m]]))),useNA="ifany"),decreasing=TRUE)
sourcecols<-names(x)[grepl("source|data.*pol.*mod|note",names(x),ignore.case=TRUE)]
srcsample<-if(length(sourcecols))lapply(x[sourcecols],function(v)head(unique(as.character(v)),10L)) else list()
report<-list(
 schema="stage88B_authentic_Wang2025_global_179263_animal_wind_pollination_source_schema",
 original_archive_object_name=objects[[valid[[1]]]],
 original_source_data_frame_rows=nrow(x),
 original_data_frame_ncols=ncol(x),
 source_original_fields=names(x),
 original_pollination_code_column=m,original_species_column=s,
 source_true_pollination_code_frequencies=as.list(modecounts),
 original_mode_data_source_columns=sourcecols,
 original_source_data_source_example_values=srcsample,
 first_five_original_species_names=head(as.character(x[[s]]),5L),
 source_missing_pollination_is_unknown_not_wind=TRUE,
 source_category_labels_need_verbatim_verified_before_any_model=TRUE,
 source_179263_original_publication_figure_not_assumed_exact_source_denom=TRUE,
 source_does_not_represent_plant_local_native_occurrence=TRUE)
writeLines(json(report),file.path(args[[2]],"stage88B_original_Wang2025_Rdata_field_schema.json"))
print("STAGE88B_REAL_WANG_GLOBAL_POLLINATION_MODE_CODE_AND_SOURCE",json(report))

# Keep only original species-literal/pollination-mode/source-id for downstream
# actual validated species×region join. Do NOT publish a copy of the original
# source database in CI artifact; this file is temporary and deleted after join.
selected<-data.frame(original_species=as.character(x[[s]]),
 original_mode=as.character(x[[m]]),stringsAsFactors=FALSE)
if(length(sourcecols)) for(col in sourcecols)
  selected[[col]]<-as.character(x[[col]])
write.csv(selected,file.path(args[[2]],"TEMP_stage88_global_original_species_pollination_labels.csv"),row.names=FALSE,na="")
