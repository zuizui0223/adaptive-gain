"""Stage 8 observational action-to-visit episode GRAIN AUDIT only.

Original Cambridge Observation_data.csv: source rows are action-duration
records, NOT one row per visit or absolute timestamps. Flower ID is a
per-visit GROUPING IDENTIFIER and NOT a persistent physical flower location.
Preserve native event order within each identified bee, never sort events by
their duration. No cross-bout source links.
"""
from __future__ import annotations
from collections import Counter,defaultdict
import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

ORIGINAL_OBS_SHA256="c38d18df02cb4feb492b86b0f4b5ca0c767388c69bac0be1b44262d0f39e7d33"
ORIGINAL_MASS_SHA256="a37ac38b137e35332a8fa1a62956617f0c4ea124f84636a6118fc73c99575f8b"
VISIT_ACTIONS={
    "horizontalLandVisit":("horizontal","land",False),
    "horizontalLandDrink":("horizontal","land",True),
    "landVisit":("vertical","land",False),
    "landDrink":("vertical","land",True),
    "hoverVisit":("vertical","hover",False),
    "hoverDrink":("vertical","hover",True),
}
NONVISIT={"boutStartStop","leaveFlower","rest"}
EXPECTED_HEADERS=[
    "Colony","Bee","Treatment","Surface","Flower ID","Observation",
    "Time (ms)","Foraging trip","Visit number","Drink number"
]
EXPECTED_COLONIES={"1","2","3"}
EXPECTED_SURFACES={"Micro-rough","Coarse-rough"}
EXPECTED_TREATMENT={"Control","Low Difference","High Difference"}
EXPECTED_SOURCE_OBSERVATION_ROWS=61592
EXPECTED_SOURCE_INDIVIDUAL_BEES=38

def native_rows(raw):
    decoded=raw.decode("utf-8-sig",errors="strict")
    reader=csv.DictReader(decoded.splitlines())
    if reader.fieldnames!=EXPECTED_HEADERS:
        raise ValueError("NO_GO_CHANGED_SOURCE_BEHAVIOR_COLUMNS")
    out=list(reader)
    if any(None in v for v in out):raise ValueError("NO_GO_RAGGED_SOURCE_BEHAVIOR")
    return out

def episode_key(row):
    return (row["Colony"].strip(),row["Bee"].strip(),
            row["Surface"].strip(),row["Foraging trip"].strip(),
            row["Flower ID"].strip())

