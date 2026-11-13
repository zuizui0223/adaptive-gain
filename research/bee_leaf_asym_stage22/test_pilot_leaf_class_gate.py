"""Stage22 MOCK-ONLY source-grain tests for FOUR class-specific paid-leaf errors.

An independent actual animal pilot must be separately approved and recorded.
The mock tests never establish real bumblebee sensory accuracy or fitness.
"""
import unittest
from pilot_leaf_class_gate import fake_leaf_classifications,audit_source

class LeafFourClassPilotTests(unittest.TestCase):
    def test_fully_blinded_four_class_source_is_nonnormalized_before_feedback(self):
        rows=fake_leaf_classifications()
        r=audit_source(rows)
        self.assertEqual(r["status"],"STAGE22_FOUR_CLASS_LEAF_MOCK_SOURCE_VERIFIED")
        self.assertEqual(r["fake_original_rows"],80)
        self.assertEqual(r["fake_bees"],2)
        self.assertEqual(r["fake_colonies"],2)
        self.assertEqual(r["real_animal_observations"],0)
        self.assertEqual(r["pooled_four_rates"],{"U0":.85,"U1":.75,"V0":.95,"V1":.95})
        self.assertAlmostEqual(r["equal_colony_mean_theoretical_gain"],.005)
        self.assertAlmostEqual(r["gain_at_pooled_class_rates"],.005)
        self.assertEqual(r["individual_illustrative_gains_by_colony"],{"MOCK_C1":.008,"MOCK_C2":.002})
    def test_each_bit_class_preserved_in_same_fake_bee(self):
        d=fake_leaf_classifications()
        d=[row for row in d if not (row["colony_id"]=="MOCK_C2" and
                                    row["leaf_type"]=="U" and row["true_leaf_bit"]==1)]
        with self.assertRaisesRegex(ValueError,"NO_GO_MISSING_LEAF_TRUE_BIT_CLASS"):
            audit_source(d)
    def test_automatic_info_or_other_leaf_cannot_leak(self):
        for change in (("root_visible",True),("feeder_reward_position_visible",True),
                       ("other_leaf_visible",True)):
            d=fake_leaf_classifications()
            d[0][change[0]]=change[1]
            with self.assertRaisesRegex(ValueError,"NO_GO_LEAF_PILOT_NOT_BLINDED"):
                audit_source(d)
    def test_source_response_before_feedback_and_classification_not_query_round(self):
        d=fake_leaf_classifications()
        d[0]["feedback_time_s"]=1.
        with self.assertRaisesRegex(ValueError,"NO_GO_FEEDBACK_BEFORE_LEAF_REPORT"):
            audit_source(d)
        d=fake_leaf_classifications()
        d[0]["source_phase"]="main_query_task"
        with self.assertRaisesRegex(ValueError,"NO_GO_LEAF_PILOT_NOT_BLINDED"):
            audit_source(d)
    def test_original_trial_identity_and_mock_only_provenance_fail_closed(self):
        d=fake_leaf_classifications()
        d[1]["trial_id"]=d[0]["trial_id"]
        with self.assertRaisesRegex(ValueError,"NO_GO_DUPLICATE_SOURCE_TRIAL_ID"):
            audit_source(d)
        d=fake_leaf_classifications()
        d[0]["mock_only"]=False
        with self.assertRaisesRegex(ValueError,"NO_GO_REAL_ANIMAL_DATA_NOT_AUTHORIZED"):
            audit_source(d)
    def test_wrong_true_or_reported_bit_cannot_be_silently_coerced(self):
        d=fake_leaf_classifications()
        d[0]["reported_leaf_bit"]="0"
        with self.assertRaisesRegex(ValueError,"NO_GO_BIT_NOT_TRUE_BINARY_INTEGER"):
            audit_source(d)
        d=fake_leaf_classifications()
        d[0]["true_leaf_bit"]=-1
        with self.assertRaisesRegex(ValueError,"NO_GO_BIT_NOT_TRUE_BINARY_INTEGER"):
            audit_source(d)

if __name__=="__main__": unittest.main()
