"""Stage79E original Rezende 2025 151 positive colour-change table species extraction.

Source original DOI 10.3390/plants14142185, Europe PMC original nested
PDF SHA256 0c2ba..., 23 pages. Extract botanical binomials from the author
Table S1 SPECIE column only (not references/habitat/color descriptions).
Some source epithets wrap onto a second line; tag source method. Review 151
published positives separately from parsed complete taxon count. Unreported
flower-age change is UNKNOWN, not negative.

Compare exact two-token Latin binomial source names to 1,408 genuine
EuPPPollNet corrected v1.3.0 accepted species. This is a literature-source
positive taxon, not evidence the field flowers visibly changed at visit time.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,re,subprocess,tempfile,urllib.request,zipfile
from pathlib import Path
from collections import Counter,defaultdict

URL="https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12299958/supplementaryFiles"
NESTED="plants-14-02185-s001.zip"
NESTED_SHA="a2af585bdc42cdc6e990c624c4328b808526e259bd21e0bd91fa39b5c316ff28"
PDF="plants-3703510-supplementary.pdf"
PDF_SHA="0c2ba82cd6eb554942fc3ac93014f7ecc9834686f695cf628f2873a2be213039"
VISIT_SHA="475863c2b193dd9c1eaad848dae05a9f518b57446cad2661979ca582c7d88617"
REGEX_BINOMIAL=re.compile(r"^\s{18,45}([A-Z][a-zA-Z-]+)\s+([a-z][a-zA-Z-]{2,})(?=\s|$)")
REGEX_GENUS_ONLY=re.compile(r"^\s{18,45}([A-Z][a-zA-Z-]{2,})(?=\s{7,}|$)")
REGEX_EPITHET_ONLY=re.compile(r"^\s{18,45}([a-z][a-zA-Z-]{2,})(?=\s|$)")
EXCLUDED_EPITHETS={"species","unidentified","undetermined","unknown","hybrid","variety"}
BAD_GENUS={"Plants","Family","Order","Taxon","Specie","Colour","Color","Pigment","Native","References",
           "Brazil","China","Australia","Mexico","Appendix","Supplementary","Figure"}

def original_pdf():
    request=urllib.request.Request(URL,headers={"User-Agent":"adaptive-gain-2025-original-flower-change-151-table/2026",
                                               "Accept":"application/zip"})
    with urllib.request.urlopen(request,timeout=90) as response:
        raw=response.read(3_000_000)
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        inner=z.read(NESTED)
    if hashlib.sha256(inner).hexdigest()!=NESTED_SHA:
        raise ValueError("STAGE79E_NESTED_AUTHOR_SUPP_SHA_CHANGED")
    with zipfile.ZipFile(io.BytesIO(inner)) as z:
        rawpdf=z.read(PDF)
    if hashlib.sha256(rawpdf).hexdigest()!=PDF_SHA:
        raise ValueError("STAGE79E_AUTHOR_REZENDE_SOURCE_PDF_SHA_CHANGED")
    return rawpdf

def pdf_lines(raw):
    with tempfile.TemporaryDirectory() as d:
        p=Path(d)/"original.pdf";p.write_bytes(raw)
        x=subprocess.run(["pdftotext","-layout",str(p),"-"],
                         capture_output=True,text=True,check=True)
    if len(x.stdout)<50000:
        raise ValueError("STAGE79E_ORIGINAL_PDF_TABLE_EMBEDDED_TEXT_NOT_COMPLETE")
    return x.stdout.splitlines()

def semantic_source_candidates(lines):
    active=False
    pending=None
    source=[]
    unresolved=[]
    for i,line in enumerate(lines,1):
        if "Supplementary Table S1." in line:
            active=True;pending=None
            continue
        if not active:continue
        if line.strip() in {"References","REFERENCES","References:"}:
            break
        if line.startswith("Plants 2025,"):
            pending=None
            continue
        if not line.strip():continue
        # Original Table S1 has order and family labels at smaller indentation
        # and the SPECIE column at approximately 22-28 leading spaces.
        same=REGEX_BINOMIAL.match(line)
        if same:
            genus,epithet=same.groups()
            pending=None
            if genus in BAD_GENUS or epithet.lower() in EXCLUDED_EPITHETS:
                unresolved.append({"source_line":i,"raw":line[:120],"reason":"NON_SPECIES_OR_HEADER"})
                continue
            source.append({"species":(genus+" "+epithet).casefold(),
                "source_pdf_line":i,"method":"species_column_same_line",
                "original_source_excerpt":line[:135]})
            continue
        # Source names like:
        # "   Epidendrum           White ..." + "   stamfordianum Bateman"
        # are split over consecutive lines by the original PDF table layout.
        if pending is not None:
            small=REGEX_EPITHET_ONLY.match(line)
            if small:
                ep=small.group(1)
                if ep.lower() not in EXCLUDED_EPITHETS:
                    source.append({"species":(pending[0]+" "+ep).casefold(),
                        "source_pdf_line":i,"method":"source_species_column_wrapped_epithet",
                        "original_source_excerpt":pending[2]+" | "+line[:100]})
                    pending=None
                    continue
            if not line.lstrip().startswith(("(","[","&","ex ","et ")):
                pending=None
        genus=REGEX_GENUS_ONLY.match(line)
        if genus:
            g=genus.group(1)
            if g not in BAD_GENUS and g[0].isupper():
                pending=(g,i,line[:120])
    result={}
    duplicates=Counter()
    for v in source:
        n=v["species"]
        duplicates[n]+=1
        if n not in result:result[n]=v
    return result,{
       "extracted_original_source_candidate_rows_in_table":len(source),
       "exact_two_token_source_candidate_species_names":len(result),
       "source_candidate_names_with_duplicate_rows":sum(v>1 for v in duplicates.values()),
       "source_unresolved_non_species_header_examples":unresolved[:25],
       "source_first60_positive_species_candidates":list(result)[:60],
       "source_last40_positive_species_candidates":list(result)[-40:],
       "published_151_positive_species_catalogue_NOT_measured_negative_states":True,
       "completeness_against_151_published_NOT_guaranteed":len(result)!=151,
    }

def original_visitor_names(path):
    b=Path(path).read_bytes()
    if hashlib.sha256(b).hexdigest()!=VISIT_SHA:
        raise ValueError("STAGE79E_ORIGINAL_1408_VISITING_PLANT_SOURCE_SHA_CHANGED")
    ro=list(csv.DictReader(io.StringIO(b.decode("utf-8"))))
    names={r["Original_plant_accepted_name_literal"].strip().casefold() for r in ro}
    if len(names)!=1408 or len(ro)!=18798:
        raise ValueError("STAGE79E_ORIGINAL_VISITING_PLANT_ROSTER_GRAIN_CHANGED")
    return ro,names

def join_names(candidates,visits):
    source=defaultdict(set)
    for r in visits:
        source[r["Original_plant_accepted_name_literal"].strip().casefold()].add(
           (r["Study_id"],r["Network_id"],r["Year_from_original_date"]))
    common=sorted(set(candidates)&set(source))
    networks=set().union(*(source[name] for name in common)) if common else set()
    return {"source_original_positive_FCC_exact_plant_species_in_1408_visit_roster":len(common),
            "source_original_positive_FCC_exact_plant_names":common,
            "original_distinct_visitation_networks_containing_positive_FCC_plant":len(networks),
            "original_distinct_study_IDs_containing_positive_FCC_plant":len({k[0] for k in networks}),
            "not_yet_within_network_two_phenotypically_measured_change_states":True,
            "all_other_1408_plant_names_change_state_UNOBSERVED_NOT_NEGATIVE":True}

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--source-original-visitor-plant-roster",type=Path,required=True)
    a.add_argument("--outdir",type=Path,required=True)
    q=a.parse_args();q.outdir.mkdir(exist_ok=True,parents=True)
    source=pdf_lines(original_pdf())
    candidates,diag=semantic_source_candidates(source)
    visitor,names=original_visitor_names(q.source_original_visitor_plant_roster)
    matched=join_names(candidates,visitor)
    report={"schema":"stage79e_original_rezende_2025_positive_fcc_table_vs_real_54study_visitor_plants",
            "source_original_PDF_SHA256":PDF_SHA,
            "source_original_published_positive_FCC_species":151,
            "source_original_species_table_parsing":diag,
            "source_exact_name_join_to_original_visit_roster":matched,
            "this_is_positive_source_literature_not_sampled_true_Negative":True,
            "no_invented_same_site_original_FCC_or_wind_gust_behavior":True,
            "real_guild_visual_interaction_effect_not_fitted":True}
    (q.outdir/"source_original_151_change_positive_rezende_EuPP_match.json").write_text(
       json.dumps(report,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("STAGE79E_SOURCE_ORIGINAL_REZENDE_POSITIVE_FCC_VISITING_PLANTS",
          json.dumps(report,sort_keys=True))
if __name__=="__main__":main()
