#!/usr/bin/env python3
"""Stage103: recover original WFO flower diameter interval and upper-bound traits.

Crucial: WFO eFloras describes a range "8--9 cm", which Stage100 initially
treated as a point value 9 cm. Preserve original interval [80,90] mm and
upper bound (0,20] for "flowers to 2 cm" rather than make up a mean.

Scan only the 237 original WFO species with unreviewed whole-flower size
mentions, authenticated in Stage100. The 58 corolla-only source taxa remain
excluded. Frozen 72 mainland contact-free exploration vs 37 original holdout.

All source values are *unreviewed botanical prose*, not measured flower
detection, and range intervals across treatment sources are envelopes of
reported morphologies, NOT formal measurement uncertainty CIs. No wind fit.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,re,statistics,sys,zipfile
from collections import Counter,defaultdict
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
for sub in ("floral_macro_stage87","floral_macro_stage100","floral_macro_stage102"):
    sys.path.insert(0,str(BASE/sub))
from global_native_floral_signal_tdwg3 import load_nhm,wcvp_regions
from authentic_WFO_diameter_strict_quality_audit import (
   load_frozen_stage100,load_geographic_frame,strict_source_candidate_evidence,
   INTERVENING_OTHER_STRUCTURE, FROZEN_SRC_BY_LABEL
)
from wfo202606_source_reader_frozen import (
    parse_meta,iter_rows,field,cleaned,canon_source_binomial,
    stable_wfo_name_id,source_legacy_wfo_ids,WFO_backbone_202606_crosswalk,
    sha256
)

FLOAT=r"\d{1,3}(?:\.\d+)?"
RANGESEP=r"(?:--|[-–—~]|\s+to\s+)"
UNIT=r"(?:mm|cm)"
AXIS=r"(?:diam(?:eter)?\.?|across|wide)"
FLOWER=r"flowers?"
RANGE_AFTER=re.compile(
    rf"\b{FLOWER}\b(?P<context>[^.;:\n]{{0,48}}?)"
    rf"\b(?P<lower>{FLOAT})\s*(?:{RANGESEP})\s*(?P<upper>{FLOAT})"
    rf"\s*(?P<unit>{UNIT})\s*(?:in\s+)?{AXIS}\b",re.I)
RANGE_BEFORE=re.compile(
    rf"\b{FLOWER}\s+(?:diam(?:eter)?\.?|width)\s*"
    rf"(?P<lower>{FLOAT})\s*(?:{RANGESEP})\s*(?P<upper>{FLOAT})"
    rf"\s*(?P<unit>{UNIT})\b",re.I)
LIMIT=r"(?:up\s+to|to|at\s+most|less\s+than|under|not\s+more\s+than|no\s+more\s+than|maximum)"
UPPER_AFTER=re.compile(
    rf"\b{FLOWER}\b(?P<context>[^.;:\n]{{0,48}}?)"
    rf"\b(?:{LIMIT})\s*(?P<upper>{FLOAT})\s*(?P<unit>{UNIT})"
    rf"\s*(?:in\s+)?{AXIS}\b",re.I)
UPPER_BEFORE=re.compile(
    rf"\b{FLOWER}\s+(?:diam(?:eter)?\.?|width)\s*(?:{LIMIT})\s*"
    rf"(?P<upper>{FLOAT})\s*(?P<unit>{UNIT})\b",re.I)

def source_evidence(text):
    txt=cleaned(text)
    evidence=[];quality=Counter();used_spans=[]
    for mode,regex in (("bounded_interval",RANGE_AFTER),
                       ("bounded_interval",RANGE_BEFORE),
                       ("upper_limit_only",UPPER_AFTER),
                       ("upper_limit_only",UPPER_BEFORE)):
        for m in regex.finditer(txt):
            subject_context=m.groupdict().get("context") or ""
            if INTERVENING_OTHER_STRUCTURE.search(subject_context):
                quality["different_organ_in_flower_clause_rejected"]+=1;continue
            if re.search(r"\d",subject_context):
                quality["multiple_numbers_in_subject_clause_rejected"]+=1;continue
            factor=10 if m.group("unit").lower()=="cm" else 1
            upper=float(m.group("upper"))*factor
            lower=float(m.group("lower"))*factor if mode=="bounded_interval" else None
            if upper<=0 or upper>250 or (lower is not None and not .1<=lower<=upper):
                quality["implausible_or_reversed_interval_rejected"]+=1;continue
            key=(m.start(),m.end(),mode,lower,upper)
            if key in used_spans:continue
            used_spans.append(key)
            evidence.append({"evidence_type":mode,"lower_mm":lower,"upper_mm":upper,
                "source_phrase_SHA256":hashlib.sha256(m.group(0).encode()).hexdigest()})
            quality["admitted_"+mode]+=1
    points,risk,_=strict_source_candidate_evidence(txt)
    for point in points:
        # The strict parser already excludes ranges/upper limits by syntax,
        # but guard additionally against any overlapping source phrase.
        if not 0.1<=point<=250:continue
        if any(x["evidence_type"]=="bounded_interval" and
               x["lower_mm"]<=point<=x["upper_mm"] for x in evidence):
            quality["potential_duplicate_point_with_range_source"]+=1
        evidence.append({"evidence_type":"exact_source_single_number",
                         "lower_mm":point,"upper_mm":point,
                         "source_phrase_SHA256":hashlib.sha256(
                            ("source_original_exact_"+str(point)+"_"+hashlib.sha256(txt.encode()).hexdigest()).encode()).hexdigest()})
    quality["admitted_exact_source_single_number"]=len(points)
    return evidence,dict(quality)

def aggregate_species(evidence):
    """An evidence envelope is NOT a true variation/precision interval."""
    if not evidence:return {"status":"no_eligible_size_evidence","lower_mm":None,"upper_mm":None}
    intervals=[x for x in evidence if x["evidence_type"]=="bounded_interval"]
    uppers=[x for x in evidence if x["evidence_type"]=="upper_limit_only"]
    points=[x for x in evidence if x["evidence_type"]=="exact_source_single_number"]
    bounds=[x for x in intervals+points if x["lower_mm"] is not None]
    if bounds:
        lo=min(x["lower_mm"] for x in bounds)
        hi=max([x["upper_mm"] for x in evidence])
        st="bounded_source_range_or_mixed" if intervals else "exact_source_singletons"
        if uppers:st="bounded_plus_upper_limit_sources"
    elif uppers:
        lo=None;hi=max(x["upper_mm"] for x in uppers)
        st="upper_limit_only_source_NO_lower_bound"
    else:
        return {"status":"no_eligible_size_evidence","lower_mm":None,"upper_mm":None}
    return {"status":st,"lower_mm":lo,"upper_mm":hi,
      "n_original_source_exact_entries":len(points),
      "n_original_source_bounded_intervals":len(intervals),
      "n_original_source_upper_only":len(uppers),
      "original_source_values_envelope_not_CI":True,
      "source_envelope_over_5fold_NEEDS_REVIEW":(hi>5*lo if lo is not None else False)}

def scan_source(path,label,accepted,crosswalk):
    if sha256(path)!=FROZEN_SRC_BY_LABEL[label]:
        raise ValueError("STAGE103_ORIGINAL_WFO_SOURCE_SHA_DRIFT_"+label)
    hits=defaultdict(list);audit=Counter();seen_text_hash=defaultdict(set)
    with zipfile.ZipFile(path) as z:
        meta=parse_meta(z);core=next(m for m in meta if m["type"]=="core")
        if core["id"] is None:raise ValueError("STAGE103_ORIGINAL_WFO_NO_CORE_ID")
        taxa={}
        for row in iter_rows(z,core):
            audit["original_taxon_rows"]+=1
            name=field(row,core["fields"],"scientificname")
            if name:sp=canon_source_binomial(name,field(row,core["fields"],"taxonrank"))
            else:
                i=field(row,core["fields"],"taxonid") or row[core["id"]]
                sp=crosswalk.get(stable_wfo_name_id(i))
            if sp in accepted:
                status=field(row,core["fields"],"taxonomicstatus").casefold().strip()
                if status and status not in {"accepted","valid"}:continue
                taxa[row[core["id"]]]=sp
        descriptions=[d for d in meta if d["type"]=="extension" and
                 ("description" in d["fields"] or "description" in d["row_type"].casefold())]
        if not descriptions:raise ValueError("STAGE103_ORIGINAL_SOURCE_DESCRIPTION_MEMBER_ABSENT")
        for d in descriptions:
            if "description" not in d["fields"] or d["coreid"] is None:continue
            for row in iter_rows(z,d):
                audit["original_full_botanical_description_rows"]+=1
                if d["coreid"]>=len(row):continue
                sp=taxa.get(row[d["coreid"]])
                if not sp:continue
                txt=cleaned(field(row,d["fields"],"description"))
                digest=hashlib.sha256(txt.encode()).hexdigest()
                if not txt or digest in seen_text_hash[sp]:continue
                seen_text_hash[sp].add(digest)
                raw,diag=source_evidence(txt)
                for k,v in diag.items():audit[k]+=v
                if raw:
                    hits[sp].extend([{**item,"original_source_prose_SHA256":digest,
                                       "original_flora_name":label} for item in raw])
                    audit["original_descriptions_with_bound_or_exact_size"]+=1
    if audit["original_full_botanical_description_rows"]<100:
        raise ValueError("STAGE103_NOT_ACTUALLY_ORIGINAL_FULL_FLORA_TEXT")
    return hits,dict(audit)

def run(stage100_zip,stage98B_zip,nhm,wcvp,china,fna,backbone,outdir):
    ledger=load_frozen_stage100(stage100_zip)
    train,test=load_geographic_frame(stage98B_zip)
    source_train={k for k,v in ledger.items() if v["source_202606_WFO_prose_state"]=="candidate_flower_diameter_from_prose"}
    if len(source_train)!=237:
        raise ValueError("STAGE103_ORIGINAL_WFO_FULLFLOWER237_SOURCE_DRIFT")
    flora=(("Flora_of_China",china),("Flora_of_North_America",fna))
    approved,_=load_nhm(nhm);native,_=wcvp_regions(wcvp,approved)
    world=set().union(*native.values())
    if len(world)!=55775 or len(native)!=367 or not source_train<=world:
        raise ValueError("STAGE103_WCVP_NATIVE_FLORA_UNIVERSE_DRIFT")
    source_ids=set()
    for label,path in flora:
        if sha256(path)!=FROZEN_SRC_BY_LABEL[label]:
            raise ValueError("STAGE103_ORIGINAL_FLORA_SHA_DRIFT")
        ids,_=source_legacy_wfo_ids(path);source_ids.update(ids)
    mapping,meta=WFO_backbone_202606_crosswalk(backbone,source_ids,source_train)
    if not mapping:raise ValueError("STAGE103_ORIGINAL_WFO_BACKBONE_SPECIES_JOIN_FAILED")
    all_evidence=defaultdict(list);provenance={}
    for label,path in flora:
        found,qc=scan_source(path,label,source_train,mapping)
        for sp,items in found.items():all_evidence[sp].extend(items)
        provenance[label]=qc
    aggregated={sp:aggregate_species(all_evidence[sp]) for sp in sorted(source_train)}
    statuses=Counter(x["status"] for x in aggregated.values())
    ranged={sp for sp,rec in aggregated.items()
        if rec.get("n_original_source_bounded_intervals",0)>0}
    exact={sp for sp,rec in aggregated.items() if rec.get("n_original_source_exact_entries",0)>0}
    only_upper={sp for sp,rec in aggregated.items() if rec["status"]=="upper_limit_only_source_NO_lower_bound"}
    measurable={sp for sp,v in aggregated.items() if v["status"]!="no_eligible_size_evidence"}
    if not measurable:raise ValueError("STAGE103_SOURCE_ORIGINAL_237_CANDIDATES_ZERO_DIMENSION_RECONSTRUCTION")
    # Some source singletons may also occur in original intervals; do not
    # invent independent "measured species" by summing grade counts.
    trnative=set().union(*(native[k] for k in train))
    honative=set().union(*(native[k] for k in test))
    region_rows=[]
    for code in sorted(train|test):
        plants=native[code]
        region_rows.append({
         "TDWG_L3":code,"original_fixed_geographic_split":"exploration" if code in train else "holdout",
         "n_WFO_original_237_unreviewed_raw_candidates":len(source_train&plants),
         "n_WFO_extracted_source_bounded_intervals":len(ranged&plants),
         "n_WFO_source_eligible_bounded_or_upper_or_singleton":len(measurable&plants),
         "n_WFO_exact_source_singleton_candidates_NOT_manual":len(exact&plants),
         "n_WFO_only_upper_bound_NO_lower":len(only_upper&plants),
         "no_regional_ERA5_gust_wind_effect_estimated":"YES"})
    groups={}
    for fold in ("exploration","holdout"):
        reg=[r for r in region_rows if r["original_fixed_geographic_split"]==fold]
        if len(reg)!=(72 if fold=="exploration" else 37):
            raise ValueError("STAGE103_ORIGINAL_MAINLAND_FOLD_COUNT_DRIFT")
        groups[fold]={"source_region_count":len(reg),
            "regions_with_10plus_actual_bounded_or_upper_source_species":sum(
                r["n_WFO_source_eligible_bounded_or_upper_or_singleton"]>=10 for r in reg),
            "regions_with_10plus_bounded_interval_source_species":sum(
                r["n_WFO_extracted_source_bounded_intervals"]>=10 for r in reg),
            "regions_with_5plus_bounded_interval_source_species":sum(
                r["n_WFO_extracted_source_bounded_intervals"]>=5 for r in reg)}
    info={"schema":"stage103_WFO_original_202606_flora_native_flower_size_intervals_not_point",
      "source_stage100_unreviewed_whole_flower_237_original_species":237,
      "exact_source_taxonomic_species":len(aggregated),
      "original_author_botanical_prose_by_flora":provenance,
      "WFO_versioned_accepted_name_crosswalk":meta,
      "source_original_Gift_pollen_guild_NOT_inferred":True,
      "source_semantic_size_classes":dict(statuses),
      "source_distinct_species_with_bounded_range":len(ranged),
      "source_distinct_species_with_exact_singleton_phrase":len(exact),
      "source_distinct_species_with_upper_limit_only":len(only_upper),
      "source_distinct_species_with_any_valid_bounded_or_upper_or_singleton":len(measurable),
      "source_eligible_size_holdout_unique_species":len(measurable&honative),
      "source_eligible_size_holdout_UNSEEN_72_train_species":len(measurable&(honative-trnative)),
      "source_frozen_mainland_regions":groups,
      "source_author_upper_endpoint_NEVER_promoted_to_exact_value":True,
      "size_intervals_are_morphological_source_envelopes_NOT_measurement_uncertainty":True,
      "bounded_intervals_not_direct_point_observations":True,
      "human_extraction_precision_still_unverified":True,
      "no_ERA5_area_weighted_wind_or_flower_selection_coefficient":True,
      "original_WFO_full_text_copyright_not_redistributed":True}
    outdir.mkdir(parents=True,exist_ok=True)
    with (outdir/"stage103_original_WFO_237_flower_source_interval_envelopes_NOT_measured.csv").open("w",newline="",encoding="utf-8") as f:
        records=[{"accepted_species":sp,**agg} for sp,agg in sorted(aggregated.items())]
        columns=list(dict.fromkeys(k for r in records for k in r))
        writer=csv.DictWriter(f,fieldnames=columns);writer.writeheader();writer.writerows(records)
    with (outdir/"stage103_original_mainland_72_37_WFO_interval_size_source_counts.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(region_rows[0]));w.writeheader();w.writerows(region_rows)
    (outdir/"stage103_WFO_original_flower_size_interval_not_point_receipt.json").write_text(
        json.dumps(info,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("STAGE103_AUTHENTIC_SOURCE_WFO_FLOWER_SIZE_INTERVALS",json.dumps({
        "bounded_species":len(ranged),"upper_only":len(only_upper),
        "singleton":len(exact),"with_any_source_bound":len(measurable),
        "mainland_heldout_37_region_source_support":groups["holdout"]},
        sort_keys=True),flush=True)
    return info

if __name__=="__main__":
    p=argparse.ArgumentParser()
    for arg in ("stage100-original-zip","stage98B-mainland-source-zip",
            "original-NHM","original-WCVP","original-China","original-FNA",
            "original-WFO-202606-backbone"):
        p.add_argument("--"+arg,required=True,type=Path)
    p.add_argument("--outdir",required=True,type=Path)
    a=p.parse_args();run(a.stage100_original_zip,a.stage98B_mainland_source_zip,
      a.original_NHM,a.original_WCVP,a.original_China,a.original_FNA,
      a.original_WFO_202606_backbone,a.outdir)
