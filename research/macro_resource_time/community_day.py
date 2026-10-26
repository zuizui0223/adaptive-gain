"""Site-day conditional randomization of observed plant/visitor/time records.

This audit asks whether a visitor's observed plant-partner/time information
exceeds the baseline arising from community-wide day-specific plant composition.
Within each compiled site-year and date, only plant labels are shuffled among
recorded visits. It PRESERVES each date x plant visit total and date x visitor
visit total; it does not preserve visitor x plant seasonal preferences, does not
model unvisited flowers, and does not measure independent survey effort.

It is not a pollinator choice, cue routeability, or latent rewiring estimate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from temporal import read_source_csv

EXPECTED_RAW_MD5 = '7a70c3e2356611b0871c163a2f9aed4a'
SHIFTED_STUDIES = {'Chacoff2018', 'Kaiser-Bunbury2017', 'Vazquez2003'}


def _xlogx_sum_by_axis(x, axis):
    """Stable exact zero convention for nonnegative integer arrays."""
    x = np.asarray(x, dtype=np.float64)
    with np.errstate(divide='ignore', invalid='ignore'):
        terms = np.where(x > 0, x * np.log(x), 0.0)
    return terms.sum(axis=axis)


def _information_for_visitors(v, d, p, nvis, ndates, nplants):
    """I(plant;date) for each indexed focal visitor, including unvisited dates."""
    v = np.asarray(v, dtype=np.int64)
    d = np.asarray(d, dtype=np.int64)
    p = np.asarray(p, dtype=np.int64)
    if len(v) == 0 or len(v) != len(d) or len(v) != len(p):
        raise ValueError('nonempty equal-length event labels required')
    if v.min() < 0 or v.max() >= nvis or d.min() < 0 or d.max() >= ndates or p.min() < 0 or p.max() >= nplants:
        raise ValueError('invalid encoded event labels')
    counts = np.bincount((v * ndates + d) * nplants + p,
                         minlength=nvis * ndates * nplants).reshape(nvis, ndates, nplants)
    n = counts.sum(axis=(1, 2)).astype(np.float64)
    if (n == 0).any():
        raise ValueError('every focal visitor must be observed')
    by_date = counts.sum(axis=2)
    by_plant = counts.sum(axis=1)
    cell = _xlogx_sum_by_axis(counts, (1, 2))
    date = _xlogx_sum_by_axis(by_date, 1)
    plant = _xlogx_sum_by_axis(by_plant, 1)
    # I(plant;date) = log(n) + [sum n_dp log n_dp - sum n_d log n_d
    #                            - sum n_p log n_p] / n.
    return np.log(n) + (cell - date - plant) / n


def site_day_conditional_null(cells: pd.DataFrame, focal_visitors, reps=199, seed=0, count_policy="visits"):
    """Test I(plant;date|visitor=v) vs date-conditional visitor/plant exchangeability.

    Input original positive rows: date, lower (plant), higher (visitor), freq>0.
    All visitors (including low-count ones) join the within-day label shuffle.
    Only named focal visitors have statistics; all focal visitors must occur.
    """
    if type(reps) is not int or reps < 1:
        raise ValueError('reps must be a positive built-in int')
    if count_policy not in ('visits', 'positive_rows'):
        raise ValueError('count_policy must be visits or positive_rows')
    fields = {'date', 'higher', 'lower', 'freq'}
    if not fields <= set(cells):
        raise ValueError(f'missing fields: {fields - set(cells)}')
    if cells.empty or cells[list(fields)].isna().any().any():
        raise ValueError('nonempty nonmissing cells required')
    freqs = pd.to_numeric(cells.freq, errors='raise').to_numpy()
    if not np.isfinite(freqs).all() or (freqs <= 0).any() or (freqs % 1 != 0).any():
        raise ValueError('positive integral frequencies required')
    focus = list(focal_visitors)
    if len(focus) == 0 or len(focus) != len(set(focus)):
        raise ValueError('nonempty unique focal visitor labels required')
    if not set(focus) <= set(cells.higher):
        raise ValueError('all focal visitors must occur in the site-year')

    date_codes, date_labels = pd.factorize(cells.date, sort=True)
    plant_codes, plants = pd.factorize(cells.lower, sort=True)
    v_codes, visitors = pd.factorize(cells.higher, sort=True)
    ndate, nplant, nvisitor = len(date_labels), len(plants), len(visitors)
    times = (freqs.astype(np.int64) if count_policy == 'visits'
             else np.ones(len(cells), dtype=np.int64))
    d = np.repeat(date_codes, times)
    p = np.repeat(plant_codes, times)
    v = np.repeat(v_codes, times)
    focus_codes = np.array([np.flatnonzero(visitors == label)[0] for label in focus], dtype=np.int64)
    lookup = np.full(nvisitor, -1, dtype=np.int64)
    lookup[focus_codes] = np.arange(len(focus))
    f = lookup[v]
    relevant = f >= 0
    fv, fd = f[relevant], d[relevant]
    nfocus = len(focus)
    observed = _information_for_visitors(fv, fd, p[relevant], nfocus, ndate, nplant)

    # The conditional pool can change a focal visitor only where it co-occurs
    # with different visitor labels and more than one observed plant species.
    support = np.zeros(nfocus, dtype=int)
    permutable_visits = np.zeros(nfocus, dtype=int)
    date_groups = []
    for day in range(ndate):
        idx = np.flatnonzero(d == day)
        if len(idx) == 0:
            continue
        code = v[idx]
        if len(np.unique(code)) >= 2 and len(np.unique(p[idx])) >= 2:
            date_groups.append(idx)
            focal_at_day = np.unique(f[idx][f[idx] >= 0])
            for j in focal_at_day:
                if np.any(code != focus_codes[j]):
                    support[j] += 1
                    permutable_visits[j] += int(np.count_nonzero(f[idx] == j))

    null = np.empty((reps, nfocus), dtype=np.float64)
    rng = np.random.default_rng(seed)
    for rep in range(reps):
        shuffled = p.copy()
        for idx in date_groups:
            shuffled[idx] = rng.permutation(p[idx])
        null[rep] = _information_for_visitors(fv, fd, shuffled[relevant], nfocus, ndate, nplant)
    mean = null.mean(axis=0)
    sd = null.std(axis=0, ddof=0)
    visits = np.bincount(fv, minlength=nfocus)
    return pd.DataFrame({
        'visitor': focus,
        'count_policy': count_policy,
        'visits': visits,
        'I_observed': observed,
        'null_mean': mean,
        'null_sd': sd,
        'excess_community_day': observed - mean,
        'p_high': (1 + np.sum(null >= observed[None, :] - 1e-12, axis=0)) / (reps + 1),
        'p_low': (1 + np.sum(null <= observed[None, :] + 1e-12, axis=0)) / (reps + 1),
        'shared_testable': support > 0,
        'shared_informative_dates': support,
        'focal_visits_in_informative_dates': permutable_visits,
        'focal_permutable_fraction': permutable_visits / visits,
        'community_visitors': nvisitor,
        'community_plants': nplant,
        'community_dates': ndate,
    })


def run(raw_path: Path, original_panels: Path, outdir: Path, reps: int):
    """Cross-check exact original eligible panels before applying a new null."""
    digest = hashlib.md5(raw_path.read_bytes()).hexdigest()
    if digest != EXPECTED_RAW_MD5:
        raise ValueError(f'raw source checksum mismatch: {digest}')
    original = pd.read_csv(original_panels)
    needed = {'study', 'site', 'year', 'visitor', 'visits', 'I'}
    if not needed <= set(original):
        raise ValueError('original eligible-panel manifest incomplete')
    if original.duplicated(['study', 'site', 'year', 'visitor']).any():
        raise ValueError('duplicate original eligible panels')
    df, encoding = read_source_csv(raw_path)
    freq = pd.to_numeric(df.freq, errors='coerce')
    dates = pd.to_datetime(df.cdate, errors='coerce')
    valid = (df[['study', 'sSite', 'lower', 'higher']].notna().all(axis=1)
             & dates.notna() & freq.notna() & (freq > 0) & (freq % 1 == 0)
             & df.sgrain.eq('day'))
    work = df.loc[valid, ['study', 'sSite', 'lower', 'higher']].copy()
    work['date'] = dates[valid]
    work['year'] = work.date.dt.year
    work['freq'] = freq[valid].astype(np.int64)
    # Preserve every positive row for the positive_rows sensitivity; repeated
    # source rows are not silently deduplicated or collapsed.
    grouped = work.groupby(['study', 'sSite', 'year'], sort=True)
    found = []
    for (study, site, year), eligible in original.groupby(['study', 'site', 'year'], sort=True):
        key = (study, site, year)
        if key not in grouped.groups:
            raise ValueError(f'eligible site-year absent from raw data: {key}')
        g = grouped.get_group(key)
        seed = int.from_bytes(hashlib.sha256(repr(key).encode()).digest()[:8], 'little')
        for policy in ('visits', 'positive_rows'):
            result = site_day_conditional_null(g, eligible.visitor.tolist(), reps=reps,
                                               seed=seed, count_policy=policy)
            result.insert(0, 'year', year)
            result.insert(0, 'site', site)
            result.insert(0, 'study', study)
            result['compiled_date_shift_study'] = study in SHIFTED_STUDIES
            found.append(result)
    res = pd.concat(found, ignore_index=True)
    for policy in ('visits', 'positive_rows'):
        sub = res[res.count_policy.eq(policy)]
        check = original.merge(sub, on=['study', 'site', 'year', 'visitor'], validate='one_to_one')
        if len(check) != len(original) or len(check) != len(sub):
            raise ValueError('focal eligible-panel keys do not match the original analysis')
        if policy == 'visits':
            if not np.array_equal(check.visits_x.to_numpy(), check.visits_y.to_numpy()):
                raise ValueError('recorded visits disagree with primary analysis')
            if not np.allclose(check.I.to_numpy(), check.I_observed.to_numpy(), atol=1e-10, rtol=0):
                raise ValueError('mutual information disagree with primary analysis')
    outdir.mkdir(parents=True, exist_ok=True)
    res.to_csv(outdir / 'community_day_panels.csv', index=False)
    grouped_studies = []
    for (policy, study), g in res.groupby(['count_policy', 'study'], sort=True):
        usable = g[g.shared_testable]
        grouped_studies.append({
            'count_policy': policy, 'study': study, 'eligible_panels': len(g),
            'shared_testable_panels': len(usable),
            'mean_excess_testable': float(usable.excess_community_day.mean()) if len(usable) else None,
            'positive_fraction_testable': float((usable.excess_community_day > 1e-10).mean()) if len(usable) else None,
            'p_high_le_005_testable': float((usable.p_high <= 0.05).mean()) if len(usable) else None,
            'compiled_date_shift_study': bool(g.compiled_date_shift_study.iloc[0]),
        })
    studies = pd.DataFrame(grouped_studies)
    studies.to_csv(outdir / 'community_day_by_source.csv', index=False)
    summary = {'status': 'completed_original_data_observational_conditional_null',
               'raw_md5': digest, 'source_encoding': encoding, 'reps': reps,
               'raw_study_labels_not_independent': True,
               'claim_boundary': 'Both counts are conditional positive-observation nulls, NOT floral availability, observer effort, animal choice, sensory routeability or latent rewiring corrections.'}
    for policy, panel_set in res.groupby('count_policy', sort=True):
        usable = panel_set[panel_set.shared_testable]
        study_subset = studies[studies.count_policy.eq(policy)]
        means = study_subset.mean_excess_testable.dropna()
        summary[policy] = {
            'eligible_panels_reconciled': len(panel_set),
            'source_labels': len(study_subset),
            'shared_testable_panels': len(usable),
            'median_excess_testable_nats': float(usable.excess_community_day.median()) if len(usable) else None,
            'positive_fraction_testable': float((usable.excess_community_day > 1e-10).mean()) if len(usable) else None,
            'p_high_le_005_testable': float((usable.p_high <= 0.05).mean()) if len(usable) else None,
            'negative_p_low_le_005_testable': float((usable.p_low <= 0.05).mean()) if len(usable) else None,
            'study_label_positive_means': int((means > 1e-10).sum()),
            'study_label_testable': len(means),
        }
    (outdir / 'community_day_summary.json').write_text(json.dumps(summary, indent=2))
    print('COMMUNITY_DAY_SUMMARY ' + json.dumps(summary), flush=True)
    print('COMMUNITY_DAY_ANALYSIS_COMPLETE', flush=True)
    return res, studies, summary


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw', default='macro_results/raw/OIK-07303_database.csv')
    parser.add_argument('--original-panels', default='macro_results/visitor_site_season_results.csv')
    parser.add_argument('--outdir', default='macro_results')
    parser.add_argument('--reps', type=int, default=199)
    args = parser.parse_args(argv)
    run(Path(args.raw), Path(args.original_panels), Path(args.outdir), args.reps)


if __name__ == '__main__':
    main()
