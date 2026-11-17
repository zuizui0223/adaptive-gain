"""Stage74E: transparent paired 2021 source UV-guide experiment contrast.

Source: 54 actual randomized arrays across 27 high/low elevation
array PAIRS, including 377 independently recounted initial bee/fly visits.
Contrast: fraction first visits to LARGE vs SMALL floral guide, paired
ambient minus reduced UV. Source published related effect, NOT a new
selection result, not a multi-species macro effect.

Uncertainty: paired-source-block nonparametric descriptive bootstrap,
seed and denominator fixed, no p-value, not a fit of original SAS model.
Retain source pairs with zero first visits in an arm as uninformative for
fractions, NOT biologically absent pollinators.
"""
from __future__ import annotations
import argparse
import json
import random
from collections import Counter,defaultdict
from pathlib import Path

SOURCE_SHA="d66d12f3dbfc83b3fe6e854b69f9e5f768a1c3f973c0db5368176e17264ace59"
BOOTSTRAPS=5000
SEED=20261117

def bootstrap_ci(diffs,nboot=BOOTSTRAPS,seed=SEED):
    if not diffs:return None
    rng=random.Random(seed)
    means=[]
    for _ in range(nboot):
        sample=[diffs[rng.randrange(len(diffs))] for _ in range(len(diffs))]
        means.append(sum(sample)/len(sample))
    means.sort()
    return [means[int(0.025*(len(means)-1))],
            means[int(0.975*(len(means)-1))]]

def source_verified_pair_frame(receipt):
    if receipt.get("source_workbook_sha256")!=SOURCE_SHA:
        raise ValueError("STAGE74E_ORIGINAL_AUTHOR_FIELD_SOURCE_SHA_NOT_VERIFIED")
    data=receipt["original_UV_light_factor_source_grain"]
    if data["source_raw_first_visit_counts_sum"]!=377:
        raise ValueError("STAGE74E_ORIGINAL_FIRST_VISITS_NOT_377")
    if data["original_distinct_randomized_array_ids"]!=54:
        raise ValueError("STAGE74E_ORIGINAL_ARRAYS_NOT_54")
    if data["original_distinct_source_elevation_population_date_pair_keys"]!=27:
        raise ValueError("STAGE74E_ORIGINAL_EXPERIMENT_PAIRS_NOT_27")
    if not receipt["source_ambient_vs_reduced_real_first_visits_count_admitted"]:
        raise ValueError("STAGE74E_ORIGINAL_VISITS_NOT_ALL_DISCRETE")
    if not receipt["source_this_is_one_plant_species_not_macro_taxonomic_replication"]:
        raise ValueError("STAGE74E_MACRO_ECOLOGICAL_SCOPE_MISLABELLED")
    return receipt["source_original_UV_light_array_treatment_visits"]

