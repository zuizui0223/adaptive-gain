"""Stage88C: actual 2025 global ANIMAL-vs-WIND species × original
NHM 59,369 flower-hue text × Kew WCVP native WGSRPD/TDWG level 3.

Strict species name agreement only; no inferred wind-pollination from
an unrecorded source mode, nonshowy green flower, genus or family.
Separate documented SOURCE animal, wind, and missing/ambiguous.

Inputs: authentic RData-extracted original Genus_species, PolModbinary,
DataSourceof PolMod (previous original-RData SHA validated), original
NHM compact text sha, real official 2026 WCVP ZIP sha. Author source
classifications are compiled/inferred across taxonomic lineages and
must not be represented as repeated in-field pollination observations.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,math,sys
from pathlib import Path
from collections import Counter,defaultdict
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"floral_macro_stage87"))
from global_native_floral_signal_tdwg3 import (
    load_nhm,wcvp_regions,strict_name,HUES
)
MODES=("animal","wind","unknown")
# Literal codes MUST be author source verified prior to acceptance.
MODE_LITERAL={
    "animal":"animal",
    "animal pollination":"animal",
    "animal-pollination":"animal",
    "biotic":"animal", # source textual mode, not measured beetle/bee guild
    "wind":"wind",
    "wind pollination":"wind",
    "wind-pollination":"wind",
    "anemophily":"wind",
    "insect":"animal",
    "insect pollination":"animal",
}
MISSING={"","na","nan","none","null","unknown","not available"}

def norm_mode(s,author_numeric_mapping=None):
    t=str(s or "").casefold().strip()
    if t in MISSING:return "unknown"
    if t in MODE_LITERAL:return MODE_LITERAL[t]
    if author_numeric_mapping and t in author_numeric_mapping:
        return author_numeric_mapping[t]
    raise ValueError("STAGE88C_UNREVIEWED_AUTHOR_MODE_VALUE_"+repr(t)[:70])

def read_source_mode(path,numeric_map):
    df={};counts=Counter();source_values=Counter();conflicts=set()
    with Path(path).open("r",newline="",encoding="utf-8-sig") as f:
        r=csv.DictReader(f)
        if not {"original_species","original_mode"}<=set(r.fieldnames or []):
            raise ValueError("STAGE88C_RDATA_ORIGINAL_SOURCE_SPECIES_MODE_EXPORT_INCOMPLETE")
        source_cols=[c for c in r.fieldnames if c not in ("original_species","original_mode")]
        source_attrib={}
        for row in r:
            counts["original_source_global_rows"]+=1
            sp=strict_name(row["original_species"])
            if sp is None:
                counts["source_unresolvable_to_strict_binomial"]+=1;continue
            mode=norm_mode(row["original_mode"],numeric_map)
            source_values[mode]+=1
            if mode=="unknown":
                counts["original_missing_mode_not_wind"]+=1;continue
            old=df.get(sp)
            if old is not None and old!=mode:
                conflicts.add(sp)
            df[sp]=mode
            if source_cols:
                source_attrib[sp]="|".join(str(row.get(c) or "")[:100] for c in source_cols)
    for sp in conflicts:
        df.pop(sp,None);source_attrib.pop(sp,None)
    counts["original_unique_strict_source_species_with_resolved_mode"]=len(df)
    counts["original_conflicting_same_binomial_mode_labels_excluded"]=len(conflicts)
    counts["source_mode_class_counts_for_source_rows"]=dict(source_values)
    counts["source_mode_original_attribution_columns"]=source_cols
    return df,source_attrib,dict(counts)

def group_mode(sp,mode,traits):
    t=traits[sp]
    return t

def summarize_one_region(code,source_names,mode_map,traits):
    out={}
    for mode in MODES:
        taxa=[sp for sp in source_names if mode_map.get(sp,"unknown")==mode]
        nc=len(taxa)
        counts=Counter();genus=defaultdict(Counter);genus_mode=set()
        for sp in taxa:
            x=traits[sp]; g=x["genus"];genus_mode.add(g)
            if x["colour_documented"]:counts["color_documented"]+=1
            if x["explicit_single_hue"]:
                h=x["explicit_single_hue"]
                counts["exclusive"]+=1
                counts["hue_"+h]+=1
                genus[g][h]+=1
            if x["positive_spot_text"]:counts["positive_spot"]+=1
            if x["petal_max_width_cm"] is not None:counts["reported_petal_width"]+=1
            if x["corolla_tube_max_length_cm"] is not None:counts["reported_tube_length"]+=1
        rec={"TDWG_L3":code,"pollination_mode":mode,
            "source_WCVP_native_NHM_species_count":nc,
            "source_native_unique_genera":len(genus_mode),
            "source_NHM_flower_colour_documented_species":counts["color_documented"],
            "source_explicit_single_hue_species":counts["exclusive"],
            "source_spot_word_positive_only_species":counts["positive_spot"],
            "source_flower_width_positive_documentation":counts["reported_petal_width"],
            "source_corolla_tube_length_positive_documentation":counts["reported_tube_length"],
            "source_colour_documentation_fraction":
                counts["color_documented"]/nc if nc else "",
            "source_spot_word_positive_rate_of_reported_NOT_guide_true_prevalence":
                counts["positive_spot"]/counts["color_documented"] if counts["color_documented"] else "",
            "source_unknown_mode_is_missing_NOT_wind":True,
            "source_mode_is_global_species_label_NOT_individual_pollen_transfer":True}
        for h in HUES:
            rec["hue_"+h+"_count"]=counts["hue_"+h]
            rec["hue_"+h+"_fraction_of_exclusive_documented"]=(
                counts["hue_"+h]/counts["exclusive"] if counts["exclusive"] else "")
            gr=[gcnt[h]/sum(gcnt.values()) for gcnt in genus.values() if sum(gcnt.values())]
            rec["hue_"+h+"_mean_of_genus_fractions"]=sum(gr)/len(gr) if gr else ""
        out[mode]=rec
    assert sum(v["source_WCVP_native_NHM_species_count"] for v in out.values())==len(source_names)
    return out

def recompute_global(traits,range_by_region,modes,source_attrib):
    rows=[];species_all=set().union(*range_by_region.values())
    source_exact=set(modes)&species_all
    source_global=Counter(modes[sp] for sp in source_exact)
    for code,taxa in sorted(range_by_region.items()):
        group=summarize_one_region(code,taxa,modes,traits)
        for m in MODES: rows.append(group[m])
    bymode={}
    for m in MODES:
        one=[r for r in rows if r["pollination_mode"]==m]
        bymode[m]={
          "original_native_region_count":sum(r["source_WCVP_native_NHM_species_count"]>0 for r in one),
          "original_native_species_region_incidence":sum(r["source_WCVP_native_NHM_species_count"] for r in one),
          "regions_with_at_least_10_explicit_single_hue_species":
            sum(r["source_explicit_single_hue_species"]>=10 for r in one),
          "regions_with_at_least_25_explicit_single_hue_species":
            sum(r["source_explicit_single_hue_species"]>=25 for r in one),
          "regions_with_at_least_50_explicit_single_hue_species":
            sum(r["source_explicit_single_hue_species"]>=50 for r in one)}
    report={
       "schema":"stage88C_original_Wang2025_animal_wind_floral_native_global_TDWG3",
       "source_original_WCVP_native_plant_species":len(species_all),
       "source_original_Wang2025_source_mode_strict_matched_species":len(source_exact),
       "source_original_Wang2025_exact_species_animal_vs_wind_counts":dict(source_global),
       "source_matched_original_modes_taxa_source_attribution_rows":sum(bool(source_attrib.get(sp,"")) for sp in source_exact),
       "source_original_367_native_region_modes":len(range_by_region),
       "source_original_all_three_modes_per_region":len(rows),
       "source_spatial_mode_composition_coverage":bymode,
       "source_global_original_taxonomy_concordance_exact_names_only":True,
       "source_unmatched_or_missing_species_mode_unknown_not_wind":True,
       "source_source_mode_compiled_or_inferred_not_source_observed_each_field_site":True,
       "source_animal_mode_includes_nonbee_pollination_not_same_as_Bombus_use":True,
       "source_true_nectar_guide_olfaction_learning_landing_missing":True}
    if len(range_by_region)!=367 or len(species_all)!=55775:
        raise ValueError("STAGE88C_PRIOR_GLOBAL_WCVP_NHM_SOURCE_COHORT_CHANGED")
    return rows,report

def write_csv(path,rows):
    if not rows:raise ValueError("STAGE88C_NO_SOURCE_GLOBAL_MODE_MATRIX")
    names=sorted(set().union(*(set(x) for x in rows)))
    with Path(path).open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=names);w.writeheader();w.writerows(rows)

def run(original_mode_csv,nhm_csv,wcvp_zip,outdir,numeric_map):
    mode,source_attrib,counts=read_source_mode(original_mode_csv,numeric_map)
    traits,nhm=load_nhm(nhm_csv)
    regions,wcvp=wcvp_regions(wcvp_zip,traits)
    rows,report=recompute_global(traits,regions,mode,source_attrib)
    report["source_original_global_mode_dataset_QA"]=counts
    report["source_original_NHM_QA"]=nhm
    report["source_original_WCVP_QA"]=wcvp
    outdir.mkdir(exist_ok=True,parents=True)
    write_csv(outdir/"stage88C_original_global_367_TDWG_native_animal_wind_unknown_hue_composition.csv",rows)
    (outdir/"stage88C_original_global_pollination_mode_floral_trait_spatial_coverage.json").write_text(
        json.dumps(report,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("STAGE88C_GLOBAL_SOURCE_ANIMAL_WIND_MODE_FLORAL_REGION_COVERAGE",json.dumps({
        "matched_taxa":len(set(mode)&set().union(*regions.values())),
        "matched_animal_wind":report["source_original_Wang2025_exact_species_animal_vs_wind_counts"],
        "mode_region":report["source_spatial_mode_composition_coverage"]},sort_keys=True),flush=True)
    return report

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--original-global-pollination-mode-csv",type=Path,required=True)
    p.add_argument("--original-NHM",type=Path,required=True)
    p.add_argument("--original-Kew-WCVP",type=Path,required=True)
    p.add_argument("--author-numeric-animal-code",default="")
    p.add_argument("--author-numeric-wind-code",default="")
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args()
    x={}
    if a.author_numeric_animal_code and a.author_numeric_wind_code:
        x={a.author_numeric_animal_code:"animal",a.author_numeric_wind_code:"wind"}
    elif a.author_numeric_animal_code or a.author_numeric_wind_code:
        raise ValueError("STAGE88C_AUTHOR_MODE_MAPPING_REQUIRES_BOTH_CODES")
    run(a.original_global_pollination_mode_csv,a.original_NHM,a.original_Kew_WCVP,a.outdir,x)
if __name__=="__main__":main()
