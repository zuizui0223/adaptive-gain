"""Stage61 exact DESIGN nonidentification of previously published 2017 experiment.

This is an elementary four-arm factorial identifiability calculation, NOT
a newly discovered biological effect or theorem. No published original bee
outcome rates are used: example fractions deliberately hypothetical.

Four original 2017 wind experiment groups (n=18 bees per arm):
 A: wind=0, odor=1, colour=0; B: wind=1, odor=1, colour=0;
 C: wind=1, odor=1, colour=1; D: wind=1, odor=0, colour=1.
The full 2x2x2 has 8 cells; the four missing cells permit opposite signs
for the wind*vision effect holding odor, and for 3-way interaction.

Even a true fully crossed design would not identify causal *cue-order
routing* without experimentally randomizing the early cue identity
and recording later cue requests, costs and the same animal's behavior.
"""
from __future__ import annotations
from fractions import Fraction
import itertools,json
from pathlib import Path

ORIGINAL_2017_WIND_ARM_KEYS={
  "A_no_wind_odor_only":(0,1,0),
  "B_wind_odor_only":(1,1,0),
  "C_wind_odor_visual":(1,1,1),
  "D_wind_visual_only":(1,0,1),
}
ALL_CELLS=tuple(itertools.product((0,1),repeat=3))
EXAMPLE={
  "A_no_wind_odor_only":Fraction(3,5),
  "B_wind_odor_only":Fraction(2,5),
  "C_wind_odor_visual":Fraction(7,10),
  "D_wind_visual_only":Fraction(13,20),
}

def _prob(x):
    if type(x) not in (int,Fraction):
        raise ValueError("NO_GO_NOT_EXACT_CONSTRUCTED_PROBABILITY")
    f=Fraction(x)
    if not 0<=f<=1:raise ValueError("NO_GO_OUT_OF_RANGE_CONSTRUCTED_STAGE_RATE")
    return f

def observed_cells(arm_values):
    if not isinstance(arm_values,dict) or set(arm_values)!=set(ORIGINAL_2017_WIND_ARM_KEYS):
        raise ValueError("NO_GO_WRONG_PUBLISHED_2017_FOUR_ARM_DESIGN")
    return {ORIGINAL_2017_WIND_ARM_KEYS[k]:_prob(v) for k,v in arm_values.items()}

def three_factor_additive_interaction(p):
    if set(p)!=set(ALL_CELLS):
        raise ValueError("NO_GO_NOT_ALL_EIGHT_CELLS_FOR_THREE_FACTOR")
    return sum(
       Fraction(-1 if sum(cell)%2==0 else 1)*p[cell]
       for cell in ALL_CELLS
    )

def wind_vision_at_odor_one(p):
    need={(1,1,1),(1,1,0),(0,1,1),(0,1,0)}
    if not need.issubset(p):
        raise ValueError("NO_GO_MISSING_NO_WIND_COLORED_ODOR_CELL")
    return (p[(1,1,1)]-p[(1,1,0)])-(p[(0,1,1)]-p[(0,1,0)])

def exact_bounds(arm_values):
    known=observed_cells(arm_values)
    absent=tuple(c for c in ALL_CELLS if c not in known)
    if len(absent)!=4:
        raise AssertionError("NO_GO_SOURCE_FOUR_MISSING_FACTORIAL_CELLS")
    source_contrasts={
      "wind_effect_odor_only":known[(1,1,0)]-known[(0,1,0)],
      "visual_added_with_wind_and_odor":known[(1,1,1)]-known[(1,1,0)],
      "odor_added_with_wind_and_visual":known[(1,1,1)]-known[(1,0,1)],
    }
    example_candidates=[]
    wind_visual=[]
    for corners in itertools.product((Fraction(0),Fraction(1)),repeat=4):
        full={**known,**dict(zip(absent,corners))}
        example_candidates.append(three_factor_additive_interaction(full))
        wind_visual.append(wind_vision_at_odor_one(full))
    t_min,t_max=min(example_candidates),max(example_candidates)
    w_min,w_max=min(wind_visual),max(wind_visual)
    return {
      "status":"EXACT_SHARP_MISSING_2017_FACTORIAL_ARM_IDENTIFIABILITY_GATE",
      "published_source_wind_group_arm_keys":{k:list(v) for k,v in ORIGINAL_2017_WIND_ARM_KEYS.items()},
      "published_original_bees_per_arm":18,
      "original_wind_four_arm_number":4,
      "full_three_factor_number_cells":8,
      "missing_factorial_wind_odor_visible_cells":[list(c) for c in absent],
      "constructed_example_observed_arm_rates":{k:str(v) for k,v in arm_values.items()},
      "observed_edge_contrasts_only_if_outcome_measured":
          {k:str(v) for k,v in source_contrasts.items()},
      "hypothetical_sharp_wind_by_visual_at_odor_one_bounds":[str(w_min),str(w_max)],
      "hypothetical_sharp_wind_by_odor_by_visual_bounds":[str(t_min),str(t_max)],
      "both_interactions_can_switch_sign_under_unmeasured_cells":
          w_min<0<w_max and t_min<0<t_max,
      "no_pollen_or_original_bee_rate_used_in_example":True,
      "order_contingent_route_policy_unobserved":True,
      "full_factorial_is_necessary_not_sufficient_for_cue_order_causal_claim":True,
      "not_novel_theorem_or_empirical_result":True,
    }

def main():
    receipt=exact_bounds(EXAMPLE)
    if receipt["hypothetical_sharp_wind_by_visual_at_odor_one_bounds"]!=["-1/10","9/10"]:
        raise AssertionError("NO_GO_2017_EXACT_4_ARM_WIND_VISION_BOUND")
    if receipt["hypothetical_sharp_wind_by_odor_by_visual_bounds"]!=["-7/4","9/4"]:
        raise AssertionError("NO_GO_2017_EXACT_THREE_WAY_BOUND")
    out=Path("stage61_2017_factorial_nonidentification")
    out.mkdir(exist_ok=True)
    (out/"2017_existing_wind_backup_design_missing_conditional_routing_example.json").write_text(
       json.dumps(receipt,indent=2,ensure_ascii=False,sort_keys=True)+"\n",encoding="utf8")
    print("STAGE61_EXISTING_2017_FOUR_ARM_NOT_EXACT_WIND_VISUAL_ODOR_ROUTING_FACTORIAL",
          json.dumps(receipt,sort_keys=True))
    print("NO_EXISTING_2017_ANIMAL_RESPONSE_ESTIMATED_FROM_SOURCE_FREE_EXAMPLE")
if __name__=="__main__":
    main()
