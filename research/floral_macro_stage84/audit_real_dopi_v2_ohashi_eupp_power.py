"""Stage84 real source: DoPI v2 full 384,896,230-byte CSV x Ohashi 219 source
spectrometer folders x EuPP original accepted-flora and publication DOIs.

A count of DoPI visits is not a new origin of a floral phenotype. Source
species/dates/locations do not identify scent, learnability, true gust, landing
or individual-pollinator cue acquisition. Source survey methods constrain what
a positive interaction means, and absence of a visitor record is UNKNOWN.

Original source:
 Zenodo 10.5281/zenodo.22876365, DoPI_dataset_2.0.csv
 Original MD5 d1c76fc0fd4df6a6828550c5866e4af1
 Original byte length 384896230
 Ohashi et al 2015 Zenodo 4942515 original 285933377 ZIP, MD5
 d98ddd3b93fb79fdbaaa5eec5818c187.
"""
from __future__ import annotations
import argparse,collections,csv,hashlib,json,re,sys,tempfile,urllib.request,zipfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"floral_macro_stage79"))
from ohashi_2015_zip_central_directory_species_coverage import original_folders

DOPI_URL="https://zenodo.org/api/records/22876365/files/DoPI_dataset_2.0.csv/content"
DOPI_BYTES=384896230
DOPI_MD5="d1c76fc0fd4df6a6828550c5866e4af1"
DOPI_FILENAME="DoPI_dataset_2.0.csv"
OHASHI_URL="https://zenodo.org/api/records/4942515/files/Ohashi_etal.zip/content"
OHASHI_MD5="d98ddd3b93fb79fdbaaa5eec5818c187"
OHASHI_SHA="860ad9ef71d99efdda441fae00090ddb1dad0145f5c54a04b581b09490e718b7"
OHASHI_BYTES=285933377
EUPP_SHA="475863c2b193dd9c1eaad848dae05a9f518b57446cad2661979ca582c7d88617"
RECEPTOR_ZIP="9139935f10fbd94a8fb888d807af872c9e5289422249d138fb8a61ac799a0b2a"
RECEPTOR_MEMBER="stage81d_derived_bee_receptor_metrics/stage81d_original_28_apis_far_near_species.csv"
SCHEMA=(
  "publication","doi","methodology","pollinator_survey","plant_survey",
  "pollinator_species","pollinator_family","pollinator_order",
  "plant_species","plant_family","interactions","year","month",
  "latitude","longitude","country","habitat","pollination","record"
)
BEES={"apidae","andrenidae","colletidae","halictidae","megachilidae",
      "melittidae","stenotritidae"}
BINOMIAL=re.compile(r"^[a-z][a-z-]* [a-z][a-z-]*$")
DOI_RE=re.compile(r"^10\.\d{4,9}/\S+$")

def normalized_name(value):
    # Strict species-level Latin binomial ONLY. No synonym inference.
    x=" ".join(str(value or "").replace("_"," ").strip().casefold().split())
    return x if BINOMIAL.fullmatch(x) and x.split()[1] not in (
        "sp","spp","cf","aff","unknown","species","hybrid") else None

def normalized_doi(value):
    x=str(value or "").strip().casefold()
    for prefix in ("https://doi.org/","http://doi.org/",
        "https://dx.doi.org/","http://dx.doi.org/","doi:"):
        if x.startswith(prefix):x=x[len(prefix):]
    return x.rstrip(" .;,") if DOI_RE.fullmatch(x.rstrip(" .;,")) else None

def publication_id(study):
    return "23_24_25_ONE_PUBLISHED_STUDY" if str(study).split("_",1)[0] in {"23","24","25"} else str(study)

