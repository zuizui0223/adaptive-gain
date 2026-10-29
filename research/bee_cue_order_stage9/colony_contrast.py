"""Stage 9 predeclared colony-equal 2x2 order×wind sucrose ITT contrast.

Produces a strict analysis for FUTURE *real* randomized trials, plus
synthetic design QA. No real bees have been randomized/tested by this code.
Do not replace measured zero intake with unknown sensor data or filter
unsuccessful choice/landing trials.
"""
from __future__ import annotations
from collections import Counter,defaultdict
import argparse
import json
import math
import random
from pathlib import Path
from statistics import mean,stdev
from scipy.stats import t as student_t

from randomization import (
    ORDERS,WINDS,QA_SEED,BLOCK_TRIALS,BEES_PER_COLONY,
    generate_allocation,audit_allocation
)

MIN_CONFIRMATORY_COLONIES=12
OBSERVATION_SECONDS=30
STATUS_VALID={"measured","verified_no_intake"}

def estimate_colony_order_wind_interaction(assignments,outcomes):
    """Fail closed unless every assigned trial has an actual valid outcome."""
    source=audit_allocation(assignments)
    ids={r["trial_id"]:r for r in assignments}
    if not isinstance(outcomes,list) or len(outcomes)!=len(assignments):
        raise ValueError("NO_GO_MISSING_OR_EXTRA_RANDOMIZED_OUTCOME")
    observed={}
    for r in outcomes:
        tid=r.get("trial_id")
        if tid in observed or tid not in ids:
            raise ValueError("NO_GO_DUPLICATE_OR_UNKNOWN_RANDOMIZATION_ID")
        if r.get("sensor_status") not in STATUS_VALID:
            raise ValueError("NO_GO_SENSOR_FAILURE_IS_NOT_NO_INTAKE")
        if r.get("analysis_window_seconds")!=OBSERVATION_SECONDS:
            raise ValueError("NO_GO_NONSTANDARD_OUTCOME_WINDOW")
        mass=r.get("verified_consumed_sucrose_mg")
        if not isinstance(mass,(int,float)) or not math.isfinite(mass) or mass<0:
            raise ValueError("NO_GO_NONNUMERIC_OR_NEGATIVE_REAL_SUCROSE_INTAKE")
        if r["sensor_status"]=="verified_no_intake" and mass!=0:
            raise ValueError("NO_GO_NO_INTAKE_CANNOT_HAVE_POSITIVE_CONSUMPTION")
        observed[tid]=mass/OBSERVATION_SECONDS
    if set(observed)!=set(ids):
        raise ValueError("NO_GO_INCOMPLETE_INTENTION_TO_TREAT_POPULATION")
    by_bee=defaultdict(lambda:defaultdict(list))
    for item in assignments:
        key=(item["colony_id"],item["bee_id"])
        arm=(item["assigned_wind"],item["assigned_cue_order"])
        by_bee[key][arm].append(observed[item["trial_id"]])
    by_colony=defaultdict(list)
    by_bee_report=[]
    for (colony,bee),cells in sorted(by_bee.items()):
        if set(cells)!={(w,o) for w in WINDS for o in ORDERS}:
            raise ValueError("NO_GO_FACTORIAL_OUTCOME_CELLS_ABSENT")
        if any(len(r)!=16 for r in cells.values()):
            raise ValueError("NO_GO_PER_BEE_CELL_NOT_EXACTLY_16_ASSIGNED_TRIALS")
        summary={f"{w}__{o}":mean(cells[w,o]) for w in WINDS for o in ORDERS}
        wind_order=summary["crosswind__reward_first"]-summary["crosswind__handling_first"]
        calm_order=summary["calm__reward_first"]-summary["calm__handling_first"]
        delta=wind_order-calm_order
        by_colony[colony].append((bee,delta,wind_order,calm_order))
        by_bee_report.append({"colony_id":colony,"bee_id":bee,
                              "order_x_wind_delta_mg_s":delta,
                              "order_effect_crosswind_mg_s":wind_order,
                              "order_effect_calm_mg_s":calm_order})
    colonies=[]
    for colony,rows in sorted(by_colony.items()):
        bees={x[0] for x in rows}
        if len(rows)!=len(bees):
            raise ValueError("NO_GO_DUPLICATE_BEE_COLONY_ANALYSIS_KEY")
        colonies.append({
            "colony_id":colony,"n_bees":len(rows),
            "order_x_wind_delta_mg_s":mean(x[1] for x in rows),
            "order_effect_crosswind_mg_s":mean(x[2] for x in rows),
            "order_effect_calm_mg_s":mean(x[3] for x in rows)})
    c=len(colonies)
    if c<MIN_CONFIRMATORY_COLONIES:
        return {"status":"NO_GO_TOO_FEW_INDEPENDENT_COLONIES",
                "independent_colony_count":c,
                "observed_rand_trials":len(outcomes),
                "required_min_confirmatory_colonies":MIN_CONFIRMATORY_COLONIES,
                "colonies":colonies,
                "no_general_p_value":True}
    values=[r["order_x_wind_delta_mg_s"] for r in colonies]
    if stdev(values)<1e-10:
        return {"status":"NO_GO_NO_BETWEEN_COLONY_CONTRAST_VARIANCE",
                "independent_colony_count":c,
                "colonies":colonies,
                "no_general_p_value":True}
    estimated=mean(values)
    sample_sd=stdev(values)
    se=sample_sd/math.sqrt(c)
    crit=float(student_t.ppf(.975,c-1))
    tvalue=estimated/se
    p=float(2*student_t.sf(abs(tvalue),c-1))
    return {
        "status":"FITTED_COLONY_INDEPENDENT_ITTs",
        "design_evidence":source,
        "outcome_unit":"verified consumed sucrose mg / fixed 30sec window = mg/s",
        "independent_randomization_cluster":"source colony (bee repeated within colony)",
        "source_colonies":c,"bees":len(by_bee),
        "randomized_trials_including_zero_drink":len(outcomes),
        "colony_equal_primary_interaction_delta_mg_s":estimated,
        "colony_between_contrast_sample_sd_mg_s":sample_sd,
        "colony_level_standard_error_mg_s":se,
        "two_sided_alpha":.05,
        "primary_t_statistic":tvalue,
        "primary_t_df":c-1,
        "primary_two_sided_t_p":p,
        "primary_student_t_95pct_CI_mg_s":[estimated-crit*se,
                                           estimated+crit*se],
        "independent_colony_order_effect_under_wind_mg_s":mean(
            c["order_effect_crosswind_mg_s"] for c in colonies),
        "independent_colony_order_effect_under_calm_mg_s":mean(
            c["order_effect_calm_mg_s"] for c in colonies),
        "colony_level_effects":colonies,
        "repeat_bee_level_effects":by_bee_report,
        "trial_level_pseudoreplication_avoided":True,
        "causally_identifies_only_randomized_presentation_order_effect_if_trial_assignment_and_measured_outcomes_are_real":True
    }

