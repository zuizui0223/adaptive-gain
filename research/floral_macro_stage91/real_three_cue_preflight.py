#!/usr/bin/env python3
"""Stage91A authentic NHM/WCVP/GIFT three-cue *availability* preflight.

NOT a wind association. Missing floral markings != unmarked. Petal width
!= open flower diameter. Absent scent field != scentless species.
Global TDWG3 regions include islands: no mainland slopes are estimated.
"""
from __future__ import annotations
import argparse, csv, json, re, sys
from pathlib import Path
from collections import Counter, defaultdict

BASE = Path(__file__).resolve().parents[1]
for name in ("floral_macro_stage87", "floral_macro_stage88", "floral_macro_stage89"):
    sys.path.insert(0, str(BASE / name))
from global_native_floral_signal_tdwg3 import load_nhm, wcvp_regions, strict_name
from source_taxonomic_family_exclusion_native_flora import source_families
from gift32_independent_pollen_mode_global_native_coverage import original_gift_species

COLS = ("flower colour", "petal colour", "corolla colour")
POS = re.compile(r"\b(?:spots?|spotted|striped|stripes?|streaked|blotched|mottled|maculate|nectar[ -]?guides?)\b", re.I)
NEG = re.compile(r"\b(?:unspotted|unmarked|immaculate|unstriped|plain|without\s+(?:any\s+)?(?:spots?|stripes?|markings?)|no\s+(?:spots?|markings?))\b", re.I)
NEGATED = re.compile(r"\b(?:not|no|without)\s+(?:spots?|spotted|striped|stripes?|markings?|nectar[ -]?guides?)\b", re.I)
WIDTH = re.compile(r"^(\d+(?:\.\d+)?)\s*(?:cm)?$", re.I)

def mark_state(row):
    text="; ".join(str(row.get(c) or "").strip() for c in COLS).strip("; ")
    if not text: return "source_colour_missing"
    p=bool(POS.search(NEGATED.sub(" ", text)))
    n=bool(NEG.search(text) or NEGATED.search(text))
    return "ambiguous" if p and n else "positive_lexical" if p else "explicit_plain_lexical" if n else "unmentioned"

def petal_width(value):
    m=WIDTH.fullmatch(str(value or "").strip())
    if not m:return None
    x=float(m.group(1))
    return x if 0<x<150 else None

def source_rows(path, accepted):
    out={}
    with Path(path).open(encoding="utf-8-sig",newline="") as h:
        rd=csv.DictReader(h)
        keys=set(rd.fieldnames or [])
        if "taxon" not in keys or not (set(COLS)&keys):
            raise ValueError("Stage91 source flower-colour text or taxon fields missing")
        print("STAGE91_ACTUAL_NHM_COMPACT_FIELDS",json.dumps(sorted(keys)),flush=True)
        scent_headers=[k for k in keys if any(s in k.casefold() for s in ("scent","odour","odor","fragrance"))]
        diameter_headers=[k for k in keys if "flower" in k.casefold() and "diameter" in k.casefold()]
        for row in rd:
            sp=strict_name(row.get("taxon"))
            if sp not in accepted:continue
            if sp in out:raise ValueError("Duplicate authenticated NHM species")
            out[sp]=(mark_state(row),petal_width(row.get("petal max. width [cm]")))
    if len(out)!=len(accepted):raise ValueError("Stage87 strict taxon list differs from Stage91 scan")
    return out,scent_headers,diameter_headers

