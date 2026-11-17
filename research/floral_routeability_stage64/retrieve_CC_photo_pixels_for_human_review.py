"""Stage64: actual CC-licensed iNaturalist original photo PIXEL feasibility.

Stage64 previous ORIGINAL metadata source workflow verified 4 FCP/VOC
source taxa, 17 fresh public iNat open-licensed photo IDs (NOT original
FCP source 100-photo IDs). This script downloads 2 per taxon from the
official iNaturalist open-data medium-size variant documented by
iNaturalistAPI. Full source attribution/CC license stays attached in
a credit ledger; no unlicensed image or precise observation coordinate.

Image output is a **human botanical review contact sheet**, never an
automated visible guide positive or absence; photo may not show flowers
or petals. 500px image can still be insufficient for UV contrast.
No RGB pixel can reveal UV reflectance or VOC, and new photo individuals
are NOT the original 2020 VOC flower individuals.
"""
from __future__ import annotations
from collections import defaultdict
import argparse,csv,hashlib,io,json,re,urllib.error,urllib.request
from pathlib import Path
from PIL import Image,ImageDraw,ImageOps

DATA_HOST="inaturalist-open-data.s3.amazonaws.com"
ALLOWED_LICENCES={"cc0","cc-by"}
N_PER_TAXON=2
TARGET_TAXA=("Dianthus deltoides","Dianthus barbatus",
             "Helichrysum stoechas","Antirrhinum majus")
URI_RE=re.compile(r"^https://inaturalist-open-data\.s3\.amazonaws\.com/photos/([0-9]+)/square\.(jpe?g|png)$")
MAX_BYTES=1_400_000
CROP_W,CROP_H=420,355

def uri_medium(row):
    url=row.get("original_photo_url_as_source_returned","")
    match=URI_RE.fullmatch(url)
    if match is None:
        raise ValueError("NO_GO_INAT_SOURCE_PHOTO_URL_NOT_AN_OPEN_DATA_SQUARE_ORIGINAL")
    if str(row.get("fresh_2026_original_iNaturalist_photo_id",""))!=match.group(1):
        raise ValueError("NO_GO_ORIGINAL_SOURCE_PHOTO_ID_URL_MISMATCH")
    if row.get("original_photo_licence_code") not in ALLOWED_LICENCES:
        raise ValueError("NO_GO_IMAGE_PREVIEW_LICENCE_NOT_CC_BY_OR_CC0")
    return url.replace("/square.","/medium.")

def select(rows):
    by=defaultdict(list)
    seen=set()
    for row in rows:
        species=row.get("source_original_iNat_species")
        if species not in TARGET_TAXA:
            raise ValueError("NO_GO_SOURCE_PILOT_TAXON_NOT_FROZEN")
        key=row.get("fresh_2026_original_iNaturalist_photo_id")
        if not key or key in seen:
            raise ValueError("NO_GO_ORIGINAL_INAT_PHOTO_ID_MISSING_OR_DUPLICATED")
        seen.add(key)
        if row.get("original_photo_licence_code") not in ALLOWED_LICENCES:
            # CC-BY-SA is valid open data; do not mix its share-alike
            # adaptation conditions into this CC0/CC-BY preview.
            continue
        uri_medium(row)
        if row.get("photo_is_open_flower_verified")!="UNKNOWN_UNREAD_IMAGE":
            raise ValueError("NO_GO_IMAGE_TRAIT_CLAIM_BEFORE_PHOTO_INSPECTION")
        by[species].append(row)
    chosen=[]
    for species in TARGET_TAXA:
        # Identity-based preselection before opening pixels; no outcome
        # or color-based cherry-picking.
        rows0=sorted(by[species],key=lambda row:hashlib.sha256(
           ("stage64-blind-source-photo-ID-20261117|"+row["fresh_2026_original_iNaturalist_photo_id"]).encode()).hexdigest())
        chosen.extend(rows0[:N_PER_TAXON])
    if len(chosen)>N_PER_TAXON*len(TARGET_TAXA):
        raise AssertionError("NO_GO_SELECTED_EXCEEDS_AUTHENTIC_SOURCE_TAXA")
    return chosen

def original_medium_image(row,opener=urllib.request.urlopen):
    url=uri_medium(row)
    req=urllib.request.Request(url,headers={
       "User-Agent":"adaptive-gain-stage64-iNat-original-CC-licensed-medium-botanical-review/2026",
       "Accept":"image/jpeg,image/png"})
    with opener(req,timeout=45) as res:
        final=res.geturl()
        if not final.startswith("https://"+DATA_HOST+"/photos/"):
            raise ValueError("NO_GO_SOURCE_CC_PHOTO_REDIRECTS_TO_DIFFERENT_OR_UNLICENSED_HOST")
        data=res.read(MAX_BYTES+1)
    if len(data)>MAX_BYTES:
        raise ValueError("NO_GO_ORIGINAL_INAT_MEDIUM_IMAGE_OVERSIZE")
    try:
        img=Image.open(io.BytesIO(data))
        img.load()
    except Exception as exc:
        raise ValueError("NO_GO_ORIGINAL_INAT_IMAGE_CANNOT_BE_READ") from exc
    if img.format not in ("JPEG","PNG") or not all(50<=d<=1000 for d in img.size):
        raise ValueError("NO_GO_ORIGINAL_MEDIUM_PHOTO_FORMAT_OR_DIMENSIONS")
    return img.convert("RGB"),hashlib.sha256(data).hexdigest(),url

