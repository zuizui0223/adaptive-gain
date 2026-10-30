"""Validation only: no alternative model, predictor, sample, or outcome is selected."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import statsmodels.api as sm
from association import within_plant, design, clustered_ols

def run(root):
    root=Path(root)
    d=pd.read_csv(root/'survey_cohort.csv');z,_=within_plant(d)
    result=json.loads((root/'association_results.json').read_text())
    checks={}
    for name,g,withcity in [('pooled',z,True)]+[(str(k),v,False) for k,v in z.groupby('site')]:
        original=result['primary'] if name=='pooled' else result['by_city_descriptive'][name]
        if original['status']!='ESTIMATED':continue
        X,names=design(g,city=withcity);Y=np.log1p(g.probes.to_numpy())
        groups=(g.site+'|'+g.date).to_numpy()
        independent=sm.OLS(Y,X).fit(cov_type='cluster',cov_kwds={'groups':groups,'use_correction':True},use_t=True)
        actual=clustered_ols(X,Y,groups)
        idx=names.index('w:r')
        db=float(np.max(np.abs(independent.params-actual['beta'])))
        dc=float(np.max(np.abs(independent.cov_params()-actual['cov'])))
        dp=float(abs(independent.pvalues[idx]-original['primary_interaction']['p_two_sided']))
        if db>1e-9 or dc>1e-9 or dp>1e-9:raise ValueError('INDEPENDENT_NUMERICAL_RECONCILIATION_FAILED')
        checks[name]={'max_coefficient_difference':db,'max_covariance_difference':dc,'primary_p_difference':dp}
    f=pd.read_csv(root/'forage.csv');n=pd.read_csv(root/'nectar.csv');w=pd.read_csv(root/'weather.csv')
    qa=json.loads((root/'cohort_receipt.json').read_text());details=[]
    for e in qa['excluded']:
        key=e['survey']
        details.append({'survey':key,'reason':e['reason'],
           'forage_metadata':f.loc[f.survey==key,['date','site','location','plant']].drop_duplicates().to_dict(orient='records'),
           'nectar_metadata':n.loc[n.survey==key,['date','site','plant']].drop_duplicates().to_dict(orient='records'),
           'weather_metadata':w.loc[w.survey==key,['date','site','location']].drop_duplicates().to_dict(orient='records')})
    weather_ids=set(w.survey)
    report={'status':'FROZEN_REAL_RESULTS_INDEPENDENTLY_RECONCILED',
            'independent_statsmodels_checks':checks,'excluded_source_metadata':details,
            'raw_surveys_with_any_weather':int(f[f.survey.isin(weather_ids)].survey.nunique()),
            'raw_behavior_rows_with_any_weather':int(f.survey.isin(weather_ids).sum()),
            'not_a_second_empirical_replication':True,'no_sample_or_model_revised':True}
    (root/'independent_verification.json').write_text(json.dumps(report,indent=2))
    print('STAGE11_INDEPENDENT_VERIFICATION '+json.dumps(report),flush=True)
    return report
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--out',default='stage11_original')
    run(p.parse_args().out)
