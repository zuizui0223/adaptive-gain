"""Stage71A corrected EuPPollNet flower-count audit (original source; no photos).

Never assume 'Flower_data=Yes' guarantees a positive, comparable flower count,
or that author Flower_data_merger alone is globally unique. Inspect original
Study_id + Flower_data_merger keys and units before any density adjustment.

This module is coverage and source-quality audit only, no association fitted.
"""
from __future__ import annotations
import argparse,csv,gzip,hashlib,io,json,math,urllib.request
from pathlib import Path
from collections import Counter,defaultdict

BASE="https://raw.githubusercontent.com/joseblanuza/EuPPollNet/v1.3.0/Data/3_Final_data/"
FLOWER_NAME="Flower_counts.csv"
FLOWER_SIZE=20315455
FLOWER_GIT_SHA="8543e446a53f3b7cffece76e1699489e7169f7fd"
NETWORK_NAME="Interaction_data.csv.gz"
NETWORK_GIT_SHA="6e639d4af81feee76eefa6804622f8b901c39feb"
NETWORK_SIZE=2374060
ORIGINAL_VISIT_ROWS=623476

def gitblob(b):
    return hashlib.sha1(f"blob {len(b)}\0".encode("ascii")+b).hexdigest()

def fetch(name):
    expected={FLOWER_NAME:(FLOWER_SIZE,FLOWER_GIT_SHA),
              NETWORK_NAME:(NETWORK_SIZE,NETWORK_GIT_SHA)}
    if name not in expected:raise ValueError("STAGE71A_UNREGISTERED_ORIGINAL_SOURCE_FILE")
    n,sha=expected[name]
    request=urllib.request.Request(BASE+name,headers={"User-Agent":"adaptive-gain-original-source-flower-count-audit/2026-11-17"})
    with urllib.request.urlopen(request,timeout=180) as s:b=s.read(n+1)
    if len(b)!=n or gitblob(b)!=sha:raise ValueError("STAGE71A_SOURCE_BYTES_OR_GIT_DIGEST_CHANGED")
    return b

def rows(raw,compressed=False):
    source=io.BytesIO(raw)
    if compressed:source=gzip.GzipFile(fileobj=source)
    with io.TextIOWrapper(source,encoding="utf-8-sig",errors="replace",newline="") as f:
        reader=csv.DictReader(f)
        names=list(reader.fieldnames or [])
        for r in reader:
            if None in r:raise ValueError("STAGE71A_CSV_OVERFLOW_COLUMNS")
            yield names,r

def valid_key(v):
    s=str(v or "").strip()
    return s if s and s.casefold() not in {"na","nan","none","null","missing"} else ""

def numeric(v):
    s=str(v or "").strip()
    if not s or s.casefold() in {"na","nan","none","null"}:return None
    try:f=float(s)
    except ValueError:return None
    return f if math.isfinite(f) and f>=0 else None

def safe_join_key(study,key):
    k=valid_key(key);st=valid_key(study)
    return (st,k) if k and st else None

