"""Post-hoc clock, observer and flower-cover sensitivity for PoMS guild composition.

Tests one *already selected* bumblebee vs other_flies strong-wind contrast.
A fixed observed 10-minute target-flower census is not a simultaneous flower
choice, sensory architecture experiment or a causal wind intervention.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import warnings
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import patsy
import statsmodels.api as sm

from stage3_full_profile import TABLES
from fit_associations import SOURCE_DATA_SHA256, prepare, read_source
from guild_composition import _design_formula

PAIR=('bumblebees','other_flies')
TIME_LABELS=('before_10','10_to_12','12_to_14','14_to_16','16_or_later')

def parse_clock(series: pd.Series):
    """Only recognize explicit clock strings, without inventing unknown hours."""
    source=series.astype('string').str.strip()
    # A small, documented grammar; retain invalid raw tokens as diagnostics.
    normalized=(source.str.upper()
                .str.replace(r'\s+', ' ', regex=True)
                .str.replace('A.M.','AM',regex=False)
                .str.replace('P.M.','PM',regex=False))
    parts=normalized.str.extract(
        r'^(?P<hour>\d{1,2}):(?P<minute>\d{2})(?::(?P<second>\d{2}))?\s*(?P<meridiem>AM|PM)?$')
    h=pd.to_numeric(parts['hour'],errors='coerce')
    minutes=pd.to_numeric(parts['minute'],errors='coerce')
    sec=pd.to_numeric(parts['second'],errors='coerce').fillna(0)
    amp=parts['meridiem']
    valid=(h.notna()&minutes.notna()&(minutes<=59)&(sec<=59)
           &((amp.isna()&(h<=23))|(amp.notna()&h.between(1,12))))
    h24=h.copy()
    pm=valid&amp.eq('PM').fillna(False)
    am=valid&amp.eq('AM').fillna(False)
    h24.loc[pm]=(h.loc[pm]%12)+12
    h24.loc[am]=(h.loc[am]%12)
    clock=h24+(minutes/60)+(sec/3600)
    clock.loc[~valid]=np.nan
    categories=pd.cut(clock,[-np.inf,10,12,14,16,np.inf],
                      labels=list(TIME_LABELS),right=False)
    bad=source.loc[~valid].dropna()
    summary={'observations':len(series),'parsed':int(valid.sum()),
             'unparseable_or_missing':int((~valid).sum()),
             'parsed_fraction':float(valid.mean()),
             'invalid_format_counts':{
                str(k):int(v) for k,v in bad.value_counts().head(12).items()
             },
             'time_bin_counts':{
                str(k):int(v) for k,v in categories.value_counts(dropna=False).items()
             }}
    return categories, summary


def run_adjusted(survey: pd.DataFrame,surface:str):
    cluster=('location_code' if surface=='one_km' else 'x1km_square')
    required={'count_start_time','recorder_type','flower_cover',cluster,*PAIR}
    if not required<=set(survey.columns):
        raise ValueError(f'missing source columns: {required-set(survey.columns)}')
    data=survey.copy()
    bins,time_summary=parse_clock(data.count_start_time)
    data['time_bin']=bins
    result={'status':'not_run','surface':surface,
            'original_stage3_eligible_surveys':len(data),
            'clock_format_audit':time_summary,
            'claim_boundary':'POSTHOC adjustment for survey clock, recorder_type and focal flower-cover on within-pair composition, not ecological causal wind effect'}
    if time_summary['parsed_fraction']<.95:
        result['status']='clock_format_unqualified'
        return result
    positive=(data[PAIR[0]]+data[PAIR[1]]).gt(0)
    included=positive&data.time_bin.notna()
    data=data.loc[included].copy()
    result['pair_positive_surveys_with_valid_clock']=len(data)
    result['excluded_pair_absence']=int((~positive).sum())
    result['excluded_invalid_clock_among_pair_positive']=int((positive&~included).sum())
    result['site_clusters']=int(data[cluster].nunique())
    if len(data)<100 or data[cluster].nunique()<15:
        result['status']='insufficient_coverage'
        return result
    data['recorder_type_clean']=(data.recorder_type.fillna('Not reported')
                                 .astype(str).replace({'':'Not reported'}))
    data['flower_cover_clean']=(data.flower_cover.fillna('Not recorded')
                               .astype(str).replace({'':'Not recorded'}))
    f=_design_formula(surface)+" + C(time_bin) + C(recorder_type_clean) + C(flower_cover_clean)"
    result['formula']=f
    try:
        X=patsy.dmatrix(f,data,return_type='dataframe')
        if len(X)!=len(data):
            result['status']='unexpected_dropped_rows'
            return result
        result['design_columns']=len(X.columns)
        result['design_rank']=int(np.linalg.matrix_rank(X.to_numpy()))
        if result['design_rank']<result['design_columns']:
            result['status']='rank_deficient'
            return result
        Y=np.column_stack([data[PAIR[0]].to_numpy(dtype=int),
                           data[PAIR[1]].to_numpy(dtype=int)])
        with warnings.catch_warnings(record=True) as warn:
            warnings.simplefilter('always')
            m=sm.GLM(Y,X,family=sm.families.Binomial()).fit(
                maxiter=160,cov_type='cluster',
                cov_kwds={'groups':data[cluster].astype(str).to_numpy()})
        result['converged']=bool(m.converged)
        result['warnings']=[str(w.message) for w in warn][-8:]
        result['pearson_overdispersion']=float(m.pearson_chi2/m.df_resid)
        wind=[x for x in m.params.index if x.startswith('C(wind_speed')]
        strong=[x for x in wind if 'Leaves moving strongly' in x]
        if len(wind)!=2 or len(strong)!=1:
            result['status']='wind_model_unidentified'
            return result
        ci=m.conf_int().loc[wind].to_numpy()
        if not np.isfinite(ci).all() or np.max(np.abs(ci))>100:
            result['status']='invalid_robust_wind_ci'
            return result
        k=strong[0];bounds=m.conf_int().loc[k]
        result.update(status='fitted',strong_wind_OR=float(np.exp(m.params[k])),
                      strong_wind_ci95=[float(np.exp(bounds.iloc[0])),
                                        float(np.exp(bounds.iloc[1]))],
                      strong_wind_cluster_p=float(m.pvalues[k]))
    except Exception as exc:
        result.update(status='model_failed',error=str(exc))
    return result

def main(argv=None):
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',default='stage3_poms_audit')
    a=parser.parse_args(argv)
    out=Path(a.out)
    output={'status':'posthoc_stage3d',
            'source_hashes':{},
            'sensitivity':{}}
    with zipfile.ZipFile(out/'poms_fit_2017_2023_source.zip') as z:
        for surface in ('one_km','public'):
            raw=z.read(TABLES[surface])
            digest=hashlib.sha256(raw).hexdigest()
            if digest!=SOURCE_DATA_SHA256[surface]:
                raise ValueError(f'source SHA-256 mismatch: {surface}')
            df,encoding=read_source(raw)
            valid,flow=prepare(df,surface)
            output['source_hashes'][surface]=digest
            res=run_adjusted(valid,surface)
            res['source_original_rows']=len(df)
            res['source_encoding']=encoding
            res['baseline_eligibility']=flow
            output['sensitivity'][surface]=res
    (out/'guild_clock_observer_sensitivity.json').write_text(
        json.dumps(output,indent=2,ensure_ascii=False,allow_nan=False))
    for surface,res in output['sensitivity'].items():
        print('POMS_GUILD_CLOCK '+json.dumps(res,ensure_ascii=False,allow_nan=False),
              flush=True)
    print('POMS_GUILD_CLOCK_COMPLETE',flush=True)

if __name__=='__main__':
    main()
