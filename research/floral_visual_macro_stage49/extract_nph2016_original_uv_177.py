"""Stage49: extract the actual original 177 Potentilleae UV pattern species source.

Koski & Ashman 2016, New Phytologist DOI 10.1111/nph.13921,
official PMC OA supplemental NPH-211-708-s001.pdf, Table S2 pages
18–23 (1-based). Source model property verified separately via source
PDF SHA256 and the source 2016 Fig 2 number (86 patterned/91 uniform).

CRITICAL: Original Table S2 source code is 0 for UV PATTERN PRESENT
(UVP < .95), 1 for UNIFORM (UVP >= .95). Never invert to yes=1.
Do not substitute the 2020 differently thresholded UV pattern labels
or count its repeated taxa as a second independent 177-plant cohort.
"""
from __future__ import annotations
from collections import Counter
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import zipfile

from probe_nph2016_177_europepmc_supplement import _fetch,API

ORIGINAL_SUPPLEMENT_ZIP_SHA256="586c26b387bb3e95bb75314eec96548919b4dc069201574568ac84e4dba6dc5a"
ORIGINAL_TABLE_PDF_SHA256="8936dc9dabc8e96d37ba98ef6c940c98d545b62f3260634bce8dfd0a4f74bd94"
MEMBER="NPH-211-708-s001.pdf"
PAGES=(17,18,19,20,21,22)
EXPECTED_SOURCE_ROWS=177
STUDY_DOI="10.1111/nph.13921"
ID=re.compile(r"^[A-Z]{1,2}_[a-z][a-z_0-9]*$",re.I)

def _number(s,field,can_missing=False):
    if s in ("NA","N/A","-","", "nan","NaN"):
        if can_missing:
            return None
        raise ValueError("NO_GO_UV_SOURCE_MISSING_"+field)
    try:
        v=float(s.replace("−","-"))
    except (TypeError,ValueError) as e:
        raise ValueError("NO_GO_UV_SOURCE_UNEXPECTED_NUMERIC_"+field+":"+str(s)[:50]) from e
    return v

def parse_source_rows(page_texts):
    found={}
    errors=[]
    for index,text in sorted(page_texts.items()):
        if index not in PAGES:
            raise ValueError("NO_GO_ORIGINAL_TABLE_S2_PAGE")
        lines=[re.sub(r"\s+"," ",x).strip() for x in text.splitlines() if x.strip()]
        starts=[i for i,s in enumerate(lines) if ID.fullmatch(s)]
        if not starts:
            raise ValueError("NO_GO_NO_SOURCE_SPECIES_LABELS_ON_PAGE_"+str(index))
        for j,start in enumerate(starts):
            stop=starts[j+1] if j+1<len(starts) else len(lines)
            code=lines[start]
            vals=lines[start+1:stop]
            source_wrapped_taxon=False
            # Original PDF wraps two long Ivesia subspecies epithets onto
            # the next text line. Join literal source text, never guess
            # synonyms, and preserve the line-wrapping provenance flag.
            if len(vals)==9 and re.fullmatch(r"[a-z]{1,12}",vals[0]):
                code=code+vals.pop(0)
                source_wrapped_taxon=True
            if len(vals)!=8:
                errors.append({"page":index+1,"source_taxon_code":code,
                               "n_source_value_lines":len(vals),
                               "first_value_tokens":vals[:12]})
                continue
            if code in found:
                raise ValueError("NO_GO_DUPLICATE_SOURCE_UV_TAXON_CODE")
            uvp=_number(vals[0],"UVP")
            if vals[1] not in ("0","1"):
                raise ValueError("NO_GO_UV_SOURCE_PATTERN_CODE_NOT_BINARY_"+code)
            flag=int(vals[1])
            colour=vals[2]
            if colour not in ("Y","W","R"):
                raise ValueError("NO_GO_UV_SOURCE_VISIBLE_COLOR_NOT_RECOGNIZED_"+code)
            d={
              "original_taxon_code":code,
              "original_taxon_code_split_across_source_PDF_lines":source_wrapped_taxon,
              "orig_2016_UV_proportion_absorbing":uvp,
              "source_TableS2_UV_pattern_0_present_1_absent":flag,
              "source_measured_UV_pattern_present":1-flag,
              "human_visible_flower_colour_code":colour,
              "source_mean_altitude_m":_number(vals[3],"ALT",True),
              "source_mean_latitude_deg":_number(vals[4],"LAT",True),
              "source_mean_annual_temp_C":_number(vals[5],"TEMP",True),
              "source_mean_annual_precip_mm":_number(vals[6],"PRECIP",True),
              "source_mean_UVB_J_per_m2_per_day":_number(vals[7],"UVB",True),
              "source_study_doi":STUDY_DOI,
              "real_source_UV_photo_pattern":True,
              "full_taxon_name_resolution_status":"ORIGINAL_AUTHOR_ABBREVIATED_SPECIES_CODE",
              "gbif_accepted_species_key":"",
              "Bombus_source_model_overlap":"NOT_COMPUTED",
              "original_source_PDF_sha256":ORIGINAL_TABLE_PDF_SHA256,
            }
            if not (0<=uvp<=1):
                raise ValueError("NO_GO_UV_ABSORPTION_PROPORTION_OUT_OF_RANGE")
            # Report discrepancies rather than silently overriding author
            # categorization; displayed UVP is rounded to two decimals.
            d["UVP_rounded_threshold_vs_author_discrete_code"] = (
                "CHECK_SOURCE_ROUNDED_THRESHOLD"
                if (flag==0 and uvp>=.95) or (flag==1 and uvp<.95)
                else "CONSISTENT_AT_TWO_DECIMAL_PRECISION"
            )
            found[code]=d
    if errors:
        raise ValueError("NO_GO_SOURCE_TABLE_S2_NON_RECTANGULAR_ROWS "+json.dumps(errors[:16],ensure_ascii=False))
    return list(found.values())

