"""Stage81A: read REAL Ohashi et al. 2015 219-taxon source ZIP, inspect 28 EuPP matches.

This deliberately discovers the original 20,490 xls/xlsx structure before
naming spectral columns or inferring a bee-visible change from the filename.
Uses original public author's 285,933,377-byte archive, checks MD5/SHA256,
verifies Stage79D authored overlap SHA and lists ORIGINAL source XLS schema.
Only a small provenance/structure receipt is uploaded, not 286MB of spectra.
"""
from __future__ import annotations
import argparse,hashlib,io,json,re,sys,tempfile,urllib.request,zipfile
from collections import Counter,defaultdict
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]/"floral_macro_stage79"
sys.path.insert(0,str(BASE))
from ohashi_2015_zip_central_directory_species_coverage import (
   download_author_full_verified,original_folders,original_folders as _folders
)
PINNED_SOURCE_SHA256="860ad9ef71d99efdda441fae00090ddb1dad0145f5c54a04b581b09490e718b7"
PINNED_PUBLISHED_SPECIES=219
PINNED_CROSSWALK_COUNT=28
README_URL="https://zenodo.org/api/records/4942515/files/README_for_Ohashi_etal.txt/content"

def source_archive_crosswalk(z:zipfile.ZipFile,author_species:list[str]):
    names=[q.filename for q in z.infolist()]
    folder_names,exact,infra,unresolved=original_folders(names)
    if len(folder_names)!=PINNED_PUBLISHED_SPECIES:
        raise ValueError("STAGE81A_NOT_219_AUTHOR_SCREENED_FLORAL_TAXA")
    matched={n:exact[n] for n in author_species if n in exact}
    if len(matched)!=PINNED_CROSSWALK_COUNT or set(author_species)!=set(matched):
        raise ValueError("STAGE81A_28_ORIGINAL_ACCEPTED_TAXA_NOT_CROSSWALKED_EXACTLY")
    paths=defaultdict(list)
    for f in z.infolist():
        if not f.filename.lower().endswith((".xls",".xlsx")):continue
        chunks=[c for c in f.filename.replace("\\","/").strip("/").split("/") if c]
        for i,c in enumerate(chunks):
            if c.casefold()=="reflectance" and i+2<len(chunks):
                paths[chunks[i+1]].append(f)
                break
    info=[]
    for name,folder in matched.items():
        arr=sorted(paths[folder],key=lambda x:x.filename)
        if not arr:raise ValueError("STAGE81A_AUTHENTIC_TAXON_WITHOUT_SPECTRAL_SHEETS_"+name)
        stems=[Path(x.filename).stem for x in arr]
        info.append({
           "original_species_literal":name,
           "original_directory":folder,
           "n_original_spectral_workbooks":len(arr),
           "extensions":dict(Counter(Path(x.filename).suffix.lower() for x in arr)),
           "source_file_size_bytes_min":min(x.file_size for x in arr),
           "source_file_size_bytes_max":max(x.file_size for x in arr),
           "sample_first_12_original_filenames":[Path(x.filename).name for x in arr[:12]],
           "file_stem_parent_patterns":dict(Counter(re.sub(r"\d+","#",s) for s in stems).most_common(12)),
        })
    return info,matched,paths

def preview_single_sheet(z:zipfile.ZipFile,info:zipfile.ZipInfo):
    """Only schema preview, never substitute a preview for full species analysis."""
    extension=Path(info.filename).suffix.casefold()
    src=z.read(info)
    if extension==".xls":
        import xlrd
        book=xlrd.open_workbook(file_contents=src)
        out=[]
        for sheet in book.sheets()[:2]:
            rows=[[str(sheet.cell_value(i,j))[:100] for j in range(min(sheet.ncols,9))]
                  for i in range(min(sheet.nrows,12))]
            out.append({"sheet_name":sheet.name,"nrows":sheet.nrows,"ncols":sheet.ncols,
                        "first_12_rows_max9cols":rows})
    else:
        from openpyxl import load_workbook
        b=load_workbook(io.BytesIO(src),read_only=True,data_only=True)
        out=[]
        for sheet in b.worksheets[:2]:
            rows=[["" if v is None else str(v)[:100] for v in row[:9]]
                  for row in list(sheet.iter_rows(min_row=1,max_row=min(sheet.max_row,12),values_only=True))]
            out.append({"sheet_name":sheet.title,"nrows":sheet.max_row,"ncols":sheet.max_column,
                        "first_12_rows_max9cols":rows})
        b.close()
    return {"source_original_filename":info.filename,
      "source_workbook_SHA256":hashlib.sha256(src).hexdigest(),
      "source_bytes":len(src),"parsed_sheet_previews":out}

