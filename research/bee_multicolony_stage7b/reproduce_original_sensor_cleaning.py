"""Reconstruct official R source sensor clustering from original 2026 Dataverse CSV.

Match author's R original procedure *before* any new ecological inference:
distinct complete source rows, discard NA, sort (experiment, flowerID,
timestamp), cluster if current start - previous raw record end <=2 s,
merge end to max, retain first source categorical data, 0<probing<250s.

Always preserve colony as experimental replicate, NEVER as tagged bee ID.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,re
from collections import Counter,defaultdict
from datetime import datetime,timedelta
from pathlib import Path

from source_semantics import read_source_records,source_semantics,NA

ORIGINAL_MD5="3a3578d61d7633635615d43829df3f3c"
AUTHOR_EXPECTED_CLEANED_EVENTS=54362
AUTHOR_EXPECTED_DUPLICATES=262
AUTHOR_EXPECTED_COMPLETE_ROWS=64947


def build_original_clustered_events(raw_rows):
    header=list(raw_rows[0])
    observed=set()
    deduped=[]
    dups=0
    for ix,row in enumerate(raw_rows):
        original_key=tuple(row[k] for k in header)
        if original_key in observed:
            dups+=1
            continue
        observed.add(original_key)
        if any((str(row[k]).strip() in NA) for k in header):
            continue
        try:
            flowerid=int(re.search(r"\d+",row["Flower"]).group())
            if flowerid<=0:raise ValueError("bad flowerID")
            date=datetime.strptime(str(row["date"]),"%Y%m%d").date()
            t=datetime.strptime(str(row["hour"]),"%H:%M:%S").time()
            stamp=datetime.combine(date,t)
            seconds=float(row["prob"])
            if seconds<0:raise ValueError("negative source probing")
        except Exception as e:
            raise ValueError(f"NO_GO_INVALID_COMPLETE_NATIVE_SOURCE_ROW_{ix}") from e
        enriched=dict(row)
        enriched["_original_index"]=ix
        enriched["_flower_id"]=flowerid
        enriched["_start"]=stamp
        enriched["_end"]=stamp+timedelta(seconds=seconds)
        deduped.append(enriched)
    # The original author's grouping does not contain colony explicitly;
    # audit if the same original experiment/flowerID crosses colonies.
    flowergroup_colonies=defaultdict(set)
    for row in deduped:
        flowergroup_colonies[(row["experiment"],row["_flower_id"])].add(row["colony"])
    ambiguous={f"{k[0]}_{k[1]}":len(v) for k,v in flowergroup_colonies.items() if len(v)>1}
    grouped=defaultdict(list)
    for row in deduped:
        key=(row["experiment"],row["_flower_id"])
        grouped[key].append(row)
    new=[]
    source_clusters=0
    before_prob_filter=0
    mixed_colony=0
    mixed_trt=0
    max_cluster_rows=0
    for key,values in grouped.items():
        ordered=sorted(values,key=lambda r:(r["_start"],r["_original_index"]))
        batches=[]
        current=[]
        # EXACT previous source row End, *not* current maximum cluster end.
        prev_end=None
        for row in ordered:
            gap=(row["_start"]-prev_end).total_seconds() if prev_end is not None else None
            if gap is None or gap>2:
                if current:batches.append(current)
                current=[row]
            else:
                current.append(row)
            prev_end=row["_end"]
        if current:batches.append(current)
        for cluster in batches:
            before_prob_filter+=1
            first=cluster[0]
            start=first["_start"]
            end=max(x["_end"] for x in cluster)
            probing=(end-start).total_seconds()
            if len({x["colony"] for x in cluster})>1:mixed_colony+=1
            if len({x["trt"] for x in cluster})>1:mixed_trt+=1
            max_cluster_rows=max(max_cluster_rows,len(cluster))
            if not (0<probing<250):
                continue
            new.append({
                "experiment":str(first["experiment"]),
                "colony":str(first["colony"]),
                "disease":str(first["disease"]),
                "cage":str(first["cage"]),
                "flower_id":int(first["_flower_id"]),
                "flower_source":str(first["Flower"]),
                "nectar_source":str(first["trt"]),
                "nectar":"quercetin" if first["trt"]=="D1" else
                         "control" if first["trt"]=="CONTROL" else
                         "__UNKNOWN_NECTAR__",
                "color":str(first["color"]),
                "day":start.date().isoformat(),
                "start_iso_local":start.isoformat(),
                "timestamp_local":start,
                "end_iso_local":end.isoformat(),
                "probing_seconds":probing,
                "original_sensor_rows_collapsed":len(cluster),
                "raw_source_first_index":first["_original_index"]
            })
    new.sort(key=lambda x:(x["timestamp_local"],x["raw_source_first_index"]))
    counts=Counter(x["colony"] for x in new)
    source_by_day=Counter((x["colony"],x["day"]) for x in new)
    canonical={
        "original_sensor_rows":len(raw_rows),
        "source_exact_duplicate_rows":dups,
        "after_original_R_distinct_and_drop_na":len(deduped),
        "original_R_expected_duplicates":AUTHOR_EXPECTED_DUPLICATES,
        "original_R_expected_complete_rows":AUTHOR_EXPECTED_COMPLETE_ROWS,
        "source_experiment_flower_groups":len(grouped),
        "experiment_flower_group_cross_colony_count":len(ambiguous),
        "experiment_flower_groups_cross_colony":ambiguous,
        "source_2second_clusters_before_probing_bounds":before_prob_filter,
        "source_2second_clusters_after_strict_0ltprob_lt250":len(new),
        "original_R_expected_processed_visits":AUTHOR_EXPECTED_CLEANED_EVENTS,
        "source_over_250_or_nonpositive_cluster_count":before_prob_filter-len(new),
        "multiple_colony_in_merged_cluster_count":mixed_colony,
        "multiple_reward_in_merged_cluster_count":mixed_trt,
        "max_source_event_rows_per_2sec_cluster":max_cluster_rows,
        "postcluster_colony_count":len(counts),
        "postcluster_colony_visit_counts":dict(sorted(counts.items())),
        "postcluster_colony_day_cells":len(source_by_day),
        "postcluster_colony_day_visit_counts":{
            f"{k[0]}_{k[1]}":int(v) for k,v in sorted(source_by_day.items())},
        "postcluster_unrecognized_nectar_count":sum(
            x["nectar"]=="__UNKNOWN_NECTAR__" for x in new),
        "requires_explicit_individual_animal_identifier_for_route_replication":True
    }
    return new,canonical

def run(root):
    path=root/"data_selfmed.csv"
    raw=path.read_bytes()
    if hashlib.md5(raw).hexdigest()!=ORIGINAL_MD5:
        raise ValueError("NO_GO_RDR_ORIGINAL_SOURCE_CSV_HASH_CHANGED")
    original_rows=read_source_records(raw)
    cleaned,receipt=build_original_clustered_events(original_rows)
    status=(
        "MATCHES_PUBLISHED_AUTHOR_COUNTS" if
        receipt["source_exact_duplicate_rows"]==AUTHOR_EXPECTED_DUPLICATES and
        receipt["after_original_R_distinct_and_drop_na"]==AUTHOR_EXPECTED_COMPLETE_ROWS and
        len(cleaned)==AUTHOR_EXPECTED_CLEANED_EVENTS and
        receipt["multiple_colony_in_merged_cluster_count"]==0 and
        receipt["multiple_reward_in_merged_cluster_count"]==0 else
        "NO_GO_PUBLISHED_RAW_SENSOR_PROCESSING_DISAGREES"
    )
    report={"status":status,"source_original_csv_md5":ORIGINAL_MD5,
            "original_source_cleaning_receipt":receipt,
            "not_individual_bee_tracks":True}
    root.mkdir(exist_ok=True,parents=True)
    (root/"rdr_reconstructed_published_sensor_visits.json").write_text(
        json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False))
    print("BEE_STAGE7B_PUBLISHED_CLUSTER_RECONCILIATION "+
          json.dumps(report,ensure_ascii=False),flush=True)
    print("BEE_STAGE7B_CLUSTER_RECONCILIATION_COMPLETE",flush=True)
    if status!="MATCHES_PUBLISHED_AUTHOR_COUNTS":
        raise ValueError(status)
    return cleaned,report

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--out",default="rdr_multicolony_source")
    a=p.parse_args()
    run(Path(a.out))
