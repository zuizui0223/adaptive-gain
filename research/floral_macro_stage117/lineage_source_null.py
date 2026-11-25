"""Stage117: common-scale lineage decomposition and conditional source-label null.
Positive NHM marking words versus other colour-documented species, NOT phenotype
presence versus absence. Species-level label shuffles retain exact range incidence,
documentation cohort and lineage totals; this is a conditional descriptive null,
not a causal or phylogenetic test. Never join the 37 geography holdout outcomes.
"""
import argparse,csv,hashlib,json,sys,zipfile
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np,pandas as pd
from scipy.stats import rankdata
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/"floral_macro_stage116"))
from regional_marking_bombus import W,B,E,G,Y,C
from taxonomy_marking import load_nhm,wcvp_regions,strict_name,source_families,mark_state

ARCHIVE_SHA="d9ceb43214cfe661e8cc23541362c8a4cf2b1181e36aa4db5313330b72a01cdd"
MEMBER="stage116_72_exploration_source_taxonomy_frame.csv"
def load(path):
    if hashlib.sha256(path.read_bytes()).hexdigest()!=ARCHIVE_SHA:
        raise ValueError("Stage116 original archive digest changed")
    with zipfile.ZipFile(path) as z:d=pd.read_csv(z.open(MEMBER))
    if len(d)!=72 or d[G].nunique()!=17 or d.TDWG_L3.nunique()!=72:
        raise ValueError("source geographic cohort drift")
    if not (d.genus_classified_fraction.eq(1)&d.family_classified_fraction.eq(1)).all():
        raise ValueError("not common family/genus species denominator")
    d["within_family_genus_composition"]=d.genus_expected-d.family_expected
    if not np.allclose(d[Y],d.family_expected+d.within_family_genus_composition+d.genus_residual,rtol=0,atol=1e-12):
        raise ValueError("exact hierarchical decomposition failed")
    return d.sort_values("TDWG_L3").reset_index(drop=True)

def zr(x):
    v=rankdata(x);return (v-v.mean())/v.std() if v.std()>0 else np.zeros(len(v))

def design(q,bee=False,interaction="none",blocks=True,wind=W):
    x=zr(q[wind]);arr=[np.ones(len(q)),x];names=["intercept","wind"]
    if bee:
        z=zr(q[B]);arr.append(z);names.append("Bombus")
        if interaction=="global":arr.append(x*z);names.append("interaction")
        elif interaction=="within":
            wx=x-pd.Series(x).groupby(q[G].to_numpy()).transform("mean").to_numpy()
            wz=z-pd.Series(z).groupby(q[G].to_numpy()).transform("mean").to_numpy()
            arr.append(wx*wz);names.append("interaction")
        elif interaction!="none":raise ValueError("unknown interaction")
    for key in C+([E] if bee else []):
        v=zr(q[key])
        if v.std()>0:arr.append(v);names.append(key)
    if blocks:
        arr.append(pd.get_dummies(q[G],drop_first=True).to_numpy(float))
    X=np.column_stack(arr)
    rank=np.linalg.matrix_rank(X)
    if rank!=X.shape[1] or len(q)-rank<5:raise ValueError("nonestimable source contrast")
    return X,names

def common_scale(q,bee=False,interaction="none",blocks=True,wind=W):
    X,names=design(q,bee,interaction,blocks,wind)
    cols=[Y,"family_expected","within_family_genus_composition","genus_residual","family_residual"]
    scale=q[Y].std(ddof=0)
    if not scale>0:raise ValueError("constant original outcome")
    coef=np.linalg.lstsq(X,q[cols].to_numpy()/scale,rcond=None)[0]
    if not np.allclose(coef[:,0],coef[:,1:4].sum(axis=1),atol=1e-10,rtol=0):
        raise ValueError("common-scale coefficient identity failed")
    return {name:dict(zip(cols,map(float,coef[i]))) for i,name in enumerate(names) if name in {"wind","Bombus","interaction"}}

def decompose(d):
    out={}
    for cut in [1,5,10]:
        q=d[d[E]>=cut]
        for inter in ["none","global","within"]:
            for blk in [True,False]:
                if inter=="within" and not blk:continue
                key=f"{cut}_{inter}_{blk}"
                out[key]={"n":len(q),"blocks":q[G].nunique(),"values":common_scale(q,True,inter,blk)}
    for wind in [W,"gust10_secondary","gust20_secondary"]:
        for blk in [True,False]:
            out[f"all72_{wind}_{blk}"]={"n":72,"blocks":17,"values":common_scale(d,False,"none",blk,wind)}
    return out

