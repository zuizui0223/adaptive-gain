"""Species-preserving no-environment-modulation reference for nectar prediction.
Not a phylogenetic test or causal inference. Null = global tube association
plus family intercept, exchangeable residuals inside fixed strata. Same
species/ranges and refit local-lineage-excluded model in every draw.
"""
import argparse,json,sys
from collections import defaultdict
from pathlib import Path
import numpy as np,pandas as pd
from scipy.stats import rankdata,kendalltau
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'floral_macro_stage121'))
from regional_reward_transfer import load_sources,separate_data,wcvp_regions
from regional_reward_environment import load,design,W,B,E,G
ALPHA=5.
def fit_slope(x,y):
    x=np.asarray(x,float);x=x-x.mean();den=float(x@x)
    # StandardScaler + Ridge(alpha=5) with unpenalized intercept, ddof=0.
    return float(x@y)/(den*(1+ALPHA/len(x))) if den>1e-12 else 0.
def evaluate_scores(x,ys,train,test):
    # ys: simulations x species, includes observed at index 0.
    xx=x[train];xc=xx-xx.mean();den=xc@xc
    slopes=(ys[:,train]@xc)/(den*(1+ALPHA/len(train))) if den>1e-12 else np.zeros(len(ys))
    xt=x[test];xt=xt-xt.mean();yt=ys[:,test];yc=yt-yt.mean(axis=1,keepdims=True);denom=(yc*yc).sum(axis=1)
    sk=np.divide(2*slopes*(yc@xt)-slopes**2*(xt@xt),denom,out=np.full(len(ys),np.nan),where=denom>1e-12)
    tau=np.array([np.sign(s)*kendalltau(x[test],y).statistic for s,y in zip(slopes,yt)])
    return sk,tau
def permutations(d,reps,mode,seed):
    x=d.tube.to_numpy(float);y=d.nectar.to_numpy(float)
    # Fit common global slope plus family offsets, not a geographical model.
    xc=x-d.groupby('family').tube.transform('mean').to_numpy()
    yc=y-d.groupby('family').nectar.transform('mean').to_numpy()
    b=fit_slope(xc,yc)
    a=(d.nectar-b*d.tube).groupby(d.family).transform('mean').to_numpy()
    fitted=a+b*x;res=y-fitted
    if mode=='family':keys=list(d.family)
    elif mode=='family_tube_bin':
        bins=np.digitize(x,np.unique(np.quantile(x,[.25,.5,.75])))
        keys=list(zip(d.family,bins))
    elif mode=='genus':keys=list(d.genus)
    else:raise ValueError('invalid null mode')
    groups=defaultdict(list)
    for i,k in enumerate(keys):groups[k].append(i)
    rng=np.random.default_rng(seed);Y=np.tile(y,(reps+1,1));movable=0;strata=0
    for idx in groups.values():
        if len(idx)<2:continue
        strata+=1;movable+=len(idx)
        for j in range(1,reps+1):
            Y[j,idx]=fitted[idx]+rng.permutation(res[idx])
    return Y,{'pooled_tube_slope':b,'movable_species':movable,'mixed_size_strata':strata,'total_species':len(y),'reps':reps}
def run(archive,source,archives,wcvp,reps=999):
    score=load(archive);data,_=load_sources(source,archives)
    d=separate_data(data['nectar'],'nectar');native,_=wcvp_regions(wcvp,set(d.species))
    accepted=set().union(*native.values());d=d[d.species.isin(accepted)].reset_index(drop=True)
    if len(d)!=373:raise ValueError('original accepted nectar species drift')
    q=score[(score.cohort=='nectar_separate')&(score.lineage_excluded=='genus')&score.status.eq('estimated_exploratory')].sort_values('TDWG_L3').reset_index(drop=True)
    if len(q)!=49 or q[G].nunique()!=12:raise ValueError('Stage121 cohort drift')
    x=d.tube.to_numpy(float);inds=[]
    for row in q.to_dict('records'):
        test=np.flatnonzero(d.species.isin(native.get(row['TDWG_L3'],set())))
        train=np.flatnonzero(~d.genus.isin(d.iloc[test].genus))
        if len(test)!=row['n_test'] or len(train)!=row['n_train']:raise ValueError('local source split drift')
        inds.append((train,test))
    out={}
    for mode in ['family','family_tube_bin','genus']:
        Y,meta=permutations(d,reps,mode,20261127)
        sk=[];tau=[]
        for tr,te in inds:
            s,t=evaluate_scores(x,Y,tr,te);sk.append(s);tau.append(t)
        S=np.asarray(sk).T;T=np.asarray(tau).T
        if not np.allclose(S[0],q.nectar_within_assemblage_pair_contrast_skill,atol=1e-10,rtol=0) or not np.allclose(T[0],q.nectar_kendall_tau_b,atol=1e-10,rtol=0):raise ValueError('Stage121 exact score replay failed')
        res={}
        for name,v in [('pair_skill',S),('tau_b',T)]:
            for bee in [False,True]:
                mask=(q[E]>=5).to_numpy() if bee else np.ones(len(q),bool)
                z=q.loc[mask];X,terms=design(z,bee,True,['n_test'])
                if X is None:raise ValueError('primary original screen not estimable')
                y=v[:,mask];valid=np.isfinite(y).all(axis=1)
                if not valid[0]:raise ValueError('observed score invalid')
                rank=rankdata(y[valid],axis=1);sd=rank.std(axis=1,keepdims=True);good=sd[:,0]>1e-12
                if not good[0]:raise ValueError('observed score constant')
                rz=(rank[good]-rank[good].mean(axis=1,keepdims=True))/sd[good]
                co=rz@np.linalg.pinv(X).T
                for i,term in enumerate(terms,1):
                    sim=co[1:,i];obs=float(co[0,i]);center=float(sim.mean())
                    res[name+('_bee' if bee else '_all')+'_'+term]={'observed':obs,'null_mean':center,'null_q025_q975':list(map(float,np.quantile(sim,[.025,.975]))),'two_sided_centered_tail_fraction':float((1+np.sum(np.abs(sim-center)>=abs(obs-center)-1e-12))/(len(sim)+1)),'valid_draws':len(sim)}
        out[mode]={**meta,'coefficients':res}
    return {'source_observed_scores_replayed':49,'rewards':'nectar only','null_is_conditional_exchangeability_not_causal_or_phylogenetic':True,'no_holdout_region_outcomes':True,'results':out}
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for k in ['archive','source','archives','wcvp','out']:p.add_argument('--'+k,required=True,type=Path)
    a=p.parse_args();r=run(a.archive,a.source,a.archives,a.wcvp);a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print('STAGE122_SPECIES_NULL',json.dumps(r,sort_keys=True))
