"""Stage53: source-authentic KEW WCVP species name/synonym -> native L3.

Read official 2026 Kew WCVP (original zip pinned SHA-256), correlate
original 2016 Koski/Ashman UV-phototyped *taxon* names with source-
accepted Kew taxon concepts, and retain only non-doubtful extant native
WGSRPD Level-3 botanical AREAS. Distinct from ISO/political countries,
fine-scale native population occupancy, UV measurement voucher locality
and Bombus occurrence.

2016 botanical source original 177 Table S2 taxon rows, 164 original
GBIF matched rows → 159 GBIF accepted species with original UV binary.
NO fuzzy name match, no forced GBIF=WCVP synonym equivalence, no
automatic accepted-species trait generalization where taxonomy conflicts.
"""
from __future__ import annotations
from collections import Counter,defaultdict
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import tempfile
import urllib.request
import zipfile

URL="https://sftp.kew.org/pub/data-repositories/WCVP/wcvp.zip"
PIN_SHA256="d32ea2b3a85e489b14e83bcc9eae7274532e1d113753f7be290d4b2dfde573fa"
MAX_ZIP_BYTES=155_000_000
EXPECTED_SOURCE_ROWS=177
EXPECTED_MAPPED=164
EXPECTED_ACCEPTED=159
NAMES_HEADER=("plant_name_id","ipni_id","taxon_rank","taxon_status",
              "family","genus_hybrid","genus","species_hybrid","species")
DIST_HEADER=("plant_locality_id","plant_name_id","continent_code_l1",
             "continent","region_code_l2","region","area_code_l3","area",
             "introduced","extinct","location_doubtful")


def _norm_name(s):
    return " ".join(str(s or "").strip().casefold().split())


def source_species(rows,expected=EXPECTED_SOURCE_ROWS):
    if len(rows)!=expected:
        raise ValueError("NO_GO_2016_PHENOTYPED_ORIGINAL_DENOMINATOR")
    bykey=defaultdict(list)
    for row in rows:
        if row.get("accepted_GBIF_species_match_status")!="EXACT_CONFIDENT_SPECIES_MAPPED":
            continue
        key=row.get("accepted_GBIF_taxon_key_or_empty","")
        name=row.get("original_S1_author_full_binomial_candidate","")
        code=row.get("source_measured_UV_pattern_present")
        if not key.isdigit() or not _norm_name(name) or code not in ("0","1"):
            raise ValueError("NO_GO_ORIGINAL_2016_GBIF_SOURCE_QUALITY")
        bykey[key].append(row)
    if expected==EXPECTED_SOURCE_ROWS:
        if len(bykey)!=EXPECTED_ACCEPTED or sum(map(len,bykey.values()))!=EXPECTED_MAPPED:
            raise ValueError("NO_GO_2016_ACCEPTED_159_OR_SOURCE_164_CHANGED")
    merged={}
    for key,originals in bykey.items():
        states={r["source_measured_UV_pattern_present"] for r in originals}
        if len(states)!=1:
            raise ValueError("NO_GO_SOURCE_INFRASPECIFIC_UV_CONFLICT")
        merged[key]={
          "gbif_accepted_species_key":key,
          "source_exact_binomial_candidates":sorted({
             _norm_name(r["original_S1_author_full_binomial_candidate"])
             for r in originals}),
          "source_original_taxon_units":len(originals),
          "original_UV_spatial_pattern_binary":int(next(iter(states))),
          "original_article_doi":"10.1111/nph.13921",
          "original_flower_specimen_native_location_unknown":True
        }
    return merged


def _rows(z,member):
    with z.open(member) as raw:
        t=io.TextIOWrapper(raw,encoding="utf-8-sig",newline="")
        reader=csv.DictReader(t,delimiter="|")
        yield reader.fieldnames
        for row in reader:
            yield row


def source_members(z):
    m={}
    for kind in ("wcvp_names.csv","wcvp_distribution.csv"):
        names=[x.filename for x in z.infolist() if Path(x.filename).name==kind]
        if len(names)!=1:
            raise ValueError("NO_GO_MISSING_OR_AMBIGUOUS_WCVP_"+kind)
        m[kind]=names[0]
    return m


def _accepted(row):
    status=str(row.get("taxon_status") or "").strip().lower()
    ident=(row.get("plant_name_id") or "").strip()
    accepted=(row.get("accepted_plant_name_id") or "").strip()
    if not ident.isdigit():
        return None
    if status=="accepted":
        return ident
    if status in ("synonym","homotypic synonym","heterotypic synonym"):
        return accepted if accepted.isdigit() else None
    return None


