#!/usr/bin/env python3
"""Source admission: measured/compiled floral rewards, not inferred from visits.
Keasar & Bodner 2025 DOI 10.1002/ajb2.70125, PMC12640470.
The paper already tests morphology/reward association. We require a different
question: incremental, condition-dependent reward prediction by signal groups.
No reward units or plant names inferred from arbitrary worksheet columns.
"""
import argparse,csv,hashlib,io,json,re,zipfile
from collections import Counter
from pathlib import Path
import openpyxl
import pandas as pd
SOURCE="https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12640470/supplementaryFiles"
MEMBERS={"morphology":"AJB2-112-e70125-s001.csv","nectar":"AJB2-112-e70125-s003.xlsx","pollen":"AJB2-112-e70125-s002.xlsx"}
ARCHIVES={
 "nhm":(14313209081,"efa944763aa5971f7642f063295436119c9cafae204325922e9979f3214d1d85","combined/original_NHM_text_traits_compact.csv"),
 "visits":(14316616619,"fd4b12ac1074833d08b2569004bd458dc212a5303ba635376a45d16ea9b2eec7","original_plant_network_year_observed_guilds_text_spectra.csv"),
 "voc":(14296278415,"9522821741ad3054345235f6a3711a709144cc86cc13c0cc6e06cd278b2f6552","original_VOC305_accepted_source_and_visual817_evidence_bridge.csv")}
NAME_HEADERS={"species","plant species","species name","plant species name","scientific name","taxon","taxon name","latin name","plant name","binomial","species latin name","species scientific name","full species name","name of species"}
BAD={"sp","spp","cf","aff","unknown","species","hybrid","unidentified","unresolved","indet"}
def canon(x):
    if not isinstance(x,str):return None
    x=" ".join(x.strip().lower().split())
    if not re.fullmatch(r"[a-z][a-z-]* [a-z][a-z-]*",x) or x.split()[1] in BAD:return None
    if x.split()[0] in {"species","genus","plant","unknown","scientific","latin"}:return None
    return x
def norm(x):
    return " ".join(re.sub(r"[^a-z0-9]+"," ",str(x or "").lower()).split())
def sha(x):return hashlib.sha256(x).hexdigest()
def load_archive(root,label):
    id,digest,member=ARCHIVES[label];p=root/f"github-actions-artifact-{id}.zip"
    raw=p.read_bytes()
    if sha(raw)!=digest:raise ValueError("existing source archive SHA changed: "+label)
    with zipfile.ZipFile(io.BytesIO(raw)) as z:return pd.read_csv(z.open(member),low_memory=False)
def members(path):
    with zipfile.ZipFile(path) as z:
        entries=z.namelist();out={}
        for label,want in MEMBERS.items():
            hits=[n for n in entries if Path(n).name.casefold()==want.casefold()]
            if len(hits)!=1:raise ValueError("article exact appendix member missing/ambiguous "+label+" "+repr(entries))
            out[label]=z.read(hits[0])
        return out
def tables(raw,typ):
    if typ=="morphology":
        # CSV dialect and encoding are inspected, not silently normalized.
        for enc in ("utf-8-sig","cp1252"):
            try:s=raw.decode(enc);break
            except UnicodeDecodeError:continue
        else:raise ValueError("unknown original CSV encoding")
        dialect=csv.Sniffer().sniff(s[:8192],delimiters=",;\t")
        return [("csv",list(csv.reader(io.StringIO(s),dialect)),{"encoding":enc,"delimiter":dialect.delimiter})]
    wb=openpyxl.load_workbook(io.BytesIO(raw),read_only=True,data_only=True)
    try:return [(s.title,list(s.values),{}) for s in wb.worksheets]
    finally:wb.close()
