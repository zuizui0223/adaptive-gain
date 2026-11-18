"""Stage82: real 194 age-spectra × observed bee null-score network join.

Match ERA5 historical 10m DAILY maximum GUST for the original EuPP source
calendar year/month. The weather cohort was frozen at Stage79I using petal
width and study characteristics before recording Bombus outcomes, not
reselected to achieve a favorable spectral age-change sign.
This is NOT wind at bee landing or floral scent plume turbulence.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
import numpy as np,pandas as pd
import statsmodels.formula.api as smf

GUST_SHA='1188e639593437f07c8eaa559730d845269d9b1d2abca52917b7bbd6c2315f90'
GUILD_SHA='ddc3d56e536b34e7a31f78f0a4f9013739bc732d69c9d294151dec303bcb86ca'
GUST='original_ERA5_fraction_days_10m_gust_ge_15_ms'
T='original_ERA5_period_daily_T_mean_C'
P='original_ERA5_period_precip_mm_per_day'
I='source_I_local_null_fisher_information'
S='source_null_ratio_U_over_I_not_fitted_beta'


def read_file(path,expected):
    b=Path(path).read_bytes()
    if hashlib.sha256(b).hexdigest()!=expected:raise ValueError('STAGE82_GENUINE_PREVIOUS_SOURCE_CHANGED')
    return pd.read_csv(path)


def join(source_weather,source_scores):
    if len(source_weather)!=151 or len(source_scores)!=194:
        raise ValueError('STAGE82_NOT_151_WEATHER_194_OBSERVED_VISITOR_SCORES')
    for label,df,col in [('weather',source_weather,'Year'),('score',source_scores,'Year_from_original_date')]:
        if df.duplicated(['Study_id','Network_id',col]).any():
            raise ValueError('STAGE82_DUPLICATED_ORIGINAL_NETWORK_'+label)
    w=source_weather.copy()
    for name in [T,P]:
        x=pd.to_numeric(w[name],errors='raise')
        w['z_'+name]=(x-x.mean())/x.std()
    w['gust_per_10pp']=pd.to_numeric(w[GUST],errors='raise')*10
    keys=['Study_id','Network_id']
    x=source_scores.merge(w,how='inner',left_on=keys+['Year_from_original_date'],right_on=keys+['Year'],validate='one_to_one')
    if len(x)!=36 or x.Study_id.nunique()!=17 or x.source_publication.nunique()!=16:
        raise ValueError('STAGE82_ORIGINAL_36_NETWORK_17_IDS_16_PUBLICATION_OVERLAP_CHANGED')
    varied=x.groupby('source_publication')['gust_per_10pp'].agg(['size','min','max'])
    n_var=int(((varied['size']>=2)&((varied['max']-varied['min'])>.1)).sum())
    if n_var!=7:raise ValueError('STAGE82_SOURCE_7_PUBLICATIONS_WITH_NONTRIVIAL_WIND_VAR_CHANGED')
    bypub=x.groupby('source_publication')[I].sum()
    source_share=bypub/bypub.sum()
    return x,{'source_weather_networks_preselected_by_size_before_guild':151,
              'matched_age_spectra_and_strict_bees_gust_networks':len(x),
              'true_source_publications':int(x.source_publication.nunique()),
              'true_original_source_study_IDs':int(x.Study_id.nunique()),
              'publications_with_1pp_within_paper_gust15_variation':n_var,
              'source_information_effective_publication_count':float(1/(source_share.pow(2).sum())),
              'source_largest_paper_fisher_information_share':float(source_share.max()),
              'source_gust_not_actual_flower_flight_hour_or_odor_turbulence':True}


def fit_wls(x,equal_paper=False):
    z=x.copy()
    z['weight']=z[I]
    if equal_paper:z['weight']=z['weight']/z.groupby('source_publication')[I].transform('sum')
    formula=(S+' ~ gust_per_10pp + z_'+T+' + z_'+P+' + C(Study_id)')
    m=smf.wls(formula,z,weights=z['weight']).fit()
    if np.linalg.matrix_rank(m.model.exog)!=len(m.params):
        raise ValueError('STAGE82_UNIDENTIFIED_STUDY_FIXED_EFFECT_DESIGN')
    robust=m.get_robustcov_results(cov_type='cluster',groups=z.source_publication)
    idx=list(m.params.index).index('gust_per_10pp')
    est=float(robust.params[idx]);interval=[float(q) for q in robust.conf_int()[idx]]
    leave=[]
    for pub in sorted(z.source_publication.unique()):
        zz=z.loc[z.source_publication!=pub]
        mm=smf.wls(formula,zz,weights=zz['weight']).fit()
        if np.linalg.matrix_rank(mm.model.exog)!=len(mm.params):
            raise ValueError('STAGE82_LEAVE_ONE_PUBLICATION_RANK_LOST')
        leave.append({'excluded_original_publication':pub,'gust_slope':float(mm.params['gust_per_10pp'])})
    return {'description':'STUDY_FIXED_EFFECT_LOCAL_NULL_SCORE_RATIO_WLS_NOT_A_FITTED_BEE_ODDS_COEFFICIENT',
            'source_weights':'source_equal_publication' if equal_paper else 'original_source_null_Fisher_information',
            'original_pub_cluster_count':int(z.source_publication.nunique()),
            'slope_per_10_percentage_points_ERA5_daily_maximum_gust15':est,
            'descriptive_publication_clustered_95_interval_NOT_causal':interval,
            'original_leave_one_publication_sign_flips':int(sum(np.sign(v['gust_slope'])!=np.sign(est) for v in leave)),
            'leave_one_publication_min_max':[float(min(v['gust_slope'] for v in leave)),float(max(v['gust_slope'] for v in leave))]}


def analyze(weather,scores):
    x,identity=join(weather,scores)
    if identity['source_information_effective_publication_count']>=2:
        raise ValueError('STAGE82_UNEXPECTED_FISHER_INFORMATION_NOT_SOURCE_DOMINATED')
    a=fit_wls(x,False);b=fit_wls(x,True)
    if abs(a['slope_per_10_percentage_points_ERA5_daily_maximum_gust15']-.5997013845250239)>1e-8:
        raise ValueError('STAGE82_SOURCE_WIND_AGE_LOCAL_SLOPE_REPRODUCTION_FAILED')
    if abs(b['slope_per_10_percentage_points_ERA5_daily_maximum_gust15']-6.956285479611987)>1e-8:
        raise ValueError('STAGE82_SOURCE_STUDY_REWEIGHTED_WIND_SLOPE_REPRODUCTION_FAILED')
    return {'schema':'stage82_194_age_ERA5_strong_gust_network_overlap_only_not_sensory_stage_effect',
            'source_support':identity,
            'information_weighted_screen':a,
            'equal_original_publication_weighted_screen':b,
            'not_an_identified_wind_age_visual_cue_or_selection_effect':True,
            'no_anemometer_measured_visitation_event_wind_or_odor_plume':True,
            'no_early_late_actual_flower_age_at_visitation':True,
            'source_age_spectra_Japan_versus_field_visitation_Europe':True,
            'effective_information_count_too_low_for_generalization':identity['source_information_effective_publication_count']<5}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--original-sizefirst-gust-exposures',type=Path,required=True)
    p.add_argument('--original-stage81c-guild-scores',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    obj=analyze(read_file(a.original_sizefirst_gust_exposures,GUST_SHA),read_file(a.original_stage81c_guild_scores,GUILD_SHA))
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(obj,sort_keys=True,indent=2)+'\n')
    print('STAGE82_ORIGINAL_ERA5_AGE_NETWORK_OVERLAP_GATES',json.dumps(obj,sort_keys=True))
if __name__=='__main__':main()