def analyze(arrays):
    counts=defaultdict(Counter)
    within=defaultdict(dict)
    array_ids=set()
    for r in arrays:
        aid=r["original_array_id"]
        if aid in array_ids:raise ValueError("STAGE74E_DUPLICATE_EXPERIMENTAL_ARRAY")
        array_ids.add(aid)
        elevation=r["original_elevation"]
        arm=r["original_array_treatment"]
        if arm not in ("ambient_uv","reduced_uv"):
            raise ValueError("STAGE74E_SOURCE_TREATMENT_NOT_BINARY_UV")
        if elevation not in ("high","low"):
            raise ValueError("STAGE74E_SOURCE_ELEVATION_NOT_HIGH_LOW")
        l=int(r["n_original_first_visits_large_guide"])
        s=int(r["n_original_first_visits_small_guide"])
        n=int(r["n_original_first_visits_total"])
        bee=int(r["n_original_bee_first_visits"])
        fly=int(r["n_original_fly_first_visits"])
        if l<0 or s<0 or n!=l+s or bee+fly!=n:
            raise ValueError("STAGE74E_SOURCE_VISIT_COUNT_NOT_EXACT")
        group=counts[(elevation,arm)]
        group["first_visits_large"]+=l
        group["first_visits_small"]+=s
        group["first_visits_total"]+=n
        group["Bee_first_visits"]+=bee
        group["Fly_first_visits"]+=fly
        group["source_array_units"]+=1
        pair=(elevation,r["original_population"],
              r["original_date_Excel_serial"],r["original_pair_id"])
        if arm in within[pair]:
            raise ValueError("STAGE74E_DUPLICATE_SOURCE_ARRAY_TREATMENT_IN_PAIR")
        within[pair][arm]=(l,s)
    if len(arrays)!=54 or len(within)!=27:
        raise ValueError("STAGE74E_SOURCE_INDEPENDENT_DESIGN_GRAIN_CHANGED")
    breakdown=[]
    for (e,t),d in sorted(counts.items()):
        breakdown.append({"elevation":e,"UV_light_treatment":t,
             "first_visits_large_guide":d["first_visits_large"],
             "first_visits_small_guide":d["first_visits_small"],
             "total_first_visits":d["first_visits_total"],
             "recorded_bee_first_visits":d["Bee_first_visits"],
             "recorded_fly_first_visits":d["Fly_first_visits"],
             "independent_original_array_units":d["source_array_units"],
             "raw_large_guide_first_visit_fraction":
                 d["first_visits_large"]/d["first_visits_total"]
                 if d["first_visits_total"]>0 else None})
    observed_total=sum(x["total_first_visits"] for x in breakdown)
    if observed_total!=377:
        raise ValueError("STAGE74E_SOURCE_RECOUNT_NOT_377")
    changes=defaultdict(list)
    perpair=[]
    for (e,pop,date,pair),d in sorted(within.items()):
        if set(d)!={"ambient_uv","reduced_uv"}:
            raise ValueError("STAGE74E_ORIGINAL_PAIR_MISSING_TREATMENT")
        ambL,ambS=d["ambient_uv"]
        redL,redS=d["reduced_uv"]
        if ambL+ambS==0 or redL+redS==0:
            dlt=None
        else:
            dlt=(ambL/(ambL+ambS))-(redL/(redL+redS))
            changes[e].append(dlt)
        perpair.append({"source_elevation":e,"source_population":pop,
            "source_original_date_serial":date,"source_array_pair":pair,
            "large_first_visits_ambientUV":ambL,
            "small_first_visits_ambientUV":ambS,
            "large_first_visits_reducedUV":redL,
            "small_first_visits_reducedUV":redS,
            "paired_large_share_difference_ambient_minus_reduced":dlt,
            "independent_first_visit_array_pair_unit":True})
    groups={}
    for e in ("high","low"):
        n=sum(x["source_elevation"]==e for x in perpair)
        vals=changes[e]
        groups[e]={
         "source_randomized_array_pairs":n,
         "paired_arrays_with_visits_in_both_arms":len(vals),
         "source_pairs_missing_fraction_due_zero_visits":n-len(vals),
         "mean_difference_large_guide_choice_share":sum(vals)/len(vals) if vals else None,
         "paired_block_descriptive_bootstrap_CI_95":bootstrap_ci(vals),
         "n_pair_differences_positive":sum(x>0 for x in vals),
         "n_pair_differences_negative":sum(x<0 for x in vals),
         "n_pair_differences_equal_zero":sum(x==0 for x in vals),
        }
    contrast=None
    if changes["high"] and changes["low"]:
        x=changes["high"];y=changes["low"]
        contrast=sum(x)/len(x)-sum(y)/len(y)
        rng=random.Random(SEED)
        bs=[]
        for _ in range(BOOTSTRAPS):
            a=sum(x[rng.randrange(len(x))] for __ in range(len(x)))/len(x)
            b=sum(y[rng.randrange(len(y))] for __ in range(len(y)))/len(y)
            bs.append(a-b)
        bs.sort()
        ci=[bs[int(0.025*(len(bs)-1))],bs[int(0.975*(len(bs)-1))]]
    else:
        ci=None
    return {
      "source_true_visits_by_elevation_UV_and_guide":breakdown,
      "source_within_original_randomized_array_pair_differences":perpair,
      "source_paired_elevation_guide_UV_difference_descriptive":groups,
      "high_minus_low_paired_difference_of_large_guide_preference":contrast,
      "source_descriptive_high_minus_low_pair_bootstrap_interval_95":ci,
      "bootstrap_replicates":BOOTSTRAPS,"bootstrap_fixed_seed":SEED,
      "p_value_or_CI_from_original_SAS_not_claimed":True,
      "original_source_plant_fitness_not_observed":True,
      "source_single_species_high_low_elevation_only":True
    }

def run(source):
    original=json.loads(Path(source).read_text(encoding="utf-8"))
    arrays=source_verified_pair_frame(original)
    data=analyze(arrays)
    return {
       "schema":"stage74e_original_2021_author_experimental_firstvisits_paired_descriptive",
       "original_Zenodo_source_workbook_SHA256":SOURCE_SHA,
       "original_published_DOI":"10.1111/nph.17631",
       "observed_377_first_visits_recomputed_from_original_Excel":True,
       "actual_original_field_experimental_source":True,
       "preexisting_sensory_drive_mechanism_not_novelty_claim":True,
       "not_global_visual_signal_pollinator_macro_test":True,
       **data
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--verified-source",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args()
    a.outdir.mkdir(exist_ok=True,parents=True)
    result=run(a.verified_source)
    (a.outdir/"original_2021_377_first_visitor_pairs_UVguide_conditions.json").write_text(
       json.dumps(result,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    slim={k:v for k,v in result.items()
          if k not in ("source_within_original_randomized_array_pair_differences",)}
    print("STAGE74E_REAL_ORIGINAL_UVGUIDE_2021_SOURCE_ELEVATION_CONTRAST",
          json.dumps(slim,sort_keys=True))
    print("DESCRIPTIVE_PAIR_BOOTSTRAP_NOT_NEW_CAUSAL_UV_GUIDE_EFFECT")
if __name__=="__main__":
    main()
