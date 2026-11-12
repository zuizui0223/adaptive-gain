"""Stage20 mock-only original root recognition confusion matrix contract.

This is NOT real sensory data. Each trial is an independent source-only
root recognition test, strictly separate from main intake/query outcomes.
"""
import unittest
from pilot_root_gate import audit_pilot,synthetic_source

class PilotRootSourceTests(unittest.TestCase):
    def test_class_specific_rates_preserved_by_original_bee_and_colony(self):
        rows=synthetic_source()
        result=audit_pilot(rows)
        self.assertEqual(result["status"],"SYNTHETIC_CLASS_SPECIFIC_ROOT_PILOT_AUDIT")
        self.assertEqual(result["source_trials"],40)
        self.assertEqual(result["fake_source_colonies"],2)
        self.assertEqual(result["fake_source_bees"],2)
        self.assertAlmostEqual(result["pooled_class_specific"]["s0"],.7)
        self.assertAlmostEqual(result["pooled_class_specific"]["s1"],.7)
        self.assertAlmostEqual(result["gain_at_pooled_class_accuracies"],.005)
        self.assertAlmostEqual(result["equal_colony_mean_math_gain"],.0425)
        self.assertTrue(result["not_a_real_organism_measurement"])
    def test_no_cue_feedback_or_future_query_leakage(self):
        rows=synthetic_source()
        rows[0]["feedback_time_s"]=rows[0]["report_time_s"]-.1
        with self.assertRaisesRegex(ValueError,"FEEDBACK_OR_TIMING"):
            audit_pilot(rows)
        rows=synthetic_source()
        rows[0]["additional_leaf_accessible"]=True
        with self.assertRaisesRegex(ValueError,"NOT_INDEPENDENT_ROOT_CLASSIFICATION"):
            audit_pilot(rows)
    def test_missing_one_true_root_class_is_not_a_complete_confusion_matrix(self):
        rows=synthetic_source()
        rows=[r for r in rows if not (r["colony_id"]=="QA_C2" and r["true_root_r"]==1)]
        with self.assertRaisesRegex(ValueError,"INSUFFICIENT_PER_BEE_ROOT_CLASS"):
            audit_pilot(rows)
    def test_actual_animal_data_cannot_be_labeled_as_mock(self):
        rows=synthetic_source()
        rows[0]["source_is_synthetic_QA_only"]=False
        with self.assertRaisesRegex(ValueError,"REAL_PILOT_NOT_AUTHORIZED"):
            audit_pilot(rows)
    def test_duplicate_trial_critical_source_identity_is_rejected(self):
        rows=synthetic_source()
        rows[1]["trial_id"]=rows[0]["trial_id"]
        with self.assertRaisesRegex(ValueError,"DUPLICATE_TRIAL"):
            audit_pilot(rows)

if __name__=="__main__":
    unittest.main()
