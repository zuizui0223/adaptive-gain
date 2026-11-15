"""Stage37: independent original Crall wind-data robustness, not causality.

Source: DOI 10.1098/rsbl.2020.0103, original Zenodo 3743898.
N=70 20-min scented perfume-bait collection sessions, nine sites, 29 dates.

Three checks beyond Stage36:
 (1) Cameron–Gelbach–Miller two-way sandwich with site & date, caveat G_site=9;
 (2) Poisson site+date FIXED intercepts with wind and relative TKE;
 (3) leave-one-original-date-out site-conditional Poisson.

Two-way cluster t8 endpoints are *approximate*, not exact calibrated
coverage. Date fixed effects are NOT the author's random-effects GLMM.
NO scent-off controls; NEVER call a wind-by-scent or plant fitness effect.
"""
from __future__ import annotations

import json
import math
import hashlib
from pathlib import Path

from conditional_site_poisson import (
    get_source,read_original_session_records,conditional_poisson
)

STAGE36_SHA='4250cb51754e59b861f90ff7063dbbc223dd515a146809273fee055de81772af'


def _design(rows):
    import numpy as np
    sites=sorted({r['site'] for r in rows})
    dates=sorted({r['date'] for r in rows})
    si={x:j for j,x in enumerate(sites)}
    di={x:j for j,x in enumerate(dates)}
    n=len(rows)
    y=np.array([r['count'] for r in rows],dtype=float)
    x0=np.column_stack([
       np.ones(n),
       [r['log_wind'] for r in rows],
       [r['relative_tke'] for r in rows]
    ])
    site=np.zeros((n,len(sites)-1))
    date=np.zeros((n,len(dates)-1))
    for i,row in enumerate(rows):
        if si[row['site']] != 0:
            site[i,si[row['site']]-1]=1.
        if di[row['date']] != 0:
            date[i,di[row['date']]-1]=1.
    groups_site=np.array([si[r['site']] for r in rows],dtype=int)
    groups_date=np.array([di[r['date']] for r in rows],dtype=int)
    return {
      'y':y,'X_site':np.column_stack((x0,site)),
      'X_full':np.column_stack((x0,site,date)),
      'group_site':groups_site,'group_date':groups_date,
      'sites':sites,'dates':dates
    }


def _interval_on_doubling(beta,se,crit):
    factor=math.log10(2)
    return [math.exp((beta-crit*se)*factor),
            math.exp((beta+crit*se)*factor)]


def _multicluster_robust(rows,stage36_beta):
    import numpy as np
    import statsmodels.api as sm
    from scipy.stats import t
    from statsmodels.stats.sandwich_covariance import cov_cluster_2groups
    design=_design(rows)
    y=design['y']
    x=design['X_site']
    if np.linalg.matrix_rank(x)!=x.shape[1]:
        raise ValueError('NO_GO_SITE_DESIGN_RANK_DEFICIENT')
    model=sm.GLM(y,x,family=sm.families.Poisson())
    fitted=model.fit(maxiter=150,method='IRLS')
    if not fitted.converged:
        raise ValueError('NO_GO_BASELINE_POISSON_NO_CONVERGENCE')
    b=float(fitted.params[1])
    if abs(b-stage36_beta)>1e-7:
        raise ValueError('NO_GO_STAGE36_BASELINE_NOT_REPRODUCED')
    # Multiway robust variance = V_site + V_date - V_site×date.
    # With 9 independent sites, finite-sample t8 is only a sensitivity.
    try:
        covariance,cov_site,cov_date=cov_cluster_2groups(
          fitted,design['group_site'],design['group_date'],
          use_correction=True)
        variance=float(covariance[1,1])
        if not math.isfinite(variance) or variance<=0:
            return {
              'status':'NO_GO_NONPOSITIVE_TWO_WAY_CLUSTER_VARIANCE',
              'two_way_wind_variance':variance,
              'site_count':len(design['sites']),
              'date_count':len(design['dates']),
              'model_wind_beta_reproduced':b,
              'not_valid_two_way_confidence_interval':True
            }
        se=math.sqrt(variance)
        lower,upper=_interval_on_doubling(
            b,se,float(t.ppf(.975,len(design['sites'])-1)))
        return {
          'status':'TWO_WAY_SITE_DATE_CLUSTER_SENSITIVITY_AVAILABLE',
          'two_way_wind_variance':variance,
          'two_way_wind_se':se,
          'wind_log10_beta':b,
          'wind_IRR_per_doubling':math.exp(b*math.log10(2)),
          'two_way_IRR_95ci_using_t8_APPROXIMATE':[lower,upper],
          'site_count':len(design['sites']),
          'date_count':len(design['dates']),
          'independence_assumption_sites_and_dates_cross_classified':True,
          'number_of_sites_small':True,
          'not_a_exactly_calibrated_95pct_interval':True,
          'not_original_random_site_date_GLMM':True,
        }
    except (ValueError,ZeroDivisionError,OverflowError) as err:
        return {
          'status':'NO_GO_TWO_WAY_CLUSTER_COVARIANCE_FAILURE',
          'failure_type':type(err).__name__,
          'failure_note':str(err)[:160],
          'site_count':len(design['sites']),
          'date_count':len(design['dates']),
          'not_valid_two_way_confidence_interval':True
        }


