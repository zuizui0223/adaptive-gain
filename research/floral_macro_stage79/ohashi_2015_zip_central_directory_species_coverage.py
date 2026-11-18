"""Stage79D source-original Ohashi 2015 219 measured species via public ZIP directory.

Original Zenodo record 4942515 original author archive Ohashi_etal.zip
contains 285,933,377 bytes and 219 screened floral petal spectral species.
Fetch only official PUBLIC ZIP central-directory byte ranges to audit species
folder names, not 286MB of spectroscopy. No authentication workaround.
This is folder coverage of 219 SCREENED species; only 48/219 were reported
as bee-perceptible colour-changing in the original published model. None
of the other 171 is automatically "no biological colour change".

Archive full MD5 is original publisher metadata ONLY; partial ranges cannot
verify the full MD5, so never claim the entire raw ZIP was hash checked.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,io,re,struct,urllib.request,urllib.error
from collections import Counter,defaultdict
from pathlib import Path

ZIP_URL="https://zenodo.org/api/records/4942515/files/Ohashi_etal.zip/content"
SOURCE_RECORD="https://zenodo.org/api/records/4942515"
SOURCE_ORIGINAL_SIZE=285933377
AUTHOR_MD5_NOT_FULLY_RECHECKED="d98ddd3b93fb79fdbaaa5eec5818c187"
SOURCE_STAGE69_SHA="475863c2b193dd9c1eaad848dae05a9f518b57446cad2661979ca582c7d88617"
END_SIG=b"PK\x05\x06";CENTRAL_SIG=b"PK\x01\x02"
MAX_CENTRAL=30_000_000

def partial(start,end,session):
    if start<0 or end<start or end-start>MAX_CENTRAL:
        raise ValueError("STAGE79D_ORIGINAL_ARCHIVE_RANGE_OUT_OF_BOUNDS")
    hdr={"Range":f"bytes={start}-{end}",
         "Accept-Encoding":"identity","User-Agent":"adaptive-gain-original-Ohashi219-ZIP-index/2026"}
    req=urllib.request.Request(ZIP_URL,headers=hdr)
    with urllib.request.urlopen(req,timeout=80) as r:
        status=r.status;rangehdr=r.headers.get("Content-Range","")
        raw=r.read(MAX_CENTRAL+1)
    if status!=206 or not rangehdr.startswith(f"bytes {start}-{end}/"):
        raise ValueError("STAGE79D_ARCHIVE_RANGE_NOT_SUPPORTED_NO_DOWNLOAD_286MB")
    original_size=int(rangehdr.split("/")[-1])
    if original_size!=SOURCE_ORIGINAL_SIZE or len(raw)!=end-start+1:
        raise ValueError("STAGE79D_SOURCE_ORIGINAL_285933377_BYTES_IDENTITY_CHANGED")
    return raw,hashlib.sha256(raw).hexdigest()

def central_locator(original_size=SOURCE_ORIGINAL_SIZE):
    # Last 66k bytes cover ZIP EOCD including max 65,535 byte comment.
    start=max(0,original_size-70_000)
    tail,tailsha=partial(start,original_size-1,None)
    idx=tail.rfind(END_SIG)
    if idx<0 or idx+22>len(tail):
        raise ValueError("STAGE79D_ZIP_END_CENTRAL_DIRECTORY_NOT_FOUND")
    fields=struct.unpack_from("<IHHHHIIH",tail,idx)
    _,disk,diskdir,localentries,allentries,cd_size,cd_start,comment=fields
    if disk!=0 or diskdir!=0 or allentries==0xffff or cd_size==0xffffffff:
        raise ValueError("STAGE79D_SOURCE_ORIGINAL_ZIP64_OR_MULTIDISK_NOT_PARSED")
    if cd_size>MAX_CENTRAL or cd_start+cd_size>original_size:
        raise ValueError("STAGE79D_SOURCE_CENTRAL_INDEX_SIZE_NOT_VALID")
    return {"entries":allentries,"directory_start":cd_start,
            "directory_bytes":cd_size,"tail_source_SHA256":tailsha}

def central_names(src):
    start=src["directory_start"];end=start+src["directory_bytes"]-1
    b,sha=partial(start,end,None)
    names=[]
    pos=0
    while pos<len(b):
        if b[pos:pos+4]!=CENTRAL_SIG:
            raise ValueError("STAGE79D_SOURCE_BAD_CENTRAL_FILE_ENTRY_SIGNATURE")
        if pos+46>len(b):raise ValueError("STAGE79D_SOURCE_SHORT_CENTRAL_ENTRY")
        flag=struct.unpack_from("<H",b,pos+8)[0]
        name_length=struct.unpack_from("<H",b,pos+28)[0]
        extra_length=struct.unpack_from("<H",b,pos+30)[0]
        comment_length=struct.unpack_from("<H",b,pos+32)[0]
        finish=pos+46+name_length+extra_length+comment_length
        if finish>len(b):raise ValueError("STAGE79D_CENTRAL_FILENAME_OUT_OF_BOUNDS")
        n=b[pos+46:pos+46+name_length]
        name=n.decode("utf-8" if flag&0x800 else "cp437")
        names.append(name)
        pos=finish
    if len(names)!=src["entries"]:
        raise ValueError("STAGE79D_AUTHOR_ORIGINAL_ZIP_CENTRAL_FILE_COUNT_MISMATCH")
    return names,sha

def original_folder_species(names):
    folder=set()
    unparsed=[]
    for f in names:
        parts=f.strip("/").split("/")
        loc=next((i for i,v in enumerate(parts) if v.casefold()=="reflectance"),None)
        if loc is None or loc+1>=len(parts):continue
        if not parts[loc+1].strip() or parts[loc+1].startswith("."):continue
        folder.add(parts[loc+1])
    exact={}
    extra=[]
    for label in sorted(folder):
        normalized=" ".join(label.split("_"))
        if re.fullmatch(r"[A-Z][a-zA-Z-]+ [a-z][a-zA-Z-]+",normalized):
            exact[normalized.casefold()]=label
        else:extra.append(label)
    return folder,exact,extra

def source_roster(path):
    raw=Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SOURCE_STAGE69_SHA:
        raise ValueError("STAGE79D_ORIGINAL_CORRECTED_EUPP_VISIT_ROSTER_CHANGED")
    rows=list(csv.DictReader(io.StringIO(raw.decode("utf-8"))))
    return {r["Original_plant_accepted_name_literal"].strip().casefold() for r in rows}

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--original-Stage69-roster",required=True,type=Path)
    a.add_argument("--outdir",required=True,type=Path)
    q=a.parse_args();q.outdir.mkdir(exist_ok=True,parents=True)
    index=central_locator()
    names,hashregion=central_names(index)
    folder,binom,extras=original_folder_species(names)
    eu=source_roster(q.original_Stage69_roster)
    both=sorted(set(binom)&eu)
    report={"schema":"stage79d_original_Ohashi2015_219_screened_plant_zip_index_public_ranges",
      "original_author_Zenodo_source":SOURCE_RECORD,
      "original_author_ZIP_total_bytes":SOURCE_ORIGINAL_SIZE,
      "publisher_source_full_zip_MD5_NOT_checked_from_partial_ranges":AUTHOR_MD5_NOT_FULLY_RECHECKED,
      "original_ZIP_tail_Range_SHA256":index["tail_source_SHA256"],
      "original_source_central_index_Range_SHA256":hashregion,
      "original_source_zip_entry_count":index["entries"],
      "original_source_reflectance_species_folder_count":len(folder),
      "original_source_exact_simple_binomial_folder_species":len(binom),
      "original_source_nonbinomial_folders_may_contain_infraspecific":extras[:65],
      "original_source_exact_simple_binomial_EuPP_visiting_species":len(both),
      "original_source_exact_simple_binomial_EuPP_visiting_species_names":both,
      "source_archive_first15_pathnames":names[:15],
      "source_original_reflectance_archive_fully_checksum_verified":False,
      "published_219_measured_is_NOT_219_Bee_visible_colour_changes":True,
      "published_bee_visible_colour_change_48_of_219_NOT_joined_to_folders":True,
      "no_eup_pollinator_guild_outcomes_used_in_sampling":True,
      "no_flower_photographs_used":True,
    }
    (q.outdir/"original_ohashi_2015_zipped_219_spectrum_folder_species_EuPP_overlap.json").write_text(
        json.dumps(report,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("STAGE79D_ORIGINAL_OHASHI219_ZIP_CENTRAL_DIR_EUPP_SPECIES_MATCH",
          json.dumps(report,sort_keys=True))
if __name__=="__main__":main()
