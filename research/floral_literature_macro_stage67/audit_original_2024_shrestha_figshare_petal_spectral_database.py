"""Stage67 authentic public 2024 flower PETAL SPECTRA database (no images).

Shrestha et al. 2024 doi:10.1016/j.dib.2024.110512,
original Figshare dataset 10.6084/m9.figshare.21081025.v2.
Spectrophotometer measured 300–700 nm petal spectra in botanical garden,
NOT UV spatial nectar guides, not wild native localities, not real visits.
We audit a curious publication discrepancy: 73 claimed study species vs 83
summed species in its 7 listed visual colour categories. Distinguish
original spectral columns, raw literal names and accepted species counts.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,math,re,urllib.parse,urllib.request,zipfile
from pathlib import Path
from collections import Counter

ARTICLE="https://api.figshare.com/v2/articles/21081025"
SOURCE_DOI="10.6084/m9.figshare.21081025.v2"
ARTICLE_DOI="10.1016/j.dib.2024.110512"
MAX_ZIP_BYTES=45_000_000
MAX_EXPANDED_MEMBER=15_000_000

def check(ok,why):
    if not ok:raise ValueError("STAGE67_FIGSHARE_ORIGINAL_SPECTRA_NO_GO_"+why)

def fetch_metadata(opener=urllib.request.urlopen):
    req=urllib.request.Request(ARTICLE,headers={"Accept":"application/json",
       "User-Agent":"adaptive-gain-stage67-literature-only-2024-flower-spectra/2026"})
    with opener(req,timeout=50) as res:raw=res.read(2_000_001)
    check(len(raw)<=2_000_000,"ORIGINAL_FIGSHARE_METADATA_TOO_LARGE")
    meta=json.loads(raw)
    check(int(meta["id"])==21081025,"FIGSHARE_SOURCE_ARTICLE_WRONG")
    check(str(meta.get("version"))=="2","SOURCE_FIGSHARE_VERSION_NOT_V2")
    check("21081025" in str(meta.get("doi","")),"ORIGINAL_SOURCE_DOI_DRIFT")
    matches=[z for z in meta.get("files",[]) if str(z.get("name","")).endswith(".zip")
             and "Shrestha" in str(z.get("name",""))]
    check(len(matches)==1,"NO_UNAMBIGUOUS_PRIMARY_SPECTRAL_ZIP")
    f=matches[0]
    check(isinstance(f.get("id"),int) and 0<int(f["size"])<=MAX_ZIP_BYTES,
          "ORIGINAL_SOURCE_ZIP_SIZE_UNSAFE")
    return meta,f

def download_exact_file(filemeta,opener=urllib.request.urlopen):
    # The Figshare-author API file ID is immutable to the requested release;
    # construct a canonical trusted downloader URL, never an arbitrary external
    # URL derived from a mutable user-controlled website document.
    url="https://ndownloader.figshare.com/files/"+str(filemeta["id"])
    request=urllib.request.Request(url,headers={
        "User-Agent":"adaptive-gain-stage67-true-open-spectral-csv/2026"})
    with opener(request,timeout=75) as resp:raw=resp.read(MAX_ZIP_BYTES+1)
    check(0<len(raw)<=MAX_ZIP_BYTES,"ORIGINAL_SPECTRAL_ZIP_SIZE")
    check(len(raw)==int(filemeta["size"]),"ORIGINAL_SOURCE_FILE_BYTE_COUNT")
    md5=filemeta.get("computed_md5") or filemeta.get("supplied_md5")
    if md5:check(hashlib.md5(raw).hexdigest()==md5,"ORIGINAL_FIGSHARE_MD5_CHANGED")
    check(zipfile.is_zipfile(io.BytesIO(raw)),"SOURCE_NOT_A_ZIP")
    return raw,{"file_size":len(raw),
       "original_figshare_file_id":int(filemeta["id"]),
       "original_figshare_filename":filemeta["name"],
       "original_source_sha256":hashlib.sha256(raw).hexdigest(),
       "original_source_figshare_MD5_or_unavailable":md5,
       "original_source_recovered_not_derived_from_RGB":True}

def clean_name(text):
    s=str(text or "").strip()
    s=re.sub(r"\.\d+$","",s)
    return " ".join(s.replace("_"," ").split())

def parse_spectral_csv(raw,path):
    s=raw.decode("utf-8-sig",errors="replace").replace("\r\n","\n").replace("\r","\n")
    rows=list(csv.reader(io.StringIO(s,newline="")))
    check(len(rows)>=101,"SOURCE_SPECTRUM_TOO_SHORT_"+path)
    hdr=rows[0]
    check(len(hdr)>=2,"NO_SPECTRAL_COLUMNS_"+path)
    # Allow the original wavelength header name to vary; require actual
    # source rows explicitly state wavelengths, not positional index 1..401.
    wavelengths=[]
    values={i:[] for i in range(1,len(hdr))}
    for row in rows[1:]:
        if not row or not str(row[0]).strip():continue
        try:wl=float(row[0])
        except ValueError:continue
        if len(row)<len(hdr):row=row+[""]*(len(hdr)-len(row))
        wavelengths.append(wl)
        for i in range(1,len(hdr)):
            try:v=float(row[i])
            except (ValueError,IndexError):v=float("nan")
            values[i].append(v)
    check(len(wavelengths)>=101 and
        len(set(wavelengths))==len(wavelengths) and
        min(wavelengths)>=290 and max(wavelengths)<=710 and
        min(wavelengths)<=330 and max(wavelengths)>=650,
        "ORIGINAL_SPECTRAL_WAVELENGTH_INVALID_"+path)
    ret=[]
    for j in range(1,len(hdr)):
        v=values[j]
        available=[(wl,val) for wl,val in zip(wavelengths,v) if math.isfinite(val)]
        uv=[vv for wl,vv in available if 300<=wl<400]
        vis=[vv for wl,vv in available if 400<=wl<=700]
        status=("SPECTRUM_MEASURED_WITH_UV_AND_VIS" if len(uv)>=70
                and len(vis)>=150 else "INCOMPLETE_SPECTRUM_NOT_ZERO")
        ret.append({
          "original_source_spectral_member":path,
          "original_spectral_column_name":hdr[j].strip(),
          "source_literal_species_candidate":clean_name(hdr[j]),
          "original_wavelength_samples":len(wavelengths),
          "finite_uv_points":len(uv),"finite_visible_points":len(vis),
          "UV_mean_reflectance_300_399_or_unknown":sum(uv)/len(uv) if uv else "",
          "visible_mean_reflectance_400_700_or_unknown":sum(vis)/len(vis) if vis else "",
          "source_measured_spectrum_status":status,
          "UV_spatial_guide_status":"NOT_OBSERVABLE_FROM_ONE_PETAL_MEAN_SPECTRUM",
          "source_native_species_collection_locality":"BAYREUTH_BOTANICAL_GARDEN_NOT_NATIVE_PROVENANCE",
          "flower_part":"petal",
          "not_GBIF_accepted_taxonomy_or_verified_negative":True})
    return ret

def scan_authentic_zip(data):
    names=[]
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        allmembers=z.infolist()
        for m in allmembers:
            if m.is_dir():continue
            check(m.file_size<=MAX_EXPANDED_MEMBER,
                  "INDIVIDUAL_ZIP_MEMBER_OVER_LIMIT")
            low=m.filename.replace("\\","/").lower()
            # The original Figshare ZIP contains macOS AppleDouble resource
            # fork metadata under __MACOSX/ and ._* names, not floral spectra.
            # Do not let short binary resource forks masquerade as CSV files.
            if low.startswith("__macosx/") or any(x.startswith("._") for x in low.split("/")):
                continue
            if not low.endswith(".csv") or not re.search(
                     r"(?:^|/)petals(?:/|$)",low):continue
            rows=parse_spectral_csv(z.read(m),m.filename)
            names.extend(rows)
    check(bool(names),"NO_REAL_SOURCE_PETAL_CSV_SPECTRAL_COLUMNS")
    nms=[r["source_literal_species_candidate"] for r in names]
    return names,{
      "original_published_claim_species":73,
      "paper_7_colour_groups_sum_11_10_10_17_10_11_14":83,
      "n_original_petal_spectral_columns_NOT_SPECIES":len(names),
      "n_distinct_original_column_labels_not_accepted_species":len(set(nms)),
      "n_distinct_source_petal_file_members":len(set(r["original_source_spectral_member"] for r in names)),
      "n_source_columns_with_complete_UV_and_visible":sum(r["source_measured_spectrum_status"]=="SPECTRUM_MEASURED_WITH_UV_AND_VIS" for r in names),
      "n_biological_species_not_claimed_from_spectral_column_names":True,
      "n_measured_UV_spatial_guide_positive_negative":"NOT_MEASURED",
      "same_garden_study_no_native_guild_absence":True,
      "no_FCP_or_iNaturalist_photographs_or_colour_labels":True}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--outdir",type=Path,default=Path("stage67_original_Figshare_73_species_petal_reflectance_source"))
    args=ap.parse_args()
    meta,file=fetch_metadata()
    raw,archive=download_exact_file(file)
    rows,receipt=scan_authentic_zip(raw)
    report={"schema":"actual_original_2024_shrestha_flower_petal_spectral_database_audit",
            "source_article_doi":ARTICLE_DOI,
            "source_data_DOI":SOURCE_DOI,
            "figshare_source_version":meta["version"],
            "original_figshare":archive,
            "actual_source_petal_columns":receipt,
            "source_measured_reflection_not_a_uv_nectar_guide_positive_negative":True,
            "no_taxonomic_inference_by_original_photo_identifiers":True}
    args.outdir.mkdir(parents=True,exist_ok=True)
    (args.outdir/"source_floral_spectra_original_Figshare_2024_receipt.json").write_text(
        json.dumps(report,indent=2,sort_keys=True,ensure_ascii=False,allow_nan=False)+"\n")
    with (args.outdir/"source_original_per_petal_spectral_column_uv_visible_integrals.csv").open(
        "w",newline="",encoding="utf8") as handle:
        w=csv.DictWriter(handle,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    print("STAGE67_REAL_PUBLISHED_2024_SPECTRAL_DB_NO_PHOTOS",
          json.dumps(receipt,sort_keys=True,ensure_ascii=False))
    print("NO_INDIRECT_UV_GUIDE_TRAIT_OR_BEE_SELECTION_FROM_PETAL_SPECTRUM")
if __name__=="__main__":main()