def resolve_names(z,original,table):
    targets={n for source in original.values()
             for n in source["source_exact_binomial_candidates"]}
    found=defaultdict(set)
    names_seen=0
    headers=next(_rows(z,table))
    if not set(NAMES_HEADER).issubset(headers or []):
        raise ValueError("NO_GO_WCVP_NAMES_SCHEMA_CHANGED")
    for r in _rows(z,table):
        if isinstance(r,list):continue
        names_seen+=1
        if r.get("family")!="Rosaceae" or (r.get("taxon_rank") or "").lower()!="species":
            continue
        if r.get("genus_hybrid") or r.get("species_hybrid"):
            continue
        text=_norm_name(str(r.get("genus") or "")+" "+str(r.get("species") or ""))
        if text not in targets:continue
        accepted=_accepted(r)
        if accepted is not None:
            found[text].add(accepted)
    matches={}
    for key,s in original.items():
        sets=[found.get(name,set()) for name in s["source_exact_binomial_candidates"]]
        all_ids=set().union(*sets)
        if not all_ids:
            status="NO_EXACT_WCVP_ACCEPTED_OR_SYNONYM_NAME"
            accepted=""
        elif len(all_ids)>1:
            status="MULTIPLE_WCVP_ACCEPTED_CONCEPTS_NO_AUTO_RECONCILIATION"
            accepted=""
        else:
            status="EXACT_AUTHOR_GENUS_SPECIES_SINGLE_WCVP_ACCEPTED_CONCEPT"
            accepted=next(iter(all_ids))
        matches[key]={
          **s,"WCVP_accepted_plant_name_id_or_unknown":accepted,
          "WCVP_match_status":status,
          "n_distinct_WCVP_accepted_concept_candidates":len(all_ids),
          "WCVP_taxonomic_concept_not_equivalent_to_GBIF_without_validation":True
        }
    return matches,names_seen


def all_name_ids_for_accepted(z,table,accepted_ids):
    """Allow distributions attached to accepted names or their synonyms."""
    mapped={}
    accepted_name={}
    for r in _rows(z,table):
        if isinstance(r,list):continue
        resolved=_accepted(r)
        ident=(r.get("plant_name_id") or "").strip()
        if resolved not in accepted_ids or not ident.isdigit():
            continue
        mapped[ident]=resolved
        if ident==resolved:
            accepted_name[resolved]=r.get("taxon_name") or (
               (r.get("genus") or "")+" "+(r.get("species") or ""))
    return mapped,accepted_name


def _region_status(row):
    introduced=row.get("introduced","")
    extinct=row.get("extinct","")
    doubtful=row.get("location_doubtful","")
    if introduced not in ("0","1") or extinct not in ("0","1") or doubtful not in ("0","1"):
        return "UNRESOLVED_INVALID_SOURCE_STATUS"
    if extinct=="1":return "EXTINCT_REGION_NOT_CURRENT_NATIVE"
    if doubtful=="1":return "DOUBTFUL_REGION_NOT_CONFIRMED_NATIVE"
    return "NATIVE" if introduced=="0" else "INTRODUCED"


def native_regions(z,table,idmap,accepted_ids):
    headers=next(_rows(z,table))
    if not set(DIST_HEADER).issubset(headers or []):
        raise ValueError("NO_GO_WCVP_DISTRIBUTION_SCHEMA_CHANGED")
    areas=defaultdict(lambda:defaultdict(set))
    n_seen=0
    n_source_matched=0
    for r in _rows(z,table):
        if isinstance(r,list):continue
        n_seen+=1
        accepted=idmap.get(r.get("plant_name_id",""))
        if accepted not in accepted_ids:continue
        n_source_matched+=1
        region=(r.get("area_code_l3") or "").strip()
        if len(region)!=3 or not region.isalpha():
            continue
        areas[accepted][region].add(_region_status(r))
    output={}
    for key in accepted_ids:
        native=[]
        introduced=[]
        conflicts=[]
        other=[]
        for area,values in sorted(areas.get(key,{}).items()):
            if "NATIVE" in values and "INTRODUCED" in values:
                conflicts.append(area)
            elif values=={"NATIVE"}:
                native.append(area)
            elif values=={"INTRODUCED"}:
                introduced.append(area)
            else:
                other.append(area)
        output[key]={
          "WCVP_confirmed_native_extant_WGSRPD_L3_areas":native,
          "WCVP_introduced_extant_WGSRPD_L3_areas":introduced,
          "WCVP_conflicting_WGSRPD_L3_areas_excluded":conflicts,
          "WCVP_doubtful_extinct_or_unknown_WGSRPD_L3_areas":other,
          "WCVP_native_status_not_validated_per_GBIF_occurrence":True
        }
    return output,n_seen,n_source_matched