def summarize(rows):
    n=len(rows)
    if n!=EXPECTED_SOURCE_ROWS:
        raise ValueError("NO_GO_SOURCE_177_TAXA_NOT_RECOVERED: "+str(n))
    code=Counter(r["source_TableS2_UV_pattern_0_present_1_absent"] for r in rows)
    if code!={0:86,1:91}:
        raise ValueError("NO_GO_SOURCE_2016_PUBLISHED_PATTERN_COUNTS_DIFFER "+str(code))
    mismatches=[
        {"source_taxon_code":r["original_taxon_code"],
         "original_reported_UVP":r["orig_2016_UV_proportion_absorbing"],
         "author_discrete_UV_code":r["source_TableS2_UV_pattern_0_present_1_absent"]}
        for r in rows if r["UVP_rounded_threshold_vs_author_discrete_code"]!=
        "CONSISTENT_AT_TWO_DECIMAL_PRECISION"
    ]
    colors=Counter(r["human_visible_flower_colour_code"] for r in rows)
    gen=Counter(r["original_taxon_code"].split("_")[0] for r in rows)
    return {
      "status":"AUTHENTIC_NPH2016_SOURCE_177_POTENTILLEAE_SPECIES_UV_PHENOTYPES",
      "n_original_2016_source_taxa":n,
      "n_UV_pattern_present_from_0":code[0],
      "n_uniform_UV_absorbing_from_1":code[1],
      "original_source_code_0_means_pattern_PRESENT":True,
      "original_source_code_1_means_uniform_ABSORBING":True,
      "two_decimal_UVP_vs_author_category_threshold_discrepancy_count":len(mismatches),
      "two_decimal_UVP_vs_author_category_threshold_discrepancies":mismatches,
      "original_author_category_not_overwritten_by_rounded_UVP":True,
      "visible_flower_color_counts":dict(sorted(colors.items())),
      "original_taxon_code_prefix_counts":dict(sorted(gen.items())),
      "species_source_level_climate_UVB_and_latitude_in_same_rows":True,
      "no_unverified_genus_expansions_or_invented_synonyms":True,
      "n_original_PDF_linewrapped_taxon_codes_reassembled":sum(
          r["original_taxon_code_split_across_source_PDF_lines"] for r in rows),
      "source_taxon_code_not_yet_verified_full_accepted_binomial":True,
      "no_inference_of_Bombus_visual_information_use":True,
      "no_new_UV_pattern_Bombus_geographic_regression":True,
    }

def main():
    import fitz
    zipbytes,_=_fetch(API)
    observed_zip_sha=hashlib.sha256(zipbytes).hexdigest()
    # Europe PMC can repackage ZIP metadata; original embedded PDF SHA
    # is the immutable source authentication, validated below.
    with zipfile.ZipFile(io.BytesIO(zipbytes)) as z:
        originals=[x for x in z.namelist() if x==MEMBER]
        if len(originals)!=1:
            raise ValueError("NO_GO_ORIGINAL_TABLE_S2_PDF_NOT_PRESENT")
        pdfbytes=z.read(MEMBER)
    if hashlib.sha256(pdfbytes).hexdigest()!=ORIGINAL_TABLE_PDF_SHA256:
        raise ValueError("NO_GO_TABLE_S2_PDF_SHA_CHANGED")
    with fitz.open(stream=pdfbytes,filetype="pdf") as pdf:
        if len(pdf)!=23:
            raise ValueError("NO_GO_2016_SUPPLEMENT_PAGES_CHANGED")
        texts={i:pdf[i].get_text("text") for i in PAGES}
    rows=parse_source_rows(texts)
    summary=summarize(rows)
    summary["original_suppl_container_sha256_observed"]=observed_zip_sha
    summary["zip_container_sha256_may_change_without_PDF_source_drift"]=True
    summary["original_TableS2_pdf_sha256"]=ORIGINAL_TABLE_PDF_SHA256
    dest=Path("stage49_2016_uv_pattern_177")
    dest.mkdir(exist_ok=True)
    with (dest/"koski_ashman2016_177_source_codes_uvp_climate.csv").open(
        "w",encoding="utf8",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=list(rows[0]))
        wr.writeheader()
        wr.writerows(rows)
    (dest/"source_177_UV_binary_source_receipt.json").write_text(
        json.dumps(summary,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf8")
    print("STAGE49_ORIGINAL_2016_177_UV_PATTERN_REAL_DATA",
          json.dumps(summary,sort_keys=True,ensure_ascii=False))
    print("STAGE49_SOURCE_177_FIRST_12_TAXON_CODES",
          json.dumps([r["original_taxon_code"] for r in rows[:12]]))
    print("NO_BOMBUS_UV_EFFECT_OR_GBIF_NAME_MATCH_ASSUMED")

if __name__=="__main__":
    main()
