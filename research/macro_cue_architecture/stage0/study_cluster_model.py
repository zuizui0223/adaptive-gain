"""Dependency-free study-FE/CR1 exploratory model of detected-link turnover.

This is an associational within-study regression, not a causal network process
model. A small number of studies and overlapping date-pair responses are key
inference limitations; report uncertainty as exploratory only.
"""
from __future__ import annotations
from collections import defaultdict
import math

# Two-sided 0.975 Student t critical values, df = 1..30 (rounded to < 1e-8).
_T975=(None,12.7062047364,4.3026527297,3.1824463053,2.7764451052,
2.5705818356,2.4469118511,2.3646242510,2.3060041350,2.2621571628,
2.2281388519,2.2009851601,2.1788128297,2.1603686565,2.1447866879,
2.1314495456,2.1199052992,2.1098155778,2.1009220402,2.0930240544,
2.0859634473,2.0796138447,2.0738730689,2.0686576104,2.0638985616,
2.0595385528,2.0555294386,2.0518305165,2.0484071418,2.0452296421,
2.0422724563)


def _mv(m, v):
    return [m[0][0]*v[0]+m[0][1]*v[1],m[1][0]*v[0]+m[1][1]*v[1]]


def _mul2(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def study_fixed_effect_regression(pairs, *, outcome, fixed_effects='study'):
    if outcome not in ('raw','rarefied'):
        raise ValueError('outcome must be raw or rarefied')
    if fixed_effects not in ('study','site'):
        raise ValueError('fixed_effects must be study or site')
    grouped=defaultdict(list)
    for record in pairs:grouped[record[fixed_effects]].append(record)
    studies=list({record['study'] for record in pairs})
    if len(studies)<3:
        raise ValueError('at least 3 study clusters required')
    X=[];Y=[];clusters=[]
    for fe_id,records in grouped.items():
        raw=[[math.log1p(r['gap']),r['imbalance']] for r in records]
        vals=[r[outcome] for r in records]
        mu=[sum(row[j] for row in raw)/len(raw) for j in range(2)]
        my=sum(vals)/len(vals)
        for row,value in zip(raw,vals):
            X.append([row[j]-mu[j] for j in range(2)])
            Y.append(value-my);clusters.append(records[0]['study'])
    n=len(Y);g=len(studies);k=len(grouped)+2
    a=sum(row[0]**2 for row in X);b=sum(row[0]*row[1] for row in X)
    c=sum(row[1]**2 for row in X);det=a*c-b*b
    if det<=1e-14:
        raise ValueError('collinear within-study predictors')
    inv=[[c/det,-b/det],[-b/det,a/det]]
    xy=[sum(row[j]*y for row,y in zip(X,Y)) for j in range(2)]
    beta=_mv(inv,xy)
    scores={st:[0.0,0.0] for st in studies}
    for st,row,y in zip(clusters,X,Y):
        resid=y-sum(row[j]*beta[j] for j in range(2))
        for j in range(2):scores[st][j]+=row[j]*resid
    meat=[[sum(vec[i]*vec[j] for vec in scores.values()) for j in range(2)] for i in range(2)]
    correction=g/(g-1)*(n-1)/(n-k)
    cov=_mul2(_mul2(inv,meat),inv)
    se=[math.sqrt(max(0.0,correction*cov[j][j])) for j in range(2)]
    df=g-1
    critical=_T975[df] if df<len(_T975) else None
    ci=[[beta[j]-critical*se[j],beta[j]+critical*se[j]] for j in range(2)] if critical else None
    return {'n_pairs':n,'n_studies':g,'n_fixed_effect_groups':len(grouped),'fixed_effects':fixed_effects,'outcome':outcome,
      'predictors':['log1p_day_gap','log_positive_record_count_ratio'],
      'beta':beta,'cluster_study_se':se,'ci95_t_cluster_df':ci,'df':df,
      'conditional_meaning':'observed-link dissimilarity; no causal routeability or detection correction'}
