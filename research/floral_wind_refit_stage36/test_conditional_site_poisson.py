"""Stage36 synthetic-only tests of conditional site Poisson inference math.

The 4/8-count mocked sites here are fictional and are NOT Crall raw data.
The actual author's 70 sessions are analyzed only in the dedicated CI.
"""
from __future__ import annotations
import math
import unittest

from conditional_site_poisson import (
  conditional_poisson,pearson_between_site,
  _solve_linear,_inverse,read_original_session_records
)


def _fake_sites():
    groups=[
      ('MOCK_S1',2,4),('MOCK_S2',3,6),('MOCK_S3',4,8),
      ('MOCK_S4',1,2)]
    rows=[]
    for site,lo,hi in groups:
        rows.append({'site':site,'date':'MOCK_DAY1',
          'count':lo,'log_wind':0.,'relative_tke':0.,
          'scent':'cin','wind':.1})
        rows.append({'site':site,'date':'MOCK_DAY2',
          'count':hi,'log_wind':math.log10(2),
          'relative_tke':0.,'scent':'cin','wind':.2})
    return rows


class SiteConditionalPoissonTests(unittest.TestCase):
    def test_closed_form_strata_share_same_rate_ratio(self):
        r=conditional_poisson(_fake_sites(),('log_wind',))
        b=r['predictors']['log_wind']
        self.assertAlmostEqual(b['beta'],math.log(2)/math.log10(2),places=7)
        self.assertAlmostEqual(b['within_site_rate_ratio_per_wind_doubling'],2.,places=7)
        self.assertEqual(r['n_sites_supplied'],4)
        self.assertEqual(r['total_visits'],30)
        self.assertTrue(r['modelbased_se_not_site_cluster_robust'])
        self.assertTrue(r['date_random_effect_not_fitted'])

    def test_uniform_predictor_shift_within_site_has_no_effect(self):
        rows=_fake_sites()
        original=conditional_poisson(rows,('log_wind',))
        for r in rows:
            r['log_wind']+=(list(sorted({x['site'] for x in rows})).index(r['site'])+1)*.2
        shifted=conditional_poisson(rows,('log_wind',))
        self.assertAlmostEqual(shifted['predictors']['log_wind']['beta'],
                               original['predictors']['log_wind']['beta'],places=8)

    def test_site_count_baseline_does_not_create_four_individuals(self):
        r=conditional_poisson(_fake_sites(),('log_wind',))
        self.assertEqual(r['n_original_session_rows_supplied'],8)
        self.assertEqual(r['n_informative_sites'],4)
        self.assertEqual(r['n_conditioned_sessions'],8)

    def test_two_predictor_zero_information_fails_closed(self):
        # no within-site TKE variation, so requesting its coefficient is unsafe
        with self.assertRaisesRegex(ValueError,'SINGULAR_CONDITIONAL_INFORMATION'):
            conditional_poisson(_fake_sites(),('log_wind','relative_tke'))

    def test_solver_inversion_independent_check(self):
        a=[[4.,1.],[1.,3.]]
        x=_solve_linear(a,[1.,2.])
        self.assertAlmostEqual(4*x[0]+x[1],1)
        self.assertAlmostEqual(x[0]+3*x[1],2)
        inv=_inverse(a)
        self.assertAlmostEqual(inv[0][0],3/11)
        self.assertAlmostEqual(inv[1][1],4/11)
        self.assertAlmostEqual(inv[0][1],-1/11)

    def test_invalid_counts_and_values_must_abort(self):
        base=_fake_sites()
        copy=[dict(x) for x in base]
        copy[0]['count']=-1
        with self.assertRaisesRegex(ValueError,'INVALID_ORIGINAL_VISITATION_COUNT'):
            conditional_poisson(copy,('log_wind',))
        copy=[dict(x) for x in base]
        copy[0]['log_wind']=float('nan')
        with self.assertRaisesRegex(ValueError,'MISSING_PREDICTOR'):
            conditional_poisson(copy,('log_wind',))

    def test_no_hidden_identification_of_causality(self):
        r=conditional_poisson(_fake_sites(),('log_wind',))
        self.assertTrue(r['not_a_causal_wind_experiment'])
        self.assertTrue(r['not_wind_by_flower_scent_on_off_interaction'])
        self.assertTrue(r['original_forest_cover_absorbed_by_site_fixed_strata'])

    def test_between_site_aggregation_only_four_sites(self):
        rows=_fake_sites()
        z=pearson_between_site(rows)
        self.assertEqual(z['n_independent_sites_as_descriptive_units'],4)
        self.assertTrue(z['site_forest_cover_and_baseline_abundance_confounded'])

    def test_fake_original_raw_bytes_are_not_authorized_source(self):
        with self.assertRaises(Exception):
            read_original_session_records(b'not original published ZIP')


if __name__=='__main__':
    unittest.main()
