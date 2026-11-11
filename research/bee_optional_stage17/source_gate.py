"""Original-record contract for a *future* optional-first-cue experiment.

This module explicitly REJECTS real animal data in this public synthetic
research branch. Device delays are fake source QA fixture values, NOT
independently calibrated thresholds for a real pilot.
"""
from __future__ import annotations
from collections import Counter
import math,random
from allocation import generate,audit,COSTS,MODES

MOCK_DELAYS={"low":.2,"medium":1.,"high":3.}
SENSOR_OK={"measured","verified_no_intake"}
ROOT_TIME=1.0
POST_ROOT_DISPATCH=1.6
WINDOW=30.0
TOLERANCE=.03

def make_mock_source(assignments,inject_middle_only_mg=2.,seed=20261111):
    """Inject an illustrative middle-cost gain; NEVER real bee performance."""
    audit(assignments)
    rng=random.Random(seed)
    cols=sorted({x["colony_id"] for x in assignments})
    rows=[]
    for r in assignments:
        tier=r["cost_tier"];mode=r["access_mode"]
        root=r["r"]
        relevant="U" if root==0 else "V"
        preleaf="U" if int(r["trial_id"][-3:])%2 else "V"
        if tier=="high":
            first="SKIP"
        elif mode=="contingent":
            first=relevant
        else:
            first=preleaf
        leaf_events=[]
        if first!="SKIP":
            first_reveal=POST_ROOT_DISPATCH+MOCK_DELAYS[tier]
            leaf_events.append({"leaf":first,"origin":"animal",
                "request_s":.5 if mode=="precommit" else 1.3,
                "dispatch_s":POST_ROOT_DISPATCH,
                "reveal_s":first_reveal,
                "measured_delay_s":MOCK_DELAYS[tier],
                "observed_value":r["u"] if first=="U" else r["v"]})
            if first!=relevant:
                second=relevant
                dispatch=first_reveal+.15
                leaf_events.append({"leaf":second,"origin":"animal",
                    "request_s":first_reveal+.10,
                    "dispatch_s":dispatch,
                    "reveal_s":dispatch+MOCK_DELAYS[tier],
                    "measured_delay_s":MOCK_DELAYS[tier],
                    "observed_value":r["u"] if second=="U" else r["v"]})
        last_reveal=leaf_events[-1]["reveal_s"] if leaf_events else None
        gate=2.0 if last_reveal is None else last_reveal+.30
        if first=="SKIP":choice=rng.choice((0,1))
        else:choice=r["correct_target"]
        idx=cols.index(r["colony_id"])
        mid_effect=(inject_middle_only_mg+.04*(idx-(len(cols)-1)/2)) if (
            tier=="medium" and mode=="contingent") else 0.
        mass=max(0.,20.+mid_effect+rng.gauss(0,.10))
        rows.append({
            "trial_id":r["trial_id"],"colony_id":r["colony_id"],
            "bee_id":r["bee_id"],"access_mode":mode,"cost_tier":tier,
            "source_original_animal_actions_video_verified":True,
            "source_motor_sham_control_verified":True,
            "source_first_request_origin":"animal" if first!="SKIP" else "animal_skip",
            "source_is_synthetic_QA_only":True,
            "first_action":first,
            "binding_action_time_s":.5 if mode=="precommit" else 1.3,
            "root_display_s":ROOT_TIME,"source_root_bit":root,
            "source_leaf_events":leaf_events,
            "physical_leaf_requests":len(leaf_events),
            "original_cost_delay_tier":tier,
            "feeder_access_s":gate,
            "final_choice_time_s":gate+.10,
            "both_target_options_accessible":True,
            "target_zero_side_source":r["target_zero_side"],
            # Both nominal offered rewards are FAKE source QA fixtures;
            # actual dose and leak-free calibration require a new pilot.
            "rewarded_target_bit_source":r["correct_target"],
            "source_calibrated_nominal_high_mg":50.0,
            "source_calibrated_nominal_low_mg":30.0,
            "source_high_low_recipe_original_device_verified":True,
            "source_reward_location_cues_masked":True,
            "predictive_cue_visible_at_feeder":False,
            "root_anchor_s":ROOT_TIME,
            "intake_window_s":WINDOW,
            "final_target_choice":choice,
            "sensor_status":"measured",
            "verified_consumed_sucrose_mg":mass,
            "feeding_contact_verified":True,
            "feeder_mass_calibrated":True,
            "blank_loss_corrected":True})
    return rows


def _tier_source_pilot(pilot):
    if not isinstance(pilot,dict) or set(pilot)!=set(COSTS):
        raise ValueError("NO_GO_INDEPENDENT_PILOT_DELAY_TIERS_REQUIRED")
    for k in COSTS:
        b=pilot[k]
        if not isinstance(b,(tuple,list)) or len(b)!=2 or not all(type(x) in (int,float)
               and math.isfinite(x) for x in b) or not 0<=b[0]<b[1]:
            raise ValueError("NO_GO_UNCALIBRATED_OR_INVALID_DEVICE_COST")
    if not (pilot["low"][1]<pilot["medium"][0] and pilot["medium"][1]<pilot["high"][0]):
        raise ValueError("NO_GO_COST_TIERS_OVERLAP")
    return True


