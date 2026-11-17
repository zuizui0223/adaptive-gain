"""Stage57 original 2025 UV-reflectance/hue/bee-bird species table × prior 583 atlas.

Oliveira et al. 2025 DOI 10.1111/plb.70138 author original Table S1
PLB-28-201-s001.docx, located in EuropePMC PMC12710832 OA ZIP.
Source independently authenticated in previous Stage57 original workflow:
  246 rows = 1 header + 245 published species entries, 11 columns.
  Exact source ZIP and inner DOCX SHA256 pinned below.
The source field 'UV reflection' is an average spectral proportion, NOT
petal UV spatial pattern, nectar-guide presence, or flower visual fitness.
The source 'PS' is literature-described primary pollination system, not
actual Bombus occurrence at a phenotyped source site.

Strict GBIF accepted species identity (exact, confidence >=95, Plantae)
joins the former source-accepted 583 distinct botanical names. Unresolved
names never add estimated accepted species, and aliases/collisions deduped.
No "245 additional species" until overlap counted. No causal SEM.
"""
from __future__ import annotations

from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import argparse,csv,hashlib,io,json,re,sys,urllib.request,zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"floral_visual_macro_stage49"))
from match_literature_visual_taxa_gbif import lookup

DOI="10.1111/plb.70138"
PMC="PMC12710832"
OA_URL=f"https://www.ebi.ac.uk/europepmc/webservices/rest/{PMC}/supplementaryFiles"
MEMBER="PLB-28-201-s001.docx"
PIN_ZIP_SHA="6145ee8fe69ff57c8c53cb9bed61ae71400a38db519fc8c0ea3486b39e007a3b"
PIN_DOCX_SHA="0d0c1019c91802fab0372b1ff7c04c845126d0d2b30395bc1525baf47b1e764b"
MAX_DATA=17_000_000
NS="{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
REQUIRED_HEADERS=("Species","Genus","Family","S","Area","VG","PS","Hue","UV reflection")
BINOMIAL=re.compile(r"^[A-Z][a-zA-Z-]+ [a-z][a-z-]+$")

def read_original_member():
    req=urllib.request.Request(OA_URL,headers={
       "Accept":"application/zip",
       "User-Agent":"adaptive-gain-stage57-Oliveira-245-primary-OA-numeric-UV-BeeBird/2026"})
    with urllib.request.urlopen(req,timeout=70) as res:
        archive=res.read(MAX_DATA+1)
    if len(archive)>MAX_DATA or hashlib.sha256(archive).hexdigest()!=PIN_ZIP_SHA:
        raise ValueError("NO_GO_2025_245_ORIGINAL_EUROPE_PMC_ARCHIVE_DIGEST")
    with zipfile.ZipFile(io.BytesIO(archive)) as z:
        found=[x for x in z.infolist() if Path(x.filename).name==MEMBER and not x.is_dir()]
        if len(found)!=1 or found[0].file_size>180_000:
            raise ValueError("NO_GO_SOURCE_245_ORIGINAL_PRIMARY_TABLE_NOT_UNIQUE")
        doc=z.read(found[0])
    if hashlib.sha256(doc).hexdigest()!=PIN_DOCX_SHA:
        raise ValueError("NO_GO_SOURCE_245_ORIGINAL_DOCX_DIGEST_CHANGED")
    return doc

def table_cells(doc):
    with zipfile.ZipFile(io.BytesIO(doc)) as z:
        if "word/document.xml" not in z.namelist():
            raise ValueError("NO_GO_NOT_WILEY_OA_PRIMARY_DOCX")
        root=ET.fromstring(z.read("word/document.xml"))
    tbls=list(root.iter(NS+"tbl"))
    if len(tbls)!=8:
        raise ValueError("NO_GO_2025_ORIGINAL_SOURCE_TABLES_CHANGED")
    table=tbls[0]
    rows=[]
    for tr in table.findall(NS+"tr"):
        cells=[]
        for cell in tr.findall(NS+"tc"):
            # Word text runs may be split arbitrarily. Never use XML itertext
            # which also includes non-visible field/control metadata.
            cells.append(" ".join("".join((e.text or "") for e in cell.iter(NS+"t")).split()))
        rows.append(cells)
    return rows

