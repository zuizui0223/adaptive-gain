"""Read author-original Smolla2016 ordered visits without fitting a cue-choice effect.

Strictly preserve original flower identities 1..12 and train/test bee pairing.
A landing sequence is NOT a sensory cue acquisition sequence.
"""
from __future__ import annotations
import csv,json,hashlib
from collections import Counter,defaultdict
from pathlib import Path

ORIGINAL_SHA256="248b8257ac4a756a16704eaedbabd3909f24be1d8bd6d4a64e6bcbb100ee8e65"
FIELDS=("colony","id","cueType","group","landed","cue","reward","firstLanding","lastLanding")

def parse_positions(text):
    parts=str(text).strip().split()
    if not parts:raise ValueError("NO_GO_EMPTY_ORIGINAL_LANDING_SEQUENCE")
    try:values=[int(v) for v in parts]
    except ValueError as e:raise ValueError("NO_GO_NONINTEGER_ORIGINAL_FLOWER_INDEX") from e
    if any(not 1<=v<=12 for v in values):
        raise ValueError("NO_GO_ORIGINAL_FLOWER_INDEX_OUTSIDE_ONE_TO_TWELVE")
    return values

def audit_rows(rows,expected_original=True):
    if not rows:raise ValueError("NO_GO_NO_ORIGINAL_BEES")
    if any(set(FIELDS)-set(row) for row in rows):
        raise ValueError("NO_GO_ORIGINAL_COLUMN_SET_CHANGED")
    groups=Counter()
    cues=Counter()
    pair=defaultdict(list)
    count={"dummy_last":0,"test_easy":0,"test_diff":0}
    samples={"dummy_last":[],"test_easy":[],"test_diff":[]}
    nonreward=Counter()
    cue_counts=Counter()
    for row in rows:
        gid=row["group"].strip()
        if gid not in count:raise ValueError("NO_GO_SOURCE_EXPERIMENT_PHASE")
        colony=row["colony"].strip();bee=row["id"].strip()
        if not bee or not colony:raise ValueError("NO_GO_MISSING_ORIGINAL_ANIMAL_ID")
        key=(colony,bee)
        positions=parse_positions(row["landed"])
        attached=parse_positions(row["cue"])
        if len(set(attached))!=len(attached):
            raise ValueError("NO_GO_REPEATED_CUE_FLOWER_WITHIN_BOUT")
        try:early=float(row["firstLanding"]);last=float(row["lastLanding"])
        except Exception as e:raise ValueError("NO_GO_ORIGINAL_LATENCY_UNPARSEABLE") from e
        if not (0<=early<=last):raise ValueError("NO_GO_ORIGINAL_LATENCY_OUT_OF_ORDER")
        pair[key].append({"phase":gid,"cue_type":row["cueType"].strip()})
        groups[gid]+=1
        cues[(gid,row["cueType"].strip())]+=1
        cue_counts[len(attached)]+=1
        count[gid]+=len(positions)
        samples[gid].append(len(positions))
        nonreward[(gid,str(row["reward"]).strip().lower())]+=1
    anomalies=[]
    for (colony,bee),items in pair.items():
        phases=[x["phase"] for x in items]
        if len(items)!=2 or Counter(phases)!=Counter({"dummy_last":1,"test_easy":1}) and Counter(phases)!=Counter({"dummy_last":1,"test_diff":1}):
            anomalies.append({"bee":bee,"colony":colony,"phases":phases})
        if len({x["cue_type"] for x in items})!=1:
            anomalies.append({"bee":bee,"colony":colony,"cue_type_changed":True})
    if anomalies:raise ValueError("NO_GO_PAIRED_TRAIN_TEST "+json.dumps(anomalies[:4]))
    if expected_original and (len(rows),len(pair),groups)!=(
        114,57,Counter({"dummy_last":57,"test_easy":29,"test_diff":28})):
        raise ValueError("NO_GO_ORIGINAL_SOURCE_BEE_GRAIN_CHANGED")
    test_bees=sum(any(x["phase"].startswith("test_") for x in items) for items in pair.values())
    train_bees=sum(any(x["phase"]=="dummy_last" for x in items) for items in pair.values())
    return {
       "status":"SOURCE_ONLY_ORIGINAL_BEE_AND_EVENT_GRAIN_VERIFIED",
       "original_rows":len(rows),"original_bees":len(pair),
       "source_train_bees":train_bees,"source_test_bees":test_bees,
       "unique_one_train_one_test_per_bee":True,
       "original_group_rows":dict(sorted(groups.items())),
       "original_cue_types_by_phase":{
           gid:dict(sorted({typ:n for (g,typ),n in cues.items() if g==gid}.items()))
           for gid in ("dummy_last","test_easy","test_diff")},
       "cue_flower_number_per_row_distribution":dict(sorted(cue_counts.items())),
       "train_landing_events":count["dummy_last"],
       "test_landing_events":count["test_easy"]+count["test_diff"],
       "test_landing_counts_by_original_group":{
           "test_easy":count["test_easy"],"test_diff":count["test_diff"]},
       "native_visit_sequence_min_max":{
           k:[min(v),max(v)] for k,v in samples.items() if v},
       "native_reward_field_forms_by_phase":{
           gid:{reward_form:n for (group,reward_form),n in nonreward.items()
                if group==gid}
           for gid in ("dummy_last","test_easy","test_diff")},
       "original_test_no_new_reward_inferred":True,
       "no_cue_preference_or_biological_effect_fit":True,
       "not_actual_sensory_query_timestamps":True,
    }

def run(root):
    root=Path(root);raw=(root/"beeLandings.csv").read_bytes()
    if hashlib.sha256(raw).hexdigest()!=ORIGINAL_SHA256:
        raise ValueError("NO_GO_ORIGINAL_BEE_LANDINGS_HASH_CHANGED")
    try:txt=raw.decode("utf-8-sig")
    except UnicodeDecodeError:txt=raw.decode("latin-1")
    rows=list(csv.DictReader(txt.splitlines()))
    report=audit_rows(rows)
    report["original_file_sha256"]=ORIGINAL_SHA256
    report["source_doi"]="10.5061/dryad.3jb68"
    out=root/"smolla2016_original_sequence_grain.json"
    out.write_text(json.dumps(report,indent=2,ensure_ascii=False))
    print("STAGE13_SOURCE_BEES_AND_SEQUENCES "+json.dumps(report,ensure_ascii=False),flush=True)
    return report

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser();p.add_argument("--out",default="stage13_original")
    run(p.parse_args().out)
