#!/usr/bin/env python3
"""Auditable survey-denominator screen and observed-network sensitivity analysis.

Source: Schwarz et al. (2021) Dryad doi:10.5061/dryad.qz612jmbp,
Zenodo public mirror, record 4744654, OIK-07303_database.csv.

IMPORTANT: input is positive flower-visit records, not a zero-preserving survey
frame. Record-row normalization is NOT sampling-effort normalization; link-set
Jaccard is not ecological rewiring or a measure of sequential sensory routing.

To reproduce with a downloaded exact source (MD5 7a70c3e2356611b0871c163a2f9aed4a):
python stage0/schwarz_stage0.py --csv OIK-07303_database.csv --output stage0_receipt.json

You may use --download to retrieve from the source, but do not publish a result
until the source digest and observation semantics have been checked.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
from dataclasses import dataclass, field
from datetime import date
import hashlib
import json
import math
from pathlib import Path
import urllib.request

SOURCE_URL = "https://zenodo.org/records/4744654/files/OIK-07303_database.csv?download=1"
EXPECTED_MD5 = "7a70c3e2356611b0871c163a2f9aed4a"
REQUIRED = ("study", "cdate", "sSite", "allSites", "lower", "higher", "freq", "sgrain", "sgrainID", "largestgrain")


@dataclass
class Day:
    study: str
    site: str
    day: str
    grain: str
    events: list[str] = field(default_factory=list)
    nonunit: int = 0
    links: set[str] = field(default_factory=set)


class Mulberry32:
    """Exact JS Math.imul/>>>-equivalent seeded generator used in the live check."""

    def __init__(self, seed: int):
        self.seed = seed & 0xffffffff

    @staticmethod
    def _rshift(x: int, n: int) -> int:
        return (x & 0xffffffff) >> n

    def next_u32(self) -> int:
        self.seed = (self.seed + 0x6D2B79F5) & 0xffffffff
        t = ((self.seed ^ self._rshift(self.seed, 15)) * (self.seed | 1)) & 0xffffffff
        s = (t ^ self._rshift(t, 7)) & 0xffffffff
        t = (t ^ ((t + ((s * (61 | t)) & 0xffffffff)) & 0xffffffff)) & 0xffffffff
        return (t ^ self._rshift(t, 14)) & 0xffffffff

    def random(self) -> float:
        return self.next_u32() / 4294967296.0


def sample_link_set(observations: list[str], m: int, rng: Mulberry32) -> set[str]:
    """Floyd's exact uniform subset of RECORD rows, not of unique links."""
    n = len(observations)
    if m > n or m < 0:
        raise ValueError("cannot draw more records than observed")
    chosen = set()
    for j in range(n - m, n):
        k = int(rng.random() * (j + 1))
        chosen.add(j if k in chosen else k)
    assert len(chosen) == m
    return {observations[i] for i in chosen}


def jaccard_dissimilarity(a: set[str], b: set[str]) -> float:
    union = len(a | b)
    return 1 - len(a & b) / union if union else 0.0


def pearson(x, y):
    if len(x) < 2:
        return None
    mx, my = sum(x)/len(x), sum(y)/len(y)
    a = sum((u-mx)*(v-my) for u,v in zip(x,y))
    b = math.sqrt(sum((u-mx)**2 for u in x)*sum((v-my)**2 for v in y))
    return a/b if b else None


def _mean(rows, key):
    return sum(z[key] for z in rows)/len(rows) if rows else None


