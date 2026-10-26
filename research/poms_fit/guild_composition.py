"""Exploratory within-census guild-composition × wind contrasts in UK PoMS FIT.

POST-HOC (after Stage 3 count-rate results were inspected), observational.
Only 1-km structured original surveys are considered. Pairwise fractions
condition on observing >=1 of the two focal guilds in a given 10-min focal-
flower FIT. No individual animals, simultaneous flower choices or causal
species-species interaction are identified by these contrasts.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import warnings
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import patsy
import statsmodels.api as sm

from stage3_full_profile import TABLES
from fit_associations import (
    SOURCE_DATA_SHA256, WIND, prepare, read_source
)

COMPARATORS = ('hoverflies', 'other_flies', 'butterflies_moths')
BASELINE = 'Leaves still/moving occasionally'

def _design_formula():
    return (
        "C(wind_speed, Treatment(reference='Leaves still/moving occasionally'))"
        " + log_flower_units + C(floral_unit) + C(target_flower_corrected)"
        " + C(year) + C(sunshine)"
        " + bs(day_of_year, df=4, degree=3) + C(location_code)"
    )

def _wind_test(model, names):
    if len(names) != 2:
        return {'status': 'wind_design_unidentified', 'terms_found': len(names)}
    r = np.zeros((2, len(model.params)), dtype=float)
    for i, name in enumerate(names):
        r[i, model.params.index.get_loc(name)] = 1
    try:
        s = model.wald_test(r, scalar=True)
        out = {'status': 'ok', 'chi2': float(s.statistic), 'df': 2,
               'p': float(s.pvalue)}
        if not all(np.isfinite(v) for v in (out['chi2'], out['p'])):
            return {'status': 'nonfinite_joint_wald'}
        return out
    except Exception as exc:
        return {'status': 'joint_wald_failed', 'error': str(exc)}

def fit_guild_pair(all_surveys: pd.DataFrame, comparator: str):
    if comparator not in COMPARATORS:
        raise ValueError('unregistered post-hoc guild contrast')
    required = {'bumblebees', comparator, 'location_code'}
    if not required <= set(all_surveys):
        raise ValueError('missing guild or site fields')
    # prepare has already validated all_insects_total source values, zero visits,
    # wind/flower/date categories and positive floral abundance.
    data = all_surveys.copy()
    for group in ('bumblebees', comparator):
        data[group] = pd.to_numeric(data[group], errors='coerce')
        if (data[group].dropna() < 0).any() or (data[group].dropna() % 1 != 0).any():
            raise ValueError('invalid guild count')
    pair = data['bumblebees'].fillna(0) + data[comparator].fillna(0)
    valid_counts = data[['bumblebees', comparator]].notna().all(axis=1)
    eligible = valid_counts & pair.gt(0)
    d = data.loc[eligible].copy()
    n_all = len(data)
    result = {
        'comparator': comparator, 'focal':'bumblebees',
        'status':'not_run', 'all_valid_source_surveys': n_all,
        'pair_observed_surveys': len(d),
        'pair_absent_surveys_excluded': int((valid_counts & ~pair.gt(0)).sum()),
        'pair_missing_surveys_excluded': int((~valid_counts).sum()),
        'focal_visit_total': int(d['bumblebees'].sum()),
        'comparator_visit_total': int(d[comparator].sum()),
        'site_clusters': int(d.location_code.nunique()),
        'claim_boundary':'posthoc within-census relative composition conditional on pair detection, not causal sorting, individual behavior or sensory routeability',
        'design_formula':_design_formula()
    }
    if len(d) < 100 or d.location_code.nunique() < 15:
        result['status'] = 'insufficient_sample'
        return result
    try:
        X = patsy.dmatrix(_design_formula(), d, return_type='dataframe')
        if len(X) != len(d):
            raise ValueError('design matrix silently dropped visits')
        # Aggregated binomial *paired counts* avoid expanding individual
        # insects as independent Bernoulli rows.
        y = np.column_stack([d['bumblebees'].to_numpy(dtype=int),
                             d[comparator].to_numpy(dtype=int)])
        with warnings.catch_warnings(record=True) as warn:
            warnings.simplefilter('always')
            model = sm.GLM(y, X, family=sm.families.Binomial()).fit(
                maxiter=160, cov_type='cluster',
                cov_kwds={'groups': d.location_code.astype(str).to_numpy()}
            )
        result['fit_warnings'] = [str(w.message) for w in warn][-8:]
        result['converged'] = bool(model.converged)
        result['design_columns'] = int(X.shape[1])
        result['design_matrix_rank'] = int(np.linalg.matrix_rank(X.to_numpy()))
        result['dispersion_Pearson_over_df'] = float(model.pearson_chi2/model.df_resid)
        wind = [n for n in model.params.index if n.startswith('C(wind_speed')]
        if result['design_matrix_rank'] < result['design_columns']:
            result['status'] = 'design_rank_deficient'
            return result
        ci = model.conf_int()
        if len(wind)!=2 or not np.isfinite(ci.loc[wind].to_numpy()).all():
            result['status']='wind_robust_ci_nonidentifiable'
            return result
        if np.max(np.abs(ci.loc[wind].to_numpy())) > 100:
            result['status']='wind_robust_ci_unbounded'
            return result
        result['status'] = 'fitted'
        result['wind_joint_wald'] = _wind_test(model,wind)
        result['wind_terms'] = {
            name:{'OR_bumble_to_comparator': float(np.exp(model.params[name])),
                  'CI95_low':float(np.exp(ci.loc[name,0])),
                  'CI95_high':float(np.exp(ci.loc[name,1])),
                  'cluster_p':float(model.pvalues[name])}
            for name in wind
        }
        strong = [name for name in wind if 'Leaves moving strongly' in name]
        if len(strong) != 1:
            result['status']='no_strong_wind_coefficient'
            return result
        result['primary_strong_term']=strong[0]
        result['strong_OR']=result['wind_terms'][strong[0]]['OR_bumble_to_comparator']
        result['strong_p']=result['wind_terms'][strong[0]]['cluster_p']
        return result
    except Exception as exc:
        result['status']='model_failure'
        result['error']=str(exc)
        return result

def holm_adjust(pvalues: dict):
    """Holm familywise adjusted p for a fixed family; missing -> 1.0."""
    if not pvalues:
        return {}
    names=list(pvalues)
    values=np.array([1 if pvalues[n] is None else float(pvalues[n]) for n in names])
    if (values < 0).any() or (values > 1).any() or not np.isfinite(values).all():
        raise ValueError('invalid p values')
    order=np.argsort(values,kind='stable')
    m=len(values)
    adjusted=np.empty(m,dtype=float)
    previous=0.0
    for j,i in enumerate(order):
        previous=max(previous, min(1.0,(m-j)*values[i]))
        adjusted[i]=previous
    return {k:float(adjusted[i]) for i,k in enumerate(names)}

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument('--out',default='stage3_poms_audit')
    a=p.parse_args(argv)
    out=Path(a.out)
    with zipfile.ZipFile(out/'poms_fit_2017_2023_source.zip') as archive:
        raw=archive.read(TABLES['one_km'])
    source_hash=hashlib.sha256(raw).hexdigest()
    if source_hash!=SOURCE_DATA_SHA256['one_km']:
        raise ValueError('source member hash mismatch')
    original,source_encoding=read_source(raw)
    surveys,flow=prepare(original,'one_km','all_insects_total')
    results=[fit_guild_pair(surveys,c) for c in COMPARATORS]
    adjusted=holm_adjust({x['comparator']:x.get('strong_p') for x in results})
    for x in results:
        x['strong_p_holm_family3']=adjusted[x['comparator']]
    report={'status':'exploratory_posthoc',
            'source_hash_one_km_csv':source_hash,
            'original_1km_rows':len(original),
            'overall_eligible_surveys':len(surveys),
            'total_eligibility':flow,
            'comparators_predeclared_to_stage3b':list(COMPARATORS),
            'total_fitted_pairs':sum(x['status']=='fitted' for x in results),
            'failed_pairs':[x['comparator'] for x in results if x['status']!='fitted'],
            'pairs':results,
            'scientific_boundary':'conditional on >=1 visit in a guild pair to one selected target flower; not an independent zero-inclusive test or evidence for causal interspecific interaction/routeability'}
    (out/'guild_composition_results.json').write_text(
        json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False))
    for x in results:
        print('POMS_GUILD_PAIR '+json.dumps(x,allow_nan=False),flush=True)
    print('POMS_GUILD_COMPOSITION_COMPLETE',flush=True)
    return report

if __name__=='__main__':
    main()