def process(original,z):
    mapping,names_rows=resolve_names(z,original,source_members(z)["wcvp_names.csv"])
    chosen_ids={r["WCVP_accepted_plant_name_id_or_unknown"] for r in mapping.values()
                if r["WCVP_accepted_plant_name_id_or_unknown"]}
    nameids,accepted_names=all_name_ids_for_accepted(
        z,source_members(z)["wcvp_names.csv"],chosen_ids)
    ranges,distribution_rows,matched_dist_rows=native_regions(
        z,source_members(z)["wcvp_distribution.csv"],nameids,chosen_ids)
    output=[]
    for species in original:
        row=mapping[species]
        ident=row["WCVP_accepted_plant_name_id_or_unknown"]
        ranges_row=ranges.get(ident,{
          "WCVP_confirmed_native_extant_WGSRPD_L3_areas":[],
          "WCVP_introduced_extant_WGSRPD_L3_areas":[],
          "WCVP_conflicting_WGSRPD_L3_areas_excluded":[],
          "WCVP_doubtful_extinct_or_unknown_WGSRPD_L3_areas":[],
          "WCVP_native_status_not_validated_per_GBIF_occurrence":True
        })
        output.append({**row,**ranges_row,
                       "WCVP_accepted_name_or_unknown":accepted_names.get(ident,"")})
    counts=Counter(r["WCVP_match_status"] for r in output)
    return output,{
       "status":"OFFICIAL_KEW_WCVP_2016_UV_SPECIES_NATIVE_BOTANICAL_AREAS",
       "n_original_2016_GBIF_accepted_UV_species":len(original),
       "n_WCVP_taxonomic_match_exact_to_single_accepted_concept":counts[
          "EXACT_AUTHOR_GENUS_SPECIES_SINGLE_WCVP_ACCEPTED_CONCEPT"],
       "WCVP_taxonomic_source_match_statuses":dict(sorted(counts.items())),
       "n_species_with_at_least_one_confirmed_WCVP_native_extant_L3_area":sum(
          bool(r["WCVP_confirmed_native_extant_WGSRPD_L3_areas"]) for r in output),
       "n_species_with_at_least_three_WCVP_native_extant_L3_areas":sum(
          len(r["WCVP_confirmed_native_extant_WGSRPD_L3_areas"])>=3 for r in output),
       "n_species_with_conflicting_WCVP_native_introduced_L3_area":sum(
          bool(r["WCVP_conflicting_WGSRPD_L3_areas_excluded"]) for r in output),
       "WCVP_names_original_rows_scanned":names_rows,
       "WCVP_distribution_original_rows_scanned":distribution_rows,
       "WCVP_distribution_records_joined_to_target_accepted_ids":matched_dist_rows,
       "WCVP_source_distinct_accepted_concepts_for_original_names":len(chosen_ids),
       "native_area_is_TDWG_WGSRPD_L3_not_ISO_or_source_specimen_point":True,
       "source_species_original_UV_phenotype_measurement_location_unknown":True,
       "source_native_region_does_not_verify_plant_present_every_hex":True,
       "no_modelled_Bombus_UV_pattern_effect_yet":True
    }


def acquire_zip():
    tmp=tempfile.TemporaryDirectory()
    dest=Path(tmp.name)/"wcvp-original.zip"
    h=hashlib.sha256()
    length=0
    req=urllib.request.Request(URL,headers={
       "Accept":"application/zip,*/*",
       "User-Agent":"adaptive-gain-floral-native-areas-stage53/2026"
    })
    with urllib.request.urlopen(req,timeout=90) as response, dest.open("wb") as output:
        while True:
            block=response.read(2*1024*1024)
            if not block:break
            length+=len(block)
            if length>MAX_ZIP_BYTES:
                raise ValueError("NO_GO_WCVP_DOWNLOAD_EXCEEDS_EXPECTED_SIZE")
            h.update(block)
            output.write(block)
    if h.hexdigest()!=PIN_SHA256 or not zipfile.is_zipfile(dest):
        tmp.cleanup()
        raise ValueError("NO_GO_OFFICIAL_WCVP_SOURCE_ZIP_DRIFT")
    return tmp,dest,length


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source-original-2016-177",required=True)
    args=p.parse_args()
    with Path(args.source_original_2016_177).open(encoding="utf8",newline="") as f:
        source=list(csv.DictReader(f))
    original=source_species(source)
    tmp,path,original_bytes=acquire_zip()
    try:
        with zipfile.ZipFile(path) as z:
            output,report=process(original,z)
    finally:
        tmp.cleanup()
    report["original_WCVP_zip_SHA256_verified"]=PIN_SHA256
    report["original_WCVP_zip_bytes"]=original_bytes
    d=Path("stage53_wcvp_native_ranges")
    d.mkdir(exist_ok=True)
    flat=[]
    for r in output:
        flat.append({k:json.dumps(v,ensure_ascii=False,sort_keys=True)
                     if isinstance(v,(list,dict)) else v for k,v in r.items()})
    with (d/"original_159_UV_plants_KEW_WCVP_native_TDWG_L3.csv").open(
        "w",encoding="utf8",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=list(flat[0]))
        wr.writeheader();wr.writerows(flat)
    (d/"original_Kew_WCVP_nativity_159_species_source_receipt.json").write_text(
       json.dumps(report,indent=2,ensure_ascii=False,sort_keys=True)+"\n",encoding="utf8")
    print("STAGE53_REAL_KEW_WCVP_2016_UV_NATIVE_SOURCE_COVERAGE",
          json.dumps(report,ensure_ascii=False,sort_keys=True))
    print("NO_NATIVE_RANGE_OR_UV_PHENOTYPED_LOCALITY_AT_INDIVIDUAL_BEE_HEX_LEVEL")


if __name__=="__main__":
    main()
