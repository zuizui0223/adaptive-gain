"""Synthetic regression checks; NOT a substitute for auditing real Schwarz raw bytes."""
import csv
from pathlib import Path
import sys
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'stage0'))
import schwarz_stage0 as m


def test_mulberry32_matches_independent_javascript_seed_receipt():
    rng = m.Mulberry32(20261018)
    assert [rng.next_u32() for _ in range(8)] == [2680775599,3432565243,2069015649,
      1166166522,1224702332,3106802961,1538116412,326522800]


def test_floyd_sample_does_not_confuse_event_rows_and_unique_links():
    a=['X','X','X','Y','Z','Z']
    for seed in range(30):
        v=m.sample_link_set(a,3,m.Mulberry32(seed))
        assert v <= {'X','Y','Z'}
        assert 1<=len(v)<=3
    assert m.jaccard_dissimilarity({'A','B'},{'B','C'}) == pytest.approx(2/3)


def make_sample(path):
    rec=[]
    for day,events in [('2020-06-01',['B','B','A','A','A']),
                       ('2020-06-03',['B','A','C','C','C']),
                       ('2020-07-15',['B','B','C','C','D'])]:
        for x in events:
            rec.append({'study':'Paper1','cdate':day,'sSite':'plot1',
                        'allSites':'plot1','lower':'Plant'+x,'higher':'BeeX',
                        'freq':'1','sgrain':'day','sgrainID':'plot1_'+day,
                        'largestgrain':'Paper1 plot1'})
    for x in range(3):
        rec.append({'study':'Paper2','cdate':'2020-08-01','sSite':'plotA',
                    'allSites':'plotA','lower':'P','higher':'Q',
                    'freq':'2','sgrain':'week','sgrainID':'plotA_2020-08',
                    'largestgrain':'Paper2 plotA'})
    with path.open('w',newline='',encoding='utf-8') as f:
        wr=csv.DictWriter(f,fieldnames=m.REQUIRED);wr.writeheader();wr.writerows(rec)


def test_study_dates_eligibility_and_no_duplicate_record_deletion(tmp_path):
    f=tmp_path/'source.csv';make_sample(f)
    got=m.audit(f,sample_rows=3,repetitions=12)
    assert got['raw_records']==18
    assert got['studies']==2
    assert got['study_site_keys']==2
    assert got['study_site_dates']==4
    assert got['grain']=={'day':{'records':15,'site_dates':3},'week':{'records':3,'site_dates':1},'month':{'records':0,'site_dates':0}}
    assert got['total_freq']==21
    assert got['exact_duplicate_rows']>0  # repeated positive events are legitimate
    assert got['comparisons']['n']==1
    p=got['comparisons']['pairs'][0]
    assert p['gap']==2 and p['study']=='Paper1'
    assert p['raw']==pytest.approx(1/3) # B/A vs B/A/C, intersection=2 and union=3
    assert 0<=p['rarefied']<=1
    assert got['md5_matches_published'] is False


def test_digest_gate_rejects_unverified_source(tmp_path):
    f=tmp_path/'demo.csv';make_sample(f)
    try:m.audit(f,require_source_md5=True)
    except ValueError as exc: assert 'MD5' in str(exc)
    else: raise AssertionError('digest gate failed')


def test_insufficient_pairs_have_no_misleading_correlation(tmp_path):
    p=tmp_path/'f.csv';make_sample(p)
    r=m.audit(p,sample_rows=200,repetitions=3)
    assert r['comparisons']['n']==0
    assert r['diagnostics']['raw_observed_turnover'] is None
    assert r['diagnostics']['corr_raw_with_lag_days'] is None
