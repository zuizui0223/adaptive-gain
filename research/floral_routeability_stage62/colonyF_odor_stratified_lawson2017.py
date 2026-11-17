"""Stage62: original Lawson 2017 B. terrestris wind backup, same-colony / same-reward-odour sensitivity.

Source original Excel already pinned & parsed in Stage61:
DOI 10.1098/rsos.170996; 72 bees grouped A/B/C/D n=18 each.
A and B share colony F; B and C share colony F; group D shares none
with A/B/C. Rewarding scents within F are imbalanced: A lav7/mint4,
B lav2/mint8, C lav5/mint3. This pre-registered source-defined sensitivity
compares A versus B, and B versus C only within F and within actual scent.

Original endpoints are per-bee counts of learning visits, correct landing
choices and reward landings. The original source did not record
first-cue/next-cue policies, wind × odor × vision full factorial, pollen
transfer, seed fitness, or a validated treatment-randomization log.
Exact constrained label-reassignment enumerations are *sensitivity
references*, never valid experimental randomization p-values or
independent-colony population inference. No original animal CSV uploaded.
"""
from __future__ import annotations
import argparse, itertools, json, math, statistics, sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"floral_routeability_stage61"))
from refit_2017_wind_bees_group_outcomes import (
    original_sheet_bytes,extract_rows,clean_original,ENDPOINTS)

COLONY="F"
ODORS=("lav","mint")
CONTRASTS=(("A","B"),("B","C"))
EXPECTED_GROUP_ODOR={
    "A":{"lav":7,"mint":4},
    "B":{"lav":2,"mint":8},
    "C":{"lav":5,"mint":3},
}
EXPECTED_GROUP_N={"A":11,"B":10,"C":8}
MAX_EXACT_REASSIGNMENTS=25000

def _selected(rows):
    if len(rows)!=72:
        raise ValueError("NO_GO_ORIGINAL_2017_72_BEE_FRAME_MISSING")
    sample=[r for r in rows if r["colony_as_published"]==COLONY
            and r["group"] in EXPECTED_GROUP_N]
    source_counts={g:Counter(r["reward_scent_as_published"] for r in sample
                             if r["group"]==g) for g in EXPECTED_GROUP_N}
    if (Counter(r["group"] for r in sample)!=Counter(EXPECTED_GROUP_N)
        or any(source_counts[g]!=Counter(EXPECTED_GROUP_ODOR[g])
               for g in EXPECTED_GROUP_N)):
        raise ValueError("NO_GO_ORIGINAL_2017_F_COLONY_BY_ODOR_COVERAGE_CHANGED")
    for r in sample:
        if any(r[e] is None for e in ENDPOINTS):
            raise ValueError("NO_GO_ORIGINAL_COLONY_F_MISSING_ENDPOINT_USE_NULL")
    return sample

def _weight_and_stats(data,left,right,metric):
    by_scent={}
    numerator=Fraction(0)
    total=0
    for odor in ODORS:
        l=[r[metric] for r in data if r["group"]==left
           and r["reward_scent_as_published"]==odor]
        u=[r[metric] for r in data if r["group"]==right
           and r["reward_scent_as_published"]==odor]
        if not l or not u:raise ValueError("NO_GO_NO_ODOR_COMMON_SUPPORT")
        delta=Fraction(sum(u),len(u))-Fraction(sum(l),len(l))
        by_scent[odor]={"n_left":len(l),"n_right":len(u),
                        "left_mean":float(Fraction(sum(l),len(l))),
                        "right_mean":float(Fraction(sum(u),len(u))),
                        "right_minus_left_exact":str(delta),
                        "right_minus_left_float":float(delta)}
        total+=len(l)+len(u)
        numerator+=delta*(len(l)+len(u))
    return numerator/total,by_scent

