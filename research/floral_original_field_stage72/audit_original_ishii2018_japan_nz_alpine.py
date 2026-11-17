"""Stage72D: Retrieve original Ishii et al. alpine Japan–NZ flower spectra and guild XLSX.

Peer-reviewed Annals of Botany DOI 10.1093/aob/mcy188, PMCID PMC6377100.
Original study: 106 native Japanese and 96 native New Zealand measured plants;
two geographically independent country-region units (NOT 202 independent
evolutionary radiations). Supplementary S2 has species pollinator obs/color
properties; S3 has wavelength-resolved source reflectance as published.
Use only real public OA archive/supplementary services; provenance goes with
raw source SHA. No user photo data, no genus syndrome imputation.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,re,tarfile,urllib.parse,urllib.request,urllib.error,zipfile,xml.etree.ElementTree as ET
from pathlib import Path

PMCID="PMC6377100"
DOI="10.1093/aob/mcy188"
SUPPORT={"aob-18614-s02.xlsx":"original_plant_pollinator_observation_and_colour_properties",
         "aob-18614-s03.xlsx":"original_wavelength_resolved_flower_reflectance"}
OA_API="https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id="+PMCID
EPMC_SUPP="https://www.ebi.ac.uk/europepmc/webservices/rest/"+PMCID+"/supplementaryFiles"
ORIGINAL_PUBLISHED_COUNTS={
 "Japanese_native_spectra_species":106,"New_Zealand_native_spectra_species":96,
 "Japan_source_observed_visits":5900,"New_Zealand_source_observed_visits":3594,
 "independent_alpine_regions_JP_and_NZ":2,
 "Japan_field_sites":1,"New_Zealand_field_sites":3,
 "Mount_Hutt_no_original_pollinator_observation":True,
}
UA="adaptive-gain-stage72d-original-Ishii2018-alpine-NCBI-PMC/2026-11-17"
MAX_DOWNLOAD=55_000_000


def get(url,maxlen=MAX_DOWNLOAD):
    if not url.startswith("https://"):
        raise ValueError("STAGE72D_NON_HTTPS_ORIGINAL_SOURCE_URL")
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"*/*"})
    with urllib.request.urlopen(req,timeout=45) as res:
        raw=res.read(maxlen+1)
        final=res.geturl()
    if len(raw)>maxlen or not raw:
        raise ValueError("STAGE72D_ORIGINAL_SOURCE_BYTES_MISSING_OR_OVERSIZE")
    return raw,final

def source_checksum(raw):
    return hashlib.sha256(raw).hexdigest()

def normalize_archive_link(url):
    if url.startswith("ftp://ftp.ncbi.nlm.nih.gov/"):
        return url.replace("ftp://","https://",1)
    if url.startswith("https://ftp.ncbi.nlm.nih.gov/"):
        return url
    raise ValueError("STAGE72D_UNEXPECTED_ORIGINAL_PMC_OA_DOWNLOAD_HOST")

def oa_original_package_url(xml):
    root=ET.fromstring(xml)
    records=root.findall(".//record")
    if len(records)!=1:
        raise ValueError("STAGE72D_NO_SINGLE_PMC_OA_PACKAGE_RECORD")
    rec=records[0]
    if rec.attrib.get("id")!=PMCID:
        raise ValueError("STAGE72D_PMC_OA_RECORD_ID_MISMATCH")
    links=rec.findall("link")
    package=[
        l.attrib.get("href") for l in links
        if (l.attrib.get("format","").lower() in ("tgz","tar.gz")
            or "tar.gz" in str(l.attrib.get("href","")))
    ]
    if not package:
        raise ValueError("STAGE72D_PMC_PACKAGE_HAS_NO_TGZ")
    return normalize_archive_link(package[0]),rec.attrib


def original_supplement_bytes_from_targz(raw):
    output={}
    with tarfile.open(fileobj=io.BytesIO(raw),mode="r:gz") as t:
        files=t.getmembers()
        for m in files:
            if not m.isfile():continue
            match=[key for key in SUPPORT if m.name.lower().endswith("/"+key)
                   or m.name.lower()==key]
            if not match:continue
            if m.size>10_000_000:raise ValueError("STAGE72D_ORIGINAL_XLSX_TOO_LARGE")
            f=t.extractfile(m)
            data=f.read() if f else b""
            if len(data)!=m.size or not zipfile.is_zipfile(io.BytesIO(data)):
                raise ValueError("STAGE72D_NOT_GENUINE_ORIGINAL_XLSX_"+m.name)
            if match[0] in output:raise ValueError("STAGE72D_DUPLICATED_SUPPLEMENT_IN_ARCHIVE")
            output[match[0]]=(data,m.name)
    return output

def original_supplement_bytes_from_zip(raw):
    output={}
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        for member in z.infolist():
            if member.is_dir():continue
            match=[key for key in SUPPORT if member.filename.lower().endswith("/"+key)
                   or member.filename.lower()==key]
            if not match:continue
            if member.file_size>10_000_000:raise ValueError("STAGE72D_ORIGINAL_XLSX_TOO_LARGE")
            data=z.read(member.filename)
            if len(data)!=member.file_size or not zipfile.is_zipfile(io.BytesIO(data)):
                raise ValueError("STAGE72D_SUPPLEMENT_NOT_REAL_XLSX")
            if match[0] in output:raise ValueError("STAGE72D_DUPLICATED_ARCHIVE_SUPPLEMENT")
            output[match[0]]=(data,member.filename)
    return output

def original_xlsx_preview(raw):
    if not zipfile.is_zipfile(io.BytesIO(raw)):
        raise ValueError("STAGE72D_SUPP_INVALID_XLSX")
    # reuse independently tested Stage72 source code only for reading
    from replay_original_kantsa2018_network_voc import read_xlsx_sparse
    books=read_xlsx_sparse(raw)
    summary=[]
    for sheet,rows in books.items():
        top=[{"row":i,"cells":{str(j+1):val[:90] for j,val in sorted(row.items())[:13]}}
             for i,row in sorted(rows.items())[:4]]
        summary.append({"sheet":sheet,"n_nonempty_rows":len(rows),
                        "max_source_nonempty_col":max((max(x) for x in rows.values() if x),default=-1)+1,
                        "first_four_rows":top})
    return summary

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args()
    a.outdir.mkdir(exist_ok=True,parents=True)
    tried=[];source={};route=""
    for how in ("pmc_oa_tar","europepmc_supplement_zip"):
        try:
            if how=="pmc_oa_tar":
                oa,final=get(OA_API,maxlen=500_000)
                targz,rec=oa_original_package_url(oa)
                raw,final=get(targz)
                got=original_supplement_bytes_from_targz(raw)
                tried.append({"route":how,"source_package_sha256":source_checksum(raw),
                              "source_pkg_bytes":len(raw),
                              "source_pmc_oa_records":rec,
                              "n_supplements_retrieved":len(got)})
            else:
                raw,final=get(EPMC_SUPP)
                got=original_supplement_bytes_from_zip(raw)
                tried.append({"route":how,"source_package_sha256":source_checksum(raw),
                              "source_pkg_bytes":len(raw),
                              "n_supplements_retrieved":len(got)})
            if len(got)==2:
                source=got;route=how;break
            tried[-1]["missing_original_source_tables"]=[k for k in SUPPORT if k not in got]
        except Exception as exc:
            tried.append({"route":how,"status":"SOURCE_UNAVAILABLE_NOT_ABSENT",
                          "error_class":type(exc).__name__,
                          "http_code":getattr(exc,"code",None)})
    receipts=[]
    for name,(raw,path) in source.items():
        receipts.append({
           "source_file":name,"original_archive_member_name":path,
           "original_source_sha256":source_checksum(raw),
           "original_source_bytes":len(raw),
           "original_supplementary_role":SUPPORT[name],
           "original_xlsx_sheets":original_xlsx_preview(raw),
        })
    report={
      "schema":"stage72d_original_Ishii2018_JP_NZ_field_spectra_and_real_visitor_primary_source_probe",
      "source_DOI":DOI,"original_article_PMCID":PMCID,
      "source_published_counts_not_yet_extracted_from_supplement":ORIGINAL_PUBLISHED_COUNTS,
      "original_retrieval_route":route or "NOT_OBTAINED",
      "original_retrieval_attempt_receipts":tried,
      "original_recovered_supplementary_files":receipts,
      "original_source_sheet_xlsx_complete":len(source)==2,
      "Japan_and_NewZealand_study_are_two_independent_regions_not_202_replicates":True,
      "no_pollinator_visit_records_in_Mount_Hutt":True,
      "no_uv_spatial_guide_binary_inferred":True,
      "no_wind_VOC_fitness_measured_in_these_source_xlsx":True,
      "no_macro_environmental_guild_effect_fitted":True,
    }
    (a.outdir/"original_Ishii2018_alpine_JP_NZ_PMC_supplement_access_receipt.json").write_text(
       json.dumps(report,indent=2,ensure_ascii=False,sort_keys=True)+"\n",encoding="utf-8")
    print("STAGE72D_SOURCE_ORIGINAL_JAPAN_NEWZEALAND_SPECTRA_VISITOR_TABLES",
          json.dumps(report,ensure_ascii=False,sort_keys=True))
    print("SOURCE_ORIGINAL_NOT_INFERRED_NO_GLOBAL_CAUSAL_SYNDROME_CLAIM")
if __name__=="__main__":main()