def contact_sheet(rows,downloaded):
    cell_w,cell_h=CROP_W,CROP_H
    cols=2
    nrows=max(1,(len(downloaded)+cols-1)//cols)
    # Plain neutral no stylization; image crops only for actual original
    # source botanical human review, with exact visible attribution below.
    board=Image.new("RGB",(cols*cell_w,nrows*cell_h),"white")
    draw=ImageDraw.Draw(board)
    for idx,(row,img,digest,url) in enumerate(downloaded):
        x=(idx%cols)*cell_w
        y=(idx//cols)*cell_h
        if img is not None:
            fitted=ImageOps.contain(img,(cell_w-12,cell_h-86))
            board.paste(fitted,(x+(cell_w-fitted.width)//2,y+6))
        draw.rectangle((x,y,x+cell_w-1,y+cell_h-1),outline=(60,60,60),width=1)
        title=row.get("source_original_iNat_species","")[:31]
        photo=row.get("fresh_2026_original_iNaturalist_photo_id","")
        license=row.get("original_photo_licence_code","")
        attrib=row.get("source_photo_attribution_as_returned","").strip()[:47]
        y0=y+cell_h-77
        draw.text((x+8,y0),f"{title} / Photo {photo}",fill=(0,0,0))
        draw.text((x+8,y0+17),f"License {license} - {attrib}",fill=(0,0,0))
        draw.text((x+8,y0+34),"Visible/UV-guide status: UNREVIEWED",fill=(0,0,0))
    return board

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--original-licensed-photo-metadata",required=True)
    a=ap.parse_args()
    with Path(a.original_licensed_photo_metadata).open(newline="",encoding="utf8") as f:
        rows=list(csv.DictReader(f))
    chosen=select(rows)
    out=Path("stage64_original_cc_photo_pixel_review")
    out.mkdir(exist_ok=True)
    download=[]
    receipts=[]
    for row in chosen:
        try:
            image,sha,url=original_medium_image(row)
            download.append((row,image,sha,url))
            receipts.append({"source_species":row["source_original_iNat_species"],
                "source_original_photo_id":row["fresh_2026_original_iNaturalist_photo_id"],
                "source_original_observation_id":row["fresh_2026_original_iNaturalist_observation_id"],
                "original_license":row["original_photo_licence_code"],
                "source_original_attribution":row["source_photo_attribution_as_returned"],
                "source_unchanged_square_url":row["original_photo_url_as_source_returned"],
                "official_iNaturalist_medium_variant_url":url,
                "source_verified_medium_image_SHA256":sha,
                "source_medium_pixel_dimensions":list(image.size),
                "actual_intrapetal_spatial_guide_presence":"UNREVIEWED_IMAGE",
                "UV_signal_status":"UNOBSERVABLE_IN_RGB",
                "original_VOC_scent_bouquet_same_photo":"UNKNOWN_NOT_SAME_SOURCE_INDIVIDUAL",
                "status":"ORIGINAL_CC_LICENSED_PIXEL_DOWNLOADED_FOR_BOTANICAL_REVIEW"})
        except (ValueError,urllib.error.HTTPError,urllib.error.URLError,
                TimeoutError) as e:
            receipts.append({"source_species":row["source_original_iNat_species"],
               "source_original_photo_id":row["fresh_2026_original_iNaturalist_photo_id"],
               "status":"ORIGINAL_PHOTO_NOT_RETRIEVED_NOT_A_NEGATIVE_GUIDE",
               "error_type":type(e).__name__,
               "error_message":str(e)[:130]})
    if download:
        contact_sheet(chosen,download).save(out/"source_CC_photos_flower_visible_pattern_CONTACT_SHEET_UNREVIEWED.png")
    summary={
      "status":"LICENSED_ORIGINAL_INAT_FOUR_TAXON_SOURCE_PIXEL_REVIEW_GATE",
      "source_original_taxon_licence_and_photo_preselection_frozen_before_pixels":True,
      "n_preselected_from_original_iNat_metadata":len(chosen),
      "n_licensed_actual_medium_photo_pixels_read":len(download),
      "n_source_species_with_pixels":len(set(r["source_original_iNat_species"] for r, *_ in download)),
      "source_image_credits_and_exceptions":receipts,
      "CC0_CC_BY_licenses_and_authors_retained":True,
      "not_original_FCP_exact_source_100_photo_IDs":True,
      "not_an_independently_measured_flower_UV_or_nectar_guide":True,
      "actual_visible_pattern_annotated_from_images":False,
      "no_species_study_VOC_photo_same_individual_or_wind_pollen_data":True,
    }
    (out/"original_CC_photo_pixel_review_credits_and_unmeasured_traits.json").write_text(
       json.dumps(summary,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf8")
    print("STAGE64_ORIGINAL_CC_LICENSED_FLOWER_PIXELS_AND_SOURCE_CREDITS",
          json.dumps({k:v for k,v in summary.items() if k!="source_image_credits_and_exceptions"},
                     ensure_ascii=False,sort_keys=True))
    print("NO_AUTOMATIC_CONFIRMED_NECTAR_GUIDE_OR_SPECIES_NEGATIVE_FROM_PIXEL")
if __name__=="__main__":
    main()
