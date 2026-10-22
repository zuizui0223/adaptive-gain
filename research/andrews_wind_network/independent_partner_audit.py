"""Independent source-row recreation and finite-label analysis of SA026.

Does not import or reuse flower_partner_wind.py functions.
"""
from pathlib import Path
from itertools import combinations
import json,hashlib
import numpy as np,pandas as pd

ROOT=Path(__file__).parent
src=ROOT/'source';report=json.load(open(ROOT/'results'/'summary.json'))
watch=pd.read_csv(src/'watch.csv',dtype=str,keep_default_na=False,encoding='latin-1')
flowers=pd.read_csv(src/'flowers.csv',dtype=str,keep_default_na=False,encoding='latin-1')
KEY=['SAMPLEDATE','PLOT_ID','WATCH']
watch['minnum']=pd.to_numeric(watch.MINUTE,errors='coerce')
watch['num']=pd.to_numeric(watch.NO_INT,errors='coerce')
watch['good']=~((watch.PPI_STATUS=='1') & ~watch.num.gt(0))
# Explicit union of row and minute failures; no production helper used.
qualities=[]
for key,part in watch.groupby(KEY,sort=False):
    all_mins=part.minnum.between(1,15).all() and set(part.minnum.dropna())==set(range(1,16))
    same_wind=part.WIND.nunique()==1 and part.WIND.iloc[0] in ('ST','BR')
    status_consistent=part.groupby('MINUTE').PPI_STATUS.nunique().max()<=1
    if all_mins and same_wind and status_consistent and part.good.all():
        qualities.append((*key,str(part.MEADOW.iloc[0]),str(part.WIND.iloc[0])))
q=pd.DataFrame(qualities,columns=KEY+['meadow','wind'])
if len(q)!=1296:raise AssertionError(('watch QC',len(q)))
fl=flowers[(flowers.FLW_STATUS=='FLW')&(flowers.PLTSP_CODE!='')][KEY+['PLTSP_CODE']].drop_duplicates()
fl=fl.merge(q,on=KEY,how='inner')
visit=watch[(watch.PPI_STATUS=='1')&(watch.num.gt(0))&(watch.PLTSP_CODE!='')].copy()
visit=visit.merge(q[KEY],on=KEY,how='inner')
visits=set(zip(visit.SAMPLEDATE,visit.PLOT_ID,visit.WATCH,visit.PLTSP_CODE))
bees={'social bee','solitary bee','halictine bee','semi-social bee','halictine bee/semi-social bee','pollenivore bee'}
beev=visit[visit.VISSP_TYPE.str.lower().str.strip().isin(bees)]
beevisits=set(zip(beev.SAMPLEDATE,beev.PLOT_ID,beev.WATCH,beev.PLTSP_CODE))
# Compute exact finite wind-label support AND wind-plant-H without production functions
site_values={};counter={'candidate_days':0,'kept_days':0,'linked_flower_occurrences':0,'pair_flower_species_dates':0}
for (meadow,date),allfl in fl.groupby(['meadow','SAMPLEDATE'],sort=True):
    byplant=allfl.groupby('PLTSP_CODE').wind.nunique()
    eligible=sorted(byplant[byplant==2].index)
    if len(eligible)<2:continue
    counter['candidate_days']+=1
    ww=q[(q.meadow==meadow)&(q.SAMPLEDATE==date)].sort_values(KEY).reset_index(drop=True)
    ids=list(zip(ww.SAMPLEDATE,ww.PLOT_ID,ww.WATCH))
    wind=(ww.wind=='BR').to_numpy()
    overlap=set(zip(allfl.SAMPLEDATE,allfl.PLOT_ID,allfl.WATCH,allfl.PLTSP_CODE))
    B=np.array([[(*key,p) in overlap for p in eligible] for key in ids],bool)
    Y=np.array([[(*key,p) in visits for p in eligible] for key in ids],bool)
    Yb=np.array([[(*key,p) in beevisits for p in eligible] for key in ids],bool)
    # A visit to a plant not independently recorded blooming in that watch
    # is not a valid measured flower-exposure event for this estimand.
    Y &= B
    Yb &= B
    allowed=[]
    for choose in combinations(range(len(ids)),int(wind.sum())):
        s=set(choose);m=np.array([i in s for i in range(len(ids))])
        if all(any(B[i,j] for i in s) and any(B[i,j] for i in range(len(ids)) if i not in s) for j in range(len(eligible))):allowed.append(m)
    if len(allowed)<2:continue
    counter['kept_days']+=1;counter['pair_flower_species_dates']+=len(eligible);counter['linked_flower_occurrences']+=B.sum()
    # Independent identity H=E[delta^2]-E[delta]^2
    def calc(m):
        res=[]
        for yy in [Y,Yb]:
            delta=yy[m].sum(0)/B[m].sum(0)-yy[~m].sum(0)/B[~m].sum(0)
            res.extend([float(np.mean(delta**2)-np.mean(delta)**2),float(np.mean(delta))])
        return np.array(res)[[0,2,1,3]]
    obs=calc(wind);ref=np.mean([calc(mm) for mm in allowed],axis=0)
    h=hashlib.sha256(str(meadow).encode()).hexdigest()[:14]
    site_values.setdefault(h,[]).append(obs-ref)
computed={h:np.mean(v,axis=0) for h,v in site_values.items()}
sc={x['meadow_hash']:x for x in report['variants']['main']['site_scores']}
errors=[]
for h,value in computed.items():
    actual=np.array([sc[h][x] for x in ['H_all','H_bee','signed_all','signed_bee']])
    errors.append(np.max(np.abs(value-actual)))
site_equal=np.mean(list(computed.values()),axis=0)
actual=np.array([report['variants']['main']['metrics'][x]['excess_above_exact_assignment_mean']
                 for x in ['H_all','H_bee','signed_all','signed_bee']])
report_qc={'source_verified':True,'independent_source_eligible_watches':len(q),
  'n_site_days_with_2_same_bloom_plants_before_perm_gate':counter['candidate_days'],
  'n_site_days_after_gate':counter['kept_days'],'n_independent_meadows':len(computed),
  'n_plant_dates':counter['pair_flower_species_dates'],
  'n_plant_watch_observation_opportunities':int(counter['linked_flower_occurrences']),
  'max_site_level_absolute_difference':float(max(errors)),
  'max_primary_stat_absolute_difference':float(np.max(np.abs(site_equal-actual))),
  'primary_excess_check':{key:float(value) for key,value in zip(['H_all','H_bee','signed_all','signed_bee'],site_equal)}}
print(json.dumps(report_qc,indent=2))
assert report_qc['n_site_days_after_gate']==35
assert report_qc['n_independent_meadows']==11
assert report_qc['n_plant_dates']==162
assert report_qc['n_plant_watch_observation_opportunities']==627
assert max(errors)<1e-12 and np.max(np.abs(site_equal-actual))<1e-12
(ROOT/'results'/'independent_audit.json').write_text(json.dumps(report_qc,indent=2))