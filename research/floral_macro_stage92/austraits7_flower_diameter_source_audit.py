#!/usr/bin/env python3
"""Stage92 original AusTraits v7.0.0 source-only flower-diameter opportunity.

Authentic Zenodo AusTraits ZIP bytes, exact NHM/WCVP native accepted species and
GIFT-v3.2 animal/wind labels are all checked against independently recorded
source SHA256. Species-wide source flower_diameter is a candidate physical
display dimension, NOT measured optical detectability nor necessarily open
flower display. No climatic predictors, islands mask, or wind fit here.
"""
from __future__ import annotations
import argparse, csv, hashlib, io, json, math, re, statistics, sys, zipfile
from collections import Counter,defaultdict
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
for m in ("floral_macro_stage87","floral_macro_stage88","floral_macro_stage89"):
    sys.path.insert(0,str(BASE/m))
from global_native_floral_signal_tdwg3 import load_nhm,wcvp_regions,strict_name
from source_taxonomic_family_exclusion_native_flora import source_families
from gift32_independent_pollen_mode_global_native_coverage import original_gift_species

AUSTRAITS_SHA="2995fb9e5eebf9271f9241b5a6c2e2cbb7b45e8eda5ce4db43c14c68f95e2f3f"
AUSTRAITS_DOI="10.5281/zenodo.15718081"
AUSTRAITS_VERSION="7.0.0"
COLUMN_ALIASES={
  "taxon":("taxon_name","accepted_name","scientific_name","species_name","taxon"),
  "trait":("trait_name","trait"),
  "value":("trait_value","value"),
  "unit":("trait_unit","unit","unit_name"),
  "dataset":("dataset_key","dataset_id","dataset","source_id"),
}
MM_PER_UNIT={"mm":1.0,"millimeter":1.0,"millimetre":1.0,
             "cm":10.0,"centimeter":10.0,"centimetre":10.0,
             "m":1000.0,"meter":1000.0,"metre":1000.0}
FLOAT=re.compile(r"^\s*(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?\s*$")

def sha256(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda:f.read(1<<20),b""):h.update(chunk)
    return h.hexdigest()

def schema(fields):
    if not fields:return None
    available={s.strip() for s in fields if s}
    found={k:next((c for c in opts if c in available),None) for k,opts in COLUMN_ALIASES.items()}
    if not all(found[k] for k in ("taxon","trait","value")):return None
    return found

def choose_source_table(z):
    options=[]
    for name in z.namelist():
        if not name.casefold().endswith(".csv") or name.endswith("/"):continue
        try:
            with io.TextIOWrapper(z.open(name),encoding="utf-8-sig",newline="") as f:
                rd=csv.reader(f); fields=next(rd,[])
        except (UnicodeDecodeError,ValueError,StopIteration):
            continue
        cols=schema(fields)
        if cols:options.append((z.getinfo(name).file_size,name,cols))
    if not options:raise ValueError("AUTHENTIC_AUSTRAITS_NO_EXACT_LONG_TRAIT_TABLE")
    return max(options,key=lambda x:x[0])

def normalized_diameter(value,unit):
    u=" ".join(str(unit or "").casefold().split()).replace("µ","u")
    factor=MM_PER_UNIT.get(u)
    if factor is None:return None,"unit_unrecognized"
    s=str(value or "").strip()
    if not FLOAT.fullmatch(s):return None,"value_not_unambiguous_numeric"
    x=float(s)*factor
    if not math.isfinite(x) or x<=0:return None,"not_positive_finite"
    if x>1000:return None,"outlier_above_1000mm_review"
    return x,"valid_source_labeled_mm"

def parse_original_austraits_zip(path,approved):
    if sha256(path)!=AUSTRAITS_SHA:
        raise ValueError("AUSTRAITS_V7_ORIGINAL_ZENODO_21MB_SHA256_DRIFT")
    out=defaultdict(lambda:defaultdict(list))
    count=Counter();raw_units=Counter();dataset=Counter()
    with zipfile.ZipFile(path) as z:
        _,member,cols=choose_source_table(z)
        with io.TextIOWrapper(z.open(member),encoding="utf-8-sig",newline="") as f:
            rd=csv.DictReader(f)
            for row in rd:
                count["source_long_format_rows"]+=1
                if (row.get(cols["trait"]) or "").strip()!="flower_diameter":continue
                count["author_flower_diameter_rows"]+=1
                ds=(row.get(cols["dataset"]) or "UNKNOWN") if cols["dataset"] else "UNKNOWN"
                raw_units[(row.get(cols["unit"]) or "UNSPECIFIED") if cols["unit"] else "UNSPECIFIED"]+=1
                sp=strict_name(row.get(cols["taxon"]))
                if sp not in approved:
                    count["not_exact_NHM_WCVP_native_taxon"]+=1
                    continue
                count["original_exact_WCVP_native_diameter_rows"]+=1
                val,why=normalized_diameter(row.get(cols["value"]),""
                       if cols["unit"] is None else row.get(cols["unit"]))
                count["exact_"+why]+=1
                if val is None:continue
                dataset[ds]+=1
                out[sp][ds].append(val)
    if count["source_long_format_rows"]<100000 or count["author_flower_diameter_rows"]<1:
        raise ValueError("AUSTRAITS_RETRIEVED_WRONG_SOURCE_TABLE_OR_NO_DIAMETER")
    species={s:statistics.median([statistics.median(v) for v in grouped.values()])
             for s,grouped in out.items()}
    return species,{
        "authentic_zipped_source_sha256":AUSTRAITS_SHA,
        "source_doi":AUSTRAITS_DOI,"source_version":AUSTRAITS_VERSION,
        "original_zip_inner_long_table_path":member,
        "original_zip_table_column_mapping":cols,
        "counts":dict(count),
        "raw_source_units":dict(raw_units),
        "valid_diameter_rows_per_dataset":dict(dataset),
        "source_species_values_are_median_of_datasets":True,
        "original_source_species_not_a_natural_random_sample":True,
        "source_flower_diameter_label_NOT_confirmed_optical_display_or_opening":True,
    }

