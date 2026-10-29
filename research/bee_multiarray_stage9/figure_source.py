"""Retrieve original Klein et al. 2017 Figure 1 *image* without inventing coordinates.

Original Scientific Reports published Figure 1 shows 3 spatial flower arrays
and their labels in centimetres. Image is only an evidence item, NOT a
machine-readable coordinate mapping. Source URLs are publisher-owned and
the output is a provenance receipt+diagnostic image in transient CI artifact.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit
import urllib.request

FIGURE_ORIGINAL="41598_2017_4919_Fig1_HTML.jpg"
SOURCE_URLS=[
    "https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs41598-017-04919-8/MediaObjects/"+FIGURE_ORIGINAL,
    "https://media.springernature.com/lw685/springer-static/image/art%3A10.1038%2Fs41598-017-04919-8/MediaObjects/"+FIGURE_ORIGINAL,
]
SOURCE_HOSTS={"media.springernature.com","static-content.springer.com"}
MAX_JPG=12*1024*1024
def fetch_image(root:Path):
    root.mkdir(exist_ok=True,parents=True)
    failed=[]
    for url in SOURCE_URLS:
        try:
            req=urllib.request.Request(url,headers={
                "User-Agent":"adaptive-gain-published-bee-flower-array-figure-source/1.0",
                "Accept":"image/jpeg,*/*"})
            with urllib.request.urlopen(req,timeout=55) as response:
                original=response.read(MAX_JPG+1)
                final_url=response.url
                typ=response.headers.get("Content-Type","")
            host=urlsplit(final_url).hostname
            if host not in SOURCE_HOSTS:raise ValueError("redirected away from original publisher")
            if len(original)>MAX_JPG or len(original)<2000:
                raise ValueError("unverified image byte size")
            if not original.startswith(b"\xff\xd8\xff"):
                raise ValueError("original publisher response is not JPEG")
            saved=root/"2017_original_source_figure1.jpg"
            saved.write_bytes(original)
            try:
                from PIL import Image
                with Image.open(saved) as img:
                    img.verify()
                with Image.open(saved) as img:
                    width,height=img.size
            except Exception as e:raise ValueError("unverified original JPEG pixels") from e
            if min(width,height)<400:raise ValueError("figure too low resolution for labeled coordinates")
            receipt={
                "source_doi":"10.1038/s41598-017-04919-8",
                "source_figure":"Scientific Reports original Figure 1",
                "publisher_original_filename":FIGURE_ORIGINAL,
                "original_publisher_url":url,
                "original_bytes":len(original),
                "original_figure_sha256":hashlib.sha256(original).hexdigest(),
                "native_image_width_pixels":width,
                "native_image_height_pixels":height,
                "actual_pixel_coordinates_are_NOT_flower_metre_coordinates":True,
                "manual_source_label_and_axis_verification_still_required":True,
                "failed_source_routes":failed}
            (root/"klein2017_figure1_source_receipt.json").write_text(
                json.dumps(receipt,indent=2,ensure_ascii=False))
            print("STAGE9_FIGURE1_SOURCE "+json.dumps(receipt,ensure_ascii=False),flush=True)
            print("STAGE9_FIGURE1_SOURCE_COMPLETE",flush=True)
            return receipt
        except Exception as e:
            failed.append({"url":url,"type":type(e).__name__,
                           "http":getattr(e,"code",None),
                           "reason":str(e)[:250]})
    receipt={"status":"NO_GO_ORIGINAL_FIGURE1_NOT_ACCESSIBLE",
             "source_urls":failed,
             "not_assumed_coordinates":True}
    (root/"klein2017_figure1_source_receipt.json").write_text(
        json.dumps(receipt,indent=2,ensure_ascii=False))
    print("STAGE9_FIGURE1_NO_GO "+json.dumps(receipt),flush=True)
    raise ValueError("NO_GO_ORIGINAL_FIGURE1_NOT_ACCESSIBLE")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--out",default="bee_stage9_original")
    a=p.parse_args()
    fetch_image(Path(a.out))
