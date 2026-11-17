"""Stage58: authentic VOC original DataSheet_1 unit/row, species/source identity audit.

The live source XLSX has 4461 rows x 913 columns, NOT necessarily
"4460 independent species". Published 305-species analysis subframe
may involve filtering primary papers/specimens; original source rows
must not be interpreted as 4460 independent VOC profiles.
Pollination mode column header 'wind' is WIND POLLINATION, not local
wind speed or plume airflow! Atmospheric wind m/s is not supplied.
Do not combine wind POLLINATION with climate-mediated dispersion.
No raw source rows archived, just counts and source geometry receipts.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from pathlib import Path
import hashlib, io, json, urllib.error, zipfile
from openpyxl import load_workbook
from inspect_original_VOC305_workbooks import download_source,MEMBERS

NAME="DataSheet_1.xlsx"
EXPECTED_ROWS=4461
EXPECTED_COLUMNS=913
N_METADATA_COLUMNS=26

def audit_bytes(blob):
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        candidates=[x for x in z.infolist() if not x.is_dir()
                    and Path(x.filename).name==NAME]
        if len(candidates)!=1:
            raise ValueError("NO_GO_VOC305_ORIGINAL_PRESENCE_WORKBOOK_NOT_UNIQUE")
        raw=z.read(candidates[0])
    if hashlib.sha256(raw).hexdigest()!=MEMBERS[NAME]:
        raise ValueError("NO_GO_VOC305_PRESENCE_ORIGINAL_INNER_SOURCE_CHANGED")
    book=load_workbook(io.BytesIO(raw),read_only=True,data_only=True)
    if len(book.worksheets)!=1:
        raise ValueError("NO_GO_VOC305_ORIGINAL_PRESENCE_MULTI_SHEET")
    ws=book.worksheets[0]
    if (ws.max_row,ws.max_column)!=(EXPECTED_ROWS,EXPECTED_COLUMNS):
        raise ValueError("NO_GO_VOC305_PRESENCE_AUTHOR_SOURCE_DIMENSION_CHANGED")
    row_iter=ws.iter_rows(values_only=True)
    head=next(row_iter)
    if list(head[:4])!=["Source article","Species","APG III synonims","wind"]:
        raise ValueError("NO_GO_VOC305_SOURCE_POLLINATION_MODE_HEADER_CHANGED")
    source_species=Counter()
    perstudy=Counter()
    aliases=Counter()
    mode=Counter()
    source_n=0
    second_value=Counter()
    empty_source=0
    matrix_nonempty=0
    for row in row_iter:
        source_n+=1
        species=str(row[1] or "").strip()
        article=str(row[0] or "").strip()
        if not species:
            empty_source+=1
            continue
        source_species[species]+=1
        if article:perstudy[article]+=1
        if row[2] and str(row[2]).strip():
            aliases[str(row[2]).strip()]+=1
        for label,value in (("wind_pollination_flag",row[3]),("animal_pollination_flag",row[4]),
                            ("insect_flag",row[5]),("lepidoptera_flag",row[6]),
                            ("diptera_flag",row[8]),("hymenoptera_flag",row[9]),
                            ("bat_flag",row[10]),("bird_flag",row[11])):
            if value not in ("",None):
                mode[label]+=1
        if row[3] not in ("",None):
            second_value[str(row[3])]+=1
        # This is source-table cell nonmissingness, NOT a measurement of
        # compound presence; "0" may have a study-specific coding meaning.
        matrix_nonempty+=sum(v not in ("",None) for v in row[30:])
    book.close()
    examples=sorted(source_species,key=lambda s:s.casefold())[:20]
    top=sorted(source_species.items(),key=lambda x:(-x[1],x[0]))[:12]
    return {
       "status":"ORIGINAL_FARRE_2020_PRESENCE_SOURCE_SPECIES_STUDY_GRAIN_AUDIT",
       "source_DOI":"10.3389/fpls.2020.01154",
       "source_original_presence_inner_SHA256":MEMBERS[NAME],
       "n_source_excel_rows_including_header":EXPECTED_ROWS,
       "n_original_source_data_rows":source_n,
       "n_data_rows_without_species_label":empty_source,
       "n_distinct_verbatim_species_labels":len(source_species),
       "n_species_labels_with_multiple_original_rows":sum(n>1 for n in source_species.values()),
       "maximum_source_rows_per_species_label":max(source_species.values()) if source_species else 0,
       "n_distinct_source_article_strings":len(perstudy),
       "n_named_source_synonym_rows":sum(aliases.values()),
       "source_wind_pollination_flag_nonempty_values":dict(sorted(second_value.items())),
       "source_receptor_pollination_mode_nonempty_row_counts":dict(sorted(mode.items())),
       "nonempty_cells_in_trailing_VOC_or_metadata_columns_not_species_count":matrix_nonempty,
       "source_header_first_70_original_column_names":list(str(v)[:85] if v is not None else "" for v in head[:70]),
       "source_header_last_12_original_column_names":list(str(v)[:85] if v is not None else "" for v in head[-12:]),
       "first_20_species_source_names_for_taxonomy_review":examples,
       "top_12_repeated_source_taxon_labels":[{"name":s,"source_rows":n} for s,n in top],
       "source_305_published_analysis_species_count_not_assumed_equal_to_XLSX_rows":True,
       "source_wind_column_is_pollination_mode_NOT_atmospheric_wind_speed":True,
       "no_live_airflow_or_plume_measurements_inferred":True,
       "source_VOC_missing_not_odor_absence":True,
       "no_817_multimodal_GBIF_accepted_overlap_claimed_yet":True,
    }

def main():
    p=Path("stage58_original_VOC_305_source_grain")
    p.mkdir(exist_ok=True)
    try:
        report=audit_bytes(download_source())
    except (ValueError,urllib.error.URLError,urllib.error.HTTPError,
            TimeoutError,zipfile.BadZipFile) as err:
        report={"status":"VOC305_ORIGINAL_DATA_GRAIN_NOT_VERIFIED_NO_FALSE_SPECIES_COUNTS",
                "source_DOI":"10.3389/fpls.2020.01154",
                "error_type":type(err).__name__,
                "error_detail":str(err)[:220]}
    (p/"original_VOC_wind_pollination_vs_airflow_species_grain_receipt.json").write_text(
        json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf8")
    print("STAGE58_ORIGINAL_VOC305_SPECIES_STUDY_WIND_POLLLINATION_GRAIN",
          json.dumps(report,sort_keys=True,ensure_ascii=False))
    print("NO_WIND_M_PER_SECOND_OR_CROSS_STUDY_POLLEN_OR_PLANT_TRAIT_SELECTION_ESTIMATED")
if __name__=="__main__":
    main()
