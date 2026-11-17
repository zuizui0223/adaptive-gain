"""Stage76B external DoPI-v2 POSITIVE flower visitor macro validation.

Source-original 676,900 European DoPI v2 records (DOI
10.5281/zenodo.22876365, SHA256 b95d3084...), original 59,369 NHM botanical
text taxon labels and original corrected EuPPollNet species name universe.

Precisely distinguishes:
- study positive documented visitor channels from independent DIRECT counts;
- pollination evidence grade 1 (confirmed), 2 (pollen carriage), 3 (visitation);
  grade 4 excluded, unknown grades never negatives;
- one plant observed by BOTH guilds is not two independent plant species;
- source publication is NOT a field site, and DoPI may overlap EuPPollNet,
  GloBI or related literature.
- only external positive study/plant/guild records, not actual geographic
  visitors on island/GBIF occurrence/native origin of a specific individual.

Flower phenotype is original botanical text lexical hue, not photo or
species-average spectrometry or true spatial UV nectar-guide measurement.
No significance, new global causal pollination syndrome, weather/SDM, fitness.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,random,re,sys
from collections import Counter,defaultdict
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"floral_macro_stage75"))
from authentic_continental_text_signal_guild_macro import (
    source_text_trait,key
)
from importlib.util import spec_from_file_location,module_from_spec

SOURCE_DOPI_SHA="b95d3084399ed2c0978af2485801108a27d14e843b9fed2611934ea582b745c8"
SOURCE_DOPI_SIZE=384896230
SOURCE_NHM_SHA="b81ab96a2883e2b2e7f254a9e7ab62a34afaa0dfe62f0062d1677ba852dc686a"
SOURCE_EUPP_NET_SHA="475863c2b193dd9c1eaad848dae05a9f518b57446cad2661979ca582c7d88617"
EXPECTED_DOPI_ROWS=676900
GRADE_SCOPES={
  "positive_visits_or_pollen_123":frozenset(("1","2","3")),
  "pollen_evidence_12":frozenset(("1","2")),
  "confirmed_1":frozenset(("1",))
}
COMPARE=(("yellow","white"),("yellow","purple"))
MIN_STUDIES=10
BOOTSTRAPS=999
SEED=20261118
BEE_FAMILIES={"apidae","andrenidae","halictidae","colletidae","megachilidae","melittidae","stenotritidae"}
NO_ID={"","na","n/a","nan","none","null","unknown"}
DOI_RE=re.compile(r"10\.\d{4,9}/[^\s/]+",re.I)

def hash_stream(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda:f.read(1<<20),b""):
            h.update(block)
    return h.hexdigest()

def verified(path,expected):
    if hash_stream(path)!=expected:
        raise ValueError("STAGE76B_ORIGINAL_SOURCE_DIGEST_MISMATCH_"+str(Path(path).name))

def csv_rows(path):
    with Path(path).open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f))

def source_guild(row):
    o=key(row.get("pollinator_order"))
    f=key(row.get("pollinator_family"))
    p=key(row.get("pollinator_species"))
    if o!="hymenoptera":return ""
    if f not in BEE_FAMILIES:return ""
    if p.startswith("bombus ") and f=="apidae":return "Bombus"
    if f=="apidae" and p.startswith("bombus"):
        return "SOURCE_TAXON_UNRESOLVED"
    return "other_bee"

def doi_id(s):
    s=str(s or "").strip().casefold()
    if s in NO_ID:return ""
    found=DOI_RE.search(s)
    return found.group(0).rstrip(".,;)") if found else ""

def study_id(row):
    # same DoPI original source policy as fd GIFT bridge: DOI first,
    # fallback publication; neither proves time/site-specific replication.
    doi=str(row.get("doi") or "").strip().casefold()
    if doi and doi not in NO_ID:return doi
    pub=str(row.get("publication") or "").strip().casefold()
    return pub if pub not in NO_ID else ""

def accepted_text_hues(nhm,eu):
    accepted=set()
    matched=set()
    source_dois=set()
    for r in eu:
        tax=key(r["Original_plant_accepted_name_literal"])
        accepted.add(tax)
        if r["NHM_text_name_match"]=="1":
            matched.add(tax)
        source_doi=doi_id(r.get("Author_study_DOI"))
        if source_doi:source_dois.add(source_doi)
    if len(accepted)!=1408 or len(matched)!=963:
        raise ValueError("STAGE76B_ORIGINAL_1408_963_SOURCE_SCOPE_CHANGED")
    target={};col=0
    for row in nhm:
        tax=key(row.get("taxon"))
        if tax not in matched:continue
        t=source_text_trait(row)
        col+=bool(t["source_colour_recorded"])
        hue=t["source_exclusive_lexical_hue"]
        if hue:target[tax]=hue
    if col!=809 or len(target)!=233:
        raise ValueError("STAGE76B_ORIGINAL_809_COLOUR_233_SINGLE_HUE_CHANGED")
    return target,source_dois

def original_positive_doPI_dedup(csv_path,hues):
    # Source frame built on plant names + actual positive recorded species
    # WITHOUT using B/O target guild to choose ecological source studies.
    needed={"plant_species","pollinator_species","pollinator_order",
            "pollinator_family","pollination","doi","publication"}
    positive=defaultdict(lambda:defaultdict(set))
    guild=defaultdict(lambda:defaultdict(lambda:defaultdict(set)))
    summaries=Counter()
    all_source_pubs=set()
    with Path(csv_path).open(encoding="utf-8-sig",errors="replace",newline="") as f:
        reader=csv.DictReader(f)
        if not needed.issubset(set(reader.fieldnames or [])):
            raise ValueError("STAGE76B_SOURCE_DOPI_ORIGINAL_HEADERS_CHANGED")
        for r in reader:
            summaries["original_DOPI_v2_source_rows"]+=1
            plant=key(r["plant_species"])
            if plant not in hues:continue
            summaries["source_rows_literal_NHM_lexical_hue_plant_match"]+=1
            grade=str(r.get("pollination") or "").strip()
            study=study_id(r)
            if not study or grade not in {"1","2","3"}:
                summaries["matched_source_rows_missing_pub_or_admitted_grade"]+=1
                continue
            all_source_pubs.add(study)
            # All positive rows with source accepted original evidence grade
            # define an observable plant set (not one inferred negative).
            for scope,grades in GRADE_SCOPES.items():
                if grade in grades:
                    positive[scope][study].add(plant)
            group=source_guild(r)
            if group not in ("Bombus","other_bee"):
                summaries["matched_source_rows_not_Bombus_or_other_bee"]+=1
                continue
            summaries["matched_positive_source_bee_rows_g"+grade+"_"+group]+=1
            for scope,grades in GRADE_SCOPES.items():
                if grade in grades:
                    guild[scope][study][group].add(plant)
    if summaries["original_DOPI_v2_source_rows"]!=EXPECTED_DOPI_ROWS:
        raise ValueError("STAGE76B_NOT_ORIGINAL_676900_DOPI_SOURCE_RECORDS")
    return positive,guild,all_source_pubs,dict(summaries)

def compare_published_source_hue_composition(positive,guild,hues,scope,pair):
    # Pre-guild source frames are based on hue-positive source plants for each
    # original study; only then are actual source B/O guild records opened.
    a,b=pair
    cohorts={
        study:{tax for tax in plants if hues[tax] in pair}
        for study,plants in positive.get(scope,{}).items()
    }
    eligible={
        study:plants for study,plants in cohorts.items()
        if len({hues[sp] for sp in plants})==2
    }
    outcomes=[];gates=Counter()
    for study,plants in sorted(eligible.items()):
        bnames=guild[scope][study].get("Bombus",set()) & plants
        onames=guild[scope][study].get("other_bee",set()) & plants
        if not bnames or not onames:
            gates["one_source_guild_no_positive_documentation"]+=1
            continue
        pB=sum(hues[sp]==a for sp in bnames)/len(bnames)
        pO=sum(hues[sp]==a for sp in onames)/len(onames)
        # Equal genus audit requires >=2 identical genus names documented on
        # both original positive guild sides, and a hue pair genuinely present
        # after this genus restriction. Not a full plant phylogeny.
        bg=defaultdict(set);og=defaultdict(set)
        for tax in bnames:bg[tax.split()[0]].add(tax)
        for tax in onames:og[tax.split()[0]].add(tax)
        same=set(bg)&set(og)
        genus_diffs=[]
        for gen in same:
            ba=bg[gen];oa=og[gen]
            if {hues[sp] for sp in ba|oa}=={a,b}:
                genus_diffs.append(sum(hues[sp]==a for sp in ba)/len(ba)-
                                    sum(hues[sp]==a for sp in oa)/len(oa))
        outcomes.append({
            "study":study,
            "source_plant_species_with_documented_any_visitor":len(plants),
            "source_plant_species_Bombus_positively_documented":len(bnames),
            "source_plant_species_other_bee_positively_documented":len(onames),
            "source_plant_species_both_guilds_documented":len(bnames&onames),
            "source_positive_study_difference_yellow_share_Bombus_minus_other_bee":pB-pO,
            "source_same_genus_positive_hue_comparable_counts":len(genus_diffs),
            "source_same_genus_equal_difference_if_identifiable":
                sum(genus_diffs)/len(genus_diffs) if genus_diffs else None,
        })
    return eligible,outcomes,dict(gates)

def study_bootstrap(vals):
    if len(vals)<MIN_STUDIES:return None
    rng=random.Random(SEED)
    data=[]
    for _ in range(BOOTSTRAPS):
        sample=[vals[rng.randrange(len(vals))] for _ in vals]
        data.append(sum(sample)/len(sample))
    data.sort()
    return [data[int(.025*(len(data)-1))],data[int(.975*(len(data)-1))]]

def audit(path_nhm,path_eu,path_dopi):
    for p,sha in ((path_nhm,SOURCE_NHM_SHA),
                  (path_eu,SOURCE_EUPP_NET_SHA),
                  (path_dopi,SOURCE_DOPI_SHA)):
        verified(p,sha)
    if path_dopi.stat().st_size!=SOURCE_DOPI_SIZE:
        raise ValueError("STAGE76B_SOURCE_DOPI_BYTES_NOT_VERIFIED")
    hues,euDOI=accepted_text_hues(csv_rows(path_nhm),csv_rows(path_eu))
    positive,guild,pubs,source_counts=original_positive_doPI_dedup(path_dopi,hues)
    results={}
    for scope in GRADE_SCOPES:
        for pair in COMPARE:
            keyname=scope+"__"+pair[0]+"_vs_"+pair[1]
            cohort,outcomes,gates=compare_published_source_hue_composition(
                positive,guild,hues,scope,pair)
            vals=[x["source_positive_study_difference_yellow_share_Bombus_minus_other_bee"]
                  for x in outcomes]
            genus_vals=[x["source_same_genus_equal_difference_if_identifiable"]
                        for x in outcomes
                        if x["source_same_genus_equal_difference_if_identifiable"] is not None]
            annotated_count=sum(bool(doi_id(x["study"]) and doi_id(x["study"]) in euDOI)
                                 for x in outcomes)
            results[keyname]={
              "source_sample_selection_only_positive_documented_flowers_before_target_guild":True,
              "source_studies_with_both_positive_hue_group_plants_before_guild_outcome":len(cohort),
              "source_studies_with_Bombus_and_other_bee_both_positively_documented":len(outcomes),
              "source_studies_with_source_DOPI_DOI_exactly_in_EuPPollNet_DOI":
                 annotated_count,
              "unknown_original_study_overlap_remains_unresolved":True,
              "source_yellow_documentation_share_Bombus_minus_other_bee_mean_if_positive":
                 sum(vals)/len(vals) if vals else None,
              "source_study_bootstrap_descriptive_95_if_at_least_10_studies":
                 study_bootstrap(vals),
              "source_study_documented_guild_contrast_positive":sum(v>0 for v in vals),
              "source_study_documented_guild_contrast_negative":sum(v<0 for v in vals),
              "source_study_documented_guild_contrast_zero":sum(v==0 for v in vals),
              "source_studies_with_informative_shared_genus":len(genus_vals),
              "source_shared_genus_mean_documented_guild_contrast_if_any":
                 sum(genus_vals)/len(genus_vals) if genus_vals else None,
              "source_shared_genus_study_bootstrap_only_if_at_least_10_studies":
                 study_bootstrap(genus_vals),
              "source_uninformative_reason_counts":gates,
              "positive_species_guild_membership_NOT_relative_visitation_rate":True,
              "study_documented_guild_coaccess_not_pollinator_preference":True,
              "source_DOI_or_publication_key_not_verifiable_same_site_or_time":True,
              "source_plant_traits_NOT_direct_UVguide_spectra":True,
              "source_visitor_absence_NOT_estimated":True,
              "confirmatory_significance_or_causal_plant_selection_estimated":False,
            }
    return {
      "schema":"stage76b_extant_DoPI_v2_2026_original_multi_publication_external_guild_macro",
      "source_original_DoPI_data_DOI":"10.5281/zenodo.22876365",
      "source_original_DOPI_676900_records_sha256":SOURCE_DOPI_SHA,
      "source_DOPI_384896230_bytes_verified":True,
      "source_original_NHM_lexically_single_hue_species":len(hues),
      "source_exact_EuPPollNet_recorded_plant_species_scope":963,
      "original_DOPI_source_counts":source_counts,
      "original_distinct_publications_with_any_source_positive_lexical_hue":len(pubs),
      "source_compared_against_original_euppollnet_study_DOIs":len(euDOI),
      "external_provider_not_proven_study_disjoint":True,
      "observed_visitors_on_island_populations_not_recorded":True,
      "original_DOPI_2026_European_visitor_evidence_not_global_guild":True,
      "source_original_macro_study_hue_guild_coverage":results,
      "positive_only_not_true_guild_absence":True,
      "global_Bombus_native_climate_model_estimated":False,
      "causal_evolutionary_hue_trait_or_UV_motif_effect_estimated":False,
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--original-NHM",type=Path,required=True)
    p.add_argument("--original-Stage69-networks",type=Path,required=True)
    p.add_argument("--original-DoPI-v2",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args()
    d=audit(a.original_NHM,a.original_Stage69_networks,a.original_DoPI_v2)
    a.outdir.mkdir(parents=True,exist_ok=True)
    (a.outdir/"original_2026_DOPI_posvisits_233_NHM_hue_macro_guild_receipt.json").write_text(
        json.dumps(d,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    print("STAGE76B_REAL_DOPI_233_NHM_VISUAL_HUE_518PUB_EXTERNAL_MACRO",
          json.dumps(d,sort_keys=True))
    print("NO_ISLAND_GUILD_OBSERVATIONS_NO_GUILD_ABSENCES_NO_FAKE_SPECTRA")
if __name__=="__main__":
    main()
