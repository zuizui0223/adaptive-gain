"""Source-only provider-landmark semantics audit: original XYZ7 need not be time-aligned.

Distinct from outcome computation. Reconstruct original author `bsxfun` usage
and document whether point7 is a static per-trial flower location.
"""
from __future__ import annotations
import hashlib
import io
import json
import zipfile
from collections import Counter
from pathlib import Path
import numpy as np
from source_audit import FILENAME, EXPECTED_MD5
from inspect_native_schema import PATTERN

def audit(folder:Path):
    original=(folder/FILENAME).read_bytes()
    if hashlib.md5(original).hexdigest()!=EXPECTED_MD5:
        raise ValueError("NO_GO_SOURCE_PROVIDER_IDENTITY_CHANGED")
    per=[]
    with zipfile.ZipFile(io.BytesIO(original)) as z:
        script=z.read("tracking and kinematic code/analyzeTrackingData.m").decode(errors="replace")
        lines=script.splitlines()
        hits=[(i,line) for i,line in enumerate(lines) if
              "RawData(:,19)" in line or "EditedData" in line or "bsxfun" in line]
        evidence=[{"line_number":i+1,
                   "original_author_context":" | ".join(lines[max(0,i-2):min(len(lines),i+3)])[:600]}
                  for i,_ in hits[:12]]
        paths=[n for n in z.namelist() if n.startswith("kinematic data/") and
               n.endswith("xyzpts.csv") and not n.split("/")[-1].startswith("._")]
        for path in sorted(paths):
            name=path.rsplit("/",1)[1]
            m=PATTERN.fullmatch(name)
            if not m:raise ValueError("NO_GO_NONSOURCE_FILE")
            raw=z.read(path).decode("utf-8-sig").replace("\r\n","\n").replace("\r","\n")
            d=np.genfromtxt(io.StringIO(raw),skip_header=1,delimiter=",",dtype=float)
            if d.ndim!=2 or d.shape[1]!=21:
                raise ValueError("NO_GO_SOURCES_NOT_21_COLUMNS "+name)
            vbee=np.isfinite(d[:,:9]).all(axis=1)
            vflower=np.isfinite(d[:,18:21]).all(axis=1)
            native_flower=d[vflower,18:21]
            distinct=np.unique(native_flower,axis=0)
            per.append({"source_filename":name,
                        "original_bee":int(m.group("bee")),
                        "wind":int(m.group("w")),
                        "stiff":int(m.group("s")),"orientation":int(m.group("p")),
                        "frames":len(d),
                        "fully_tracked_bee_frames":int(vbee.sum()),
                        "native_flower_frames":int(vflower.sum()),
                        "concurrent_full_bee_and_flower":int(np.sum(vbee & vflower)),
                        "distinct_native_flower_positions":len(distinct),
                        "flower_position_repeated_identically":len(distinct)==1 and len(native_flower)>0})
    groups=Counter((r["native_flower_frames"],r["distinct_native_flower_positions"]) for r in per)
    stats={"status":"2016_ORIGINAL_POINT7_SCHEMA_DIAGNOSED",
           "source_md5":EXPECTED_MD5,"source_csv_trial_count":len(per),
           "trial_counts_by_flower_obs_and_unique":{
               "%s_native_obs_%s_positions"%k:v for k,v in sorted(groups.items())},
           "source_bee_frame_counts_range":[min(r["fully_tracked_bee_frames"] for r in per),max(r["fully_tracked_bee_frames"] for r in per)],
           "trials_with_any_valid_bee_frame":sum(r["fully_tracked_bee_frames"]>0 for r in per),
           "trials_with_any_native_flower_landmark":sum(r["native_flower_frames"]>0 for r in per),
           "trials_with_at_least_one_concurrent_bee_flower_frame":sum(r["concurrent_full_bee_and_flower"]>0 for r in per),
           "trials_with_single_distinct_native_flower_landmark":sum(r["distinct_native_flower_positions"]==1 for r in per),
           "native_author_code_pt7_usage":evidence,
           "per_trial_source_qa":per,
           "not_a_predicted_landing_or_wind_effect":True}
    out=folder/"stage10_original_point7_qa.json"
    out.write_text(json.dumps(stats,indent=2,ensure_ascii=False,allow_nan=False))
    print("STAGE10_ORIGINAL_LANDMARK_DIAGNOSIS "+
          json.dumps({k:v for k,v in stats.items() if k!="per_trial_source_qa"},ensure_ascii=False),flush=True)
    print("STAGE10_POINT7_NATIVE_QA_COMPLETE",flush=True)
    return stats

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser();p.add_argument("--out",default="bee_stage10_original")
    audit(Path(p.parse_args().out))
