"""Stage72C author-source exact matrix reconstruction and VOC-source species join.

SOURCE: Kantsa et al. (2018) DOI 10.1038/s41467-018-03448-w,
Figshare 10.6084/m9.figshare.5663455.v2 (authentic original files 10377684,
10389468, SHA256 validated in Stage72B).
One Greek study site only. Descriptive NOT new causal ecology inference.
"""
from __future__ import annotations

import argparse,csv,json,math
from collections import Counter
from pathlib import Path

from replay_original_kantsa2018_network_voc import (
    fetch_original,read_xlsx_sparse,safe_float,SOURCE_FILES,KNOWN_2018
)

def literal(name):
    # Space/casing normalization only; no guessed synonym or alternate spelling.
    return " ".join(str(name).strip().casefold().split())

def reconstruct_network(raw):
    d=read_xlsx_sparse(raw,"network")
    sheet=d["p-p_network"]
    # Source Excel positions: row 3 col B..AP = 41 original plant labels;
    # rows 4..171 = 168 original visitor labels, numeric cells at col B..AP.
    plants={col:name for col,name in sheet[3].items() if col>=1}
    visitors={n:row[0] for n,row in sheet.items() if n>=4 and 0 in row}
    if len(plants)!=41 or len(visitors)!=168:
        raise ValueError("STAGE72C_ORIGINAL_SOURCE_EXPECTED_41_X_168_MATRIX_NOT_SATISFIED")
    if len({literal(s) for s in plants.values()})!=41:
        raise ValueError("STAGE72C_ORIGINAL_MATRIX_PLANT_COLUMNS_NOT_UNIQUE")
    if len({literal(s) for s in visitors.values()})!=168:
        raise ValueError("STAGE72C_ORIGINAL_VISITOR_ROW_NAMES_NOT_UNIQUE")
    counts=Counter();n_non_numeric=0
    byplant=[]
    for col,plant in sorted(plants.items()):
        total=links=species_bombus=0
        observed_visitors=[]
        for row,visitor in sorted(visitors.items()):
            rawval=sheet[row].get(col,"")
            value=safe_float(rawval)
            if value is None or not value.is_integer():
                n_non_numeric+=1
                continue
            value=int(value)
            counts["author_network_numeric_cells"]+=1
            counts["author_network_event_count"]+=value
            counts["author_network_positive_links"]+=(value>0)
            total+=value;links+=(value>0)
            if value>0:observed_visitors.append(visitor)
            if literal(visitor).startswith("bombus "):
                species_bombus+=value
        byplant.append({
          "original_network_plant_literal":plant,
          "author_original_visitor_event_count":total,
          "author_original_nonzero_visitor_links":links,
          "author_original_positive_visitor_names_delimited":"|".join(observed_visitors),
          "Bombus_genus_literal_taxon_name_visitor_rows_without_guild_inference":species_bombus,
          "2018_source_sampled_one_field_region":1,
        })
    if n_non_numeric:
        raise ValueError(f"STAGE72C_ORIGINAL_MATRIX_41x168_NONNUMERIC_COUNT_{n_non_numeric}")
    if counts["author_network_numeric_cells"]!=41*168:
        raise ValueError("STAGE72C_ORIGINAL_MATRIX_INCOMPLETE_NUMERIC_CELLS")
    if counts["author_network_positive_links"]!=KNOWN_2018["published_nonzero_plant_insect_links"]:
        raise ValueError("STAGE72C_ORIGINAL_NONZERO_LINK_COUNT_NOT_REPRODUCED")
    # One original author source cell difference from the abstract:
    # 7,954 source vs 7,955 manuscript. Flag; NEVER manufacture one visit.
    if counts["author_network_event_count"]!=7954:
        raise ValueError("STAGE72C_ORIGINAL_7954_SOURCE_DIGEST_COUNTS_NOT_REPRODUCED")
    report={
      "original_plants":len(plants),
      "original_visitor_species_row_labels":len(visitors),
      "original_source_plant_insect_matrix_cells":counts["author_network_numeric_cells"],
      "original_source_nonzero_links":counts["author_network_positive_links"],
      "original_source_VISITOR_EVENTS_NUMERIC_SUM":counts["author_network_event_count"],
      "published_article_stated_events":KNOWN_2018["published_visitor_events"],
      "original_source_vs_manuscript_event_difference":counts["author_network_event_count"]-KNOWN_2018["published_visitor_events"],
      "source_difference_not_silently_added_to_plant_or_guild":True,
      "non_numeric_or_missing_visitor_matrix_cells":n_non_numeric,
      "source_full_visitor_taxa_labels_used_not_inferred_from_color":True,
    }
    return byplant,report

def original_voc_species(raw):
    d=read_xlsx_sparse(raw,"voc")
    taxa=[x for x in d if literal(x)!="title"]
    if len(taxa)!=41:
        raise ValueError("STAGE72C_2018_VOC_SOURCE_SPECIES_SHEET_COUNT_CHANGED")
    output=[]
    for t in taxa:
        entries=[];names=set()
        for rownum,row in sorted(d[t].items()):
            if rownum==1:continue
            name=str(row.get(0,"")).strip()
            n=safe_float(row.get(1,""))
            if not name or n is None or n==0:continue
            names.add(name)
            entries.append(n)
        output.append({
            "original_figshare_VOC_plant_sheet_literal":t,
            "original_VOC_source_positive_compound_emission_rows":len(entries),
            "original_VOC_source_distinct_compound_names":len(names),
            "original_VOC_total_emission_ng_per_g_per_hour":sum(entries) if entries else "",
            "measured_source_zero_not_same_as_unlisted_compound_absence":1,
        })
    if sum(r["original_VOC_source_positive_compound_emission_rows"] for r in output)!=955:
        raise ValueError("STAGE72C_SOURCE_955_POSITIVE_VOC_ROWS_CHANGED")
    return output