def download_source(url,target,expected_bytes,expected_md5,expected_sha=None):
    if not url.startswith("https://zenodo.org/api/records/"):
        raise ValueError("STAGE84_UNAPPROVED_ORIGINAL_SOURCE_HOST")
    h=hashlib.md5();sha=hashlib.sha256();n=0
    req=urllib.request.Request(url,headers={"User-Agent":"academic-pollinator-original-source-staging-v1",
                                             "Accept":"application/octet-stream,text/csv,*/*"})
    with urllib.request.urlopen(req,timeout=180) as response,target.open("wb") as out:
        if response.status not in (200,206):
            raise ValueError("STAGE84_ORIGINAL_SOURCE_HTTP_STATUS")
        while True:
            b=response.read(4*1024*1024)
            if not b:break
            out.write(b);h.update(b);sha.update(b);n+=len(b)
            if n>expected_bytes:raise ValueError("STAGE84_PUBLIC_SOURCE_OVERSIZED")
    if n!=expected_bytes or h.hexdigest()!=expected_md5 or (
            expected_sha and sha.hexdigest()!=expected_sha):
        raise ValueError("STAGE84_ORIGINAL_SOURCE_MD5_SHA_OR_SIZE_CHANGED")
    return {"original_url":url,"source_bytes":n,"source_md5":h.hexdigest(),
            "source_sha256":sha.hexdigest(),"original_author_checksum_verified":True}

def ohashi_universe(author_zip,receptor_zip):
    with zipfile.ZipFile(author_zip) as z:
        folders,exact,infra,unknown=original_folders(z.namelist())
    if len(folders)!=219 or len(exact)!=180 or len(infra)!=33 or len(unknown)!=6:
        raise ValueError("STAGE84_AUTHENTIC_219_SOURCE_FOLDER_ROSTER_CHANGED")
    raw=Path(receptor_zip).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=RECEPTOR_ZIP:
        raise ValueError("STAGE84_REAL_28_BEERECEPTOR_ARTIFACT_SHA_CHANGED")
    with zipfile.ZipFile(receptor_zip) as z:
        import io
        src=list(csv.DictReader(io.StringIO(z.read(RECEPTOR_MEMBER).decode("utf-8-sig"))))
    measured28={normalized_name(r["source_species"]) for r in src}
    if len(src)!=28 or len(measured28)!=28 or not measured28.issubset(set(exact)):
        raise ValueError("STAGE84_REAL_28_SOURCE_BEE_RECEPTOR_SPECIES_NOT_219_ROSTER")
    return set(exact),measured28,{"original_219_taxon_folders":len(folders),
        "original_exact_simple_binomial_taxa":len(exact),
        "original_infraspecific_names_unresolved_separately":len(infra),
        "original_other_folder_names_unresolved":len(unknown),
        "genuine_28_specifically_bee_receptor_modeled_source_taxa":len(measured28),
        "source_no_219_bee_receptor_values_inferred_from_folder_membership":True}

def eupp_dois(source_eupp):
    raw=Path(source_eupp).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=EUPP_SHA:
        raise ValueError("STAGE84_TRUE_ORIGINAL_EUPP_SHA_CHANGED")
    import io
    rows=list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
    if len(rows)!=18798:raise ValueError("STAGE84_TRUE_ORIGINAL_EUPP_18798_ROWS_CHANGED")
    dois={normalized_doi(x["Author_study_DOI"]) for x in rows}
    p={publication_id(x["Study_id"]) for x in rows}
    names={normalized_name(x["Original_plant_accepted_name_literal"]) for x in rows}
    dois.discard(None);names.discard(None)
    return dois,names,{"original_EuPP_plant_network_rows":len(rows),
         "original_EuPP_source_accepted_species":len(names),
         "original_EuPP_distinct_publication_keys":len(p),
         "original_EuPP_unique_normalized_DOIs":len(dois)}

def guild(row):
    p=str(row.get("pollinator_species") or "").strip().casefold()
    order=str(row.get("pollinator_order") or "").strip().casefold()
    fam=str(row.get("pollinator_family") or "").strip().casefold()
    if not p or not normalized_name(p):return "UNRESOLVED_POLLINATOR"
    if order!="hymenoptera" or fam not in BEES:return "NON_BEE_OR_UNRESOLVED"
    if p.startswith("bombus "):return "BOMBUS"
    return "OTHER_BEE"

def source_site_key(row,doi):
    # STRICT original identical time AND coordinate key; no arbitrary imputation.
    # Not all DoPI rows at the same coordinate are the same sampling design.
    country=str(row.get("country") or "").strip()
    year=str(row.get("year") or "").strip()
    month=str(row.get("month") or "").strip()
    lat=str(row.get("latitude") or "").strip()
    lon=str(row.get("longitude") or "").strip()
    habitat=str(row.get("habitat") or "").strip()
    if not (doi and country and year and month and lat and lon):return None
    try:
        if not (-90<=float(lat)<=90 and -180<=float(lon)<=180):return None
        if not 1<=int(float(month))<=12:return None
        if not 1800<=int(float(year))<=2026:return None
    except ValueError:return None
    return (doi,country,year,str(int(float(month))),lat,lon,habitat)

