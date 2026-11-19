"""Stage90A: quantify pseudoreplication by original native plant ranges and genera.

The earlier Stage89B GLOBAL study had 155 valid TDWG3 regions (113 GBIF
Bombus-positive) with >=10 explicitly one-hue documented source taxon
names in EACH of independently GIFT-labelled animal vs wind floras.
Every widely distributed plant occurs in multiple native TDWG3 regions.
Its repeated hue/mode label is NOT independent biological evolution.

Data MUST be original and checksum verified:
 GIFT3.2 independent source 5770 species labels (island run 34803493307),
 author original NHM 59369 botanical descriptions,
 official Kew WCVP 55775 region-native accepted species,
 and independent Stage89 367-region original crosswalk receipt.
No source phenotype inferred from genus or from missing taxon records.

The inverse-range-breadth weighted hue fraction in region r is
   sum_{sp native in r, hue h, source mode m} (1/N_native_regions(sp))
    / sum_{sp native in r, source single-hue, mode m} (1/N_native_regions(sp)).
And analogous within-genus equal-genus weights. This is a sensitivity to
native range frequency, not a phylogenetic PGLS or evolutionary transition.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,math,sys,zipfile
from collections import Counter,defaultdict
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/"floral_macro_stage87"))
sys.path.insert(0,str(BASE/"floral_macro_stage88"))
sys.path.insert(0,str(BASE/"floral_macro_stage89"))
from global_native_floral_signal_tdwg3 import load_nhm,wcvp_regions,HUES
from source_taxonomic_family_exclusion_native_flora import source_families
from gift32_independent_pollen_mode_global_native_coverage import original_gift_species

REFERENCE_ZIP_SHA="26ffa12c78a583743735d89575b6b8d4c4066a01da5b2a7e54aea531915bb7a8"
REFERENCE_MEMBER="stage89_original_GIFT32_native_animal_wind_unknown_367_TDWG3_hues.csv"
MODES=("animal","wind","unknown")
HUES_SEQUENCE=tuple(HUES)

def frozen_stage89_reference(path):
    raw=Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=REFERENCE_ZIP_SHA:
        raise ValueError("STAGE90_STAGE89_GIFT32_TRUE_NATIVE_COHORT_SOURCE_SHA_CHANGED")
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        rows=list(csv.DictReader(io.StringIO(z.read(REFERENCE_MEMBER).decode("utf-8-sig"))))
    if len(rows)!=1101:
        raise ValueError("STAGE90_ORIGINAL_367_REGION_3_SOURCE_MODE_ROWS_CHANGED")
    return {(r["TDWG_L3"],r["pollination_mode"]):r for r in rows}

def within_region_weighted(mode_taxa,traits,breadth,family):
    originals=[s for s in mode_taxa if traits[s]["explicit_single_hue"] is not None]
    counts=Counter(traits[s]["explicit_single_hue"] for s in originals)
    bygenus=defaultdict(list)
    for sp in originals:bygenus[sp.split()[0]].append(sp)
    b={sp:breadth[sp] for sp in originals}
    weights={sp:1./breadth[sp] for sp in originals}
    if any(not (0<weights[s]<=1) for s in originals):
        raise ValueError("STAGE90_GIFT_NATIVE_RANGE_BREADTH_WEIGHT_NOT_VALID")
    denom=sum(weights.values())
    inv_hue={h:sum(weights[s] for s in originals if traits[s]["explicit_single_hue"]==h)/denom
         if denom else None for h in HUES_SEQUENCE}
    inv_genus={}
    for h in HUES_SEQUENCE:
        vals=[]
        for group in bygenus.values():
            wtotal=sum(weights[s] for s in group)
            vals.append(sum(weights[s] for s in group if traits[s]["explicit_single_hue"]==h)/wtotal)
        inv_genus[h]=sum(vals)/len(vals) if vals else None
    ef=(denom**2/sum(w*w for w in weights.values())) if denom else None
    fams=Counter(family.get(s,"UNKNOWN_WCVP_FAMILY") for s in originals)
    out={
       "source_documented_one_hue_species":len(originals),
       "source_documented_one_hue_distinct_genera":len(bygenus),
       "source_documented_one_hue_unique_original_families":len(fams),
       "source_one_hue_inverse_range_weight_sum":denom,
       "source_one_hue_inverse_range_effective_number":ef,
       "source_one_hue_native_range_breadth_median":(
          sorted(b.values())[len(b)//2] if b else None),
       "source_one_hue_native_range_breadth_max":max(b.values()) if b else None,
       "source_one_hue_widest_native_species_fraction":(
          sum(1 for v in b.values() if v>=10)/len(b) if b else None),
       "source_one_hue_most_repeated_species_taxon":
          max(b,key=b.get) if b else None,
       "source_one_hue_family_top3":fams.most_common(3),
       "source_one_hue_original_hue_counts":dict(counts)}
    for h in HUES_SEQUENCE:
        out[f"hue_{h}_pooled_inverse_native_range"]=inv_hue[h]
        out[f"hue_{h}_genus_equal_inverse_native_range"]=inv_genus[h]
    return out

def analyze_source(gift_source,nhm_source,wcvp_source,stage89_reference,outdir):
    modes,gift_qc=original_gift_species(gift_source)
    trait,nhm_qc=load_nhm(nhm_source)
    regions,wcvp_qc=wcvp_regions(wcvp_source,trait)
    fam,fam_qc=source_families(wcvp_source,trait)
    prior=frozen_stage89_reference(stage89_reference)
    if len(regions)!=367 or len(set().union(*regions.values()))!=55775:
        raise ValueError("STAGE90_WCVP_ORIGINAL_GLOBAL_NATIVE_REGION_SOURCE_CHANGED")
    breadth=Counter(s for names in regions.values() for s in names)
    core=set(breadth)&set(modes)
    if len(core)!=3172 or sum(modes[s]=="wind" for s in core)!=612:
        raise ValueError("STAGE90_GIFT32_NATIVE_REGION_EXACT_MODE_COHORT_DRIFT")
    bymode={m:{s for s in core if modes[s]==m} for m in ("animal","wind")}
    bygenus=defaultdict(lambda:defaultdict(set))
    for mode,plants in bymode.items():
        for sp in plants:bygenus[sp.split()[0]][mode].add(sp)
    mixed={g:s for g,s in bygenus.items() if len(s["wind"])>0 and len(s["animal"])>0}
    mixed_w_hue={g:s for g,s in mixed.items() if
        any(trait[x]["explicit_single_hue"] is not None for x in s["wind"]) and
        any(trait[x]["explicit_single_hue"] is not None for x in s["animal"])}
    rows=[];region_common=Counter()
    mode_counters=defaultdict(Counter);original_tol=1e-10
    within_region_mixed=[]
    for code,sps in sorted(regions.items()):
        animal_spp={s for s in sps if s in bymode["animal"]}
        wind_spp={s for s in sps if s in bymode["wind"]}
        both_genus={g for g in {s.split()[0] for s in animal_spp}&
                    {s.split()[0] for s in wind_spp}}
        both_genus_hue={
          g for g in both_genus if
          any(s.split()[0]==g and trait[s]["explicit_single_hue"] is not None for s in animal_spp) and
          any(s.split()[0]==g and trait[s]["explicit_single_hue"] is not None for s in wind_spp)}
        within_region_mixed.append({"TDWG_L3":code,
           "source_genera_with_both_modes_in_same_native_region":len(both_genus),
           "source_genera_with_both_modes_AND_source_colour_in_same_native_region":len(both_genus_hue)})
        for m,mode_taxa in (("animal",animal_spp),("wind",wind_spp)):
            rec={"TDWG_L3":code,"pollination_mode":m}
            rec.update(within_region_weighted(mode_taxa,trait,breadth,fam))
            reference=prior.get((code,m))
            if reference is None:raise ValueError("STAGE90_MISSING_PRIOR_STAGE89_MODE_REGION")
            if rec["source_documented_one_hue_species"]!=int(reference["source_explicit_single_hue_species"]):
                raise ValueError("STAGE90_ORIGINAL_SOURCE_HUE_MODE_COUNTS_CHANGED")
            for h in HUES_SEQUENCE:
                for sourcekey in ("fraction_of_exclusive_documented","mean_of_genus_fractions"):
                    value=reference[f"hue_{h}_{sourcekey}"]
                    if value and rec["source_documented_one_hue_species"]>0:
                        if sourcekey=="fraction_of_exclusive_documented":
                            actual=(rec["source_one_hue_original_hue_counts"].get(h,0) /
                                rec["source_documented_one_hue_species"])
                        else:
                            genus_source=defaultdict(list)
                            for sp in mode_taxa:
                                if trait[sp]["explicit_single_hue"] is not None:
                                    genus_source[sp.split()[0]].append(sp)
                            actual=sum(sum(trait[s]["explicit_single_hue"]==h for s in g)/len(g)
                                for g in genus_source.values())/len(genus_source)
                        if abs(float(value)-actual)>original_tol:
                            raise ValueError("STAGE90_PREVIOUS_GIFT_367_REGION_HUE_METRIC_REGRESSION_"+h+"_"+m)
            for key in ("source_one_hue_family_top3","source_one_hue_original_hue_counts"):
                rec[key]=json.dumps(rec[key],ensure_ascii=False,sort_keys=True)
            rows.append(rec)
            mode_counters[m]["native_source_taxon_region_incidence"]+=len(mode_taxa)
            mode_counters[m]["colour_documented_native_source_incidence"]+=rec["source_documented_one_hue_species"]
    if len(rows)!=734:raise ValueError("STAGE90_367_X_TWO_SOURCE_MODE_REGION_MATRIX_CHANGED")
    bymode_summary={}
    for m in ("animal","wind"):
        source=sorted(breadth[sp] for sp in bymode[m])
        one_hue={sp for sp in bymode[m] if trait[sp]["explicit_single_hue"] is not None}
        x=sorted(breadth[sp] for sp in one_hue)
        bymode_summary[m]={
          "original_native_source_distinct_species":len(bymode[m]),
          "original_native_source_distinct_genera":len({s.split()[0] for s in bymode[m]}),
          "original_source_lexical_one_hue_species":len(one_hue),
          "original_source_lexical_one_hue_genera":len({s.split()[0] for s in one_hue}),
          "original_source_native_region_incidence":sum(source),
          "native_region_breadth_species_median":source[len(source)//2] if source else None,
          "native_region_breadth_one_hue_median":x[len(x)//2] if x else None,
          "native_region_breadth_one_hue_max":max(x) if x else None,
          "one_hue_species_native_in_ge_10_TDWG_regions":sum(v>=10 for v in x),
          "source_regional_lexical_hue_incidence":mode_counters[m]["colour_documented_native_source_incidence"],
          "source_region_range_repetition_is_not_independent_origin":True}
    outdir.mkdir(parents=True,exist_ok=True)
    def write(path,records):
        keys=sorted(set().union(*(r.keys() for r in records)))
        with path.open("w",newline="",encoding="utf-8") as f:
            wr=csv.DictWriter(f,fieldnames=keys)
            wr.writeheader();wr.writerows(records)
    write(outdir/"stage90_original_367_TDWG_GIFT_modes_inverse_native_range_hues.csv",rows)
    write(outdir/"stage90_original_TDWG_regions_with_both_modes_source_genera.csv",within_region_mixed)
    support={
       "schema":"stage90A_global_exact_GIFT_native_WCVP_species_recurrence_pollination_mode_support",
       "input_artifacts":{"Stage89_GIFT32_artifact_sha256":REFERENCE_ZIP_SHA,
                          "GIFT32_GIFT_source_artifact_sha256":gift_qc["archive_sha256"],
                          "original_NHM_N=59369_sha256":nhm_qc.get("source_sha256"),
                          "original_WCVP_N=55775_sha256":wcvp_qc.get("source_sha256")},
       "original_source_global_TDWG_regions":len(regions),
       "original_WCVP_native_source_flora_species":len(breadth),
       "source_GIFT32_mode_assigned_species":len(core),
       "source_mode_arm_range_and_hue_support":bymode_summary,
       "source_total_distinct_GIFT_mode_genera":len(bygenus),
       "source_genera_with_both_animal_and_wind_modes":len(mixed),
       "source_genera_with_both_modes_and_explicit_hue_in_both":len(mixed_w_hue),
       "source_both_mode_genera_original_taxonomic_names":sorted(mixed),
       "source_both_mode_and_hue_genera_original_names":sorted(mixed_w_hue),
       "original_regions_with_any_both_mode_native_genus":sum(x["source_genera_with_both_modes_in_same_native_region"]>0 for x in within_region_mixed),
       "original_regions_with_any_both_mode_hue_genus":sum(x["source_genera_with_both_modes_AND_source_colour_in_same_native_region"]>0 for x in within_region_mixed),
       "source_original_prior_367x3_GIFT_hue_fractions_all_reproduced":True,
       "source_original_WCVP_accepted_family_meta":{k:v for k,v in fam_qc.items() if k!="WCVP_taxonomic_original_header"},
       "this_range_weighting_is_NOT_a_phylogenetic_model":True,
       "source_mode_source_compiled_not_field_observed_for_each_native_site":True,
       "source_missing_pollination_status_UNKNOWN_not_wind":True,
       "source_plant_hue_words_not_true_olfactory_visual_information":True,
       "source_no_true_bumblebee_preference_odour_flight_cost_landing":True}
    (outdir/"stage90_source_native_range_breadth_genus_support_receipt.json").write_text(
        json.dumps(support,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("STAGE90_REAL_SOURCE_GIFT_WCVP_NATIVE_BREADTH_AND_GENUS_SUPPORT",
        json.dumps({k:v for k,v in support.items() if k in (
          "source_genera_with_both_animal_and_wind_modes",
          "source_genera_with_both_modes_and_explicit_hue_in_both",
          "source_mode_arm_range_and_hue_support",
          "original_regions_with_any_both_mode_native_genus",
          "original_regions_with_any_both_mode_hue_genus",
          "source_original_prior_367x3_GIFT_hue_fractions_all_reproduced")},sort_keys=True),flush=True)
    return support

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--GIFT32-source-artifact",type=Path,required=True)
    p.add_argument("--NHM-original",type=Path,required=True)
    p.add_argument("--WCVP-original",type=Path,required=True)
    p.add_argument("--Stage89-derived-artifact",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    args=p.parse_args()
    analyze_source(args.GIFT32_source_artifact,args.NHM_original,args.WCVP_original,
                   args.Stage89_derived_artifact,args.outdir)
if __name__=="__main__":main()
