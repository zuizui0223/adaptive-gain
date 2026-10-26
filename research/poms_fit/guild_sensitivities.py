"""Stage 3c post-hoc falsification tests for the selected wind/guild association.

This stress test was designed AFTER the structured PoMS FIT Stage 3b
bumblebee-to-other-flies odds ratio was seen. It cannot serve as
pre-registered confirmation, ecological causality, or individual choice
and does not measure wind direction.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.stats.contingency_tables import StratifiedTable

from stage3_full_profile import TABLES
from fit_associations import SOURCE_DATA_SHA256, WIND, prepare, read_source
from guild_composition import fit_guild_pair

BUMBLE='bumblebees'
FLIES='other_flies'
CALM=WIND[0]
STRONG=WIND[2]

def trim_high_counts(eligible: pd.DataFrame):
    """Remove whole high-contribution FIT surveys without synthesizing visits."""
    pair=eligible[BUMBLE]+eligible[FLIES]
    positive=pair.loc[pair.gt(0)]
    if positive.empty:
        raise ValueError('no detected guild-pair counts')
    q99=float(np.quantile(positive.to_numpy(),0.99,method='higher'))
    retained=eligible.loc[pair.le(q99)].copy()
    return retained,{
        'rule':'remove entire original 10min survey if bumblebees + other_flies > 99th percentile of pair-positive FIT surveys',
        'q99_pair_visits':q99,
        'source_surveys':len(eligible),
        'surveys_removed':len(eligible)-len(retained),
        'bumble_visits_removed':int(eligible[BUMBLE].sum()-retained[BUMBLE].sum()),
        'other_fly_visits_removed':int(eligible[FLIES].sum()-retained[FLIES].sum())
    }

def matched_stratum_cm_h(eligible: pd.DataFrame):
    """Conservative site × year × target matched wind table, no fake zeros."""
    required={'location_code','year','target_flower_corrected','wind_speed',BUMBLE,FLIES}
    if not required <= set(eligible):
        raise ValueError('missing matched-strata fields')
    e=eligible.loc[eligible.wind_speed.isin([CALM,STRONG])].copy()
    # Exclude target pairs whose denominator is 0, NOT imputed zeros.
    e=e.loc[(e[BUMBLE]+e[FLIES])>0]
    tables=[]
    target_strata=[]
    used_sites=set()
    surveys=0
    nonzero_cells=0
    for key,g in e.groupby(['location_code','year','target_flower_corrected'],
                           observed=True,dropna=True,sort=True):
        if not {CALM,STRONG} <= set(g.wind_speed.astype(str)):
            continue
        calm=g.loc[g.wind_speed==CALM]
        strong=g.loc[g.wind_speed==STRONG]
        table=np.array([[strong[BUMBLE].sum(),strong[FLIES].sum()],
                        [calm[BUMBLE].sum(),calm[FLIES].sum()]],dtype=float)
        if table[0].sum()==0 or table[1].sum()==0:
            continue
        tables.append(table)
        target_strata.append(tuple(str(x) for x in key))
        used_sites.add(str(key[0]))
        surveys+=len(g)
        nonzero_cells+=int((table==0).sum())
    result={
        'status':'not_fit',
        'stratum':'location_code × compiled year × corrected target flower',
        'contrast':'strong vs calm within strata',
        'pair':'bumblebees vs other_flies',
        'pair-positive_surveys_in_complete_matched_strata':surveys,
        'matched_strata':len(tables),
        'matched_sites':len(used_sites),
        'aggregated_zero_cells':nonzero_cells,
        'conditioning':'observed guild pair >0; other wind category discarded',
        'claim_boundary':'exploratory descriptive CMH; individual insect visits within same site/survey are not independent and season within a matched year remains uncontrolled',
    }
    if len(tables)<15 or len(used_sites)<10:
        result['status']='insufficient_matched_coverage'
        return result
    try:
        # Some sparse tables contain 0 cells; shift_zeros=True documents
        # a 0.5 continuity correction rather than manufacturing 0 visits.
        model=StratifiedTable(tables,shift_zeros=True)
        odds=float(model.oddsratio_pooled)
        lo,hi=model.oddsratio_pooled_confint()
        p=float(model.test_null_odds().pvalue)
        if not np.isfinite([odds,lo,hi,p]).all():
            result['status']='nonfinite_statistic'
            return result
        result.update(status='computed_descriptive_only',
                      pooled_OR_strong_bumble_to_fly=odds,
                      naive_95ci_low=float(lo),naive_95ci_high=float(hi),
                      naive_asymptotic_p=p,
                      explicit_note='CMH precision assumes within-cell independent insect counts; not a valid site-clustered p-value. For sign/magnitude sensitivity only.')
    except Exception as exc:
        result.update(status='failed',error=str(exc))
    return result

def run(archive_path: Path,out_path: Path):
    repo={'public':{},'one_km':{}}
    with zipfile.ZipFile(archive_path) as z:
        for surface in repo:
            raw=z.read(TABLES[surface])
            sha=hashlib.sha256(raw).hexdigest()
            if sha!=SOURCE_DATA_SHA256[surface]:
                raise ValueError(f'original CSV digest changed: {surface}')
            df,code=read_source(raw)
            eligible,flow=prepare(df,surface)
            repo[surface]={'encoding':code,'original_sha256':sha,
                           'original_surveys':len(df),'eligible_surveys':len(eligible),
                           'flow':flow,'frame':eligible}
    public=fit_guild_pair(repo['public']['frame'],FLIES,surface='public')
    trim,trim_receipt=trim_high_counts(repo['one_km']['frame'])
    structured_trim=fit_guild_pair(trim,FLIES,surface='one_km')
    matched=matched_stratum_cm_h(repo['one_km']['frame'])
    report={
        'status':'posthoc_selected_positive_signal_stress_test',
        'source_digests':{x:repo[x]['original_sha256'] for x in repo},
        'public_mode_transfer':public,
        'structured_99pct_trim':{'result':structured_trim,'removal':trim_receipt},
        'structured_matched_strata':matched,
        'not_independent_programmes':True,
        'claim_boundary':'ecological detection-composition association only, NOT wind-caused niche sorting, interspecific competition or sensory routeability'
    }
    out_path.parent.mkdir(parents=True,exist_ok=True)
    out_path.write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False))
    print('POMS_GUILD_STRESS_TEST '+json.dumps(report,ensure_ascii=False,allow_nan=False),flush=True)
    print('POMS_GUILD_STRESS_COMPLETE',flush=True)
    return report

def main(argv=None):
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',default='stage3_poms_audit')
    args=ap.parse_args(argv)
    out=Path(args.out)
    run(out/'poms_fit_2017_2023_source.zip',out/'guild_stress_tests.json')

if __name__=='__main__':
    main()