def validate_mock_source(assignments,source,pilot_delays):
    audit(assignments)
    _tier_source_pilot(pilot_delays)
    if not isinstance(source,list) or len(source)!=len(assignments):
        raise ValueError("NO_GO_MISSING_ALL_ASSIGNED_SOURCE_TRIALS")
    lookup={r["trial_id"]:r for r in assignments}
    seen=set();byarm=Counter();skips=Counter();events_count=0;validated=[]
    for row in source:
        tid=row.get("trial_id")
        if tid not in lookup or tid in seen:
            raise ValueError("NO_GO_DUPLICATE_OR_UNKNOWN_SOURCE_TRIAL")
        seen.add(tid)
        assigned=lookup[tid]
        mode=assigned["access_mode"];tier=assigned["cost_tier"]
        byarm[tier,mode]+=1
        if (row.get("source_is_synthetic_QA_only") is not True or
            row.get("source_original_animal_actions_video_verified") is not True or
            row.get("source_motor_sham_control_verified") is not True):
            raise ValueError("NO_GO_ANIMAL_ACTION_NOT_VERIFIED_OR_REAL_DATA_NOT_ACCEPTED")
        if row.get("access_mode")!=mode or row.get("cost_tier")!=tier or row.get("original_cost_delay_tier")!=tier:
            raise ValueError("NO_GO_REROUTED_SOURCE_ASSIGNED_MODE_OR_COST")
        if row.get("source_root_bit")!=assigned["r"] or abs(row.get("root_display_s",-1)-ROOT_TIME)>TOLERANCE:
            raise ValueError("NO_GO_ROOT_CUE_SOURCE_IDENTITY_OR_CLOCK")
        action=row.get("first_action")
        if action not in ("SKIP","U","V"):
            raise ValueError("NO_GO_FIRST_INFORMATION_ACTION_UNRECOGNIZED")
        if row.get("source_first_request_origin")!=("animal_skip" if action=="SKIP" else "animal"):
            raise ValueError("NO_GO_NOT_ANIMAL_ORIGIN_FIRST_INFORMATION_ACTION")
        tbind=row.get("binding_action_time_s")
        if type(tbind) not in (float,int) or not math.isfinite(tbind) or (
           mode=="precommit" and not (0<=tbind<ROOT_TIME)) or (
           mode=="contingent" and not (ROOT_TIME<tbind<POST_ROOT_DISPATCH)):
            raise ValueError("NO_GO_BINDING_ACTION_TIME_INCORRECT")
        events=row.get("source_leaf_events")
        if not isinstance(events,list) or len(events)>2:
            raise ValueError("NO_GO_INVALID_SOURCE_LEAF_EVENTS")
        if action=="SKIP":
            if events or row.get("physical_leaf_requests")!=0:
                raise ValueError("NO_GO_SOURCE_SKIP_MASQUERADING_AS_QUERY")
            skips[tier]+=1
        else:
            if not events or events[0].get("leaf")!=action:
                raise ValueError("NO_GO_MISSING_ANIMAL_FIRST_QUERY")
        first_reveal=None;last_reveal=None;previous_leaf=None
        for index,e in enumerate(events):
            leaf=e.get("leaf")
            if leaf not in ("U","V") or e.get("origin")!="animal":
                raise ValueError("NO_GO_NOT_ANIMAL_ORIGIN_LEAF_REQUEST")
            if leaf==previous_leaf:
                raise ValueError("NO_GO_SECOND_LEAF_MUST_DIFFER")
            t_req=e.get("request_s");t_disp=e.get("dispatch_s")
            t_reveal=e.get("reveal_s");cost=e.get("measured_delay_s")
            if any(type(v) not in (int,float) or not math.isfinite(v) for v in
                   (t_req,t_disp,t_reveal,cost)):
                raise ValueError("NO_GO_SOURCE_QUERY_CHRONOLOGY")
            if index==0:
                if abs(t_disp-POST_ROOT_DISPATCH)>TOLERANCE or (
                    mode=="precommit" and abs(t_req-tbind)>TOLERANCE) or (
                    mode=="contingent" and abs(t_req-tbind)>TOLERANCE):
                    raise ValueError("NO_GO_SOURCE_QUERY_CHRONOLOGY")
            else:
                if not (last_reveal<t_req<=t_disp):
                    raise ValueError("NO_GO_SOURCE_QUERY_CHRONOLOGY")
            if not pilot_delays[tier][0]<=cost<=pilot_delays[tier][1]:
                raise ValueError("NO_GO_SOURCE_COST_DELAY_OUTSIDE_PILOT")
            if not (t_disp>ROOT_TIME and t_reveal>t_disp and
                    abs((t_reveal-t_disp)-cost)<TOLERANCE):
                raise ValueError("NO_GO_SOURCE_QUERY_CHRONOLOGY")
            if e.get("observed_value")!=(assigned["u"] if leaf=="U" else assigned["v"]):
                raise ValueError("NO_GO_SOURCE_LEAF_VALUE_NOT_ORIGINAL")
            first_reveal=t_reveal if index==0 else first_reveal
            previous_leaf=leaf;last_reveal=t_reveal
        if row.get("physical_leaf_requests")!=len(events):
            raise ValueError("NO_GO_MISMATCH_SOURCE_PAID_QUERY_COUNT")
        events_count+=len(events)
        gate=row.get("feeder_access_s")
        target_time=row.get("final_choice_time_s")
        expected=2.0 if last_reveal is None else last_reveal+.30
        if (type(gate) not in (float,int) or not math.isfinite(gate) or
            abs(gate-expected)>TOLERANCE or
            type(target_time) not in (float,int) or
            not gate<=target_time<ROOT_TIME+WINDOW):
            raise ValueError("NO_GO_FEEDER_RELEASE_CHRONOLOGY")
        if row.get("rewarded_target_bit_source")!=assigned["correct_target"]:
            raise ValueError("NO_GO_PHYSICAL_REWARD_TARGET_BIT_MISMATCH")
        high=row.get("source_calibrated_nominal_high_mg")
        low=row.get("source_calibrated_nominal_low_mg")
        if (type(high) not in (float,int) or type(low) not in (float,int) or
            not math.isfinite(high) or not math.isfinite(low) or not (0<=low<high) or
            row.get("source_high_low_recipe_original_device_verified") is not True or
            row.get("source_reward_location_cues_masked") is not True):
            raise ValueError("NO_GO_PHYSICAL_REWARD_MAPPING_NOT_BLINDED_OR_CALIBRATED")
        if row.get("target_zero_side_source")!=assigned["target_zero_side"] or (
            row.get("both_target_options_accessible") is not True or
            row.get("predictive_cue_visible_at_feeder") is not False):
            raise ValueError("NO_GO_ORIGINAL_CHOICE_TARGET_GEOMETRY_OR_LEAKAGE")
        if row.get("root_anchor_s")!=ROOT_TIME or row.get("intake_window_s")!=WINDOW:
            raise ValueError("NO_GO_MEASUREMENT_TIME_REANCHORED_TO_LAST_QUERY")
        if row.get("sensor_status") not in SENSOR_OK:
            raise ValueError("NO_GO_SOURCE_SENSOR_FAILURE_IS_NOT_REAL_ZERO")
        mass=row.get("verified_consumed_sucrose_mg")
        if type(mass) not in (int,float) or not math.isfinite(mass) or mass<0:
            raise ValueError("NO_GO_SOURCE_UNVERIFIED_INTAKE")
        if row["sensor_status"]=="verified_no_intake" and mass!=0:
            raise ValueError("NO_GO_SOURCE_NO_DRINK_INTAKE_MISMATCH")
        choice=row.get("final_target_choice")
        if choice not in (0,1,"no_choice") or (choice=="no_choice" and mass!=0):
            raise ValueError("NO_GO_ORIGINAL_TARGET_OR_NO_CHOICE_MISMATCH")
        if (mass>0 and row.get("feeding_contact_verified") is not True) or (
             row.get("feeder_mass_calibrated") is not True or
             row.get("blank_loss_corrected") is not True):
            raise ValueError("NO_GO_SOURCE_FEEDER_BLANK_VIDEO_VALIDATION_MISSING")
        validated.append({**row,"correct_target":assigned["correct_target"]})
    if seen!=set(lookup):
        raise ValueError("NO_GO_INCOMPLETE_INTENTION_TO_TREAT")
    if len(byarm)!=6:
        raise ValueError("NO_GO_NOT_ALL_SIX_DESIGN_ARMS")
    receipt={
       "status":"SYNTHETIC_OPTIONAL_QUERY_SOURCE_GATE_PASSED",
       "n_fake_trials":len(source),
       "six_original_arms":{"__".join(k):int(v) for k,v in sorted(byarm.items())},
       "source_explicit_skip_trials":int(sum(skips.values())),
       "source_skip_counts_by_cost":dict(skips),
       "physical_first_and_second_leaf_events":events_count,
       "all_original_bee_actions_video_flagged_only_in_mock":True,
       "real_animal_original_video_audited":False,
       "all_device_cost_calibration_ranges_are_fictitious_QA":True,
       "original_intake_window_anchored_to_root_in_all_trials":True,
       "no_real_bees":True}
    return receipt,validated


if __name__=="__main__":
    import json
    a=generate(6,6)
    gate,_=validate_mock_source(a,make_mock_source(a),
             {"low":(.19,.21),"medium":(.99,1.01),"high":(2.99,3.01)})
    print("STAGE17_SYNTHETIC_SOURCE_GATE "+json.dumps(gate))
