"""Stage87D: GBIF ~3.96M original Bombus occurrences -> TDWG3 OBSERVED richness.

Archived GBIF occurrence download DOI 10.15468/dl.jbewdc:
  0003256-260226173443078; 3,958,417 records, 1950-2025, Asia,
  Europe, North America, human observation / specimen source records.
Do not interpret a region lacking a GBIF record as Bombus absence.
No global bee suitability or pollination service SDM is inferred.
Spatial point-to-TDWG source polygons, not country name replacement.
"""
from __future__ import annotations
import argparse,collections,csv,hashlib,io,json,math,re,urllib.request,zipfile
from pathlib import Path
import numpy as np
import shapely
from shapely.geometry import shape
from shapely.strtree import STRtree

GEO_SHA_BLOB="91104e5159e31f88154833a51d3b0d1c9271083f"
KEY="0003256-260226173443078"
GBIF_URL="https://api.gbif.org/v1/occurrence/download/request/"+KEY+".zip"
EXPECTED_OCC=3958417
GBIF_DOI="10.15468/dl.jbewdc"
BOMBUS_SPECIES=re.compile(r"^bombus\s+([a-z][a-z-]+)(?:\s|$)",re.I)
BAD_EPITHET={"sp","spp","cf","aff","species","hybrid","unknown"}
CHUNK=12500
MAX_SOURCE_ZIP_BYTES=2_300_000_000

def sha(b):
    return hashlib.sha1(("blob "+str(len(b))+"\0").encode()+b).hexdigest()

def download_source(target):
    """Full original bytes; no download succeeds on HTML instead of archive."""
    r=urllib.request.Request(GBIF_URL,headers={
        "User-Agent":"public-GBIF-dwca-archival-spatial-floral-pollinator-macro",
        "Accept":"application/zip,application/octet-stream,*/*"})
    digest=hashlib.sha256();n=0
    with urllib.request.urlopen(r,timeout=240) as remote,Path(target).open("wb") as f:
        if remote.status not in (200,206):
            raise ValueError("STAGE87D_GBIF_SOURCE_HTTP_STATUS_NOT_DOWNLOAD")
        while True:
            chunk=remote.read(4*1024*1024)
            if not chunk:break
            f.write(chunk);digest.update(chunk);n+=len(chunk)
            if n>MAX_SOURCE_ZIP_BYTES:
                raise ValueError("STAGE87D_GBIF_DOWNLOAD_EXCEEDS_BOUNDED_ORIGINAL_SIZE")
    if n<5000000 or not zipfile.is_zipfile(target):
        raise ValueError("STAGE87D_GBIF_DOWNLOAD_NOT_A_REAL_COMPLETE_ZIP")
    return {"original_archived_download_doi":GBIF_DOI,
      "original_archived_download_key":KEY,
      "GBIF_download_original_zip_bytes":n,
      "GBIF_download_SHA256":digest.hexdigest(),
      "source_url":GBIF_URL,"original_1950_2025_AsiaEuropeNorthAmerica":True}

def geometries(source):
    b=Path(source).read_bytes()
    if sha(b)!=GEO_SHA_BLOB:
        raise ValueError("STAGE87D_TDWG3_OFFICIAL_SOURCE_BLOB_NOT_VERIFIED")
    feat=json.loads(b)["features"]
    valid=[];codes=[];reject=collections.Counter()
    for a in feat:
        c=str(a["properties"].get("LEVEL3_COD","")).strip().upper()
        if not c:raise ValueError("STAGE87D_GIS_TDWG3_NO_CODE")
        polygon=shape(a["geometry"])
        if polygon.is_empty or not polygon.is_valid:
            reject["invalid_original_features_excluded"]+=1
            continue
        codes.append(c);valid.append(polygon)
    if len(valid)<350 or reject["invalid_original_features_excluded"]!=19:
        raise ValueError("STAGE87D_GIS_ORIGINAL_VALID_POLYGON_FRAME_CHANGED")
    return STRtree(valid),codes,dict(reject)

