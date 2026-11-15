"""Stage37 SOURCE-FREE unit tests with invented session rows only."""
import math
import unittest

from conditional_site_poisson import conditional_poisson
from twoway_cluster_date_fixed import (
    _design, _multicluster_robust,_date_fixed,_date_loo,analyze
)


def artificial_sessions():
    """70 mock rows, 9 mock sites, 29 mock dates; NOT actual Crall data."""
    rows=[]
    for i in range(70):
        site=f'MOCK_S{i%9:02d}'
        date=f'MOCK_D{i%29:02d}'
        wind=-1.4+.17*(i%7)+.042*((i*5)%11)
        tke=-.55+.091*((i*13)%17)
        count=2+(i*19)%8
        rows.append({
          'site':site,'date':date,'scent':'cin',
          'log_wind':wind,'wind':10**wind,
          'relative_tke':tke,'cover200m':.65,
          'count':count,
        })
    return rows


class Stage37SiteDateRobustnessTests(unittest.TestCase):
    def test_nine_sites_twenty_nine_dates_preserved(self):
        x=_design(artificial_sessions())
        self.assertEqual(len(x['sites']),9)
        self.assertEqual(len(x['dates']),29)
        self.assertEqual(x['X_site'].shape,(70,11))
        self.assertEqual(x['X_full'].shape,(70,39))

    def test_cluster_model_uses_independently_fitted_base_coefficient(self):
        rows=artificial_sessions()
        b=conditional_poisson(rows,('log_wind','relative_tke'))[
            'predictors']['log_wind']['beta']
        r=_multicluster_robust(rows,b)
        self.assertIn(r['status'],(
            'TWO_WAY_SITE_DATE_CLUSTER_SENSITIVITY_AVAILABLE',
            'NO_GO_NONPOSITIVE_TWO_WAY_CLUSTER_VARIANCE',
            'NO_GO_TWO_WAY_CLUSTER_COVARIANCE_FAILURE'))
        self.assertEqual(r['site_count'],9)
        self.assertEqual(r['date_count'],29)
        if r['status']=='TWO_WAY_SITE_DATE_CLUSTER_SENSITIVITY_AVAILABLE':
            lo,hi=r['two_way_IRR_95ci_using_t8_APPROXIMATE']
            self.assertLessEqual(lo,hi)
            self.assertTrue(r['not_a_exactly_calibrated_95pct_interval'])

    def test_wrong_base_fit_for_original_source_must_stop(self):
        with self.assertRaisesRegex(ValueError,'BASELINE_NOT_REPRODUCED'):
            _multicluster_robust(artificial_sessions(),99.)

    def test_date_fixed_can_abort_without_inventing_an_effect(self):
        rows=artificial_sessions()
        orig=conditional_poisson(rows,('log_wind','relative_tke'))[
            'predictors']['log_wind']['beta']
        d=_date_fixed(rows,orig)
        self.assertIn(d['status'],(
            'SITE_PLUS_DATE_FIXED_POISSON_SENSITIVITY_AVAILABLE',
            'NO_GO_WIND_OR_TKE_UNIDENTIFIED_AFTER_DATE_SITE',
            'NO_GO_DATE_FIXED_POISSON_NONCONVERGENCE',
            'NO_GO_DATE_FIXED_WIND_SE_NONFINITE',
            'NO_GO_DATE_FIXED_POISSON_FAILED'))
        if d['status']=='SITE_PLUS_DATE_FIXED_POISSON_SENSITIVITY_AVAILABLE':
            self.assertTrue(d['not_random_site_date_GLMM'])
            self.assertTrue(d['date_fixed_model_fit'])
            self.assertEqual(d['source_dates'],29)

    def test_leave_date_out_preserves_original_unit(self):
        z=_date_loo(artificial_sessions())
        self.assertEqual(z['dates_removed'],29)
        self.assertEqual(z['successful_date_omissions'],29)
        self.assertEqual(z['failed_date_omissions'],0)
        self.assertTrue(z['not_independent_date_level_95pct_ci'])

    def test_unverified_base_receipt_is_rejected(self):
        with self.assertRaisesRegex(ValueError,'PREVIOUS_REFIT_NOT_SOURCE_VERIFIED'):
            analyze(artificial_sessions(),{'status':'FAKE'})

    def test_fake_rows_with_bad_grain_cannot_pass_source_check(self):
        rows=artificial_sessions()
        pseudo={'status':'CRALL_REAL_SESSION_SITE_CONDITIONAL_POISSON_REFIT_WITH_LIMITS',
                'primary_site_conditional_poisson':{'predictors':{
                   'log_wind':{'beta':0.}}}}
        with self.assertRaisesRegex(ValueError,'NOT_ORIGINAL_CRALL_SESSION_GRAIN'):
            analyze(rows[:-1],pseudo)

    def test_model_does_not_automatically_imply_wind_by_scent(self):
        self.assertTrue(all(x['scent']=='cin' for x in artificial_sessions()))
        x=_date_loo(artificial_sessions())
        self.assertTrue(x['no_day_effect_model_fitted_by_LOO'])

if __name__=='__main__':
    unittest.main()
