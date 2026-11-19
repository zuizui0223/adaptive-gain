#!/usr/bin/env python3
"""Stage99 exact-species and trait-source reuse across 72 mainland train /37 holdout.

Original source-only identity audit, NOT a floral-wind ecological regression.
Read actual original WCVP accepted native regions + NHM botanical-text marks
+ AusTraits source-labeled flower diameter + WFO full-flora floral scent lexical
prose + GIFT independent pollen mode, and source-frozen Stage98B geometry-only
contact removal.  Never identify repeated identical species as independent
evolved phenotypes.  Original data sources must have pinned byte hashes.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,sys,zipfile
from collections import Counter
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
for name in ("floral_macro_stage87","floral_macro_stage88",
             "floral_macro_stage89","floral_macro_stage91","floral_macro_stage92"):
    sys.path.insert(0,str(BASE/name))
from global_native_floral_signal_tdwg3 import load_nhm,wcvp_regions,NHM_SHA,WCVP_SHA
from real_three_cue_preflight import source_rows
from austraits7_flower_diameter_source_audit import parse_original_austraits_zip
from gift32_independent_pollen_mode_global_native_coverage import original_gift_species

STAGE98B_SHA="8026b800672cad2afd97e2fe416349cc3aca8f650e78ae8c001dd31de104c8b7"
WFO_SPP_SHA="eb32786c6464a6edecd7ff0d12e61762cdb107f3082124066aadcc03292dd88e"
ORIGINAL_HOLDOUT="stage98B_holdout_original_mainland_37_UNCHANGED.csv"
CONTACT_FREE_TRAIN="stage98B_train_original_mainland_no_holdout_polygon_contact_72.csv"
REMOVED_TRAIN="stage98B_excluded_original_exploration_16_contacting_holdout.csv"
WFO_MEMBER="stage93_derived/stage93_original_WFO_species_fragrance_lexical_states_NOT_VOC.csv"

def sha256(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):
            h.update(b)
    return h.hexdigest()

def original_tdwg_fold_ids(source):
    if sha256(source)!=STAGE98B_SHA:
        raise ValueError("STAGE99_72_37_SOURCE_GEOGRAPHIC_ZIP_SHA_MISMATCH")
    with zipfile.ZipFile(source) as z:
        def rows(name):
            return list(csv.DictReader(io.StringIO(z.read(name).decode("utf-8-sig"))))
        t=rows(CONTACT_FREE_TRAIN);h=rows(ORIGINAL_HOLDOUT);ex=rows(REMOVED_TRAIN)
    a={r["TDWG_L3"] for r in t}
    b={r["TDWG_L3"] for r in h}
    c={r["TDWG_L3"] for r in ex}
    if len(a)!=72 or len(b)!=37 or len(c)!=16 or a&b or a&c or b&c:
        raise ValueError("STAGE99_SOURCE_FOLD_NOT_72_37_EXCLUDED16")
    if any(r["shared_split"]!="exploration" or r["land_scope"]!="mainland" for r in t):
        raise ValueError("STAGE99_TRAIN_NOT_STRICT_MAINLAND")
    if any(r["shared_split"]!="holdout" or r["land_scope"]!="mainland" for r in h):
        raise ValueError("STAGE99_TEST_NOT_ORIGINAL_HOLDOUT")
    return a,b,c

def load_original_WFO_source_positive_and_negatives(wfo_zip,allowed_species):
    if sha256(wfo_zip)!=WFO_SPP_SHA:
        raise ValueError("STAGE99_WFO_ORIGINAL_SPECIES_SOURCE_SHA_MISMATCH")
    with zipfile.ZipFile(wfo_zip) as z:
        if WFO_MEMBER not in z.namelist():
            raise ValueError("STAGE99_WFO_SOURCE_SPECIES_MEMBER_MISSING")
        rows=list(csv.DictReader(io.StringIO(z.read(WFO_MEMBER).decode("utf-8-sig"))))
    if len(rows)!=27899:
        raise ValueError("STAGE99_ORIGINAL_WFO_FLORA_27899_SOURCE_DRIFT")
    names=set();a=set();b=set();other=0
    for r in rows:
        key=r["accepted_species"].casefold().strip()
        if not key or key in names or key not in allowed_species:
            raise ValueError("STAGE99_WFO_NOT_EXACT_ACCEPTED_SOURCE_NAME")
        names.add(key)
        state=r["source_flora_lexical_fragrance_state"]
        if state=="positive_candidate":a.add(key)
        elif state=="explicit_negative_candidate":b.add(key)
        elif state=="unmentioned_or_uncertain":other+=1
        else:raise ValueError("STAGE99_UNEXPECTED_WFO_SOURCE_FLORAL_SCENT_STATE")
    if (len(a),len(b),other)!=(420,105,27374):
        raise ValueError("STAGE99_WFO_SCENT_ORIGINAL_SOURCE_STATE_MARGINS_CHANGED")
    return a,b,{"full_original_description_taxa":len(rows),
         "floral_scent_source_positive":len(a),"floral_scent_explicit_negative":len(b),
         "floral_scent_unmentioned_never_negative":other}

def novelty_report(train_native,holdout_native,traits):
    train=set(train_native)&traits
    hold=set(holdout_native)&traits
    both=train&hold
    novel=hold-train
    return {
      "source_total_globally_recognized_trait_species":len(traits),
      "distinct_source_species_in_contact_free_72train":len(train),
      "distinct_source_species_in_fixed_37holdout":len(hold),
      "distinct_exact_species_shared_train_and_holdout":len(both),
      "distinct_exact_species_new_only_in_holdout":len(novel),
      "holdout_exact_species_reuse_fraction":len(both)/len(hold) if hold else None,
      "holdout_new_species_fraction":len(novel)/len(hold) if hold else None,
      "distinct_holdout_genera_total":len({s.split()[0] for s in hold}),
      "distinct_holdout_genera_containing_new_species":len({s.split()[0] for s in novel}),
      "distinct_holdout_genera_absent_in_training":len(
          {s.split()[0] for s in hold}-{s.split()[0] for s in train}),
      "original_species_identity_holdout_NOT_phylogenetic_independence":True,
    }

def source_region_holdout_novelty(native,hold_codes,train_native,traits_by_channel):
    rows=[]
    for code in sorted(hold_codes):
        row={"TDWG_L3":code,"original_shared_spatial_fold":"holdout",
             "source_exact_native_species":len(native[code]),
             "source_new_native_species_not_in_72train":len(native[code]-train_native)}
        for label,trait in traits_by_channel.items():
            native_trait=native[code]&trait
            novel=native_trait-train_native
            row[label+"_source_trait_species"]=len(native_trait)
            row[label+"_novel_trait_species_not_in_72train"]=len(novel)
            row[label+"_novel_fraction"]=len(novel)/len(native_trait) if native_trait else ""
        row["this_is_source_identity_support_not_species_independent_fitness"]="YES"
        rows.append(row)
    return rows

def run(stage98B_zip,nhm_file,wcvp_file,gift_zip,austraits_zip,wfo_zip,outdir):
    train_codes,hold_codes,removed_codes=original_tdwg_fold_ids(stage98B_zip)
    traits,nhm_qc=load_nhm(nhm_file)
    native,wcvp_qc=wcvp_regions(wcvp_file,traits)
    universe=set().union(*native.values())
    if len(native)!=367 or len(universe)!=55775:
        raise ValueError("STAGE99_ORIGINAL_WCVP_NHM_ACCEPTED_NATIVE_COHORT_CHANGED")
    if not (train_codes|hold_codes|removed_codes)<=set(native):
        raise ValueError("STAGE99_TRUE_WCVP_SOURCE_GEO_CODE_JOIN_MISSING")
    train_native=set().union(*(native[x] for x in train_codes))
    hold_native=set().union(*(native[x] for x in hold_codes))
    removed_native=set().union(*(native[x] for x in removed_codes))
    markings,_headers,_dia=source_rows(nhm_file,set(traits))
    marks={sp for sp,(state,width) in markings.items()
           if state=="positive_lexical" and sp in universe}
    if len(marks)!=906:
        raise ValueError("STAGE99_ORIGINAL_POSITIVE_ONLY_906_MARKING_SOURCE_CHANGED")
    animal_modes,giftmeta=original_gift_species(gift_zip)
    modes={m:set() for m in ("animal","wind")}
    for sp in universe:
        v=animal_modes.get(sp)
        if v in modes:modes[v].add(sp)
    if (len(modes["animal"]),len(modes["wind"]))!=(2560,612):
        raise ValueError("STAGE99_GIFT_SOURCE_ANIMAL_WIND_COHORT_CHANGED")
    measured,ausmeta=parse_original_austraits_zip(austraits_zip,universe)
    size=set(measured)
    if len(size)!=104:
        raise ValueError("STAGE99_ORIGINAL_AUSTRAITS_104_DIAMETERS_CHANGED")
    scent_pos,scent_neg,wfo_meta=load_original_WFO_source_positive_and_negatives(
         wfo_zip,universe)
    groups={
       "all_native_species":universe,
       "reported_marking_lexical_positive_not_true_guide":marks,
       "source_measured_flower_diameter":size,
       "WFO_floral_scent_lexical_positive":scent_pos,
       "WFO_floral_scent_explicit_negative":scent_neg,
       "GIFT_qualified_animal_pollination":modes["animal"],
       "GIFT_qualified_wind_pollination":modes["wind"],
    }
    report={k:novelty_report(train_native,hold_native,v) for k,v in groups.items()}
    regional=source_region_holdout_novelty(native,hold_codes,train_native,groups)
    receipt={
      "schema":"stage99_original_source_72train_37holdout_species_identity_recurrence",
      "source_original_GitHub_stage98B_SHA256":STAGE98B_SHA,
      "source_original_WFO_species_artifact_SHA256":WFO_SPP_SHA,
      "source_original_NHM_SHA256":NHM_SHA,
      "source_original_WCVP_SHA256":WCVP_SHA,
      "source_original_GIFT_SHA256":giftmeta.get("archive_sha256"),
      "source_original_AusTraits7_SHA256":ausmeta.get("authentic_zipped_source_sha256"),
      "original_native_plant_universe":len(universe),
      "source_original_contact_free_train_regions":len(train_codes),
      "source_original_holdout_regions":len(hold_codes),
      "source_original_excluded_train_regions":len(removed_codes),
      "source_trait_categories_source_only":report,
      "source_original_wfo_scent_lexical_coding":wfo_meta,
      "repeated_species_native_area_records_are_NOT_independent_evolution":True,
      "heldout_region_identity_does_NOT_imply_heldout_species_identity":True,
      "no_actual_wind_cue_association_fitted":True,
      "no_source_trait_fitness_or_receptor_data":True,
      "training_source_geo_contact_excluded_but_100km_buffer_not_verified":True,
      "no_phylogenetic_independent_lineages_inferred":True,
    }
    outdir.mkdir(parents=True,exist_ok=True)
    with (outdir/"stage99_original_37holdout_region_trait_identity_novelty_counts.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(regional[0]));w.writeheader();w.writerows(regional)
    (outdir/"stage99_original_mainland_three_cue_shared_species_source_receipt.json").write_text(
         json.dumps(receipt,indent=2,sort_keys=True)+"\n")
    print("STAGE99_TRUE_ORIGINAL_SOURCE_TRAIN_HOLDOUT_TRAIT_SPECIES_REUSE",
          json.dumps(report,sort_keys=True),flush=True)
    return receipt

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--stage98B-contact-free-source-zip",required=True,type=Path)
    p.add_argument("--original-NHM",required=True,type=Path)
    p.add_argument("--original-WCVP",required=True,type=Path)
    p.add_argument("--original-GIFT",required=True,type=Path)
    p.add_argument("--original-AusTraits7",required=True,type=Path)
    p.add_argument("--original-WFO-scent-species-zip",required=True,type=Path)
    p.add_argument("--outdir",required=True,type=Path)
    a=p.parse_args()
    run(a.stage98B_contact_free_source_zip,a.original_NHM,a.original_WCVP,
        a.original_GIFT,a.original_AusTraits7,a.original_WFO_scent_species_zip,a.outdir)