def source_file(z):
    items=[f for f in z.infolist() if not f.is_dir() and f.filename.lower().endswith(
            (".txt",".csv",".tsv"))]
    prior=[f for f in items if "occurrence" in f.filename.casefold() and
           f.file_size>10000000]
    cand=max(prior or [f for f in items if f.file_size>10000000],key=lambda f:f.file_size)
    # Distinct original data member, not meta.xml, citations or images.
    with z.open(cand) as f:
        header=f.readline(1_000_000).decode("utf-8-sig",errors="replace").strip("\r\n")
    delim="\t" if header.count("\t")>header.count(",") else ","
    fields=next(csv.reader([header],delimiter=delim))
    normalized={x.strip().casefold().replace("_",""):x for x in fields}
    def has_any(names):return any(k in normalized for k in names)
    if not has_any(("decimallatitude",)) or not has_any(("decimallongitude",)):
        raise ValueError("STAGE87D_GBIF_SOURCE_HAS_NO_LAT_LON")
    if not has_any(("species","scientificname","acceptedscientificname","verbatimscientificname")):
        raise ValueError("STAGE87D_GBIF_SOURCE_HAS_NO_TAXON_NAME")
    return cand,delim,fields,normalized

def field(row,columns,*variants):
    for k in variants:
        v=columns.get(k)
        if v:return row.get(v,"")
    return ""

def norm_species(x):
    s=" ".join(str(x or "").strip().casefold().split())
    m=BOMBUS_SPECIES.match(s)
    if not m:return None
    epi=m.group(1)
    return "Bombus "+epi if epi not in BAD_EPITHET else None

def quality(row,columns):
    try:
        lon=float(field(row,columns,"decimallongitude"))
        lat=float(field(row,columns,"decimallatitude"))
    except (TypeError,ValueError):return None,"BAD_COORD"
    if not (math.isfinite(lon) and math.isfinite(lat) and
            -180<=lon<=180 and -90<=lat<=90) or (abs(lon)<.0001 and abs(lat)<.0001):
        return None,"INVALID_OR_ZERO_GEO"
    issue=str(field(row,columns,"issue","issues")).upper()
    if "ZERO_COORDINATE" in issue or "COUNTRY_COORDINATE_MISMATCH" in issue:
        return None,"GBIF_GEOSPATIAL_ISSUE"
    raw=field(row,columns,"coordinateuncertaintyinmeters")
    uncertainty=None
    if raw not in ("",None):
        try:uncertainty=float(raw)
        except (TypeError,ValueError):pass
        if uncertainty is not None and math.isfinite(uncertainty) and uncertainty>100000:
            return None,"UNCERTAINTY_OVER_100KM"
    sp=norm_species(field(row,columns,"species","acceptedscientificname","scientificname",
         "verbatimscientificname"))
    if not sp:return None,"UNRESOLVED_OR_NON_BOMBUS_SPECIES"
    return (lon,lat,sp,uncertainty),"ACCEPT"

def iter_chunks(csvfile,delimiter,fieldnames):
    reader=csv.DictReader(io.TextIOWrapper(csvfile,encoding="utf-8-sig",
                                           errors="replace",newline=""),delimiter=delimiter)
    # Source original headers are required; do not silently rely on guessed positions.
    normalized=[s.casefold().replace("_","") for s in reader.fieldnames or []]
    if normalized!=[x.casefold().replace("_","") for x in fieldnames]:
        raise ValueError("STAGE87D_GBIF_SOURCE_HEADER_CHANGED_DURING_STREAM")
    chunk=[]
    for r in reader:
        chunk.append(r)
        if len(chunk)>=CHUNK:
            yield chunk;chunk=[]
    if chunk:yield chunk

