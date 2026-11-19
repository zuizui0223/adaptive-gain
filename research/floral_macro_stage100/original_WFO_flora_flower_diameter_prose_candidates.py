#!/usr/bin/env python3
"""Stage100 original WFO eFloras full-text flower-width lexical candidate audit.

Do NOT label a flower size when only petal, corolla-tube, inflorescence, leaf,
peduncle or fruit width is mentioned. Whole-flower candidate lexical statements
are not automatically validated true open-display size (or pollinator vision).

Original complete official WFO China/FNA descriptions + 2026-06 name-id
backbone are SHA/MD5-checked and joined exactly to original WCVP native species.
Results are source-mention opportunities, not wind effects or causal adaptation.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,re,sys,zipfile,statistics
from collections import Counter,defaultdict
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
for folder in ("floral_macro_stage87","floral_macro_stage89","floral_macro_stage100"):
    sys.path.insert(0,str(BASE/folder))
from global_native_floral_signal_tdwg3 import load_nhm,wcvp_regions
from gift32_independent_pollen_mode_global_native_coverage import original_gift_species
from wfo202606_source_reader_frozen import (
    parse_meta,iter_rows,field,cleaned,canon_source_binomial,
    source_legacy_wfo_ids,WFO_backbone_202606_crosswalk,
    stable_wfo_name_id,SOURCE_SHA256 as SOURCE_WFO_ORIGINAL_SHA,sha256,
)

WFO_BACKBONE_ZENODO_MD5="0e4486945cd9f7af548ca87eb9a870ed"
FROZEN_SRC_BY_LABEL={
  "Flora_of_China":SOURCE_WFO_ORIGINAL_SHA["Flora_of_China"],
  "Flora_of_North_America":SOURCE_WFO_ORIGINAL_SHA["Flora_of_North_America"]
}
# Exclude intervening organs which have a width other than flower display.
OTHER_ORGAN=re.compile(
    r"\b(?:inflorescences?|heads?|capitula|spikes?|panicles?|racemes?|"
    r"peduncles?|bracts?|leaves?|leaf|fruits?|seeds?|ovaries|"
    r"stems?|calyces|pollen|anthers?|stamens?|sepals?)\b",re.I)
PRECEDING_RANGE=re.compile(r"\d+(?:\.\d+)?\s*(?:to|[-–—])\s*$",re.I)
APPROX_NOTE=re.compile(r"\b(?:ca\.?|c\.?|approximately|about)\s*$",re.I)
NUMBER=r"(?P<num>(?:\d{1,3})(?:\.\d+)?)\s*(?P<unit>mm|cm)\b"
TYPE=r"(?P<organ>flowers?|corollas?)"
P_AFTER=re.compile(rf"\b{TYPE}\b(?P<between>[^.;:\n]{{0,75}}?)"
                   rf"(?P<measure>{NUMBER})\s*(?:in\s+)?"
                   rf"(?P<axis>diam(?:eter)?\.?|across|wide)\b",re.I)
P_BEFORE=re.compile(rf"\b{TYPE}\s+(?P<axis>diam(?:eter)?\.?|width)\s*"
                    rf"(?:is\s+|of\s+|ca\.?\s+|about\s+)?"
                    rf"(?P<measure>{NUMBER})",re.I)

def width_candidates(text):
    """Extract conservative explicit whole-flower diameter or corolla width.

    Returns numeric source-tagged candidates only; unmentioned != small/zero.
    """
    txt=cleaned(text)
    found=[];counts=Counter();seen=set()
    for pattern in (P_AFTER,P_BEFORE):
        for m in pattern.finditer(txt):
            counts["all_candidate_source_lexical_matches"]+=1
            organ=m.group("organ").casefold()
            between=m.groupdict().get("between") or ""
            fragment=m.group(0)
            if OTHER_ORGAN.search(between):
                counts["discard_intervening_other_organ"]+=1
                continue
            number_start=m.start("num")
            if PRECEDING_RANGE.search(txt[max(m.start(),number_start-18):number_start]):
                counts["discard_numeric_range"]+=1
                continue
            numeric=float(m.group("num"))*(10. if m.group("unit").casefold()=="cm" else 1.)
            if not (0.1<=numeric<=250):
                counts["discard_implausible_or_unbounded_numeric_mm"]+=1
                continue
            if organ.startswith("corolla"):
                kind="corolla_width_TEXT_NOT_WHOLE_FLOWER"
            else:
                kind="flower_diameter_TEXT_CANDIDATE"
            key=(m.start(),m.end(),kind,round(numeric,5))
            if key in seen:continue
            seen.add(key)
            found.append((kind,numeric))
            counts["admitted_"+kind]+=1
    return found,dict(counts)

def per_species_source_cue(cues):
    """Only species with a single nonconflicting measurement are candidates."""
    flower=[v for kind,v in cues if kind=="flower_diameter_TEXT_CANDIDATE"]
    corolla=[v for kind,v in cues if kind=="corolla_width_TEXT_NOT_WHOLE_FLOWER"]
    if len(flower):
        if max(flower)>min(flower)*1.5:
            return "multiple_conflicting_flower_diameter_prose",None
        return "candidate_flower_diameter_from_prose",statistics.median(flower)
    if corolla:
        if max(corolla)>min(corolla)*1.5:
            return "multiple_conflicting_corolla_width_prose",None
        return "candidate_corolla_width_only_NOT_whole_flower",statistics.median(corolla)
    return "no_unambiguous_diameter_phrase",None

def scan_source(path,label,accepted,wfo_ids):
    if sha256(path)!=FROZEN_SRC_BY_LABEL[label]:
        raise ValueError("STAGE100_AUTHOR_ORIGINAL_WFO_SOURCE_SHA_DRIFT_"+label)
    counts=Counter();pairs=defaultdict(list);described=set()
    with zipfile.ZipFile(path) as z:
        meta=parse_meta(z)
        core=next(x for x in meta if x["type"]=="core")
        if core["id"] is None:raise ValueError("STAGE100_SOURCE_WFO_NO_PRIMARY_TAXON_ID")
        taxa={}
        for row in iter_rows(z,core):
            counts["original_source_taxon_rows"]+=1
            raw=field(row,core["fields"],"scientificname")
            if raw:
                sp=canon_source_binomial(raw,field(row,core["fields"],"taxonrank"))
            else:
                rawid=field(row,core["fields"],"taxonid") or row[core["id"]]
                wfo=stable_wfo_name_id(rawid)
                sp=wfo_ids.get(wfo)
            if not sp or sp not in accepted:continue
            status=field(row,core["fields"],"taxonomicstatus").casefold().strip()
            if status and status not in {"accepted","valid"}:continue
            key=row[core["id"]]
            if key in taxa and taxa[key]!=sp:
                raise ValueError("STAGE100_DUPLICATE_ORIGINAL_WFO_TAXON_CORE_ID")
            taxa[key]=sp
        counts["source_native_accepted_taxon_ids"]=len(taxa)
        descriptions=[d for d in meta if d["type"]=="extension" and
            ("description" in d["row_type"].casefold() or "description" in d["fields"])]
        if not descriptions:raise ValueError("STAGE100_NO_ORIGINAL_AUTHOR_DESCRIPTION_EXT")
        for d in descriptions:
            if d["coreid"] is None:continue
            col=next((v for v in ("description","text","abstract") if v in d["fields"]),None)
            if col is None:continue
            for row in iter_rows(z,d):
                counts["original_source_full_description_rows"]+=1
                if d["coreid"]>=len(row):continue
                sp=taxa.get(row[d["coreid"]])
                if sp is None:continue
                txt=cleaned(field(row,d["fields"],col))
                if not txt:continue
                described.add(sp)
                matches,diag=width_candidates(txt)
                for k,v in diag.items():counts[k]+=v
                if matches:
                    pairs[sp].extend(matches)
                    counts["matched_source_description_rows_with_explicit_size_phrase"]+=1
        if counts["original_source_taxon_rows"]<100 or not counts["original_source_full_description_rows"]:
            raise ValueError("STAGE100_ORIGINAL_FULL_FLORA_SOURCE_NOT_READ")
    return described,pairs,dict(counts)

def run(nhm,wcvp,gift,china,fna,backbone,output):
    accepted,_=load_nhm(nhm)
    native,_=wcvp_regions(wcvp,accepted)
    modes,_=original_gift_species(gift)
    universe=set().union(*native.values())
    if len(native)!=367 or len(universe)!=55775 or len(set(modes)&universe)!=3172:
        raise ValueError("STAGE100_ORIGINAL_GLOBAL_NATIVE_SPECIES_MODE_COHORT_CHANGED")
    flora=(("Flora_of_China",china),("Flora_of_North_America",fna))
    ids=set()
    source_idcounts={}
    for label,path in flora:
        if sha256(path)!=FROZEN_SRC_BY_LABEL[label]:
            raise ValueError("STAGE100_ORIGINAL_WFO_SOURCE_ORIGINAL_SHA_DRIFT")
        these,counts=source_legacy_wfo_ids(path)
        ids.update(these);source_idcounts[label]=counts
    mapping,meta=WFO_backbone_202606_crosswalk(backbone,ids,universe)
    if len(mapping)<1000:raise ValueError("STAGE100_NO_VERIFIED_WFO_NATIVE_NAME_MAP")
    all_seen=set();raw=defaultdict(list);orig={};species_source_labels=defaultdict(set)
    for label,path in flora:
        seen,cues,counters=scan_source(path,label,universe,mapping)
        all_seen.update(seen)
        for sp,v in cues.items():
            raw[sp].extend(v)
            species_source_labels[sp].add(label)
        orig[label]={"source_SHA256":FROZEN_SRC_BY_LABEL[label],
                     "source_total_described_native_species":len(seen),
                     "source_candidate_species":len(cues),
                     "counters":counters}
    results={sp:per_species_source_cue(v) for sp,v in raw.items()}
    types=Counter(state for state,value in results.values())
    flower={s:v for s,(state,v) in results.items()
             if state=="candidate_flower_diameter_from_prose" and v is not None}
    corolla={s:v for s,(state,v) in results.items()
             if state=="candidate_corolla_width_only_NOT_whole_flower" and v is not None}
    if not all(sp in universe for sp in results):
        raise ValueError("STAGE100_SOURCE_SPECIES_NOT_IN_NATIVE_ACCEPTED_WCVP")
    if len(all_seen)<1000:raise ValueError("STAGE100_SOURCE_NONTRIVIAL_DESCRIPTIONS_MISSING")
    appearances=Counter(sp for plants in native.values() for sp in plants)
    original_species_ledger=[
        {"accepted_species_exact_WCVP":sp,
         "source_202606_WFO_prose_state":results[sp][0],
         "source_unreviewed_prose_whole_flower_diameter_mm":(
            results[sp][1] if results[sp][0]=="candidate_flower_diameter_from_prose" else ""),
         "source_corolla_width_only_NOT_whole_flower_mm":(
            results[sp][1] if results[sp][0]=="candidate_corolla_width_only_NOT_whole_flower" else ""),
         "source_original_flora_providers":"|".join(sorted(species_source_labels[sp])),
         "independent_GIFT_pollen_vector_mode":modes.get(sp,"unknown"),
         "original_WCVP_native_TDWG_region_repetitions":appearances[sp],
         "floral_size_description_manual_validation":"PENDING",
         "source_exact_full_flower_visual_display_not_verified":"YES"}
        for sp in sorted(results)]
    sizes=[]
    for code,plants in sorted(native.items()):
        subset=set(plants)&set(flower)
        mode=Counter(modes.get(sp,"unknown") for sp in subset)
        sizes.append({"TDWG_L3":code,"n_source_original_native_species":len(plants),
            "n_real_original_eflora_described_native_species":len(set(plants)&all_seen),
            "n_source_unreviewed_whole_flower_diameter_phrase_species":len(subset),
            "n_source_distinct_size_phrase_genera":len({sp.split()[0] for sp in subset}),
            "n_size_phrase_GIFT_animal":mode["animal"],
            "n_size_phrase_GIFT_wind":mode["wind"],
            "n_size_phrase_GIFT_unknown":mode["unknown"],
            "source_size_phrase_species_median_mm":statistics.median([flower[s] for s in subset]) if subset else "",
            "n_source_corolla_width_only_NOT_whole_flower_species":len(set(plants)&set(corolla)),
            "mainland_spatial_scope":"NOT_AUDITED_INCLUDES_ISLANDS",
            "source_diameter_not_automatically_true_visual_display":"TRUE"})
    rec={"schema":"stage100_authentic_202606_WFO_flora_direct_whole_flower_diameter_prose_source_audit",
        "source_original_NHM_WCVP_native_species":len(universe),
        "source_original_TDWG3_regions_INCLUDING_islands":len(native),
        "original_source_flora_identity_verified":orig,
        "original_WFO_202606_backbone_crosswalk":meta,
        "original_WFO_flora_taxon_ID_inventory":source_idcounts,
        "unique_source_native_species_with_original_botanical_prose":len(all_seen),
        "unique_accepted_native_species_with_ANY_direct_width_phrase":len(results),
        "species_source_phrase_state_counts":dict(types),
        "n_original_source_unreviewed_flower_diameter_phrase_species":len(flower),
        "n_original_source_only_corolla_width_not_whole_flower_species":len(corolla),
        "source_species_ledger_exact_rows":len(original_species_ledger),
        "source_species_ledger_no_raw_botanical_description_redistribution":True,
        "source_GIFT_mode_with_whole_flower_diameter_phrase":dict(Counter(modes.get(s,"unknown") for s in flower)),
        "flower_diameter_prose_candidates_are_NOT_manually_phenotype_validated":True,
        "no_range_imputation_or_petals_or_inflorescences":True,
        "source_undocumented_is_unknown_NOT_zero_size":True,
        "no_ecological_wind_flower_cue_coefficient_estimated":True,
        "not_a_125_region_mainland_area_wind_exposure":True}
    output.mkdir(parents=True,exist_ok=True)
    with (output/"stage100_WFO_original_accepted_species_whole_flower_diameter_SOURCE_CANDIDATE.csv").open("w",newline="",encoding="utf-8") as f:
        wr=csv.DictWriter(f,fieldnames=list(original_species_ledger[0]))
        wr.writeheader();wr.writerows(original_species_ledger)
    with (output/"stage100_wfo_original_size_phrase_367_regions_INCLUDES_ISLANDS.csv").open("w",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=list(sizes[0]));wr.writeheader();wr.writerows(sizes)
    (output/"stage100_original_eflora_flower_diameter_prose_candidate_receipt.json").write_text(
        json.dumps(rec,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("STAGE100_ACTUAL_ORIGINAL_WFO_FLOWER_DIAMETER_PHRASE_SUPPORT",json.dumps({
        "native_species_with_prose":len(all_seen),
        "whole_flower_diameter_candidates":len(flower),
        "corolla_only_candidates":len(corolla),
        "mode_breakdown":rec["source_GIFT_mode_with_whole_flower_diameter_phrase"],
        "candidate_type_counts":dict(types)},sort_keys=True),flush=True)
    return rec

if __name__=="__main__":
    p=argparse.ArgumentParser()
    for arg in ("original-NHM","original-WCVP","original-GIFT",
                "original-China","original-FNA","original-WFO-backbone"):
        p.add_argument("--"+arg,required=True,type=Path)
    p.add_argument("--outdir",required=True,type=Path)
    a=p.parse_args()
    run(a.original_NHM,a.original_WCVP,a.original_GIFT,
        a.original_China,a.original_FNA,a.original_WFO_backbone,a.outdir)
