"""Stage86: authentic DoPI v2 strict source metadata x 49 Ohashi Apis receptor taxa.

Scientific goal: count *source-independent ecological comparison opportunities*
added by Stage85 compared with Stage83, without relabelling any DoPI
presence-only visitor record as absence, same-effort sampling, bee learning,
pollination fitness, effective odor plume or wind-at-flower.

This deliberately DOES NOT fit guild "preference" coefficients from
heterogeneous positive-only literature interaction records.
"""
from __future__ import annotations
import argparse,collections,csv,hashlib,io,json,math,sys,tempfile,zipfile
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/"floral_macro_stage84"))
from audit_real_dopi_v2_ohashi_eupp_power import (
    DOPI_URL,DOPI_BYTES,DOPI_MD5,normalized_name,normalized_doi,
    source_site_key,guild,download_source,
)

STAGE85_SOURCE_ZIP_SHA="fd49543ccbc27631e37ccff25d7fc7ab17def7f2b8f9365658d272d24d25097d"
STAGE85_SOURCE_ARTIFACT=14414838373
STAGE85_SPECIES="stage85_true_original_derived_50_receiver/stage85_50_original_apis_far_near_species.csv"
STAGE85_RECEIPT="stage85_true_original_derived_50_receiver/stage85_50_apis_true_original_source_receipt.json"
STAGE85_VALID_EARLY_LATE=49
RECEPTOR_SIGNALS=(
   "median_delta_far_green_abs","median_delta_near_hex_chroma",
   "median_age_colour_shift_hex","descriptive_far_maintained_near_reduced",
)
CONDITIONS=("ALL_METADATA","AUTHOR_DO_DIRECT","DO_PLANT_AND_INSECT_ALL","DO_ALL_AND_POLLEN_GRADE_1_2")

def source_traits(path):
    raw=Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=STAGE85_SOURCE_ZIP_SHA:
        raise ValueError("STAGE86_SOURCE_REAL_STAGE85_ZIP_SHA_CHANGED")
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        species=list(csv.DictReader(io.StringIO(z.read(STAGE85_SPECIES).decode("utf-8-sig"))))
        meta=json.loads(z.read(STAGE85_RECEIPT))
    if (len(species)!=49 or
        int(meta.get("original_source_complete_age_species",0))!=49 or
        int(meta.get("original_source_complete_flower_age_parts",0))!=82 or
        int(meta.get("source_previous_28_species_in_full_50",0))!=28 or
        int(meta.get("source_additional_22_species_comparable_age_parts",0))!=21):
        raise ValueError("STAGE86_ORIGINAL_STAGE85_49_28_21_DENOMINATOR_CHANGED")
    traits={};new=set();old=set()
    for r in species:
        sp=normalized_name(r["source_species"])
        if sp is None or sp in traits:raise ValueError("STAGE86_RECEPTOR_TAXON_NAME_NOT_UNIQUE")
        values={c:float(r[c]) for c in RECEPTOR_SIGNALS}
        if not all(math.isfinite(v) for v in values.values()):
            raise ValueError("STAGE86_RECEPTOR_NAN_NOT_ADMITTED")
        if not values["descriptive_far_maintained_near_reduced"] in (0,1):
            raise ValueError("STAGE86_RECEPTOR_DISCORDANCE_NOT_BINARY")
        traits[sp]=values
        (new if str(r["source_species_new_for_DOPI"])=="1" else old).add(sp)
    if len(traits)!=49 or len(new)!=21 or len(old)!=28 or new&old:
        raise ValueError("STAGE86_ORIGINAL_STAGE85_49_DISTINCT_SPECIES_CHANGED")
    # Explicitly guard the known source age-incomplete Houttuynia,
    # not misreported Firmiana where a second part has a complete pair.
    if "houttuynia cordata" in traits or "firmiana simplex" not in traits:
        raise ValueError("STAGE86_ORIGINAL_SOURCE_MISSING_TAXON_IDENTITY_INCORRECT")
    return traits,new,old,meta

