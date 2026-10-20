"""Independent original-data wind: arrival counts versus orchid-bee composition.

This secondary analysis is exploratory. Do not call the existing published
orchid-bee wind/count association a new field discovery.
"""
import argparse,hashlib,io,json,zipfile
from pathlib import Path
import numpy as np,pandas as pd,statsmodels.api as sm
import statsmodels.formula.api as smf

SOURCE_MD5="42e53512e4bdad2701593a89d1c87dfd"
def load(path):
    original=Path(path).read_bytes()
    if hashlib.md5(original).hexdigest()!=SOURCE_MD5:raise ValueError("SOURCE_MD5_MISMATCH")
    with zipfile.ZipFile(io.BytesIO(original)) as z:
        s=pd.read_csv(io.BytesIO(z.read("Zenodo/integratedSpatialWindData.csv")),encoding="latin-1")
        b=pd.read_csv(io.BytesIO(z.read("Zenodo/beedata.csv")))
    s["key"]=s.site.astype(str)+"|"+s.date.astype(str)+"|"+s.scent.astype(str)
    b["key"]=b.site.astype(str)+"|"+b.date.astype(str)+"|"+b.scent.astype(str)
    if s.key.duplicated().any():raise ValueError("DUPLICATE_SESSION")
    found=b.loc[b.key.isin(s.key)].copy()
    found["taxon"]=found.genus.astype(str).str.strip()+" "+found.species.astype(str).str.strip()
    mat=pd.crosstab(found.key,found.taxon).reindex(s.key,fill_value=0).reset_index(drop=True)
    if not np.array_equal(mat.sum(axis=1).to_numpy(int),s["count"].to_numpy(int)):
        raise ValueError("UNMATCHED_SPECIES_AND_COUNT")
    s["month"]=pd.to_datetime(s.date,format="%m/%d/%y").dt.strftime("%Y-%m")
    s["block"]=s.site+"|"+s.month+"|"+s.scent
    s["logwind"]=np.log(s["wind.mean"].to_numpy(float))
    qc={"sessions":len(s),"sites":int(s.site.nunique()),"bee_count":int(s["count"].sum()),
        "matched_specimens":len(found),"unmatched_specimens":len(b)-len(found),
        "true_zero_sessions":int((s["count"]==0).sum()),"species":mat.shape[1]}
    return s,mat.to_numpy(float),qc

def center(a,g):
    a=np.asarray(a,float);g=np.asarray(g);v=a.copy()
    for key in np.unique(g):
        ix=(g==key);v[ix]-=a[ix].mean()
    return v

def reshuffle(a,g,rng):
    a=np.asarray(a,float);g=np.asarray(g);z=a.copy()
    for key in np.unique(g):
        ix=np.flatnonzero(g==key);z[ix]=rng.permutation(a[ix])
    return z

def abundance_stat(a,y,g):
    x=center(a,g);z=center(y,g)
    den=np.sqrt(np.dot(x,x)*np.dot(z,z))
    return float(np.dot(x,z)/den) if den>0 else 0.

def composition_stat(a,c,g):
    x=center(a,g);n=c.sum(axis=1);res=c.copy()
    if not np.dot(x,x):return 0.
    for key in np.unique(g):
        ix=g==key;tot=c[ix].sum(axis=0)
        if tot.sum()>0:res[ix]-=n[ix,None]*tot[None,:]/tot.sum()
    k=x@res
    return float(np.sum(k*k/(c.sum(axis=0)+1.))/np.dot(x,x))

def analyze(path,reps=4999,seed=20261021):
    s,c,qc=load(path)
    m=smf.glm("count ~ logwind + C(site) + C(month) + C(scent)",
       data=s,family=sm.families.Poisson())
    fit=m.fit(maxiter=100)
    cluster=m.fit(cov_type="cluster",cov_kwds={"groups":s.site},maxiter=100)
    x=s.logwind.to_numpy(float);y=s["count"].to_numpy(float);g=s.block.to_numpy()
    obs=abundance_stat(x,y,g);rng=np.random.default_rng(seed)
    null=np.array([abundance_stat(reshuffle(x,g,rng),y,g) for _ in range(reps)])
    p_count=(1+int((np.abs(null)>=abs(obs)-1e-12).sum()))/(reps+1)
    positive=s["count"].to_numpy()>0
    sp=s.loc[positive].reset_index(drop=True)
    species=c[positive];wp=sp.logwind.to_numpy(float);gp=sp.block.to_numpy()
    obs2=composition_stat(wp,species,gp)
    null2=np.array([composition_stat(reshuffle(wp,gp,rng),species,gp) for _ in range(reps)])
    p_comp=(1+int((null2>=obs2-1e-12).sum()))/(reps+1)
    cl=cluster.conf_int().loc["logwind"].to_numpy(float)
    return {"source_doi":"10.5281/zenodo.3675327","source_md5":SOURCE_MD5,
      "source_qc":qc,"wind_per_doubling_rr":float(np.exp(fit.params["logwind"]*np.log(2))),
      "site_cluster_95ci_rr":list(np.exp(cl*np.log(2))),
      "n_independent_sites":int(s.site.nunique()),
      "within_block_count_corr":obs,"count_perm_p_two_sided":p_count,
      "composition_score":obs2,"composition_perm_p_right_tail":p_comp,
      "permutation_reps":reps,
      "uncertainty":"nine site clusters; wind not randomized; composition tests condition on positive catches; no ecological interaction hierarchy inferred"}

def main():
    a=argparse.ArgumentParser();a.add_argument("--source",required=True)
    a.add_argument("--out",default="wind_orchid_results.json")
    a.add_argument("--reps",type=int,default=4999);args=a.parse_args()
    result=analyze(args.source,args.reps)
    Path(args.out).parent.mkdir(exist_ok=True,parents=True)
    Path(args.out).write_text(json.dumps(result,indent=2))
    print("ORCHID_COUNT_COMPOSITION_COMPLETE",json.dumps(result))
if __name__=="__main__":main()
