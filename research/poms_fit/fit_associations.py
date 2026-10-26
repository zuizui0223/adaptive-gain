"""Exploratory zero-inclusive UK PoMS FIT wind/time visit-rate analysis.

A single-target-flower 10-minute survey is not a choice-set or cue-routeability
experiment. Wind comparisons are observational conditional rate associations.
"""
from __future__ import annotations
import argparse,hashlib,io,json,warnings,zipfile
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from stage3_source_audit import DATASET_DOI
from stage3_full_profile import TABLES

SOURCE_SHA256='9e30b02e640279f0c777526f1d4e0cf057ae9ab7991da5e9a5936659f1d5dcfb'
WIND=['Leaves still/moving occasionally','Leaves moving gently all the time','Leaves moving strongly']
SUN=['Entirely in sunshine','Partly in sun and partly shaded','Entirely shaded']
GUILDS=['bumblebees','hoverflies','other_flies','butterflies_moths']

def read_source(raw):
    for encoding in ('utf-8','cp1252','latin-1'):
        try:return pd.read_csv(io.StringIO(raw.decode(encoding,errors='strict')),low_memory=False),encoding
        except UnicodeDecodeError:pass
    raise ValueError('no strict text decoder')

def prepare(df,surface,outcome='all_insects_total',exclude_other=False):
    req={'sample_id','date','year','target_flower_corrected','floral_unit',
         'floral_unit_count','wind_speed','sunshine',outcome}
    location='location_code' if surface=='one_km' else 'x1km_square'
    req.add(location)
    if surface=='public':req|={'country','habitat_type'}
    if not req<=set(df):raise ValueError(f'missing columns: {req-set(df)}')
    t=df.copy();n=len(t)
    t['date_parsed']=pd.to_datetime(t.date,errors='coerce',dayfirst=True)
    t['day_of_year']=t.date_parsed.dt.dayofyear
    t['floral_unit_count']=pd.to_numeric(t.floral_unit_count,errors='coerce')
    t[outcome]=pd.to_numeric(t[outcome],errors='coerce')
    conditions={
      'sample_date_year':t.sample_id.notna()&t.date_parsed.notna()&t.year.notna(),
      'flower_units_positive':t.floral_unit_count.gt(0)&np.isfinite(t.floral_unit_count),
      'count_integer_nonnegative':t[outcome].ge(0)&np.isfinite(t[outcome])&(t[outcome]%1==0),
      'wind_recorded':t.wind_speed.isin(WIND),
      'sunshine_recorded':t.sunshine.isin(SUN),
      'target_and_floral_unit':t.target_flower_corrected.notna()&t.floral_unit.notna(),
      'location_recorded':t[location].notna(),
    }
    if surface=='public':conditions['habitat_country_recorded']=t.country.notna()&t.habitat_type.notna()
    if exclude_other:conditions['named_target']=~t.target_flower_corrected.eq('Other - please describe below')
    flow={'raw':n};mask=np.ones(n,dtype=bool)
    for name,cond in conditions.items():
        keep=cond.fillna(False).to_numpy(dtype=bool)
        flow[name+'_excluded']=int(np.sum(mask & ~keep))
        mask &= keep
    t=t.loc[mask].copy()
    if t.empty:raise ValueError('no eligible source surveys')
    flow.update(eligible=int(len(t)),zeros=int(t[outcome].eq(0).sum()))
    t['y']=t[outcome].astype(int)
    t['year']=t.year.astype(str)
    t['wind_speed']=pd.Categorical(t.wind_speed,categories=WIND,ordered=False)
    t['log_flower_units']=np.log1p(t.floral_unit_count.astype(float))
    return t,flow

def source_wind_support(d,surface):
    key='location_code' if surface=='one_km' else 'x1km_square'
    v=d.groupby(key,observed=True).wind_speed.nunique()
    return {'sites':int(len(v)),'sites_with_ge2_wind_levels':int((v>=2).sum()),
            'surveys_in_such_sites':int(d[key].isin(v[v>=2].index).sum())}

def formula(surface):
    f=("y ~ C(wind_speed, Treatment(reference='Leaves still/moving occasionally'))"
       " + log_flower_units + C(floral_unit) + C(target_flower_corrected)"
       " + C(year) + C(sunshine) + bs(day_of_year, df=4, degree=3)")
    return f+(' + C(location_code)' if surface=='one_km' else ' + C(country) + C(habitat_type)')