def _date_fixed(rows,stage36_beta):
    """Site+date fixed-effects sensitivity; never call it author GLMM."""
    import numpy as np
    import statsmodels.api as sm
    from scipy.stats import norm
    d=_design(rows)
    full=d['X_full']
    n=len(rows)
    # First ensure BOTH wind and TKE remain identifiable after projecting
    # away site+date nuisance contrasts. A rank-deficient nuisance design
    # alone does not make the wind term unidentified.
    N=np.column_stack((full[:,0],full[:,3:]))
    W=full[:,1:3]
    resid=W-N @ np.linalg.lstsq(N,W,rcond=None)[0]
    resid_rank=int(np.linalg.matrix_rank(resid,tol=1e-9))
    if resid_rank<2:
        return {
          'status':'NO_GO_WIND_OR_TKE_UNIDENTIFIED_AFTER_DATE_SITE',
          'residual_wind_tke_rank':resid_rank,
          'date_fixed_model_fit':False
        }
    # Retain the target two variables by adding any linearly independent
    # nuisance contrasts only after intercept and both target columns.
    chosen=[0,1,2]
    for j in range(3,full.shape[1]):
        z=full[:,chosen+[j]]
        if np.linalg.matrix_rank(z,tol=1e-9)==len(chosen)+1:
            chosen.append(j)
    X=full[:,chosen]
    if np.linalg.matrix_rank(X,tol=1e-9)!=X.shape[1]:
        raise ValueError('NO_GO_DATE_FIXED_DESIGN_RANK')
    try:
        fit=sm.GLM(d['y'],X,family=sm.families.Poisson()).fit(
            maxiter=200,method='IRLS')
        if not fit.converged:
            return {'status':'NO_GO_DATE_FIXED_POISSON_NONCONVERGENCE',
                    'date_fixed_model_fit':False}
        b=float(fit.params[1])
        se=float(fit.bse[1])
        if not all(map(math.isfinite,(b,se))) or se<=0:
            return {'status':'NO_GO_DATE_FIXED_WIND_SE_NONFINITE',
                    'date_fixed_model_fit':False}
        return {
            'status':'SITE_PLUS_DATE_FIXED_POISSON_SENSITIVITY_AVAILABLE',
            'n_sessions':n,'source_sites':len(d['sites']),
            'source_dates':len(d['dates']),
            'wind_log10_beta':b,
            'wind_IRR_per_doubling':math.exp(b*math.log10(2)),
            'modelbased_95ci_IRR_wind_doubling':
              _interval_on_doubling(b,se,1.96),
            'wind_beta_change_from_site_only':b-stage36_beta,
            'n_independent_design_columns':X.shape[1],
            'n_full_columns_requested':full.shape[1],
            'n_dependent_nuisance_columns_dropped':full.shape[1]-X.shape[1],
            'residual_wind_tke_rank':resid_rank,
            'df_residual':int(fit.df_resid),
            'not_random_site_date_GLMM':True,
            'date_fixed_model_fit':True,
            'modelbased_uncertainty_not_colony_clustered':True
        }
    except (ValueError,OverflowError) as err:
        return {'status':'NO_GO_DATE_FIXED_POISSON_FAILED',
                'failure_type':type(err).__name__,
                'failure_note':str(err)[:150],
                'date_fixed_model_fit':False}


