"""Independent source reconstruction of taxonomy-conditional lexical reports.
Only exploration region outcomes are joined. Baselines are descriptive, not
independent evolutionary origins, and unmentioned is NOT unmarked.
"""
import argparse,csv,json,sys
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np,pandas as pd
from regional_marking_bombus import frame,model_set,G,E,Y,Y2
BASE=Path(__file__).resolve().parents[1]
for folder in ["floral_macro_stage87","floral_macro_stage88","floral_macro_stage91"]:
    sys.path.insert(0,str(BASE/folder))
from global_native_floral_signal_tdwg3 import load_nhm,wcvp_regions,strict_name
from source_taxonomic_family_exclusion_native_flora import source_families
from real_three_cue_preflight import mark_state

def taxonomic_components(local,pool,mark,taxon,min_other=3):
    """Local documented taxa vs unique reference species with shared lineage.
    Descriptive inclusive baseline and strict disjoint-species reference.
    Unsupported local taxa are explicitly excluded from the latter.
    """
    total=Counter();pos=Counter();here=Counter();herepos=Counter()
    for sp in pool:
        t=taxon.get(sp)
        if t is None:continue
        total[t]+=1;pos[t]+=mark[sp]
    for sp in local:
        t=taxon.get(sp)
        if t is None:continue
        here[t]+=1;herepos[t]+=mark[sp]
    n=sum(here.values())
    if not n:return {}
    obs=sum(herepos.values())/n
    exp=sum(here[t]*pos[t]/total[t] for t in here)/n
    balanced=float(np.mean([herepos[t]/here[t] for t in here]))
    supported=[t for t in here if total[t]-here[t]>=min_other]
    n_supported=sum(here[t] for t in supported)
    if n_supported:
        obs_disjoint=sum(herepos[t] for t in supported)/n_supported
        exp_disjoint=sum(here[t]*(pos[t]-herepos[t])/(total[t]-here[t]) for t in supported)/n_supported
    else:obs_disjoint=exp_disjoint=None
    return {"observed":obs,"expected":exp,"residual":obs-exp,"balanced":balanced,
        "disjoint_observed":obs_disjoint,"disjoint_expected":exp_disjoint,
        "disjoint_residual":obs_disjoint-exp_disjoint if n_supported else None,
        "disjoint_support_fraction":n_supported/n,"documented_taxon_classified":n,
        "n_distinct_lineages":len(here),"classified_fraction":n/len(local) if local else None}

def run(root,nhm,wcvp):
    d=frame(root)
    traits,_=load_nhm(nhm)
    ranges,_=wcvp_regions(wcvp,traits)
    if len(ranges)!=367 or len(set().union(*ranges.values()))!=55775:
        raise ValueError("original global range scope changed")
    families,_=source_families(wcvp,traits)
    explore=set(d.TDWG_L3)
    if not explore<=set(ranges):raise ValueError("exploration region missing")
    ranges={k:ranges[k] for k in explore}
    pool=set().union(*ranges.values())
    states={}
    with nhm.open(encoding="utf-8-sig",newline="") as f:
        for row in csv.DictReader(f):
            sp=strict_name(row.get("taxon"))
            if sp in pool:states[sp]=mark_state(row)
    if set(states)!=pool:raise ValueError("source NHM coverage changed")
    doc={sp for sp in pool if states[sp]!="source_colour_missing"}
    mark={sp:int(states[sp]=="positive_lexical") for sp in doc}
    genus={sp:sp.split()[0] for sp in doc}
    family={sp:families[sp] for sp in doc if sp in families}
    rangefreq=Counter(sp for sps in ranges.values() for sp in sps)
    rows=[]
    for rec in d.to_dict("records"):
        code=rec["TDWG_L3"];local=ranges[code]&doc
        n=len(ranges[code]);k=sum(mark[sp] for sp in local)
        if n!=rec["source_n_original_native_species"] or not local or abs(len(local)/n-rec["NHM_colour_field_description_coverage"])>1e-12 or abs(k/n-rec[Y2])>1e-12 or abs(k/len(local)-rec[Y])>1e-12:
            raise ValueError("Stage114 original denominator mismatch "+code)
        row={"TDWG_L3":code,"n_colour_documented":len(local),"n_mark_positive":k}
        row["inverse_exploration_range_weighted_rate"]=sum(mark[s]/rangefreq[s] for s in local)/sum(1/rangefreq[s] for s in local)
        row["no_graminoid_rate"]=None
        sub={s for s in local if s in family and family[s] not in {"Poaceae","Cyperaceae","Juncaceae"}}
        if sub:row["no_graminoid_rate"]=sum(mark[s] for s in sub)/len(sub)
        for name,tax in [("genus",genus),("family",family)]:
            for key,val in taxonomic_components(local,doc,mark,tax).items():row[name+"_"+key]=val
        rows.append(row)
    merged=d.merge(pd.DataFrame(rows),on="TDWG_L3",validate="1:1")
    q=merged[merged[E]>=5].copy()
    analyses={}
    for tax in ["genus","family"]:
        for target in ["expected","residual","balanced"]:
            label=tax+"_"+target;analyses[label]=model_set(q,label)
        # Strictly exclude local species from the reference estimate; require
        # >=50% within-region documented species support in matched lineages.
        sub=q[q[tax+"_disjoint_support_fraction"]>=.5]
        for target in ["disjoint_observed","disjoint_expected","disjoint_residual"]:
            label=tax+"_"+target;analyses[label]=model_set(sub,label)
    for target in ["inverse_exploration_range_weighted_rate","no_graminoid_rate"]:
        analyses[target]=model_set(q,target)
    for tax in ["genus","family"]:
        analyses[tax+"_expected_as_control"]=model_set(q,Y,extra=[tax+"_expected"])
    return merged,{"exploration_regions":len(rows),"old72_original_source_counts_reproduced":len(rows),
        "unique_exploration_native_species":len(pool),"unique_exploration_colour_documented_species":len(doc),
        "unique_exploration_mark_positive":sum(mark.values()),
        "n_primary_bombus_regions":len(q),"primary_results":analyses,
        "taxon_support":{k:{"min":float(q[k+"_disjoint_support_fraction"].min()),"median":float(q[k+"_disjoint_support_fraction"].median()),"n_ge_half":int((q[k+"_disjoint_support_fraction"]>=.5).sum())} for k in ["genus","family"]},
        "NO_holdout_geographic_outcome_join":True,"NO_phylogenetic_independence_or_causal_claim":True,"unknown_marking_not_absence":True}

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--archives",type=Path,required=True);p.add_argument("--nhm",type=Path,required=True);p.add_argument("--wcvp",type=Path,required=True);p.add_argument("--outdir",type=Path,required=True);a=p.parse_args()
    m,r=run(a.archives,a.nhm,a.wcvp);a.outdir.mkdir(parents=True,exist_ok=True)
    m.to_csv(a.outdir/"stage116_72_exploration_source_taxonomy_frame.csv",index=False)
    (a.outdir/"stage116_source_taxonomy_diagnostics.json").write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
    print("STAGE116_SOURCE_TAXONOMY",json.dumps(r,sort_keys=True))
