import unittest
from allocation import generate
from source_gate import make_mock_source,validate_mock_source

FAKE_TIERS={"low":(.19,.21),"medium":(.99,1.01),"high":(2.99,3.01)}
class OptionalFirstSourceTests(unittest.TestCase):
    def source(self):
        a=generate(6,6,seed=71)
        telemetry=make_mock_source(a)
        return a,telemetry
    def test_real_skip_is_explicit_animal_choice_not_missingness(self):
        a,records=self.source()
        qa,valid=validate_mock_source(a,records,FAKE_TIERS)
        self.assertEqual(qa["status"],"SYNTHETIC_OPTIONAL_QUERY_SOURCE_GATE_PASSED")
        self.assertEqual(len(valid),len(a))
        self.assertEqual(len(qa["six_original_arms"]),6)
        self.assertGreater(qa["source_explicit_skip_trials"],0)
        for x in records:
            if x["first_action"]=="SKIP":
                self.assertEqual(x["source_leaf_events"],[])
                self.assertEqual(x["physical_leaf_requests"],0)
            if x["source_leaf_events"]:
                self.assertTrue(all(z["origin"]=="animal" for z in x["source_leaf_events"]))
    def test_precommit_skip_must_be_before_root_and_contingent_after_root(self):
        a,recs=self.source()
        one=next(x for x in recs if x["access_mode"]=="precommit")
        one["binding_action_time_s"]=1.3
        with self.assertRaisesRegex(ValueError,"BINDING_ACTION_TIME"):
            validate_mock_source(a,recs,FAKE_TIERS)
        a,recs=self.source()
        one=next(x for x in recs if x["access_mode"]=="contingent")
        one["binding_action_time_s"]=.5
        with self.assertRaisesRegex(ValueError,"BINDING_ACTION_TIME"):
            validate_mock_source(a,recs,FAKE_TIERS)
    def test_no_controller_generated_animal_query(self):
        a,recs=self.source()
        one=next(x for x in recs if x["source_leaf_events"])
        one["source_leaf_events"][0]["origin"]="controller"
        with self.assertRaisesRegex(ValueError,"NOT_ANIMAL_ORIGIN"):
            validate_mock_source(a,recs,FAKE_TIERS)
    def test_cost_delay_and_cue_values_checked(self):
        a,recs=self.source()
        one=next(x for x in recs if x["source_leaf_events"])
        one["source_leaf_events"][0]["measured_delay_s"]=100.
        with self.assertRaisesRegex(ValueError,"COST_DELAY"):
            validate_mock_source(a,recs,FAKE_TIERS)
        a,recs=self.source()
        one=next(x for x in recs if x["source_leaf_events"])
        one["source_leaf_events"][0]["observed_value"]=1-one["source_leaf_events"][0]["observed_value"]
        with self.assertRaisesRegex(ValueError,"LEAF_VALUE"):
            validate_mock_source(a,recs,FAKE_TIERS)
    def test_source_failure_must_not_become_a_zero(self):
        a,recs=self.source()
        recs[0]["sensor_status"]="failed"
        with self.assertRaisesRegex(ValueError,"SENSOR_FAILURE"):
            validate_mock_source(a,recs,FAKE_TIERS)
    def test_source_first_choice_skip_includes_actual_target_choice(self):
        a,recs=self.source()
        one=next(x for x in recs if x["first_action"]=="SKIP")
        self.assertIn(one["final_target_choice"],(0,1,"no_choice"))
        self.assertEqual(one["root_anchor_s"],1.)
        self.assertEqual(one["intake_window_s"],30.)
    def test_physical_reward_target_must_match_hidden_correct_bit(self):
        a,recs=self.source()
        one=recs[0]
        self.assertEqual(one["rewarded_target_bit_source"],a[0]["correct_target"])
        self.assertGreater(one["source_calibrated_nominal_high_mg"],
                           one["source_calibrated_nominal_low_mg"])
        one["rewarded_target_bit_source"]=1-one["rewarded_target_bit_source"]
        with self.assertRaisesRegex(ValueError,"REWARD_TARGET"):
            validate_mock_source(a,recs,FAKE_TIERS)
    def test_reward_odor_and_visual_identity_must_be_masked_before_choice(self):
        a,recs=self.source()
        recs[0]["source_reward_location_cues_masked"]=False
        with self.assertRaisesRegex(ValueError,"REWARD_MAPPING"):
            validate_mock_source(a,recs,FAKE_TIERS)
    def test_no_early_leaf_reveal_before_root(self):
        a,recs=self.source()
        one=next(x for x in recs if x["source_leaf_events"])
        one["source_leaf_events"][0]["reveal_s"]=.8
        with self.assertRaisesRegex(ValueError,"SOURCE_QUERY_CHRONOLOGY"):
            validate_mock_source(a,recs,FAKE_TIERS)

if __name__=="__main__":unittest.main()