def aggregate(path,tree,codes):
    observation=collections.Counter();records=collections.Counter()
    rank=collections.defaultdict(lambda:collections.Counter())
    grids=collections.defaultdict(set)
    species_grid=collections.defaultdict(set)
    per_species_uncertainty10=collections.defaultdict(set)
    sampled_source_region=set()
    with zipfile.ZipFile(path) as z:
        original,delimiter,columns,normalized=source_file(z)
        n=0
        with z.open(original) as f:
            for rawrows in iter_chunks(f,delimiter,columns):
                pts=[];info=[]
                for row in rawrows:
                    n+=1
                    source,why=quality(row,normalized)
                    observation[why]+=1
                    if source:
                        lon,lat,sp,uncertainty=source
                        pts.append((lon,lat))
                        info.append((lon,lat,sp,uncertainty))
                if not pts:continue
                geom=shapely.points(np.array(pts,dtype=float))
                pair=tree.query(geom,predicate="within")
                assignments=collections.defaultdict(set)
                for ii,jj in zip(pair[0],pair[1]):
                    assignments[int(ii)].add(codes[int(jj)])
                for ix,(lon,lat,sp,uncertainty) in enumerate(info):
                    matches=assignments.get(ix,set())
                    if not matches:
                        observation["quality_pass_outside_TDWG_valid_regions"]+=1
                        continue
                    if len(matches)!=1:
                        observation["point_in_multiple_source_TDWG_regions"]+=1
                        continue
                    code=next(iter(matches))
                    records[code]+=1;sampled_source_region.add(code)
                    rank[code][sp]+=1
                    cell=(math.floor(lon),math.floor(lat))
                    grids[code].add(cell)
                    species_grid[(code,sp)].add(cell)
                    if uncertainty is not None and uncertainty<=10000:
                        per_species_uncertainty10[(code,sp)].add(cell)
        if n!=EXPECTED_OCC:
            raise ValueError("STAGE87D_ORIGINAL_3958417_GBIF_RECORD_COUNT_DRIFT_"+str(n))
        source_receipt={"original_zip_member":original.filename,
           "original_zip_member_uncompressed_bytes":original.file_size,
           "original_source_delimiter":"tab" if delimiter=="\t" else "comma",
           "original_occurrence_header":columns[:120],
           "observed_original_full_source_count":n,
           "source_rejection_and_quality_counts":dict(observation),
           "valid_source_TDWG3_regions_with_positive_Bombus_records":len(sampled_source_region),
           "source_coverage_excludes_unknown_effort_zero_Bombus_regions":True}
    rows=[]
    for code in sorted(records):
        byspecies=rank[code]
        primary=[sp for sp,num in byspecies.items()
                 if num>=3 and len(species_grid[(code,sp)])>=2]
        strict10=[sp for sp in primary if len(per_species_uncertainty10.get((code,sp),set()))>=2]
        rows.append({"TDWG_L3":code,
          "GBIF_Bombus_original_positive_occurrence_records":records[code],
          "GBIF_Bombus_strict_binomial_recorded_species":len(byspecies),
          "GBIF_Bombus_3occ_2grid_recorded_species_primary":len(primary),
          "GBIF_Bombus_2grid_coord_uncertainty_le10km_sensitivity_species":len(strict10),
          "GBIF_Bombus_unique_1degree_recorded_cells":len(grids[code]),
          "GBIF_Bombus_1degree_cells_not_survey_effort_zero":True,
          "GBIF_Bombus_source_occurrence_not_native_or_true_absence":True,
          "GBIF_Bombus_source_year_max_2025":True})
    return rows,source_receipt

def run(td,source_zip,outdir):
    tree,codes,gis=geometries(td)
    rows,meta=aggregate(source_zip,tree,codes)
    if len(rows)<100 or sum(r["GBIF_Bombus_3occ_2grid_recorded_species_primary"]>0 for r in rows)<80:
        raise ValueError("STAGE87D_BOMBUS_3CONTINENT_ORIGINAL_SPATIAL_COVERAGE_INSUFFICIENT")
    outdir.mkdir(parents=True,exist_ok=True)
    with (outdir/"stage87D_original_GBIF_Bombus_TDWG3_recorded_richness.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    report={"schema":"stage87D_2026_archive_3958417_GBIF_bombus_observed_TDWG3_richness",
      "original_download_doi":GBIF_DOI,"source_GBIF_download_key":KEY,
      "original_TDWG_valid_polygon_geo_source_blob_sha":GEO_SHA_BLOB,
      "source_GIS_polygon_quality":gis,
      "original_source_archive":meta,
      "source_TDWG3_regions_with_recorded_bumblebees":len(rows),
      "source_native_bumblebee_distribution_NOT_identified":True,
      "source_missing_plant_region_bumblebee_records_NOT_true_absence":True,
      "GBIF_source_local_effort_bias_not_removed":True,
      "sampling_from_three_NH_continents_not_equivalent_to_global_insect_pollinators":True,
      "source_not_nectar_guides_odor_wind_learning_landing":True}
    (outdir/"stage87D_original_GBIF_Bombus_source_spatial_receipt.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print("STAGE87D_SOURCE_GLOBAL_BOMBUS_RECORDED_NATIVE_FLORA_REGION_OVERLAP",json.dumps({
      "n_original_records":meta["observed_original_full_source_count"],
      "Bombus_region_count":len(rows),
      "richness_nregion_ge3":sum(x["GBIF_Bombus_3occ_2grid_recorded_species_primary"]>=3 for x in rows),
      "quality_counts":meta["source_rejection_and_quality_counts"]},sort_keys=True),flush=True)
    return report

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--original-gbif-zip",type=Path,required=True)
    p.add_argument("--original-tdwg-geojson",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    x=p.parse_args();run(x.original_tdwg_geojson,x.original_gbif_zip,x.outdir)
if __name__=="__main__":main()
