"""Stage58 | ecology-facing specialization of *existing* finite routeability theory.

Reuse adaptive_gain.core's exact solver and the published project's k=2
four-world canonical routing task. Here the *hypothetical* environmental
router is an early coarse perception (e.g., which sensor track is reliable);
terminal_0 is local visible/UV discrimination, terminal_1 is close-range
olfactory/chemical discrimination. World/target outcomes do NOT come from
real flowers or bees. The assumed positive integer costs are receiver
attention/flight/handling currencies, NOT emission costs or measured ms.

Crall 2020 orchid-bee bait sessions, Chang 2016 Bombus successful landings,
Baird 2021 honeybee optic-flow flights and Stage57 source UV trait/SDM
are INDEPENDENT systems with incompatible denominators and wind regimes.
Never use any measured coefficient to set a hypothetical sensory cost.
No source study identifies odor ON/OFF x floral visual guide x wind and
complete opportunity→contact→pollen probabilities within one cohort.

The advance over a simple additive E+wind+scent regression is an *explicit
falsifiable route/topology* hypothesis. The mathematical exact cost
bound is an existing adaptive-gain theorem, not a new floral theorem.
"""
from __future__ import annotations

from dataclasses import asdict
from fractions import Fraction
import json
from pathlib import Path
from typing import Any

from adaptive_gain.core import (
    FiniteTask, Query, adaptive_minimum_resolution,
    fixed_minimum_resolution, adaptive_only_at_budget, bundle_resolves
)
from adaptive_gain.extremal_routing_family import extremal_routing_task

ROUTER="coarse_environment_or_encounter_state"
VISUAL="local_visible_or_UV_discrimination"
SCENT="local_scent_or_chemical_discrimination"
SOURCE_SYSTEMS={
    "Crall2020": {
        "doi":"10.1098/rsbl.2020.0103",
        "source_branch":"analysis/floral-crall-date-multicluster-stage37-20261115",
        "source_experiment":"70 source scented-bait 20min sessions, 9 sites and 29 dates",
        "original_estimate":"within-site association IRR=1.39852 per doubling observed 0.0206-0.73 m/s wind",
        "positive_end_point":"male orchid-bee arrivals to all-scented bait stations",
        "missing":["odor-off wind factorial","wild flower visual contrast","landings","pollen","fitness"],
    },
    "Chang2016":{
        "doi":"10.1242/jeb.137976",
        "source_branch":"analysis/floral-within-bee-trial-selection-stage44-20261116",
        "source_experiment":"archived 157 successful landing tracks/28 B labels; 23 matched B labels",
        "original_estimate":"W1-W0 near-flower speed +0.121429 m/s; six-method original-source robustness",
        "positive_end_point":"ground-speed change of successful landing tracks in headwind",
        "missing":["failed approach denominator","visual-guide manipulation","odor ON/OFF","pollen","fitness"],
    },
    "Baird2021":{
        "doi":"10.1098/rspb.2020.3051",
        "source_branch":"literature_independent",
        "source_experiment":"honeybee experimental optic-flow texture x head/tail wind",
        "original_estimate":"visual optic-flow components govern flight speed and height control",
        "positive_end_point":"flight ground speed/height response",
        "missing":["floral UV-guide phenotype","odor","pollen","fitness"],
    },
    "Stage57_2016UV_BeeGuild":{
        "doi":"10.1111/nph.13921",
        "source_branch":"analysis/floral-environment-path-literature-stage57-20261117",
        "source_experiment":"159 originally UV-phenotyped species; 106 have source bee-HEX coverage",
        "original_estimate":"source E-to-modelled Bombus-fraction R2 0.18288; genus adjusted quasi-separation",
        "positive_end_point":"source-correlated plant UV pattern and current predicted bee species names",
        "missing":["original phenotyped locality linked to bees","VOC","contact","pollen","fitness"],
    }
}


def routing_task(*,coarse_cost:int,visible_cost:int,chemical_cost:int,
                 removed: str|None=None)->FiniteTask:
    """Original exact k=2 task, only costs and an explicit cue collapse altered.

    The original task has targets (0,1,0,1), an early router with outputs
    (0,0,1,1), and two complementary branch-specific terminal queries.
    There is no arbitrary invention of a new species-by-wind observation.
    """
    costs=(coarse_cost,visible_cost,chemical_cost)
    if any(type(x) is not int or x<1 for x in costs):
        raise ValueError("NO_GO_OBSERVATION_COST_MUST_BE_POSITIVE_INTEGER")
    if removed not in (None,"coarse","visible","chemical"):
        raise ValueError("NO_GO_UNKNOWN_CUE_REMOVAL_NOT_A_SOURCE_OBSERVATION")
    original=extremal_routing_task(2)
    if tuple(w.target for w in original.worlds)!=(0,1,0,1):
        raise ValueError("NO_GO_CANONICAL_4_WORLD_TARGET_CHANGED")
    if tuple(q.outcomes for q in original.queries)!=(
        (0,0,1,1),(0,1,1,1),(0,0,0,1)):
        raise ValueError("NO_GO_ORIGINAL_CANONICAL_ROUTING_STRUCTURE_CHANGED")
    names=(ROUTER,VISUAL,SCENT)
    queries=[]
    for index,q in enumerate(original.queries):
        outcome=(0,0,0,0) if removed==("coarse","visible","chemical")[index] else q.outcomes
        queries.append(Query(names[index],costs[index],outcome))
    return FiniteTask(original.worlds,tuple(queries))


