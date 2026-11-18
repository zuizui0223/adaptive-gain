"""Stage85: original Ohashi age-stage spectra for the 50 strict DoPI-matched plants.

DoPI record is used ONLY as an outcome-blind source taxon roster.
No VOC, pollinator learning, wind, landing or fitness effect can follow
from colour measurements in Japan and visitation records in Europe.

Original Ohashi archive: 285933377 bytes, SHA256
860ad9ef71d99efdda441fae00090ddb1dad0145f5c54a04b581b09490e718b7.
Original DoPI v2 coverage receipt: Stage84 genuine source/CRC locked.
Only source-derived summary metrics are exported; 401 x N raw spectra
and age/part sample manifest MUST be deleted after pavo modeling.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,sys,tempfile,zipfile
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np

P81=Path(__file__).resolve().parents[1]/"floral_macro_stage81"
P79=Path(__file__).resolve().parents[1]/"floral_macro_stage79"
sys.path.insert(0,str(P81));sys.path.insert(0,str(P79))
from extract_real_ohashi_age_spectral_28 import (
    AUTHOR_SHA,valid_source_workbook,parse_filename,read_real_source_spectrum
)
from ohashi_2015_zip_central_directory_species_coverage import (
    original_folders,download_author_full_verified
)

STAGE84_RECEIPT_SHA="50c3f5a7468dff211fe0ca75d49bc50a1004930898742fe3f85a8ec0f22467a1"
DOPI_RESULT="stage84_original_DOPI_v2_Ohashi219_28_vs_EuPP_publication_coverage.json"
DOPI_ROSTER="stage84_original_219_source_name_180_strict_binomial_manifest.json"
EXPECTED_EUPP=28
EXPECTED_NEW=22
EXPECTED_FULL=50
EXPECTED_EUPP_SPECTRA=1360

def read_verified_stage84(stage84_zip):
    b=Path(stage84_zip).read_bytes()
    if hashlib.sha256(b).hexdigest()!=STAGE84_RECEIPT_SHA:
        raise ValueError("STAGE85_ORIGINAL_STAGE84_GENUINE_CROSSWALK_ZIP_SHA_CHANGED")
    with zipfile.ZipFile(stage84_zip) as z:
        src=json.loads(z.read(DOPI_RESULT))
        original=json.loads(z.read(DOPI_ROSTER))
    old={str(t).casefold() for t in original["current_28_actual_apis_receptor_modelled"]}
    add={str(t).casefold() for t in src["source_new_spectrometer_taxa_outside_current_28"]}
    allnames={str(t).casefold() for t in original["strict_180_original_author_taxa"]}
    assert len(old)==EXPECTED_EUPP and len(add)==EXPECTED_NEW
    if old&add or len(old|add)!=EXPECTED_FULL or not (old|add)<=allnames:
        raise ValueError("STAGE85_NOT_GENUINE_DISJOINT_28_22_SOURCE_FLORA")
    if src["source_180_original_exact_binomial_spectrometer_taxa"]["source_strict_matched_source_taxa"]!=50:
        raise ValueError("STAGE85_DOPI_50_ORIGINAL_SOURCE_SPECIES_CHANGED")
    if src["source_original_Ohashi_archive_verified"]["source_sha256"]!=AUTHOR_SHA:
        raise ValueError("STAGE85_AUTHOR_SOURCE_NOT_OHASHI_2015")
    return sorted(old|add),old,add,hashlib.sha256(b).hexdigest()

def parse_source_spectra(z,names):
    folders,exact,infra,unresolved=original_folders(z.namelist())
    if (len(folders),len(exact),len(infra),len(unresolved))!=(219,180,33,6):
        raise ValueError("STAGE85_ORIGINAL_OHASHI_219_SOURCE_FOLDERS_CHANGED")
    if not set(names)<=set(exact):
        raise ValueError("STAGE85_OHASHI_SOURCE_FOLDERS_MISSING_TARGET_TAXA")
    real=[f for f in z.infolist() if valid_source_workbook(f.filename)]
    if len(real)!=10245:
        raise ValueError("STAGE85_SOURCE_VALID_XLS_10245_CHANGED")
    byspecies=defaultdict(list)
    for f in real:
        parts=f.filename.replace("\\","/").split("/")
        for i,token in enumerate(parts):
            if token.casefold()=="reflectance" and i+2<len(parts):
                byspecies[parts[i+1]].append(f);break
    return exact,byspecies

def export(stage84_zip,outdir):
    taxa,old,new,receipt_sha=read_verified_stage84(stage84_zip)
    out=Path(outdir);out.mkdir(parents=True,exist_ok=True)
    issues=[];samples=[];data=[]
    original_counts=Counter()
    with tempfile.TemporaryDirectory() as tmp:
        author_zip=Path(tmp)/"Ohashi_etal.zip"
        author=download_author_full_verified(author_zip)
        if author["original_full_source_SHA256"]!=AUTHOR_SHA:
            raise ValueError("STAGE85_OHASHI_AUTHENTIC_FULL_ZIP_SHA_CHANGED")
        with zipfile.ZipFile(author_zip) as z:
            exact,byspecies=parse_source_spectra(z,taxa)
            allfiles=[f.filename.replace("\\","/") for f in z.infolist()]
            has_specs={sp:any(
                f"/Reflectance/{exact[sp]}/" in name and
                "specification" in Path(name).name.casefold() and
                "__MACOSX" not in name and "/._" not in name
                for name in allfiles) for sp in taxa}
            for sp in taxa:
                seen=set()
                for f in sorted(byspecies[exact[sp]],key=lambda q:q.filename):
                    group=parse_filename(f.filename)
                    if group is None:
                        issues.append({"source_species":sp,"original_filename":Path(f.filename).name,
                              "reason":"AUTHOR_STAGE_SAMPLE_PART_FILENAME_UNRESOLVED"})
                        continue
                    stage,rep,part=group
                    k=(stage,rep,part)
                    if k in seen:
                        raise ValueError("STAGE85_DUPLICATE_AUTHOR_SPECIES_STAGE_REPLICATE_PART_"+sp)
                    seen.add(k)
                    try:
                        spectrum=read_real_source_spectrum(z,f)
                    except Exception as exc:
                        issues.append({"source_species":sp,"original_filename":Path(f.filename).name,
                            "reason":"INVALID_SOURCE_XLS_REFLECTANCE_GRID_"+type(exc).__name__,
                            "details":str(exc)[:120]})
                        continue
                    sid="s"+str(len(data)+1).zfill(6)
                    data.append(spectrum)
                    samples.append({"sample_id":sid,"source_species":sp,
                        "original_stage":stage,"original_individual_sample_number":rep,
                        "original_flower_part":part,"has_author_part_specifications":int(has_specs[sp]),
                        "source_species_new_for_DOPI":int(sp in new)})
                    original_counts["valid_total"]+=1
                    original_counts["valid_new_22" if sp in new else "valid_prior_28"]+=1
    # Preserve the empirically verified 28-source subset with exactly 1,360 samples.
    if original_counts["valid_prior_28"]!=EXPECTED_EUPP_SPECTRA:
        raise ValueError("STAGE85_EXISTING_28_SOURCE_XLS_1360_REPRODUCIBILITY_FAILED")
    stage_part=defaultdict(lambda:{"e":set(),"m":set(),"l":set()})
    for r in samples:
        stage_part[(r["source_species"],r["original_flower_part"])][r["original_stage"]].add(
             r["original_individual_sample_number"])
    eligible={k for k,v in stage_part.items() if len(v["e"])==10 and len(v["l"])==10}
    incomplete={k:v for k,v in stage_part.items() if k not in eligible}
    valid_taxa={sp for sp,part in eligible}
    if not new <= {r["source_species"] for r in samples}:
        raise ValueError("STAGE85_SOURCE_TAXON_WITH_ZERO_VALID_SPECTRA")
    if not old <= valid_taxa:
        raise ValueError("STAGE85_PRIOR_28_SPECIES_EARLY_LATE_REGRESSION")
    if len(data)<=1360 or len({r["source_species"] for r in samples})!=50:
        raise ValueError("STAGE85_NOT_ALL_50_OHASHI_SOURCE_SPECIES_OR_SAMPLES")
    arr=np.array(data,dtype=float).T
    if arr.shape!=(401,len(samples)) or not np.isfinite(arr).all():
        raise ValueError("STAGE85_SOURCE_SPECTRAL_MATRIX_NOT_401_WAVELENGTHS")
    wide=out/"temp_original_50_stage_spectra_wide.csv"
    with wide.open("w",newline="",encoding="utf-8") as h:
        w=csv.writer(h)
        w.writerow(["wl"]+[r["sample_id"] for r in samples])
        for ix,vals in enumerate(arr):w.writerow([ix+300]+[format(float(v),".5f") for v in vals])
    manifest=out/"temp_original_50_source_sample_manifest.csv"
    with manifest.open("w",newline="",encoding="utf-8") as h:
        wr=csv.DictWriter(h,list(samples[0]))
        wr.writeheader();wr.writerows(samples)
    result={
       "schema":"stage85_full_authentic_Ohashi_original_50_DOPI_strict_binomial_source_spectra",
       "original_2015_author_MD5_SHA_verified":author,
       "source_previous_stage84_real_DOPI_coverage_artifact_zip_sha256":receipt_sha,
       "original_50_source_species_with_spectra":len({r["source_species"] for r in samples}),
       "source_original_spectral_replicates_all":len(samples),
       "source_original_prior_28_true_spectral_replicates":original_counts["valid_prior_28"],
       "source_original_new_22_true_spectral_replicates":original_counts["valid_new_22"],
       "original_spectrometer_taxa_eligible_early_late":len(valid_taxa),
       "original_new_22_with_valid_early_late":len(valid_taxa&new),
       "original_old_28_with_valid_early_late":len(valid_taxa&old),
       "original_flower_parts_total":len(stage_part),
       "original_flower_parts_early_late_10_each":len(eligible),
       "original_flower_parts_not_equal_10_and_10":[
          {"taxon":sp,"part":p,"e":len(v["e"]),"m":len(v["m"]),"l":len(v["l"])}
          for (sp,p),v in sorted(incomplete.items())],
       "original_source_spectra_issues":issues[:100],
       "source_issues_count":len(issues),
       "source_50_spectra_matrix_401_wavelengths_sha256":hashlib.sha256(wide.read_bytes()).hexdigest(),
       "source_50_spectra_sample_manifest_sha256":hashlib.sha256(manifest.read_bytes()).hexdigest(),
       "source_new_22_exact_taxa":sorted(new),
       "source_28_previous_taxa":sorted(old),
       "temporary_full_original_reflectance_matrix_NOT_to_be_redistributed":True,
       "not_Bombus_perceptual_parameters_or_wind_learning_landing":True
    }
    (out/"stage85_source_50_spectrometer_manifest_receipt.json").write_text(
      json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    print("STAGE85_ORIGINAL_50_TRUE_SPECTRA",json.dumps({
      k:v for k,v in result.items() if isinstance(v,(str,int,bool))},sort_keys=True),flush=True)
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source-stage84-artifact-zip",required=True,type=Path)
    p.add_argument("--outdir",required=True,type=Path)
    args=p.parse_args()
    export(args.source_stage84_artifact_zip,args.outdir)
if __name__=="__main__":main()
