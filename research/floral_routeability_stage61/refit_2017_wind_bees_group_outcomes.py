"""Stage61 independent summary of 72 originally published Lawson 2017 wind bees.

Original source DOI 10.1098/rsos.170996, source internal OA XLSX
rsos170996supp2.xlsx SHA256 b3802f... (Stage61 exact source audit).
Source '2. Wind Simulation Data' original 73 rows = 1 header + 72
bees, four original groups of 18. Counts are original behavioural
endpoints (visits to learning criterion, correct landing choices,
rewarding flower landings), NOT independent flight approaches/plant pollen.

This is a REANALYSIS of existing 2017 experiment, not a new ecological
effect, no causal 2x2x2 factorial, no measured first cue or downstream
adaptive cue selection, and no pollen/seed fitness. Raw original rows
remain ephemeral; only grouped aggregates are uploaded.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,statistics,zipfile
from collections import Counter,defaultdict
from pathlib import Path
import xml.etree.ElementTree as ET
from probe_2017_wind_visual_odor_original_data import get_source

PIN="b3802f57516c0ebac025f363dd2943796e749ef82b9b32e15fd0deb78c98432c"
FILE="rsos170996supp2.xlsx"
SHEET="xl/worksheets/sheet2.xml"
N="{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
EXPECTED_HEADER=(
 "condition","group","flower visits taken to reach learning criteria",
 "number of correct choices made after landing","lands on rewarding flowers",
 "colony","scent of rewarding flowers")
GROUPS={"A":"calm_odour_only",
        "B":"wind_odour_only",
        "C":"wind_odour_plus_visual",
        "D":"wind_visual_only"}
ENDPOINTS=("visits_to_learning_criterion",
           "correct_choices_after_landing_count",
           "rewarding_flower_landings_count")

def original_sheet_bytes():
    with zipfile.ZipFile(io.BytesIO(get_source())) as z:
        xs=[x for x in z.infolist() if not x.is_dir()
            and Path(x.filename).name==FILE]
        if len(xs)!=1:raise ValueError("NO_GO_ORIGINAL_LAWSON_WIND_SOURCE_FILE_ID")
        data=z.read(xs[0])
    if hashlib.sha256(data).hexdigest()!=PIN:
        raise ValueError("NO_GO_ORIGINAL_LAWSON_WIND_XLSX_PIN")
    return data

def extract_rows(xlsx):
    with zipfile.ZipFile(io.BytesIO(xlsx)) as z:
        if SHEET not in z.namelist():
            raise ValueError("NO_GO_LAWSON_ORIGINAL_WIND_WORKSHEET_MISSING")
        strings=[]
        if "xl/sharedStrings.xml" in z.namelist():
            root=ET.fromstring(z.read("xl/sharedStrings.xml"))
            strings=["".join(t.text or "" for t in item.iter(N+"t"))
                     for item in root.iter(N+"si")]
        doc=ET.fromstring(z.read(SHEET))
    rows=[]
    for r in doc.iter(N+"row"):
        vals=[""]*7
        for cell in r.findall(N+"c"):
            idx=ord(cell.attrib.get("r","A")[0])-65
            if not 0<=idx<=6:continue
            v=cell.find(N+"v")
            if cell.attrib.get("t")=="s" and v is not None:
                n=int(v.text)
                if n<0 or n>=len(strings):
                    raise ValueError("NO_GO_2017_WIND_SHARED_SOURCE_STRING")
                vals[idx]=strings[n]
            elif cell.attrib.get("t")=="inlineStr":
                vals[idx]="".join(t.text or "" for t in cell.iter(N+"t"))
            elif v is not None:vals[idx]=v.text or ""
        rows.append(vals)
    if not rows or tuple(rows[0])!=EXPECTED_HEADER:
        raise ValueError("NO_GO_PUBLISHED_SOURCE_WIND_BEHAVIOR_HEADERS")
    return rows[1:]

def clean_original(trial_rows):
    if len(trial_rows)!=72:
        raise ValueError("NO_GO_PUBLISHED_2017_72_BEES_ORIGINAL_WIND_DATA")
    out=[]
    for row in trial_rows:
        group=row[1].strip()
        if group not in GROUPS or not row[5]:
            raise ValueError("NO_GO_PUBLISHED_2017_GROUP_OR_COLONY_UNKNOWN")
        payload={"group":group,"condition_text_as_published":row[0],
                 "colony_as_published":row[5],
                 "reward_scent_as_published":row[6]}
        for col,name in zip((2,3,4),ENDPOINTS):
            text=row[col].strip()
            if not text or text.upper() in ("NA","N/A"):
                payload[name]=None
                continue
            try:
                value=float(text)
            except ValueError as ex:
                raise ValueError("NO_GO_2017_WIND_COUNT_NOT_NUMERIC_"+name) from ex
            if not value.is_integer() or value<0:
                raise ValueError("NO_GO_2017_WIND_BEHAVIORAL_COUNT_INVALID_"+name)
            payload[name]=int(value)
        out.append(payload)
    if Counter(x["group"] for x in out)!=Counter({k:18 for k in GROUPS}):
        raise ValueError("NO_GO_2017_WIND_ARM_N18_NOT_RECONCILED")
    for g in GROUPS:
        if len({x["condition_text_as_published"] for x in out if x["group"]==g})!=1:
            raise ValueError("NO_GO_2017_TREATMENT_MIXED_WITHIN_ARM")
    return out

def describe(original):
    groups={}
    for key,description in GROUPS.items():
        sample=[x for x in original if x["group"]==key]
        metrics={}
        for var in ENDPOINTS:
            data=[x[var] for x in sample if x[var] is not None]
            metrics[var]={"n_observed":len(data),
                          "mean":statistics.mean(data) if data else None,
                          "median":statistics.median(data) if data else None,
                          "minimum":min(data) if data else None,
                          "maximum":max(data) if data else None}
        groups[key]={
          "group_description":description,
          "n_bees":len(sample),
          "source_colony_counts":dict(sorted(Counter(x["colony_as_published"] for x in sample).items())),
          "source_reward_odor_labels":dict(sorted(Counter(x["reward_scent_as_published"] for x in sample).items())),
          "source_authored_endpoint_counts":metrics,
        }
    differences={}
    for outcome in ENDPOINTS:
        a,b,c,d=(groups[k]["source_authored_endpoint_counts"][outcome]["mean"]
                 for k in ("A","B","C","D"))
        differences[outcome]={
          "B_minus_A_wind_effect_odour_only":b-a if a is not None and b is not None else None,
          "C_minus_B_visual_added_with_wind_odour":c-b if b is not None and c is not None else None,
          "C_minus_D_odour_added_with_wind_visual":c-d if c is not None and d is not None else None,
          "not_wind_by_visual_or_odor_factorial_interaction":True
        }
    return {
      "status":"REPRODUCED_ORIGINAL_LAWSON_2017_72_BEE_WIND_EXPERIMENT_GROUP_DESCRIPTIVES",
      "source_paper_DOI":"10.1098/rsos.170996",
      "original_source_XLSX_SHA256":PIN,
      "source_authored_wind_bees":len(original),
      "source_wind_treatment_groups":groups,
      "published_reanalysis_original_four_arm_observed_edge_differences":differences,
      "no_p_value_or_colony_independent_inference":True,
      "no_wind_by_odor_by_visual_full_factorial_effect":True,
      "no_original_per_trial_cue_order_or_first_cue_policy":True,
      "no_measured_animal_pollen_or_plant_fitness":True,
      "no_claim_of_novel_visual_backup_or_adaptive_route_observation":True,
    }

def main():
    original=clean_original(extract_rows(original_sheet_bytes()))
    report=describe(original)
    out=Path("stage61_2017_source_72_wind_backup_reanalysis")
    out.mkdir(exist_ok=True)
    (out/"original_Lawson_2017_72_bees_four_arm_behavior_means.json").write_text(
       json.dumps(report,indent=2,sort_keys=True,ensure_ascii=False)+"\n",
       encoding="utf8")
    print("STAGE61_REAL_ORIGINAL_2017_WIND_BACKUP_72_BEE_GROUPS",
          json.dumps(report,sort_keys=True,ensure_ascii=False))
    print("NO_NEW_MULTISENSORY_WIND_CUE_ORDER_OR_POLLEN_IDENTIFIED")
if __name__=="__main__":
    main()