def source_region_counts(native, traits, modes, families):
    c=Counter()
    pos_families=Counter()
    positive_genera=set()
    for sp in native:
        state,width=traits[sp]
        mode=modes.get(sp,"unknown")
        c["n_native"]+=1
        c["pollen_mode_"+mode]+=1
        c["mark_"+state]+=1
        if width is not None:c["n_source_petals_width_numeric"]+=1
        if state=="positive_lexical":
            pos_families[families.get(sp,"UNKNOWN")]+=1
            positive_genera.add(sp.split()[0])
    return {
        "n_native":c["n_native"],
        "pollen_animal":c["pollen_mode_animal"],
        "pollen_wind":c["pollen_mode_wind"],
        "pollen_unknown":c["pollen_mode_unknown"],
        "n_mark_positive_source_only":c["mark_positive_lexical"],
        "n_mark_explicit_plain_source_only":c["mark_explicit_plain_lexical"],
        "n_mark_ambiguous":c["mark_ambiguous"],
        "n_mark_unmentioned_not_negative":c["mark_unmentioned"],
        "n_source_colour_missing":c["mark_source_colour_missing"],
        "n_numeric_PETAL_width_not_flower_diameter":c["n_source_petals_width_numeric"],
        "n_verified_open_flower_diameter":0,
        "n_verified_floral_fragrance":0,
        "n_marking_positive_genera":len(positive_genera),
        "top_positive_family":pos_families.most_common(1)[0][0] if pos_families else "",
        "top_positive_family_n":pos_families.most_common(1)[0][1] if pos_families else 0,
        "mainland_classification":"PENDING_AUDITED_REGION_GEOMETRY",
        "trait_wind_regression_admissible":"NO"
    }

def run(nhm_path,wcvp_path,gift_path,output):
    raw,nhm=load_nhm(nhm_path)
    regions,wcvp=wcvp_regions(wcvp_path,raw)
    family,_=source_families(wcvp_path,raw)
    modes,gift=original_gift_species(gift_path)
    unique=set().union(*regions.values())
    if len(regions)!=367 or len(unique)!=55775:
        raise ValueError("Stage91 pinned global native species/region count changed")
    if len(unique&set(modes))!=3172 or sum(modes.get(s)=="wind" for s in unique)!=612:
        raise ValueError("Stage91 pinned GIFT mode-qualified cohort changed")
    data,scent_headers,diameter_headers=source_rows(nhm_path,set(raw))
    rows=[dict(TDWG_L3=k,**source_region_counts(v,data,modes,family))
          for k,v in sorted(regions.items())]
    states=Counter(data[s][0] for s in unique)
    widths=sum(data[s][1] is not None for s in unique)
    receipt={
       "schema":"stage91_3cue_original_NHM_WCVP_GIFT_support_ONLY",
       "native_unique_species":len(unique),"all_TDWG3_regions_INCLUDES_ISLANDS":len(regions),
       "GIFT_mode_assigned_native_species":3172,
       "GIFT_animal_mode":sum(modes.get(s)=="animal" for s in unique),
       "GIFT_wind_mode":sum(modes.get(s)=="wind" for s in unique),
       "unique_species_flower_mark_lexical_states":dict(states),
       "unique_species_numeric_PETAL_width_NOT_flower_diameter":widths,
       "flower_diameter_validated_species":0,"fragrance_validated_species":0,
       "candidate_structured_scent_fields_NOT_validated":scent_headers,
       "candidate_structured_flower_diameter_fields_NOT_validated":diameter_headers,
       "original_NHM_sha_verified":True,"original_WCVP_sha_verified":True,
       "original_GIFT_sha_verified":True,
       "mainland_geo_source_AUDITED":False,
       "ERA5_1991_2020_primary_gust_source_recovered":False,
       "no_multivariate_cue_model_or_spurious_zero":True,
       "no_real_wind_cue_coefficients":True,
    }
    output.mkdir(parents=True,exist_ok=True)
    with (output/"stage91_global_TDWG3_3cue_availability_INCLUDES_ISLANDS.csv").open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=rows[0].keys())
        writer.writeheader();writer.writerows(rows)
    (output/"stage91_source_support.json").write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
    print("REAL_NHM_WCVP_GIFT_STAGE91_SOURCE_ONLY",json.dumps({
        "species":len(unique),"regions":len(rows),"marking_candidate_species":states["positive_lexical"],
        "numeric_petal_width_species":widths,"validated_fragrance_species":0},sort_keys=True))
    return receipt

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--nhm",required=True,type=Path)
    p.add_argument("--wcvp",required=True,type=Path)
    p.add_argument("--gift",required=True,type=Path)
    p.add_argument("--outdir",required=True,type=Path)
    a=p.parse_args();run(a.nhm,a.wcvp,a.gift,a.outdir)
