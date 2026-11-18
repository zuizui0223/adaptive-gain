"""Stage80 finite Bayesian cue-routing example, NOT a fitted ecological model.

The only real-data use is to define preregisterable stage-by-context hypotheses.
No literature effect size is used as a prior, accuracy or cost parameter.

Phases: FAR (choose scent/large-scale visual cue/approach/abandon),
NEAR (optionally observe guide, land or abandon), CONTACT (land payoff).
The hidden target is whether one candidate flower is rewarding now.
All three binary observations are conditionally independent given that state,
which is an illustrative assumption, NOT a property inferred from field data.
Wind may alter odor and visual observation accuracy, approach cost and
landing success, separately. Learning is represented only by prior_reward;
no observed bee learning rate is reconstructed.
"""
from __future__ import annotations
from dataclasses import dataclass,asdict
from functools import lru_cache
from typing import Tuple
import json

@dataclass(frozen=True)
class Context:
    prior_reward: float
    accuracy_scent: float
    accuracy_visual: float
    accuracy_guide: float
    cost_scent: float
    cost_visual: float
    cost_guide: float
    cost_approach: float
    landing_success: float
    value_reward: float = 1.0
    cost_empty: float = 2.0
    cost_failed_landing: float = 0.3

    def __post_init__(self):
        for name in ('prior_reward','landing_success'):
            v=getattr(self,name)
            if not 0<=v<=1:raise ValueError(f'{name} out of [0,1]')
        for name in ('accuracy_scent','accuracy_visual','accuracy_guide'):
            v=getattr(self,name)
            if not .5<=v<=1:raise ValueError(f'{name} out of [.5,1]')
        for name in ('cost_scent','cost_visual','cost_guide','cost_approach',
                     'value_reward','cost_empty','cost_failed_landing'):
            if getattr(self,name)<0:raise ValueError(f'{name} must be nonnegative')


def binary_observation(p:float, accuracy:float)->Tuple[Tuple[float,float],...]:
    """Return Pr(signal), Pr(rewarding | signal), including zero-probability guard."""
    prob_true = p*accuracy + (1-p)*(1-accuracy)
    prob_false=1-prob_true
    post_true=p*accuracy/prob_true if prob_true else p
    post_false=p*(1-accuracy)/prob_false if prob_false else p
    return ((prob_true,post_true),(prob_false,post_false))


def solve(ctx:Context)->dict:
    """Exact finite dynamic program; returns actions and signed expected net value."""
    acc={'scent':ctx.accuracy_scent,'visual':ctx.accuracy_visual}
    costs={'scent':ctx.cost_scent,'visual':ctx.cost_visual}

    def land(p):
        return (ctx.landing_success*(p*ctx.value_reward - (1-p)*ctx.cost_empty)
                -(1-ctx.landing_success)*ctx.cost_failed_landing)

    @lru_cache(None)
    def near(p:float,guide_used:bool):
        candidates={'abandon':0., 'land_without_more_information':land(p)}
        if not guide_used:
            candidates['inspect_near_guide']=(
                -ctx.cost_guide + sum(pr*near(post,True)[0] for pr,post in
                                      binary_observation(p,ctx.accuracy_guide)))
        action=max(sorted(candidates),key=lambda k:candidates[k])
        return (candidates[action],action)

    @lru_cache(None)
    def far(p:float,remaining:Tuple[str,...]):
        near_value=near(p,False)[0]
        candidates={'abandon':0.,'approach_and_then_decide':-ctx.cost_approach+near_value}
        for cue in remaining:
            remainder=tuple(k for k in remaining if k!=cue)
            candidates['inspect_far_'+cue]=(-costs[cue]+sum(
                pr*far(post,remainder)[0] for pr,post in binary_observation(p,acc[cue])))
        best=max(sorted(candidates),key=lambda k:candidates[k])
        return (candidates[best],best)

    all_cues=('scent','visual')
    opt,first=far(ctx.prior_reward,all_cues)
    forced_first={cue:-costs[cue]+sum(
            pr*far(post,tuple(k for k in all_cues if k!=cue))[0]
            for pr,post in binary_observation(ctx.prior_reward,acc[cue])) for cue in all_cues}
    bypass=max(0.,-ctx.cost_approach+near(ctx.prior_reward,False)[0])
    return {'status':'SYNTHETIC_DECISION_THEORY_ONLY_NOT_MACRO_EFFECT',
            'optimal_expected_payoff':opt,'optimal_first_action':first,
            'forced_first_expected_payoff':forced_first,
            'bypass_far_cues_value':bypass,
            'conditional_far_cue_advantage_over_bypass':opt-bypass,
            'context':asdict(ctx),
            'note':'No natural accuracy, cognition, wind plume, flower trait or fitness coefficient identified.'}

if __name__=='__main__':
    scenarios={
      'calm':Context(.45,.90,.68,.85,.025,.035,.07,.08,.96),
      'gusty':Context(.45,.57,.78,.85,.025,.035,.07,.10,.89),
      'hazardous':Context(.45,.52,.80,.85,.025,.035,.07,.55,.30),
    }
    print(json.dumps({k:solve(v) for k,v in scenarios.items()},indent=2,sort_keys=True))
