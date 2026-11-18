"""Stage79F: MACRO source opportunity for wind-dependent decision-stage signals.

Actually source-reviewed positive FCC plant names (2025 Rezende 151 reported,
144 exact-binomial names parsed, 9 strict EuPPollNet overlaps), independent
NHM botanical petal width/orientation/marking source from original 59,369
taxa (118 original field-visited taxa with petal max width, 31 with positive
patterns), original corrected EuPPollNet 18,798 species-by-network-year units.

This AUDITS feasibility before opening bee visitor response/gust exposure.
It never uses source unreported floral change/nectar guide as a negative.
Species are repeated; studies and networks are not independent evolutionary
replications; petal width is not real total floral display.
"""
from __future__ import annotations
import argparse,csv,hashlib,json
from collections import Counter,defaultdict
from pathlib import Path

PINS={
 "farnear":"39e89f3d20410e1d54d1b366e62fd3362878bab12815835282731e224f65a1f7",
 "fcc":"c6bc8b499e67545ef997766f35abe2a9074c52077ae84ab2818b3376529f3683",
 "roster":"475863c2b193dd9c1eaad848dae05a9f518b57446cad2661979ca582c7d88617",
}
# PINS 'farnear' and 'fcc' are Actions ZIP artifact digests, not the source
# individual JSON/CSV file hashes. Verify their original provider action
# artifact identity in the CI retrieval step, not against member bytes.

def source_row(path):
    return list(csv.DictReader(Path(path).open(encoding="utf-8",newline="")))

def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def key(r):
    return (r["Study_id"],r["Network_id"],r["Year"])

def index_source(reference,source_rows):
    mapped={t:set() for t in reference}
    for r in source_rows:
        name=r["Original_plant_accepted_name_literal"].strip().casefold()
        if name in mapped:
            mapped[name].add((r["Study_id"],r["Network_id"],r["Year_from_original_date"]))
    return mapped

