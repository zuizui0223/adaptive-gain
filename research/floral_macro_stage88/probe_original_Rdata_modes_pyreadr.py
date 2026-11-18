"""Independent Python parser of the verified Wang et al 2025 original RData.

The author source Rdata file is small (2,719,385 bytes), and contains
179,263 documented pollination modes among 194,476 source species.
This source diagnostic verifies original API file SHA, lists every real
source object and source pollination code, without guessing numeric labels.
"""
from __future__ import annotations
import argparse,hashlib,json,urllib.request
from pathlib import Path
from collections import Counter
from tempfile import TemporaryDirectory
import pandas as pd
import pyreadr

URL="https://datadryad.org/api/v2/files/4049686/download"
SHA="dfb34e3ce42bb07bdae6e2dea71de3653155670bc3032bc11e5f2d58303759e6"
SIZE=2719385

def inspect():
    with TemporaryDirectory() as td:
        p=Path(td)/"Wang2025_original_179263_pollination_mode.Rdata"
        req=urllib.request.Request(URL,headers={"User-Agent":"independent-academic-global-pollination-2026"})
        with urllib.request.urlopen(req,timeout=150) as r:
            data=r.read(SIZE+1)
        if len(data)!=SIZE or hashlib.sha256(data).hexdigest()!=SHA:
            raise ValueError("STAGE88_POLLINATION_AUTHOR_SOURCE_SIZE_OR_SHA_CHANGED")
        p.write_bytes(data)
        frames=pyreadr.read_r(str(p))
    dataframes={k:v for k,v in frames.items() if isinstance(v,pd.DataFrame)}
    keys={k:{"rows":len(v),"columns":list(v.columns)} for k,v in dataframes.items()}
    target=[k for k,v in dataframes.items() if
            any("polmodbinary"==c.casefold() for c in v.columns) and
            any("genus_species"==c.casefold() for c in v.columns)]
    if len(target)!=1:
        raise ValueError("STAGE88_ORIGINAL_RDATA_POLLINATION_FRAME_MISSING_or_AMBIGUOUS "+str(keys)[:1200])
    df=dataframes[target[0]]
    species=next(c for c in df.columns if c.casefold()=="genus_species")
    mode=next(c for c in df.columns if c.casefold()=="polmodbinary")
    counts=Counter(df[mode].astype("string").fillna("__SOURCE_MISSING__"))
    attrs=[x for x in df.columns if "data" in x.casefold() and "pol" in x.casefold()]
    out={"schema":"stage88_original_Dryad_RData_179263_PolModbinary_independent_python_source",
      "author_original_file_SHA256":SHA,
      "author_original_bytes":SIZE,
      "real_RData_objects":keys,
      "source_pollination_data_frame":target[0],
      "source_original_dataframe_rows":len(df),
      "source_original_unique_species_string_count":df[species].nunique(),
      "source_PolModbinary_column":mode,
      "source_Genus_species_column":species,
      "source_original_pollination_code_values":dict(counts),
      "source_original_pollination_source_attribution_columns":attrs,
      "original_SourceofPolMod_attribution_top_values":{
        c:df[c].astype("string").value_counts(dropna=False).head(12).to_dict()
        for c in attrs},
      "not_a_species_by_native_region_distribution":True,
      "not_direct_field_measured_pollination_mode_for_every_species":True,
      "author_paper_figures_not_assumed_source_matched":True}
    return out

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args()
    o=inspect()
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(o,indent=2,sort_keys=True,ensure_ascii=False,default=str)+"\n")
    print("STAGE88_TRUE_AUTHOR_GLOBAL_MODE_ACTUAL_CODED_COUNTS",json.dumps(o,sort_keys=True,default=str))
if __name__=="__main__":main()
