"""Stage80L: original EuPPPollNet 52-publication vs 54-Study_id correction.

This reanalysis takes the pinned actual Stage79I ZIP (37 observed-network
within-source bee null scores, 151 original exposure rows). Preserve Stage79I
estimator/temperature/precipitation scaling and habitat-level fixed effects.
Change only uncertainty clustering and information weight normalization
from EuPP original Study IDs to their actual source-publication units.

EuPPPollNet DOI 10.1111/geb.70000, Methods 2.3: 52 independent studies
are represented by 54 study IDs because one study is split into IDs
23, 24 and 25 for three different habitat types.

This is descriptive WLS sensitivity, not gust-effect identification.
"""
from __future__ import annotations
import argparse,hashlib,io,json,zipfile
from pathlib import Path

ARTIFACT_SHA='d81b24bef6c01e849121cbbbf1dc085953767fc52d909f40757fc912be403b7d'
ARTIFACT_ID=14399842321
COLUMNS=('Study_id','Network_id','Year')
WIND='original_ERA5_fraction_days_10m_gust_ge_15_ms'
INFO='original_source_width_local_null_information'
SCORE='original_source_width_null_score_ratio'


def publication_id(study_id):
    """The author's known habitat split; shared surname alone is not a paper."""
    key=str(study_id).split('_',1)[0]
    if key in {'23','24','25'}:return '23_24_25_ONE_PUBLISHED_STUDY'
    return str(study_id)


