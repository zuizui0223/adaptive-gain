"""Stage63: stochastic Bayes decision counterpart to inherited exact routeability.

Four *constructed* equally weighted worlds (branch b=0/1, reward
target t=0/1). Coarse cue R reports branch b with symmetric error e_R
but zero direct information about t. Terminal visible signal V diagnoses
t with error e_V only for branch=0; terminal odour O diagnoses t with
error e_O only for branch=1. Off-branch terminals are independent fair
coin observations. Independent cues conditional on world. No empirical
bee/flower sensory observations are asserted from these assumptions.

Fixed policy selects a noncontingent subset of cues (0..3), pays every
chosen cue, then makes Bayes optimal 0/1 target classification.
Adaptive policy sequentially chooses to stop or pay for the next cue
based on previous observations. Exact rational posterior + dynamic
programming computes Bayes risk, which includes 0/1 wrong-target loss
plus abstract acquisition costs. The static comparator is stronger than
an 'odour-only' strawman: any subset with optimal joint Bayes decoding.

This standard finite Bayesian design is NOT a new mathematical theorem.
It is a more realistic, falsifiable translation of existing deterministic
adaptive-gain theory; actual wind-speed dependence of cue error/cost,
receptor guild differences, first-cue policies and plant pollen fitness
remain unmeasured. Crall 2020, Chang 2016, Lawson 2017 are different
experiments and DO NOT calibrate the hypothetical errors.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations,product
import json
from pathlib import Path

CUES=("R_coarse_branch_state","V_visible_spatial_cue","O_floral_odor_cue")
WORLDS=((0,0),(0,1),(1,0),(1,1)) # branch, target
PRIOR=(F(1,4),)*4

def _f(x,key,lo=F(0),hi=F(1)):
    if type(x) not in (int,F):
        raise ValueError("NO_GO_FLOAT_OR_UNVERIFIED_SOURCE_VALUE_"+key)
    q=F(x)
    if not lo<=q<=hi:
        raise ValueError("NO_GO_OUT_OF_RANGE_"+key)
    return q

@dataclass(frozen=True)
class CueContext:
    # Bayesian 0/1 classification loss 1 for incorrect target.
    router_error:F
    visual_error:F
    odor_error:F
    router_cost:F
    visual_cost:F
    odor_cost:F

    def validated(self):
        for k in ("router_error","visual_error","odor_error"):
            _f(getattr(self,k),k,F(0),F(1,2))
        for k in ("router_cost","visual_cost","odor_cost"):
            _f(getattr(self,k),k,F(0),F(1,2))
        return self

    @property
    def costs(self):
        return (self.router_cost,self.visual_cost,self.odor_cost)

def prob_one(world,cue:int,context:CueContext)->F:
    b,t=world
    if cue==0:
        return 1-context.router_error if b==1 else context.router_error
    if cue==1:
        return ((1-context.visual_error) if t==1 else context.visual_error
                ) if b==0 else F(1,2)
    if cue==2:
        return ((1-context.odor_error) if t==1 else context.odor_error
                ) if b==1 else F(1,2)
    raise ValueError("NO_GO_UNKNOWN_CONSTRUCTED_SENSORY_CUE")

def posterior(looks:tuple[tuple[int,int],...],context:CueContext):
    context.validated()
    if len(set(q for q,_ in looks))!=len(looks):
        raise ValueError("NO_GO_SENSORY_CUE_ACQUIRED_TWICE")
    if any(q not in (0,1,2) or y not in (0,1) for q,y in looks):
        raise ValueError("NO_GO_CUE_OUTCOME_NOT_BINARY")
    masses=[]
    for world,pr in zip(WORLDS,PRIOR):
        p=pr
        for q,y in looks:
            o=prob_one(world,q,context)
            p*=o if y else (1-o)
        masses.append(p)
    z=sum(masses)
    if z==0:
        return None,F(0)
    return tuple(p/z for p in masses),z

def bayes_wrong_loss(weights):
    if weights is None: return F(0)
    p0=weights[0]+weights[2]
    p1=weights[1]+weights[3]
    return min(p0,p1)

def next_outcome_prob(weights,q,ctx):
    return sum(weights[i]*prob_one(world,q,ctx) for i,world in enumerate(WORLDS))

def exact_adaptive(ctx:CueContext):
    ctx.validated()
    @lru_cache(None)
    def value(looks):
        weights,prob=posterior(looks,ctx)
        if weights is None:
            return F(0),("IMPOSSIBLE_HISTORY",)
        best=bayes_wrong_loss(weights)
        actions=["STOP_AND_CLASSIFY"]
        seen={q for q,y in looks}
        for q in range(3):
            if q in seen:continue
            p1=next_outcome_prob(weights,q,ctx)
            p0=1-p1
            left=value(looks+((q,0),))[0] if p0 else F(0)
            right=value(looks+((q,1),))[0] if p1 else F(0)
            candidate=ctx.costs[q]+p0*left+p1*right
            if candidate<best:
                best=candidate;actions=[CUES[q]]
            elif candidate==best:
                actions.append(CUES[q])
        return best,tuple(actions)
    initial_loss,initial_actions=value(())
    after_router={}
    for outcome in (0,1):
        v,a=value(((0,outcome),))
        after_router[str(outcome)]={
          "optimal_remaining_loss_after_router_sunk_cost_exact":str(v),
          "optimal_next_actions":list(a)}
    return {
      "minimal_expected_loss_exact":initial_loss,
      "initial_optimal_actions":initial_actions,
      "optimal_continuation_after_router":after_router,
      "source_free_rational_dynamic_programming":True,
      "finite_world_target_zero_one_loss":True
    }

def exact_fixed(ctx:CueContext):
    ctx.validated()
    options=[]
    for k in range(4):
        for subset in combinations(range(3),k):
            expected_misclassification=F(0)
            for ys in product((0,1),repeat=k):
                look=tuple(zip(subset,ys))
                weights,p=posterior(look,ctx)
                if p==0:continue
                expected_misclassification+=p*bayes_wrong_loss(weights)
            loss=sum((ctx.costs[i] for i in subset),F(0))+expected_misclassification
            options.append((loss,subset,expected_misclassification))
    best=min(x[0] for x in options)
    optimal=[x for x in options if x[0]==best]
    return {
      "minimal_expected_loss_exact":best,
      "optimal_fixed_cue_subsets":[tuple(CUES[i] for i in x[1]) for x in optimal],
      "all_fixed_subsets":tuple({
         "subset":tuple(CUES[i] for i in x[1]),
         "acquisition_plus_target_error_loss_exact":str(x[0]),
         "target_error_only_exact":str(x[2])
      } for x in options),
      "strongest_noncontingent_Bayesian_decoding_baseline":True
    }

def router_direct_target_information_zero(ctx:CueContext):
    for y in (0,1):
        weights,prob=posterior(((0,y),),ctx)
        if prob<=0 or (weights[0]+weights[2])!=F(1,2):
            raise AssertionError("NO_GO_ROUTER_CARRIES_DIRECT_TARGET_INFORMATION")
    return True

def context_run(name,ctx):
    a=exact_adaptive(ctx)
    f=exact_fixed(ctx)
    if a["minimal_expected_loss_exact"]>f["minimal_expected_loss_exact"]:
        raise AssertionError("NO_GO_ADAPTIVE_CANNOT_BE_WORSE_THAN_FIXED_BUNDLE")
    r=f["minimal_expected_loss_exact"]-a["minimal_expected_loss_exact"]
    if not router_direct_target_information_zero(ctx):
        raise AssertionError("NO_GO_ROUTER_DIRECT_TARGET_UNINFORMATIVE")
    return {
      "scenario_assumed_not_measured":name,
      "symmetric_cue_bit_error_assumptions_exact":{
         "R":str(ctx.router_error),"V":str(ctx.visual_error),"O":str(ctx.odor_error)},
      "receiver_abstract_acquisition_costs_exact":{
         "R":str(ctx.router_cost),"V":str(ctx.visual_cost),"O":str(ctx.odor_cost)},
      "optimal_adaptive_expected_loss_exact":str(a["minimal_expected_loss_exact"]),
      "optimal_fixed_expected_loss_exact":str(f["minimal_expected_loss_exact"]),
      "optimal_adaptive_expected_loss":float(a["minimal_expected_loss_exact"]),
      "optimal_fixed_expected_loss":float(f["minimal_expected_loss_exact"]),
      "adaptive_loss_advantage_exact":str(r),
      "adaptive_loss_advantage":float(r),
      "adaptive_initial_action_candidates":list(a["initial_optimal_actions"]),
      "fixed_optimal_cue_subset_candidates":[list(s) for s in f["optimal_fixed_cue_subsets"]],
      "adaptive_next_cue_if_router_y0_y1":a["optimal_continuation_after_router"],
      "router_direct_target_mutual_information_zero":True,
      "fixed_policy_uses_best_joint_Bayes_decoder_not_a_strawman":True,
      "stochastic_context_not_actual_wind_or_Bombus_parameters":True,
    }

# Explicitly constructed scenarios, not calibration to the 2017 source bees.
SCENARIOS={
 "high_reliability_both_terminals_ideal_router":
     CueContext(F(0),F(1,20),F(1,20),F(1,20),F(1,10),F(1,10)),
 "moderate_noisy_router":
     CueContext(F(3,20),F(1,20),F(1,20),F(1,20),F(1,10),F(1,10)),
 "uninformative_router":
     CueContext(F(1,2),F(1,20),F(1,20),F(1,20),F(1,10),F(1,10)),
 "olfactory_terminal_noisy_not_wind_calibrated":
     CueContext(F(1,20),F(1,20),F(2,5),F(1,20),F(1,10),F(1,10)),
 "visual_terminal_noisy_not_wind_calibrated":
     CueContext(F(1,20),F(7,20),F(1,20),F(1,20),F(1,10),F(1,10)),
 "both_terminals_noisy_not_wind_calibrated":
     CueContext(F(1,20),F(3,10),F(2,5),F(1,20),F(1,10),F(1,10)),
}

def run_all():
    rows=[context_run(k,ctx) for k,ctx in SCENARIOS.items()]
    keys=[r["adaptive_loss_advantage_exact"] for r in rows]
    if keys!=["1/10","1/10","0","0","1/100","0"]:
        raise AssertionError("NO_GO_CONSTRUCTED_BAYES_ROUTEABILITY_PHASES_MISMATCH")
    return {
      "status":"STAGE63_FINITE_NOISY_BAYES_CONDITIONAL_FLORAL_ROUTEABILITY_CONSTRUCTED_PREDICTIONS",
      "counterexample_scenarios":rows,
      "source_crall_wind_bait_and_2017_Lawson_not_used_to_fit_error_rates":True,
      "source_2017_bee_four_groups_do_not_measure_first_to_second_cue_queries":True,
      "source_2016_Bombus_SDM_and_2025_UV_VOC_are_not_concurrent_populations":True,
      "not_a_novel_Bayesian_decision_theorem":True,
      "existing_deterministic_routeability_theorem_not_empirical_validation":True,
      "requires_randomized_first_cue_and_receiver_observed_next_query":True,
      "no_causal_wind_odor_vision_or_pollen_effect_estimated":True,
      "phenotyped_native_plant_and_local_pollinator_cooccurrence_missing":True,
    }

def main():
    output=run_all()
    dest=Path("stage63_noisy_Bayes_sensory_routing")
    dest.mkdir(exist_ok=True)
    (dest/"exact_noisy_cue_contingent_vs_fixed_Bayes_risk_source_free.json").write_text(
       json.dumps(output,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
    print("STAGE63_EXACT_NOISY_BAYES_ADAPTIVE_VS_BEST_FIXED_SENSORY_LOSS",
          json.dumps(output,sort_keys=True,ensure_ascii=False))
    print("NO_SOURCE_EMISSION_WIND_SPEED_BEE_BRAIN_CUE_QUERY_OR_POLLEN_FIT")
if __name__=="__main__":
    main()
