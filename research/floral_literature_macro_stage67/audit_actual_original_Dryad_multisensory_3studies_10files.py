"""Stage67 original 3 Dryad data archives: read REAL SOURCE bytes with digest.

Xie2025 island bee flower-colour interaction study, Coetzee2026 Erica
receiver-specific bee-avoidance/nectar-robbing study, and FloRes2022 floral
reward/corolla/phenology database. No FCP photos, artificial floral colour,
GBIF range stand-ins, or treating XLSX sheet columns as independent species.
Every file is an original Dryad version/fixed downloadable id and SHA256.
Metadata archive is the external original API version-file list 44038731710.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,re,urllib.request,zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

SOURCE_RUN=44038731710
ROOT="https://datadryad.org"
MAX_SOURCE_FILE=4_000_000
MAX_UNCOMPRESSED=15_000_000
ALLOWED={
  "Xie2025_flower_spectral_41_islands_and_bee_visits":{
    "bee_visitation_frequency_to_each_floral_color_within_each_island.xlsx",
    "flower_color_reflectance_spectra.xlsx",
    "plant_bee_interactions_on_islands.zip","README.md"},
  "Coetzee2026_Erica_64_species_receiver_contrast_nectar_robbing":{
    "Data_Is_bee-avoidance_driven_by_nectar_robbing__Data_Dryad_20Jan2026.xlsx",
    "Erica.population.spectra.1.csv","README.md"},
  "BadenBohm2022_FloRes_flower_phenology_nectar_pollen_tube":{
    "Data.zip","README.docx","Attachments.zip"}}
EXPECTED_FILES={
  "Xie2025_flower_spectral_41_islands_and_bee_visits":4,
  "Coetzee2026_Erica_64_species_receiver_contrast_nectar_robbing":3,
  "BadenBohm2022_FloRes_flower_phenology_nectar_pollen_tube":3}
XML="{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"

def check(cond,msg):
    if not cond:raise ValueError("STAGE67_TRUE_DRYAD_MULTIMODAL_NO_GO_"+msg)

def read_download(file,opener=urllib.request.urlopen):
    href=file["source_download_URL"]
    check(isinstance(href,str) and re.fullmatch(r"/api/v2/files/[0-9]+/download",href),
          "DRYAD_FILE_ID_FROM_ORIGINAL_API_MISSING")
    url=ROOT+href
    req=urllib.request.Request(url,headers={
       "User-Agent":"adaptive-gain-stage67-actual-published-primary-Dryad-spectral-multiguild/2026",
       "Accept":"application/octet-stream,*/*"})
    with opener(req,timeout=80) as response:
        raw=response.read(MAX_SOURCE_FILE+1)
    size=int(file["file_size_source_bytes_or_null"])
    check(0<size<=MAX_SOURCE_FILE and len(raw)==size,"DRYAD_ORIGINAL_SOURCE_SIZE")
    check(hashlib.sha256(raw).hexdigest()==file["hash_source_or_unknown"],
          "DRYAD_ORIGINAL_SOURCE_SHA256_CHANGED")
    return raw

def xlsx_structure(raw):
    check(zipfile.is_zipfile(io.BytesIO(raw)),"REAL_XLSX_NOT_ZIP")
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        names=z.namelist()
        check("xl/workbook.xml" in names,"XLSX_WORKBOOK_XML_NOT_FOUND")
        root=ET.fromstring(z.read("xl/workbook.xml"))
        sheet_names=[x.get("name") for x in root.findall(".//"+XML+"sheet")]
        sheets=[p for p in names if re.fullmatch(r"xl/worksheets/sheet[0-9]+.xml",p)]
        dims=[]
        for p in sorted(sheets):
            xml=z.read(p)
            check(len(xml)<=MAX_UNCOMPRESSED,"XLSX_WORKSHEET_TOO_LARGE")
            tree=ET.fromstring(xml)
            dim=tree.find(XML+"dimension")
            if dim is None:dim=tree.find(".//"+XML+"dimension")
            n_rows=len(tree.findall(".//"+XML+"row"))
            dims.append({"worksheet_xml":p,"original_dimension":dim.get("ref") if dim is not None else "",
                "numeric_or_text_row_elements":n_rows})
        return {"n_native_worksheet_tabs":len(sheet_names),
               "original_worksheet_tab_names":sheet_names,
               "n_physical_worksheet_xml_members":len(sheets),
               "original_workbook_worksheet_dimensions":dims,
               "no_XLSX_column_counts_inferred_as_biological_species":True}

def csv_structure(raw):
    s=raw.decode("utf-8-sig",errors="replace").replace("\r\n","\n").replace("\r","\n")
    rows=list(csv.reader(io.StringIO(s,newline="")))
    # Source rows need not contain individual flower UV labels; record format.
    return {"n_physical_csv_rows_including_header":len(rows),
           "n_original_source_csv_header_columns":len(rows[0]) if rows else 0,
           "first_original_csv_headers":(rows[0] if rows else [])[:24],
           "no_source_columns_inferred_as_distinct_Bombus_or_botanical_species":True}

def zip_members(raw):
    check(zipfile.is_zipfile(io.BytesIO(raw)),"ORIGINAL_DRYAD_ZIP_ARCHIVE_INVALID")
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        files=[f for f in z.infolist() if not f.is_dir()
               and not f.filename.startswith("__MACOSX/")
               and not any(x.startswith("._") for x in f.filename.split("/"))]
        check(len(files)<=3000,"ORIGINAL_DRYAD_ZIP_TOO_MANY_MEMBERS")
        uncompressed=sum(f.file_size for f in files)
        check(uncompressed<=200_000_000,"ORIGINAL_DRYAD_ZIP_BOMB_GUARD")
        ext_count={}
        for f in files:
            ext=Path(f.filename).suffix.lower() or "NO_EXT"
            ext_count[ext]=ext_count.get(ext,0)+1
        return {"n_real_archive_members":len(files),
           "total_uncompressed_source_member_bytes":uncompressed,
           "source_member_filename_first100":[f.filename for f in files[:100]],
           "original_file_extension_counts":ext_count,
           "not_each_repeated_file_a_new_species_or_interaction":True}

def source_audit(meta):
    check(meta["schema"]=="source_only_2022_2025_2026_Dryad_original_dataset_version_files",
          "PUBLISHED_SOURCE_API_MANIFEST_DIFFERENT")
    out={}
    for name,source in meta["datasets"].items():
        check(name in ALLOWED and source["version_id"] in (406487,421991,193417),
              "PINNED_ORIGINAL_DRYAD_VERSION_CHANGED")
        check(source["query_DOI"].startswith("10.5061/dryad."),
              "SOURCE_DOI_NOT_DRYAD")
        files=source["files"]
        check(len(files)==EXPECTED_FILES[name],"PUBLISHED_DATASET_SOURCE_FILES_CHANGED")
        file_results=[]
        for item in files:
            filename=item["filename"].rsplit("/",1)[-1]
            check(filename in ALLOWED[name],"UNREVIEWED_EXTERNAL_FILENAME")
            data=read_download(item)
            record={"original_filename":filename,
                "original_version_id":source["version_id"],
                "file_size":len(data),
                "verified_SHA256":hashlib.sha256(data).hexdigest(),
                "original_API_download_file_link":ROOT+item["source_download_URL"],
                "original_dataset_DOI":source["query_DOI"],
                "not_a_genetic_evolution_reproductive_fitness_observation":True}
            suffix=Path(filename).suffix.lower()
            if suffix==".csv":record["original_format_audit"]=csv_structure(data)
            elif suffix==".zip":record["original_format_audit"]=zip_members(data)
            elif suffix==".xlsx":record["original_format_audit"]=xlsx_structure(data)
            elif suffix==".docx":record["original_format_audit"]=zip_members(data)
            elif suffix==".md":
                record["original_format_audit"]={"source_text_lines":len(data.splitlines()),
                  "original_text_title":data.decode("utf-8-sig",errors="replace").splitlines()[:3]}
            file_results.append(record)
        out[name]={"source_version":source["version_id"],
          "original_DOI":source["query_DOI"],"source_original_files":file_results,
          "real_files_checked":len(file_results),"real_original_SHA256_all_verified":True}
        print("STAGE67_GENUINE_3_PUBLIC_PRIMARY_DRYAD_SOURCE_FILES",name,
           json.dumps({"version":source["version_id"],"n_files":len(file_results),
             "format_audits":{r["original_filename"]:{
               k:v for k,v in r["original_format_audit"].items()
               if k.startswith("n_") or k.startswith("first_original_csv_headers") or k.startswith("original_file_extension_counts")}
               for r in file_results}},sort_keys=True))
    return {"schema":"original_2022_2025_2026_source_Dryad_download_SHA_and_format_audit",
         "n_real_independent_study_data_archives":3,
         "total_real_published_source_files_verified":sum(z["real_files_checked"] for z in out.values()),
         "source_original_API_provenance_run":SOURCE_RUN,
         "source_data":out,
         "no_source_image_photography_or_assigned_UV_spatial_guide_binary":True,
         "no_original_XLSX_column_interpreted_as_distinct_species":True,
         "no_visitation_x_UV_evolution_effect_claimed":True}
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--original-official-Dryad-source-file-index",required=True,type=Path)
    p.add_argument("--outdir",default="stage67_real_Dryad_3study_primary_source_bytes_QC",type=Path)
    a=p.parse_args()
    receipt=json.loads(a.original_official_Dryad_source_file_index.read_text())
    summary=source_audit(receipt)
    a.outdir.mkdir(parents=True,exist_ok=True)
    (a.outdir/"source_3studies_original_file_SHA_and_tabular_metadata_receipt.json").write_text(
       json.dumps(summary,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    print("STAGE67_REAL_SOURCE_3_STUDIES_10_FILES_SHA_VALIDATED",
       json.dumps({"n_sources":summary["n_real_independent_study_data_archives"],
         "source_files_verified":summary["total_real_published_source_files_verified"]}))
if __name__=="__main__":main()