def source_labels(d,nhm,wcvp):
    raw,_=load_nhm(nhm);regions,_=wcvp_regions(wcvp,raw)
    if len(regions)!=367 or len(set().union(*regions.values()))!=55775:raise ValueError("global source registry drift")
    regions={code:regions[code] for code in d.TDWG_L3}
    pool=set().union(*regions.values())
    if len(pool)!=20196:raise ValueError("exploration native pool drift")
    mark={};length={}
    with nhm.open(encoding="utf-8-sig",newline="") as f:
        for row in csv.DictReader(f):
            sp=strict_name(row.get("taxon"))
            if sp in pool and mark_state(row)!="source_colour_missing":
                mark[sp]=int(mark_state(row)=="positive_lexical")
                length[sp]=sum(len(str(row.get(c) or "").strip()) for c in ("flower colour","petal colour","corolla colour"))
    species=sorted(mark);ids={s:i for i,s in enumerate(species)}
    y=np.array([mark[s] for s in species],dtype=float)
    if len(y)!=11133 or y.sum()!=302:raise ValueError("source marking cohort drift")
    incidence=np.zeros((len(d),len(y)),dtype=float)
    for i,code in enumerate(d.TDWG_L3):
        incidence[i,[ids[s] for s in regions[code] if s in ids]]=1
    if not np.array_equal(incidence.sum(axis=1),d.n_colour_documented.to_numpy()) or not np.array_equal(incidence@y,d.n_mark_positive.to_numpy()):
        raise ValueError("reconstructed 72 source counts do not match Stage116")
    freq=incidence.sum(axis=0)
    A=incidence/incidence.sum(axis=1,keepdims=True)
    if not np.allclose(A@y,d[Y],atol=1e-12,rtol=0):raise ValueError("source observed marking report rate drift")
    return A,y,species,freq,np.array([length[s] for s in species])

def group_indices(keys):
    groups=defaultdict(list)
    for i,k in enumerate(keys):groups[k].append(i)
    return [np.array(v,dtype=int) for _,v in sorted(groups.items())]

def conditional_null(A,y,weights,groups,reps,seed):
    # Every random label vector preserves the number of positive reports in
    # each source stratum, and each species' entire original native-range vector.
    means=np.zeros(len(y));mixed=[]
    for idx in groups:
        k=int(y[idx].sum());means[idx]=k/len(idx)
        if 0<k<len(idx):mixed.append((idx,k))
    fixed=y.copy()
    for idx,k in mixed:fixed[idx]=0
    expected=weights@means;observed=weights@y
    rng=np.random.default_rng(seed)
    sim=np.tile(weights@fixed,(reps,1))
    # Add each stratum's selected positive contributions without an expensive
    # species x draw matrix. Singleton/all-positive/all-nonpositive are fixed.
    for idx,k in mixed:
        for j in range(reps):
            chosen=rng.choice(idx,size=k,replace=False)
            sim[j]+=weights[:,chosen].sum(axis=1)
    return {"strata":len(groups),"mixed_strata":len(mixed),"movable_positive_labels":sum(k for _,k in mixed),
        "species_in_mixed_strata":sum(len(idx) for idx,_ in mixed),"reps":reps,
        "observed":observed,"conditional_expected":expected,
        "null_q025":np.quantile(sim,.025,axis=0),"null_q975":np.quantile(sim,.975,axis=0),
        "two_sided_centered_tail_fraction":(1+np.sum(np.abs(sim-expected)>=np.abs(observed-expected)-1e-12,axis=0))/(reps+1)}

def null_diagnostics(d,A,y,species,freq,length,reps=999):
    q=d[d[E]>=5];specs=[("wind_all72",d,False,"none","wind"),("Bombus_additive_37",q,True,"none","Bombus"),("global_product_37",q,True,"global","interaction"),("within_product_37",q,True,"within","interaction")]
    weights=[];labels=[]
    for label,sub,bee,inter,term in specs:
        X,names=design(sub,bee,inter,True)
        weights.append(np.linalg.pinv(X)[names.index(term)]@A[sub.index,:]/sub[Y].std(ddof=0));labels.append(label)
    weights=np.array(weights)
    genus=[s.split()[0] for s in species]
    # Fixed coarse bins, not selected from the observed effect sign.
    rb=np.digitize(freq,[2,5,10]);lb=np.digitize(length,[10,30,60])
    modes={"all_documented":group_indices(["all"]*len(y)),
        "within_genus":group_indices(genus),
        "within_genus_range":group_indices(list(zip(genus,rb))),
        "within_genus_range_description_length":group_indices(list(zip(genus,rb,lb)))}
    out={}
    for mode,groups in modes.items():
        result=conditional_null(A,y,weights,groups,reps,20261126)
        out[mode]={k:(dict(zip(labels,map(float,v))) if isinstance(v,np.ndarray) else v) for k,v in result.items()}
    return out

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--stage116",required=True,type=Path);p.add_argument("--nhm",type=Path);p.add_argument("--wcvp",type=Path);p.add_argument("--out",required=True,type=Path);p.add_argument("--decompose-only",action="store_true");a=p.parse_args()
    d=load(a.stage116)
    result={"source_stage116_SHA256":ARCHIVE_SHA,"common_scale_coefficients":decompose(d),"source_labels_not_true_trait_negatives":True,"NO_holdout_outcome_join":True,"NO_causal_phylogenetic_or_confirmatory_claim":True}
    if not a.decompose_only:
        A,y,s,f,l=source_labels(d,a.nhm,a.wcvp);result["conditional_source_label_nulls"]=null_diagnostics(d,A,y,s,f,l)
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("STAGE117_SOURCE_HIERARCHY",json.dumps(result,sort_keys=True))
