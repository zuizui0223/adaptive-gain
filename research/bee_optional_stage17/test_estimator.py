import unittest
from allocation import generate
from source_gate import make_mock_source,validate_mock_source
from estimator import estimate_mock_ITT

TIERS={"low":(.19,.21),"medium":(.99,1.01),"high":(2.99,3.01)}
class OptionalStopEstimatorTests(unittest.TestCase):
    def test_injected_middle_only_did_curvature_recovered_at_colony_level(self):
        a=generate(12,6,seed=73);source=make_mock_source(a,inject_middle_only_mg=2.0)
        qa,data=validate_mock_source(a,source,TIERS)
        self.assertIsNotNone(data)
        out=estimate_mock_ITT(a,data)
        self.assertEqual(out["n_independent_mock_colonies"],12)
        self.assertEqual(out["n_mock_trials"],12*6*48)
        self.assertAlmostEqual(out["middle_vs_extremes_curvature_mg"],2.,delta=.1)
        self.assertEqual(set(out["mode_effects_by_cost_mg"]),{"low","medium","high"})
        self.assertTrue(out["NO_REAL_BEES"])
        self.assertEqual(out["source_unit"],"colony-equal after bee-equal")
    def test_actual_first_skip_remains_ITT_and_changes_request_rate(self):
        a=generate(6,6,seed=7);src=make_mock_source(a)
        _,data=validate_mock_source(a,src,TIERS)
        z=estimate_mock_ITT(a,data)
        self.assertEqual(z["n_mock_trials"],len(a))
        self.assertEqual(z["mean_leaf_requests_by_tier"]["high"],0.)
        self.assertEqual(z["mean_skip_fraction_by_tier"]["high"],1.)
        self.assertEqual(z["status"],"SYNTHETIC_PILOT_LT_12_COLONIES")
    def test_failed_sensor_is_not_analyzable_and_no_subsetting(self):
        a=generate(6,6,seed=7);src=make_mock_source(a)
        _,data=validate_mock_source(a,src,TIERS)
        with self.assertRaisesRegex(ValueError,"ALL_ASSIGNED"):
            estimate_mock_ITT(a,data[:-1])
    def test_missing_underlying_intake_data_is_not_an_optional_stop(self):
        a=generate(6,6,seed=7);src=make_mock_source(a)
        _,data=validate_mock_source(a,src,TIERS)
        data[0]["verified_consumed_sucrose_mg"]=None
        with self.assertRaisesRegex(ValueError,"INTAKE"):
            estimate_mock_ITT(a,data)

if __name__=="__main__":unittest.main()
