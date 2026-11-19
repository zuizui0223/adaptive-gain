"""Stage89C: independent database *label* concordance in exact species.

Two separately author-verified source botanically recorded modes:
 GIFT v3.2 public 2026 API source derived in island H5c, exact species
  GIFT source artifact 10332810251 SHA074a...
 AusTraits v7.0.0 official 21,100,078-byte author 1,798,215 raw traits
  13,440 pollen_syndrome source records, subset raw "insect"/"wind"
  original archive SHA2995fb...

Ecological labels may share reference floras between databases; nominal
source-database agreement is NOT two independent field surveys, nor a
phylogenetic history of evolutionary trait transitions. Exact same-name
species binomials only; no family imputation or transform of "mixed" to
an invented binary value. No source plant phenotypes/GBIF joins here.
"""
from __future__ import annotations
import argparse,hashlib,json,sys,tempfile,zipfile
from pathlib import Path
from collections import Counter,defaultdict
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"floral_macro_stage88"))
from original_austraits_v7_insect_wind_global_native_coverage import (
    download_real_austraits,pollination_source,ARCHIVE_SHA
)
from gift32_independent_pollen_mode_global_native_coverage import (
    original_gift_species,SOURCE_ARTIFACT_SHA
)

def safe_kappa(gift,aus,ids):
    n=len(ids)
    if n==0:return None
    agree=sum(gift[s]==aus[s] for s in ids)/n
    a=sum(gift[s]=="animal" for s in ids)/n
    b=sum(aus[s]=="animal" for s in ids)/n
    expected=a*b+(1-a)*(1-b)
    return (agree-expected)/(1-expected) if expected<1-1e-12 else None

def source_cross(gift,aus,au_source,bootstrap=2000):
    allids=sorted(set(gift)&set(aus))
    counts=Counter((gift[s],aus[s]) for s in allids)
    agree=sum(a==b for a,b in [tuple((gift[s],aus[s])) for s in allids])
    genera=defaultdict(list)
    for s in allids:genera[s.split()[0]].append(s)
    genus_keys=sorted(genera)
    rng=np.random.default_rng(20261119)
    boots=[]
    for _ in range(bootstrap):
        chosen=rng.integers(0,len(genus_keys),size=len(genus_keys)) if genus_keys else []
        ids=[sp for i in chosen for sp in genera[genus_keys[i]]]
        if ids:boots.append(sum(gift[s]==aus[s] for s in ids)/len(ids))
    result={
       "source_distinct_GIFT_exact_species":len(gift),
       "source_distinct_AusTraits_exact_species":len(aus),
       "source_exact_name_overlap":len(allids),
       "source_exact_name_overlap_unique_genera":len(genera),
       "source_two_category_original_labels_cross_table":[
          {"GIFT_source_mode":g,"AusTraits_source_mode":a,"species":counts[(g,a)]}
          for g in ("animal","wind") for a in ("animal","wind")],
       "source_agreement_species_count":agree,
       "source_disagreement_species_count":len(allids)-agree,
       "source_agreement_fraction":agree/len(allids) if allids else None,
       "source_Cohens_kappa_descriptive":safe_kappa(gift,aus,allids),
       "source_genus_cluster_bootstrap_descriptive_concordance_95":[
          float(x) for x in np.quantile(boots,[.025,.975])] if boots else None,
       "source_discordant_taxon_names_and_AusTraits_source_datasets":[
          {"species":s,"GIFT":gift[s],"AusTraits":aus[s],
           "AusTraits_original_dataset_keys":au_source.get(s)}
          for s in allids if gift[s]!=aus[s]][:100],
       "source_GIFT_vs_AusTraits_may_share_original_literature":True,
       "source_agreement_not_independent_pollination_or_selection_replication":True,
       "source_phylogenetic_ancestry_not_adjusted":True,
       "source_absent_from_either_database_UNKNOWN_not_false_mode":True,
       "source_no_at_flower_wind_VOC_learning_or_landing":True
    }
    return result

def run(gift_zip,outdir):
    gift,gift_info=original_gift_species(gift_zip)
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/"austraits-7.0.0.zip"
        source=download_real_austraits(p)
        with zipfile.ZipFile(p) as z:
            aus,aus_origins,aus_qa=pollination_source(z)
    if source["original_SHA256"]!=ARCHIVE_SHA:
        raise ValueError("STAGE89C_REAL_AUSTRAITS_2025_7_0_SHA_CHANGED")
    result=source_cross(gift,aus,aus_origins)
    result["original_independently_validated_source_GIFT"]={
        "ZIP_sha256":SOURCE_ARTIFACT_SHA,**gift_info}
    result["original_source_AusTraits_v7"]={**source,
        "source_pollination_labels":aus_qa}
    outdir.mkdir(exist_ok=True,parents=True)
    (outdir/"stage89C_original_GIFT_vs_AusTraits_pollination_species_concordance.json").write_text(
        json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True)+"\n")
    print("STAGE89C_TRUE_SOURCE_GIFT_AUSTRAITS_MODE_CONCORDANCE",json.dumps({
       k:v for k,v in result.items() if k in (
         "source_exact_name_overlap","source_exact_name_overlap_unique_genera",
         "source_two_category_original_labels_cross_table",
         "source_agreement_fraction","source_genus_cluster_bootstrap_descriptive_concordance_95")},sort_keys=True))
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--original-GIFT-H5c-artifact-zip",type=Path,required=True)
    p.add_argument("--outdir",type=Path,required=True)
    a=p.parse_args();run(a.original_GIFT_H5c_artifact_zip,a.outdir)
if __name__=="__main__":main()