def exact_reference(data,left,right,metric):
    # Preserve original source colony F, reward-scent class and group
    # counts; it is NOT a true randomization distribution unless original
    # bee-treatment allocation was genuinely random within these strata.
    strata=[]
    n_possible=1
    for odor in ODORS:
        x=[r[metric] for r in data if r["group"] in (left,right)
           and r["reward_scent_as_published"]==odor]
        n_left=sum(r["group"]==left and r["reward_scent_as_published"]==odor
                   for r in data)
        n_right=sum(r["group"]==right and r["reward_scent_as_published"]==odor
                    for r in data)
        if n_left==0 or n_right==0 or len(x)!=(n_left+n_right):
            raise ValueError("NO_GO_PERMUTATION_COMMON_SUPPORT")
        choices=math.comb(len(x),n_left)
        n_possible*=choices
        if n_possible>MAX_EXACT_REASSIGNMENTS:
            raise ValueError("NO_GO_PERMUTATION_SPACE_TOO_LARGE")
        # The stratum comparison from all allowed reassignments.
        diffs=[]
        S=sum(x)
        for left_indices in itertools.combinations(range(len(x)),n_left):
            left_sum=sum(x[i] for i in left_indices)
            # difference (right group - left group).
            diffs.append(Fraction(S-left_sum,n_right)
                         -Fraction(left_sum,n_left))
        if len(diffs)!=choices:raise AssertionError("NO_GO_INCORRECT_EXACT_ENUMERATION")
        strata.append((len(x),diffs))
    observed,_=_weight_and_stats(data,left,right,metric)
    denom=sum(n for n,_ in strata)
    reference=sorted((Fraction(strata[0][0])*a + Fraction(strata[1][0])*b)/denom
                     for a in strata[0][1] for b in strata[1][1])
    if len(reference)!=n_possible:raise AssertionError("NO_GO_REFERENCE_CARDINALITY")
    # Descriptive rank under hypothetical label-exchangeability only.
    more_extreme=sum(abs(z)>=abs(observed) for z in reference)
    # Exact source finite-population quantiles, NOT sampling CI.
    percentile=lambda p:reference[int((len(reference)-1)*p)]
    return {
       "source_odor_constrained_hypothetical_label_reassignment_count":len(reference),
       "observed_equal_source_odor_pooled_standardized_difference":float(observed),
       "observed_equal_source_odor_pooled_standardized_difference_exact":str(observed),
       "reference_2p5_percentile_not_confidence_bound":float(percentile(.025)),
       "reference_50_percentile_not_population_null":float(percentile(.50)),
       "reference_97p5_percentile_not_confidence_bound":float(percentile(.975)),
       "hypothetical_fraction_as_extreme_not_an_experimental_p_value":
           float(Fraction(more_extreme,len(reference))),
       "original_bee_treatment_exchangeability_NOT_AUTHENTICATED":True,
       "stratified_reassignment_NOT_randomized_p_value":True,
       "original_2017_colony_F_is_one_biological_colony":True,
    }

def audit(original):
    data=_selected(original)
    rows= {}
    for left,right in CONTRASTS:
        key=left+"_to_"+right
        treated=[r for r in data if r["group"] in (left,right)]
        out={}
        for metric in ENDPOINTS:
            raw=Fraction(sum(r[metric] for r in treated if r["group"]==right),
                         sum(r["group"]==right for r in treated))-Fraction(
                         sum(r[metric] for r in treated if r["group"]==left),
                         sum(r["group"]==left for r in treated))
            standardized,by_scent=_weight_and_stats(treated,left,right,metric)
            out[metric]={
                "source_F_all_odor_raw_mean_right_minus_left":float(raw),
                "source_F_common_odour_strata_original":by_scent,
                "source_F_odor_pool_standardized_mean_right_minus_left":float(standardized),
                **exact_reference(treated,left,right,metric)
            }
        rows[key]={
           "n_bees_left":sum(r["group"]==left for r in treated),
           "n_bees_right":sum(r["group"]==right for r in treated),
           "original_endpoints":out}
    return {
        "status":"AUTHENTIC_LAWSON_2017_COLONY_F_ODOR_STRATIFIED_BACKUP_SENSITIVITY",
        "source_original_paper_DOI":"10.1098/rsos.170996",
        "source_original_bumblebee_wind_bees":72,
        "restricted_original_colony_id":COLONY,
        "n_source_F_bees_A_B_C":len(data),
        "original_F_colony_group_odor_counts":EXPECTED_GROUP_ODOR,
        "source_compared_edges_only":["A_to_B","B_to_C"],
        "source_original_wind_no_CtoD_shared_colony":True,
        "observational_comparisons":rows,
        "no_source_validated_treatment_randomization":True,
        "no_real_p_value_or_replicated_colony_inference":True,
        "published_existing_wind_visual_backup_NOT_a_novel_result":True,
        "no_2017_per_bee_cue_order_decision_route_measurement":True,
        "no_landing_failure_pollen_seed_fitness":True,
        "not_a_full_2x2x2_wind_odour_visual_interaction":True
    }

def main():
    original=clean_original(extract_rows(original_sheet_bytes()))
    output=audit(original)
    dest=Path("stage62_original_2017_common_colony_odour")
    dest.mkdir(exist_ok=True)
    (dest/"Lawson2017_author_source_colonyF_odour_confound_sensitivity.json").write_text(
       json.dumps(output,sort_keys=True,indent=2,ensure_ascii=False,allow_nan=False)+"\n",
       encoding="utf8")
    print("STAGE62_REAL_LAWSON_2017_WITHIN_F_ODOR_CORRECTED_CONTRASTS",
          json.dumps(output,sort_keys=True,ensure_ascii=False,allow_nan=False))
    print("NO_EXCHANGEABILITY_VALIDATED_OR_CUE_ORDER_OR_POLLEN_EFFECT")
if __name__=="__main__":
    main()
