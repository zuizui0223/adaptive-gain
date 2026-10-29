import unittest
from randomization import generate_allocation
from colony_contrast import generate_synthetic_QA_outcomes
from future_source_contract import (
    audit_real_trial_telemetry,make_synthetic_QA_telemetry,
    analyze_future_source,validate_calibrated_wind_ranges
)

# All fixture values are artificial, NOT measured bee outcomes or real wind
# calibration. They only test a future data acquisition and analysis contract.
FAKE_PILOT={"calm":(0.0,.20),"crosswind":(.8,1.2)}

class WindCueHardwareSourceContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assign=generate_allocation(n_colonies=12,bees_per_colony=4,seed=44)
        mock=generate_synthetic_QA_outcomes(cls.assign,seed=23)
        cls.source=make_synthetic_QA_telemetry(cls.assign,mock)
    def test_full_synthetic_instrumentation_data_leads_to_colony_equal_result(self):
        audit,observations=audit_real_trial_telemetry(
            self.assign,self.source,FAKE_PILOT)
        self.assertEqual(audit["status"],"HARDWARE_AND_MASS_CONTRACT_PASSED")
        self.assertEqual(len(observations),len(self.assign))
        self.assertEqual(audit["minimum_observed_arm_adherence"],1)
        result=analyze_future_source(self.assign,self.source,FAKE_PILOT)
        self.assertEqual(result["status"],
                         "SOURCE_TELEMETRY_AND_COLONY_ESTIMATOR_APPLIED")
        self.assertEqual(result["colony_estimand"]["source_colonies"],12)
    def test_unconfirmed_feeder_loss_is_not_consumed_sucrose(self):
        corrupt=[dict(v) for v in self.source]
        corrupt[0]["feeding_contact_verified"]=False
        with self.assertRaisesRegex(ValueError,"NOT_LINKED_TO_BEE_FEEDING"):
            audit_real_trial_telemetry(self.assign,corrupt,FAKE_PILOT)
    def test_no_choice_cannot_have_positive_sucrose(self):
        corrupt=[dict(v) for v in self.source]
        corrupt[0]["choice"]="no_choice"
        with self.assertRaisesRegex(ValueError,"CONTRADICTORY"):
            audit_real_trial_telemetry(self.assign,corrupt,FAKE_PILOT)
    def test_actual_flower_undisclosed_at_release_is_protocol_violation(self):
        corrupt=[dict(v) for v in self.source]
        indices=[i for i,r in enumerate(self.assign) if
                 (r["assigned_cue_order"],r["assigned_wind"])==
                 ("reward_first","crosswind")][:24]
        for i in indices:
            corrupt[i]["left_accessible_at_release"]=False
        audit,obs=audit_real_trial_telemetry(
            self.assign,corrupt,FAKE_PILOT)
        self.assertIsNone(obs)
        self.assertEqual(audit["status"],
                         "NO_GO_REAL_PROTOCOL_ADHERENCE_BELOW_98_PERCENT")
        self.assertEqual(
            audit["per_trial_protocol_failure_histogram"]
                ["one_flower_unavailable_at_release"],len(indices))
        self.assertEqual(audit["n_assigned_trials"],len(self.assign))
    def test_wind_exposure_must_match_separately_locked_pilot_ranges(self):
        corrupt=[dict(v) for v in self.source]
        sample=next(i for i,r in enumerate(self.assign)
                    if r["assigned_wind"]=="crosswind")
        corrupt[sample]["measured_wind_m_s"]=0
        corrupt[sample]["measured_wind_xyz_m_s"]=[0,0,0]
        audit,observations=audit_real_trial_telemetry(
            self.assign,corrupt,FAKE_PILOT)
        self.assertEqual(
            audit["per_trial_protocol_failure_histogram"]
                ["assigned_wind_not_physically_delivered"],1)
        self.assertEqual(audit["n_assigned_trials"],len(self.assign))
        with self.assertRaisesRegex(ValueError,"CALIBRATION_RANGES_OVERLAP"):
            validate_calibrated_wind_ranges({
                "calm":(0,.9),"crosswind":(.8,1.2)})
    def test_missing_source_clock_or_bad_cue_order_never_accepted(self):
        corrupt=[dict(v) for v in self.source]
        corrupt[0]["cue1_actual_s"]=7
        with self.assertRaisesRegex(ValueError,"INVERTED"):
            audit_real_trial_telemetry(self.assign,corrupt,FAKE_PILOT)
        corrupt=[dict(v) for v in self.source]
        del corrupt[0]["cue1_actual_s"]
        with self.assertRaisesRegex(ValueError,"REVEAL_TIMESTAMPS"):
            audit_real_trial_telemetry(self.assign,corrupt,FAKE_PILOT)
    def test_source_must_contain_wind_direction_turbulence_and_synchronization(self):
        for key,pattern in (
            ("measured_wind_xyz_m_s","MISSING_3D_WIND_DIRECTION"),
            ("measured_wind_turbulence_sd_m_s","MISSING_WIND_TURBULENCE"),
            ("max_camera_anemometer_clock_error_ms","SYNCHRONIZATION")
        ):
            corrupt=[dict(v) for v in self.source]
            del corrupt[0][key]
            with self.assertRaisesRegex(ValueError,pattern):
                audit_real_trial_telemetry(self.assign,corrupt,FAKE_PILOT)
    def test_no_report_of_effect_if_sensors_fail_or_source_trials_missing(self):
        corrupt=[dict(v) for v in self.source]
        corrupt[0]["sensor_status"]="sensor_failed"
        with self.assertRaisesRegex(ValueError,"MISSING_TRIAL_OUTCOME"):
            audit_real_trial_telemetry(self.assign,corrupt,FAKE_PILOT)
        with self.assertRaisesRegex(ValueError,"WITHOUT_SOURCE_TELEMETRY"):
            audit_real_trial_telemetry(self.assign,self.source[1:],FAKE_PILOT)

if __name__=="__main__":unittest.main()
