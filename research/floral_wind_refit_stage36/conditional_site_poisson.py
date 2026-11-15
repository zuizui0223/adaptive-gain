"""Stage36: original Crall 70-session within-site wind-visitation refit.

NO new bee or flower data. Source DOI 10.5281/zenodo.3743898, author's
published 2020 archive. Fetch exact original ZIP, verify declared MD5,
validate true session/count/forest/weather joins without redistributing
original rows.

PRIMARY: site-CONDITIONAL Poisson for count ~ log10(mean wind speed)
+ original relative TKE, conditioning on site total, 20-min session
exposure. This is a new sensitivity refit, NOT an exact reproduction
of author's GLMM (which has (1|site)+(1|date) random intercepts plus
forest cover200m). Site fixed effects absorb its between-site cover.

No causality, no wind x scent ON/OFF estimate, no true flower landing,
nectar guide, pollen deposition or fitness estimate.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import math
from collections import defaultdict
from pathlib import Path

from audit_original_session_design import (
    _read_rows,_finite_number,DATA_FILES,run as source_audit,
)
from zenodo_crall_original_source import (
    _fetch,_candidate_download_urls,assess_api_metadata,
    _verify_md5_if_declared,
)

META_ID=3743898
ARCHIVE_NAME='CrallEtAl_OrchidBeeWindEcology.zip'
EXPECTED_ARCHIVE_SHA256='4250cb51754e59b861f90ff7063dbbc223dd515a146809273fee055de81772af'
EXPECTED_SESSION_N=70
EXPECTED_BEE_COUNT=409
EXPECTED_SITE_N=9
EXPECTED_SCENT={'cin':67,'meth':3}
PAPER_FORMULA='count ~ log10(wind.mean) + cover200m + rel.wind.KE + (1|site) + (1|date)'
COLLECTION='Zenodo/collectionMetadata.csv'
INTEGRATED='Zenodo/integratedSpatialWindData.csv'


def get_source():
    """Fetch official published Zenodo record and verify full ZIP identity."""
    meta=json.loads(_fetch(f'https://zenodo.org/api/records/{META_ID}').decode('utf8'))
    source=assess_api_metadata(meta,META_ID)
    if meta.get('id')!=META_ID:
        raise ValueError('NO_GO_UNEXPECTED_ZENODO_VERSION')
    links=_candidate_download_urls(meta)
    if len(links)!=1:
        raise ValueError('NO_GO_AMBIGUOUS_ARCHIVE')
    filename,url,checksum,expected_length=links[0]
    if filename!=ARCHIVE_NAME:
        raise ValueError('NO_GO_UNEXPECTED_ARCHIVE_FILENAME')
    blob=_fetch(url)
    if len(blob)!=int(expected_length):
        raise ValueError('NO_GO_ARCHIVE_CHANGED_LENGTH')
    _verify_md5_if_declared(blob,checksum)
    if hashlib.sha256(blob).hexdigest()!=EXPECTED_ARCHIVE_SHA256:
        raise ValueError('NO_GO_AUTHOR_VERSION_ARCHIVE_SHA_CHANGED')
    return blob


def read_original_session_records(blob):
    if not isinstance(blob,bytes):
        raise ValueError('NO_GO_NO_RAW_AUTHOR_ARCHIVE')
    import zipfile
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        _,coll=_read_rows(z.read(COLLECTION))
        _,ints=_read_rows(z.read(INTEGRATED))
    if len(coll)!=EXPECTED_SESSION_N or len(ints)!=EXPECTED_SESSION_N:
        raise ValueError('NO_GO_ORIGINAL_SESSION_COUNT_CHANGED')
    def key(row):
        return (row['site'].strip(),row['date'].strip(),row['scent'].strip())
    a={key(row):row for row in coll}
    b={key(row):row for row in ints}
    if len(a)!=EXPECTED_SESSION_N or len(b)!=EXPECTED_SESSION_N or set(a)!=set(b):
        raise ValueError('NO_GO_SOURCE_SESSION_JOIN_OR_DUPLICATION')
    sessions=[]
    for ky in sorted(a):
        x=a[ky]
        y=b[ky]
        try:
            count=int(float(x['count']))
            original_integrated_count=int(float(y['count']))
        except (ValueError,TypeError):
            raise ValueError('NO_GO_ORIGINAL_COUNT_NOT_INTEGER')
        if str(count)!=str(x['count']).strip() and not str(x['count']).strip().endswith('.0'):
            raise ValueError('NO_GO_NONINTEGER_COUNT')
        if count<0 or count!=original_integrated_count:
            raise ValueError('NO_GO_ORIGINAL_CROSS_SOURCE_COUNT_DISAGREEMENT')
        if y['keep'].strip()!='1':
            raise ValueError('NO_GO_AUTHOR_KEEP_POLICY_NOT_RESOLVED')
        if x['start.time'].strip()!=y['start.time'].strip():
            raise ValueError('NO_GO_AUTHOR_START_TIME_DISAGREEMENT')
        wind=_finite_number(x['wind.mean'])
        tke=_finite_number(x['rel.wind.KE'])
        cover=_finite_number(y['cover200m'])
        if (wind is None or wind<=0 or not math.isfinite(wind)
            or tke is None or not math.isfinite(tke)
            or cover is None or not 0<=cover<=1):
            raise ValueError('NO_GO_MISSING_WIND_TKE_OR_COVER')
        wind2=_finite_number(y['wind.mean'])
        if wind2 is None or abs(wind-wind2)>0.0002:
            raise ValueError('NO_GO_ORIGINAL_WIND_CROSS_SOURCE_MISMATCH')
        if x['scent'].strip() not in EXPECTED_SCENT:
            raise ValueError('NO_GO_ORIGINAL_SCENT_UNEXPECTED')
        sessions.append({
            'site':ky[0],
            'date':ky[1],
            'scent':ky[2],
            'count':count,
            'wind':wind,
            'log_wind':math.log10(wind),
            'relative_tke':tke,
            'cover200m':cover,
        })
    if sum(r['count'] for r in sessions)!=EXPECTED_BEE_COUNT:
        raise ValueError('NO_GO_409_ORIGINAL_BEE_COUNT_NOT_REPRODUCED')
    if len({r['site'] for r in sessions})!=EXPECTED_SITE_N:
        raise ValueError('NO_GO_SOURCE_SITE_COUNT_CHANGED')
    cnt={x:sum(r['scent']==x for r in sessions) for x in EXPECTED_SCENT}
    if cnt!=EXPECTED_SCENT:
        raise ValueError('NO_GO_SOURCE_SCENT_DISTRIBUTION_CHANGED')
    return sessions


def _solve_linear(a,b):
    """Gaussian elimination with partial pivoting, no hidden ridge."""
    n=len(b)
    if len(a)!=n or any(len(row)!=n for row in a):
        raise ValueError('NO_GO_BAD_LINEAR_SYSTEM')
    m=[list(map(float,a[i]))+[float(b[i])] for i in range(n)]
    for j in range(n):
        pivot=max(range(j,n),key=lambda i:abs(m[i][j]))
        if abs(m[pivot][j])<1e-11:
            raise ValueError('NO_GO_SINGULAR_CONDITIONAL_INFORMATION')
        m[pivot],m[j]=m[j],m[pivot]
        val=m[j][j]
        for k in range(j,n+1):m[j][k]/=val
        for i in range(n):
            if i!=j:
                v=m[i][j]
                if v:
                    for k in range(j,n+1):m[i][k]-=v*m[j][k]
    return [m[i][-1] for i in range(n)]


def _inverse(a):
    n=len(a)
    cols=[_solve_linear(a,[int(i==j) for i in range(n)]) for j in range(n)]
    return [[cols[j][i] for j in range(n)] for i in range(n)]


def _sites(rows,predictors):
    sites=defaultdict(list)
    for row in rows:
        if row['count']<0 or not isinstance(row['count'],int):
            raise ValueError('NO_GO_INVALID_ORIGINAL_VISITATION_COUNT')
        site=row['site']
        xs=[]
        for v in predictors:
            x=row.get(v)
            if not isinstance(x,(int,float)) or not math.isfinite(x):
                raise ValueError('NO_GO_MISSING_PREDICTOR_'+v)
            xs.append(float(x))
        sites[site].append((row['count'],xs))
    if len(sites)<3:
        raise ValueError('NO_GO_TOO_FEW_INDEPENDENT_SITES')
    return sites


def conditional_poisson(rows,predictors=('log_wind','relative_tke')):
    """True conditional site-FE likelihood, not a Poisson GLMM with random date."""
    predictors=tuple(predictors)
    if not predictors or len(set(predictors))!=len(predictors):
        raise ValueError('NO_GO_INVALID_PREDICTOR_SET')
    sites=_sites(rows,predictors)
    n=len(rows)
    dim=len(predictors)
    groups=[]
    for site in sorted(sites):
        values=sites[site]
        total=sum(y for y,x in values)
        if total==0:continue
        if len(values)<2:continue
        means=[sum(x[j] for y,x in values)/len(values) for j in range(dim)]
        centered=[(y,[x[j]-means[j] for j in range(dim)]) for y,x in values]
        groups.append((site,total,centered))
    if len(groups)<3:
        raise ValueError('NO_GO_TOO_FEW_INFORMATIVE_SITES')

    def objective(beta):
        likelihood=0.
        grad=[0.]*dim
        hess=[[0.]*dim for _ in range(dim)]
        expected=[]

        for site,total,observed in groups:
            eta=[sum(beta[j]*x[j] for j in range(dim)) for y,x in observed]
            maximum=max(eta)
            ww=[math.exp(e-maximum) for e in eta]
            scale=sum(ww)
            pp=[v/scale for v in ww]
            mu=[sum(p*x[j] for p,(y,x) in zip(pp,observed)) for j in range(dim)]
            likelihood+=sum(y*e for (y,x),e in zip(observed,eta))
            likelihood-=total*(maximum+math.log(scale))
            for j in range(dim):
                grad[j]+=sum(y*x[j] for y,x in observed)-total*mu[j]
                for k in range(dim):
                    cov=sum(p*x[j]*x[k] for p,(y,x) in zip(pp,observed))-mu[j]*mu[k]
                    hess[j][k]+=total*cov
            expected.extend((site,y,total*p) for p,(y,x) in zip(pp,observed))
        return likelihood,grad,hess,expected

    beta=[0.]*dim
    convergence=False
    iterations=0
    for it in range(90):
        iterations=it+1
        old,grad,H,_=objective(beta)
        if max(abs(g) for g in grad)<1e-9:
            convergence=True
            break
        step=_solve_linear(H,grad)
        fac=1.
        while fac>=2**-20:
            candidate=[b+fac*z for b,z in zip(beta,step)]
            if objective(candidate)[0]>=old-1e-10:
                beta=candidate
                break
            fac*=.5
        if fac<2**-20:
            raise ValueError('NO_GO_CONDITIONAL_POISSON_LINE_SEARCH')
        if max(abs(fac*z) for z in step)<1e-11:
            convergence=True
            break
    if not convergence:
        raise ValueError('NO_GO_CONDITIONAL_POISSON_NO_CONVERGENCE')

    likelihood,grad,H,expected=objective(beta)
    inv=_inverse(H)
    residual=sum(((y-mu)**2)/mu for site,y,mu in expected if mu>0)
    df=len(expected)-len(groups)-dim
    eta={p:{
         'beta':beta[j],
         'modelbased_se':math.sqrt(inv[j][j]) if inv[j][j]>=0 else None,
         'modelbased_95ci':[beta[j]-1.96*math.sqrt(inv[j][j]),
                            beta[j]+1.96*math.sqrt(inv[j][j])],
        } for j,p in enumerate(predictors)}
    wind=eta.get('log_wind')
    if wind:
        d=math.log10(2)
        wind['within_site_rate_ratio_per_wind_doubling']=math.exp(wind['beta']*d)
        wind['modelbased_95ci_IRR_wind_doubling']=[
            math.exp(v*d) for v in wind['modelbased_95ci']]
    return {
        'status':'CONDITIONAL_POISSON_SITE_FIXED_REFIT_NOT_ORIGINAL_GLMM',
        'specification':'condition on each site total; independent Poisson sessions; logged wind and original relative TKE; dates NOT modeled as random intercept',
        'predictors':eta,
        'n_original_session_rows_supplied':n,
        'n_sites_supplied':len(sites),
        'n_informative_sites':len(groups),
        'n_conditioned_sessions':len(expected),
        'total_visits':sum(y for site,y,mu in expected),
        'log_likelihood_without_constant':likelihood,
        'pearson_deviance_overdispersion_ratio':residual/df if df>0 else None,
        'modelbased_se_not_site_cluster_robust':True,
        'date_random_effect_not_fitted':True,
        'original_forest_cover_absorbed_by_site_fixed_strata':True,
        'not_a_causal_wind_experiment':True,
        'not_wind_by_flower_scent_on_off_interaction':True
    }


def pearson_between_site(rows):
    """Between-site site-mean descriptive correlation, not a Poisson test."""
    sites=defaultdict(list)
    for r in rows:sites[r['site']].append(r)
    values=[]
    for site,obs in sorted(sites.items()):
        values.append((sum(x['log_wind'] for x in obs)/len(obs),
                       sum(x['count'] for x in obs)/len(obs)))
    mx=sum(x for x,y in values)/len(values)
    my=sum(y for x,y in values)/len(values)
    num=sum((x-mx)*(y-my) for x,y in values)
    dx=sum((x-mx)**2 for x,y in values)
    dy=sum((y-my)**2 for x,y in values)
    rho=num/math.sqrt(dx*dy) if dx>0 and dy>0 else None
    return {
        'n_independent_sites_as_descriptive_units':len(values),
        'correlation_site_mean_log10_wind_vs_mean_visit_count':rho,
        'not_a_robust_between_site_causal_effect':True,
        'site_forest_cover_and_baseline_abundance_confounded':True
    }


def fitted_source_refit(source_blob):
    rows=read_original_session_records(source_blob)
    model=conditional_poisson(rows,('log_wind','relative_tke'))
    wind_only=conditional_poisson(rows,('log_wind',))
    cin=[r for r in rows if r['scent']=='cin']
    cin_model=conditional_poisson(cin,('log_wind','relative_tke'))
    loo={}
    for site in sorted({r['site'] for r in rows}):
        others=[r for r in rows if r['site']!=site]
        res=conditional_poisson(others,('log_wind','relative_tke'))
        loo[site]=res['predictors']['log_wind']['beta']
    lbd=list(loo.values())
    summary={
       'status':'CRALL_REAL_SESSION_SITE_CONDITIONAL_POISSON_REFIT_WITH_LIMITS',
       'source_record_id':META_ID,
       'source_Zenodo_doi':'10.5281/zenodo.3743898',
       'author_original_R_model_formula':PAPER_FORMULA,
       'actual_model_is_NOT_author_random_site_and_date_GLMM':True,
       'source_sessions':len(rows),
       'source_sites':len({r['site'] for r in rows}),
       'source_dates':len({r['date'] for r in rows}),
       'source_total_visit_count':sum(r['count'] for r in rows),
       'median_original_wind_m_s':sorted(r['wind'] for r in rows)[len(rows)//2],
       'scent_observation_counts':{
          'cin':sum(r['scent']=='cin' for r in rows),
          'meth':sum(r['scent']=='meth' for r in rows)},
       'primary_site_conditional_poisson':model,
       'wind_only_site_conditional_poisson':wind_only,
       'cineole_only_sensitivity':cin_model,
       'leave_one_site_out_logwind_beta':{
         'min':min(lbd),'max':max(lbd),
         'count_positive':sum(x>0 for x in lbd),
         'n_sites_removed':len(lbd)
       },
       'between_site_site_mean_descriptive_only':pearson_between_site(rows),
       'original_bee_record_count_not_used_as_independent_n':450,
       'scent_free_control_sessions':0,
       'landing_traces_or_pollen_transfer_records':0,
       'plant_seed_or_fitness_records':0,
       'no_original_author_rows_redistributed':True,
       'conclusions_limited_to_scent_bait_visitation_association':True,
    }
    if summary['source_sessions']!=70 or summary['source_total_visit_count']!=409:
        raise ValueError('NO_GO_AUTHOR_SESSION_TOTAL_CHANGED')
    return summary


def main():
    folder=Path('stage36_refit_receipts')
    folder.mkdir(parents=True,exist_ok=True)
    try:
        source=get_source()
        result=fitted_source_refit(source)
    except Exception as e:
        result={
          'status':'NO_GO_NO_VALIDATED_CRALL_SITE_CONDITIONAL_REFIT',
          'error_type':type(e).__name__,
          'error':str(e)[:320],
          'no_original_author_rows_redistributed':True,
          'no_statistical_claim':True}
    (folder/'stage36_source_locked_within_site_poisson.json').write_text(
        json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+'\n',
        encoding='utf8')
    print(json.dumps(result,ensure_ascii=False,allow_nan=False,sort_keys=True))
    if result['status']!='CRALL_REAL_SESSION_SITE_CONDITIONAL_POISSON_REFIT_WITH_LIMITS':
        raise SystemExit(1)


if __name__=='__main__':
    main()
