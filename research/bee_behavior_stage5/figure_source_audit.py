"""Acquire exact original published ten-flower geometry figure for manual audit.

No coordinate guessing from source flower numbering. Figure source hashes,
media formats and cross-source verification remain explicit. Figure image is
kept as a separate CI diagnostic artifact only, not re-hosted in Git.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import pathlib
import urllib.request

FIG_URLS=[
"https://media.springernature.com/full/springer-static/image/art%3A10.1186%2Fs40462-019-0150-z/MediaObjects/40462_2019_150_Fig2_HTML.jpg",
"https://media.springernature.com/full/springer-static/image/art%3A10.1186%2Fs40462-019-0150-z/MediaObjects/40462_2019_150_Fig2_HTML.png",
"https://media.springernature.com/lw685/springer-static/image/art%3A10.1186%2Fs40462-019-0150-z/MediaObjects/40462_2019_150_Fig2_HTML.jpg",
"https://media.springernature.com/lw685/springer-static/image/art%3A10.1186%2Fs40462-019-0150-z/MediaObjects/40462_2019_150_Fig2_HTML.png",
"https://link.springer.com/content/pdf/10.1186/s40462-019-0150-z.pdf",
"https://d-nb.info/1181293162/34",
]
MAX_SOURCE=16*1024*1024

def fetch_figure(out:pathlib.Path,urls=FIG_URLS):
    out.mkdir(parents=True,exist_ok=True)
    fails=[]
    for url in urls:
        try:
            req=urllib.request.Request(url,headers={
                "User-Agent":"adaptive-gain-original-publisher-spatial-figure-validation/1.0",
                "Accept":"image/jpeg,image/png,application/pdf,*/*"})
            with urllib.request.urlopen(req,timeout=35) as rsp:
                data=rsp.read(MAX_SOURCE+1)
                status=getattr(rsp,"status",200)
                typ=rsp.headers.get("Content-Type","")
            if len(data)<500 or len(data)>MAX_SOURCE:
                raise ValueError("source bytes outside cap")
            if data.startswith(b"\xff\xd8\xff"):
                ext=".jpg"
                (out/"source_original_figure_2.jpg").write_bytes(data)
                rendered=out/"source_original_figure_2.jpg"
            elif data.startswith(b"\x89PNG\r\n\x1a\n"):
                ext=".png"
                (out/"source_original_figure_2.png").write_bytes(data)
                rendered=out/"source_original_figure_2.png"
            elif data.startswith(b"%PDF"):
                ext=".pdf"
                # Use original publisher-page figure only. Render entire
                # scientific page as an inspectable PNG. Avoid OCR or custom
                # fabricated flower coordinates.
                import fitz
                document=fitz.open(stream=data,filetype="pdf")
                if len(document)<3:raise ValueError("publisher PDF shorter than 3 pages")
                page=document.load_page(2)
                pix=page.get_pixmap(matrix=fitz.Matrix(2.1,2.1),alpha=False)
                rendered=out/"source_original_figure_2_page.png"
                pix.save(str(rendered))
            else:
                raise ValueError("publisher response is neither PNG JPEG nor PDF")
            receipt={
                "source_url":url,
                "http_status":status,
                "source_media_type":typ,
                "source_extension":ext,
                "original_bytes":len(data),
                "original_sha256":hashlib.sha256(data).hexdigest(),
                "rendered_image_file":rendered.name,
                "source_publication_doi":"10.1186/s40462-019-0150-z",
                "figure_2_must_be_manually_read_before_using_label_geometry":True,
                "published_9m_nearest_F1_F4_and_15p8m_second_F1_F6":True,
                "no_coordinates_extracted_yet":True,
                "failed_other_urls":fails}
            (out/"figure_source_receipt.json").write_text(json.dumps(receipt,indent=2))
            print("STAGE5_ORIGINAL_FIGURE_SOURCE "+json.dumps(receipt),flush=True)
            return receipt
        except Exception as e:
            fails.append({"source_url":url,
                          "reason":str(e)[:240],
                          "exception":type(e).__name__})
    receipt={"status":"NO_GO_FIGURE_SOURCE_UNAVAILABLE",
             "tried":fails,"cannot_fit_spatial_geometry":True}
    (out/"figure_source_receipt.json").write_text(json.dumps(receipt,indent=2))
    print("STAGE5_FIGURE_SOURCE_NO_GO "+json.dumps(receipt),flush=True)
    return receipt

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--out",default="bee_stage5_geo_source")
    args=p.parse_args()
    result=fetch_figure(pathlib.Path(args.out))
    if result.get("status")=="NO_GO_FIGURE_SOURCE_UNAVAILABLE":
        raise SystemExit(2)