def source_entries(rawrows):
    if len(rawrows)!=246 or len(rawrows[0])!=11 or tuple(rawrows[0][:9])!=REQUIRED_HEADERS:
        raise ValueError("NO_GO_ORIGINAL_245_TABLE_S1_SOURCE_HEADERS_OR_ROW_COUNT")
    out=[]
    for i,r in enumerate(rawrows[1:],1):
        if len(r)!=11:raise ValueError("NO_GO_ORIGINAL_245_STUDY_ROW_COLUMNS")
        full=r[0].strip()
        words=full.split()
        cand=" ".join(words[:2]) if len(words)>=2 else ""
        exact=bool(BINOMIAL.fullmatch(cand) and cand.split()[0].casefold()==r[1].strip().casefold())
        raw=r[8].strip()
        try:uv=float(raw)
        except ValueError: uv=None
        if uv is not None and not 0<=uv<=1:
            raise ValueError("NO_GO_ORIGINAL_UV_REFLECTANCE_OUT_OF_RANGE")
        out.append({
           "source_study_DOI":DOI,
           "source_original_docx_tableS1_row_1_based":i+1,
           "source_original_species_with_authority":full,
           "source_canonical_binomial_if_lexically_exact":cand if exact else "",
           "source_genus_literal":r[1],
           "source_family_literal":r[2],
           "source_attractant_structure_literal":r[3],
           "source_geographic_area_category_literal":r[4],
           "source_visitor_group_literal":r[5],
           "source_pollination_system_literal":r[6],
           "source_colour_hue_category_literal":r[7],
           "source_average_UV_reflection_proportion_or_unknown":uv,
           "source_reference_identifier_literal":r[9],
           "source_final_metadata_column":r[10][:120],
           "original_average_UV_reflectance_is_not_spatial_UV_pattern":True,
           "original_PS_is_not_verified_actual_pollinator_visits":True,
           "original_source_site_GPS_undetermined":True,
        })
    if len(out)!=245:raise ValueError("NO_GO_2025_TABLE_245_SPECIES_NOT_RETRIEVED")
    return out

