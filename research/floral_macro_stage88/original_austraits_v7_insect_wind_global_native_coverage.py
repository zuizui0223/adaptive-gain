"""Stage88F: independent original AusTraits v7 insect/wind syndrome coverage.

Fallback to Wang2025 179k Dryad archive only because anonymous original
Dryad file HTTP401 and Wiley supplement HTTP403. This is NOT equivalent
taxon coverage or a confirmatory independent evolutionary test.

Original published AusTraits v7 DOI 10.5281/zenodo.15718081:
 archive key austraits-7.0.0.zip
 SHA256 2995fb9e5eebf9271f9241b5a6c2e2cbb7b45e8eda5ce4db43c14c68f95e2f3f
 declared MD5 f169a9bca41d847df4fb8c6011ee3ea8
 original all 1,798,215 long trait records; 13,440 reported
 pollination_syndrome records for 9,079 raw taxon labels (prior independent
 BALANCE source full-archive validation).
 Strict explicitly coded 'insect' vs 'wind' and only one unique source
 syndrome label per accepted simple species; other and conflicting UNKNOWN.
 No inferential assignment from family, flower hue, spot or absence.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,sys,tempfile,urllib.request,zipfile
from pathlib import Path
from collections import Counter,defaultdict

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"floral_macro_stage87"))
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"floral_macro_stage88"))
from global_native_floral_signal_tdwg3 import load_nhm,wcvp_regions,strict_name
from global_native_pollination_mode_tdwg3 import recompute_global,write_csv

AUSTRAITS_URL="https://zenodo.org/api/records/15718081/files/austraits-7.0.0.zip/content"
ARCHIVE_SHA="2995fb9e5eebf9271f9241b5a6c2e2cbb7b45e8eda5ce4db43c14c68f95e2f3f"
ARCHIVE_MD5="f169a9bca41d847df4fb8c6011ee3ea8"
EXPECTED_FULL_TRAIT_ROWS=1798215
EXPECTED_POLLEN_SOURCE_ROWS=13440
EXPECTED_POLLEN_SOURCE_NAMES=9079

def download_real_austraits(path):
    h=hashlib.sha256();m=hashlib.md5();n=0
    req=urllib.request.Request(AUSTRAITS_URL,headers={"User-Agent":"independent-global-pollen-mode-trait-coverage/1.0"})
    with urllib.request.urlopen(req,timeout=240) as r,Path(path).open("wb") as f:
        while True:
            x=r.read(4*1024*1024)
            if not x:break
            n+=len(x)
            if n>1_100_000_000:raise ValueError("AUSTRAITS_SOURCE_UNEXPECTED_OVERSIZE")
            h.update(x);m.update(x);f.write(x)
    if h.hexdigest()!=ARCHIVE_SHA or m.hexdigest()!=ARCHIVE_MD5:
        raise ValueError("STAGE88F_REAL_AUTHOR_ARCHIVE_SHA_OR_MD5_CHANGED")
    return {"original_author_release_Zenodo":15718081,
            "original_ZIP_bytes":n,
            "original_SHA256":h.hexdigest(),"original_MD5":m.hexdigest()}

def original_long_source_table(z):
    found=[]
    for f in z.infolist():
        if f.filename.casefold().endswith(".csv") and f.file_size>1_000_000:
            with z.open(f) as r:
                header=next(csv.reader([r.readline().decode("utf-8-sig",errors="replace")]))
            h=set(header)
            if {"taxon_name","trait_name","value","dataset_id"}<=h:
                found.append(f)
    # The official v7 archive contains both its primary traits.csv and
    # excluded_data.csv with the same long-format schema. Only traits.csv
    # is the analysis dataset; excluded_data must never be admitted.
    canonical=[f for f in found if Path(f.filename).name.casefold()=="traits.csv"]
    if len(canonical)!=1:
        raise ValueError("STAGE88F_AUSTRAITS_PRIMARY_TRAITS_CSV_NOT_UNIQUE "+
                         str([(x.filename,x.file_size) for x in found]))
    return canonical[0]

def pollination_source(z):
    source=original_long_source_table(z)
    labels=defaultdict(set);origins=defaultdict(set)
    counts=Counter();raw_modes=Counter();data_sources=Counter()
    with io.TextIOWrapper(z.open(source),encoding="utf-8-sig",errors="replace",newline="") as h:
        for row in csv.DictReader(h):
            counts["all_original_long_traits"]+=1
            if row["trait_name"]!="pollination_syndrome":continue
            counts["original_pollination_syndrome_source_rows"]+=1
            rawlabel=str(row["taxon_name"] or "").strip()
            mode=str(row["value"] or "").strip().casefold()
            raw_modes[mode]+=1
            data_sources[str(row["dataset_id"] or "").strip()]+=1
            name=strict_name(rawlabel)
            if not name:
                counts["source_non_simple_binomial_syndrome_rows"]+=1;continue
            labels[name].add(mode)
            origins[name].add(str(row["dataset_id"] or "").strip())
    if counts["all_original_long_traits"]!=EXPECTED_FULL_TRAIT_ROWS:
        raise ValueError("STAGE88F_ORIGINAL_1798215_ALL_SOURCE_ROWS_CHANGED")
    if counts["original_pollination_syndrome_source_rows"]!=EXPECTED_POLLEN_SOURCE_ROWS:
        raise ValueError("STAGE88F_ORIGINAL_13440_INSECT_WIND_SOURCE_ROWS_CHANGED")
    if sum(raw_modes.values())!=EXPECTED_POLLEN_SOURCE_ROWS:
        raise ValueError("STAGE88F_ORIGINAL_SYNDROME_MODE_COUNTS_LOST")
    species={}
    conflicting=set()
    for sp,values in labels.items():
        if len(values)==1 and next(iter(values)) in {"wind","insect"}:
            species[sp]="wind" if "wind" in values else "animal"
        else:conflicting.add(sp)
    unique_original_names=len(labels)
    result={"original_archive_long_source_file":source.filename,
            "original_long_source_rows":counts["all_original_long_traits"],
            "original_syndrome_source_rows":counts["original_pollination_syndrome_source_rows"],
            "original_all_source_syndrome_rows_for_non_species_binomials":counts["source_non_simple_binomial_syndrome_rows"],
            "source_exact_simple_species_with_any_syndrome_record":unique_original_names,
            "source_exact_species_insect_only":sum(s=="animal" for s in species.values()),
            "source_exact_species_wind_only":sum(s=="wind" for s in species.values()),
            "source_conflicting_or_other_syndrome_names_excluded":len(conflicting),
            "original_raw_syndrome_label_counts":dict(raw_modes),
            "source_data_set_keys_for_pollination_syndrome":dict(data_sources),
            "source_recovered_mode_species_count":len(species),
            "source_unknown_is_never_assumed_wind_or_insect":True,
            "source_trait_is_independent_reported_syndrome_NOT_local_fitness_or_actual_bee_visits":True}
    return species,{sp:"|".join(sorted(src)) for sp,src in origins.items()},result

def run(nhm,wcvp,outdir):
    traits,nhm_result=load_nhm(nhm)
    regions,wcvp_result=wcvp_regions(wcvp,traits)
    with tempfile.TemporaryDirectory() as td:
        path=Path(td)/"austraits-7.0.0.zip"
        source=download_real_austraits(path)
        with zipfile.ZipFile(path) as z:
            modes,origins,qa=pollination_source(z)
    matrix,cover=recompute_global(traits,regions,modes,origins)
    outdir.mkdir(parents=True,exist_ok=True)
    write_csv(outdir/"stage88F_original_AusTraits_v7_global_native_animal_wind_unknown_TDWG3_hues.csv",matrix)
    receipt={"schema":"stage88F_original_AusTraits7_global_53k_NHM_WCVP_insect_wind_NATIVE_region_coverage",
      "original_AusTraits_release":source,"source_pollination_syndrome":qa,
      "source_2026_Kew_WCVP":wcvp_result,"source_original_NHM":nhm_result,
      "source_mode_by_native_floras":cover,
      "original_AusTraits_not_Wang_2025_global_179263_source":True,
      "source_Australian_database_taxon_bias_possible":True,
      "source_flowering_species_with_unrecorded_syndromes_unknown_not_wind":True,
      "source_unpublished_original_raw_trait_records_not_redistributed":True,
      "not_an_observed_sensory_cue_order_or_Bombus_preference":True}
    (outdir/"stage88F_original_AusTraits7_insect_wind_global_native_coverage_receipt.json").write_text(
        json.dumps(receipt,indent=2,sort_keys=True,ensure_ascii=False)+"\n")
    print("STAGE88F_TRUE_ORIGINAL_AUSTRAITS_MODE_NATIVE_REGION_SOURCE_COVERAGE",json.dumps({
        "source":qa,"global_exact_taxon_crosswalk":cover.get("source_original_Wang2025_source_mode_strict_matched_species"),
        "source_global_arm_region_coverage":cover["source_spatial_mode_composition_coverage"]},sort_keys=True))
    return receipt

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source-NHM",type=Path,required=True)
    p.add_argument("--source-WCVP-zip",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args()
    run(a.source_NHM,a.source_WCVP_zip,a.outdir)
if __name__=="__main__":main()
