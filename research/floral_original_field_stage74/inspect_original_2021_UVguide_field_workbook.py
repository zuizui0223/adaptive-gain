"""Stage74C: inspect original field experimental UV guide design and reflectance.

Download original Finnell & Koski 2021 Zenodo authored content via official
file links; validate SHA independently reproduced in Stage74B. Parse original
Excel sheet field names and records, *not* PDF/table claims.

If exact source design is present, next iteration can reproduce visit choice
ratios at array-pair level without imputing unknown observed guild negatives.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import sys
import zipfile
from collections import Counter
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parent))
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"floral_original_field_stage72"))
from audit_original_2021_sensory_drive_Zenodo import (
    manifest_meta,record_files_metadata,pick_original_download_url,
    get,verify_original_author_digest,REFERENCE_DOI,PUBLICATION_DOI
)
from replay_original_kantsa2018_network_voc import read_xlsx_sparse,table_from_sheet

PIN={
 "FinnKosk_PollData_Final.xlsx":{
    "size":67593,
    "sha256":"d66d12f3dbfc83b3fe6e854b69f9e5f768a1c3f973c0db5368176e17264ace59"},
 "ColorContrastData.xlsx":{
    "size":16068,
    "sha256":"68d000362b9840a752f8e82cab005406eb81eaa4ab48f1e1ca8814829757ddd7"},
 "Spectra Used for Vismodels.zip":{
    "size":826745,
    "sha256":"1e849dd5374de206abeb192d543b14cea07dc0a385cf616fbe713de2bd7fea87"},
}
KEYS=("UV","elev","altitude","guide","array","pollin","background",
      "visits","count","first","bare","foliage","reflect","date","site")

def safe_source_download(filemeta):
    name=filemeta["key"]
    expected=PIN[name]
    url=pick_original_download_url(filemeta)
    if not url:raise ValueError("STAGE74C_AUTHOR_FILE_NO_ORIGINAL_DOWNLOAD_LINK")
    raw,final,mime=get(url,2_000_000)
    if len(raw)!=expected["size"]:
        raise ValueError("STAGE74C_ORIGINAL_FIELD_SOURCE_BYTES_CHANGED_"+name)
    sha=hashlib.sha256(raw).hexdigest()
    if sha!=expected["sha256"]:
        raise ValueError("STAGE74C_ORIGINAL_FIELD_SOURCE_SHA_CHANGED_"+name)
    valid,algo,source_sha=verify_original_author_digest(raw,filemeta.get("checksum",""))
    if not valid:raise ValueError("STAGE74C_AUTHORED_ZENODO_CHECKSUM_NOT_VALID")
    return raw,{"name":name,"sha256":sha,"bytes":len(raw),
                "author_digest_algorithm":algo}

def preview_sheets(raw,name):
    if not zipfile.is_zipfile(io.BytesIO(raw)):
        raise ValueError("STAGE74C_ORIGINAL_XLSX_NOT_ZIP_"+name)
    books=read_xlsx_sparse(raw)
    info=[]
    for sheet,rows in books.items():
        header,body=table_from_sheet(rows)
        row0=[{str(k+1):v for k,v in sorted(row.items())[:16]}
              for _,row in sorted(rows.items())[:7]]
        possible_fields=[
          h for h in header
          if any(t in h.lower() for t in KEYS)]
        hist=Counter()
        for row in body:
            for column,value in row.items():
                if any(t in str(column).lower() for t in KEYS):
                    hist[column]+=bool(str(value).strip())
        info.append({
          "author_sheet":sheet,
          "original_nonempty_excel_row_count":len(rows),
          "original_first_nonempty_row_number":min(rows) if rows else None,
          "first_nonempty_row_assumed_column_labels":header[:40],
          "candidate_source_field_labels":possible_fields,
          "original_first7_row_data":row0,
          "post_header_source_data_rows":len(body),
          "source_key_field_nonempty_record_counts":dict(hist),
          "numeric_exposure_or_visitor_zeros_NOT_imputed":True,
          "not_yet_analyzed_as_one_independent_population_per_row":True,
        })
    return info

def spectra_archive(raw):
    if not zipfile.is_zipfile(io.BytesIO(raw)):
        raise ValueError("STAGE74C_AUTHORED_ZENODO_NOT_ZIP")
    with zipfile.ZipFile(io.BytesIO(raw)) as f:
        files=[r for r in f.infolist() if not r.is_dir()]
        dirs=Counter()
        for row in files:
            path=row.filename.replace("\\","/")
            parts=path.split("/")
            dirs["/".join(parts[:2])]+=1
        return {
            "archive_member_count":len(files),
            "source_first40_members":[{"filename":x.filename,"bytes":x.file_size}
                                      for x in files[:40]],
            "source_original_subfolder_member_counts":dict(dirs),
            "original_field_spectrum_units_are_NOT_visitor_event_units":True,
        }

def run():
    meta,rec=manifest_meta()
    files=record_files_metadata(meta)
    listed={f.get("key",""):f for f in files}
    collected={}
    proofs={}
    for name in PIN:
        if name not in listed:
            raise ValueError("STAGE74C_ORIGINAL_ZENODO_LISTING_MISSING_"+name)
        raw,proof=safe_source_download(listed[name])
        collected[name]=raw
        proofs[name]=proof
    return {
      "schema":"stage74c_authentic_2021_UV_guide_background_visits_original_xlsx_grain",
      "source_original_article_DOI":PUBLICATION_DOI,
      "original_data_record_DOI":REFERENCE_DOI,
      "original_source_verified_checksums":proofs,
      "source_visits_Excel_sheets":preview_sheets(collected["FinnKosk_PollData_Final.xlsx"],"poll_visits"),
      "source_color_contrast_Excel_sheets":preview_sheets(collected["ColorContrastData.xlsx"],"color_contrast"),
      "source_77_member_Zenodo_spectra_zip":spectra_archive(collected["Spectra Used for Vismodels.zip"]),
      "source_design_reported_array_count_NOT_RECOMPUTED_YET":54,
      "source_design_reported_first_visits_NOT_RECOMPUTED_YET":377,
      "original_2021_Published_prior_experiment_not_new_scientific_novelty":True,
      "source_CI_validation_is_original_data_not_published_effect_reproduction":True,
      "source_single_plant_species_condition":True,
      "no_global_phylogenetic_visual_selection_or_wind_x_scent_claim":True
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args()
    a.outdir.mkdir(parents=True,exist_ok=True)
    data=run()
    (a.outdir/"author_2021_UVguide_original_experiment_workbook_source_structure.json").write_text(
      json.dumps(data,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    print("STAGE74C_REAL_ZENODO_AUTHOR_EXPERIMENT_FACTOR_AND_SPECTRAL_SOURCE",
          json.dumps(data,ensure_ascii=False,sort_keys=True))
    print("NO_MANUSCRIPT_FIRST_VISIT_COUNT_ASSUMED_AS_RAW_EXPERIMENT")
if __name__=="__main__":
    main()
