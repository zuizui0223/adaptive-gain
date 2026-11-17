"""Stage58: connect authentic floral VOC source 305 species to 817 visual atlas.

Original Farré-Armengol et al. 2020 (10.3389/fpls.2020.01154) source:
305 single named species rows in DataSheet_1.xlsx / 4460 Excel data rows
(with 4155 blank spreadsheet trailing rows). Original 3 workbooks and
the source metadata/pollination-mode grain previously independently verified
in Stage58. Each source name is author/primary-study-derived; the published
305 are not 305 directly manipulated plants with experimentally silenced
VOC. Original "wind" column is WIND POLLINATION, not meteorological wind.

Use original Stage57 817 GBIF-accepted botanical evidence names as join
reference: NEVER join by genus or assume absence of non-overlapping traits.
Only strict confident exact GBIF species matching + synonym acceptedUsageKey.
No local wind speed, odor plume, petal UV guide, flower visit, pollen,
causal interaction or contact-stage information in this crosswalk.

Result: source provenance + accepted-key MODALITY COVERAGE and overlap.
"""
from __future__ import annotations
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import argparse,csv,io,json,math,re,sys,zipfile,hashlib
from openpyxl import load_workbook

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"floral_visual_macro_stage49"))
from match_literature_visual_taxa_gbif import lookup
from inspect_original_VOC305_workbooks import download_source,MEMBERS

SHEET="DataSheet_1.xlsx"
EXPECTED=305
REFERENCE=817
BINOMIAL=re.compile(r"^[A-Z][a-zA-Z-]+ [a-z][a-zA-Z-]+$")

def authentic_source_305(blob):
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        matching=[x for x in z.infolist() if Path(x.filename).name==SHEET and not x.is_dir()]
        if len(matching)!=1:raise ValueError("NO_GO_VOC_ORIGINAL_PRESENCE_SHEET_ID")
        source=z.read(matching[0])
    if hashlib.sha256(source).hexdigest()!=MEMBERS[SHEET]:
        raise ValueError("NO_GO_VOC_ORIGINAL_MEASURED_SOURCE_SHA")
    wb=load_workbook(io.BytesIO(source),read_only=True,data_only=True)
    ws=wb.worksheets[0]
    if (ws.max_row,ws.max_column)!=(4461,913):
        raise ValueError("NO_GO_VOC_AUTHOR_ORIGINAL_PRESENCE_DIMENSION")
    itr=ws.iter_rows(min_col=1,max_col=23,values_only=True)
    header=next(itr)
    if list(header[:5])!=["Source article","Species","APG III synonims","wind","animal"]:
        raise ValueError("NO_GO_VOC_WIND_POLLINATION_NOT_METEOROLOGY_SOURCE")
    records=[]
    for source_row,r in enumerate(itr,start=2):
        species=str(r[1] or "").strip()
        if not species:continue
        words=species.split()
        candidate=" ".join(words[:2]) if len(words)>=2 else ""
        exact=bool(BINOMIAL.fullmatch(candidate))
        rec={
          "original_VOC_source_row":source_row,
          "original_VOC_source_taxon_verbatim":species,
          "original_VOC_source_canonical_binomial_or_unknown":candidate if exact else "",
          "original_VOC_published_article_citation_SHA256":hashlib.sha256(
                 str(r[0] or "").encode()).hexdigest(),
          "original_VOC_source_APG_synonym_literal":str(r[2] or "")[:100],
          "original_VOC_source_wind_POLLINATED_flag_or_UNKNOWN":(
               "wind_pollinated" if r[3]==1 or r[3]=="1" else "UNSPECIFIED"),
          "original_VOC_source_hymenoptera_guild_or_UNKNOWN":(
               "hymenoptera" if r[9]==1 or r[9]=="1" else "UNSPECIFIED"),
          "original_VOC_source_bird_guild_or_UNKNOWN":(
               "bird" if r[11]==1 or r[11]=="1" else "UNSPECIFIED"),
          "original_VOC_annual_mean_temp_K_or_unknown":r[12] if isinstance(r[12],(int,float)) else "",
          "original_VOC_annual_precip_mm_or_unknown":r[15] if isinstance(r[15],(int,float)) else "",
          "original_VOC_primary_original_source_DOI":"10.3389/fpls.2020.01154",
          "source_VOC_compiled_observations_NOT_odor_on_off_manipulation":True,
          "source_wind_column_NOT_airflow_velocity":True,
        }
        records.append(rec)
    wb.close()
    unique={r["original_VOC_source_taxon_verbatim"] for r in records}
    if len(records)!=EXPECTED or len(unique)!=EXPECTED:
        raise ValueError("NO_GO_305_SINGLE_SOURCE_SPECIES_WITH_UNIQUE_AUTHOR_NAME")
    return records

