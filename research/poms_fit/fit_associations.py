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

# The publisher generates packaging HTML dynamically, so full ZIP hashes change.
# Pin actual data CSV bytes separately rather than incorrectly pinning ZIP bytes.
SOURCE_DATA_CRC32={'one_km':'4eb3f12d','public':'fdd5e69f'}
SOURCE_DATA_BYTES={'one_km':1690496,'public':6712935}
SOURCE_DATA_SHA256={
 'one_km':'29d3deb757c053774c26ece0a7683081a4b4fe81d9497877fe1179f232182e52',
 'public':'bcd2ef780d3208a5a4aba5c191178900ccef705e5b569dc0160b27d00652dc3c'
}
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

def formula(surface,drop_redundant_unit=False):
    flower_term="" if drop_redundant_unit else " + C(floral_unit)"
    f=("y ~ C(wind_speed, Treatment(reference='Leaves still/moving occasionally'))"
       " + log_flower_units" + flower_term + " + C(target_flower_corrected)"
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

def fit(d,surface,family_variant='poisson',drop_redundant_unit=False):
    cl='location_code' if surface=='one_km' else 'x1km_square'
    if family_variant not in ('poisson','nb_alpha1','nb_alpha2'):
        raise ValueError('undeclared family variant')
    result={'status':'not_fit','family_variant':family_variant,
            'redundant_floral_unit_removed':bool(drop_redundant_unit),
            'n':len(d),'cluster_count':int(d[cl].nunique()),
            'formula':formula(surface,drop_redundant_unit)}
    if len(d)<100 or d[cl].nunique()<15 or d.y.sum()<=0:
        result['status']='insufficient';return result
    with warnings.catch_warnings(record=True) as issues:
        warnings.simplefilter('always')
        try:
            fam=(sm.families.Poisson() if family_variant=='poisson' else
                 sm.families.NegativeBinomial(alpha=(1.0 if family_variant=='nb_alpha1' else 2.0)))
            m=smf.glm(result['formula'],data=d,family=fam).fit(
                maxiter=120,cov_type='cluster',
                cov_kwds={'groups':d[cl].astype(str).to_numpy()})
        except Exception as e:
            result.update(status='model_failed',error=str(e));return result
    result['status']='fitted'
    result['converged']=bool(m.converged)
    result['overdispersion']=float(m.pearson_chi2/m.df_resid)
    result['zero_rate_observed']=float(d.y.eq(0).mean())
    mu=np.asarray(m.predict(d),dtype=float)
    if family_variant=='poisson':
        zero_pred=np.exp(-mu)
    else:
        alpha=(1.0 if family_variant=='nb_alpha1' else 2.0)
        zero_pred=(1.0+alpha*mu)**(-1.0/alpha)
    result['zero_rate_under_fitted_family']=float(zero_pred.mean())
    result['warnings']=[str(w.message) for w in issues][-8:]
    wind=[n for n in m.params.index if n.startswith('C(wind_speed')]
    seasonal=[n for n in m.params.index if 'bs(day_of_year' in n]
    result['wind_wald']=wald(m,wind);result['season_wald']=wald(m,seasonal)
    ci=m.conf_int()
    if wind and not np.isfinite(ci.loc[wind].to_numpy()).all():
        result['status']='nonidentifiable_robust_intervals'
        result['wind_point_IRR_only']={n:float(np.exp(m.params[n])) for n in wind}
        result['wind_terms']={}
        return result
    if wind and np.any(np.abs(ci.loc[wind].to_numpy())>100):
        result['status']='nonidentifiable_extreme_robust_intervals'
        result['wind_point_IRR_only']={n:float(np.exp(m.params[n])) for n in wind}
        result['wind_terms']={}
        return result
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
    report={'status':'observational_only','doi':DATASET_DOI,
            'source_zip_sha256_receipt_not_a_pinned_digest':digest,
            'no_routeability_inference':True,'data_member_sha256':{},'surfaces':{}}
    with zipfile.ZipFile(path) as z:
        for surface,member in [('one_km',TABLES['one_km']),('public',TABLES['public'])]:
            info=z.getinfo(member)
            if f'{info.CRC:08x}'!=SOURCE_DATA_CRC32[surface] or info.file_size!=SOURCE_DATA_BYTES[surface]:
                raise ValueError(f'official original CSV member changed: {surface}')
            member_bytes=z.read(member)
            member_digest=hashlib.sha256(member_bytes).hexdigest()
            if member_digest != SOURCE_DATA_SHA256[surface]:
                raise ValueError(f'original source CSV SHA-256 changed: {surface}')
            report['data_member_sha256'][surface]=member_digest
            data,encoding=read_source(member_bytes)
            entry={'raw_surveys':len(data),'encoding':encoding,'models':{}}
            outcomes=['all_insects_total']+GUILDS if surface=='one_km' else ['all_insects_total']
            for outcome in outcomes:
                d,flow=prepare(data,surface,outcome)
                entry['models'][outcome]={'eligibility':flow,
                    'wind_overlap':source_wind_support(d,surface),
                    'descriptive_by_wind':raw_wind(d),'fit':fit(d,surface)}
                if outcome=='all_insects_total':
                    entry['models'][outcome]['posthoc_nb_sensitivity']={
                        'alpha1':fit(d,surface,'nb_alpha1'),
                        'alpha2':fit(d,surface,'nb_alpha2')}
            if surface=='one_km':
                d,flow=prepare(data,surface,'all_insects_total',exclude_other=True)
                units_per_target=d.groupby('target_flower_corrected').floral_unit.nunique()
                exact_alias=bool((units_per_target==1).all())
                original_fit=({'status':'nonidentifiable_exact_floral_unit_target_alias',
                               'n':len(d),'formula':formula(surface),
                               'note':'Original predeclared model has an exact rank deficit. Refuse invalid covariance inference.'}
                              if exact_alias else fit(d,surface))
                entry['models']['total_exclude_other']={'eligibility':flow,
                    'wind_overlap':source_wind_support(d,surface),
                    'descriptive_by_wind':raw_wind(d),'fit':original_fit,
                    'design_diagnostic':{
                        'all_named_targets_have_one_floral_unit_type':bool((units_per_target==1).all()),
                        'target_units_nunique_by_label':{str(k):int(v) for k,v in units_per_target.items()},
                        'interpretation':'Nested floral-unit and target indicators are exactly aliased; retain the failed predeclared full specification.'}}
                if exact_alias:
                    entry['models']['total_exclude_other']['posthoc_exact_alias_repair']=fit(
                        d,surface,drop_redundant_unit=True)
            report['surfaces'][surface]=entry
    (out/'fit_associations_results.json').write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False))
    for surface,e in report['surfaces'].items():
        for outcome,r in e['models'].items():
            print('POMS_ASSOCIATION '+json.dumps({'surface':surface,'outcome':outcome,**r},allow_nan=False),flush=True)
    print('POMS_ASSOCIATION_COMPLETE',flush=True)

if __name__=='__main__':main()
