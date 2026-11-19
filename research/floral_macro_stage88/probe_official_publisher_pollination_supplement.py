"""Try paper's officially published Dataset S2 Rdata (not Dryad private API).

Wang et al 2025 New Phytologist DOI 10.1111/nph.70196 lists the exact file
'nph70196-sup-0002-DatasetS2.Rdata' as public supporting information.
Dryad public REST metadata lists its own Rdata, but since 2026 anonymous
file API responds HTTP 401; that is an *access blocker*, not missing data.
This attempts only openly published Wiley supplement public download routes,
not bypassing any authenticated endpoint or anti-bot challenge.

A source is admitted only if it decodes a genuine RData species x
pollination column and genuinely contains >170k original source records.
No alternative source is interpreted as exact byte-identical to Dryad.
"""
from __future__ import annotations
import argparse,hashlib,json,urllib.request,urllib.error,urllib.parse,tempfile
from pathlib import Path
import pandas as pd
import pyreadr

DOI="10.1111/nph.70196"
NAME="nph70196-sup-0002-DatasetS2.Rdata"
CANDIDATES=[
  "https://nph.onlinelibrary.wiley.com/doi/suppl/"+DOI+"/supinfo/"+NAME,
  "https://onlinelibrary.wiley.com/doi/suppl/"+DOI+"/supinfo/"+NAME,
]
ALLOWED={"nph.onlinelibrary.wiley.com","onlinelibrary.wiley.com",
         "onlinelibrary.wiley.com","api.wiley.com"}
SIZE_MIN=1_000_000
SIZE_MAX=35_000_000

def attempt():
    receipts=[]
    for url in CANDIDATES:
        u=urllib.parse.urlparse(url)
        if u.scheme!="https" or u.hostname not in ALLOWED:
            raise ValueError("STAGE88_PUBLISHER_HOST_NOT_AN_OFFICIAL_WILEY_SITE")
        headers={"User-Agent":"Academic dataset source verification / floral macroecology"}
        req=urllib.request.Request(url,headers=headers)
        try:
            with urllib.request.urlopen(req,timeout=90) as res:
                content=res.read(SIZE_MAX+1)
                final=res.geturl()
                ct=res.headers.get("content-type","")
            if not SIZE_MIN<=len(content)<=SIZE_MAX:
                receipts.append({"url":url,"status":"REJECTED_NOT_SOURCE_SIZE",
                                 "actual_bytes":len(content),"mime":ct})
                continue
            with tempfile.TemporaryDirectory() as td:
                p=Path(td)/NAME;p.write_bytes(content)
                try:allobjects=pyreadr.read_r(str(p))
                except Exception as e:
                    receipts.append({"url":url,"status":"RDATA_DECODER_FAILED",
                          "actual_bytes":len(content),"exception":type(e).__name__,
                          "message":str(e)[:160]})
                    continue
                candidates={k:v for k,v in allobjects.items() if isinstance(v,pd.DataFrame)
                    and len(v)>170000
                    and any("polmodbinary"==x.casefold() for x in v.columns)
                    and any("genus_species"==x.casefold() for x in v.columns)}
            if len(candidates)!=1:
                receipts.append({"url":url,"status":"ORIGINAL_MODE_FRAME_NOT_UNIQUE",
                   "frame_keys":list(allobjects)})
                continue
            k=next(iter(candidates));df=candidates[k]
            s=next(x for x in df if x.casefold()=="genus_species")
            m=next(x for x in df if x.casefold()=="polmodbinary")
            return {"original_publisher_DOI":DOI,
               "original_supplement_filename":NAME,
               "successful_official_publisher_download_url":url,
               "original_supplement_sha256":hashlib.sha256(content).hexdigest(),
               "original_file_size_bytes":len(content),
               "original_source_data_frame_name":k,
               "original_source_rows":len(df),
               "original_source_unique_species":df[s].nunique(),
               "original_source_mode_codes":
                     df[m].astype("string").fillna("SOURCE_MISSING").value_counts().to_dict(),
               "no_source_class_imputation_or_phylogenetic_genus_reassignment":True,
               "actual_source_became_accessible":True,
               "failed_prior_public_endpoints":receipts}
        except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError,OSError) as e:
            receipts.append({"url":url,"status":"ORIGINAL_PUBLISHER_DOWNLOAD_UNAVAILABLE",
             "error_code":getattr(e,"code",None),
             "cause":type(e).__name__})
    return {"original_publisher_DOI":DOI,"original_supplement_filename":NAME,
        "original_source_became_accessible":False,
        "original_source_access_errors":receipts,
        "no_inferred_taxon_mode_or_manufactured_179263_records":True}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",required=True,type=Path)
    args=p.parse_args()
    d=attempt();args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n")
    print("STAGE88B3_OFFICIAL_PUBLIC_PUBLISHER_ORIGINAL_SUPPLEMENT",json.dumps(d))
if __name__=="__main__":main()