def strict_join(network,voc):
    a={literal(n["original_network_plant_literal"]):n for n in network}
    b={literal(v["original_figshare_VOC_plant_sheet_literal"]):v for v in voc}
    if len(a)!=len(network) or len(b)!=len(voc):
        raise ValueError("STAGE72C_SOURCE_LITERAL_PLANT_NAME_DUPLICATE")
    shared=sorted(set(a)&set(b))
    missing_a=sorted(set(a)-set(b));missing_b=sorted(set(b)-set(a))
    joint=[]
    for key in sorted(a):
        n=a[key];v=b.get(key)
        joint.append({
          "original_network_plant_name":n["original_network_plant_literal"],
          "original_VOC_plant_sheet_name_if_exact":v["original_figshare_VOC_plant_sheet_literal"] if v else "",
          "source_strict_literal_name_VOC_match":int(v is not None),
          "original_2018_nonzero_visitor_links":n["author_original_nonzero_visitor_links"],
          "original_2018_visitor_event_counts":n["author_original_visitor_event_count"],
          "original_2018_bombus_literal_genus_visitor_counts":n["Bombus_genus_literal_taxon_name_visitor_rows_without_guild_inference"],
          "original_2018_source_positive_VOC_compound_rows":v["original_VOC_source_positive_compound_emission_rows"] if v else "",
          "original_2018_source_sum_VOC_emission_ng_g_h":v["original_VOC_total_emission_ng_per_g_per_hour"] if v else "",
          "original_spatial_UV_guide_measured_in_these_workbooks":"NO",
          "original_flower_field_abundance_control_in_these_workbooks":"NOT_VERIFIED",
          "genuine_source_region":"Lesvos scrubland, Greece",
          "original_cross_region_independent_replication":"NO",
        })
    summary={
      "source_network_plant_species":len(a),
      "source_species_specific_VOC_sheets":len(b),
      "strict_original_literal_species_overlap":len(shared),
      "network_only_original_plant_names":missing_a,
      "VOC_only_original_plant_names":missing_b,
      "n_original_species_with_actual_source_network_visits_and_positive_VOC_emission":
           sum(r["source_strict_literal_name_VOC_match"]==1 and
               r["original_2018_visitor_event_counts"]>0 and
               r["original_2018_source_positive_VOC_compound_rows"]>0 for r in joint),
      "all_plant_species_source_verified_not_only_title_screening":True,
      "source_synonym_and_spelling_reconciliation_not_automated":True,
      "original_UV_reflectance_spectrum_coordinates_not_extracted_from_ref28":True,
      "original_2017_2018_same_community_not_independent_source_regions":True,
    }
    return joint,summary

def write(rows,out):
    with Path(out).open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader();w.writerows(rows)

def run(out):
    network=fetch_original("network");voc=fetch_original("voc")
    nw,n= reconstruct_network(network)
    vx= original_voc_species(voc)
    joined,j=strict_join(nw,vx)
    out.mkdir(exist_ok=True,parents=True)
    write(joined,out/"2018_original_Lesvos_true_network_VOC_species_strict_crosswalk.csv")
    receipt={
       "schema":"stage72c_original_Lesvos_Kantsa2018_raw_41x168_network_x_41_VOC_measured_source",
       "original_2018_article":"10.1038/s41467-018-03448-w",
       "original_Figshare_DOI":"10.6084/m9.figshare.5663455.v2",
       "source_network_SHA256":SOURCE_FILES["network"]["sha256"],
       "source_VOC_SHA256":SOURCE_FILES["voc"]["sha256"],
       "original_network_matrix_replay":n,
       "original_plant_scent_visits_source_overlap":j,
       "not_pooled_new_global_ecology_effect":True,
       "any_null_as_biological_absence_inferred":False,
       "species_trait_source_site_coincidence":"SAME_COMMUNITY_NOT_SPECIMEN_MAPPED",
       "floral_UV_reflectance_original_2017_ref28_bytes_not_acquired":True,
       "VOC_stated_emission_rates_are_not_atmospheric_wind_speed":True,
       "species_level_strength_unstandardized_by_flowers_or_effort":True,
    }
    (out/"stage72c_original_raw_network_VOC_crosswalk_receipt.json").write_text(
        json.dumps(receipt,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("STAGE72C_ORIGINAL_FIELD_NETWORK_SAME_STUDY_VOC_STRICT_CROSSWALK",
          json.dumps(receipt,ensure_ascii=False,sort_keys=True))
    print("ORIGINAL_SOURCE_VISITS_7954_NOT_PUBLISHED_7955_NO_INVENTED_EVENT")
    return receipt

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--outdir",required=True,type=Path)
    a=p.parse_args()
    run(a.outdir)
if __name__=="__main__":main()
