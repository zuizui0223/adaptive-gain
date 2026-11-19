#!/usr/bin/env python3
"""Stage91: pre-outcome, COMMON mainland-only regional block split.

Requires independently audited geographic source to classify every TDWG3
regional polygon as mainland/island/mixed. Never infer mainland from a region
name or from observed flower/pollinator traits. Mixed-island polygons excluded.
No ecological analysis until a real 367-region geography registry is supplied.
"""
from __future__ import annotations
import argparse,csv,hashlib,json
from collections import Counter
from pathlib import Path

SALT="floral_stage91_three_cue_geographic_split_20261119_v1"
SCOPES={"mainland","island","mixed"}

def split_regions(region_codes, audited, *, salt=SALT, holdout_mod=5):
    required={str(s).strip().upper() for s in region_codes}
    if len(required)!=len(region_codes) or not required:
        raise ValueError("duplicate or empty source region IDs")
    if holdout_mod<2:raise ValueError("holdout modulus must be >=2")
    mapping={}
    for row in audited:
        r=str(row.get("TDWG_L3") or "").strip().upper()
        scope=str(row.get("land_scope") or "").casefold().strip()
        block=str(row.get("spatial_block_id") or "").strip()
        digest=str(row.get("polygon_sha256") or "").lower().strip()
        origin=str(row.get("geometry_source") or "").strip()
        if r in mapping or not r or scope not in SCOPES or not block or not origin:
            raise ValueError("incomplete/duplicate geographic audit")
        if len(digest)!=64 or any(c not in "0123456789abcdef" for c in digest):
            raise ValueError("unverified geographic polygon SHA256")
        mapping[r]=(scope,block,digest,origin)
    if set(mapping)!=required:
        raise ValueError("geography registry must cover exactly every source TDWG3 region")
    blocks={}
    out=[]
    for r in sorted(mapping):
        scope,block,digest,origin=mapping[r]
        if scope!="mainland":continue
        if block not in blocks:
            h=hashlib.sha256(f"{salt}|{block}".encode()).hexdigest()
            blocks[block]="holdout" if int(h,16)%holdout_mod==0 else "exploration"
        out.append({"TDWG_L3":r,"shared_split":blocks[block],"spatial_block_id":block,
                    "land_scope":scope,"polygon_sha256":digest,"geometry_source":origin})
    if len(blocks)<3 or set(blocks.values())!={"holdout","exploration"}:
        raise ValueError("not enough independent geographic blocks for both arms")
    receipt={"total_source_regions_audited":len(mapping),"mainland_regions":len(out),
        "island_regions_excluded":sum(x[0]=="island" for x in mapping.values()),
        "mixed_regions_excluded":sum(x[0]=="mixed" for x in mapping.values()),
        "distinct_mainland_blocks":len(blocks),
        "block_split_counts":dict(Counter(blocks.values())),
        "fixed_preoutcome_salt":salt,
        "holdout_denominator":holdout_mod,
        "same_split_required_for_all_three_separate_responses":True,
        "spatial_separation_buffer_verified":False,
        "wind_or_cue_values_used_to_define_split":False}
    return out,receipt

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--region-source-summary",type=Path,required=True)
    p.add_argument("--audited-geometry-registry",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args()
    with a.region_source_summary.open(encoding="utf-8-sig",newline="") as f: source=list(csv.DictReader(f))
    with a.audited_geometry_registry.open(encoding="utf-8-sig",newline="") as f: geo=list(csv.DictReader(f))
    out,receipt=split_regions([r["TDWG_L3"] for r in source],geo)
    a.outdir.mkdir(parents=True,exist_ok=True)
    with (a.outdir/"stage91_shared_mainland_split.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=out[0].keys());w.writeheader();w.writerows(out)
    (a.outdir/"stage91_shared_mainland_split_receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps(receipt,sort_keys=True))

if __name__=="__main__":main()
