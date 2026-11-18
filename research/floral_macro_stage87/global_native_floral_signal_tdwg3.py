"""Stage87A: GLOBAL plant-floral signal × native TDWG-3 region composition.

Original source: Natural History Museum botanical prose (59,369 taxon
labels; 888,328 source botanical traits) x Kew WCVP 2026 accepted species
native (not introduced/doubtful/extinct) level-3 TDWG ranges.

This is a GLOBAL flora-level source opportunity, not the European EuPP
visitor network or the previous 49 plant spectra. Source text is COARSE
visible hue/symmetry/flower size, NOT measured bee receptor spectra,
nectar guide, odor, recognition distance or evolved local phenotype.
A missing text record means UNKNOWN, never a measured negative.
WCVP native region is a range polygon, never a localized population count.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,math,re,zipfile
from pathlib import Path
from collections import Counter,defaultdict

NHM_SHA="b81ab96a2883e2b2e7f254a9e7ab62a34afaa0dfe62f0062d1677ba852dc686a"
WCVP_SHA="d32ea2b3a85e489b14e83bcc9eae7274532e1d113753f7be290d4b2dfde573fa"
HUES={
  "yellow":r"yellow|yellowish|golden|gold",
  "white":r"white|whitish|cream|ivory",
  "purple":r"purple|purplish|violet|violaceous|lilac|lavender|mauve",
  "blue":r"blue|bluish|azure|cyan",
  "pink":r"pink|pinkish|rose|rosy|salmon",
  "red":r"red|reddish|scarlet|crimson|maroon|carmine",
  "orange":r"orange|orangish|copper",
  "green":r"green|greenish",
  "brown":r"brown|brownish",
  "black":r"black|blackish",
  "gray":r"grey|gray|greyish|grayish",
}
PATTERNS={k:re.compile(r"(?<![a-z])(?:"+v+r")(?![a-z])")
          for k,v in HUES.items()}
SPOT=re.compile(r"(?<![a-z])spot(?:ted)?(?![a-z])")
SPECIES=re.compile(r"^[a-z][a-z-]* [a-z][a-z-]*$")
COLS=("flower colour","petal colour","corolla colour")
REQUIRED_NHM=59369
REQUIRED_HUE_TEXT=31773

def sha256(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for b in iter(lambda:f.read(4*1024*1024),b""):h.update(b)
    return h.hexdigest()

def strict_name(s):
    x=" ".join(str(s or "").replace("_"," ").casefold().split())
    return x if SPECIES.fullmatch(x) and x.split()[1] not in {
        "sp","spp","cf","aff","unknown","species","hybrid"} else None

def source_hues(row):
    text=", ".join(str(row.get(c) or "").casefold() for c in COLS)
    recorded=bool(text.strip(", "))
    return recorded,tuple(sorted(k for k,p in PATTERNS.items() if p.search(text)))

def numeric_cm(cell):
    """Measured-source botanical description typed petal width, NOT flower display."""
    s=str(cell or "").strip().casefold()
    m=re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*(?:cm)?\s*",s)
    if not m:return None
    v=float(m.group(1))
    return v if math.isfinite(v) and 0<v<150 else None

def load_nhm(path):
    if sha256(path)!=NHM_SHA:raise ValueError("STAGE87_NHM_59369_SOURCE_SHA_CHANGED")
    records={};dupes=set()
    count=Counter(); unparsed=[]
    with Path(path).open(encoding="utf-8-sig",newline="") as h:
        for row in csv.DictReader(h):
            count["original_NHM_source_taxon_labels"]+=1
            name=strict_name(row.get("taxon"))
            documented,hues=source_hues(row)
            if documented:count["NHM_documented_colour_text"]+=1
            if not name:
                count["NHM_not_strict_species_binomial"]+=1
                continue
            if name in records:dupes.add(name);continue
            petal=numeric_cm(row.get("petal max. width [cm]"))
            tubes=numeric_cm(row.get("corolla tube max. length [cm]"))
            spot=bool(SPOT.search(", ".join(str(row.get(c) or "").casefold() for c in COLS)))
            records[name]={"colour_documented":documented,"hues":hues,
                "explicit_single_hue":hues[0] if len(hues)==1 else None,
                "positive_spot_text":spot,
                "petal_max_width_cm":petal,"corolla_tube_max_length_cm":tubes,
                "genus":name.split()[0]}
            count["NHM_strict_unique_species"]+=1
            count["NHM_strict_flower_colour_documented"]+=documented
            count["NHM_strict_exclusive_colour_lexical_family"]+=(len(hues)==1)
            count["NHM_strict_positive_spot_word"]+=spot
            count["NHM_strict_source_petal_width"]+=(petal is not None)
            count["NHM_strict_source_tube_length"]+=(tubes is not None)
    if count["original_NHM_source_taxon_labels"]!=REQUIRED_NHM:
        raise ValueError("STAGE87_NHM_59369_SOURCE_COUNT_CHANGED")
    if count["NHM_documented_colour_text"]!=REQUIRED_HUE_TEXT:
        raise ValueError("STAGE87_NHM_ORIGINAL_31773_COLOUR_TEXT_CHANGED")
    if dupes:raise ValueError("STAGE87_DUPLICATE_SCIENTIFIC_BINOMIAL_SOURCE")
    return records,dict(count)

def flag(s):
    t=str(s or "").strip()
    if t=="0":return False
    if t=="1":return True
    return None

def wcvp_regions(path,traits):
    if sha256(path)!=WCVP_SHA:raise ValueError("STAGE87_WCVP_ORIGINAL_SOURCE_DIGEST_CHANGED")
    accepted=defaultdict(set);counter=Counter()
    with zipfile.ZipFile(path) as z:
        if not {"wcvp_names.csv","wcvp_distribution.csv"}<=set(z.namelist()):
            raise ValueError("STAGE87_WCVP_ORIGINAL_RAW_TABLES_MISSING")
        with io.TextIOWrapper(z.open("wcvp_names.csv"),encoding="utf-8",errors="replace",newline="") as f:
            for row in csv.DictReader(f,delimiter="|"):
                counter["original_all_WCVP_name_rows"]+=1
                if row["taxon_status"].strip().casefold()!="accepted" or row["taxon_rank"].strip().casefold()!="species":continue
                sp=strict_name(row["taxon_name"])
                if sp in traits:
                    accepted[sp].add(row["plant_name_id"].strip())
        valid={next(iter(ids)):sp for sp,ids in accepted.items() if len(ids)==1 and next(iter(ids))}
        counter["strict_NHM_names_exact_WCVP_accepted"]=len(valid)
        counter["NHM_names_WCVP_accepted_ambiguous"]=sum(len(ids)>1 for ids in accepted.values())
        species_by_region=defaultdict(set); native_states=defaultdict(set)
        with io.TextIOWrapper(z.open("wcvp_distribution.csv"),encoding="utf-8",errors="replace",newline="") as f:
            for row in csv.DictReader(f,delimiter="|"):
                counter["original_all_WCVP_distribution_rows"]+=1
                sp=valid.get(row["plant_name_id"].strip())
                if sp is None:continue
                code=str(row["area_code_l3"]).strip().upper()
                if not code:continue
                if flag(row["extinct"]) is not False or flag(row["location_doubtful"]) is not False:
                    counter["matched_extinct_doubtful_unknown_or_missing_excluded"]+=1;continue
                b=flag(row["introduced"])
                if b is None:
                    counter["matched_introduction_flag_unknown_excluded"]+=1;continue
                native_states[(code,sp)].add("introduced" if b else "native")
        for (code,sp),statuses in native_states.items():
            if statuses=={"native"}:
                species_by_region[code].add(sp)
                counter["regional_native_taxon_incidence"]+=1
            elif statuses=={"native","introduced"}:
                counter["source_native_and_introduced_same_region_conflict_excluded"]+=1
            else:
                counter["source_non_native_explicitly_introduced"]+=1
    if not species_by_region:raise ValueError("STAGE87_WCVP_SOURCE_NO_NATIVE_REGIONS")
    counter["global_TDWG3_regions_with_source_native_trait_taxa"]=len(species_by_region)
    counter["globally_unique_accepted_NHM_source_native_species"]=len(set().union(*species_by_region.values()))
    return species_by_region,dict(counter)

def summarize(regions,traits):
    # A real documented hue is a lexical report, not a receptor-space effect.
    # All WCVP native species provide observed denominators; only documented
    # colour source species are eligible for lexical colour composition.
    freq=Counter(sp for sps in regions.values() for sp in sps)
    rows=[]
    for code,sps in sorted(regions.items()):
        counts=Counter();genera=defaultdict(list);hue_genus=defaultdict(lambda:Counter())
        for sp in sps:
            t=traits[sp];g=t["genus"]
            genera[g].append(sp)
            counts["n_accepted_native_species_with_any_NHM_source"]+=1
            counts["n_unique_source_native_genera"]+=0
            counts["n_source_colour_documented"]+=t["colour_documented"]
            counts["n_source_single_explicit_hue"]+=(t["explicit_single_hue"] is not None)
            counts["n_source_positive_spot_word"]+=t["positive_spot_text"]
            counts["n_source_petal_width"]+=(t["petal_max_width_cm"] is not None)
            counts["n_source_tube_length"]+=(t["corolla_tube_max_length_cm"] is not None)
            if t["explicit_single_hue"]:
                k=t["explicit_single_hue"]
                counts["hue_"+k]+=1
                hue_genus[g][k]+=1
            for h in t["hues"]:
                counts["positive_any_hue_word_"+h]+=1
        counts["n_unique_source_native_genera"]=len(genera)
        record={"TDWG_L3":code,**dict(counts)}
        n=counts["n_source_single_explicit_hue"]
        colour=counts["n_source_colour_documented"]
        record["source_documented_colour_coverage_fraction"]=colour/len(sps)
        # Explicitly denominated composition among *single lexical hue* plants.
        for h in HUES:
            record["hue_"+h+"_count"]=counts["hue_"+h]
            record["hue_"+h+"_fraction_of_exclusive_documented"]=(
                counts["hue_"+h]/n if n else "")
            # Genus-balanced mean within all source-colour-description genera.
            gg=[cs[h]/sum(cs.values()) for cs in hue_genus.values() if sum(cs.values())>0]
            record["hue_"+h+"_mean_of_genus_fractions"]=sum(gg)/len(gg) if gg else ""
        widths=[traits[sp]["petal_max_width_cm"] for sp in sps if traits[sp]["petal_max_width_cm"] is not None]
        record["petal_max_width_mean_of_documented_species_cm"]=sum(widths)/len(widths) if widths else ""
        record["source_positive_spot_description_rate_NOT_true_trait_prevalence"]=(
            counts["n_source_positive_spot_word"]/colour if colour else "")
        record["source_lexical_hue_is_not_measured_bee_colour"]="YES"
        record["source_spot_unmentioned_means_UNKNOWN_not_negative"]="YES"
        record["WCVP_region_native_status_not_population_origin"]="YES"
        rows.append(record)
    return rows,{"region_count":len(rows),
       "regions_with_at_least_25_documented_single_hues":sum(r["n_source_single_explicit_hue"]>=25 for r in rows),
       "regions_with_at_least_50_documented_single_hues":sum(r["n_source_single_explicit_hue"]>=50 for r in rows),
       "global_source_species_range_repetitions":dict(Counter(freq.values())),
       "source_species_repeated_across_regions_not_phylogenetic_independent":True,
       "any_flower_hue_missing_not_assumed_absence":True}

def write(path,rows):
    columns=sorted(set().union(*(set(r) for r in rows)))
    with Path(path).open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=columns);w.writeheader();w.writerows(rows)

def run(nhm_path,wcvp_path,outdir):
    traits,nhm=load_nhm(nhm_path)
    region,wcvp=wcvp_regions(wcvp_path,traits)
    result,meta=summarize(region,traits)
    outdir.mkdir(parents=True,exist_ok=True)
    write(outdir/"stage87_native_TDWG3_original_NHM_visual_source_community.csv",result)
    receipt={"schema":"stage87_original_global_NHM_59369_text_WCVP_native_TDWG3_flora_source",
      "sources":{"nhm":{"source_sha256":NHM_SHA,**nhm},
                 "wcvp":{"source_sha256":WCVP_SHA,**wcvp}},
      "source_region_composition":meta,
      "study_not_restricted_to_prior_49_spectrometer_taxa":True,
      "spatial_native_ranges_not_local_population_survey":True,
      "no_global_true_Bombus_occurrence_or_suitability_already_included":True,
      "no_true_flower_age_UV_guide_odour_learning_landing_or_fitness_assessed":True}
    (outdir/"stage87_real_global_NHM_WCVP_native_TDWG3_receipt.json").write_text(
        json.dumps(receipt,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    print("STAGE87_ORIGINAL_GLOBAL_FLORAL_NHM_NATIVE_REGION",json.dumps({
       "sources":receipt["sources"],
       "region":{k:v for k,v in meta.items() if k!="global_source_species_range_repetitions"}},sort_keys=True),flush=True)
    return receipt

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--original-NHM",required=True,type=Path)
    p.add_argument("--original-WCVP-zip",required=True,type=Path)
    p.add_argument("--outdir",required=True,type=Path)
    x=p.parse_args();run(x.original_NHM,x.original_WCVP_zip,x.outdir)
if __name__=="__main__":main()
