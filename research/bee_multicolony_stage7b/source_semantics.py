"""Read actual 2026 KU Leuven robotic-flower source semantics before modelling.

No tag ID exists. Every row is a *colony-level device sensor event* and
cannot be assigned to an individual bee. Original experiment has 18 colonies,
not 65k independent animal trajectories.
"""
from __future__ import annotations
from collections import Counter,defaultdict
import argparse,csv,hashlib,io,json,re
from pathlib import Path
from datetime import datetime
import math

KNOWN_COLUMNS=["experiment","name","hour","prob","Flower","date","trt",
               "cage","group","color","colony","disease"]
NA={"","#N/A","NA","N/A","nan","null","None"}

def read_source_records(raw:bytes):
    decoded=raw.decode("utf-8-sig",errors="strict")
    rows=list(csv.DictReader(io.StringIO(decoded)))
    if not rows:raise ValueError("NO_GO_RDR_NO_ORIGINAL_SENSOR_EVENTS")
    if list(rows[0])!=KNOWN_COLUMNS:
        raise ValueError("NO_GO_RDR_NATIVE_CSV_HEADER_DRIFT")
    if any(None in row for row in rows):raise ValueError("NO_GO_RDR_RAGGED_SENSOR_ROW")
    return rows

def source_semantics(rows,r_code:str):
    categorical=["experiment","name","trt","cage","group","color","colony","disease"]
    counts={c:Counter(row[c].strip() for row in rows) for c in categorical}
    numeric=Counter()
    time_fail=Counter()
    valid=[]
    invalid=[]
    for ix,row in enumerate(rows):
        raw={k:(v or "").strip() for k,v in row.items()}
        if any(raw[k] in NA for k in ("date","hour","colony","Flower","prob","group","color")):
            invalid.append({"reason":"missing source sensor fields","source_row_index":ix})
            continue
        try:
            source_day=datetime.strptime(raw["date"],"%Y%m%d").date()
            clock=datetime.strptime(raw["hour"],"%H:%M:%S").time()
            sec=clock.hour*3600+clock.minute*60+clock.second
            duration=float(raw["prob"].replace(",","."))
            if not math.isfinite(duration) or duration<0:
                raise ValueError("negative/nonfinite probing seconds")
        except (ValueError,TypeError):
            invalid.append({"reason":"invalid date/time/probing type","source_row_index":ix})
            continue
        if raw["Flower"].lower() in ("device","test","dummy"):
            invalid.append({"reason":"non-flower system sensor row","source_row_index":ix})
            continue
        new={"date":str(source_day),"seconds":sec,
             "colony":raw["colony"],"Flower":raw["Flower"],
             "group":raw["group"],"color":raw["color"],
             "trt":raw["trt"],"disease":raw["disease"],
             "experiment":raw["experiment"],"cage":raw["cage"],
             "probing_seconds":duration,"source_index":ix}
        valid.append(new)
    groups=defaultdict(list)
    colony_conflicts={}
    for r in valid:
        groups[r["colony"]].append(r)
    for colony,values in groups.items():
        source_groups={r["disease"] for r in values}
        source_treats={r["trt"] for r in values}
        colony_conflicts[colony]={
            "source_disease_classes":sorted(source_groups),
            "trt_classes":sorted(source_treats),
            "days":len({r["date"] for r in values}),
            "original_raw_sensor_events":len(values),
            "unique_device_ids":len({r["Flower"] for r in values}),
            "distinct_cages":sorted({r["cage"] for r in values})}
    date_counts=Counter(r["date"] for r in valid)
    devices=Counter((r["colony"],r["date"],r["Flower"]) for r in valid)
    # Source code search is a qualitative code-method audit only, not model fitting.
    expressions=re.compile(
        "duplicat|250|difftime|prob|filter|arrange|distinct|group_by|visit|drop_na|trt|querc|second",
        re.I)
    matches=[
        {"source_line":i+1,"excerpt":line.strip()[:190]}
        for i,line in enumerate(r_code.splitlines())
        if expressions.search(line)
    ][:110]
    receipt={
        "source_original_rows":len(rows),
        "source_record_valid_for_timestamp_and_id":len(valid),
        "invalid_source_row_count":len(invalid),
        "invalid_reason_histogram":dict(Counter(x["reason"] for x in invalid)),
        "original_field_levels":{
            c:{"nunique":len(v),
               "values":dict(v.most_common(25)) if len(v)<=25 else
                        {k:n for k,n in v.most_common(8)}}
            for c,v in counts.items()},
        "valid_colonies":len(groups),
        "colony_source_group_date_device_profile":colony_conflicts,
        "distinct_source_days":len(date_counts),
        "source_day_min":min(date_counts) if date_counts else None,
        "source_day_max":max(date_counts) if date_counts else None,
        "source_event_day_counts":dict(sorted(date_counts.items())),
        "colony_date_device_streams":len(devices),
        "source_prob_seconds_min":min((r["probing_seconds"] for r in valid),default=None),
        "source_prob_seconds_max":max((r["probing_seconds"] for r in valid),default=None),
        "source_prob_seconds_over250":sum(r["probing_seconds"]>250 for r in valid),
        "source_R_analysis_selected_lines":matches,
        "source_data_firmly_colony_level_no_individual_tags":True,
        "colony_id_not_an_individual_bee":True
    }
    return valid,receipt

def run(folder):
    source_file=folder/"data_selfmed.csv"
    rfile=folder/"Data_analysis_selfmed.R"
    raw=source_file.read_bytes()
    if hashlib.md5(raw).hexdigest()!="3a3578d61d7633635615d43829df3f3c":
        raise ValueError("NO_GO_ORIGINAL_PUBLIC_SOURCE_DIGEST_CHANGED")
    records=read_source_records(raw)
    valid,audit=source_semantics(records,rfile.read_text(encoding="utf-8-sig",errors="strict"))
    out=folder/"rdr_multicolony_semantic_quality.json"
    out.write_text(json.dumps(audit,indent=2,ensure_ascii=False,allow_nan=False))
    print("BEE_STAGE7B_SOURCE_SEMANTICS "+json.dumps(audit,ensure_ascii=False),flush=True)
    # Focused source-author preprocessing excerpt, for internal source
    # methods verification before implementing any independent estimator.
    raw_script=rfile.read_text(encoding="utf-8-sig",errors="strict")
    excerpts=[{"line":i+1,"source":v.strip()} for i,v in enumerate(raw_script.splitlines())
              if (63<=i+1<=96 or 150<=i+1<=212)]
    print("BEE_STAGE7B_ORIGINAL_R_FILTERS "+
          json.dumps(excerpts,ensure_ascii=False),flush=True)
    print("BEE_STAGE7B_SEMANTICS_COMPLETE",flush=True)
    return valid,audit

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--out",default="rdr_multicolony_source")
    args=p.parse_args()
    run(Path(args.out))
