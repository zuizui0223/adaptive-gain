"""Stage81B genuine 28-taxon early/late stage spectral-age feature extraction.

Inputs: original 286MB Ohashi et al. 2015 Zenodo ZIP with MD5/SHA256 and
Stage79D verified 28 exact accepted name overlaps. Owner original README:
  Reflectance/<Species>/<Species>-e10o.xls
  e/m/l are early/middle/late; digits denote sample number,
  suffix is measured petal area. Column 1 nm; column 6 %T/R.
The public ZIP also contains unevenly distributed AppleDouble ._*.xls metadata, NOT spectra.
Do not count or read them as separate samples.

This DOES NOT implement the author's D65/Apis receptor model, background
adaptation, hexagon-space 0.09 criterion, randomization and BH correction.
All outputs are RAW reflectance %-point magnitudes, not bee-visible/green
receptor contrast, true UV guides or wind/odor/visitation effects.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,math,re,sys,tempfile,zipfile
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np

STAGE79=Path(__file__).resolve().parents[1]/"floral_macro_stage79"
sys.path.insert(0,str(STAGE79))
from ohashi_2015_zip_central_directory_species_coverage import (
    download_author_full_verified,original_folders
)
AUTHOR_SHA="860ad9ef71d99efdda441fae00090ddb1dad0145f5c54a04b581b09490e718b7"
SOURCE_WAVELENGTH=np.arange(300,701,dtype=float)
FILE_RE=re.compile(r"-(?P<stage>[eml])(?P<sample>[0-9]{1,3})(?P<part>[A-Za-z]*)\.xls$",re.I)

def valid_source_workbook(path):
    p=path.replace("\\","/").split("/")
    return (path.lower().endswith(".xls") and
       not any(s.startswith("._") for s in p) and
       not any(s=="__MACOSX" for s in p))

def parse_filename(filename):
    name=Path(filename).name
    m=FILE_RE.search(name)
    if not m:return None
    replicate=int(m.group("sample"))
    if not 1<=replicate<=10:return None
    return m.group("stage").lower(),replicate,(m.group("part").lower() or "principal")

def read_real_source_spectrum(z,info):
    import xlrd
    raw=z.read(info)
    if not raw:raise ValueError("EMPTY_XLS")
    book=xlrd.open_workbook(file_contents=raw)
    sheet=book.sheet_by_index(0)
    if sheet.ncols<6 or sheet.nrows<390:
        raise ValueError("SOURCE_WRONG_SPECTRO_COLUMN_OR_TOO_FEW_ROWS")
    if str(sheet.cell_value(0,0)).casefold()!="wavelength" or str(sheet.cell_value(0,5)).strip()!="%T/R":
        raise ValueError("SOURCE_SPECTRUM_COLUMN_1_6_HEADER_DIFFERENT")
    values={}
    for idx in range(1,sheet.nrows):
        try:
            w=float(sheet.cell_value(idx,0));v=float(sheet.cell_value(idx,5))
        except (TypeError,ValueError):continue
        if not math.isfinite(w) or not math.isfinite(v):continue
        nearest=round(w)
        if 300<=nearest<=700 and abs(nearest-w)<.2:
            if nearest in values:raise ValueError("SOURCE_DUPLICATE_WAVELENGTH")
            values[nearest]=v
    if len(values)<395:
        raise ValueError("SOURCE_NO_COMPLETE_300_TO_700_1NM_GRID")
    if not all(w in values for w in range(300,701)):
        raise ValueError("SOURCE_MISSING_AT_LEAST_ONE_WAVELENGTH")
    y=np.array([values[int(w)] for w in SOURCE_WAVELENGTH])
    if not np.isfinite(y).all() or np.any(y<0) or np.any(y>120):
        raise ValueError("SOURCE_SPECTROMETER_REFLECTANCE_PERCENT_OUTSIDE_0_120")
    return y

def measured_early_late_metrics(early,late,seed=20261118,permutations=999):
    """Unpaired stage replicates; source sample numbers are NOT repeated individuals."""
    e=np.asarray(early,dtype=float);l=np.asarray(late,dtype=float)
    if e.ndim!=2 or l.ndim!=2 or e.shape[1]!=401 or l.shape[1]!=401:
        raise ValueError("EXPECTED_INDEPENDENT_SOURCE_401_POINT_SPECTRA")
    if len(e)<3 or len(l)<3:raise ValueError("TOO_FEW_ORIGINAL_REPLICATES")
    e_mean=e.mean(axis=0);l_mean=l.mean(axis=0)
    delta=l_mean-e_mean
    score=float(np.sqrt(np.mean(np.square(delta))))
    # Difference in group mean raw spectra, NOT an Apis chromatic distance.
    combined=np.concatenate([e,l],axis=0)
    rng=np.random.default_rng(seed)
    n=len(e)
    count=0
    for _ in range(permutations):
        permutation=rng.permutation(len(combined))
        d=combined[permutation[n:]].mean(axis=0)-combined[permutation[:n]].mean(axis=0)
        count+=float(np.sqrt(np.mean(np.square(d))))>=score-1e-12
    def band(a,b):
        return float(delta[a-300:b-300].mean())
    return {
        "n_early_independent_original_plant_samples":int(len(e)),
        "n_late_independent_original_plant_samples":int(len(l)),
        "raw_reflectance_early_late_RMS_percent_points":score,
        "raw_early_late_signed_delta_UV300_399_percent_points":band(300,400),
        "raw_early_late_signed_delta_blue400_499_percent_points":band(400,500),
        "raw_early_late_signed_delta_green500_599_percent_points":band(500,600),
        "raw_early_late_signed_delta_red600_700_percent_points":float(delta[300:401].mean()),
        "raw_spectrum_permutation_p_999_not_bee_colour":(1+count)/(1+permutations),
        "provenance_original_spectrum_early_late_unpaired":True,
        "not_receptor_or_perceptually_identifiable_0_09":True,
    }

def author_part_age_archive(z,roster):
    files=[f for f in z.infolist() if f.filename.lower().endswith(".xls")]
    original_count=len(files)
    valid=[f for f in files if valid_source_workbook(f.filename)]
    counted_meta=original_count-len(valid)
    folders,exact,_,_=original_folders([x.filename for x in z.infolist()])
    if len(folders)!=219 or len(roster)!=28:
        raise ValueError("NOT_219_ORIGINAL_SCREENED_OR_28_EUPP_ACCEPTED_TAXA")
    if len(exact.keys()&set(roster))!=28:
        raise ValueError("STAGE81B_NOT_ALL_28_SOURCE_EXACT_NAMES")
    bydir=defaultdict(list)
    for f in valid:
        p=f.filename.replace("\\","/").split("/")
        for i,s in enumerate(p):
            if s.lower()=="reflectance" and i+2<len(p):
                bydir[p[i+1]].append(f);break
    return original_count,len(valid),counted_meta,exact,bydir

def real_source_age_audit(z,roster):
    total,valid,meta,exact,bydir=author_part_age_archive(z,roster)
    # FULL archive scan, not a top-12 filename-pattern preview: exactly half are
    # AppleDouble metadata (sometimes hidden in __MACOSX, not a ._ basename).
    if total!=20490 or valid!=10245 or meta!=10245:
        raise ValueError("STAGE81B_FULL_SOURCE_TRUE_XLS_APPLEDOUBLE_COUNTS_CHANGED")
    actual_28=sum(len(bydir[exact[r]]) for r in roster)
    if actual_28!=1360:
        raise ValueError("STAGE81B_28_SOURCE_SPECIES_TRUE_WORKBOOK_COUNT_CHANGED")
    out=[];problems=[];audit=Counter()
    for literal in sorted(roster):
        author_folder=exact[literal]
        rows=defaultdict(list)
        replicate_seen=set()
        for f in bydir[author_folder]:
            info=parse_filename(f.filename)
            if not info:
                problems.append({"source_species":literal,
                   "source_file":Path(f.filename).name,"reason":"STAGE_PART_SAMPLE_NAME_UNRESOLVED"})
                continue
            stage,replicate,part=info
            ident=(stage,replicate,part)
            if ident in replicate_seen:
                raise ValueError("SOURCE_DUPLICATE_AGE_SAMPLE_PART_"+literal)
            replicate_seen.add(ident)
            try:
                vals=read_real_source_spectrum(z,f)
            except Exception as exc:
                problems.append({"source_species":literal,
                  "source_file":Path(f.filename).name,"reason":type(exc).__name__,
                  "detail":str(exc)[:120]})
                continue
            rows[part].append((stage,replicate,vals))
            audit["source_good_original_real_spectra"]+=1
        for part,replicates in sorted(rows.items()):
            e=[v for s,r,v in replicates if s=="e"]
            l=[v for s,r,v in replicates if s=="l"]
            m=[v for s,r,v in replicates if s=="m"]
            r={
              "source_original_accepted_species":literal,
              "original_author_spectrometer_folder":author_folder,
              "original_flower_part_literal":part,
              "source_early_samples":len(e),
              "source_middle_samples":len(m),
              "source_late_samples":len(l),
              "true_center_versus_outer_spatial_guide_not_confirmed":True,
              "source_original_28_species_not_all_bee_visible_colour_changers":True,
            }
            if len(e)>=3 and len(l)>=3:
                seed=int(hashlib.sha256((literal+part).encode()).hexdigest()[:8],16)
                r.update(measured_early_late_metrics(e,l,seed=seed))
                audit["source_true_early_late_matched_parts"]+=1
            else:
                r["status"]="NO_GO_INSUFFICIENT_SOURCE_STAGE_REPLICATES"
            out.append(r)
    audit.update({
      "original_zip_spreadsheet_extension_entries_including_AppleDouble":total,
      "true_original_excel_spectra_excluding_AppleDouble":valid,
      "excluded_AppleDouble_metadata_entries":meta,
      "distinct_EuPP_overlap_species":len(roster),
      "original_EuPP_28_species_spectra_entries":sum(len(bydir[exact[r]]) for r in roster),
      "original_28_species_independently_parsed_valid_real_workbooks":audit["source_good_original_real_spectra"],
      "original_28_species_part_records":len(out),
      "original_28_species_with_early_late_at_least_one_part":len({
       r["source_original_accepted_species"] for r in out
       if "raw_reflectance_early_late_RMS_percent_points" in r}),
      "source_biological_measured_absence_not_deduced_from_no_sheet":True,
      "source_no_d65_green_foliage_apis_receptor_model_or_author_0_09_classification":True,
      "source_original_individual_parts_not_independent_evolutionary_taxa":True,
    })
    return out,problems,dict(audit)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--stage79d-overlap",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    x=p.parse_args()
    source=json.loads(x.stage79d_overlap.read_text())
    if source["original_full_source_SHA256"]!=AUTHOR_SHA:
        raise ValueError("STAGE81B_ORIGINAL_AUTHOR_ZIP_SHA_MISMATCH_IN_PRIOR_AUDIT")
    names=source["exact_measured_species_with_2025_EuPP_visit_names"]
    with tempfile.TemporaryDirectory() as folder:
        fname=Path(folder)/"Ohashi_etal.zip"
        receipt=download_author_full_verified(fname)
        if receipt["original_full_source_SHA256"]!=AUTHOR_SHA:
            raise ValueError("STAGE81B_REAL_OHASHI_FULL_ZIP_SOURCE_SHA_CHANGED")
        with zipfile.ZipFile(fname) as z:
            rows,problems,counts=real_source_age_audit(z,names)
    x.outdir.mkdir(parents=True,exist_ok=True)
    # Only derived group-level phenotypes and reason codes; no bulk original data.
    fields=sorted(set().union(*(set(z) for z in rows)))
    with (x.outdir/"stage81b_28_species_source_early_late_part_spectral_metrics.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fields);w.writeheader();w.writerows(rows)
    with (x.outdir/"stage81b_28_species_spectrum_source_issues.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,["source_species","source_file","reason","detail"],extrasaction="ignore")
        w.writeheader();w.writerows(problems)
    report={
        "schema":"stage81b_original_ohashi_true_spectra_28_age_part_raw_reflectance_source",
        "author_full_source":receipt,
        "original_28_taxa_accepted_source_names":names,
        "original_true_source_counts":counts,
        "source_parsing_issue_count":len(problems),
        "source_issue_reason_frequencies":dict(Counter(z["reason"] for z in problems)),
        "source_age_raw_spectrum_only_not_bee_hexagon_colour_contrast":True,
        "published_48_bee_visible_out_of_219_not_assigned_to_28":True,
        "no_new_gust_scent_learning_landing_or_EuPP_visitor_effect_estimated":True,
    }
    (x.outdir/"stage81b_true_original_spectral_age_audit.json").write_text(
        json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+"\n")
    print("STAGE81B_OHASHI_REAL_28_AGE_PART_SOURCE_MEASURED_SPECTRA",
          json.dumps(counts,sort_keys=True),flush=True)
if __name__=="__main__":main()