def source_doi_site(row):
    """Source DOI/site key is an *opportunity*, never a common-effort network."""
    doi=normalized_doi(row.get("doi"))
    key=source_site_key(row,doi)
    return key,doi

def record_stratum(row):
    method=str(row.get("methodology") or "").strip().upper()
    plant=str(row.get("plant_survey") or "").strip().casefold()
    poll=str(row.get("pollinator_survey") or "").strip().casefold()
    grade=str(row.get("pollination") or "").strip()
    result=["ALL_METADATA"]
    if method=="DO":
        result.append("AUTHOR_DO_DIRECT")
        if plant=="all" and poll=="all":
            result.append("DO_PLANT_AND_INSECT_ALL")
            if grade in ("1","2"):
                result.append("DO_ALL_AND_POLLEN_GRADE_1_2")
    return result

def add_site(sites,key,sp,visitor_guild,source_values):
    group=sites.get(key)
    if group is None:
        group={"plant_names":set(),"bee_species":collections.defaultdict(set),
               "species_by_guild":collections.defaultdict(set),
               "source_methods":set(),"survey_pairs":set(),
               "source_record_count":0}
        sites[key]=group
    group["plant_names"].add(sp)
    group["source_record_count"]+=1
    group["source_methods"].add(source_values["methodology"])
    group["survey_pairs"].add((source_values["plant_survey"],source_values["pollinator_survey"]))
    if visitor_guild in ("BOMBUS","OTHER_BEE"):
        group["bee_species"][sp].add(visitor_guild)
        group["species_by_guild"][visitor_guild].add(sp)

def quantify_sites(sites,traits,new,old):
    out={}
    for label in CONDITIONS:
        x=sites[label]
        # Explicitly require 2 distinct plants with source positive bee ID
        # before inspecting any visual trait score; no outside-window imputation.
        presize=[(key,g) for key,g in x.items() if len(g["plant_names"])>=2]
        opt=[]
        for key,g in presize:
            bees=g["bee_species"]
            if len(bees)<2:continue
            both=(g["species_by_guild"].get("BOMBUS",set()) and
                  g["species_by_guild"].get("OTHER_BEE",set()))
            if not both:continue
            names=set(bees)
            if len({t.split()[0] for t in names})<2:continue
            opt.append((key,g,names))
        cross_new=[(key,g,names) for key,g,names in opt if names&new]
        cross_old=[(key,g,names) for key,g,names in opt if names<=old]
        selected_plants=set().union(*(names for key,g,names in opt)) if opt else set()
        pubs={key[0] for key,g,names in opt}
        npubs={key[0] for key,g,names in cross_new}
        original_28_only_keys=[
            (key,g) for key,g in x.items()
            if len(g["plant_names"]&old)>=2 and
               len({t.split()[0] for t in g["plant_names"]&old})>=2 and
               len({sp for sp in g["bee_species"] if sp in old})>=2 and
               bool(g["species_by_guild"].get("BOMBUS",set())&old) and
               bool(g["species_by_guild"].get("OTHER_BEE",set())&old)
        ]
        contrasts={}
        for signal in RECEPTOR_SIGNALS:
            # This counts only metadata groups with distinct ORIGINAL
            # measured plant-stage properties; it is NOT a pollinator
            # preference/causal coefficient or nectar-guide discrimination.
            hits=[]
            for key,g,names in opt:
                vals={traits[sp][signal] for sp in names}
                if len(vals)>=2:hits.append((key,names))
            contrasts[signal]={
                "metadata_blocks_with_at_least_two_distinct_source_trait_values":len(hits),
                "source_original_DOIs_with_cross_species_contrast":len({k[0] for k,sps in hits}),
                "candidate_blocks_containing_a_new21_taxon":sum(bool(sps&new) for k,sps in hits)}
        counts=collections.Counter(key[0] for key,g,names in opt)
        weights=[c/sum(counts.values()) for c in counts.values()] if counts else []
        out[label]={
           "original_source_metadata_blocks_with_any_optical_species":len(x),
           "source_prebee_metadata_blocks_with_2_or_more_measured_plants":len(presize),
           "source_metadata_blocks_with_2_distinct_bee_visited_plants_two_genera_and_both_guilds":len(opt),
           "prior_original_28_only_candidate_blocks_same_filter":len(original_28_only_keys),
           "candidate_blocks_with_any_new_21_source_age_plant":len(cross_new),
           "candidate_blocks_restricted_to_old_28_source_plants":len(cross_old),
           "incremental_blocks_over_prior_28_only_definition":len(opt)-len(original_28_only_keys),
           "unique_normalized_original_DOIs_in_selected_blocks":len(pubs),
           "original_source_DOIs_with_new21_candidate":len(npubs),
           "selected_plant_species":len(selected_plants),
           "selected_new21_source_species":len(selected_plants&new),
           "original_DOI_effective_number_by_candidate_blocks":float(1/sum(w*w for w in weights)) if weights else 0.,
           "largest_one_DOI_fraction_of_candidate_blocks":float(max(weights)) if weights else 0.,
           "original_DOI_candidate_count_top5":[{"DOI":doi,"candidate_blocks":count} for doi,count in counts.most_common(5)],
           "source_receptor_predeclared_contrast_opportunity":contrasts,
           "source_same_DOI_location_year_month_is_not_same_observation_effort":True,
           "source_repeated_plant_taxa_do_not_mean_independent_phenotype_origins":True,
           "source_positive_only_bee_records_not_absence_or_flower_use_preference":True}
    return out

