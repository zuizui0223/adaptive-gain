import copy, unittest
from allocation import generate
from telemetry import mock_telemetry, validate_traces

class ContractTests(unittest.TestCase):
    def prep(self):
        rows=generate(2,2,seed=100)
        trace=mock_telemetry(rows)
        wind={'calm':(.05,.15),'crosswind':(.95,1.05)}
        return rows,trace,wind
    def test_actual_request_after_root_only_in_contingent_mode(self):
        rows,events,wind=self.prep()
        receipt,valid=validate_traces(rows,events,wind)
        self.assertEqual(len(valid),len(rows))
        self.assertEqual(receipt['status'],'SYNTHETIC_PHYSICAL_GATE_PASSED')
        for assignment,obs in zip(rows,events):
            if assignment['access_mode']=='contingent':
                self.assertFalse(obs['pre_root_request_is_binding'])
                self.assertTrue(obs['post_root_request_is_binding'])
            else:
                self.assertTrue(obs['pre_root_request_is_binding'])
                self.assertFalse(obs['post_root_request_is_binding'])
    def test_source_cannot_have_precommit_only_after_root(self):
        rows,events,wind=self.prep()
        e=next(x for x in events if next(r for r in rows if r['trial_id']==x['trial_id'])['access_mode']=='precommit')
        e['pre_root_request_time_s']=1.5
        with self.assertRaisesRegex(ValueError,'PRECOMMIT'):validate_traces(rows,events,wind)
    def test_source_cannot_preselect_contingent_request_before_root(self):
        rows,events,wind=self.prep()
        e=next(x for x in events if next(r for r in rows if r['trial_id']==x['trial_id'])['access_mode']=='contingent')
        e['pre_root_request_is_binding']=True
        with self.assertRaisesRegex(ValueError,'CONTINGENT'):validate_traces(rows,events,wind)
    def test_selected_cue_bits_must_match_recorded_source_world(self):
        rows,events,wind=self.prep()
        events[0]['observed_first_leaf_value']=1-events[0]['observed_first_leaf_value']
        with self.assertRaisesRegex(ValueError,'SOURCE_CUE'):validate_traces(rows,events,wind)
    def test_wrong_animal_sensor_failure_not_zero(self):
        rows,events,wind=self.prep()
        events[0]['sensor_status']='failed'
        with self.assertRaisesRegex(ValueError,'SENSOR'):validate_traces(rows,events,wind)
    def test_request_count_must_be_true_physical_source_events(self):
        rows,events,wind=self.prep()
        events[0]['second_leaf_requested']=events[0]['first_leaf_requested']
        with self.assertRaisesRegex(ValueError,'SECOND_LEAF'):validate_traces(rows,events,wind)
    def test_active_cue_request_must_be_video_or_sensor_verified_as_animal_initiated(self):
        rows,events,wind=self.prep()
        events[0]['source_pre_root_animal_motor_act_verified']=False
        with self.assertRaisesRegex(ValueError,'ANIMAL_REQUEST_SENSOR'):
            validate_traces(rows,events,wind)
    def test_mock_controller_selected_leaf_not_counted_as_bee_information_choice(self):
        rows,events,wind=self.prep()
        e=next(x for x in events if next(r for r in rows if r['trial_id']==x['trial_id'])['access_mode']=='contingent')
        e['source_first_leaf_selector_origin']='controller'
        with self.assertRaisesRegex(ValueError,'NOT_ACTUAL_ANIMAL_QUERY'):
            validate_traces(rows,events,wind)
    def test_3d_wind_required_not_just_name(self):
        rows,events,wind=self.prep()
        events[0]['actual_wind_vector_xyz_m_s']=None
        with self.assertRaisesRegex(ValueError,'WIND_VECTOR'):validate_traces(rows,events,wind)
    def test_one_technical_noncompliance_arm_fails_under_98pct_gate(self):
        rows,events,wind=self.prep()
        # At least two of 64 trials in one (wind,mode) arm must fail
        # to cross the prespecified 98% source-compliance threshold.
        assigned=next(r for r in rows if r['trial_id']==events[0]['trial_id'])
        k=(assigned['assigned_wind'],assigned['access_mode'])
        modified=0
        for event in events:
            condition=next(r for r in rows if r['trial_id']==event['trial_id'])
            if (condition['assigned_wind'],condition['access_mode'])==k:
                event['actual_wind_scalar_m_s']=.4
                event['actual_wind_vector_xyz_m_s']=[0,.4,0]
                modified+=1
                if modified==2:break
        self.assertEqual(modified,2)
        receipt,valid=validate_traces(rows,events,wind)
        self.assertIsNone(valid)
        self.assertEqual(receipt['status'],'NO_GO_BELOW_ARM_PROTOCOL_COMPLIANCE')

if __name__=='__main__':unittest.main()