def exact_route_context(coarse_cost:int,visible_cost:int,chemical_cost:int,
                        *,budget:int,removed:str|None=None)->dict[str,Any]:
    """A mathematical cost/availability profile, never calibrated to source wind."""
    if type(budget) is not int or budget<0:
        raise ValueError("NO_GO_ECOLOGICAL_TIME_BUDGET_NOT_INTEGER")
    task=routing_task(coarse_cost=coarse_cost,
                      visible_cost=visible_cost,chemical_cost=chemical_cost,
                      removed=removed)
    a=adaptive_minimum_resolution(task)
    f=fixed_minimum_resolution(task)
    if (a.minimum_worst_path_cost is None)!=(f.minimum_cost is None):
        raise ArithmeticError("NO_GO_ADAPTIVE_FIXED_REACHABILITY_ORDER")
    if removed is None:
        predicted_ca=coarse_cost+max(visible_cost,chemical_cost)
        predicted_cf=coarse_cost+visible_cost+chemical_cost
        if a.minimum_worst_path_cost!=predicted_ca or f.minimum_cost!=predicted_cf:
            raise AssertionError("NO_GO_WEIGHTED_CANONICAL_ROUTABILITY_FORMULA")
    else:
        if a.minimum_worst_path_cost is not None or f.minimum_cost is not None:
            raise AssertionError("NO_GO_COLLAPSED_PRIVATE_CUE_REMAINS_RESOLVABLE")
    ca=a.minimum_worst_path_cost
    cf=f.minimum_cost
    adaptive=ca is not None and ca<=budget
    fixed=cf is not None and cf<=budget
    return {
       "status":"EXACT_CONSTRUCTED_RECEIVER_SENSORY_ROUTEABILITY_NOT_EMPIRICAL",
       "cue_roles":[ROUTER,VISUAL,SCENT],
       "costs_abstract_positive_integer":[coarse_cost,visible_cost,chemical_cost],
       "cue_collapsed_to_constant_or_none":removed or "",
       "environment_budget_abstract_units":budget,
       "exact_adaptive_minimum_worst_case_cost_or_unresolvable":ca,
       "exact_fixed_minimum_bundle_cost_or_unresolvable":cf,
       "conditional_access_gap_or_unknown":cf-ca if ca is not None else None,
       "adaptive_resolves_under_budget":adaptive,
       "fixed_resolves_under_budget":fixed,
       "adaptive_only_within_budget":adaptive and not fixed,
       "first_optimal_query_if_resolvable":list(a.optimal_first_queries),
       "initial_router_direct_target_information_bits":0,
       "observed_flower_signal_strength":None,
       "observed_airflow_m_per_s":None,
       "observed_pollinator_pollen_success":None,
       "no_original_quantitative_wind_to_cost_conversion":True,
       "mathematical_theorem_preexists_in_adaptive_gain":True,
       "different_environment_costs_are_assumptions_not_causal_wind_estimates":True
    }


def exact_opportunity_chain(*,detection,landing_given_detection,
                            pollen_given_landing)->Fraction:
    """Source-free D*L*T chain, only valid as observed for the SAME cohort."""
    vals=(detection,landing_given_detection,pollen_given_landing)
    if any(type(v) not in (Fraction,int) for v in vals):
        raise ValueError("NO_GO_NO_UNVERIFIED_FLOAT_POLLEN_PROBABILITIES")
    v=tuple(Fraction(x) for x in vals)
    if any(x<0 or x>1 for x in v):
        raise ValueError("NO_GO_OUTSIDE_UNIT_STAGE_PROBABILITY")
    return v[0]*v[1]*v[2]


def break_even_landing(*,calm_detection,calm_landing,wind_detection):
    """If pollen conditional on landing is unchanged, exact analytical gate."""
    for key,x in (("calm_detection",calm_detection),
                  ("calm_landing",calm_landing),
                  ("wind_detection",wind_detection)):
        if type(x) not in (Fraction,int) or not Fraction(0)<=x<=Fraction(1):
            raise ValueError("NO_GO_INVALID_BREAK_EVEN_STAGE_"+key)
    if wind_detection==0:
        return None
    return Fraction(calm_detection)*Fraction(calm_landing)/Fraction(wind_detection)


