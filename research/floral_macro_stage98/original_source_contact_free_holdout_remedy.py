#!/usr/bin/env python3
"""Stage98B source-only train-side removal of exact TDWG polygon contacts.

Reads Stage94 original fixed mainland 88/37 split and Stage98A original
pairwise 3256 boundary audits by SHA256. Remove EXPLORATION regions with any
source-original WGS84 polygon contact/overlap to any frozen HOLDOUT region.
Never move a source region between folds or select on climate, floral signal,
bee archive or prediction. Zero contact after pruning does NOT establish
100-km geodesic buffer or lineage/taxon-name independence.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,zipfile
from collections import Counter,defaultdict
from pathlib import Path

STAGE94_GEO_SHA="3475b544d0530e5dfa71b6324f80055d98971d1a3c364309596a381ea025d833"
STAGE98_CONTACT_SHA="aca6a2cd7a97de0c23fa259e391d3725cdbd92d7344b3a43353468f51add5f2c"
STAGE94_MEMBER="stage94_original_mainland_shared_geoblock_split.csv"
STAGE98_MEMBER="stage98_source_exact_contact_region_pairs.csv"
STAGE98_RECEIPT="stage98_original_frozen_holdout_geography_adjacency_receipt.json"

def sha(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):h.update(b)
    return h.hexdigest()

def original_zip_rows(path,digest,member):
    if sha(path)!=digest:raise ValueError("STAGE98B_ORIGINAL_SOURCE_ZIP_SHA_DRIFT")
    with zipfile.ZipFile(path) as z:
        if member not in z.namelist():raise ValueError("STAGE98B_REQUIRED_SOURCE_MEMBER_MISSING")
        return list(csv.DictReader(io.StringIO(z.read(member).decode("utf-8-sig"))))

def derive_contact_pruned_source_split(fold,contact):
    original={r["TDWG_L3"]:r for r in fold}
    if len(original)!=len(fold):
        raise ValueError("STAGE98B_DUPLICATE_MAINLAND_REGION")
    explorer={r["TDWG_L3"] for r in fold if r["shared_split"]=="exploration"}
    holdout={r["TDWG_L3"] for r in fold if r["shared_split"]=="holdout"}
    if explorer&holdout or explorer|holdout!=set(original):
        raise ValueError("STAGE98B_NONEXCLUSIVE_SOURCE_FOLD")
    if any(r["land_scope"]!="mainland" for r in fold):
        raise ValueError("STAGE98B_NONMAINLAND_SOURCE_ENTERED")
    to_remove=set();adjacent=defaultdict(set)
    pairs=set()
    for row in contact:
        t=row["exploration_TDWG_L3"];h=row["holdout_TDWG_L3"]
        if t not in explorer or h not in holdout:
            raise ValueError("STAGE98B_SOURCE_CONTACT_CROSS_FOLD_ID_MISMATCH")
        key=(t,h)
        if key in pairs:raise ValueError("STAGE98B_DUPLICATE_CONTACT_PAIR")
        pairs.add(key)
        if str(row["pair_source_geometry_intersects"]).casefold() not in ("true","1"):
            raise ValueError("STAGE98B_NONCONTACT_WRONGLY_LISTED_AS_CONTACT")
        to_remove.add(t);adjacent[t].add(h)
    train=[{**r,"admission":"exploration_contact_free"}
           for r in fold if r["shared_split"]=="exploration" and r["TDWG_L3"] not in to_remove]
    test=[{**r,"admission":"original_holdout_UNCHANGED"}
          for r in fold if r["shared_split"]=="holdout"]
    removed=[{**original[t],
       "admission":"excluded_exploration_due_to_original_holdout_polygon_contact",
       "contacting_holdout_count":len(adjacent[t]),
       "contacting_holdout_TDWG_codes":"|".join(sorted(adjacent[t]))}
        for t in sorted(to_remove)]
    if any(t in {r["TDWG_L3"] for r in train} for t in to_remove):
        raise ValueError("STAGE98B_SOURCE_CONTACT_EXCLUSION_INCOMPLETE")
    if not set(original)==({r["TDWG_L3"] for r in train}|
                           {r["TDWG_L3"] for r in test}|set(to_remove)):
        raise ValueError("STAGE98B_EXCLUDED_ORIGINAL_REGIONS_UNACCOUNTED")
    if any(r["shared_split"]!="holdout" for r in test):
        raise ValueError("STAGE98B_HOLDOUT_ASSIGNMENT_CHANGED")
    counts={"original_mainland_region_count":len(fold),
       "original_exploration_region_count":len(explorer),
       "original_holdout_region_count":len(holdout),
       "original_train_holdout_source_contact_pairs":len(pairs),
       "source_heldout_regions_touched":len({h for t,h in pairs}),
       "source_exploration_regions_removed_contact":len(to_remove),
       "source_exploration_regions_retained":len(train),
       "source_holdout_regions_retained_UNCHANGED":len(test),
       "source_noncontact_exploration_blocks_retained":len({r["spatial_block_id"] for r in train}),
       "source_holdout_blocks_retained_UNCHANGED":len({r["spatial_block_id"] for r in test}),
       "no_train_polygon_contact_with_any_heldout_region_after_exclusion":True,
       "100km_geodesic_buffer_verified":False,
       "independent_plant_lineages_between_folds_verified":False}
    return train,test,removed,counts

def write_csv(path,rows):
    if not rows:raise ValueError("STAGE98B_NO_SOURCE_RECORDS_FOR_OUTPUT")
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def run(geo_zip,contacts_zip,outdir):
    fold=original_zip_rows(geo_zip,STAGE94_GEO_SHA,STAGE94_MEMBER)
    contact=original_zip_rows(contacts_zip,STAGE98_CONTACT_SHA,STAGE98_MEMBER)
    if len(fold)!=125 or len(contact)!=22:
        raise ValueError("STAGE98B_SOURCE_LOCKED_125_22_COHORT_DRIFT")
    with zipfile.ZipFile(contacts_zip) as z:
        r=json.loads(z.read(STAGE98_RECEIPT))
    previous=r["source_region_counts"]
    if previous["total_train_holdout_region_pairs_evaluated"]!=3256:
        raise ValueError("STAGE98B_3256_ORIGINAL_GEO_PAIRS_NOT_CONFIRMED")
    if previous["intersecting_train_holdout_pairs"]!=len(contact):
        raise ValueError("STAGE98B_ORIGINAL_CONTACT_PAIR_COUNT_NOT_VERIFIED")
    train,test,removed,counts=derive_contact_pruned_source_split(fold,contact)
    if (counts["original_exploration_region_count"]!=88 or
        counts["original_holdout_region_count"]!=37 or
        counts["source_exploration_regions_removed_contact"]!=16 or
        counts["source_exploration_regions_retained"]!=72):
        raise ValueError("STAGE98B_ORIGINAL_GEO_FIXED_88_37_CONTACT_COUNTS_CHANGED")
    outdir.mkdir(parents=True,exist_ok=True)
    write_csv(outdir/"stage98B_train_original_mainland_no_holdout_polygon_contact_72.csv",train)
    write_csv(outdir/"stage98B_holdout_original_mainland_37_UNCHANGED.csv",test)
    write_csv(outdir/"stage98B_excluded_original_exploration_16_contacting_holdout.csv",removed)
    result={
       "schema":"stage98B_source_original_TDWG3_geometry_contact_free_train_ONLY",
       "original_source_artifact_sha256":{"stage94":STAGE94_GEO_SHA,"stage98A":STAGE98_CONTACT_SHA},
       "source_cohorts":counts,
       "source_split_membership_never_reassigned":True,
       "only_source_geography_consulted":True,
       "no_climate_flower_trait_or_GBIF_outcome_opened":True,
       "not_a_validated_100km_buffer":True,
       "regional_botanical_species_names_can_repeat_across_folds":True,
       "no_causal_wind_flower_claim_estimated":True
    }
    (outdir/"stage98B_source_contact_free_exploration_holdout_receipt.json").write_text(
        json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True)+"\n")
    print("STAGE98B_ORIGINAL_SOURCE_CONTACT_FREE_MAINLAND_TRAINING",
          json.dumps(counts,sort_keys=True),flush=True)
    return result

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--stage94-original-geo-zip",required=True,type=Path)
    p.add_argument("--stage98A-original-boundary-zip",required=True,type=Path)
    p.add_argument("--outdir",required=True,type=Path)
    a=p.parse_args()
    run(a.stage94_original_geo_zip,a.stage98A_original_boundary_zip,a.outdir)