def regional(rows,traits,modes,fams):
    vals=[(s,traits[s]) for s in rows if s in traits]
    families={fams.get(s,"UNKNOWN") for s,_ in vals}
    genera={s.split()[0] for s,_ in vals}
    bymode=Counter(modes.get(s,"unknown") for s,_ in vals)
    return {"n_original_WCVP_native_species_in_region":len(rows),
      "n_original_AusTraits_flower_diameter_species":len(vals),
      "n_distinct_source_diameter_genera":len(genera),
      "n_distinct_source_diameter_families":len(families),
      "diameter_median_mm_of_source_species":statistics.median([v for _,v in vals]) if vals else "",
      "n_diameter_species_GIFT_animal":bymode["animal"],
      "n_diameter_species_GIFT_wind":bymode["wind"],
      "n_diameter_species_GIFT_UNKNOWN":bymode["unknown"],
      "n_diameter_independent_source_dataset_effects":"NOT_INFERRED",
      "mainland_scope":"NOT_GEOMETRY_VERIFIED_INCLUDES_ISLANDS",
      "wind_exposure_join_admissible":"NO"}

def run(nhm,wcvp,gift,aus,out):
    allnhm,nhmmeta=load_nhm(nhm)
    native,wcvpmeta=wcvp_regions(wcvp,allnhm)
    mode,modeinfo=original_gift_species(gift)
    fam,faminfo=source_families(wcvp,allnhm)
    unique=set().union(*native.values())
    if len(unique)!=55775 or len(native)!=367 or len(unique&set(mode))!=3172:
        raise ValueError("STAGE92_INHERITED_SOURCE_NATIVE_MODE_COHORT_CHANGED")
    species,sourceinfo=parse_original_austraits_zip(aus,unique)
    if not species:raise ValueError("AUTHENTIC_AUSTRAITS_NO_VALID_EXACT_NATIVE_DIAMETERS")
    breadth=Counter(s for names in native.values() for s in names)
    rows=[dict(TDWG_L3=k,**regional(sp, species, mode, fam))
          for k,sp in sorted(native.items())]
    modecounts=Counter(mode.get(sp,"unknown") for sp in species)
    result={
      "schema":"stage92_authentic_AusTraits7_explicit_flower_diameter_x_WCVP55775_TDWG3_support_ONLY",
      "native_accepted_species":len(unique),"region_source_count_INCLUDES_ISLANDS":len(native),
      "exact_WCVP_native_valid_flower_diameter_species":len(species),
      "valid_species_by_qualified_GIFT_mode":dict(modecounts),
      "valid_species_unique_genera":len({s.split()[0] for s in species}),
      "valid_species_unique_WCVP_families":len({fam.get(s,"UNKNOWN") for s in species}),
      "regional_species_repetitions_NOT_independent_evolution":sum(breadth[s] for s in species),
      "source":sourceinfo,
      "original_NHM_source_sha_verified":True,
      "original_WCVP_source_sha_verified":True,
      "original_GIFT_source_sha_verified":True,
      "mainland_only_spatial_region_frame_verified":False,
      "signal_size_exposure_regression_executed":False,
      "flower_diameter_IS_source_labeled_not_always_open_display":True
    }
    out.mkdir(parents=True,exist_ok=True)
    with (out/"stage92_AusTraits7_flower_diameter_367_regions_INCLUDES_ISLANDS.csv").open("w",newline="",encoding="utf-8") as f:
        wr=csv.DictWriter(f,fieldnames=list(rows[0]));wr.writeheader();wr.writerows(rows)
    (out/"stage92_real_AusTraits7_flower_diameter_source_support.json").write_text(
       json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("STAGE92_REAL_AUSTRAITS7_NATIVE_FLOWER_DIAMETER_OPPORTUNITY",
        json.dumps({k:v for k,v in result.items() if k!="source"},sort_keys=True),flush=True)
    return result

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--original-NHM",type=Path,required=True)
    p.add_argument("--original-WCVP",type=Path,required=True)
    p.add_argument("--original-GIFT",type=Path,required=True)
    p.add_argument("--original-AusTraits7",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args();run(a.original_NHM,a.original_WCVP,a.original_GIFT,a.original_AusTraits7,a.outdir)