def scan_dopi(path,all180,measured28,eupp_dois_set,eupp_species_set):
    # DoPI original 'record' field is NOT assumed a globally unique row ID.
    # Audit collisions explicitly and do not discard/duplicate-generate visits.
    seen_records={}
    duplicated_record_keys=set()
    repeated_record_rows=0
    repeated_record_identical_rows=0
    repeated_record_conflicting_rows=0
    source_record_id_missing=0
    source_duplicate_examples=[]
    n=0;matched_180=0;matched_28=0
    plant_all=set();plant_180=set();plant_28=set()
    pub_all=set();pub_180=set();pub_28=set()
    matched_doi_by_species=collections.defaultdict(set)
    matched28_doi_by_species=collections.defaultdict(set)
    sample_method=collections.Counter();qual=collections.Counter()
    guild_counts_180=collections.Counter();guild_counts_28=collections.Counter()
    surveyed=collections.Counter();unknown_doi_28=0
    matched28_direct=0;all_doi_rows=0
    site=collections.defaultdict(lambda:{"plants":collections.defaultdict(set),
                                         "methods":set(),"plant_surveys":set(),"pollinator_surveys":set()})
    field_schema=[]
    with Path(path).open("r",encoding="utf-8-sig",errors="strict",newline="") as f:
        csv.field_size_limit(10_000_000)
        reader=csv.DictReader(f)
        field_schema=list(reader.fieldnames or [])
        if any(x not in field_schema for x in SCHEMA):
            raise ValueError("STAGE84_REAL_DOPI_V2_EXPECTED_31_COLUMN_SCHEMA_CHANGED")
        for row in reader:
            n+=1
            if n>1_200_000:raise ValueError("STAGE84_UNEXPECTED_ORIGINAL_DOPI_RECORD_COUNT")
            rid=str(row.get("record") or "").strip()
            if rid.casefold() in ("","na","n/a","none","null","unknown"):
                source_record_id_missing+=1
            else:
                # Use compact canonical 128-bit content digest for memory-safe
                # duplicate identity vs distinct interactions with reused ID.
                signature=hashlib.blake2b(("\\x1f".join(str(row.get(k) or "") for k in (
                    "publication","doi","plant_species","pollinator_species",
                    "interactions","year","month","latitude","longitude","methodology",
                    "pollination","country"))).encode("utf-8"),digest_size=16).digest()
                prior=seen_records.get(rid)
                if prior is None:seen_records[rid]=signature
                else:
                    repeated_record_rows+=1
                    duplicated_record_keys.add(rid)
                    if prior==signature:repeated_record_identical_rows+=1
                    else:repeated_record_conflicting_rows+=1
                    if len(source_duplicate_examples)<8:
                        source_duplicate_examples.append({
                           "source_reused_record_id":rid[:45],
                           "same_selected_original_row_fields":prior==signature,
                           "plant_species":str(row.get("plant_species") or "")[:70],
                           "pollinator_species":str(row.get("pollinator_species") or "")[:70],
                           "source_methodology":str(row.get("methodology") or "")[:70]})
            name=normalized_name(row.get("plant_species"))
            if name:plant_all.add(name)
            doi=normalized_doi(row.get("doi"))
            if doi:pub_all.add(doi);all_doi_rows+=1
            if name not in all180:continue
            matched_180+=1;plant_180.add(name)
            g=guild(row);guild_counts_180[g]+=1
            if doi:pub_180.add(doi);matched_doi_by_species[name].add(doi)
            if name not in measured28:continue
            matched_28+=1;plant_28.add(name);guild_counts_28[g]+=1
            study=str(row.get("publication") or "").strip()
            method=str(row.get("methodology") or "").strip()
            pollination=str(row.get("pollination") or "").strip()
            p_survey=str(row.get("plant_survey") or "").strip()
            poll_survey=str(row.get("pollinator_survey") or "").strip()
            sample_method[method or "UNKNOWN"]+=1
            qual[pollination or "UNKNOWN"]+=1
            surveyed[(p_survey or "UNKNOWN",poll_survey or "UNKNOWN")]+=1
            if doi:pub_28.add(doi);matched28_doi_by_species[name].add(doi)
            else:unknown_doi_28+=1
            # Explicitly report source-positive direct visits vs pollen inferred:
            low=method.casefold()
            if any(t in low for t in ("visit","observ","field")):matched28_direct+=1
            key=source_site_key(row,doi)
            if key and g in ("BOMBUS","OTHER_BEE"):
                site[key]["plants"][name].add(g)
                site[key]["methods"].add(method)
                site[key]["plant_surveys"].add(p_survey)
                site[key]["pollinator_surveys"].add(poll_survey)
    if n<500_000:
        raise ValueError("STAGE84_ORIGINAL_DOPI_BULK_FILE_NOT_FULLY_READ")
    site_co_two=0;site_co_both=0;site_co_both_two_genera=0;site_pub=set()
    for k,v in site.items():
        supported={sp:gg for sp,gg in v["plants"].items() if gg}
        if len(supported)<2:continue
        site_co_two+=1
        if "BOMBUS" in set().union(*supported.values()) and "OTHER_BEE" in set().union(*supported.values()):
            site_co_both+=1;site_pub.add(k[0])
            if len({x.split()[0] for x in supported})>=2:site_co_both_two_genera+=1
    new_pub=pub_28-eupp_dois_set
    common_pub=pub_28&eupp_dois_set
    extra_180=plant_180-measured28
    return {
        "source_record_rows_checked":n,
        "source_unique_nonblank_record_labels":len(seen_records),
        "source_record_label_missing_or_placeholder_rows":source_record_id_missing,
        "source_reused_record_labels":len(duplicated_record_keys),
        "source_repeated_record_label_rows":repeated_record_rows,
        "source_repeated_record_label_identical_selected_content_rows":repeated_record_identical_rows,
        "source_repeated_record_label_different_selected_content_rows":repeated_record_conflicting_rows,
        "source_reused_record_label_examples":source_duplicate_examples,
        "source_do_not_treat_record_label_as_unique_independent_pollination_event":True,
        "source_unchanged_source_rows_not_auto_deduplicated":True,
        "source_exact_original_header_columns":field_schema,
        "source_valid_binomial_plant_species_in_all_DOPI":len(plant_all),
        "source_total_unique_DOIs_with_records":len(pub_all),
        "source_rows_with_normalized_DOIs":all_doi_rows,
        "source_180_original_exact_binomial_spectrometer_taxa":{
            "source_strict_matched_source_taxa":len(plant_180),
            "source_strict_matched_records":matched_180,
            "original_spectrometer_species_with_DOPI_not_in_28_receptor_panel":len(extra_180),
            "matched_taxa_NOT_currently_bee_receptor_modelled":sorted(extra_180),
            "source_distinct_publication_DOIs":len(pub_180),
            "source_pollinator_guild_record_frequencies":dict(guild_counts_180)},
        "source_28_current_apis_receptor_taxa":{
            "source_exact_matched_species":len(plant_28),
            "source_exact_matched_species_names":sorted(plant_28),
            "source_matched_record_rows":matched_28,
            "source_record_rows_without_valid_DOI":unknown_doi_28,
            "source_unique_publication_DOIs":len(pub_28),
            "source_normalized_DOIs_shared_with_original_EUPP":len(common_pub),
            "source_normalized_DOIs_not_found_in_original_EUPP":len(new_pub),
            "source_DOIs_not_found_in_EUPP_NOT_ALL_independent_new_field_studies":True,
            "source_publications_new_DOI_records":sorted(new_pub)[:80],
            "source_pollinator_guild_record_frequencies":dict(guild_counts_28),
            "source_methodology_labels":dict(sample_method.most_common(30)),
            "source_pollination_evidence_code":dict(qual.most_common()),
            "source_plant_pollinator_survey_scope_pairs": [
                {"plant_survey":a,"pollinator_survey":b,"source_rows":v}
                for (a,b),v in surveyed.most_common(25)],
            "methodology_keyword_direct_field_visit_source_rows_NOT_verifiable_as_all_effective_pollination":matched28_direct,
            "source_explicit_same_DOI_country_year_month_coordinates_two_matched_species_keys":site_co_two,
            "source_site_candidate_two_species_with_both_Bombus_other_bee":site_co_both,
            "source_site_candidate_two_species_two_genera_both_guilds":site_co_both_two_genera,
            "source_DOIs_with_source_site_candidate_two_species_both_guilds":len(site_pub),
            "source_site_identity_is_not_verified_common_survey_effort":True,
            "source_nominal_record_count_is_not_visited_flower_abundance_offset":True,
            "source_missing_visitors_are_NOT_true_absences":True},
        "source_new_spectrometer_taxa_outside_current_28":sorted(extra_180),
        "source_same_original_EUPP_plant_names_present_in_DOPI_28":{
            "count":len(plant_28&eupp_species_set),
            "new_vs_EuPP_strict_28_taxa":len(plant_28-eupp_species_set)},
        "not_a_fitted_flower_signal_Bombus_effect":True,
        "no_measured_wind_odor_plume_approach_landing_or_cognition":True,
        "not_per_species_author_bee_visible_change_classes":True
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--eupp-source-accepted-plant-network",type=Path,required=True)
    ap.add_argument("--stage81d-receptor-zip",type=Path,required=True)
    ap.add_argument("--outdir",type=Path,required=True)
    a=ap.parse_args()
    a.outdir.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as scratch:
        root=Path(scratch)
        dopi=root/DOPI_FILENAME
        source_dopi=download_source(DOPI_URL,dopi,DOPI_BYTES,DOPI_MD5)
        ohashi=root/"Ohashi_etal.zip"
        source_ohashi=download_source(OHASHI_URL,ohashi,OHASHI_BYTES,OHASHI_MD5,OHASHI_SHA)
        exact180,measured28,roster=ohashi_universe(ohashi,a.stage81d_receptor_zip)
        # Small source roster survives as a derived-only provenance receipt even
        # if subsequent DoPI taxonomy checks find source integrity problems.
        (a.outdir/"stage84_original_219_source_name_180_strict_binomial_manifest.json").write_text(
            json.dumps({"original_2015_source_ohashi_archive_sha256":OHASHI_SHA,
                        "source_taxon_structure":roster,
                        "strict_180_original_author_taxa":sorted(exact180),
                        "current_28_actual_apis_receptor_modelled":sorted(measured28),
                        "not_all_219_source_taxa_have_reconstructed_receptor_values":True},
                       indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
        eupp_dois_set,eupp_species_set,eupp=eupp_dois(a.eupp_source_accepted_plant_network)
        result=scan_dopi(dopi,exact180,measured28,eupp_dois_set,eupp_species_set)
    result.update({"schema":"stage84_full_original_2026_DOPI_v2_Ohashi219_28_source_species_independence_audit",
        "source_original_DOPI_full_download_verified":source_dopi,
        "source_original_Ohashi_archive_verified":source_ohashi,
        "source_original_Ohashi_taxon_roster":roster,
        "original_EUPP_reference":eupp,
        "full_original_bulk_source_not_redistributed":True,
        "source_no_automatic_synonym_or_genus_level_substitution":True})
    (a.outdir/"stage84_original_DOPI_v2_Ohashi219_28_vs_EuPP_publication_coverage.json").write_text(
        json.dumps(result,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("STAGE84_ACTUAL_DOPI_V2_219_SPECTROMETER_28_RECEPTOR_EUPP_CROSSWALK",
      json.dumps({k:v for k,v in result.items() if k not in (
         "source_original_DOPI_full_download_verified","source_original_Ohashi_archive_verified",
         "source_original_Ohashi_taxon_roster","source_28_current_apis_receptor_taxa")},sort_keys=True),flush=True)
    print("STAGE84_TRUE_28_SOURCE_SUMMARY",
      json.dumps({k:v for k,v in result["source_28_current_apis_receptor_taxa"].items()
        if k not in ("source_publications_new_DOI_records","source_pollination_evidence_code",
                     "source_methodology_labels","source_plant_pollinator_survey_scope_pairs",
                     "source_exact_matched_species_names")},sort_keys=True),flush=True)

if __name__=="__main__":main()