def generate_synthetic_QA_outcomes(assignments,delta=.02,
                                   seed=QA_SEED+1,
                                   sigma_colony_delta=.025,
                                   sigma_bee_delta=.030,
                                   sigma_trial=.080):
    """GAUSSIAN SYNTHETIC QA ONLY; no real-animal predicted effect."""
    if not 0<=delta<1:
        raise ValueError("NO_GO_SYNTHETIC_EFFECT_RANGE")
    rng=random.Random(seed)
    c_intercept={}
    c_delta={}
    b_intercept={}
    b_delta={}
    observed=[]
    for r in assignments:
        col=r["colony_id"];bee=(col,r["bee_id"])
        if col not in c_intercept:
            c_intercept[col]=rng.gauss(0,.012)
            c_delta[col]=rng.gauss(0,sigma_colony_delta)
        if bee not in b_intercept:
            b_intercept[bee]=rng.gauss(0,.025)
            b_delta[bee]=rng.gauss(0,sigma_bee_delta)
        wind=int(r["assigned_wind"]=="crosswind")
        order=int(r["assigned_cue_order"]=="reward_first")
        # Example outcome is nonnegative by construction; any clipping is
        # part of a QA mock and invalid for direct power calibration.
        pseudo=(
            .30+c_intercept[col]+b_intercept[bee]+
            .005*order-.030*wind+
            (delta+c_delta[col]+b_delta[bee])*order*wind+
            rng.gauss(0,sigma_trial))
        value=max(0.,pseudo)
        observed.append({
            "trial_id":r["trial_id"],
            "analysis_window_seconds":OBSERVATION_SECONDS,
            "sensor_status":"measured",
            "verified_consumed_sucrose_mg":value*OBSERVATION_SECONDS})
    return observed

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--out",default="bee_stage9_design_output")
    args=p.parse_args(argv)
    allocation=generate_allocation(n_colonies=24,bees_per_colony=12)
    fake=generate_synthetic_QA_outcomes(allocation)
    report=estimate_colony_order_wind_interaction(allocation,fake)
    if report["status"]!="FITTED_COLONY_INDEPENDENT_ITTs":
        raise ValueError("NO_GO_STAGE9_SYNTHETIC_ANALYSIS_VALIDATION")
    # Do not publish actual individual allocations or synthetic per-bee data:
    # summarize only the testable estimator and its two-level clustered
    # sample size. No empirical result exists in this branch.
    receipt={
        "status":"SYNTHETIC_DESIGN_AND_ESTIMATOR_QA_ONLY",
        "synthetic_replicates_are_NOT_REAL_BEES":True,
        "independent_original_colonies_assumed":24,
        "synthetic_original_factorial_trials":len(allocation),
        "synthetic_effect_parameter_injected_mg_s":.02,
        "synthetic_recovered_colony_equal_delta_mg_s":report[
            "colony_equal_primary_interaction_delta_mg_s"],
        "synthetic_colony_student_t_p_not_empirical":report[
            "primary_two_sided_t_p"],
        "synthetic_colony_contrast_ci_not_empirical":report[
            "primary_student_t_95pct_CI_mg_s"],
        "actual_source_animal_outcomes_analyzed":0,
        "real_data_only_after_ethical_approval_secure_allocation_and_new_collection":True
    }
    out=Path(args.out)
    out.mkdir(parents=True,exist_ok=True)
    (out/"bee_stage9_synthetic_colony_estimator_QA.json").write_text(
        json.dumps(receipt,indent=2,ensure_ascii=False))
    print("STAGE9_SYNTHETIC_COLONY_ESTIMATOR_QA "+
          json.dumps(receipt,ensure_ascii=False),flush=True)
    print("STAGE9_PROSPECTIVE_CAUSAL_ESTIMATOR_VALIDATED_NO_REAL_ANIMALS",flush=True)

if __name__=="__main__":main()
