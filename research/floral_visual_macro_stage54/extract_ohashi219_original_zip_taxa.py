"""Stage54: original Ohashi et al 2015 219-spp spectra archive taxon list.

Only read ZIP central directory byte ranges of the original 285.9-MB
Zenodo deposit. The dataset README was separately verified by MD5 and
states 219 folders named for the taxa with 300–700nm stage-specific
early/middle/late spectra. Original file content / spectral values are
NOT read or claimed verified until a separate member fetch.

This stage builds a 219 *measured at different stages* taxon-name
source frame; it DOES NOT assign each species a positive/negative
perceptible colour-change state from the archive filename alone.
"""
from __future__ import annotations
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import struct
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"floral_visual_macro_stage46"))
from zip_range_catalog import get_range,parse_central_directory

ZENODO_URL="https://zenodo.org/api/records/4942515/files/Ohashi_etal.zip/content"
FILE_SIZE=285933377
ORIGINAL_FILE_MD5="md5:d98ddd3b93fb79fdbaaa5eec5818c187"
MAX_CENTRAL_DIR=18_000_000
CHUNK=3_000_000

def source_index():
    # GitHub/Zenodo metadata above was independently confirmed in the
    # Stage54 access probe; range checks must match file size, not whole MD5.
    tail_start=FILE_SIZE-262144
    tail=get_range(ZENODO_URL,FILE_SIZE,tail_start,FILE_SIZE-1)
    idx=tail.rfind(b"PK\x05\x06")
    if idx<0 or len(tail)-idx<22:
        raise ValueError("NO_GO_OHASHI_ORIGINAL_ZIP_EOCD_MISSING")
    _,disk,cd_disk,ndisk,ntotal,length,offset,comment=struct.unpack_from(
        "<4s4HIIH",tail,idx)
    if disk!=0 or cd_disk!=0 or ndisk!=ntotal or ntotal in (0,0xffff) or length==0xffffffff:
        raise ValueError("NO_GO_ZIP64_ORIGINAL_OHASHI_ARCHIVE_NOT_SUPPORTED")
    if offset+length>FILE_SIZE or length>MAX_CENTRAL_DIR:
        raise ValueError("NO_GO_ZENODO_219_SOURCE_CENTRAL_DIRECTORY_SIZE")
    blocks=[]
    for start in range(offset,offset+length,CHUNK):
        stop=min(offset+length,start+CHUNK)-1
        blocks.append(get_range(ZENODO_URL,FILE_SIZE,start,stop))
    original_cd=b"".join(blocks)
    if len(original_cd)!=length:
        raise ValueError("NO_GO_OHASHI_CD_TRUNCATED")
    items=parse_central_directory(original_cd,ntotal)
    source_names=Counter()
    modes=Counter()
    examples=[]
    for item in items:
        path=item["filename"].replace("\\","/")
        parts=[p for p in path.split("/") if p and p not in (".","..")]
        if (len(parts)>=3 and parts[0]=="Ohashi_etal"
            and parts[1]=="Reflectance"
            and parts[2] not in (".DS_Store",)
            and not parts[2].startswith("._")
            and not path.endswith("/")):
            source_names[parts[2]]+=1
            if len(parts)>3 and not Path(parts[-1]).name.startswith("._"):
                modes[Path(parts[-1]).suffix.lower()]+=1
        if len(examples)<18:
            examples.append(path[:220])
    return {
       "status":"ORIGINAL_OHASHI_2015_219_SOURCE_SPECTRAL_TAXON_ZIP_DIRECTORY",
       "original_source_doi":"10.5061/dryad.8fh42",
       "zenodo_original_record_id":4942515,
       "original_Zenodo_deposit_md5":ORIGINAL_FILE_MD5,
       "source_file_size_bytes_verified_by_http_ranges":FILE_SIZE,
       "original_index_byte_ranges_verified":len(original_cd)+len(tail),
       "central_directory_source_SHA256":hashlib.sha256(original_cd).hexdigest(),
       "n_source_archive_members":len(items),
       "n_original_spectral_species_directory_names":len(source_names),
       "species_source_directory_names":sorted(source_names),
       "files_per_species_summary":{
           "min":min(source_names.values()) if source_names else None,
           "max":max(source_names.values()) if source_names else None,
       },
       "observed_spectral_file_suffixes":dict(modes),
       "first_original_source_archive_paths":examples,
       "source_taxa_are_original_spectral_study_not_verified_colour_changers":True,
       "whole_285MB_ZIP_checksum_not_independently_verified_by_partial_ranges":True,
       "no_UV_guide_or_age_change_label_extracted_from_names_only":True,
       "no_phylogeny_or_Bombus_geographic_effect":True,
    }

def main():
    x=source_index()
    folder=Path("stage54_219_original_spectral_species")
    folder.mkdir(exist_ok=True)
    (folder/"original_Zenodo_219_spectral_species_directory_receipt.json").write_text(
        json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+"\n",
        encoding="utf8")
    print("STAGE54_SOURCE_OHASHI_219_SPECTRAL_ORIGINAL_TAXON_DIRECTORY",
          json.dumps({k:v for k,v in x.items()
                      if k!="species_source_directory_names"},sort_keys=True))
    print("STAGE54_FIRST_20_OHASHI_TAXON_DIRS",
          json.dumps(x["species_source_directory_names"][:20],ensure_ascii=False))
    if x["n_original_spectral_species_directory_names"]!=219:
        raise SystemExit("NO_GO_SOURCE_219_TAXA_NOT_RECOVERED_FROM_AUTHORED_ARCHIVE")


if __name__=="__main__":
    main()
