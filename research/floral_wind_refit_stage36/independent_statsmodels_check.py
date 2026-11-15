"""Stage36 numerical cross-check with INDEPENDENT statsmodels Poisson IRLS.

This deliberately reuses the ORIGINAL pinned Crall Zenodo observation table,
but NOT the hand-coded conditional-Poisson optimizer from our first fit.
For fixed site intercepts, unconditional Poisson GLM maximization and
site-total-conditioned Poisson must agree in the wind/turbulence coefficients.

Robust site/date SEs are purely descriptive with 9 sites and 29 dates,
NOT an exact replica of the author's site+date random-intercept GLMM.
"""
from __future__ import annotations
import json
import math
from pathlib import Path

from conditional_site_poisson import get_source,read_original_session_records

def independently_refit(rows,primary):
    import numpy as np
    import statsmodels.api as sm
    from scipy.stats import t
    site=sorted({r['site'] for r in rows})
    dates=sorted({r['date'] for r in rows})
    idx_site={value:j for j,value in enumerate(site)}
    idx_date={value:j for j,value in enumerate(dates)}
    y=np.array([r['count'] for r in rows],dtype=float)
    features=[]
    for row in rows:
        group=[0.]* (len(site)-1)
        if idx_site[row['site']]>0:
            group[idx_site[row['site']]-1]=1.
        features.append([1.,row['log_wind'],row['relative_tke'],*group])
    X=np.asarray(features,dtype=float)
    if np.linalg.matrix_rank(X)!=X.shape[1]:
        raise ValueError('NO_GO_SITE_FIXED_GLM_RANK_DEFICIENT')
    model=sm.GLM(y,X,family=sm.families.Poisson())
    fitted=model.fit(maxiter=150,method='IRLS')
    if not fitted.converged:
        raise ValueError('NO_GO_STATSMODELS_POISSON_DID_NOT_CONVERGE')
    expected=primary['predictors']
    diffs={
      'log_wind':abs(float(fitted.params[1])-expected['log_wind']['beta']),
      'relative_tke':abs(float(fitted.params[2])-expected['relative_tke']['beta'])}
    if max(diffs.values())>1e-7:
        raise ValueError('NO_GO_TWO_INDEPENDENT_POISSON_SOLVERS_DISAGREE')
    siteids=np.array([idx_site[r['site']] for r in rows],dtype=int)
    dateids=np.array([idx_date[r['date']] for r in rows],dtype=int)
    # Statsmodels small-sample correction, but only 9 site clusters:
    # neither the normal nor t8 intervals have universal calibrated coverage.
    fit_site=model.fit(maxiter=150,cov_type='cluster',
                       cov_kwds={'groups':siteids,'use_correction':True})
    fit_date=model.fit(maxiter=150,cov_type='cluster',
                       cov_kwds={'groups':dateids,'use_correction':True})
    b=float(fitted.params[1])
    mult=math.log10(2)
    def ci(se,crit):
        return [math.exp((b-crit*se)*mult),
                math.exp((b+crit*se)*mult)]
    df_site=len(site)-1
    df_date=len(dates)-1
    return {
       'status':'INDEPENDENT_STATSMODELS_ORIGINAL_SESSION_POISSON_AGREEMENT',
       'independent_solver':'statsmodels GLM log-Poisson IRLS with 8 site indicators',
       'primary_solver':'hand-coded conditional site-total Poisson',
       'n_original_source_sessions':len(rows),
       'n_sites':len(site),'n_dates':len(dates),
       'total_visits':int(y.sum()),
       'model_rank':int(np.linalg.matrix_rank(X)),
       'model_columns':int(X.shape[1]),
       'max_wind_and_tke_coefficient_absolute_diff':max(diffs.values()),
       'wind_log10_coefficient':b,
       'wind_rate_ratio_per_doubling':math.exp(b*mult),
       'modelbased_IRR_95ci':ci(float(fitted.bse[1]),1.96),
       'site_cluster_sandwich_se_logwind':float(fit_site.bse[1]),
       'site_cluster_IRR_95ci_t8_approx':ci(float(fit_site.bse[1]),
                                            float(t.ppf(.975,df_site))),
       'date_cluster_sandwich_se_logwind':float(fit_date.bse[1]),
       'date_cluster_IRR_95ci_t28_approx':ci(float(fit_date.bse[1]),
                                              float(t.ppf(.975,df_date))),
       'actual_original_GLMM_with_random_site_date_NOT_reproduced':True,
       'site_cluster_nine_not_asymptotically_large':True,
       'date_within_site_autocorrelation_and_other_dependence_unresolved':True,
       'conditioned_on_bait_sampling_not_scent_ON_OFF':True,
       'not_causal_odor_plume_mediation':True,
       'original_raw_csv_not_redistributed':True,
    }

def main():
    first=Path('stage36_refit_receipts/stage36_source_locked_within_site_poisson.json')
    if not first.exists():
        raise ValueError('NO_GO_MISSING_PRIMARY_SOURCE_VERIFIED_REFIT')
    x=json.loads(first.read_text(encoding='utf8'))
    if x.get('status')!='CRALL_REAL_SESSION_SITE_CONDITIONAL_POISSON_REFIT_WITH_LIMITS':
        raise ValueError('NO_GO_INVALID_PRIMARY_SOURCE_CLAIM')
    data=read_original_session_records(get_source())
    result=independently_refit(data,x['primary_site_conditional_poisson'])
    dest=Path('stage36_refit_receipts')
    (dest/'stage36_independent_statsmodels_poisson_check.json').write_text(
        json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf8')
    print(json.dumps(result,sort_keys=True,allow_nan=False))

if __name__=='__main__':
    main()
