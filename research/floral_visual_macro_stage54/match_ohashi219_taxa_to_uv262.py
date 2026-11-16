"""Stage54: source-authenticated Ohashi 2015 219 spectral taxa × UV 262 accepted species crosswalk.

2015 source (Ohashi, Makino, Arikawa, Functional Ecology,
doi:10.1111/1365-2435.12420) original Zenodo zip central-directory
species directories, source MD5 and file size verified in Stage54.
219 original taxa include some infraspecific varieties and possible
multiple directories for one accepted biological species.

Map binomial strings with strict original GBIF exact, confidence >=95.
Cross-study UV evidence from original 262 accepted-key source artifact.
Do NOT label bee/butterfly/fly perceptible colour change per taxon merely
from an archive directory. Paper reports 48 bee, 97 butterfly, 28 fly
perceptible whole/partial age changes but tables and measured reflectance
values have not been read by this script.
"""
from __future__ import annotations

from collections import Counter,defaultdict
from concurrent.futures import ThreadPoolExecutor
import argparse,csv,json,re,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"floral_visual_macro_stage49"))
from match_literature_visual_taxa_gbif import lookup

SOURCE_TAXA=219
SOURCE_UV_ACCEPTED=262
SPECTRA_DOI="10.1111/1365-2435.12420"
ORIGINAL_ARCHIVE_MD5="md5:d98ddd3b93fb79fdbaaa5eec5818c187"
BINOMIAL=re.compile(r"^[A-Z][a-zA-Z-]+ [a-z][a-z-]+$")
INFRASPECIFIC_TOKENS={"var","subsp","ssp","f","forma","cf","aff","sp","spp"}


def parse_original_folder(folder):
    if not isinstance(folder,str) or not folder:
        return {"binomial":"","status":"SOURCE_FOLDER_UNRESOLVED"}
    parts=folder.split("_")
    if len(parts)<2:
        return {"binomial":"","status":"SOURCE_FOLDER_UNRESOLVED"}
    name=parts[0]+" "+parts[1]
    if parts[1].lower() in INFRASPECIFIC_TOKENS or not BINOMIAL.fullmatch(name):
        return {"binomial":"","status":"SOURCE_NOT_EXACT_BINOMIAL"}
    extra=parts[2:]
    return {
       "binomial":name,
       "status":"LEXICAL_BINOMIAL_FROM_AUTHENTIC_ORIGINAL_ZENODO_DIRECTORY",
       "infraspecific_or_additional_source_tokens":extra,
       "source_subspecific_rank_present":any(
           token.lower() in INFRASPECIFIC_TOKENS for token in extra),
       "species_key_not_guaranteed_unique_per_source_directory":True
    }


def validate_source_219(source):
    if (source.get("status")!="ORIGINAL_OHASHI_2015_219_SOURCE_SPECTRAL_TAXON_ZIP_DIRECTORY"
        or source.get("n_original_spectral_species_directory_names")!=SOURCE_TAXA
        or source.get("original_Zenodo_deposit_md5")!=ORIGINAL_ARCHIVE_MD5):
        raise ValueError("NO_GO_UNAUTHENTICATED_OHASHI_ORIGINAL_219_SOURCE")
    names=source.get("species_source_directory_names")
    if not isinstance(names,list) or len(set(names))!=SOURCE_TAXA:
        raise ValueError("NO_GO_OHASHI_219_ORIGINAL_DIRECTORY_NAMES")
    return sorted(names)


def validate_uv262(path):
    with Path(path).open(encoding="utf8",newline="") as h:
        rows=list(csv.DictReader(h))
    if len(rows)!=SOURCE_UV_ACCEPTED:
        raise ValueError("NO_GO_UV_262_ACCEPTED_ORIGINAL_SOURCE_COUNT")
    keys={r.get("gbif_accepted_species_key","") for r in rows}
    if len(keys)!=SOURCE_UV_ACCEPTED or not all(k.isdigit() for k in keys):
        raise ValueError("NO_GO_UV_262_GBIF_ACCEPTED_KEY_UNIQUE")
    return {r["gbif_accepted_species_key"]:r for r in rows}


