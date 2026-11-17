"""Stage59: authenticate 305 original floral VOC source species and overlap 817 visual names.

Farré-Armengol et al. 2020, DOI 10.3389/fpls.2020.01154, primary
source supplementary original DataSheet_1.xlsx SHA256 pinned in Stage58.
Sheet has 4460 data rows but exactly 305 rows labelled Species; remaining
4155 spreadsheet rows ARE NOT additional floral specimens/species.
Source "wind" column is WIND POLLINATION MODE, not atmospheric wind speed.

Use minimal OOXML parsing (stdlib zip/xml) of authentic Excel to avoid
altering source or presuming empty VOC cells are measured absence.
Accepted species key: strict live GBIF EXACT confidence>=95 Plantae match.
Visual 817 source IDs are from independent Stage57 original CI; a name
intersection is not joint locality, simultaneous flower emission, actual
pollinator sensory use, wind manipulation, or causal selection.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,re,sys,zipfile,urllib.error
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"floral_visual_macro_stage49"))
sys.path.insert(0,str(ROOT/"floral_routeability_stage58"))
from match_literature_visual_taxa_gbif import lookup
from inspect_original_VOC305_workbooks import download_source, MEMBERS

NS_MAIN="{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
NS_REL="{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
SOURCE_NAME="DataSheet_1.xlsx"
EXPECTED_ROWS=4461
EXPECTED_NAMED=305
PRIOR_VISUAL_N=817
CANONICAL=re.compile(r"^[A-Z][a-zA-Z-]+ [a-z][a-z-]+$")
COL_RE=re.compile(r"[A-Z]+")
MIN_METACOLS=23

def colnum(cellref:str)->int:
    m=COL_RE.match(cellref)
    if not m: raise ValueError("NO_GO_ORIGINAL_XLSX_MISSING_CELL_REFERENCE")
    n=0
    for x in m.group():
        n=n*26+(ord(x)-64)
    return n-1

def shared_strings(z):
    if "xl/sharedStrings.xml" not in z.namelist():
        return []
    root=ET.fromstring(z.read("xl/sharedStrings.xml"))
    return ["".join((t.text or "") for t in entry.iter(NS_MAIN+"t"))
            for entry in root.iter(NS_MAIN+"si")]

def parse_xlsx_rows(xlsx:bytes):
    with zipfile.ZipFile(io.BytesIO(xlsx)) as z:
        if "xl/worksheets/sheet1.xml" not in z.namelist():
            raise ValueError("NO_GO_ORIGINAL_VOC_PRESENCE_FIRST_WORKSHEET_MISSING")
        lookup_strings=shared_strings(z)
        with z.open("xl/worksheets/sheet1.xml") as f:
            root=None
            for event,elem in ET.iterparse(f,events=("start","end")):
                if root is None and event=="start":
                    root=elem
                if event!="end" or elem.tag!=NS_MAIN+"row":
                    continue
                vals={}
                for cell in elem.findall(NS_MAIN+"c"):
                    n=colnum(cell.attrib.get("r",""))
                    typ=cell.attrib.get("t","")
                    value=cell.find(NS_MAIN+"v")
                    if typ=="s":
                        if value is None or not (value.text or "").isdigit():
                            raise ValueError("NO_GO_ORIGINAL_VOC_BAD_SHARED_STRING_REF")
                        idx=int(value.text)
                        if idx>=len(lookup_strings):
                            raise ValueError("NO_GO_ORIGINAL_VOC_SHARED_STRING_OOB")
                        x=lookup_strings[idx]
                    elif typ=="inlineStr":
                        x="".join((q.text or "") for q in cell.iter(NS_MAIN+"t"))
                    elif value is not None:
                        x=value.text or ""
                    else:
                        x=""
                    if x!="":
                        vals[n]=x
                yield int(elem.attrib.get("r","0")),vals
                if root is not None:
                    root.clear()

def source_binomial(raw):
    tokens=" ".join(str(raw).split()).split()
    if len(tokens)<2:return ""
    cand=" ".join(tokens[:2])
    return cand if CANONICAL.fullmatch(cand) else ""

def verify_and_extract(sheetbytes:bytes,expected_named=EXPECTED_NAMED,
                       expected_rows=EXPECTED_ROWS):
    header=None
    species=[]
    n_xml_rows=0
    seen=set()
    n_chemical_headers=0
    pollination_modes=("wind","animal","insect","lepidoptera",
                       "coleoptera","diptera","hymenoptera","bat","bird")
    for row_index,vals in parse_xlsx_rows(sheetbytes):
        n_xml_rows+=1
        if row_index==1:
            header=vals
            required=("Source article","Species","APG III synonims","wind")
            if tuple(vals.get(i) for i in range(4))!=required:
                raise ValueError("NO_GO_ORIGINAL_VOC305_HEADER_POLLINATION_MODE_CHANGED")
            if vals.get(12)!="Annual Mean Temperature (K)":
                raise ValueError("NO_GO_VOC_SOURCE_CLIMATE_UNITS_CHANGED")
            n_chemical_headers=sum(
                bool(v) for k,v in vals.items() if k>=MIN_METACOLS)
            if n_chemical_headers<800:
                raise ValueError("NO_GO_ORIGINAL_VOC_COMPOUND_SCHEMA_TOO_SMALL")
            continue
        label=vals.get(1,"").strip()
        if not label:
            continue
        if label in seen:
            raise ValueError("NO_GO_DUPLICATED_ORIGINAL_VOC_SPECIES_LABEL")
        seen.add(label)
        if header is None:
            raise ValueError("NO_GO_NO_ORIGINAL_VOC_HEADER")
        source_id=vals.get(0,"").strip()
        original_name=source_binomial(label)
        compound_cols=[c for c in vals if c>=MIN_METACOLS and header.get(c)]
        recorded_positive=0
        recorded_explicit_zero=0
        unexpected_numeric=set()
        for c in compound_cols:
            text=str(vals[c]).strip()
            try: number=float(text)
            except ValueError:
                unexpected_numeric.add(text[:40]);continue
            if number==1:recorded_positive+=1
            elif number==0:recorded_explicit_zero+=1
            else:unexpected_numeric.add(text[:40])
        details={
          "source_original_author_species_name":label,
          "source_species_canonical_binomial_if_valid":original_name,
          "source_original_APGIII_synonym_as_printed":vals.get(2,""),
          "source_article_abbrev":source_id[:150],
          "original_source_row_number":row_index,
          "source_wind_pollination_flag_yes_if_1_else_unknown":
             "1" if vals.get(3)=="1" else "",
          "source_hymenoptera_pollination_flag_yes_if_1_else_unknown":
             "1" if vals.get(9)=="1" else "",
          "source_lepidoptera_pollination_flag_yes_if_1_else_unknown":
             "1" if vals.get(6)=="1" else "",
          "source_bird_pollination_flag_yes_if_1_else_unknown":
             "1" if vals.get(11)=="1" else "",
          "source_annual_mean_temperature_K_or_missing":vals.get(12,""),
          "source_annual_precipitation_L_m2_or_missing":vals.get(15,""),
          "source_VOC_positive_presence_columns_in_original_full_bouquet":
             recorded_positive,
          "source_VOC_explicit_numeric_zero_columns":recorded_explicit_zero,
          "source_VOC_nonbinary_numeric_examples":json.dumps(sorted(unexpected_numeric)[:12]),
          "source_VOC_profile_has_any_explicit_positive_cell":recorded_positive>0,
          "no_positive_VOC_cells_not_observed_scentlessness":True,
          "original_VOC_column_names_chemical_identification_not_validated":True,
          "wind_flag_is_wind_pollination_NOT_atmospheric_wind":True,
          "source_missing_VOC_not_scentless":True,
          "source_original_DOI":"10.3389/fpls.2020.01154",
        }
        species.append(details)
    if len(species)!=expected_named:
        raise ValueError("NO_GO_ORIGINAL_VOC305_NAMED_SOURCE_SPECIES_CHANGED")
    if n_xml_rows!=expected_rows:
        raise ValueError("NO_GO_ORIGINAL_VOC305_SOURCE_XLSX_ROW_COUNT_CHANGED")
    return species,{
       "status":"AUTHENTIC_ORIGINAL_2020_VOC305_SOURCE_SPECIES_EXTRACTED",
       "original_xlsx_source_data_rows":n_xml_rows-1,
       "n_source_named_distinct_species_records":len(species),
       "n_original_source_non_species_rows":n_xml_rows-1-len(species),
       "n_first_header_named_chemical_or_summary_columns":n_chemical_headers,
       "n_canonical_binomial_source_candidates":sum(bool(x["source_species_canonical_binomial_if_valid"]) for x in species),
       "n_original_source_wind_pollination_yes":sum(x["source_wind_pollination_flag_yes_if_1_else_unknown"]=="1" for x in species),
       "n_original_species_without_an_explicit_positive_VOC_cell":sum(not x["source_VOC_profile_has_any_explicit_positive_cell"] for x in species),
       "no_positive_VOC_cells_not_an_odor_absence_inference":True,
       "n_original_source_hymenoptera_pollination_yes":sum(x["source_hymenoptera_pollination_flag_yes_if_1_else_unknown"]=="1" for x in species),
       "n_original_source_bird_pollination_yes":sum(x["source_bird_pollination_flag_yes_if_1_else_unknown"]=="1" for x in species),
       "source_chemical_cell_numbers_are_source_columns_not_direct_receptor_behaviour":True,
       "no_original_wind_speed_m_per_s":True,
       "source_workbook_inner_sha256":MEMBERS[SOURCE_NAME],
    }

def original_presence_workbook():
    payload=download_source()
    with zipfile.ZipFile(io.BytesIO(payload)) as z:
        matches=[i for i in z.infolist()
                 if Path(i.filename).name==SOURCE_NAME and not i.is_dir()]
        if len(matches)!=1:raise ValueError("NO_GO_VOC_SOURCE_XLSX_IDENTIFICATION")
        raw=z.read(matches[0])
    if hashlib.sha256(raw).hexdigest()!=MEMBERS[SOURCE_NAME]:
        raise ValueError("NO_GO_VOC_SOURCE_XLSX_SHA_MISMATCH")
    return raw

def accepted_crosswalk(species,gbif,visual):
    if len(visual)!=PRIOR_VISUAL_N:
        raise ValueError("NO_GO_SOURCE_VISUAL_817_ACCEPTED_FRAME")
    prior={}
    for item in visual:
        key=item.get("gbif_accepted_species_key","")
        if not key.isdigit() or key in prior:
            raise ValueError("NO_GO_DUPLICATED_OR_UNKNOWN_VISUAL817_ACCEPTED_KEY")
        prior[key]=item
    unique=set()
    overlap=set()
    overlap_direct=set()
    overlap_mean=set()
    overlap_age=set()
    overlap_review=set()
    combined=[]
    by_source=Counter()
    for item in species:
        candidate=item["source_species_canonical_binomial_if_valid"]
        match=gbif.get(candidate,{"taxonomy_status":"SOURCE_NAME_NOT_LEXICAL_BINOMIAL"})
        key=match.get("gbif_accepted_usage_key")
        key=str(key) if isinstance(key,int) and key>0 else ""
        status=match.get("taxonomy_status","UNRESOLVED")
        if status=="EXACT_CONFIDENT_SPECIES_MAPPED" and key:
            unique.add(key)
            if key in prior:
                overlap.add(key)
                v=prior[key]
                if v["source_UV_pattern_directly_measured_or_unknown"] in ("0","1"):
                    overlap_direct.add(key)
                if v["original_Oliveira2025_UV_mean_source"]=="True":
                    overlap_mean.add(key)
                if v["original_Ohashi2015_spectral_taxon_source"]=="True":
                    overlap_age.add(key)
                if v["original_2025_literature_colour_change_reported"]=="True":
                    overlap_review.add(key)
        by_source[status]+=1
        combined.append({
          **item,
          "GBIF_strict_taxonomy_status":status,
          "GBIF_strict_accepted_species_key_or_unknown":key,
          "in_prior_817_visual_evidence_source_only":key in prior if key else "",
          "also_source_measured_UV_pattern_or_unknown":(
              prior[key]["source_UV_pattern_directly_measured_or_unknown"]
              if key in prior else ""),
          "also_source_Oliveira_UV_mean_available":(
              prior[key]["original_Oliveira2025_UV_mean_source"]
              if key in prior else ""),
          "source_same_population_VOC_visual_spectra_observed":False,
          "no_wind_scent_visual_causal_interaction":True,
        })
    return combined,{
       "status":"ORIGINAL_VOC305_2020_STRICT_GBIF_ACCEPTED_TO_817_VISUAL_SOURCE_CROSSWALK",
       "original_VOC_2020_source_named_species":len(species),
       "GBIF_status_source_rows":dict(sorted(by_source.items())),
       "n_distinct_strict_GBIF_accepted_VOC_species":len(unique),
       "n_source_VOC_accepted_also_in_visual817":len(overlap),
       "n_source_VOC_accepted_also_direct_measured_UV_spatial_230":len(overlap_direct),
       "n_source_VOC_accepted_also_UVmean_Oliveira_243":len(overlap_mean),
       "n_source_VOC_accepted_also_Ohashi_age_spectra_207":len(overlap_age),
       "n_source_VOC_accepted_also_reviewed_colourchange_124":len(overlap_review),
       "n_distinct_accepted_source_union_817_plus_VOC":len(set(prior)|unique),
       "original_visual817_without_VOC_source":len(set(prior)-unique),
       "not_same_original_observation_or_local_plant_individual":True,
       "source_no_actual_wind_airflow_field":True,
       "no_new_receiver_routeability_or_plant_fitness_coefficient":True,
       "unlisted_VOC_species_are_unknown_not_verified_scentless":True,
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--original-visual-817",required=True)
    args=ap.parse_args()
    source,quality=verify_and_extract(original_presence_workbook())
    with Path(args.original_visual_817).open(encoding="utf8",newline="") as f:
        visual=list(csv.DictReader(f))
    names=sorted({x["source_species_canonical_binomial_if_valid"] for x in source
                  if x["source_species_canonical_binomial_if_valid"]})
    with ThreadPoolExecutor(max_workers=5) as pool:
        response=list(pool.map(lookup,names))
    records,summary=accepted_crosswalk(source,dict(zip(names,response)),visual)
    summary["source_identity_qa"]=quality
    p=Path("stage59_original_VOC305_visual817_overlap")
    p.mkdir(exist_ok=True)
    with (p/"original_VOC305_accepted_source_and_visual817_evidence_bridge.csv").open(
        "w",encoding="utf8",newline="") as f:
        fieldnames=list(records[0])
        writer=csv.DictWriter(f,fieldnames=fieldnames)
        writer.writeheader();writer.writerows(records)
    (p/"VOC305_source_visual817_strict_accepted_overlap_receipt.json").write_text(
        json.dumps(summary,indent=2,ensure_ascii=False,sort_keys=True)+"\n",
        encoding="utf8")
    print("STAGE59_ORIGINAL_VOC305_VISUAL817_ACCEPTED_SOURCE_OVERLAP",
          json.dumps(summary,sort_keys=True,ensure_ascii=False))
    print("NO_ORIGINAL_GUILD_WIND_LOCALITY_OR_JOINT_SIGNAL_CAUSAL_FIT")

if __name__=="__main__":
    main()
