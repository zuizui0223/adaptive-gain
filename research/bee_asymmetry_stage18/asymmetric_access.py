"""Exact Bayesian value of root-dependent optional information acquisition.

NO bees or colonies were measured. The state variables are IID across trials,
but asymmetric within a trial: R~Bern(.5), U~Bern(q), V~Bern(.5), q∈[0,.5].
If R=0 the target bit is U; if R=1 it is V. The root signal is perfectly
perceived for THIS restricted proposition. Leaves reveal their bit exactly.

A correct guess pays 1, incorrect pays 0; each requested leaf costs c.
Contingent arm may SKIP or select U/V after R. Precommit arm must commit
SKIP/U/V before R but may buy the second leaf after learning R and its first.
Original leaf-source and root-visible experimental claims NOT established.
"""
from __future__ import annotations
import argparse
import json
import math
import random
from pathlib import Path


def _check(q,c):
    if type(q) not in (float,int) or not math.isfinite(q) or not 0<=q<=.5:
        raise ValueError("NO_GO_INVALID_OR_NONMINORITY_BRANCH_TARGET_PREVALENCE")
    if type(c) not in (float,int) or not math.isfinite(c) or c<0:
        raise ValueError("NO_GO_INVALID_LEAF_QUERY_COST")


def values(q,c):
    """Exact full-choice-state root-specific contingent vs precommit value."""
    _check(q,c)
    q=float(q);c=float(c)
    root0={"SKIP":1-q,"U":1-c}
    root1={"SKIP":.5,"V":1-c}
    # Strict positive improvement is necessary for paying for a leaf; in
    # ties the animal is assumed to choose the cost-free SKIP action.
    best0=max(root0,key=lambda k:root0[k])
    best1=max(root1,key=lambda k:root1[k])
    contingent=.5*(root0[best0]+root1[best1])
    precommit={
      "SKIP":.75-.5*q,
      "U":.5*(1+max(.5,1-c))-c,
      "V":.5*(1+max(1-q,1-c))-c,
    }
    first=max(precommit,key=lambda k:precommit[k])
    pre_value=precommit[first]
    gain=contingent-pre_value
    if gain<-1e-11:
        raise ValueError("NO_GO_ADAPTIVE_VALUE_ORDERING")
    return {
      "rare_branch_one_prior":q,"leaf_cost_correctness_reward_units":c,
      "source_R_is_perfectly_observed":True,
      "source_U_one_probability":q,"source_V_one_probability":.5,
      "root0_best":best0,"root1_best":best1,
      "root_state_changes_whether_to_query":
          (best0=="SKIP")!=(best1=="SKIP"),
      "contingent_value":contingent,
      "precommit_value":pre_value,
      "precommit_best_initial_action":first,
      "precommit_all_initial_actions":precommit,
      "root0_candidate_values":root0,
      "root1_candidate_values":root1,
      "access_value_gain":max(0.,gain),
      "precommit_can_request_second_leaf":True,
      "first_leaf_can_be_declined_in_both_arms":True,
      "no_biological_cost_calibration":True,
      "empirical":False,
    }


def maximum_value(q):
    """Exact sharp upper envelope for 0≤q≤.5 over c≥0.

    When q≤1/4, first precommit optimum changes to SKIP at c=1/4;
    the access advantage reaches 1/8. For q≥1/4, the switch from
    buying two possible leaves to SKIP occurs at c=(q+1/2)/3;
    the optimum advantage is (q+1/2)/6.
    """
    _check(q,0.)
    q=float(q)
    if q<=.25:
        cost=.25
        maximum=.125
    else:
        cost=(q+.5)/3
        maximum=(q+.5)/6
    z=values(q,cost)
    if abs(z["access_value_gain"]-maximum)>1e-12:
        raise ValueError("NO_GO_SHARP_ASYMMETRIC_CEILING_NOT_ATTAINED")
    return {
      "q":q,
      "max_access_value":maximum,
      "attaining_cost":cost,
      "max_is_for_normalized_correctness_reward_not_sucrose":True,
    }


def sample_hidden_worlds(n,q=.2,seed=20261111):
    """Source-free IID-with-replacement nonuniform binary experimental worlds."""
    _check(q,0.)
    if type(n) is not int or not 1<=n<=1_000_000 or type(seed) is not int:
        raise ValueError("NO_GO_INVALID_MOCK_WORLD_COUNT_OR_SEED")
    rng=random.Random(seed)
    return [(rng.randrange(2),int(rng.random()<q),rng.randrange(2))
            for _ in range(n)]


def condition_grid():
    q_values=(0.,.05,.10,.20,.25,.30,.40,.50)
    costs=(0.,.01,.05,.1,.15,.2,.25,.275,.3,1/3,.35,.4,.5,.8)
    return {
        "status":"EXACT_STATE_DEPENDENT_STOP_DECISION_TOPOLOGY",
        "q_values":q_values,"cost_values":costs,
        "cases":[values(q,c) for q in q_values for c in costs],
        "sharp_max_by_q":[maximum_value(q) for q in q_values],
        "main_falsifiable_example":values(.2,.25),
        "trial_state_priors":"R~Bern(.5), U~Bern(q), V~Bern(.5), independent and re-drawn each trial",
        "root_reliability_assumed":1.,
        "zero_original_bee_measurements":True,
        "no_behavioral_effect_estimated":True,
        "no_real_query_delay_calibration":True,
        "no_empirical_colony_variance":True,
    }


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--out",default="stage18_exact_outputs")
    root=Path(p.parse_args().out)
    root.mkdir(parents=True,exist_ok=True)
    result=condition_grid()
    (root/"stage18_asymmetry_decision_surface.json").write_text(
        json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False))
    outcome={"math":"EXACT_EIGHT_WORLD_NONUNIFORM_PRIORS",
             "n_cases":len(result["cases"]),
             "test_case_root0_skip_root1_v":result["main_falsifiable_example"],
             "asymmetry_q20_ceiling":maximum_value(.2),
             "symmetric_q50_ceiling":maximum_value(.5),
             "real_animals":0}
    print("STAGE18_ROOT_CONDITIONAL_STOP_MATH "+
          json.dumps(outcome,ensure_ascii=False,allow_nan=False),flush=True)