def attach_taxonomy_and_prior(source,matched,prior):
    if len(prior)!=583:raise ValueError("NO_GO_ORIGINAL_PRIOR_MULTIMODAL_583_ACCEPTED_FRAME")
    accepted={r["gbif_accepted_species_key"] for r in prior}
    if len(accepted)!=583 or not all(str(k).isdigit() for k in accepted):
        raise ValueError("NO_GO_PRIOR_583_ACCEPTED_KEY_DUPLICATE")
    output=[]
    for r in source:
        orig=r["source_canonical_binomial_if_lexically_exact"]
        tax=matched.get(orig,{"taxonomy_status":"SOURCE_TAXON_NOT_LEXICAL_BINOMIAL"})
        key=tax.get("gbif_accepted_usage_key")
        key=str(key) if isinstance(key,int) and key>0 else ""
        output.append({
            **r,
            "GBIF_strict_match_status":tax["taxonomy_status"],
            "GBIF_accepted_species_key_or_unknown":key,
            "already_present_in_prior_source_atlas_583":key in accepted if key else "",
            "source_flower_UV_pattern_spatial_trait":"NOT_CLASSIFIED_FROM_MEAN_UV_REFLECTION",
            "colour_change_bee_perceptibility":"NOT_MEASURED_IN_THIS_SOURCE",
            "no_site_specific_native_Bombus_guild":"NOT_MEASURED",
        })
    unique={x["GBIF_accepted_species_key_or_unknown"] for x in output if
            x["GBIF_strict_match_status"]=="EXACT_CONFIDENT_SPECIES_MAPPED"}
    if "" in unique:raise ValueError("NO_GO_EMPTY_CONFIDENT_GBIF_ACCEPTED")
    overlaps=unique&accepted
    status_counts=dict(sorted(Counter(x["GBIF_strict_match_status"] for x in output).items()))
    return output,{
       "status":"ORIGINAL_2025_OLIVEIRA_245_MEASURED_UV_MEAN_AND_BEE_BIRD_GUILD_ACCEPTED_SPECIES_CROSSWALK",
       "source_245_original_Wiley_PMC_docx_rows":len(output),
       "source_original_OA_docx_SHA256":PIN_DOCX_SHA,
       "n_original_source_binomial_candidates":sum(bool(x["source_canonical_binomial_if_lexically_exact"]) for x in output),
       "n_original_source_numeric_average_UV_reflectance":sum(x["source_average_UV_reflection_proportion_or_unknown"] is not None for x in output),
       "original_source_primary_pollinator_class_counts":dict(sorted(Counter(x["source_pollination_system_literal"] for x in output).items())),
       "source_uv_numeric_not_receptor_spatial_contrast":True,
       "GBIF_query_name_count":len(matched),
       "GBIF_taxonomy_status_counts":status_counts,
       "n_exact_confident_accepted_source_rows":sum(x["GBIF_strict_match_status"]=="EXACT_CONFIDENT_SPECIES_MAPPED" for x in output),
       "n_distinct_GBIF_accepted_species_in_2025_reflectance_source":len(unique),
       "n_source_2025_overlap_prior_accepted_583":len(overlaps),
       "n_source_2025_new_accepted_not_in_prior_583":len(unique-accepted),
       "n_combined_prior_and_2025_unique_accepted":len(accepted|unique),
       "not_245_new_species_until_original_GBIF_key_deduplication":True,
       "source_2025_PS_not_actual_Bombus_receptor_behaviour":True,
       "no_UV_spatial_pattern_or_native_guild_causal_or_SEM_claim":True,
       "no_confounded_2025_region_guild_effect_fitted":True,
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source-prior-583-accepted",required=True)
    args=ap.parse_args()
    doc=read_original_member()
    source=source_entries(table_cells(doc))
    with Path(args.source_prior_583_accepted).open(encoding="utf8",newline="") as fp:
        prior=list(csv.DictReader(fp))
    candidates=sorted({r["source_canonical_binomial_if_lexically_exact"] for r in source
                       if r["source_canonical_binomial_if_lexically_exact"]})
    with ThreadPoolExecutor(max_workers=4) as pool:
        values=list(pool.map(lookup,candidates))
    matched=dict(zip(candidates,values))
    combined,receipt=attach_taxonomy_and_prior(source,matched,prior)
    out=Path("stage57_2025_original_245_uv_BeeBird_accepted_species")
    out.mkdir(exist_ok=True)
    with (out/"Oliveira2025_original_245_species_UVreflectance_guild_GBIF_prior583.csv").open(
         "w",encoding="utf8",newline="") as fp:
        safe=[{k:(v if v is not None else "") for k,v in q.items()} for q in combined]
        writer=csv.DictWriter(fp,fieldnames=list(safe[0]))
        writer.writeheader();writer.writerows(safe)
    (out/"2025_245_source_reflectance_guild_to_583_accepted_union_receipt.json").write_text(
        json.dumps(receipt,indent=2,ensure_ascii=False,sort_keys=True)+"\n",encoding="utf8")
    print("STAGE57_OLIVEIRA_REAL_245_UV_BEE_BIRD_GBIF_ACCEPTED_FRAME",
          json.dumps(receipt,sort_keys=True,ensure_ascii=False))
    print("NO_VISUAL_GUIDE_OR_BOMBUS_CAUSAL_EFFECT_FROM_MEAN_REFLECTANCE")
if __name__=="__main__":
    main()
