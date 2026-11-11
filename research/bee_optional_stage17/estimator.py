"""Stage17 colony- and bee-equal injected synthetic curvature estimator.

Do not fit this to actual animal data without independent preregistration,
source-specific blinded pilot and ethical approval. No animal source included.
"""
from __future__ import annotations
from collections import defaultdict
from statistics import mean,stdev
from math import sqrt,isfinite
from scipy.stats import t as student_t
from allocation import audit,COSTS,MODES

def estimate_mock_ITT(assignments,validated):
    audit(assignments)
    if not isinstance(validated,list) or len(validated)!=len(assignments):
        raise ValueError("NO_GO_NOT_ALL_ASSIGNED_OUTCOMES")
    original={x["trial_id"]:x for x in assignments}
    seen=set();by_bee=defaultdict(lambda:defaultdict(list))
    for row in validated:
        tid=row.get("trial_id")
        if tid not in original or tid in seen:
            raise ValueError("NO_GO_UNKNOWN_OR_DUPLICATE_SOURCE_BEHAVIOR")
        seen.add(tid)
        a=original[tid]
        if row.get("source_is_synthetic_QA_only") is not True:
            raise ValueError("NO_GO_REAL_BEE_OBSERVATION_NOT_AUTHORIZED")
        if row.get("cost_tier")!=a["cost_tier"] or row.get("access_mode")!=a["access_mode"]:
            raise ValueError("NO_GO_ASSIGNED_MODE_COST_CHANGED")
        mass=row.get("verified_consumed_sucrose_mg")
        if type(mass) not in (int,float) or not isfinite(mass) or mass<0:
            raise ValueError("NO_GO_MISSING_REAL_INTAKE_OR_NONFINITE")
        if row.get("sensor_status") not in ("measured","verified_no_intake"):
            raise ValueError("NO_GO_SENSOR_FAILURE_IS_NOT_ZERO")
        n=row.get("physical_leaf_requests")
        if type(n) is not int or n not in (0,1,2):
            raise ValueError("NO_GO_INVALID_SOURCE_REQUEST_COUNT")
        action=row.get("first_action")
        if (n==0)!=(action=="SKIP"):
            raise ValueError("NO_GO_INFERRED_SKIP_NOT_RECORDED")
        choice=row.get("final_target_choice")
        if choice not in (0,1,"no_choice"):
            raise ValueError("NO_GO_INVALID_SOURCE_TARGET_CHOICE")
        by_bee[a["colony_id"],a["bee_id"]][a["cost_tier"],a["access_mode"]].append(
            {"intake":mass,"leaf_requests":n,"skipped":int(n==0),
             "correct":int(choice==a["correct_target"]),"choice":choice})
    if seen!=set(original):
        raise ValueError("NO_GO_MISSING_ALL_ASSIGNED_SAMPLE")
    per_colony=defaultdict(list)
    for (col,bee),cells in sorted(by_bee.items()):
        if set(cells)!={(c,m) for c in COSTS for m in MODES} or any(len(x)!=8 for x in cells.values()):
            raise ValueError("NO_GO_NOT_EIGHT_SOURCE_TRIALS_PER_BEE_CELL")
        cell_means={(tier,mode):{feature:mean(x[feature] for x in records)
                   for feature in ("intake","leaf_requests","skipped","correct")}
                   for (tier,mode),records in cells.items()}
        D={cost:cell_means[cost,"contingent"]["intake"]-
                cell_means[cost,"precommit"]["intake"] for cost in COSTS}
        K=D["medium"]-(D["low"]+D["high"])/2
        by_cost={tier:{
            "mean_leaf_requests":mean(cell_means[tier,mode]["leaf_requests"] for mode in MODES),
            "mean_skip_fraction":mean(cell_means[tier,mode]["skipped"] for mode in MODES),
            "correct_choice_fraction":mean(cell_means[tier,mode]["correct"] for mode in MODES)}
            for tier in COSTS}
        per_colony[col].append({"bee":bee,"K":K,"D":D,"diagnostics":by_cost})
    source_colonies=[]
    for col,records in sorted(per_colony.items()):
        source_colonies.append({
            "colony_id":col,"n_fake_bees":len(records),
            "K":mean(z["K"] for z in records),
            "D":{cost:mean(z["D"][cost] for z in records) for cost in COSTS},
            "diagnostics":{cost:{feature:mean(z["diagnostics"][cost][feature] for z in records)
                       for feature in ("mean_leaf_requests","mean_skip_fraction","correct_choice_fraction")}
                for cost in COSTS}})
    C=len(source_colonies)
    value=mean(c["K"] for c in source_colonies)
    out={
        "status":"SYNTHETIC_PILOT_LT_12_COLONIES" if C<12 else "SYNTHETIC_ONLY_COLONY_ESTIMATOR_QA",
        "n_independent_mock_colonies":C,
        "n_mock_bees":len(by_bee),"n_mock_trials":len(assignments),
        "middle_vs_extremes_curvature_mg":value,
        "mode_effects_by_cost_mg":{
             tier:mean(c["D"][tier] for c in source_colonies) for tier in COSTS},
        "mean_leaf_requests_by_tier":{
             tier:mean(c["diagnostics"][tier]["mean_leaf_requests"] for c in source_colonies)
             for tier in COSTS},
        "mean_skip_fraction_by_tier":{
             tier:mean(c["diagnostics"][tier]["mean_skip_fraction"] for c in source_colonies)
             for tier in COSTS},
        "source_unit":"colony-equal after bee-equal",
        "actual_recruitment":0,"NO_REAL_BEES":True,
        "not_a_physiological_cost_curvature":True,
        "synthetic_injected_reward_not_observed_fitness":True,
        "all_source_assigned_trials_including_skip_used":True}
    if C>=12:
        vals=[x["K"] for x in source_colonies]
        sd=stdev(vals)
        if sd<=1e-12:
            out["status"]="NO_GO_MOCK_COLONY_CONTRAST_ZERO_VARIANCE"
        else:
            se=sd/sqrt(C);tstat=value/se
            crit=float(student_t.ppf(.975,C-1))
            out.update({
                "synthetic_colony_df":C-1,
                "synthetic_two_sided_p_NOT_EMPIRICAL":float(2*student_t.sf(abs(tstat),C-1)),
                "synthetic_CI95_NOT_EMPIRICAL":[value-crit*se,value+crit*se]})
    return out
