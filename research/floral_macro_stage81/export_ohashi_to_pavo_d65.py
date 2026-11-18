"""Stage81D: export ORIGINAL 28 source spectra (true XLS) for receptor analysis.

No source original ZIP or sample spectra are committed or published. The
temporary sample matrix is consumed by pavo in CI, and deleted after the run.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,tempfile,zipfile
from collections import Counter
from pathlib import Path
import numpy as np
from extract_real_ohashi_age_spectral_28 import (
    AUTHOR_SHA,download_author_full_verified,author_part_age_archive,
    valid_source_workbook,parse_filename,read_real_source_spectrum
)

def build(original_overlap,output):
    roster=json.loads(Path(original_overlap).read_text())
    if roster["original_full_source_SHA256"]!=AUTHOR_SHA:
        raise ValueError("STAGE81D_SOURCE_ZIP_DIGEST_PRIOR_CHANGED")
    names=roster["exact_measured_species_with_2025_EuPP_visit_names"]
    if len(names)!=28:raise ValueError("STAGE81D_WRONG_28_ORIGINAL_TAXA")
    out=Path(output);out.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        archive=Path(tmp)/"Ohashi_etal.zip"
        receipt=download_author_full_verified(archive)
        if receipt["original_full_source_SHA256"]!=AUTHOR_SHA:
            raise ValueError("STAGE81D_AUTHOR_286MB_SOURCE_NOT_IDENTICAL")
        with zipfile.ZipFile(archive) as z:
            _,real,meta,exact,bydir=author_part_age_archive(z,names)
            if real!=10245 or meta!=10245:
                raise ValueError("STAGE81D_REAL_MAC_DOUBLE_XLS_MISMATCH")
            arrays=[];fields=[];issues=[];replicates=set()
            specification=set()
            for f in z.namelist():
                if ("specification" not in Path(f).name.lower() or
                    "__MACOSX" in f or "/._" in f):continue
                for n in names:
                    if "/Reflectance/"+exact[n]+"/" in f.replace("\\","/"):
                        specification.add(n)
            for source_species in sorted(names):
                for f in sorted(bydir[exact[source_species]],key=lambda x:x.filename):
                    x=parse_filename(f.filename)
                    if not x:
                        issues.append({"species":source_species,"file":f.filename,
                                       "reason":"SOURCE_AGE_SAMPLE_PART_NAME_UNRESOLVED"})
                        continue
                    stage,rep,part=x
                    key=(source_species,stage,rep,part)
                    if key in replicates:
                        raise ValueError("STAGE81D_SOURCE_DUPLICATED_SAMPLE_ID")
                    replicates.add(key)
                    spectra=read_real_source_spectrum(z,f)
                    sid="s"+str(len(arrays)+1).zfill(5)
                    arrays.append(spectra)
                    fields.append({
                       "sample_id":sid,"source_species":source_species,
                       "original_stage":stage,"original_individual_sample_number":rep,
                       "original_flower_part":part,
                       "has_author_part_specifications":int(source_species in specification),
                    })
    if issues or len(arrays)!=1360 or len({f["source_species"] for f in fields})!=28:
        raise ValueError("STAGE81D_FALSE_ORIGINAL_28_SPECIES_1360_SPECTRA_SOURCE_COMPLETENESS")
    x=np.array(arrays,dtype=float).T
    if x.shape!=(401,1360) or not np.isfinite(x).all():
        raise ValueError("STAGE81D_SPECTRAL_WIDE_MATRIX_INCOMPLETE")
    with (out/"temp_original_28_spectra_wide.csv").open("w",newline="") as h:
        writer=csv.writer(h)
        writer.writerow(["wl"]+[z["sample_id"] for z in fields])
        for i,row in enumerate(x):writer.writerow([300+i]+[format(float(v),".5f") for v in row])
    with (out/"temp_original_28_spectra_manifest.csv").open("w",newline="") as h:
        writer=csv.DictWriter(h,fieldnames=list(fields[0]));writer.writeheader();writer.writerows(fields)
    receipt.update({
        "schema":"stage81d_receptor_input_original_unredistributed_28_species_1360_true_spectra",
        "real_original_28_spectrometer_workbooks":len(arrays),
        "source_28_spectra_age_part_manifest_sha256":hashlib.sha256(
           (out/"temp_original_28_spectra_manifest.csv").read_bytes()).hexdigest(),
        "source_Python_to_R_original_wide_401x1360_sha256":hashlib.sha256(
           (out/"temp_original_28_spectra_wide.csv").read_bytes()).hexdigest(),
        "source_author_custom_part_specifications_species":len(specification),
        "source_original_recorded_age_groups":dict(Counter(f["original_stage"] for f in fields)),
        "no_original_source_raw_spectral_data_redistributed":True
    })
    (out/"stage81d_manifest_provenance_receipt.json").write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
    print("STAGE81D_SOURCE_ORIGINAL_R_PAVO_INPUT",json.dumps({
      "real_sample_spectra":len(fields),"source_true_401_wavelengths":401,
      "author_custom_part_spec_taxa":len(specification),
      "age_groups":receipt["source_original_recorded_age_groups"]}),flush=True)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--stage79d-overlap",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    opt=p.parse_args()
    build(opt.stage79d_overlap,opt.outdir)