def scan_real_source(file,traits,new,old):
    n=0;n_named=0;method=collections.Counter()
    exact_plants=collections.Counter();guilds=collections.Counter()
    pub_by_taxon=collections.defaultdict(set);pubs=set()
    grade=collections.Counter();scope=collections.Counter()
    matched_pub_new=set();matched_pub_old=set()
    rows_by_source={"old_28":0,"new_21":0}
    bytaxonguild=collections.defaultdict(collections.Counter)
    sites={label:{} for label in CONDITIONS}
    unlocatable=0;recognized_source_site=0
    with Path(file).open(encoding="utf-8-sig",newline="") as f:
        reader=csv.DictReader(f)
        for row in reader:
            n+=1
            if n>1_200_000:raise ValueError("STAGE86_DOPI_SOURCE_UNEXPECTED_TOO_MANY_ROWS")
            name=normalized_name(row.get("plant_species"))
            if name not in traits:continue
            n_named+=1;exact_plants[name]+=1
            typ="new_21" if name in new else "old_28"
            rows_by_source[typ]+=1
            doi=normalized_doi(row.get("doi"))
            if doi:
                pubs.add(doi);pub_by_taxon[name].add(doi)
                (matched_pub_new if name in new else matched_pub_old).add(doi)
            vg=guild(row)
            guilds[vg]+=1;bytaxonguild[name][vg]+=1
            method[str(row.get("methodology") or "").strip()]+=1
            grade[str(row.get("pollination") or "").strip()]+=1
            plant_survey=str(row.get("plant_survey") or "").strip()
            poll_survey=str(row.get("pollinator_survey") or "").strip()
            scope[(plant_survey,poll_survey)]+=1
            key,doi=source_doi_site(row)
            if key is None:
                unlocatable+=1;continue
            recognized_source_site+=1
            vals={"methodology":str(row.get("methodology") or "").strip(),
                  "plant_survey":plant_survey,"pollinator_survey":poll_survey}
            for cond in record_stratum(row):
                add_site(sites[cond],key,name,vg,vals)
    if n!=676900 or len(traits)!=49:
        raise ValueError("STAGE86_SOURCE_COMPLETE_DOPI_676900_ROWS_OR_RECEPTOR_49_CHANGED")
    matched_species=set(exact_plants)
    if not matched_species<=set(traits):
        raise ValueError("STAGE86_TAXON_NAME_NOT_SOURCE_VERIFIED")
    new_count=matched_species&new
    old_count=matched_species&old
    species_analysable_both_guilds={sp for sp,g in bytaxonguild.items()
                                   if g["BOMBUS"]>0 and g["OTHER_BEE"]>0}
    result={
     "schema":"stage86_real_full_DoPI49_Apis_receptor_study_site_and_source_design_power_gate",
     "original_DoPI_v2_full_source_676900_rows":n,
     "original_measured_spectra_species_with_valid_early_late":49,
     "source_28_old_receptor_species":len(old),
     "source_21_new_receptor_species":len(new),
     "source_49_receptor_plant_species_in_DoPI":len(matched_species),
     "source_old_28_names_present":len(old_count),
     "source_new_21_names_present":len(new_count),
     "source_rows_in_all_49_real_original_taxa":n_named,
     "original_source_old_new_row_breakdown":rows_by_source,
     "source_unique_original_publication_DOIs_49_species":len(pubs),
     "original_new21_source_taxon_publication_DOIs":len(matched_pub_new),
     "original_old28_source_taxon_publication_DOIs":len(matched_pub_old),
     "source_DOIs_unique_to_new21_not_in_prior28":len(matched_pub_new-matched_pub_old),
     "source_DOIs_shared_between_old28_and_new21":len(matched_pub_new&matched_pub_old),
     "source_matched_taxa_with_BOTH_species_ranked_bee_guild_positive_rows":len(species_analysable_both_guilds),
     "source_new21_taxa_with_BOTH_guild_positive_rows":len(species_analysable_both_guilds&new),
     "source_record_guild_categories":dict(guilds),
     "source_methodologies":dict(method),
     "source_pollination_grade_frequency":dict(grade),
     "source_top10_survey_scope_pairs":[{"source_plant_survey":x,"source_pollinator_survey":y,"source_rows":c}
                                       for (x,y),c in scope.most_common(10)],
     "source_rows_without_exact_spatiotemporal_DOI":unlocatable,
     "source_rows_with_exact_spatiotemporal_DOI":recognized_source_site,
     "source_original_49_taxa_rows_per_species":dict(sorted(exact_plants.items())),
     "source_original_DOIs_per_49_measured_species":{k:len(v) for k,v in sorted(pub_by_taxon.items())},
     "source_original_guild_positive_rows_per_species":{k:dict(v) for k,v in sorted(bytaxonguild.items())},
     "source_candidate_metadata_design_gates":quantify_sites(sites,traits,new,old),
     "source_not_same_plant_population_as_2015_Japan_spectra":True,
     "source_not_plant_or_pollinator_survey_hours_or_visits_per_flower":True,
     "source_DOI_is_not_a_guarantee_of_unique_field_location_or_replication":True,
     "source_not_original_field_floral_age_or_true_nectar_guide_measurement":True,
     "source_no_behavioural_information_order_wind_plume_learning_or_landing":True}
    return result

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--stage85-derived-artifact-zip",type=Path,required=True)
    ap.add_argument("--outdir",type=Path,required=True)
    args=ap.parse_args()
    traits,new,old,meta=source_traits(args.stage85_derived_artifact_zip)
    args.outdir.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        path=Path(td)/"DoPI_dataset_2.0.csv"
        source=download_source(DOPI_URL,path,DOPI_BYTES,DOPI_MD5)
        result=scan_real_source(path,traits,new,old)
    result["original_DoPI_v2_publisher_bytes_and_MD5_verified"]=source
    result["source_49_species_apis_true_original_measurement_receipt"]=meta
    result["source_derived_inputs_only_no_original_archive_redistributed"]=True
    receipt=args.outdir/"stage86_DoPI49_true_original_source_spatiotemporal_network_power.json"
    receipt.write_text(json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    print("STAGE86_TRUE_SOURCE_DOPI_49_SPECIES_VISUAL_CUE_NETWORK_OPPORTUNITY",
       json.dumps({k:v for k,v in result.items() if isinstance(v,(int,bool))},sort_keys=True),flush=True)
    for label,z in result["source_candidate_metadata_design_gates"].items():
        print("STAGE86_CANDIDATE_DESIGN",label,json.dumps(
          {k:v for k,v in z.items() if isinstance(v,(int,float,bool))},sort_keys=True),flush=True)

if __name__=="__main__":main()
