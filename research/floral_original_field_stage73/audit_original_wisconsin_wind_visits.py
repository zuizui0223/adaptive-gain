"""Stage73B: source-authenticated Wisconsin 2022 field VISITS × wind × floral traits.

Original field study Cammarano et al., four sites in Wisconsin USA.
DO NOT infer UV spatial nectar guides, objectively measured reflectance or VOC
from author literature-based categorical petal colour/wavelength-scale labels.
Wind Beaufort is the original observational ordinal source covariate, not
a manipulated treatment. Excel is source-original, Git blob SHA verified.

Only initial field-source workbook structure/coverage audit; do not attach
visitor rows to wind until the original plot/date/site composite keys have
been audited. No pseudo-zero visitor records imputed.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,sys,urllib.request
from collections import Counter,defaultdict
from pathlib import Path

REPO="Plant-herbivory-interaction-lab/CammaranoMonardaPollinator2024"
SOURCE_PATH="Data/Pollination_neighborhood_data21.xlsx"
SOURCE_GIT_BLOB_SHA1="d456ddae4b5a737fc3351a5df612bd6a4b2c6244"
SOURCE_BYTES=69522
SOURCE_URL=("https://raw.githubusercontent.com/"+REPO+"/main/"+SOURCE_PATH)
SOURCE_DOI_STATUS="NATURAL_AREAS_JOURNAL_ACCEPTED_2024_AUTHOR_REPO"
EXPECTED_SHEETS=("plots","plants","visitors","plant_spp_traits","visitor_spp_traits")

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"floral_original_field_stage72"))
from replay_original_kantsa2018_network_voc import read_xlsx_sparse

def gitblob_sha(raw):
    return hashlib.sha1(f"blob {len(raw)}\0".encode()+raw).hexdigest()

def download_original_excel():
    req=urllib.request.Request(SOURCE_URL,headers={"User-Agent":
                            "adaptive-gain-Wisconsin-original-author-repository-wind-and-visitors/2026-11-17"})
    with urllib.request.urlopen(req,timeout=40) as res:
        raw=res.read(SOURCE_BYTES+1)
    if len(raw)!=SOURCE_BYTES or gitblob_sha(raw)!=SOURCE_GIT_BLOB_SHA1:
        raise ValueError("STAGE73B_AUTHENTIC_WISCONSIN_ORIGINAL_GIT_SOURCE_CHANGED")
    return raw

def normalize_key(s):
    return " ".join(str(s).strip().casefold().split())

def table_from_sheet(rows):
    if not rows:return [],[]
    # Expect author header at the first original nonempty row.
    first=min(rows)
    head=rows[first]
    max_col=max(head)
    names=[head.get(i,"") for i in range(max_col+1)]
    return names,[
        {names[i] or f"UNLABELLED_COL_{i+1}":v for i,v in r.items()
         if i<len(names)}
        for rownum,r in sorted(rows.items()) if rownum>first
    ]

def summarize_sheet(name,rows):
    headers,data=table_from_sheet(rows)
    report={
      "author_source_sheet":name,
      "source_nonempty_excel_rows_including_header":len(rows),
      "assumed_header_original_first_nonempty_row":min(rows) if rows else None,
      "source_original_header_names_first50":headers[:50],
      "source_data_rows_nonempty_after_header":len(data),
      "sample_first_three_data_rows":[
          {k:str(v)[:110] for k,v in row.items()} for row in data[:3]],
      "source_missing_or_ambiguous_row_identifiers_not_filled":True,
    }
    cols=defaultdict(list)
    for row in data:
        for col,value in row.items():cols[col].append(value)
    report["source_per_column_nonmissing_counts"]=dict(
         sorted(((k,len(v)) for k,v in cols.items()),key=lambda x:x[0]))
    report["source_per_column_distinct_literal_counts"]=dict(
         sorted(((k,len({normalize_key(t) for t in v})) for k,v in cols.items()),key=lambda x:x[0]))
    for field in ("wind","temp","site","date","plot","start","end",
                  "petal_color","petal_wvl","flower_sp","visitor_sp"):
        match=[k for k in cols if normalize_key(k)==field]
        if match:
            sourcefield=match[0]
            values=cols[sourcefield]
            report[f"original_{field}_distinct_value_sample"]=sorted({str(v) for v in values})[:24]
            report[f"original_{field}_raw_nonempty_count"]=len(values)
    return report

def run():
    source=download_original_excel()
    books=read_xlsx_sparse(source)
    if not set(EXPECTED_SHEETS).issubset({normalize_key(k) for k in books}):
        raise ValueError("STAGE73B_AUTHOR_ORIGINAL_FIVE_REQUIRED_SHEETS_NOT_PRESENT")
    d=[summarize_sheet(k,v) for k,v in books.items()]
    report={
      "schema":"stage73b_source_original_Wisconsin_four_field_sites_wind_visitors_color_record_grain",
      "source_repo":REPO,"original_source_Excel":SOURCE_PATH,
      "original_Git_blob_SHA1":SOURCE_GIT_BLOB_SHA1,
      "actual_source_SHA256":hashlib.sha256(source).hexdigest(),
      "source_authentic_bytes":len(source),
      "source_sheet_count":len(d),
      "source_Excel_sheets":d,
      "field_study_sites_published_author_readme":4,
      "source_sampling_year_published_author_readme":2022,
      "wind_is_beaufort_ordinal_field_observation":True,
      "petal_wvl_is_ordinal_literature_color_NOT_spectrometric_nm":True,
      "source_plot_date_site_keys_not_yet_validated":True,
      "visitor_zeros_are_not_inferred_from_absent_rows":True,
      "source_no_original_UV_spatial_guide":True,
      "original_source_wind_and_visits_association_fitted":False,
      "source_is_independent_geographic_study_from_Lesvos_and_China":True,
    }
    return report

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args()
    result=run()
    a.outdir.mkdir(parents=True,exist_ok=True)
    (a.outdir/"original_wisconsin_2022_author_WIND_VISIT_FLORAL_WORKBOOK_coverage.json").write_text(
       json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True)+"\n",encoding="utf-8")
    print("STAGE73B_ORIGINAL_REAL_FIELD_WIND_FLOWER_VISITS_SOURCE_SCHEMA",
          json.dumps(result,ensure_ascii=False,sort_keys=True))
    print("NO_ORDINAL_PETAL_COLOR_AS_REFLECTANCE_NO_PSEUDOREPLICATION_NO_WIND_TREATMENT")
if __name__=="__main__":main()