def analyze(far,nearrows,positive,roster):
    assert far["original_plant_species_recorded_in_field_visits"]==1408
    assert far["original_source_species_with_petal_MAX_width_cm"]==118
    assert far["original_source_species_with_positive_pattern_text"]==31
    assert far["original_field_network_year_keys_in_accepted_plant_roster"]==1862
    assert positive["source_original_species_table_parsing"]["exact_two_token_source_candidate_species_names"]==144
    sourceFCC=set(positive["source_exact_name_join_to_original_visit_roster"]
                       ["source_original_positive_FCC_exact_plant_names"])
    if len(sourceFCC)!=9:raise ValueError("STAGE79F_ORIGINAL_9_FCC_POSITIVE_EUPP_TAXA_CHANGED")
    bynetwork=defaultdict(list)
    visited=defaultdict(set)
    for row in roster:
        site=(row["Study_id"],row["Network_id"],row["Year_from_original_date"])
        visited[row["Original_plant_accepted_name_literal"].strip().casefold()].add(site)
    for row in nearrows:
        bynetwork[key(row)].append(row)
    width_species={
        r["original_plant_literal_accepted_name"].strip().casefold()
        for r in nearrows if r["source_petal_max_width_cm"] not in ("",None)}
    motif_species={
        r["original_plant_literal_accepted_name"].strip().casefold()
        for r in nearrows if str(r["source_positive_marking_text_only"])=="1"}
    original_networks={(r["Study_id"],r["Network_id"],r["Year_from_original_date"])
                       for r in roster}
    pernet=[]
    anyfcc=set()
    panels=defaultdict(set)
    for k in sorted(original_networks):
        rowset=bynetwork.get(k,[])
        sizes=[(r["original_plant_literal_accepted_name"].strip().casefold(),
                float(r["source_petal_max_width_cm"]))
               for r in rowset if r["source_petal_max_width_cm"] not in ("",None)]
        marks={r["original_plant_literal_accepted_name"].strip().casefold()
               for r in rowset if str(r["source_positive_marking_text_only"])=="1"}
        fcc={s for s in sourceFCC if k in visited[s]}
        if fcc:anyfcc.add(k)
        haswidth=len(sizes)>=2 and len({v for s,v in sizes})>=2
        hasmarked=bool(marks)
        hasFCC=bool(fcc)
        flags={
          "has_distinct_petal_width_comparison":haswidth,
          "has_positive_reported_near_pattern":hasmarked,
          "has_positive_reported_colorchange":hasFCC,
          "has_distinct_width_AND_positive_pattern":haswidth and hasmarked,
          "has_distinct_width_AND_positive_colorchange":haswidth and hasFCC,
          "has_positive_pattern_AND_positive_colorchange":hasmarked and hasFCC,
          "has_all_three_sources":haswidth and hasmarked and hasFCC
        }
        for attr,val in flags.items():
            if val:panels[attr].add(k)
        pernet.append({"Study_id":k[0],"Network_id":k[1],"Year":k[2],
          "source_plant_species_with_width_cm":len(sizes),
          "source_NHM_positive_pattern_species":len(marks),
          "source_2025_positive_FCC_species":len(fcc),
          **{label:int(v) for label,v in flags.items()},
          "original_reported_FCC_negative_states_ever_measured":0,
          "source_Bombus_guild_chosen_before_cohort":0,
          "source_ERA5_gust_chosen_before_cohort":0})
    fccstudy={
       s:{"source_original_visiting_network_count":len(visited[s]),
          "source_original_study_ID_count":len({k[0] for k in visited[s]}),
          "original_NHM_petal_width_available":s in width_species,
          "original_NHM_positive_pattern":s in motif_species}
       for s in sorted(sourceFCC)}
    if len(anyfcc)!=453:
        raise ValueError("STAGE79F_ORIGINAL_453_FCC_POSITIVE_VISITED_NETWORKS_CHANGED")
    return {
      "schema":"stage79f_original_rezende_FCC_2025_and_NHM_distal_petal_width_positive_pattern_source_EUPP",
      "source_original_EuPP_accepted_plant_species":1408,
      "source_original_corrected_EuPP_plant_field_network_keys":len(original_networks),
      "source_reviewed_FCC_article_positive_151_species":151,
      "source_PDF_reconstructed_exact_binomial_positive_FCC_species":144,
      "original_FCC_source_exact_visited_taxa":len(sourceFCC),
      "source_PDF_7_unresolved_names_NOT_counted_as_negative_or_true_absence":True,
      "source_original_source_petal_width_species":len(width_species),
      "source_original_reported_pattern_positive_species":len(motif_species),
      "source_original_FCC_positive_species_with_petal_width":len(sourceFCC&width_species),
      "source_original_FCC_positive_species_with_pattern_positive":len(sourceFCC&motif_species),
      "source_original_FCC_vs_petal_width_overlapping_names":sorted(sourceFCC&width_species),
      "source_original_FCC_vs_pattern_overlapping_names":sorted(sourceFCC&motif_species),
      "source_original_signal_opportunity_networks":{
           t:len(nets) for t,nets in panels.items()},
      "source_original_signal_opportunity_studies":{
           t:len({k[0] for k in nets}) for t,nets in panels.items()},
      "source_FCC_positive_species_study_and_network_reuse":fccstudy,
      "no_original_source_validated_FCC_absent_vs_present_comparison":True,
      "no_original_source_verified_UV_guide_negative_vs_positive":True,
      "source_bird_honeybee_or_Bombus_identity_cannot_be_inferred_from_flower_color":True,
      "true_visual_signal_by_strong_gust_ordered_beta_estimated":False,
      "source_colourchange_reward_state_not_directly_known":True,
      "source_petal_width_is_NOT_total_distant_visual_display_size":True,
    },pernet

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--far-near-original-receipt",type=Path,required=True)
    p.add_argument("--far-near-original-plant-networks",type=Path,required=True)
    p.add_argument("--fcc-original-positive-receipt",type=Path,required=True)
    p.add_argument("--original-EuPP-source",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args()
    if hashlib.sha256(a.original_EuPP_source.read_bytes()).hexdigest()!=PINS["roster"]:
        raise ValueError("STAGE79F_ORIGINAL_GUILD_SPECIES_ROSTER_NOT_SOURCE_SHA_PINNED")
    data,rows=analyze(read(a.far_near_original_receipt),
                      source_row(a.far_near_original_plant_networks),
                      read(a.fcc_original_positive_receipt),
                      source_row(a.original_EuPP_source))
    a.outdir.mkdir(exist_ok=True,parents=True)
    (a.outdir/"stage79f_true_original_FCC_size_marking_crosssource_coverage.json").write_text(
        json.dumps(data,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    with (a.outdir/"stage79f_source_network_signal_positive_coverage.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    print("STAGE79F_REAL_SOURCE_DISTANT_SIZE_NEAR_MARKING_FCC_GUILD_OPPORTUNITY",
          json.dumps(data,sort_keys=True))
if __name__=="__main__":
    main()
