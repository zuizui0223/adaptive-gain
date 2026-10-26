"""Stage 3e: source-defined floral morphology classes and overlap audit.

Read original PoMS FIT source members, preserve native flower_structure labels.
Profiles are screening metadata, not fitted effects or selected discoveries.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import zipfile
from pathlib import Path
import numpy as np
import pandas as pd
from fit_associations import (
    SOURCE_DATA_SHA256, prepare, read_source, WIND
)
from stage3_full_profile import TABLES

OTHER="Other - please describe below"
GUILDS=("bumblebees","other_flies")

def profile_structure(source,surface):
    location="location_code" if surface=="one_km" else "x1km_square"
    if not {"flower_structure","target_flower_corrected",location,*GUILDS} <= set(source):
        raise ValueError("source morphology fields absent")
    df,flow=prepare(source,surface)
    native={str(k):int(v) for k,v in
            df["flower_structure"].value_counts(dropna=False).items()}
    d=df.copy()
    raw=d["flower_structure"].astype("string").str.strip().str.lower()
    d["structure_normalized"]=raw.replace({"":pd.NA})
    d["pair_total"]=d["bumblebees"]+d["other_flies"]
    d["pair_positive"]=d["pair_total"]>0
    named=d[~d["target_flower_corrected"].eq(OTHER)].copy()
    target_groups=[]
    for (target,structure), g in d.groupby(
        ["target_flower_corrected","structure_normalized"],
        dropna=False,observed=True):
        target_groups.append({
            "target":str(target),"structure":str(structure),
            "surveys":len(g),"pair_positive_surveys":int(g["pair_positive"].sum()),
            "bee_visits":int(g["bumblebees"].sum()),
            "fly_visits":int(g["other_flies"].sum())})
    matrix=[]
    for label,g in d.groupby("structure_normalized",dropna=False,observed=True):
        subset={"source_structure":str(label),
                "all_surveys":len(g),
                "named_target_surveys":int(~g["target_flower_corrected"].eq(OTHER).sum()) if False else int((g["target_flower_corrected"]!=OTHER).sum()),
                "distinct_corrected_targets":int(g["target_flower_corrected"].nunique()),
                "pair_positive_surveys":int(g["pair_positive"].sum()),
                "pair_positive_named_target_surveys":int((g["pair_positive"] & g["target_flower_corrected"].ne(OTHER)).sum()),
                "bee_visits":int(g["bumblebees"].sum()),
                "fly_visits":int(g["other_flies"].sum()),
                "wind":{}}
        for w in WIND:
            t=g[g["wind_speed"]==w]
            subset["wind"][w]={
                "surveys":len(t),
                "pair_positive_surveys":int(t["pair_positive"].sum()),
                "named_pair_positive_surveys":int((t["pair_positive"] & t["target_flower_corrected"].ne(OTHER)).sum()),
                "unique_sites":int(t[location].nunique())}
        pairs=g.loc[g["pair_positive"] & g["target_flower_corrected"].ne(OTHER) &
                    g["wind_speed"].isin([WIND[0],WIND[2]])]
        common=(pairs.groupby([location,"wind_speed"],observed=True)
                .size().unstack(fill_value=0))
        subset["sites_with_both_calm_strong_pair_positive_named"]=int(
            ((common.get(WIND[0],pd.Series(0,index=common.index))>0) &
             (common.get(WIND[2],pd.Series(0,index=common.index))>0)).sum())
        matrix.append(subset)
    structure_per_target=named.groupby("target_flower_corrected")["structure_normalized"].nunique(dropna=True)
    return {
        "surface":surface, "input_rows":len(source),
        "eligible_surveys":len(df),"eligibility":flow,
        "native_structure_values":native,
        "normalized_structure_levels":matrix,
        "corrected_target_by_structure":target_groups,
        "named_target_count":int(named["target_flower_corrected"].nunique()),
        "named_target_structure_unique_fraction":float((structure_per_target<=1).mean()),
        "named_targets_with_multiple_structures":[str(x) for x in structure_per_target[structure_per_target>1].index],
        "named_target_pair_positive_surveys":int(named["pair_positive"].sum()),
        "other_target_surveys":int(d["target_flower_corrected"].eq(OTHER).sum()),
        "normalization_policy":"lowercase and trim source strings; no free-form morphology guessing"
    }

def run(source_zip:Path,out:Path):
    report={
        "phase":"data_quality_before_stage3e_interaction_fit",
        "claim_boundary":"survey selected target morphology is not a free resource choice or direct wind mechanism",
        "surfaces":{},"member_sha256":{}}
    with zipfile.ZipFile(source_zip) as archive:
        for surface,filename in TABLES.items():
            original=archive.read(filename)
            digest=hashlib.sha256(original).hexdigest()
            if digest!=SOURCE_DATA_SHA256[surface]:
                raise ValueError(f"{surface} original CSV hash mismatch")
            df,enc=read_source(original)
            report["surfaces"][surface]=profile_structure(df,surface)
            report["surfaces"][surface]["encoding"]=enc
            report["member_sha256"][surface]=digest
    out.parent.mkdir(exist_ok=True,parents=True)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False))
    for surface,r in report["surfaces"].items():
        print("POMS_STRUCTURE_PROFILE "+json.dumps(r,ensure_ascii=False,allow_nan=False),flush=True)
    print("POMS_STRUCTURE_PROFILE_COMPLETE",flush=True)
    return report

def main(argv=None):
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",default="stage3_poms_audit")
    args=ap.parse_args(argv)
    root=Path(args.out)
    run(root/"poms_fit_2017_2023_source.zip",root/"floral_structure_audit.json")

if __name__=="__main__":
    main()