def inspect(rows):
    # Only explicitly named species columns are admissible. Genus-only,
    # inferred authorities, merged cells, arbitrary binomial-looking text
    # and synonym replacement are NOT used. Multiple candidate headers fail closed.
    candidates=[]
    for i,r in enumerate(rows[:12]):
        for j,v in enumerate(r):
            if norm(v) not in NAME_HEADERS:continue
            values=[canon(row[j]) for row in rows[i+1:] if len(row)>j]
            values=[v for v in values if v]
            if len(values)>=5:candidates.append((i,j,values))
    out={"rows":len(rows),"first_nonempty_rows":[[str(v or "")[:160] for v in r[:35]] for r in rows[:8]],
         "name_header_candidates":[{"header_row":i+1,"column":j+1,"header":str(rows[i][j]),"n_strict_names":len(vals),"n_unique":len(set(vals))} for i,j,vals in candidates]}
    if len(candidates)!=1:return out,None
    i,j,vals=candidates[0]
    out["selected_explicit_species_header"]={"row":i+1,"column":j+1,"header":str(rows[i][j])}
    out["source_headers"]=[str(v or "") for v in rows[i]]
    out["n_strict_names"]=len(vals);out["n_unique_strict_names"]=len(set(vals))
    # No numeric reward value is yet admitted: physical-unit and source
    # duplicate/cultivar/zero semantics require independent explicit schema review.
    return out,set(vals)
def run(a,b,root):
    one=members(a);two=members(b)
    if any(one[k]!=two[k] for k in MEMBERS):raise ValueError("original appendix bytes differ between two retrievals")
    n=load_archive(root,"nhm");e=load_archive(root,"visits");v=load_archive(root,"voc")
    if len(n)!=59369 or len(e)!=18798:raise ValueError("existing source cohort changed")
    N=set(n.taxon.map(canon).dropna());E=set(e.Original_plant_accepted_name_literal.map(canon).dropna())
    V=set(v.source_species_canonical_binomial_if_valid.map(canon).dropna())
    P=set(e.loc[e.Stage67_direct_petal_spectra_name_match.eq(1),"Original_plant_accepted_name_literal"].map(canon).dropna())
    source_sets={"NHM_strict_literal":N,"EuPP_strict_literal":E,"VOC_strict_literal":V,"EuPP_with_direct_petal_spectrum":P}
    if (len(E),len(V),len(E&V),len(P),len(P&V))!=(1395,298,48,36,1):raise ValueError("strict archive overlap changed")
    info={"source_article":"10.1002/ajb2.70125","source_zenodo_doi":"10.5281/zenodo.17157828",
          "source_endpoint":SOURCE,"original_outer_archive_sha":[sha(a.read_bytes()),sha(b.read_bytes())],
          "two_retrievals_member_bytes_equal":True,"existing_source_sizes":{k:len(v) for k,v in source_sets.items()},
          "existing_EuPP_VOC_overlap":len(E&V),"existing_EuPP_petal_VOC_overlap":len(P&V),
          "original_appendices":{},"exact_literal_source_co_support":{},"no_claim_of_actual_reward_measurement_at_visit_site":True,
          "no_numeric_reward_model_before_unit_and_duplicate_review":True,"no_holdout_region_outcomes":True}
    sets={}
    for label,data in one.items():
        sheets=[]
        for sheet,rows,meta in tables(data,label):
            audit,s=inspect(rows);sheets.append({"sheet":sheet,**meta,**audit})
            if s is not None:
                sets.setdefault(label,[]).append(s)
        info["original_appendices"][label]={"member":MEMBERS[label],"sha256":sha(data),"bytes":len(data),"sheets":sheets}
    admitted={}
    for label,ss in sets.items():
        if len(ss)!=1:continue
        s=ss[0];admitted[label]=s
        info["exact_literal_source_co_support"][label]={"strict_names":len(s),**{k:len(s&v) for k,v in source_sets.items()},
             "with_EuPP_and_VOC":len(s&E&V),"with_EuPP_and_petal_spectrum":len(s&E&P),"with_EuPP_and_both_sensory_sources":len(s&E&P&V)}
    if "nectar" in admitted and "pollen" in admitted:
        s=admitted["nectar"]&admitted["pollen"]
        info["exact_literal_source_co_support"]["both_rewards"]={"strict_names":len(s),"with_EuPP":len(s&E),"with_VOC":len(s&V)}
    info["all_three_source_name_columns_unambiguous"]=len(admitted)==3
    # No raw appendix reproduction; only schema, digest, derived coverage.
    return info
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--first",type=Path,required=True);p.add_argument("--second",type=Path,required=True);p.add_argument("--archives",type=Path,required=True);p.add_argument("--out",type=Path,required=True);a=p.parse_args()
    info=run(a.first,a.second,a.archives)
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(info,indent=2,sort_keys=True,ensure_ascii=False)+"\n")
    print("STAGE118_REWARD_SOURCE_SCHEMA_AND_COSUPPORT",json.dumps(info,ensure_ascii=False,sort_keys=True))
