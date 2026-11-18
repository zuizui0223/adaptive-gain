"""Stage79D original 2015 Ohashi 219 species ZIP archive structure audit.

Source exact public Zenodo original Ohashi_etal.zip (285,933,377 bytes;
official author MD5 d98ddd3b93fb79fdbaaa5eec5818c187). Range is
sometimes disabled by public Zenodo, so this uses standard public HTTPS
streamed GET, no auth, checking FULL original MD5 + byte size. Read only
ZIP directory entries (not source images and not invent early/late spectra).
Original 219 studied flower taxa are NOT 219 positive colour-change species.

Match original author species folder names to original EuPPPollNet 1408
strict accepted plant names, exact two-term species only. Recognize variants
separately, never silently collapse infraspecific names or synonym guesses.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,re,tempfile,urllib.request,zipfile
from collections import Counter,defaultdict
from pathlib import Path

ORIGINAL_URL="https://zenodo.org/api/records/4942515/files/Ohashi_etal.zip/content"
SOURCE_BYTES=285933377
SOURCE_MD5="d98ddd3b93fb79fdbaaa5eec5818c187"
SOURCE_STAGE69_SHA="475863c2b193dd9c1eaad848dae05a9f518b57446cad2661979ca582c7d88617"
EXPECTED_SCREENED=219
BINOMIAL=re.compile(r"^[A-Z][A-Za-z-]+ [a-z][A-Za-z-]+$")
EPITHETS_UNKNOWN={"species","sp","spp","aff","cf","hybrid","unknown"}
MAX_ENTRIES=300000

def download_author_full_verified(output):
    temp=output.with_suffix(".partial")
    for attempt in range(2):
        h=hashlib.md5();sha=hashlib.sha256();n=0
        req=urllib.request.Request(ORIGINAL_URL,headers={
            "Accept":"application/zip,application/octet-stream,*/*",
            "User-Agent":"academic-open-original-flower-age-colour-data-2026"})
        try:
            with urllib.request.urlopen(req,timeout=130) as stream,temp.open("wb") as f:
                while True:
                    b=stream.read(4*1024*1024)
                    if not b:break
                    f.write(b);n+=len(b);h.update(b);sha.update(b)
                    if n>SOURCE_BYTES:
                        raise ValueError("STAGE79D_PUBLIC_AUTHOR_ZIP_EXCEEDS_PINNED_BYTE_SIZE")
            if n!=SOURCE_BYTES or h.hexdigest()!=SOURCE_MD5:
                raise ValueError(f"STAGE79D_ORIGINAL_AUTHOR_MD5_OR_BYTES_CHANGED size={n} MD5={h.hexdigest()}")
            temp.replace(output)
            return {"original_downloaded_bytes":n,
              "original_author_MD5_recomputed":h.hexdigest(),
              "original_full_source_SHA256":sha.hexdigest(),
              "original_source_full_bytes_and_MD5_verified":True,
              "source_original_Zenodo_public_url":ORIGINAL_URL}
        except (TimeoutError,OSError) as exc:
            if attempt==1:raise
            temp.unlink(missing_ok=True)
    raise RuntimeError("STAGE79D_SOURCE_DOWNLOAD_UNAVAILABLE")

def original_folders(names):
    folders=set()
    for name in names:
        # Published author README: Reflectance/<Species_folder>/*.xls.
        p=[z for z in name.replace("\\","/").strip("/").split("/") if z]
        indices=[i for i,s in enumerate(p) if s.casefold()=="reflectance"]
        for idx in indices:
            if idx+1>=len(p):continue
            child=p[idx+1]
            if child.startswith(".") or child.startswith("__MACOSX"):continue
            folders.add(child)
    exact={};infra={};unresolved=[]
    for folder in sorted(folders):
        norm=" ".join(folder.split("_"))
        if BINOMIAL.fullmatch(norm):
            genus,epithet=norm.split()
            if epithet.casefold() not in EPITHETS_UNKNOWN:
                if norm.casefold() in exact:
                    raise ValueError("STAGE79D_DUPLICATED_DISTINCT_SOURCE_FOLDER_NAMES")
                exact[norm.casefold()]=folder
            else:unresolved.append(folder)
        elif any(z in norm.casefold().split() for z in ("var","subsp","ssp")):
            infra[folder]=norm
        else:unresolved.append(folder)
    return folders,exact,infra,unresolved

def source_field_plant_universe(path):
    raw=Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SOURCE_STAGE69_SHA:
        raise ValueError("STAGE79D_TRUE_1408_EUPP_SOURCE_VISITOR_ROSTER_SHA_CHANGED")
    import io
    r=list(csv.DictReader(io.StringIO(raw.decode("utf-8"))))
    names={a["Original_plant_accepted_name_literal"].strip().casefold() for a in r}
    if len(r)!=18798 or len(names)!=1408:
        raise ValueError("STAGE79D_ORIGINAL_EURO_VISIT_PLANT_DENOMINATOR_CHANGED")
    return names

def audit_zip(source,plant_names,receipt):
    with zipfile.ZipFile(source) as z:
        member=z.infolist()
        if len(member)>MAX_ENTRIES:raise ValueError("STAGE79D_ARCHIVE_UNEXPECTED_FILES_OVER_LIMIT")
        names=[x.filename for x in member]
        folders,exact,infra,unknown=original_folders(names)
        if len(folders)!=EXPECTED_SCREENED:
            raise ValueError("STAGE79D_NOT_219_ORIGINAL_AUTHOR_MEASURED_FLOWER_FOLDERS_"+str(len(folders)))
        spectra_names=[x.filename for x in member if x.filename.casefold().endswith((".xls",".xlsx"))]
    common=sorted(set(exact)&plant_names)
    return {**receipt,
      "schema":"stage79d_full_original_Ohashi2015_219_early_mid_late_petals_spectral_zip_vs_real_visits",
      "original_author_published_219_screened_species_not_verified_visible_change_219":True,
      "original_author_published_48_bee_visible_changes_not_linked_to_source_folders":True,
      "original_source_219_distinct_spectral_taxon_folders":len(folders),
      "original_source_all_ZIP_members":len(member),
      "original_source_spectral_spreadsheet_member_count":len(spectra_names),
      "original_two_token_binomial_spectral_source_taxa":len(exact),
      "original_infraspecific_source_folders_separate":len(infra),
      "original_unresolved_original_source_folders":unknown[:35],
      "exact_measured_2015_spectrometer_species_with_2025_EuPP_visits":len(common),
      "exact_measured_species_with_2025_EuPP_visit_names":common,
      "source_flower_stage_colour_change_not_inferred_from_folder_membership":True,
      "original_infraspecific_and_synonyms_NOT_fuzzy_merged":True,
      "source_spectrometer_early_to_late_receptor_model_not_yet_recomputed":True,
      "source_2015_Japan_original_spectrometer_not_Europe_same_field_site":True,
      "source_no_photos_or_flower_image_trait_extraction":True,
      "source_no_Bombus_or_gust_effect_model_fitted":True,
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--original-Stage69-roster",required=True,type=Path)
    p.add_argument("--outdir",required=True,type=Path)
    a=p.parse_args();a.outdir.mkdir(parents=True,exist_ok=True)
    names=source_field_plant_universe(a.original_Stage69_roster)
    with tempfile.TemporaryDirectory() as tmp:
        fname=Path(tmp)/"Ohashi_etal.zip"
        receipt=download_author_full_verified(fname)
        report=audit_zip(fname,names,receipt)
    (a.outdir/"original_ohashi_2015_zipped_219_spectrum_folder_species_EuPP_overlap.json").write_text(
        json.dumps(report,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("STAGE79D_TRUE_AUTHOR_OHASHI_219_SPECTROMETER_SPECIES_COVERAGE",
        json.dumps(report,sort_keys=True))
if __name__=="__main__":main()
