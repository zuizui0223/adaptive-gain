"""Stage79B independent source macro floral distant/near-field signal COVERAGE.

Source real NHM botanical NLP descriptions (original combined.csv 59,369
taxon labels, original git blob SHA pinned), joined by literal species to
corrected EuPPollNet original 18,798 plant×field network-year units across 54
study IDs. Trait availability is measured BEFORE using ANY Bombus counts,
strong ERA5 gusts or interaction effects.

Distant visual size: source petal MAX WIDTH cm is only a proxy for one
component of display extent, NOT total floral display or bee receptor contrast.
Near-field morphology: positive textual marking descriptors are not measured
UV nectar guides, and missing descriptors are UNKNOWN, never confirmed
negative patterns. Corrolla-tube length is morphology/access, not long-range
visual extent. Flower orientation may proxy landing geometry but not measured
aerodynamic landing cost.

No islands. No photos. No false mark-negative or flower-age-change labels.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,math,re,urllib.request
from collections import Counter,defaultdict
from pathlib import Path

SOURCE_REPO="NaturalHistoryMuseum/plant-traits"
ORIGINAL_SOURCE_URL=("https://raw.githubusercontent.com/NaturalHistoryMuseum/"
                     "plant-traits/main/output/raw/ocr-traits/combined.csv")
ORIGINAL_SOURCE_GITBLOB="e1cfd2d5c518c2061ec91d1a9e8b64fc7ca69389"
ORIGINAL_EUPPNET_STAGE69_SHA="475863c2b193dd9c1eaad848dae05a9f518b57446cad2661979ca582c7d88617"
EXPECTED_SOURCE_NHM=59369
EXPECTED_SOURCE_EUPP_PLANTS=1408
EXPECTED_SOURCE_PLANT_NETWORKS=18798
EXPECTED_SOURCE_STUDIES=54
EXPECTED_NETWORKS=1864
MAX_SOURCE_BYTES=26_000_000
MAX_PETAL_WIDTH_CM=150
TEXT_COLOUR=("flower colour","petal colour","corolla colour")
NUMERIC_FIELDS=(
    "petal min. width [cm]","petal max. width [cm]",
    "corolla tube min. length [cm]","corolla tube max. length [cm]")
TEXT_MORPH_FIELDS=("flower orientation","flower symmetry","flower shape")
POTENTIAL_MARK=re.compile(r"(?<![a-z])(?:spot(?:ted)?|strip(?:ed)?|streak(?:ed)?|vein(?:ed)?|patch(?:ed)?|nectar guide|bull.?s.?eye|eye.?spot)(?![a-z])",re.I)

def gitsha(raw):
    return hashlib.sha1(f"blob {len(raw)}\0".encode()+raw).hexdigest()

def original_nhm():
    req=urllib.request.Request(ORIGINAL_SOURCE_URL,headers={
      "User-Agent":"adaptive-gain-stage79-real-floral-trait-distal-proximal/2026",
      "Accept":"text/csv"})
    with urllib.request.urlopen(req,timeout=120) as response:
        b=response.read(MAX_SOURCE_BYTES+1)
    if len(b)>MAX_SOURCE_BYTES or gitsha(b)!=ORIGINAL_SOURCE_GITBLOB:
        raise ValueError("STAGE79B_ORIGINAL_NHM_COMBINED_SOURCE_GITBLOB_CHANGED")
    return b

def key(s):
    return " ".join(str(s or "").strip().casefold().split())

def parsed_size(v):
    v=str(v or "").strip()
    if not v or v.casefold() in {"na","nan","none","null"}:
        return None
    try:x=float(v)
    except ValueError:return None
    if not math.isfinite(x) or x<=0 or x>MAX_PETAL_WIDTH_CM:
        return None
    return x

def ingest_nhm(raw):
    reader=csv.DictReader(io.StringIO(raw.decode("utf-8-sig"),newline=""))
    needed={"taxon",*NUMERIC_FIELDS,*TEXT_MORPH_FIELDS,*TEXT_COLOUR}
    if not needed.issubset(set(reader.fieldnames or [])):
        raise ValueError("STAGE79B_ORIGINAL_NHM_SOURCE_SIZE_COLUMNS_NOT_PRESENT_"+str(sorted(needed-set(reader.fieldnames or []))))
    data={}
    fields=Counter()
    nrows=0
    for row in reader:
        nrows+=1
        name=key(row["taxon"])
        if not name or name in data:
            raise ValueError("STAGE79B_ORIGINAL_NHM_TAXON_DUPLICATE")
        x={f:parsed_size(row.get(f)) for f in NUMERIC_FIELDS}
        shape={f:str(row.get(f) or "").strip() for f in TEXT_MORPH_FIELDS}
        colour={f:str(row.get(f) or "").strip() for f in TEXT_COLOUR}
        desc=" ".join(colour.values())
        flag=int(bool(POTENTIAL_MARK.search(desc)))
        data[name]={
           **x,
           "source_orientation_text":shape["flower orientation"],
           "source_symmetry_text":shape["flower symmetry"],
           "source_shape_text":shape["flower shape"],
           "source_any_color_text":int(bool(desc.strip())),
           "source_reported_positive_marking_text":flag,
           "source_original_petal_width_is_individual_nlp_description_not_total_flower_display":True,
           "source_marking_text_is_NOT_measured_UV_or_spatial_nectar_guide":True,
        }
        for f in NUMERIC_FIELDS:
            fields["source_numeric_usable_"+f]+=x[f] is not None
        for f in TEXT_MORPH_FIELDS:
            fields["source_positive_text_recorded_"+f]+=bool(shape[f])
        fields["source_positive_colour_descriptor_marking"]+=flag
    if nrows!=EXPECTED_SOURCE_NHM:
        raise ValueError("STAGE79B_ORIGINAL_NHM_59369_SOURCE_CHANGED")
    return data,{"source_actual_taxa":nrows,
                 "original_blob_git_SHA1":gitsha(raw),
                 "original_source_SHA256":hashlib.sha256(raw).hexdigest(),
                 "source_full_corpus_coverage":dict(fields)}

def visit_roster(path):
    b=path.read_bytes()
    if hashlib.sha256(b).hexdigest()!=ORIGINAL_EUPPNET_STAGE69_SHA:
        raise ValueError("STAGE79B_ORIGINAL_EUPP_STAGE69_PLANT_NETWORK_SHA_CHANGED")
    rows=list(csv.DictReader(io.StringIO(b.decode("utf-8"))))
    tax={key(r["Original_plant_accepted_name_literal"]) for r in rows}
    studies={r["Study_id"] for r in rows}
    nets={(r["Study_id"],r["Network_id"],r["Year_from_original_date"]) for r in rows}
    if (len(rows),len(tax),len(studies),len(nets))!=(
        EXPECTED_SOURCE_PLANT_NETWORKS,EXPECTED_SOURCE_EUPP_PLANTS,
        EXPECTED_SOURCE_STUDIES,EXPECTED_NETWORKS):
        raise ValueError("STAGE79B_CORRECTED_EUPP_VISIT_ROSTER_SOURCE_GRAIN_CHANGED")
    return rows,tax,nets

def coverage(nhm,roster,taxa,nets):
    overlap={n for n in taxa if n in nhm}
    withmax={n for n in overlap if nhm[n]["petal max. width [cm]"] is not None}
    withmin={n for n in overlap if nhm[n]["petal min. width [cm]"] is not None}
    shape={f:{n for n in overlap if nhm[n]["source_"+f+"_text"]}
           for f in ("orientation","symmetry","shape")}
    positive_mark={n for n in overlap if nhm[n]["source_reported_positive_marking_text"]}
    tube={n for n in overlap if nhm[n]["corolla tube max. length [cm]"] is not None}
    bynet=defaultdict(list)
    tax_rows=[]
    for r in roster:
        tax=key(r["Original_plant_accepted_name_literal"])
        k=(r["Study_id"],r["Network_id"],r["Year_from_original_date"])
        if tax in nhm:
            obs=nhm[tax]
            tax_rows.append({
                "Study_id":k[0],"Network_id":k[1],"Year":k[2],
                "original_plant_literal_accepted_name":tax,
                "source_petal_max_width_cm":obs["petal max. width [cm]"]
                    if obs["petal max. width [cm]"] is not None else "",
                "source_petal_min_width_cm":obs["petal min. width [cm]"]
                    if obs["petal min. width [cm]"] is not None else "",
                "source_corolla_tube_max_length_cm":obs["corolla tube max. length [cm]"]
                    if obs["corolla tube max. length [cm]"] is not None else "",
                "source_positive_marking_text_only":obs["source_reported_positive_marking_text"],
                "source_flower_orientation_text":obs["source_orientation_text"],
                "source_flower_symmetry_text":obs["source_symmetry_text"],
                "source_flower_shape_text":obs["source_shape_text"],
                "original_missing_marking_is_NOT_verified_negative":1,
                "source_petal_width_is_NOT_whole_flower_display":1,
                "source_field_visual_signal_was_measured_same_population":0,
            })
            bynet[k].append((tax,obs))
    statuses=Counter()
    local=[]
    for k in sorted(nets):
        group=bynet.get(k,[])
        numeric=[(name,x["petal max. width [cm]"]) for name,x in group
                 if x["petal max. width [cm]"] is not None]
        marked=[n for n,x in group if x["source_reported_positive_marking_text"]]
        genera={name.split()[0] for name,score in numeric}
        flags={
            "source_network_has_at_least_2_distinct_plant_species_with_petal_max_width":len(numeric)>=2,
            "source_network_has_at_least_2_different_measured_petal_width_values":
                 len({x[1] for x in numeric})>=2,
            "source_network_has_at_least_2_genera_and_distinct_measured_width_values":
                 len(genera)>=2 and len({x[1] for x in numeric})>=2,
            "source_network_has_positive_documented_close_pattern":
                 len(marked)>=1,
            "source_network_has_size_measure_and_positive_close_pattern":
                 bool(numeric and marked),
            "source_network_has_2_size_species_and_close_pattern":
                 len(numeric)>=2 and bool(marked)
        }
        for label,state in flags.items():
            statuses[label]+=state
        local.append({
          "Study_id":k[0],"Network_id":k[1],"Year":k[2],
          "source_species_original_NHM_text":len(group),
          "source_distinct_taxa_with_max_petal_width":len(numeric),
          "source_distinct_values_petal_max_width":len({x[1] for x in numeric}),
          "source_distinct_petal_width_genera":len(genera),
          "source_positive_pattern_documented_species":len(marked),
          **{label:int(value) for label,value in flags.items()},
          "site_assigned_Bombus_visits_used_in_cohort_selection":0,
          "source_unreported_visual_pattern_remains_UNKNOWN":1,
        })
    out={
        "schema":"stage79b_original_nhm_petal_width_text_guide_proxy_EuPPollNet_macro",
        "original_source_studies":EXPECTED_SOURCE_STUDIES,
        "original_field_network_year_keys":len(nets),
        "original_plant_species_recorded_in_field_visits":len(taxa),
        "original_plant_names_lexically_in_NHM":len(overlap),
        "original_source_species_with_petal_MAX_width_cm":len(withmax),
        "original_source_species_with_petal_MIN_width_cm":len(withmin),
        "original_source_species_with_corolla_tube_MAX_length_cm":len(tube),
        "original_source_species_with_positive_pattern_text":len(positive_mark),
        "original_source_species_with_flower_orientation_text":len(shape["orientation"]),
        "original_source_species_with_flower_symmetry_text":len(shape["symmetry"]),
        "original_source_species_with_flower_shape_text":len(shape["shape"]),
        "network_design_coverage_selected_BEFORE_any_visiting_bee_outcome":dict(statuses),
        "networks_with_same_source_metadata_genera_not_phylogenetic_independence":True,
        "source_far_visual_size_proxy_is_petal_width_only_NOT_true_DISPLAY":True,
        "source_positive_mark_text_not_true_UV_nectar_guide":True,
        "source_unknown_marking_is_NEVER_zero":True,
        "source_plant_trait_same_field_population_coincident":False,
        "no_flowers_photo_visual_extraction":True,
        "no_WIND_interaction_or_causal_paths_fitted":True,
    }
    return out,local,tax_rows

def write(path,rows):
    if not rows:return
    with Path(path).open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader();w.writerows(rows)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source-Stage69-network-plant",required=True,type=Path)
    p.add_argument("--outdir",required=True,type=Path)
    a=p.parse_args();a.outdir.mkdir(exist_ok=True,parents=True)
    nhm,source=ingest_nhm(original_nhm())
    roster,taxa,nets=visit_roster(a.source_Stage69_network_plant)
    result,sites,species=coverage(nhm,roster,taxa,nets)
    result["original_source_nhm_raw_corpus"]=source
    write(a.outdir/"original_EuPP_plant_petal_width_marking_trait_availability.csv",species)
    write(a.outdir/"original_1864_field_network_visual_size_near_motif_outcome_blind_cohorts.csv",sites)
    (a.outdir/"original_macro_source_far_petal_width_near_marking_coverage.json").write_text(
        json.dumps(result,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("STAGE79B_REAL_NHM_LONG_SHORT_DISTANCE_VISUAL_TRAITS_COVERAGE",
          json.dumps(result,sort_keys=True,ensure_ascii=False))
    print("NO_TRUE_FLOWER_DISPLAY_VISUAL_UV_GUIDE_NEGATIVES_NO_BOMBUS_EFFECT_FITTED")
if __name__=="__main__":
    main()