def run(source_zip:Path):
    import numpy as np
    import pandas as pd
    import statsmodels.formula.api as smf
    blob=source_zip.read_bytes()
    digest=hashlib.sha256(blob).hexdigest()
    if digest!=ARTIFACT_SHA:
        raise ValueError('STAGE80L_STAGE79I_ACTUAL_ORIGINAL_ARTIFACT_DIGEST_CHANGED')
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        exp=pd.read_csv(z.open('source_original_sizefirst_ERA5_gust15_exposures.csv'))
        y=pd.read_csv(z.open('source_original_sizefirst_Bombus_width_nullscores.csv'))
    if len(exp)!=151 or len(y)!=37 or y.Study_id.nunique()!=15:
        raise ValueError('STAGE80L_ORIGINAL_151_37_15_COHORT_CHANGED')
    for tab in (exp,y):
        if tab.duplicated(list(COLUMNS)).any():
            raise ValueError('STAGE80L_DUPLICATED_ORIGINAL_NETWORK_YEAR')
    for col in (WIND,'original_ERA5_period_daily_T_mean_C','original_ERA5_period_precip_mm_per_day'):
        exp[col]=pd.to_numeric(exp[col],errors='raise')
        if not exp[col].notna().all():
            raise ValueError('STAGE80L_MISSING_SOURCE_METEO_EXPOSURE')
    # Scale the original full 151 exposures BEFORE joining the 37 bee outcomes.
    exp['z_t']=(exp.original_ERA5_period_daily_T_mean_C-exp.original_ERA5_period_daily_T_mean_C.mean())/exp.original_ERA5_period_daily_T_mean_C.std()
    exp['z_p']=(exp.original_ERA5_period_precip_mm_per_day-exp.original_ERA5_period_precip_mm_per_day.mean())/exp.original_ERA5_period_precip_mm_per_day.std()
    exp['w']=exp[WIND]*10.
    x=y.merge(exp[list(COLUMNS)+['w','z_t','z_p']],on=list(COLUMNS),how='left',validate='one_to_one',indicator=True)
    if not (x._merge=='both').all():
        raise ValueError('STAGE80L_NETWORK_JOIN_FAILED')
    x[INFO]=pd.to_numeric(x[INFO],errors='raise')
    x[SCORE]=pd.to_numeric(x[SCORE],errors='raise')
    if not np.isfinite(x[INFO]).all() or (x[INFO]<=0).any() or not np.isfinite(x[SCORE]).all():
        raise ValueError('STAGE80L_INFORMATION_OR_SCORE_INVALID')
    x['publication_id']=x.Study_id.map(publication_id)
    if x.publication_id.nunique()!=14 or not {'23_Holzschuh','25_Holzschuh'}.issubset(set(x.Study_id)):
        raise ValueError('STAGE80L_15_STUDY_IDS_DID_NOT_MAP_TO_14_SOURCE_PUBLICATIONS')
    form='original_source_width_null_score_ratio ~ w + z_t + z_p + C(Study_id)'
    def fit(weights,cluster):
        m=smf.wls(form,x,weights=weights).fit()
        if np.linalg.matrix_rank(m.model.exog)<len(m.params):
            raise ValueError('STAGE80L_STUDY_FIXED_EFFECT_DESIGN_RANK_DEFICIENT')
        r=m.get_robustcov_results(cov_type='cluster',groups=x[cluster])
        i=list(m.params.index).index('w')
        return {'source_original_study_cluster_unit':cluster,
                'slope_per_10_percentage_point_ERA5_gust15':float(r.params[i]),
                'study_cluster_95_interval_NOT_causal':[float(v) for v in r.conf_int()[i]],
                'cluster_count':int(x[cluster].nunique())}
    w=x[INFO]
    bystudy=w/x.groupby('Study_id')[INFO].transform('sum')
    bypub=w/x.groupby('publication_id')[INFO].transform('sum')
    result={
        'schema':'stage80l_true_original_37_network_publication_cluster_sensitivity',
        'source_original_stage79i_github_actions_artifact_id':ARTIFACT_ID,
        'source_original_github_artifact_zip_sha256_verified':digest,
        'source_publisher_DOI':'10.1111/geb.70000',
        'source_publisher_52_independent_studies_vs_54_study_ids_reason':'one source study split into original IDs 23,24,25 for habitat comparisons',
        'source_original_clustering_count':{
            'network_years_informative':int(len(x)),
            'study_id_labels':int(x.Study_id.nunique()),
            'source_publications':int(x.publication_id.nunique()),
            'split_study_ids_in_original_37_networks':sorted(set(x.Study_id)&{'23_Holzschuh','24_Holzschuh','25_Holzschuh'})},
        'original_15_studyID_information_weighted':fit(w,'Study_id'),
        'original_15_studyID_equal_weighted':fit(bystudy,'Study_id'),
        'corrected_14_publication_clustered_information_weighted':fit(w,'publication_id'),
        'corrected_14_publication_equal_weighted':fit(bypub,'publication_id'),
        'no_association_significance_or_causal_identification_claimed':True,
        'unequal_visit_effort_and_species_phylogeny_not_controlled':True,
        'no_measured_sensory_stage_scent_plume_landing_or_bee_fitness':True,
    }
    frac=x.groupby('publication_id')[INFO].sum()
    frac=frac/frac.sum()
    result['source_publication_information_concentration']={
        'largest_publication_fraction':float(frac.max()),
        'effective_publication_number_by_information_weights':float(1/(frac.pow(2).sum()))}
    if abs(result['original_15_studyID_information_weighted']['slope_per_10_percentage_point_ERA5_gust15']-1.4384233037722225)>1e-6:
        raise ValueError('STAGE80L_BASELINE_STAGE79I_NOT_INDEPENDENTLY_REPRODUCED')
    if abs(result['original_15_studyID_equal_weighted']['slope_per_10_percentage_point_ERA5_gust15']-.733977314521)>1e-6:
        raise ValueError('STAGE80L_STAGE79K_STUDY_EQUALLY_WEIGHTED_NOT_REPRODUCED')
    return result


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--stage79i-source-zip',type=Path,required=True)
    p.add_argument('--out',type=Path)
    args=p.parse_args()
    out=json.dumps(run(args.stage79i_source_zip),indent=2,sort_keys=True,ensure_ascii=False)+'\n'
    if args.out:
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(out,encoding='utf-8')
    else:print(out)
if __name__=='__main__':main()
