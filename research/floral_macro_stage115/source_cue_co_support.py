#!/usr/bin/env python3
"""Exact source-species cue availability, NOT a biological trade-off fit."""
import argparse,csv,hashlib,io,json,re,zipfile
from collections import Counter
from pathlib import Path

SOURCES={
 14313209081:("efa944763aa5971f7642f063295436119c9cafae204325922e9979f3214d1d85","combined/original_NHM_text_traits_compact.csv"),
 14534460860:("eb32786c6464a6edecd7ff0d12e61762cdb107f3082124066aadcc03292dd88e","stage93_derived/stage93_original_WFO_species_fragrance_lexical_states_NOT_VOC.csv"),
 14595854235:("95fb60fa049ed4e79673e1f1dc12aaddb97f5fadd1dc27f905d31dd25b8cfe90","stage103_original_WFO_237_flower_source_interval_envelopes_NOT_measured.csv")}
POS=re.compile(r"\b(?:spots?|spotted|striped|stripes?|streaked|blotched|mottled|maculate|nectar[ -]?guides?)\b",re.I)
NEG=re.compile(r"\b(?:unspotted|unmarked|immaculate|unstriped|plain|without\s+(?:any\s+)?(?:spots?|stripes?|markings?)|no\s+(?:spots?|markings?))\b",re.I)
NEGATED=re.compile(r"\b(?:not|no|without)\s+(?:spots?|spotted|striped|stripes?|markings?|nectar[ -]?guides?)\b",re.I)

def mark(row):
    t="; ".join(str(row.get(c) or "").strip() for c in ("flower colour","petal colour","corolla colour")).strip("; ")
    if not t:return "colour_missing"
    p=bool(POS.search(NEGATED.sub(" ",t)));n=bool(NEG.search(t) or NEGATED.search(t))
    return "ambiguous" if p and n else "positive" if p else "explicit_plain" if n else "unmentioned"

def read(root,id,key):
    sha,member=SOURCES[id]
    f=root/f"github-actions-artifact-{id}.zip"
    if hashlib.sha256(f.read_bytes()).hexdigest()!=sha:raise ValueError("source digest mismatch")
    with zipfile.ZipFile(f) as z:
        rows=list(csv.DictReader(io.StringIO(z.read(member).decode("utf-8-sig"))))
    data={row[key].strip().casefold():row for row in rows}
    if len(data)!=len(rows):raise ValueError("duplicate species key")
    return data

def run(root):
    nhm=read(root,14313209081,"taxon")
    scent=read(root,14534460860,"accepted_species")
    size=read(root,14595854235,"accepted_species")
    if len(nhm)!=59369 or len(scent)!=27899 or len(size)!=237 or not set(scent)<=set(nhm):
        raise ValueError("source cohort changed")
    table=Counter();sizes=Counter();pairs=Counter(); modes=Counter()
    for sp,s in scent.items():
        m=mark(nhm[sp]);c=s["source_flora_lexical_fragrance_state"]
        table[(c,m)]+=1
        mk=m in {"positive","explicit_plain"}
        sk=c in {"positive_candidate","explicit_negative_candidate"}
        sz=sp in size and size[sp]["status"]!="no_eligible_size_evidence"
        if sz:sizes[(c,m)]+=1
        for key,ok in {"mark_explicit":mk,"scent_explicit":sk,"WFO_size_source_supported":sz,"mark_and_scent":mk and sk,"size_and_scent":sz and sk,"size_and_mark":sz and mk,"all_three":sz and sk and mk}.items():
            if ok:pairs[key]+=1
        if mk and sk:modes[s["independent_GIFT_source_pollination_mode"]]+=1
    expected={"mark_explicit":598,"scent_explicit":525,"WFO_size_source_supported":212,"mark_and_scent":16,"size_and_scent":3,"size_and_mark":3,"all_three":0}
    actual={k:pairs[k] for k in expected}
    if actual!=expected:raise ValueError(f"source co-support drift {actual}")
    return {"source_archives":{str(k):v[0] for k,v in SOURCES.items()},"WFO_scent_species_exact_NHM_matches":len(scent),"source_support_counts":actual,"mark_by_scent":{"|".join(k):v for k,v in sorted(table.items())},"mark_by_scent_with_WFO_size":{"|".join(k):v for k,v in sorted(sizes.items())},"GIFT_modes_among_mark_scent_explicit":dict(modes),"unknown_is_not_absence":True,"WFO_size_source_bounds_not_measured_size":True,"AusTraits_104_measured_species_not_in_this_join":True,"NO_geographic_holdout_region_outcome_rows_joined":True,"NO_within_species_cue_substitution_or_causal_inference":True}

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--archives",required=True,type=Path);p.add_argument("--out",required=True,type=Path);a=p.parse_args()
    assert mark({"flower colour":"purple spotted"})=="positive"
    assert mark({"flower colour":"without spots"})=="explicit_plain"
    assert mark({"flower colour":"white"})=="unmentioned"
    assert mark({})=="colour_missing"
    d=run(a.archives);a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n")
    print("STAGE115_ACTUAL_SAME_SPECIES_SOURCE_SUPPORT",json.dumps(d,sort_keys=True))