def audit(original_flower, original_visits, original_network_units):
    counts=Counter();units=Counter();source_metadata=Counter()
    original_keys=defaultdict(list)
    example_headers=None
    multi_nonidentical=Counter()
    all_flower_rows=[]
    for headers,r in rows(original_flower):
        if example_headers is None:example_headers=headers
        counts["flower_rows"]+=1
        for need in ("Study_id","Network_id","Flower_data_merger","Flower_count","Units"):
            if need not in r:raise ValueError("STAGE71A_ORIGINAL_FLOWER_HEADER_MISSING_"+need)
        k=safe_join_key(r["Study_id"],r["Flower_data_merger"])
        value=numeric(r["Flower_count"]); rawunit=valid_key(r.get("Units"))
        source_metadata[r["Study_id"]]+=1
        units[rawunit or "UNKNOWN"]+=1
        if k:
            original_keys[k].append((value,rawunit,r.get("Plant_species",""),r.get("Network_id",""),r.get("Flower_count","")))
            counts["flower_rows_with_usable_join_key"]+=1
        else:counts["flower_rows_without_source_join_key"]+=1
        if value is None:counts["flower_rows_missing_or_invalid_numeric_count"]+=1
        elif value==0:counts["flower_rows_reported_zero_count"]+=1
        else:counts["flower_rows_with_positive_count"]+=1
        if "\ufffd" in " ".join((r.get("Plant_species",""),r.get("Units",""))):
            counts["flower_rows_with_decoding_uncertainty"]+=1
    if counts["flower_rows"]==0:raise ValueError("STAGE71A_ORIGINAL_FLOWER_SOURCE_EMPTY")
    bystudy=Counter(k[0] for k in original_keys)
    key_multiplicity=Counter(len(v) for v in original_keys.values())
    safe_values={}
    for k,records in original_keys.items():
        # Even multiple equal records may represent different sampling units.
        # Only one exact original source count per key is unambiguous.
        if len(records)==1:
            value, unit, species, network, original=records[0]
            if value is not None and value>0 and unit:
                safe_values[k]=(value,unit,species,network)
                counts["flower_keys_single_positive_numeric_with_explicit_unit"]+=1
        else:
            if len(set((r[0],r[1],r[2]) for r in records))>1:
                multi_nonidentical[k[0]]+=1
    target={}
    for row in original_network_units:
        if row["Stage67_direct_petal_spectra_name_match"]!="1":continue
        pk=(row["Study_id"],row["Network_id"],row["Year_from_original_date"],
            row["Original_plant_accepted_name_literal"].casefold())
        if pk in target:raise ValueError("STAGE71A_STAGE69_SPECTRAL_DUPLICATE_NETWORK_PLANT_UNIT")
        target[pk]={"keys":set(),"raw_flags":set(),"visit_records":0,
                    "missing_join_rows":0,"explicit_keys":0}
    if len(target)!=2557:raise ValueError("STAGE71A_ORIGINAL_2557_SPECTRAL_PLANT_UNITS_CHANGED")
    n_record=0
    observed_link_keys=set()
    all_join_key_flags=Counter()
    key_to_names=defaultdict(set)
    for headers,r in rows(original_visits,compressed=True):
        n_record+=1
        all_join_key_flags[valid_key(r.get("Flower_data")) or "UNKNOWN"]+=1
        pk=(r["Study_id"],r["Network_id"],(r["Date"] or "")[:4],
            r["Plant_accepted_name"].strip().casefold())
        k=safe_join_key(r.get("Study_id"),r.get("Flower_data_merger"))
        if k and pk in target:
            key_to_names[k].add(pk[3])
        if pk not in target:continue
        z=target[pk];z["visit_records"]+=1
        z["raw_flags"].add(valid_key(r.get("Flower_data")) or "UNKNOWN")
        if k:
            z["keys"].add(k)
            observed_link_keys.add(k)
        else:
            z["missing_join_rows"]+=1
    if n_record!=ORIGINAL_VISIT_ROWS:
        raise ValueError("STAGE71A_NOT_CORRECTED_623476_VISITS")
    # Source key matching across distinct original plant accepted names can lead
    # to deterministic cross-species count leakage: always reject such keys.
    ambiguous_species_keys={k for k,v in key_to_names.items() if len(v)>1}
    summary_rows=[]
    counts["spectral_network_plant_units"]=len(target)
    studies_with_safe=set();taxa_with_safe=set()
    for pk,z in sorted(target.items()):
        keyset=z["keys"]
        candidate=[k for k in keyset if k in safe_values and k not in ambiguous_species_keys]
        # A plant×network unit may have multiple dates and source flower-count keys.
        # Do not average/weight independent visits without matching date and census.
        single_exact=len(keyset)==1 and len(candidate)==1 and z["missing_join_rows"]==0
        multi_date=len(keyset)>1
        if not keyset:label="NO_ORIGINAL_LINK_KEY"
        elif len(keyset)>1:label="MULTIPLE_SOURCE_COUNT_KEYS_NEEDS_TIME_ALIGNMENT"
        elif keyset & ambiguous_species_keys:label="SOURCE_KEY_SHARED_ACROSS_MULTIPLE_PLANT_SPECIES"
        elif len(candidate)!=1:label="COUNT_NOT_SINGLE_VALID_POSITIVE_VALUE_WITH_UNIT"
        elif z["missing_join_rows"]:label="PARTIAL_MISSING_ORIGINAL_VISIT_LINK"
        else:label="ONE_ORIGINAL_POSITIVE_COUNT_UNIT_PRESENT_NOT_FIELD_COMPARABLE"
        counts["spectral_units_"+label]+=1
        if single_exact:
            studies_with_safe.add(pk[0]);taxa_with_safe.add(pk[3])
        num,unit=(safe_values[candidate[0]][:2] if single_exact else ("",""))
        summary_rows.append({
           "Study_id":pk[0],"Network_id":pk[1],"Year":pk[2],
           "Original_plant_accepted_name":pk[3],
           "original_visit_rows":z["visit_records"],
           "source_flower_data_flags":"|".join(sorted(z["raw_flags"])),
           "n_distinct_source_flower_merger_keys":len(keyset),
           "missing_linked_source_visit_rows":z["missing_join_rows"],
           "flower_census_coverage_class":label,
           "source_census_usable_single_key_numeric_positive":int(single_exact),
           "original_flower_count_value_only_if_unambiguous":num,
           "original_flower_count_unit_only_if_unambiguous":unit,
           "usable_for_field_per_flower_visitation_RATE":0
        })
    summary={
      "schema":"stage71a_source_authenticated_EuPPollNet_v130_original_flower_census_semantics",
      "source_original_author_release":"joseblanuza/EuPPollNet@v1.3.0",
      "source_flower_csv_Git_blob_SHA1":FLOWER_GIT_SHA,
      "source_flower_csv_sha256":hashlib.sha256(original_flower).hexdigest(),
      "source_visit_csv_gz_Git_blob_SHA1":NETWORK_GIT_SHA,
      "original_623476_visit_records":n_record,
      "original_flower_count_source_columns":example_headers,
      "original_flower_count_source_nrows":counts["flower_rows"],
      "original_flower_count_valid_key_count":len(original_keys),
      "flower_count_source_key_multiplicity_histogram":dict(sorted(key_multiplicity.items())),
      "original_flower_count_distinct_studies":len(source_metadata),
      "original_flower_count_unit_counts":dict(units.most_common()),
      "flower_count_key_collision_with_multiple_target_plant_names":len(ambiguous_species_keys),
      "spectral_plant_network_year_units":len(target),
      "spectral_plant_network_year_coverage_classes":{
           k.removeprefix("spectral_units_"):v for k,v in counts.items()
           if k.startswith("spectral_units_")},
      "spectral_plant_networks_one_key_valid_positive_unit_studies":len(studies_with_safe),
      "spectral_plant_networks_one_key_valid_positive_unit_taxa":len(taxa_with_safe),
      "original_visit_flower_data_indicator_record_counts":dict(all_join_key_flags),
      "source_rows_coverage_and_missing_summary":dict(counts),
      "correspondence_of_flowers_count_units_to_standardized_flower_visiting_effort":"NOT_ESTABLISHED",
      "original_source_plant_species_flower_key_species_identity_verified":False,
      "site_date_synchronized_flower_abundance_validated":False,
      "valid_denominator_rate_for_visitor_events_per_flower":False,
      "no_source_photo_traits_read":True,
      "trait_visitation_association_fitted":False
    }
    return summary_rows,summary

def read_rows(path):
    with Path(path).open("r",encoding="utf-8",newline="") as f:return list(csv.DictReader(f))

def save(records,report,dest):
    dest.mkdir(parents=True,exist_ok=True)
    with (dest/"source_2557_spectral_plant_flower_count_link_audit.csv").open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
    (dest/"original_flower_count_source_audit_receipt.json").write_text(
        json.dumps(report,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--stage69-original-network-units",required=True,type=Path)
    p.add_argument("--outdir",required=True,type=Path)
    a=p.parse_args()
    records,report=audit(fetch(FLOWER_NAME),fetch(NETWORK_NAME),
                         read_rows(a.stage69_original_network_units))
    save(records,report,a.outdir)
    print("STAGE71A_ORIGINAL_AUTHENTIC_FLOWER_COUNT_DENOMINATOR_AUDIT",json.dumps(report,sort_keys=True))
    print("NO_FIELD_PER_FLOWER_RATE_NO_FALSE_STUDY_EFFORT_EQUIVALENCE_NO_VISIT_TRAIT_EFFECT")
if __name__=="__main__":main()