def source_episode_audit(rows,source_expected=(EXPECTED_SOURCE_OBSERVATION_ROWS,
                                               EXPECTED_SOURCE_INDIVIDUAL_BEES)):
    if not rows:raise ValueError("NO_GO_EMPTY_BEHAVIORAL_SOURCE")
    key_episodes=defaultdict(list)
    bees=defaultdict(list)
    counts=Counter()
    action_by_phase=Counter()
    incomplete_times=0
    invalid_times=0
    source_time_totals=Counter()
    malformed=[]
    for i,row in enumerate(rows):
        obs=row["Observation"].strip()
        c=row["Colony"].strip()
        b=row["Bee"].strip()
        treatment=row["Treatment"].strip()
        surf=row["Surface"].strip()
        if obs not in VISIT_ACTIONS and obs not in NONVISIT:
            malformed.append({"source_event":i,"problem":"unknown original observation label",
                              "label":obs})
        if c not in EXPECTED_COLONIES or surf not in EXPECTED_SURFACES or treatment not in EXPECTED_TREATMENT:
            malformed.append({"source_event":i,"problem":"original treatment, colony or surface unknown"})
        t=row["Time (ms)"].strip()
        if t in ("", "NA","N/A","nan"):
            incomplete_times+=1
        else:
            try:
                duration=float(t)
                if duration<0 or not (duration<float("inf")):
                    raise ValueError("nonfinite duration")
                source_time_totals[obs]+=duration
            except Exception:
                invalid_times+=1
        counts[obs]+=1
        action_by_phase[(surf,obs)]+=1
        key_episodes[(c,b)].append((i,row))
    unique_bees=len(key_episodes)
    if source_expected is not None and (len(rows),unique_bees)!=source_expected:
        raise ValueError("NO_GO_ORIGINAL_CAMBRIDGE_SOURCE_POPULATION_CHANGED")
    episodes=[]
    cross_run_same_flower_id=Counter()
    previous_id_seen=defaultdict(set)
    raw_rows_in_visits=0
    invalid_trip_values=0
    bee_source_runs=Counter()
    by_colony=Counter()
    by_treatment=Counter()
    by_surface=Counter()
    no_flower_action_episodes=0
    nonunique_orientation=0
    mixed_surface_per_bee=Counter()
    for (colony,bee),events in key_episodes.items():
        lastkey=None
        segment=[]
        bee_source_runs[(colony,bee)]=len(events)
        def push_group():
            nonlocal no_flower_action_episodes,nonunique_orientation,raw_rows_in_visits
            if not segment:return
            first=segment[0][1]
            visit_actions=[(idx,rr,rr["Observation"].strip()) for idx,rr in segment
                           if rr["Observation"].strip() in VISIT_ACTIONS]
            if not visit_actions:
                no_flower_action_episodes+=1
                return
            orientations={VISIT_ACTIONS[x[2]][0] for x in visit_actions}
            if len(orientations)!=1:
                nonunique_orientation+=1
            orientations_present=sorted(orientations)
            handling={VISIT_ACTIONS[x[2]][1] for x in visit_actions}
            drank=any(VISIT_ACTIONS[x[2]][2] for x in visit_actions)
            hover=any(VISIT_ACTIONS[x[2]][1]=="hover" for x in visit_actions)
            land=any(VISIT_ACTIONS[x[2]][1]=="land" for x in visit_actions)
            raw_rows_in_visits+=len(visit_actions)
            episodes.append({
                "colony":colony,"bee":bee,
                "bee_key":(colony,bee),
                "surface":first["Surface"].strip(),
                "treatment":first["Treatment"].strip(),
                "trip":first["Foraging trip"].strip(),
                "source_flower_group_id":first["Flower ID"].strip(),
                "source_visit_number":first["Visit number"].strip(),
                "source_first_row":segment[0][0],
                "source_last_row":segment[-1][0],
                "actions_in_original_group":len(segment),
                "recorded_venue_actions":len(visit_actions),
                "orientations":orientations_present,
                "orientation":orientations_present[0] if len(orientations)==1 else "__AMBIGUOUS__",
                "hover_observed":hover,
                "land_observed":land,
                "drank":drank,
                "initial_action":visit_actions[0][2],
                "original_record_order_not_physical_coordinates":True
            })
        for idx,row in events:
            k=episode_key(row)
            if lastkey!=k:
                push_group()
                segment=[]
                if k in previous_id_seen[(colony,bee)]:
                    cross_run_same_flower_id[(colony,bee)]+=1
                previous_id_seen[(colony,bee)].add(k)
                lastkey=k
            segment.append((idx,row))
        push_group()
        by_colony[colony]+=len(events)
    for episode in episodes:
        by_treatment[episode["treatment"]]+=1
        by_surface[episode["surface"]]+=1
    by_group=Counter((e["colony"],e["bee"]) for e in episodes)
    by_episodesource_type=Counter(
        (e["surface"],e["orientation"],str(e["hover_observed"]),str(e["land_observed"]),str(e["drank"]))
        for e in episodes)
    keys_by_source=Counter(episode_key(v) for v in rows)
    report={
        "original_action_rows":len(rows),
        "original_source_bee_keys":unique_bees,
        "original_colonies":len(set(k[0] for k in key_episodes)),
        "source_action_counts":dict(counts),
        "action_by_source_surface":{f"{s}:{x}":n for (s,x),n in action_by_phase.items()},
        "missing_recorded_action_durations_ms":incomplete_times,
        "invalid_recorded_action_durations_ms":invalid_times,
        "n_source_bad_behavior_labels_or_assignments":len(malformed),
        "small_bad_source_examples":malformed[:12],
        "source_total_action_duration_ms_by_activity":dict(source_time_totals),
        "source_event_row_count_by_colony":dict(by_colony),
        "source_visit_episodes_reconstructed":len(episodes),
        "source_visit_actions_within_episodes":raw_rows_in_visits,
        "source_no_valid_flower_action_episode_groups":no_flower_action_episodes,
        "source_flower_episodes_conflicting_orientation":nonunique_orientation,
        "source_repeat_noncontiguous_flower_id_groups":sum(cross_run_same_flower_id.values()),
        "source_flower_ID_distinct_BEFORE_grouping":len(keys_by_source),
        "unique_tagged_bees_with_actual_visits":len(by_group),
        "source_visit_episode_counts_by_surface":dict(by_surface),
        "source_visit_episode_counts_by_treatment":dict(by_treatment),
        "source_episode_type_counts":{"|".join(x):n for x,n in by_episodesource_type.items()},
        "source_bee_episode_number_range":{
            "min":min(by_group.values()) if by_group else 0,
            "median":sorted(by_group.values())[len(by_group)//2] if by_group else 0,
            "max":max(by_group.values()) if by_group else 0},
        "original_row_order_is_sequence_within_a_bee_not_sorted_by_duration":True,
        "source_Time_ms_is_duration_NOT_absolute_timestamp":True,
        "Flower_ID_is_a_visit_episode_not_physical_coordinate":True,
        "no_experimental_true_reward_received_per_visit_assumed":True,
        "original_source_two_incomplete_bees_reported_by_publisher":[
            "Yellow 4","Green 47"],
        "original_source_bee_mass_Pink60_imputed_by_publisher":True,
    }
    return episodes,report

def run(folder):
    original=(folder/"Observation_data.csv").read_bytes()
    if hashlib.sha256(original).hexdigest()!=ORIGINAL_OBS_SHA256:
        raise ValueError("NO_GO_Cambridge_SOURCE_ObservationData_BYTE_CHANGE")
    mass=(folder/"Bee_masses.csv").read_bytes()
    if hashlib.sha256(mass).hexdigest()!=ORIGINAL_MASS_SHA256:
        raise ValueError("NO_GO_CAMBRIDGE_SOURCE_BEE_MASS_BYTE_CHANGE")
    data=native_rows(original)
    episodes,report=source_episode_audit(data)
    (folder/"cambridge_behavior_episode_qa.json").write_text(
        json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False))
    print("STAGE8_BEE_EPISODE_SOURCE_AUDIT "+
          json.dumps(report,ensure_ascii=False,allow_nan=False),flush=True)
    print("STAGE8_SOURCE_EPISODE_AUDIT_COMPLETE",flush=True)
    return episodes,report

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--out",default="bee_stage8_source")
    a=p.parse_args()
    run(Path(a.out))
