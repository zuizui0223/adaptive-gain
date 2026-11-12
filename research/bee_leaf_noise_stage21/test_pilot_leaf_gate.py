"""SYNTHETIC-ONLY individual/colony leaf bit recognition source-grain tests."""
import unittest
from pilot_leaf_gate import synthetic_source,audit_pilot

class LeafReadoutSourceContractTests(unittest.TestCase):
    def test_leaf_bit_specific_confusions_preserved_per_individual_and_colony(self):
        r=audit_pilot(synthetic_source())
        self.assertEqual(r["status"],"SYNTHETIC_BLINDED_LEAF_CHANNEL_PILOT_QA")
        self.assertEqual(r["source_mock_trials"],40)
        self.assertEqual(r["source_mock_bees"],2)
        self.assertEqual(r["source_mock_colonies"],2)
        self.assertEqual(r["per_leaf_source_marginal_accuracy"],{"U":.9,"V":.9})
        self.assertAlmostEqual(r["gain_at_pooled_accuracies"],0)
        self.assertAlmostEqual(r["equal_colony_mean_theoretical_gain"],.01)
        self.assertEqual(r["real_bees"],0)
    def test_no_root_or_reward_information_leaks_during_leaf_recognition(self):
        rows=synthetic_source()
        rows[0]["root_r_visible"]=True
        with self.assertRaisesRegex(ValueError,"LEAF_PILOT_NOT_BLINDED"):
            audit_pilot(rows)
        rows=synthetic_source()
        rows[0]["target_reward_position_visible"]=True
        with self.assertRaisesRegex(ValueError,"LEAF_PILOT_NOT_BLINDED"):
            audit_pilot(rows)
    def test_response_is_before_correctness_feedback(self):
        rows=synthetic_source()
        rows[0]["feedback_time_s"]=rows[0]["response_time_s"]-.1
        with self.assertRaisesRegex(ValueError,"SOURCE_LEAF_FEEDBACK_TIMING"):
            audit_pilot(rows)
    def test_two_true_bit_classes_required_for_each_leaf_and_bee(self):
        rows=synthetic_source()
        rows=[r for r in rows if not (r["colony_id"]=="QA_C2" and
                   r["leaf_type"]=="U" and r["source_true_bit"]==1)]
        with self.assertRaisesRegex(ValueError,"MISSING_SOURCE_LEAF_BIT_CLASS"):
            audit_pilot(rows)
    def test_duplicate_trial_identity_fails_closed(self):
        rows=synthetic_source()
        rows[1]["trial_id"]=rows[0]["trial_id"]
        with self.assertRaisesRegex(ValueError,"DUPLICATE_ORIGINAL_TRIAL"):
            audit_pilot(rows)
    def test_no_actual_animal_sources_are_accepted_in_public_QA(self):
        rows=synthetic_source()
        rows[0]["source_is_mock_only"]=False
        with self.assertRaisesRegex(ValueError,"REAL_ANIMAL_SOURCE_NOT_AUTHORIZED"):
            audit_pilot(rows)
    def test_marginal_accuracy_is_not_enough_if_one_bit_class_is_unreadable(self):
        rows=synthetic_source()
        # An always-zero U observer has 80% accuracy with U~Bern(.2),
        # but zero U=1 sensitivity: don't certify channel reliability.
        rows[0]["source_reported_bit"]=0
        # The source contract preserves class confusion and makes no
        # accuracy claim based only on the overall correct fraction.
        q=audit_pilot(rows)
        self.assertEqual(q["real_bees"],0)
        self.assertIn("by_true_bit_class",q["source_semantics"])

if __name__=="__main__":unittest.main()