def audit(path: Path, *, repetitions: int = 80, sample_rows: int = 20, seed: int = 20261018,
          require_source_md5: bool = False) -> dict:
    if not isinstance(repetitions, int) or repetitions <= 0:
        raise ValueError('repetitions must be positive')
    if not isinstance(sample_rows, int) or sample_rows <= 0:
        raise ValueError('sample_rows must be positive')
    file_hash = hashlib.md5(path.read_bytes()).hexdigest()
    if require_source_md5 and file_hash != EXPECTED_MD5:
        raise ValueError(f'input MD5 {file_hash} differs from publicly advertised digest {EXPECTED_MD5}')
    datasets: dict[tuple[str,str,str],Day] = {}
    sites: dict[tuple[str,str], list[Day]] = defaultdict(list)
    studies: dict[str, dict] = {}
    missing = Counter()
    name_plants, name_pollinators, unique_records = set(), set(), set()
    row_count, freq_total, duplicate_identical = 0, 0, 0
    first, last = '9999', '0000'
    with path.open('r', encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or tuple(reader.fieldnames) != REQUIRED:
            raise ValueError('unexpected raw event schema; do not infer columns')
        for record in reader:
            if None in record:
                raise ValueError('extra unnamed columns in CSV record')
            row_count += 1
            for key in REQUIRED:
                if not (record.get(key) or '').strip():
                    missing[key] += 1
            day, study, site = record['cdate'], record['study'], record['sSite']
            try:
                parsed = date.fromisoformat(day)
                fr = int(record['freq'])
            except (TypeError, ValueError) as e:
                raise ValueError('invalid date or integer freq') from e
            if fr <= 0:
                raise ValueError('freq must be positive')
            first, last = min(first, day), max(last, day)
            signature = tuple(record[k] for k in REQUIRED)
            if signature in unique_records:
                duplicate_identical += 1
            else:
                unique_records.add(signature)
            freq_total += fr
            key = (study,site,day)
            if key not in datasets:
                d = Day(study=study, site=site, day=day, grain=record['sgrain'])
                datasets[key] = d
                sites[(study,site)].append(d)
            d = datasets[key]
            if d.grain != record['sgrain']:
                raise ValueError('same study/site/day has conflicting sampling grain')
            link = record['lower']+'↔'+record['higher']
            d.events.append(link); d.links.add(link)
            d.nonunit += int(fr != 1)
            name_plants.add(record['lower']);name_pollinators.add(record['higher'])
            if study not in studies:
                studies[study] = {'rows':0, 'nonunit':0, 'grains':set(), 'sites':set(), 'days':set()}
            st = studies[study];st['rows']+=1;st['nonunit']+=int(fr!=1)
            st['grains'].add(record['sgrain']);st['sites'].add(site);st['days'].add(key)
    grain_summary={g:{'records':0,'site_dates':0} for g in ('day','week','month')}
    for d in datasets.values():
        g=grain_summary.setdefault(d.grain,{'records':0,'site_dates':0})
        g['records']+=len(d.events);g['site_dates']+=1

    pairs=[]
    for key,seq in sites.items():
        seq.sort(key=lambda d:d.day)
        for x,y in zip(seq[:-1],seq[1:]):
            gap=(date.fromisoformat(y.day)-date.fromisoformat(x.day)).days
            if (x.grain=='day' and y.grain=='day' and 1<=gap<=30 and
                    len(x.events)>=sample_rows and len(y.events)>=sample_rows and
                    x.nonunit==0 and y.nonunit==0):
                pairs.append({'x':x,'y':y,'gap':gap,'study':x.study,
                              'site':f'{x.study}|{x.site}',
                              'imbalance':math.log(max(len(x.events),len(y.events)) / min(len(x.events),len(y.events))),
                              'raw':jaccard_dissimilarity(x.links,y.links)})
    rng=Mulberry32(seed)
    for item in pairs:
        x,y=item['x'],item['y']
        item['rarefied']=sum(jaccard_dissimilarity(
            sample_link_set(x.events,sample_rows,rng),
            sample_link_set(y.events,sample_rows,rng))
            for _ in range(repetitions))/repetitions
    simple=[{k:v for k,v in p.items() if k not in ('x','y')} for p in pairs]
    per_study=defaultdict(list)
    for p in simple: per_study[p['study']].append(p)
    mean_study={study:{'n':len(s), 'raw':_mean(s,'raw'),
                       'rarefied20':_mean(s,'rarefied'),
                       'lag':_mean(s,'gap')} for study,s in per_study.items()}
    intervals=[(1,7),(8,14),(15,30)]
    bins=[{'gap':f'{a}-{b}', 'n':len(s), 'raw':_mean(s,'raw'),
           'rarefied20':_mean(s,'rarefied')} for a,b in intervals
          for s in ([p for p in simple if a<=p['gap']<=b],)]
    return {
        'source':SOURCE_URL, 'md5':file_hash, 'md5_matches_published':file_hash==EXPECTED_MD5,
        'raw_records':row_count, 'total_freq':freq_total, 'studies':len(studies),
        'study_site_keys':len(sites), 'study_site_dates':len(datasets),
        'plant_name_strings':len(name_plants), 'pollinator_name_strings':len(name_pollinators),
        'exact_duplicate_rows':duplicate_identical,'date_first':first,'date_last':last,
        'missing':dict(missing), 'grain':grain_summary,
        'comparisons':{'n':len(simple),'studies':len(per_study),'sites':len(set(p['site'] for p in simple)),
                       'lag_range':[1,30],'min_positive_records_per_day':sample_rows,
                       'freq1_only':True,'pairs':simple},
        'diagnostics':{'raw_observed_turnover':_mean(simple,'raw'),
                       'equal_record_rarefied_turnover':_mean(simple,'rarefied'),
                       'corr_raw_with_record_count_imbalance':pearson([p['imbalance'] for p in simple],[p['raw'] for p in simple]),
                       'corr_rarefied_with_record_count_imbalance':pearson([p['imbalance'] for p in simple],[p['rarefied'] for p in simple]),
                       'corr_raw_with_lag_days':pearson([p['gap'] for p in simple],[p['raw'] for p in simple]),
                       'corr_rarefied_with_lag_days':pearson([p['gap'] for p in simple],[p['rarefied'] for p in simple]),
                       'lag_bins':bins,'by_study':mean_study},
        'simulation':{'seed':seed,'replicates_per_pair':repetitions,'sampling':'20 positive row events without replacement per site/date'},
        'claim_ceiling':['positive visit rows are NOT observer effort or zero-visit observation opportunities',
                         'link Jaccard is observed detection turnover not latent rewiring',
                         'compiled dates may be season-shifted and sites pooled',
                         'overlapping date comparisons require study/site clustered inference',
                         'no animal cue order or independently known reward target is present']
    }


def main():
    pa=argparse.ArgumentParser(description=__doc__)
    pa.add_argument('--csv',type=Path,help='verified original OIK-07303_database.csv file')
    pa.add_argument('--download',action='store_true',help='download public Zenodo mirror with source-digest check')
    pa.add_argument('--output',type=Path,default=Path('schwarz_stage0_receipt.json'))
    pa.add_argument('--sample-rows',type=int,default=20)
    pa.add_argument('--repetitions',type=int,default=80)
    pa.add_argument('--seed',type=int,default=20261018)
    pa.add_argument('--require-md5',action='store_true')
    pa.add_argument('--study-cluster-model', action='store_true', help='exploratory study-FE/CR1 regression (requires numpy/scipy)')
    args=pa.parse_args()
    if args.download:
        if args.csv is None:
            args.csv=Path('OIK-07303_database.csv')
        if args.csv.exists():
            raise FileExistsError(f'refusing to overwrite existing file {args.csv}')
        urllib.request.urlretrieve(SOURCE_URL,args.csv)
        args.require_md5=True
    if args.csv is None or not args.csv.is_file():
        pa.error('provide --csv existing original or use --download')
    report=audit(args.csv,repetitions=args.repetitions,sample_rows=args.sample_rows,
                 seed=args.seed,require_source_md5=args.require_md5)
    if args.study_cluster_model and report['comparisons']['n']:
        from study_cluster_model import study_fixed_effect_regression
        report['exploratory_models']={
            fixed: {outcome:study_fixed_effect_regression(report['comparisons']['pairs'],outcome=outcome,fixed_effects=fixed)
                    for outcome in ('raw','rarefied')}
            for fixed in ('study','site')
        }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    concise={k:v for k,v in report.items() if k not in ('comparisons',)}
    concise['comparisons']={k:v for k,v in report['comparisons'].items() if k!='pairs'}
    print(json.dumps(concise,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
