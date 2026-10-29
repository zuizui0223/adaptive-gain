"""Stage10 original source *schema* details; no original outcome estimators.

Use only source MD5-gated archive from source_audit.py. Do NOT treat
Mac Finder metadata (__MACOSX) as real CSV events.
"""
from __future__ import annotations
from collections import Counter
import csv
import io
import json
import re
import zipfile
from pathlib import Path
from source_audit import FILENAME,EXPECTED_MD5
import hashlib

PATTERN=re.compile(r"^B(?P<bee>\d+)_BC(?P<tag>\d+)_F(?P<flight>\d+)_S(?P<s>\d+)_P(?P<p>\d+)_T(?P<trial>\d+)_W(?P<w>\d+)_C(?P<c>\d+)H(?P<h>\d+)S(?P<ss>\d+)xyzpts\.csv$")

def schema(root):
    file=root/FILENAME
    if not file.is_file():
        raise ValueError("NO_GO_ORIGINAL_SOURCE_ZIP_MISSING")
    if hashlib.md5(file.read_bytes()).hexdigest()!=EXPECTED_MD5:
        raise ValueError("NO_GO_ZENODO_ORIGINAL_MD5_CHANGED")
    with zipfile.ZipFile(file) as z:
        readme=z.read("README.txt").decode("utf-8-sig",errors="replace")
        script=z.read("tracking and kinematic code/analyzeTrackingData.m").decode("utf-8-sig",errors="replace")
        paths=[x for x in z.namelist() if x.startswith("kinematic data/") and
               x.endswith("xyzpts.csv") and "/._" not in x]
        if not paths:raise ValueError("NO_GO_NO_GENUINE_XYZPTS_SOURCE_FILES")
        groups=Counter()
        bees={}
        tags={}
        ids=[]
        grids=Counter()
        bad=[]
        rowcounts=[]
        colcounts=Counter()
        for path in paths:
            name=path.rsplit("/",1)[1]
            m=PATTERN.fullmatch(name)
            if not m:
                bad.append(path)
                continue
            d={k:int(v) for k,v in m.groupdict().items()}
            ids.append(d)
            groups[(d["s"],d["p"],d["w"])]+=1
            bees.setdefault(d["bee"],set()).add(d["tag"])
            tags.setdefault(d["tag"],set()).add(d["bee"])
            # Audit number of original source tracked frames and 3D columns.
            with z.open(path) as f:
                text=io.TextIOWrapper(f,encoding="utf-8-sig",newline="")
                reader=csv.reader(text)
                header=next(reader)
                rows=sum(1 for _ in reader)
            grids[(d["s"],d["p"],d["w"],d["bee"])]+=1
            colcounts[tuple(header)]+=1
            rowcounts.append(rows)
        if bad:
            raise ValueError("NO_GO_UNEXPLAINED_AUTHOR_ORIGINAL_CSV_NAMES "+str(bad[:3]))
        if len(colcounts)!=1:
            raise ValueError("NO_GO_ORIGINAL_CSV_TRACKING_COLUMN_SCHEMA_DIFFERS")
        header=next(iter(colcounts))
        if len(header)!=21 or header[:3]!=("pt1_X","pt1_Y","pt1_Z"):
            raise ValueError("NO_GO_NOT_EXPECTED_TRACKER_POINTS")
        receipt={
            "status":"ZENODO_ORIGINAL_2016_NATIVE_SCHEMA_RECONCILED",
            "published_original_readme":readme,
            "original_analysis_script_top":script[:3000],
            "source_original_csv_count":len(paths),
            "original_3d_coordinate_columns":len(header),
            "source_frame_counts_min_max":[min(rowcounts),max(rowcounts)],
            "distinct_original_B_identifiers":len(bees),
            "distinct_original_BC_tag_ids":len(tags),
            "B_to_BC_tag_mapping_one_to_one":all(len(v)==1 for v in bees.values()) and all(len(v)==1 for v in tags.values()),
            "original_condition_file_counts":{"S%s_P%s_W%s"%k:v for k,v in sorted(groups.items())},
            "original_source_B_IDs":sorted(bees),
            "original_xyz_header":header,
            "source_sampling_frames_not_independent_animals":True,
            "source_csv_trials_may_include_exclusions_or_immobilized_controls":True,
            "no_empirical_effect_estimated":True,
        }
        return receipt

def run(root):
    out=root/"zenodo60234_native_schema.json"
    try:
        r=schema(root)
    except Exception as e:
        r={"status":"NO_GO_NATIVE_2016_SCHEMA","error":str(e)}
        out.write_text(json.dumps(r,indent=2))
        print("STAGE10_NATIVE_SCHEMA_NO_GO "+json.dumps(r),flush=True)
        raise
    out.write_text(json.dumps(r,indent=2,ensure_ascii=False))
    print("STAGE10_SOURCE_NATIVE_SCHEMA "+json.dumps(r,ensure_ascii=False),flush=True)
    print("STAGE10_NATIVE_METADATA_COMPLETE",flush=True)
    return r

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--out",default="bee_stage10_original")
    run(Path(p.parse_args().out))