def wald(fit,names):
    if not names:return {'status':'no_terms'}
    r=np.zeros((len(names),len(fit.params)))
    for i,n in enumerate(names):r[i,fit.params.index.get_loc(n)]=1
    try:
        x=fit.wald_test(r,scalar=True)
        return {'status':'ok','statistic':float(x.statistic),'df':len(names),'p':float(x.pvalue)}
    except Exception as e:return {'status':'nonidentifiable','error':str(e)}

def fit(d,surface):
    cl='location_code' if surface=='one_km' else 'x1km_square'
    result={'status':'not_fit','n':len(d),'cluster_count':int(d[cl].nunique()),
            'formula':formula(surface)}
    if len(d)<100 or d[cl].nunique()<15 or d.y.sum()<=0:
        result['status']='insufficient';return result
    with warnings.catch_warnings(record=True) as issues:
        warnings.simplefilter('always')
        try:
            m=smf.glm(result['formula'],data=d,family=sm.families.Poisson()).fit(
                maxiter=120,cov_type='cluster',
                cov_kwds={'groups':d[cl].astype(str).to_numpy()})
        except Exception as e:
            result.update(status='model_failed',error=str(e));return result
    result['status']='fitted'
    result['converged']=bool(m.converged)
    result['overdispersion']=float(m.pearson_chi2/m.df_resid)
    result['zero_rate_observed']=float(d.y.eq(0).mean())
    result['zero_rate_poisson_fitted']=float(np.exp(-m.predict(d)).mean())
    result['warnings']=[str(w.message) for w in issues][-8:]
    wind=[n for n in m.params.index if n.startswith('C(wind_speed')]
    seasonal=[n for n in m.params.index if 'bs(day_of_year' in n]
    result['wind_wald']=wald(m,wind);result['season_wald']=wald(m,seasonal)
    ci=m.conf_int()
    result['wind_terms']={n:{
        'IRR':float(np.exp(m.params[n])),'CI95_low':float(np.exp(ci.loc[n,0])),
        'CI95_high':float(np.exp(ci.loc[n,1])),'cluster_p':float(m.pvalues[n])} for n in wind}
    return result

def raw_wind(d):
    g=d.groupby('wind_speed',observed=True).agg(
        surveys=('y','size'),visits_mean=('y','mean'),visits_sum=('y','sum'),
        zero_surveys=('y',lambda x:int((x==0).sum())))
    g['zero_rate']=g.zero_surveys/g.surveys
    return json.loads(g.reset_index().to_json(orient='records'))

def main(argv=None):
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',default='stage3_poms_audit')
    a=ap.parse_args(argv);out=Path(a.out)
    path=out/'poms_fit_2017_2023_source.zip'
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    if digest!=SOURCE_SHA256:raise ValueError('source checksum changed')
    report={'status':'observational_only','doi':DATASET_DOI,
            'source_sha256':digest,'no_routeability_inference':True,'surfaces':{}}
    with zipfile.ZipFile(path) as z:
        for surface,member in [('one_km',TABLES['one_km']),('public',TABLES['public'])]:
            data,encoding=read_source(z.read(member))
            entry={'raw_surveys':len(data),'encoding':encoding,'models':{}}
            outcomes=['all_insects_total']+GUILDS if surface=='one_km' else ['all_insects_total']
            for outcome in outcomes:
                d,flow=prepare(data,surface,outcome)
                entry['models'][outcome]={'eligibility':flow,
                    'wind_overlap':source_wind_support(d,surface),
                    'descriptive_by_wind':raw_wind(d),'fit':fit(d,surface)}
            if surface=='one_km':
                d,flow=prepare(data,surface,'all_insects_total',exclude_other=True)
                entry['models']['total_exclude_other']={'eligibility':flow,
                    'wind_overlap':source_wind_support(d,surface),
                    'descriptive_by_wind':raw_wind(d),'fit':fit(d,surface)}
            report['surfaces'][surface]=entry
    (out/'fit_associations_results.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
    for surface,e in report['surfaces'].items():
        for outcome,r in e['models'].items():
            print('POMS_ASSOCIATION '+json.dumps({'surface':surface,'outcome':outcome,**r}),flush=True)
    print('POMS_ASSOCIATION_COMPLETE',flush=True)

if __name__=='__main__':main()
