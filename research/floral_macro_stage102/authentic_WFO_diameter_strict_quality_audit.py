#!/usr/bin/env python3
"""Stage102: independently audit original WFO size phrase extraction specificity.

Do not call machine checks human validation. Trace 295 WFO size candidate
species back to two SHA-verified ORIGINAL botanical description archives,
using the author-supplied versioned WFO-2026-06 name crosswalk and frozen
Stage100 source-candidate species ledger. Implement a stricter *independent*
organ/proximity grammar and compare the source phenotype counts from both
parsers. Annotate lexical risk features, not false-positive labels.

No published copyright full botanical prose is redistributed: only short
matched phrase examples (max 62 chars) in GitHub job logs for a small,
preselected review queue, plus cryptographic hashes and quality tags in
the derived ZIP. Actual precision still requires independent source reading.
No gust/regression, no biological fitness/receptor signal conclusion.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,re,sys,statistics,zipfile
from collections import Counter,defaultdict
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
for folder in ("floral_macro_stage87","floral_macro_stage100"):
    sys.path.insert(0,str(BASE/folder))
from global_native_floral_signal_tdwg3 import load_nhm,wcvp_regions
from original_WFO_flora_flower_diameter_prose_candidates import (
    width_candidates,per_species_source_cue,P_AFTER,P_BEFORE,
    FROZEN_SRC_BY_LABEL
)
from wfo202606_source_reader_frozen import (
    parse_meta,iter_rows,field,cleaned,canon_source_binomial,
    stable_wfo_name_id,source_legacy_wfo_ids,WFO_backbone_202606_crosswalk,
    sha256
)

FROZEN_STAGE100_ZIP_SHA="06c370061a4c069038aaf11ecd59a423fb00cb051db6ec67632e316ce9d2ebd4"
FROZEN_STAGE98B_ZIP_SHA="8026b800672cad2afd97e2fe416349cc3aca8f650e78ae8c001dd31de104c8b7"
STAGE100_LEDGER="stage100_WFO_original_accepted_species_whole_flower_diameter_SOURCE_CANDIDATE.csv"
STAGE100_RECEIPT="stage100_original_eflora_flower_diameter_prose_candidate_receipt.json"
STAGE98B_TRAIN="stage98B_train_original_mainland_no_holdout_polygon_contact_72.csv"
STAGE98B_HOLDOUT="stage98B_holdout_original_mainland_37_UNCHANGED.csv"
WFO_SOURCE_MAP={"China":"Flora_of_China","NorthAmerica":"Flora_of_North_America"}
INTERNAL_SAMPLE_SALT="stage102_fixed_original_WFO_independent_parser_QA_20261120_v1"

# New predeclared high-specificity parser: a second grammar, not relabelling
# the old same-source positive count as a verified ground truth.
STRONG_WHOLE_AFTER=re.compile(
    r"\bflowers?\b(?P<context>[^.;:\n]{0,40}?)"
    r"\b(?P<number>\d{1,3}(?:\.\d+)?)\s*(?P<unit>mm|cm)\s*"
    r"(?:(?:in)\s+)?(?P<axis>diam(?:eter)?\.?|across|wide)\b",re.I)
STRONG_WHOLE_BEFORE=re.compile(
    r"\bflowers?\s+(?:diam(?:eter)?\.?|width)\s*(?:is\s+|of\s+|ca\.?\s+|about\s+)?"
    r"(?P<number>\d{1,3}(?:\.\d+)?)\s*(?P<unit>mm|cm)\b",re.I)
INTERVENING_OTHER_STRUCTURE=re.compile(
    r"\b(?:leaves?|petals?|sepals?|tepals?|corollas?|lobes?|"
    r"tubes?|tubular|flower\s+tubes?|heads?|capitula|capitulum|"
    r"inflorescences?|clusters?|cymes?|corymbs?|umbels?|"
    r"panicles?|racemes?|spikes?|spikelets?|bracts?|"
    r"peduncles?|stems?|branches?|ovaries|fruits?|seeds?|"
    r"pollen|anthers?|stamens?|receptacles?)\b",re.I)
# eFloras commonly uses literal "--" to encode a botanical size range
# ("8--9 cm", not a measured singleton 9 cm). Prefix may also be an upper
# bound ("flowers to 2 cm"); neither is an exact point observation.
RANGE_PREFIX=re.compile(
    r"(?:\d+(?:\.\d+)?\s*(?:to|[-–—~]{1,3})\s*|"
    r"(?:up\s+to|to|at\s+most|not\s+more\s+than|"
    r"less\s+than|under|maximum|max\.?)\s*)$",re.I)
NEGATIVE_MEASUREMENT=re.compile(r"\b(?:not|without|no|rarely)\b",re.I)

def strict_source_candidate_evidence(original):
    txt=cleaned(original)
    candidates=[];risk=Counter();seen=set();examples=[]
    for p in (STRONG_WHOLE_AFTER,STRONG_WHOLE_BEFORE):
        for m in p.finditer(txt):
            before=m.groupdict().get("context") or ""
            key=(m.start(),m.end())
            if key in seen:continue
            seen.add(key)
            local=txt[max(0,m.start()-36):min(len(txt),m.end()+30)]
            blocked=[]
            if INTERVENING_OTHER_STRUCTURE.search(before):blocked.append("ambiguous_other_organ_in_clause")
            previous=txt[max(m.start(),m.start("number")-35):m.start("number")]
            if RANGE_PREFIX.search(previous):
                blocked.append("unresolved_numeric_range_or_upper_limit")
            if NEGATIVE_MEASUREMENT.search(before):blocked.append("negation_or_contrast_context")
            # Single num unit and anchored grammatical subject are mandatory.
            v=float(m.group("number"))*(10 if m.group("unit").lower()=="cm" else 1)
            if not .1<=v<=250:blocked.append("out_of_biological_QA_bounds")
            if any(x in txt[max(m.start(),m.start("number")-5):m.start("number")] for x in ("±","+/-")):
                blocked.append("uncertainty_term")
            state="strict_clause_candidate" if not blocked else "flagged_possible_false_organ_assignment"
            risk[state]+=1
            for flag in blocked:risk["risk_"+flag]+=1
            if not blocked:candidates.append(v)
            examples.append({"value_mm":v,"state":state,"risk_flags":blocked,
                 "fragment_sha256":hashlib.sha256(local.encode()).hexdigest(),
                 "very_short_fragment_for_internal_QA":re.sub(r"\s+"," ",m.group(0))[:62]})
    return candidates,dict(risk),examples

def load_frozen_stage100(archive):
    if sha256(archive)!=FROZEN_STAGE100_ZIP_SHA:
        raise ValueError("STAGE102_ORIGINAL_STAGE100_LEDGER_SHA_MISMATCH")
    with zipfile.ZipFile(archive) as z:
        if not {STAGE100_LEDGER,STAGE100_RECEIPT}<=set(z.namelist()):
            raise ValueError("STAGE102_REQUIRED_STAGE100_SOURCE_LEDGER_MISSING")
        rows=list(csv.DictReader(io.StringIO(z.read(STAGE100_LEDGER).decode("utf-8-sig"))))
        receipt=json.loads(z.read(STAGE100_RECEIPT))
    if len(rows)!=295 or receipt["n_original_source_unreviewed_flower_diameter_phrase_species"]!=237 or receipt["n_original_source_only_corolla_width_not_whole_flower_species"]!=58:
        raise ValueError("STAGE102_ORIGINAL_STAGE100_237_58_SOURCE_COHORT_CHANGED")
    data={}
    for r in rows:
        key=r["accepted_species_exact_WCVP"].casefold().strip()
        if not key or key in data:raise ValueError("STAGE102_DUPLICATE_SOURCE_SPECIES")
        data[key]=r
    return data

def load_geographic_frame(artifact):
    if sha256(artifact)!=FROZEN_STAGE98B_ZIP_SHA:
        raise ValueError("STAGE102_ORIGINAL_GEO_72_37_SHA_MISMATCH")
    with zipfile.ZipFile(artifact) as z:
        def read(member):
            return list(csv.DictReader(io.StringIO(z.read(member).decode("utf-8-sig"))))
        train=read(STAGE98B_TRAIN);test=read(STAGE98B_HOLDOUT)
    a={r["TDWG_L3"] for r in train};b={r["TDWG_L3"] for r in test}
    if len(a)!=72 or len(b)!=37 or a&b:
        raise ValueError("STAGE102_ORIGINAL_MAINLAND_72_37_COHORT_CHANGED")
    return a,b

def scan_original_flora_for_qa(archive,label,approved,crosswalk):
    if sha256(archive)!=FROZEN_SRC_BY_LABEL[label]:
        raise ValueError("STAGE102_ORIGINAL_FLORA_SOURCE_SHA_CHANGED_"+label)
    coreids={};source_counts=Counter();hits=defaultdict(list)
    with zipfile.ZipFile(archive) as z:
        meta=parse_meta(z);core=next(m for m in meta if m["type"]=="core")
        for row in iter_rows(z,core):
            source_counts["original_core_rows"]+=1
            if core["id"] is None:raise ValueError("STAGE102_WFO_CORE_ID_MISSING")
            native=field(row,core["fields"],"scientificname")
            if native:species=canon_source_binomial(native,field(row,core["fields"],"taxonrank"))
            else:
                rawid=field(row,core["fields"],"taxonid") or row[core["id"]]
                wfo=stable_wfo_name_id(rawid)
                species=crosswalk.get(wfo)
            if species in approved:
                key=row[core["id"]]
                if key in coreids and coreids[key]!=species:
                    raise ValueError("STAGE102_ORIGINAL_TAXON_CORE_ID_COLLISION")
                coreids[key]=species
        source_counts["original_matched_295_taxonIDs"]=len(coreids)
        descs=[d for d in meta if d["type"]=="extension" and
               ("description" in d["row_type"].lower() or "description" in d["fields"])]
        if not descs:raise ValueError("STAGE102_ORIGINAL_WFO_DESCRIPTIONS_MISSING")
        for d in descs:
            if d["coreid"] is None or "description" not in d["fields"]:continue
            for row in iter_rows(z,d):
                source_counts["original_author_description_rows"]+=1
                if d["coreid"]>=len(row):continue
                sp=coreids.get(row[d["coreid"]])
                if not sp:continue
                txt=cleaned(field(row,d["fields"],"description"))
                if not txt:continue
                old,_=width_candidates(txt)
                stricter,flags,fragments=strict_source_candidate_evidence(txt)
                old_fragments=[]
                if old:
                    for pattern in (P_AFTER,P_BEFORE):
                        for m in pattern.finditer(txt):
                            # The original parser itself makes the final
                            # admission decision; this snippet is a review
                            # locator only, never an admitted measurement.
                            phrase=re.sub(r"\s+"," ",m.group(0))[:62]
                            old_fragments.append({
                               "value_mm":None,
                               "state":"original_lexical_match_NEEDS_MANUAL_REVIEW",
                               "risk_flags":[],
                               "fragment_sha256":hashlib.sha256(phrase.encode()).hexdigest(),
                               "very_short_fragment_for_internal_QA":phrase})
                if old or stricter:
                    hits[sp].append({"original_old":old,"stricter":stricter,
                         "risk":flags,"examples":fragments+old_fragments,
                         "text_sha256":hashlib.sha256(txt.encode()).hexdigest()})
                    source_counts["source_taxon_description_rows_with_old_or_strict_hits"]+=1
    if source_counts["original_author_description_rows"]<100:
        raise ValueError("STAGE102_ORIGINAL_WFO_FULL_FLORA_NOT_ACTUALLY_READ")
    return hits,dict(source_counts)

def audit_species(evidence,ledger):
    keys=set(ledger);res=[]
    for sp in sorted(keys):
        old=[]
        strong=[]
        risks=Counter()
        fragments=[]
        hashes=set()
        for record in evidence.get(sp,[]):
            old.extend(record["original_old"])
            strong.extend(record["stricter"])
            risks.update(record["risk"])
            hashes.add(record["text_sha256"])
            fragments.extend(record["examples"])
        oldstate,oldval=per_species_source_cue(old)
        prior=ledger[sp]["source_202606_WFO_prose_state"]
        if oldstate!=prior:
            raise ValueError("STAGE102_OLD_ST100_SOURCE_PARSER_REPLAY_NOT_IDENTICAL_"+sp+
                 " previous="+prior+" replay="+oldstate)
        # Unchanged original Stage100 species identity. Strict source-only
        # sensitivity has its own new per-species status.
        if not strong:strict_state="NO_STRICT_CLAUSE_CONSENSUS"
        elif max(strong)>1.5*min(strong):strict_state="STRICT_CONFLICTING_VALUES"
        else:strict_state="STRICT_FRACTIONAL_MEASUREMENT_CANDIDATE"
        res.append({"source_accepted_species":sp,
            "original_stage100_organ_grade":prior,
            "original_stage100_unreviewed_mm":oldval if oldval is not None else "",
            "stricter_grammar_status":strict_state,
            "strict_original_mm":statistics.median(strong) if strict_state=="STRICT_FRACTIONAL_MEASUREMENT_CANDIDATE" else "",
            "original_author_description_SHA256_count":len(hashes),
            "strict_match_count":len(strong),
            "risk_flora_intervening_other_organ_count":risks["risk_ambiguous_other_organ_in_clause"],
            "risk_numeric_range_count":risks["risk_unresolved_numeric_range_or_upper_limit"],
            "risk_negation_count":risks["risk_negation_or_contrast_context"],
            "strict_source_text_human_validated":"NO",
            "raw_original_description_redistributed":"NO",
            "_examples":fragments})
    return res

def run(stage100_zip,stage98B_zip,nhm,wcvp,china,fna,wfo_backbone,outdir):
    original=load_frozen_stage100(stage100_zip)
    train,test=load_geographic_frame(stage98B_zip)
    full_nhm,_=load_nhm(nhm);regions,_=wcvp_regions(wcvp,full_nhm)
    world=set().union(*regions.values())
    if len(regions)!=367 or len(world)!=55775 or not set(original)<=world:
        raise ValueError("STAGE102_WCVP_NATIVE_SOURCE_COHORT_NOT_EXACT")
    src=(("Flora_of_China",china),("Flora_of_North_America",fna))
    source_ids=set()
    for label,path in src:
        if sha256(path)!=FROZEN_SRC_BY_LABEL[label]:
            raise ValueError("STAGE102_SOURCE_FLORA_ZIP_SHA_DRIFT")
        ids,_=source_legacy_wfo_ids(path);source_ids.update(ids)
    matched,cross_meta=WFO_backbone_202606_crosswalk(wfo_backbone,source_ids,set(original))
    if not matched:raise ValueError("STAGE102_WFO_BACKBONE_NO_EXACT_STAGE100_IDS")
    evidence=defaultdict(list);data_qc={}
    for label,path in src:
        found,qc=scan_original_flora_for_qa(path,label,set(original),matched)
        for sp,entries in found.items():evidence[sp].extend(entries)
        data_qc[label]=qc
    actual=audit_species(evidence,original)
    # Stratified sample selected before manual labelling, not cherry-picked.
    preselected=[]
    for kind in ("strict","flagged","corolla"):
        pool=[r for r in actual if
           (kind=="strict" and r["original_stage100_organ_grade"]=="candidate_flower_diameter_from_prose" and r["stricter_grammar_status"]=="STRICT_FRACTIONAL_MEASUREMENT_CANDIDATE") or
           (kind=="flagged" and r["original_stage100_organ_grade"]=="candidate_flower_diameter_from_prose" and r["stricter_grammar_status"]!="STRICT_FRACTIONAL_MEASUREMENT_CANDIDATE") or
           (kind=="corolla" and r["original_stage100_organ_grade"]=="candidate_corolla_width_only_NOT_whole_flower")]
        pool=sorted(pool,key=lambda r:hashlib.sha256((INTERNAL_SAMPLE_SALT+"|"+kind+"|"+r["source_accepted_species"]).encode()).hexdigest())
        for r in pool[:(6 if kind!="corolla" else 3)]:
            sample=[e for e in r["_examples"] if e["very_short_fragment_for_internal_QA"]]
            if not sample:continue
            preferred=("strict_clause_candidate" if kind=="strict" else
                       "original_lexical_match_NEEDS_MANUAL_REVIEW")
            e=next((x for x in sample if x["state"]==preferred),sample[0])
            preselected.append({"stratum":kind,
               "accepted_species":r["source_accepted_species"],
               "source_fragment_sha256":e["fragment_sha256"],
               "automated_state":e["state"],
               "human_validation":"NOT_YET_DONE"})
            # Limited to 15 short, separately identified lexical fragments,
            # never a whole flora treatment reproduced.
            print("STAGE102_TINY_ORIGINAL_PHRASE_QA",json.dumps({
              "category":kind,"species":r["source_accepted_species"],
              "short_source_match_fragment_max62chars":e["very_short_fragment_for_internal_QA"],
              "automated":e["state"]},ensure_ascii=False),flush=True)
    bystate=Counter(r["original_stage100_organ_grade"] for r in actual)
    classified=Counter(r["stricter_grammar_status"] for r in actual)
    strict_flower={r["source_accepted_species"] for r in actual
         if r["original_stage100_organ_grade"]=="candidate_flower_diameter_from_prose" and
             r["stricter_grammar_status"]=="STRICT_FRACTIONAL_MEASUREMENT_CANDIDATE"}
    source_flower={r["source_accepted_species"] for r in actual
        if r["original_stage100_organ_grade"]=="candidate_flower_diameter_from_prose"}
    if len(source_flower)!=237 or len(actual)!=295:
        raise ValueError("STAGE102_SOURCE_REAL_237_58_LEDGER_CORRUPTED")
    trainsp=set().union(*(regions[k] for k in train))
    holdsp=set().union(*(regions[k] for k in test))
    cohorts={
       "original_237_stage100_flower_candidates":len(source_flower),
       "strict_grammar_retained_original_flower_candidates":len(strict_flower),
       "source_strict_retention_fraction_not_accuracy":len(strict_flower)/len(source_flower),
       "stage100_237_holdout_distinct_source_candidates":len(source_flower&holdsp),
       "strict_source_grammar_holdout_distinct_species":len(strict_flower&holdsp),
       "strict_source_grammar_holdout_UNSEEN_in_72_training":len(strict_flower&(holdsp-trainsp)),
       "original_holdout_regions_with_at_least_10_candidates":sum(len(regions[k]&source_flower)>=10 for k in test),
       "strict_holdout_regions_with_at_least_10_candidates":sum(len(regions[k]&strict_flower)>=10 for k in test),
       "stage100_candidate_species_with_detected_range_or_upper_limit":sum(
          int(r["risk_numeric_range_count"])>0
          for r in actual if r["original_stage100_organ_grade"]=="candidate_flower_diameter_from_prose"),
       "strict_train_regions_with_at_least_10_candidates":sum(len(regions[k]&strict_flower)>=10 for k in train),
       "original_source_description_species_audited":len(original),
    }
    summary={"schema":"stage102_original_WFO_flower_size_independent_syntactic_QA_NOT_human_precision",
       "source_original_stage100_artifact_SHA256":FROZEN_STAGE100_ZIP_SHA,
       "source_original_stage98B_geography_SHA256":FROZEN_STAGE98B_ZIP_SHA,
       "source_original_WFO_flora_SHA256":FROZEN_SRC_BY_LABEL,
       "WFO_202606_original_taxon_backbone_metadata":cross_meta,
       "source_flora_legacy_dwc_meta_counts":data_qc,
       "source_old_grammar_states":dict(bystate),
       "source_stricter_grammar_states":dict(classified),
       "source_grammar_retention":cohorts,
       "stratified_validation_candidate_sample_size":len(preselected),
       "human_precision_estimate_UNAVAILABLE":True,
       "manually_verified_true_whole_flower_diameter_count_UNAVAILABLE":True,
       "source_lexical_retention_not_trait_prevalence":True,
       "no_confirmatory_wind_cue_regression":True,
       "strict_source_organ_is_NOT_a_measurement_confirmation":True,
       "source_size_and_optical_detectability_not_interchangeable":True}
    outdir.mkdir(parents=True,exist_ok=True)
    with (outdir/"stage102_original_WFO_295_species_strict_extraction_flags_NO_QUOTED_PROSE.csv").open("w",newline="",encoding="utf-8") as f:
        clean=[{k:v for k,v in r.items() if k!="_examples"} for r in actual]
        w=csv.DictWriter(f,fieldnames=list(clean[0]));w.writeheader();w.writerows(clean)
    with (outdir/"stage102_source_original_review_queue_15_species_HASH_ONLY.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(preselected[0]));w.writeheader();w.writerows(preselected)
    (outdir/"stage102_original_WFO_lexical_sensitivity_not_precision_report.json").write_text(
        json.dumps(summary,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("STAGE102_AUTHENTIC_WFO_SIZE_GRAMMAR_SENSITIVITY",json.dumps(cohorts,sort_keys=True),flush=True)
    return summary

if __name__=="__main__":
    p=argparse.ArgumentParser()
    for name in ("stage100-original-derived-zip","stage98B-original-geography-zip","original-NHM","original-WCVP",
       "original-China","original-FNA","original-WFO-202606-backbone"):
       p.add_argument("--"+name,required=True,type=Path)
    p.add_argument("--outdir",required=True,type=Path)
    a=p.parse_args()
    run(a.stage100_original_derived_zip,a.stage98B_original_geography_zip,
        a.original_NHM,a.original_WCVP,a.original_China,a.original_FNA,
        a.original_WFO_202606_backbone,a.outdir)