def join(source_folders,gbif_results,uv262):
    if len(source_folders)!=SOURCE_TAXA:
        raise ValueError("NO_GO_OHASHI_SPECIES_DIRECTORY_COUNT")
    combined=[]
    for folder in source_folders:
        name=parse_original_folder(folder)
        tax=gbif_results.get(name.get("binomial"),{
             "taxonomy_status":"SOURCE_FOLDER_UNRESOLVED"})
        key=tax.get("gbif_accepted_usage_key")
        overlap=uv262.get(str(key)) if isinstance(key,int) else None
        combined.append({
          "original_2015_spectral_taxon_folder":folder,
          "source_original_binomial_unreconciled":name["binomial"],
          "source_infraspecific_tokens":"_".join(name.get("infraspecific_or_additional_source_tokens",[])),
          "original_directory_taxon_name_status":name["status"],
          "gbif_name_taxonomic_mapping_status":tax["taxonomy_status"],
          "gbif_accepted_species_key_or_missing":key or "",
          "2015_source_spectral_across_flower_age_available":"SOURCE_ZIP_DIRECTORY_ONLY",
          "2015_bee_perceptible_colour_change":"NOT_CLASSIFIED_FROM_SOURCE_DIRECTORY",
          "2015_butterfly_perceptible_colour_change":"NOT_CLASSIFIED_FROM_SOURCE_DIRECTORY",
          "2015_fly_perceptible_colour_change":"NOT_CLASSIFIED_FROM_SOURCE_DIRECTORY",
          "original_2016_2021_UV_accepted_source_overlap":bool(overlap),
          "original_UV_direct_measured_pattern_or_missing":(
             overlap["source_measured_UV_spatial_pattern_or_missing"] if overlap else ""),
          "source_2015_original_study_DOI":SPECTRA_DOI,
          "taxon_has_individual_literature_source_location":"NOT_ESTABLISHED",
          "not_a_biological_colour_change_negative_or_absence":True,
          "not_a_flower_signal_information_use_or_fitness_estimate":True
        })
    mapped=[r for r in combined if r["gbif_name_taxonomic_mapping_status"]=="EXACT_CONFIDENT_SPECIES_MAPPED"]
    unique={r["gbif_accepted_species_key_or_missing"] for r in mapped}
    overlapping={r["gbif_accepted_species_key_or_missing"] for r in mapped
                 if r["original_2016_2021_UV_accepted_source_overlap"]}
    return combined,{
       "status":"AUTHENTIC_OHASHI_2015_SOURCE_219_SPECTRAL_TAXA_GBIF_UV262_CROSSWALK",
       "n_original_spectral_age_sampled_taxon_directories":len(combined),
       "n_valid_original_binomial_candidates":sum(
           bool(r["source_original_binomial_unreconciled"]) for r in combined),
       "n_exact_high_confidence_GBIF_mapped_original_2015_taxon_directories":len(mapped),
       "n_distinct_accepted_GBIF_species_in_original_2015_spectra":len(unique),
       "n_distinct_accepted_species_also_in_UV262":len(overlapping),
       "n_species_unique_added_to_262_accepted_source_frame":len(unique-overlapping),
       "n_combined_unique_accepted_species_UV_and_spectral":len(uv262)+len(unique-overlapping),
       "2015_paper_summary_bee_perceptible_48_of_219_not_species_labels":True,
       "2015_paper_summary_butterfly_perceptible_97_of_219_not_species_labels":True,
       "2015_paper_summary_fly_perceptible_28_of_219_not_species_labels":True,
       "2015_original_Zenodo_zip_only_partial_range_audited":True,
       "no_false_visual_information_negative_from_unread_2015_spectra":True,
       "no_native_species_distribution_or_bee_effect_estimated":True
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--ohashi-original-source-index",required=True)
    p.add_argument("--UV262-source-accepted",required=True)
    args=p.parse_args()
    source=json.loads(Path(args.ohashi_original_source_index).read_text())
    folders=validate_source_219(source)
    uv=validate_uv262(args.UV262_source_accepted)
    names=sorted({parse_original_folder(f)["binomial"] for f in folders if parse_original_folder(f)["binomial"]})
    with ThreadPoolExecutor(max_workers=4) as ex:
        query=list(ex.map(lookup,names))
    resolved=dict(zip(names,query))
    rows,summary=join(folders,resolved,uv)
    output=Path("stage54_Ohashi219_UV262_taxon_bridge")
    output.mkdir(exist_ok=True)
    with (output/"Ohashi219_original_spectral_directory_GBIF_accepted_and_UV262_link.csv").open(
        "w",encoding="utf8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=list(rows[0]))
        w.writeheader();w.writerows(rows)
    (output/"original_Ohashi219_species_taxonomy_UV262_overlap_receipt.json").write_text(
       json.dumps(summary,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print("STAGE54_OHASHI219_REAL_SPECTRA_DIRECTORY_GBIF_UV262_OVERLAP",
          json.dumps(summary,sort_keys=True,ensure_ascii=False))
    print("NO_219_PERCEPTIBLE_COLOR_CHANGE_PER_SPECIES_STATE_YET")

if __name__=="__main__":
    main()