def hypothetical_wind_stage_contrast():
    """No individual or population biological measurement is created."""
    calm=(Fraction(2,5),Fraction(4,5),Fraction(3,4))
    breeze=(Fraction(3,5),Fraction(1,2),Fraction(3,4))
    compensated=(Fraction(3,5),Fraction(3,4),Fraction(3,4))
    t0=exact_opportunity_chain(
         detection=calm[0],landing_given_detection=calm[1],pollen_given_landing=calm[2])
    t1=exact_opportunity_chain(
         detection=breeze[0],landing_given_detection=breeze[1],pollen_given_landing=breeze[2])
    t2=exact_opportunity_chain(
         detection=compensated[0],landing_given_detection=compensated[1],pollen_given_landing=compensated[2])
    threshold=break_even_landing(calm_detection=calm[0],
               calm_landing=calm[1],wind_detection=breeze[0])
    if (t0,t1,t2,threshold)!=(
        Fraction(6,25),Fraction(9,40),Fraction(27,80),Fraction(8,15)
    ):
        raise AssertionError("NO_GO_EXACT_OPPORTUNITY_CHAIN_WIND_CONTRAST")
    return {
       "status":"STAGE34_33_ALREADY_KNOWN_EXACT_CONSTRUCTED_STAGE_CHAIN",
       "calm_per_opportunity_transfer_fraction":str(t0),
       "wind_per_opportunity_transfer_fraction":str(t1),
       "wind_with_visual_motor_compensation_transfer_fraction":str(t2),
       "wind_minus_calm_transfer_fraction":str(t1-t0),
       "break_even_windy_landing_given_discovery_if_same_pollen_fraction":str(threshold),
       "wind_arrival_probability_improves_but_pollen_transfer_declines":True,
       "cannot_join_Crall_Chang_Baird_to_obtain_any_of_these_probabilities":True,
       "wind_routeability_budget_not_equal_to_plant_fitness_measure":True,
    }


def study_integration_receipt():
    for x in SOURCE_SYSTEMS.values():
        if not x["doi"].startswith("10.") or "pollen" not in x["missing"]:
            raise AssertionError("NO_GO_UNSUPPORTED_EMPIRICAL_WIND_POLLEN_JOIN")
    cost_contexts={
      "reference_calm_assumed":exact_route_context(1,2,2,budget=4),
      "facilitated_chemical_cue_but_harder_visual_assumed":exact_route_context(
          1,3,1,budget=4),
      "visual_access_bottleneck_assumed":exact_route_context(1,5,1,budget=4),
      "early_router_disrupted_assumed":exact_route_context(
          1,3,1,budget=4,removed="coarse")
    }
    if [z["adaptive_only_within_budget"] for z in cost_contexts.values()]!=[
        True,True,False,False]:
        raise AssertionError("NO_GO_EXPECTED_TOPOLOGY_ACCESSIBILITY_PHASES")
    return {
       "status":"SOURCE_SCOPED_WIND_SCENT_VISUAL_ROUTEABILITY_MATHEMATICAL_BRIDGE",
       "original_source_systems":SOURCE_SYSTEMS,
       "exact_source_free_routeability_scenarios":cost_contexts,
       "independently_known_source_free_pollen_chain":hypothetical_wind_stage_contrast(),
       "new_falsifiable_hypothesis":"Wind-mediated cue routeability (conditional sensory access), not raw visual/scent cue count, moderates local receiver decisions conditional on guild and environment.",
       "distinct_roles":"scent plume detection, close-range local visual/chemical discrimination, mechanical landing, pollen success",
       "existing_mathematical_result_only":True,
       "ecological_routeability_contrast_not_empirically_estimated":True,
       "no_causal_visual_x_scent_x_wind_factorial_available":True,
       "source_studies_not_same_insects_or_source_flower_system":True,
       "no_automatic_pollinator_derived_evolutionary_selection_or_feedback_oscillation":True,
    }


def main():
    out=Path("stage58_wind_scent_visual_routeability")
    out.mkdir(exist_ok=True)
    receipt=study_integration_receipt()
    path=out/"exact_constructed_routeability_and_original_source_separation.json"
    path.write_text(json.dumps(receipt,sort_keys=True,ensure_ascii=False,indent=2)+"\n",
                    encoding="utf8")
    print("STAGE58_EXACT_SOURCE_FREE_FLORAL_WIND_SCENT_ROUTEABILITY",
          json.dumps(receipt,sort_keys=True,ensure_ascii=False))
    print("NO_REAL_WIND_SENSORY_PATH_POLARIZATION_OR_POLLEN_ESTIMATED")

if __name__=="__main__":
    main()
