"""Stage77D: genuine 305-species floral VOC source tables × 233 visual plants.

2020 original Frontiers article: DOI 10.3389/fpls.2020.01154,
305 reported species, 66 families, 851 VOCs from 58 source studies.
EUROPE PMC original 24-member supplementary ZIP has three genuine XLSX
DataSheet_1/2/3. Its original bytes were independently SHA verified at
Stage77C (source byte SHA256 fixed here).

This inspects actually named plant taxa IN author original numeric worksheets,
not an article abstract or paper-reported sample size. It does not assume
documented species scent is invariant at the EuPPollNet field site/time,
or that source compiled pollinator syndrome is an independent direct visit.
Original floral scent meta-analysis already studied climate/pollinators.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,posixpath,re,urllib.request,xml.etree.ElementTree as ET,zipfile
from collections import Counter,defaultdict
from pathlib import Path

OA_SUPP="https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7412988/supplementaryFiles"
ZIP_SHA="44b9f0b8ee0a41be3958a18552e84afb518ecca57e34b573e4a7d800ae1dfb88"
ZIP_SIZE=8428937
XLSX={
 "DataSheet_1.xlsx":1582240,
 "DataSheet_2.xlsx":1023324,
 "DataSheet_3.xlsx":1542488,
}
SOURCE_NHM_SHA="b81ab96a2883e2b2e7f254a9e7ab62a34afaa0dfe62f0062d1677ba852dc686a"
SOURCE_EUPP_SHA="475863c2b193dd9c1eaad848dae05a9f518b57446cad2661979ca582c7d88617"
NS={"s":"http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r":"http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "p":"http://schemas.openxmlformats.org/package/2006/relationships"}
CELL=re.compile(r"^([A-Z]+)(\d+)$")
SOURCE_ARTICLE="10.3389/fpls.2020.01154"
SHEET_CANDIDATES=("species","taxon","plant species","plant name","floral species")
BINOMIAL=re.compile(r"^[A-Z][a-zA-Z-]+ [a-z][a-zA-Z-]+$")
NON_SPECIES_EPITHETS={"unidentified","unknown","unresolved","undetermined",
    "species","sp","spp","hybrid","indet","indeterminate","cf","aff"}


def source_binomial(value):
    text=str(value or "").strip()
    if not BINOMIAL.fullmatch(text):
        return False
    genus,epithet=text.split()
    return (genus.casefold() not in {"species","genus","unknown","unidentified"}
            and epithet.casefold() not in NON_SPECIES_EPITHETS)
SHEET_ROW_PREVIEW=6

def sha(b):
    return hashlib.sha256(b).hexdigest()

def load_source_zip():
    req=urllib.request.Request(OA_SUPP,headers={
       "User-Agent":"adaptive-gain-VOC-original-taxonomy-XLSX-audit/2026-11-18",
       "Accept":"application/zip"})
    with urllib.request.urlopen(req,timeout=75) as f:
        raw=f.read(ZIP_SIZE+1)
    # Europe PMC dynamically repackages a ZIP: the *outer* archive digest
    # can change because ZIP entry timestamps/order are not stable. This
    # is explicitly diagnosed, never silently treated as source-sheet change.
    current_sha=sha(raw)
    if not zipfile.is_zipfile(io.BytesIO(raw)):
        raise ValueError("STAGE77D_ORIGINAL_SUPPLEMENT_NOT_REAL_ZIP")
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        files=[x for x in z.infolist() if not x.is_dir()]
        if len(files)!=24:
            raise ValueError("STAGE77D_ORIGINAL_EUROPEPMC_24_SOURCE_MEMBERS_CHANGED")
        for path,size in XLSX.items():
            if path not in z.namelist() or z.getinfo(path).file_size!=size:
                raise ValueError("STAGE77D_ORIGINAL_AUTHOR_XLSX_CONTENT_SIZE_CHANGED_"+path)
    return raw,{
       "original_historical_retrieval_ZIP_SHA256":ZIP_SHA,
       "original_current_dynamic_ZIP_SHA256":current_sha,
       "historical_ZIP_8428937_bytes":ZIP_SIZE,
       "current_downloaded_original_ZIP_bytes":len(raw),
       "outer_source_ZIP_repackaged_sha_drift":current_sha!=ZIP_SHA,
       "actual_original_member_count":len(files),
       "original_3_source_XLSX_content_sizes_verified":True,
       "dynamic_ZIP_outer_digest_is_not_stable_XLSX_identity":True,
    }

def col_idx(cell_ref):
    m=CELL.fullmatch(cell_ref)
    if not m:raise ValueError("STAGE77D_INVALID_REAL_XLSX_CELL_REF")
    v=0
    for c in m.group(1):v=v*26+ord(c)-ord("A")+1
    return v-1

def text_from_cell(cell,shared):
    t=cell.get("t","")
    val=cell.find("s:v",NS)
    inline=cell.find("s:is",NS)
    raw=val.text or "" if val is not None else ""
    if t=="s" and raw:
        ix=int(raw)
        return shared[ix] if ix<len(shared) else ""
    if inline is not None:
        return "".join(x.text or "" for x in inline.findall(".//s:t",NS))
    return raw

def original_workbook(raw,name):
    if not zipfile.is_zipfile(io.BytesIO(raw)):
        raise ValueError("STAGE77D_ORIGINAL_AUTHOR_WORKBOOK_NOT_XLSX_"+name)
    with zipfile.ZipFile(io.BytesIO(raw)) as f:
        names=set(f.namelist())
        if "xl/workbook.xml" not in names:
            raise ValueError("STAGE77D_MISSING_AUTHOR_WORKBOOK_XML")
        wb=ET.fromstring(f.read("xl/workbook.xml"))
        sheets=wb.find("s:sheets",NS)
        shared=[]
        if "xl/sharedStrings.xml" in names:
            r=ET.fromstring(f.read("xl/sharedStrings.xml"))
            shared=["".join(x.text or "" for x in z.findall(".//s:t",NS))
                for z in r.findall("s:si",NS)]
        rel={}
        if "xl/_rels/workbook.xml.rels" in names:
            root=ET.fromstring(f.read("xl/_rels/workbook.xml.rels"))
            for x in root.findall("p:Relationship",NS):
                href=x.attrib["Target"].lstrip("/")
                if not href.startswith("xl/"):
                    href=posixpath.normpath("xl/"+href)
                rel[x.attrib["Id"]]=href
        records=[]
        candidate_names=set()
        for i,sheet in enumerate(sheets.findall("s:sheet",NS),start=1):
            sheetname=sheet.attrib.get("name",f"Sheet{i}")
            relationship=sheet.attrib.get("{"+NS["r"]+"}id","")
            dest=rel.get(relationship,f"xl/worksheets/sheet{i}.xml")
            if dest not in names:
                raise ValueError("STAGE77D_ORIGINAL_SHEET_TARGET_NOT_FOUND")
            root=ET.fromstring(f.read(dest))
            sd=root.find("s:sheetData",NS)
            rows=[]
            for row in sd.findall("s:row",NS) if sd is not None else []:
                values={}
                for cell in row.findall("s:c",NS):
                    name=cell.attrib.get("r","")
                    x=col_idx(name)
                    text=text_from_cell(cell,shared).strip()
                    if text:values[x]=text
                if values:rows.append((int(row.attrib.get("r","0")),values))
            first=[{
               "excel_row":num,
               "source_col1_value_dict":{str(k+1):v[:90] for k,v in sorted(cells.items())[:25]}
               } for num,cells in rows[:SHEET_ROW_PREVIEW]]
            # Only count actual species when FIRST row a verified semantic
            # species column. Never infer genotype or original species from
            # any two-word chemical name scattered through a table.
            found_cols={}
            for rownum,cells in rows[:5]:
                for c,val in cells.items():
                    if val.strip().casefold() in SHEET_CANDIDATES:
                        found_cols[(rownum,c)]=val
            for (headrow,col),label in found_cols.items():
                entries=set()
                for rownum,cells in rows:
                    if rownum<=headrow:continue
                    value=cells.get(col,"").strip()
                    if source_binomial(value):
                        entries.add(value.casefold())
                candidate_names|=entries
            records.append({
                "source_original_workbook":name,
                "source_sheet":sheetname,
                "source_nonempty_rows":len(rows),
                "source_max_nonempty_col_count":max(
                    (max(x)+1 for _,x in rows if x),default=0),
                "original_first6_record_rows":first,
                "semantic_exact_plant_species_header_evidence":[
                    {"row":r,"column_1indexed":c+1,"literal_label":t}
                    for (r,c),t in found_cols.items()],
                "source_original_candidate_explicit_taxa_in_semantic_species_columns":
                    len(entries) if found_cols else 0,
                "no_taxa_guessed_from_compound_or_pollinator_names":True,
            })
    return records,candidate_names

def original_targets(nhm,network):
    for p,expected in ((nhm,SOURCE_NHM_SHA),(network,SOURCE_EUPP_SHA)):
        if sha(p.read_bytes())!=expected:
            raise ValueError("STAGE77D_ORIGINAL_SOURCE_NHM_OR_EUPP_SHA_CHANGED")
    with network.open(encoding="utf-8",newline="") as f:
        eu={r["Original_plant_accepted_name_literal"].casefold().strip()
            for r in csv.DictReader(f)}
    if len(eu)!=1408:raise ValueError("STAGE77D_NOT_1408_ORIGINAL_EUPP_PLANTS")
    import sys
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"floral_macro_stage75"))
    from authentic_continental_text_signal_guild_macro import source_text_trait
    matched=set();hu=set()
    with nhm.open(encoding="utf-8",newline="") as f:
        for r in csv.DictReader(f):
            tax=r["taxon"].casefold().strip()
            if tax not in eu:continue
            matched.add(tax)
            if source_text_trait(r)["source_exclusive_lexical_hue"]:hu.add(tax)
    if len(matched)!=963 or len(hu)!=233:
        raise ValueError("STAGE77D_NOT_963_233_SOURCE_NHM_VS_EUPP_ACCEPTED")
    return eu,matched,hu

def direct_source_spectrometer_73(original_source):
    # Exact 2024 source-original measured 300-399nm reflectance species
    # crosswalk, archived independently in the authenticated Stage68 run.
    with Path(original_source).open(encoding="utf-8",newline="") as f:
        source=list(csv.DictReader(f))
    if len(source)!=73:
        raise ValueError("STAGE77D_ORIGINAL_73_SPECTROMETER_ROWS_CHANGED")
    names=[r["spectral_original_species_name"].casefold().strip() for r in source]
    if len(set(names))!=73 or any(not x for x in names):
        raise ValueError("STAGE77D_ORIGINAL_73_SPECTRA_DUPLICATE_OR_EMPTY")
    if not all("original_2024_true_petal_UV_300_399_percent" in x for x in source):
        raise ValueError("STAGE77D_SPECTRA_SOURCE_NO_DIRECT_UV")
    return set(names),sha(Path(original_source).read_bytes())


def run(nhm,eu,source_spectrometer=None):
    original,zip_source=load_source_zip()
    # A second authoritative HTTP retrieval validates actual XLSX content,
    # not the potentially repackaged outer ZIP timestamps or compression.
    second,second_outer=load_source_zip()
    with zipfile.ZipFile(io.BytesIO(second)) as z1,zipfile.ZipFile(io.BytesIO(original)) as z2:
        member_checks={
          name:{
            "original_sha256_download_1":sha(z2.read(name)),
            "original_sha256_download_2":sha(z1.read(name)),
            "original_content_identical_over_two_fresh_authoritative_fetches":
                sha(z2.read(name))==sha(z1.read(name)),
          } for name in XLSX
        }
        if not all(v["original_content_identical_over_two_fresh_authoritative_fetches"] for v in member_checks.values()):
            raise ValueError("STAGE77D_AUTHOR_ORIGINAL_XLSX_MEMBER_DRIFT_ACROSS_FRESH_FETCHES")
    workbooks=[]
    candidates=set()
    with zipfile.ZipFile(io.BytesIO(original)) as z:
        files=[x for x in z.infolist() if not x.is_dir()]
        if len(files)!=24:raise ValueError("STAGE77D_ORIGINAL_24_ARCHIVE_MEMBERS_CHANGED")
        for name,size in XLSX.items():
            b=z.read(name)
            if len(b)!=size:
                raise ValueError("STAGE77D_ORIGINAL_DATASHEET_BYTE_LENGTH_CHANGED_"+name)
            sheets,taxa=original_workbook(b,name)
            candidates|=taxa
            workbooks.append({
                "original_source_workbook":name,
                "source_original_xlsx_bytes":len(b),
                "source_original_xlsx_sha256":sha(b),
                "source_original_sheets":sheets,
                "explicit_binomial_species_found_in_verified_header_columns":len(taxa),
            })
    e,n,h=original_targets(nhm,eu)
    if source_spectrometer is None:
        spectra_diagnostic={
          "source_original_direct_2024_spectrometer_73_taxa_retrieved":False,
          "source_direct_2024_spectra_and_VOC_overlap_not_yet_evaluated":True,
        }
    else:
        sp,specsha=direct_source_spectrometer_73(source_spectrometer)
        if len(sp&e)!=36:
            raise ValueError("STAGE77D_ORIGINAL_36_REAL_SPECTRA_EUPP_VISITOR_TAXA_CHANGED")
        spectra_diagnostic={
          "source_original_direct_2024_spectrometer_73_taxa_retrieved":True,
          "source_original_direct_2024_spectrometer_file_SHA256":specsha,
          "source_original_direct_2024_spectrometer_species":len(sp),
          "source_direct_spectrometer_species_with_original_EuPP_visits":len(sp&e),
          "source_original_VOC_overlap_with_73_direct_spectrometer_species":len(candidates&sp),
          "source_original_VOC_overlap_with_direct_spectrometer_AND_EuPP":len(candidates&sp&e),
          "source_original_strict_spectrometer_VOC_EuPP_taxon_names":sorted(candidates&sp&e),
          "garden_spectrometer_VOC_compilation_and_field_visits_are_NOT_same_population":True,
          "no_false_three_modality_site_cotemporal_coincidence":True,
        }
    return {
       "schema":"stage77d_2020_multispecies_VOC_original_XLSX_readout_and_source_overlap",
       "source_original_review_DOI":SOURCE_ARTICLE,
       "source_original_supplement_PMCID":"PMC7412988",
       "original_historical_EuropePMC_dynamic_ZIP_SHA256":ZIP_SHA,
       "original_current_EuropePMC_ZIP_audit":zip_source,
       "original_second_download_ZIP_audit":second_outer,
       "original_author_source_XLSX_per_member_double_fetch_sha256":member_checks,
       "original_source_three_XLSX_workbooks":workbooks,
       "original_source_all_candidate_species_names_from_verified_XLSX_headers":len(candidates),
       "original_exact_EuPP_species_name_overlap_if_source_header_verified":len(candidates&e),
       "original_exact_NHM_EuPP_name_overlap_if_source_header_verified":len(candidates&n),
       "original_exact_233_VISUAL_HUE_species_source_VOC_overlap_if_header_verified":len(candidates&h),
       "original_measured_SPECTRAL_VISUAL_x_VOC_x_EuPP_crosssource":spectra_diagnostic,
       "source_species_first_two_tokens_without_authorship_are_NOT_autojoined":True,
       "source_2020_scent_dataset_cannot_prove_VOC_at_EuPP_field_site_time":True,
       "source_2020_scent_compilation_prior_studies_not_independent_flower_evolution":True,
       "VOC_scent_wind_Bombus_causal_mediation_fitted":False,
       "no_false_missing_scent_negative":True,
       "source_2020_original_305_66_851_sample_counts_not_assumed_from_files":True,
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source-NHM",type=Path,required=True)
    p.add_argument("--source-EuPP",type=Path,required=True)
    p.add_argument("--original-73-spectra",type=Path,required=False)
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args()
    result=run(a.source_NHM,a.source_EuPP,a.original_73_spectra)
    a.outdir.mkdir(exist_ok=True,parents=True)
    (a.outdir/"2020_original_3_VOC_XLSX_direct_species_crosswalk.json").write_text(
        json.dumps(result,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("STAGE77D_REAL_AUTHOR_2020_305_VOC_CHEMISTRY_SHEETS_SPECIES_MATCH",
          json.dumps(result,sort_keys=True,ensure_ascii=False))
    print("NO_FIELD_POPULATION_SCENT_BOMBUS_CAUSAL_LINK_INFERRED")
if __name__=="__main__":
    main()