def _date_loo(rows):
    all_dates=sorted({r['date'] for r in rows})
    values=[]
    failures=[]
    for date in all_dates:
        try:
            z=conditional_poisson(
                [r for r in rows if r['date']!=date],
                ('log_wind','relative_tke')
            )
            values.append(z['predictors']['log_wind']['beta'])
        except ValueError as exc:
            failures.append(type(exc).__name__+':'+str(exc)[:90])
    return {
       'dates_removed':len(all_dates),
       'successful_date_omissions':len(values),
       'failed_date_omissions':len(failures),
       'min_logwind_beta':min(values) if values else None,
       'max_logwind_beta':max(values) if values else None,
       'positive_count':sum(x>0 for x in values),
       'not_independent_date_level_95pct_ci':True,
       'no_day_effect_model_fitted_by_LOO':True,
    }


def analyze(rows,stage36,original_archive_sha256=None):
    if not isinstance(stage36,dict) or stage36.get('status')!=(
        'CRALL_REAL_SESSION_SITE_CONDITIONAL_POISSON_REFIT_WITH_LIMITS'):
        raise ValueError('NO_GO_PREVIOUS_REFIT_NOT_SOURCE_VERIFIED')
    if original_archive_sha256 != STAGE36_SHA:
        raise ValueError('NO_GO_ORIGINAL_ZENODO_ARCHIVE_SHA_NOT_VERIFIED')
    if len(rows)!=70 or len({r['site'] for r in rows})!=9 or (
       len({r['date'] for r in rows})!=29) or sum(r['count'] for r in rows)!=409:
        raise ValueError('NO_GO_NOT_ORIGINAL_CRALL_SESSION_GRAIN')
    beta=stage36['primary_site_conditional_poisson']['predictors']['log_wind']['beta']
    result={
       'status':'ORIGINAL_CRALL_70_SESSION_DAY_AND_CLUSTER_SENSITIVITY_AUDITED',
       'source':'10.5281/zenodo.3743898',
       'archive_sha256_expected':STAGE36_SHA,
       'n_20minute_sessions':len(rows),'n_sites':9,'n_dates':29,
       'n_original_orchid_bee_visits':409,
       'source_scent_on_sessions':70,'source_scent_off_sessions':0,
       'site_date_two_way_sandwich':_multicluster_robust(rows,beta),
       'site_plus_date_fixed_poisson':_date_fixed(rows,beta),
       'leave_one_date_out':_date_loo(rows),
       'original_author_site_date_random_intercept_GLMM_fitted':False,
       'no_wind_causal_effect':True,
       'no_wind_by_scent_on_off_interaction_tested':True,
       'no_actual_flower_landing_or_pollen_or_seeds_measured':True,
       'no_original_author_source_data_redistributed':True
    }
    return result


def main():
    dest=Path('stage37_original_robustness_receipts')
    dest.mkdir(parents=True,exist_ok=True)
    source_previous=Path('../floral_wind_refit_stage36/stage36_refit_receipts/stage36_source_locked_within_site_poisson.json')
    blob=get_source()
    digest=hashlib.sha256(blob).hexdigest()
    if not source_previous.exists():
        # Standalone in Stage37, recreate with same original source and
        # unchanged Stage36 frozen data pipeline, not hand-entered effects.
        from conditional_site_poisson import fitted_source_refit
        original=fitted_source_refit(blob)
    else:
        original=json.loads(source_previous.read_text(encoding='utf8'))
    rows=read_original_session_records(blob)
    result=analyze(rows,original,original_archive_sha256=digest)
    output=dest/'stage37_site_date_robustness.json'
    output.write_text(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+'\n',
                      encoding='utf8')
    print(json.dumps(result,sort_keys=True,allow_nan=False))


if __name__=='__main__':
    main()