def author_readme():
    try:
        r=urllib.request.Request(README_URL,headers={"User-Agent":"original-floral-spectra-research-2026"})
        with urllib.request.urlopen(r,timeout=35) as f:raw=f.read(20000)
        if not raw or len(raw)>12000:raise ValueError("README_UNEXPECTED_SIZE")
        return {"access":"RETRIEVED","sha256":hashlib.sha256(raw).hexdigest(),
          "first_90_original_lines":raw.decode("utf-8-sig",errors="replace").splitlines()[:90]}
    except Exception as e:
        return {"access":"UNAVAILABLE_NOT_TRAIT_ABSENCE","reason":type(e).__name__}

def run(overlap_path:Path,outdir:Path):
    prior=json.loads(overlap_path.read_text())
    if prior.get("original_full_source_SHA256")!=PINNED_SOURCE_SHA256:
        raise ValueError("STAGE81A_PREVIOUS_AUTHOR_SOURCE_SHA_CHANGED")
    species=prior["exact_measured_species_with_2025_EuPP_visit_names"]
    if len(species)!=PINNED_CROSSWALK_COUNT:raise ValueError("STAGE81A_NOT_28_AUTHOR_SOURCE_EXACT_NAMES")
    with tempfile.TemporaryDirectory() as folder:
        zipfile_=Path(folder)/"Ohashi_etal.zip"
        receipt=download_author_full_verified(zipfile_)
        if receipt["original_full_source_SHA256"]!=PINNED_SOURCE_SHA256:
            raise ValueError("STAGE81A_TRUE_AUTHOR_FULL_ZIP_HASH_CHANGED")
        with zipfile.ZipFile(zipfile_) as z:
            struct,matched,sheets=source_archive_crosswalk(z,species)
            preview=[]
            selected=("caltha palustris","lythrum salicaria","wisteria floribunda",
               "trifolium pratense","lamium purpureum","taraxacum officinale")
            for s in selected:
                if s not in matched:continue
                for f in sorted(sheets[matched[s]],key=lambda x:x.filename)[:2]:
                    try:preview.append(preview_single_sheet(z,f))
                    except Exception as e:
                        preview.append({"source_original_filename":f.filename,
                          "source_status":"READ_FAILED_NOT_BIOLOGICAL_TRAIT_ABSENCE",
                          "error_type":type(e).__name__,"error_detail":str(e)[:180]})
            report={
                "schema":"stage81a_pinned_2015_author_28_crosswalk_filename_excel_layout_probe",
                "original_source_metadata":receipt,
                "original_eupp_exact_overlap":struct,
                "original_workbook_schema_previews":preview,
                "original_published_species_screened":219,
                "original_published_bee_perceptible_changes":48,
                "original_published_no_significant_bee_colour_change":120,
                "original_published_significant_but_subthreshold_bee_colour_change":51,
                "source_name_crosswalk_not_source_verified_bee_visible_classification":True,
                "source_no_wild_Europe_field_optics_or_scent_or_landing":True,
                "no_new_biological_effect_or_measured_receptor_perceptual_state_yet":True,
                "original_source_readme":author_readme(),
            }
    outdir.mkdir(parents=True,exist_ok=True)
    (outdir/"stage81a_original_ohashi_28_workbook_stage_layout.json").write_text(
       json.dumps(report,sort_keys=True,ensure_ascii=False,indent=2)+"\n")
    print("STAGE81A_REAL_OHASHI_28_ORIGINAL_EXCEL_STAGE_PROBE",json.dumps({
      "original_source_sha":receipt["original_full_source_SHA256"],
      "number_source_taxa":len(struct),
      "source_spectral_workbooks_in_28":sum(x["n_original_spectral_workbooks"] for x in struct),
      "preview_count":len(preview),
      "source_readme":report["original_source_readme"]["access"],
    },sort_keys=True))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--stage79d-overlap",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    x=p.parse_args()
    run(x.stage79d_overlap,x.outdir)