def attach_accepted(voc,accepted_lookup,visual):
    if len(voc)!=EXPECTED or len(visual)!=REFERENCE:
        raise ValueError("NO_GO_ORIGINAL_305_VOC_OR_817_VISUAL_SOURCE_FRAME")
    prior={str(r["gbif_accepted_species_key"]):r for r in visual}
    if len(prior)!=REFERENCE or not all(k.isdigit() for k in prior):
        raise ValueError("NO_GO_PRIOR_817_ACCEPTED_KEY_IDENTITY")
    rows=[]
    for r in voc:
        name=r["original_VOC_source_canonical_binomial_or_unknown"]
        match=accepted_lookup.get(name,{"taxonomy_status":"SOURCE_LEXICAL_BINOMIAL_UNRESOLVED"})
        key=match.get("gbif_accepted_usage_key")
        key=str(key) if isinstance(key,int) and key>0 else ""
        other=prior.get(key)
        rows.append({
          **r,
          "gbif_strict_taxonomic_match_status":match["taxonomy_status"],
          "gbif_accepted_species_key_or_unknown":key,
          "same_accepted_taxon_in_source_visual817":bool(other) if key else "",
          "source_measured_spatial_UV_pattern_or_unknown":(
             other["source_UV_pattern_directly_measured_or_unknown"] if other else ""),
          "same_source_taxon_Oliveira2025_numeric_UV":(
             other["original_Oliveira2025_UV_mean_source"] if other else ""),
          "same_source_taxon_Ohashi2015_age_spectra":(
             other["original_Ohashi2015_spectral_taxon_source"] if other else ""),
          "same_source_taxon_colorchange_reviewed":(
             other["original_2025_literature_colour_change_reported"] if other else ""),
          "candidate_joint_MODALITY_evidence_NOT_same_individual":bool(other) if key else False,
          "floral_VOC_unobserved_species_not_scentless":True,
          "source_visual_unobserved_species_not_without_guide":True,
        })
    accepted={r["gbif_accepted_species_key_or_unknown"] for r in rows
              if r["gbif_strict_taxonomic_match_status"]=="EXACT_CONFIDENT_SPECIES_MAPPED"}
    if "" in accepted:raise ValueError("NO_GO_CONFIDENT_ACCEPTED_ZERO")
    overlap=accepted&set(prior)
    allvisual=Counter()
    for r in rows:
        key=r["gbif_accepted_species_key_or_unknown"]
        if key not in overlap:continue
        if r["source_measured_spatial_UV_pattern_or_unknown"] in ("0","1"):
            allvisual["measured_UV_spatial_binary"]+=1
        if r["same_source_taxon_Oliveira2025_numeric_UV"] in (True,"True"):
            allvisual["quantitative_UV_mean"]+=1
        if r["same_source_taxon_Ohashi2015_age_spectra"] in (True,"True"):
            allvisual["source_age_spectra_folder"]+=1
        if r["same_source_taxon_colorchange_reviewed"] in (True,"True"):
            allvisual["positive_review_colourchange"]+=1
    return rows,{
      "status":"ORIGINAL_FARRE_305_VOC_SPECIES_STRICT_GBIF_ACCEPTED_TO_817_VISUAL_TRAIT_MODALITY_OVERLAP",
      "n_original_VOC_2020_named_species_source_rows":len(voc),
      "n_gbif_exact_name_lookups":len(accepted_lookup),
      "source_original_gbif_match_status_count":dict(sorted(
          Counter(r["gbif_strict_taxonomic_match_status"] for r in rows).items())),
      "n_original_VOC_source_exact_accepted_rows":sum(
          r["gbif_strict_taxonomic_match_status"]=="EXACT_CONFIDENT_SPECIES_MAPPED" for r in rows),
      "n_distinct_VOC_accepted_species":len(accepted),
      "n_prior_visual_source_accepted_species":REFERENCE,
      "n_accepted_VOC_species_also_in_visual_source817":len(overlap),
      "n_accepted_VOC_species_not_in_existing_visual817":len(accepted-set(prior)),
      "n_combined_visual817_and_VOC_accepted_botanical_source_UNION":len(set(prior)|accepted),
      "same_species_modalities_but_NOT_same_voucher_or_original_native_sample":dict(sorted(allvisual.items())),
      "original_305_VOC_2020_is_compiled_not_new_field_measurements":True,
      "source_wind_means_pollination_mode_not_airflow":True,
      "no_source_ambient_wind_speed_or_VOC_plume_values":True,
      "no_missing_scent_as_zero_and_no_missing_visual_as_zero":True,
      "no_identified_VOC_x_UV_x_Bombus_env_wind_pollen_interaction":True,
    }

def main():
    opts=argparse.ArgumentParser()
    opts.add_argument("--source-accepted-visual817",required=True)
    args=opts.parse_args()
    voc=authentic_source_305(download_source())
    with Path(args.source_accepted_visual817).open(encoding="utf8",newline="") as fp:
        visual=list(csv.DictReader(fp))
    names=sorted({r["original_VOC_source_canonical_binomial_or_unknown"] for r in voc
                 if r["original_VOC_source_canonical_binomial_or_unknown"]})
    with ThreadPoolExecutor(max_workers=5) as pool:
        match=dict(zip(names,pool.map(lookup,names)))
    rows,receipt=attach_accepted(voc,match,visual)
    out=Path("stage58_VOC305_visual817_source_accepted_overlap")
    out.mkdir(exist_ok=True)
    with (out/"FArre2020_305_original_VOC_source_accepted_to_817_visual_evidence.csv").open(
         "w",encoding="utf8",newline="") as fp:
        w=csv.DictWriter(fp,fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    (out/"original_VOC305_visual817_GBIF_accepted_overlap_receipt.json").write_text(
       json.dumps(receipt,ensure_ascii=False,sort_keys=True,indent=2)+"\n",
       encoding="utf8")
    print("STAGE58_ORIGINAL_305_VOC_TO_817_VISUAL_ACCEPTED_SOURCE_OVERLAP",
          json.dumps(receipt,ensure_ascii=False,sort_keys=True))
    print("NO_INTERPRETATION_OF_SOURCE_WIND_POLLINATION_AS_METEOROLOGICAL_WIND")
if __name__=="__main__":
    main()
