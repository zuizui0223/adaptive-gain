"""Stage25: source-grain QA, Bonferroni CP intervals, and hard no-biology gate."""
import copy
import hashlib
import json
import math
import unittest

from source_confidence_gate import audit, cp_interval


def invented_source(n_per_class=6,source_kind='mock'):
    rows=[]
    for col in ('MOCK_COL_A','MOCK_COL_B'):
        for n in range(n_per_class):
            bee=f'{col}-B{n:03d}'
            for cue in ('Z','U','V'):
                for true_bit in (0,1):
                    rows.append({
                      'trial_id':f'{col}-{n}-{cue}-{true_bit}',
                      'colony_id':col, 'bee_id':bee,
                      'cue':cue, 'true_bit':true_bit,
                      'reported_bit':true_bit,
                      'cue_time_utc':'2026-11-01T09:00:00+09:00',
                      'response_time_utc':'2026-11-01T09:00:01+09:00',
                      'feedback_time_utc':'2026-11-01T09:00:02+09:00',
                      'original_response_blinded':True,
                      'other_sources_hidden':True, 'reward_hidden':True
                    })
    manifest={
      'source_kind':source_kind,
      'independent_bee_sampling_by_class':True,
      'randomized_and_blinded_true_classes':True,
      'source_specific_isolation_verified':True,
      'recorded_before_correctness_feedback':True,
      'q_interval':['0.16','0.24'],
      'c_interval':['0.13','0.17'],
      'ethics_reference':'FAKE_FOR_QA_NOT_AN_APPROVAL',
      'original_source_uri':'MOCK_SOURCE_DOES_NOT_EXIST'
    }
    source={'manifest':manifest,'trials':rows}
    resign(source)
    return source


def resign(source):
    # Integrity digest protects fixture against accidental mismatches.
    source['manifest']['trial_data_sha256']=hashlib.sha256(
        json.dumps(source['trials'],sort_keys=True,separators=(',',':'),
                   ensure_ascii=False).encode('utf-8')).hexdigest()


class Stage25SourceGateTest(unittest.TestCase):
    def test_missing_original_data_never_looks_positive(self):
        out=audit({'manifest':{'source_kind':'missing'},'trials':[]})
        self.assertEqual(out['status'],'NO_GO_NO_ORIGINAL_TRIALS')
        self.assertFalse(out['biological_positive_claim'])

    def test_binomial_exact_equal_tailed_boundary_cases(self):
        alpha=.05
        lo,hi=map(float,cp_interval(10,10,alpha))
        self.assertLessEqual(lo,(alpha/2)**(1/10))
        self.assertEqual(hi,1.)
        lo,hi=map(float,cp_interval(0,10,alpha))
        self.assertEqual(lo,0.)
        self.assertGreaterEqual(hi,1-(alpha/2)**(1/10))
        lo,hi=map(float,cp_interval(5,10,alpha))
        self.assertLess(lo,.5)
        self.assertGreater(hi,.5)

    def test_mock_marginal_intervals_and_no_go_outside_theorem(self):
        out=audit(invented_source())
        self.assertEqual(out['status'],'MOCK_ONLY_NO_BIOLOGICAL_INFERENCE')
        self.assertEqual(out['n_rows'],72)
        self.assertEqual(out['n_colonies'],2)
        self.assertEqual(out['unique_bee_ids'],12)
        self.assertFalse(out['biological_positive_claim'])
        self.assertEqual(out['q_and_c_interval_status'],
                         'EXTERNALLY_ASSUMED_NOT_COVERED_BY_THIS_CI')
        for colony in out['per_colony'].values():
            self.assertEqual(colony['conditional_model']['status'],
                             'NO_GO_SENSORY_INTERVAL_OUTSIDE_STAGE24_DOMAIN')
            for class_rate in colony['recognition_rates'].values():
                self.assertEqual(class_rate['correct'],6)
                self.assertEqual(class_rate['n_bees'],6)
                lo,hi=map(float,class_rate['cp_interval_outward'])
                self.assertLess(lo,.5)
                self.assertEqual(hi,1.)

    def test_a_fake_favorable_model_certificate_still_means_zero_bees(self):
        out=audit(invented_source(n_per_class=45))
        self.assertEqual(out['n_rows'],540)
        self.assertEqual(out['status'],'MOCK_ONLY_NO_BIOLOGICAL_INFERENCE')
        self.assertFalse(out['biological_positive_claim'])
        self.assertFalse(out['animal_policy_choices_measured'])
        self.assertFalse(out['independence_source_proof_verified'])
        for colony in out['per_colony'].values():
            self.assertEqual(colony['conditional_model']['status'],
                'CONDITIONAL_MODEL_STRICTLY_POSITIVE_CONTINGENT_ADVANTAGE_CERTIFIED')
            self.assertGreater(
                float(colony['conditional_model']['fixed_policy_gap_lower']),0.)
            self.assertTrue(colony['conditional_model']['no_empirical_certification'])

    def test_declared_original_is_not_authenticated_by_file(self):
        src=invented_source(source_kind='declared_original_unverified')
        out=audit(src)
        self.assertEqual(out['status'],
                         'SOURCE_DECLARED_ORIGINAL_BUT_UNAUTHENTICATED')
        self.assertFalse(out['biological_positive_claim'])

    def test_sha_mismatch_fails_closed(self):
        src=invented_source()
        src['trials'][0]['reported_bit']=1
        with self.assertRaisesRegex(ValueError,'DIGEST_MISMATCH'):
            audit(src)

    def test_same_animal_same_class_is_not_two_independent_units(self):
        src=invented_source()
        bad=copy.deepcopy(src['trials'][0])
        bad['trial_id']='fake-replicated-video-frame'
        src['trials'].append(bad)
        resign(src)
        with self.assertRaisesRegex(ValueError,'PSEUDO_REPLICATED_TRIAL'):
            audit(src)

    def test_cue_response_feedback_order_must_be_original(self):
        src=invented_source()
        src['trials'][0]['feedback_time_utc']='2026-11-01T08:59:59+09:00'
        resign(src)
        with self.assertRaisesRegex(ValueError,'FEEDBACK_BEFORE_RESPONSE'):
            audit(src)

    def test_root_or_other_channel_leak_is_a_hard_error(self):
        src=invented_source()
        src['trials'][0]['other_sources_hidden']=False
        resign(src)
        with self.assertRaisesRegex(ValueError,'RESPONSE_LEAKAGE'):
            audit(src)

    def test_incorrect_class_source_cannot_be_autocorrected(self):
        src=invented_source()
        src['trials'][0]['true_bit']=2
        resign(src)
        with self.assertRaisesRegex(ValueError,'INVALID_SOURCE_CLASS'):
            audit(src)

    def test_q_cost_missing_never_becomes_eight_dimensional_ci(self):
        src=invented_source()
        del src['manifest']['q_interval']
        out=audit(src)
        for colony in out['per_colony'].values():
            self.assertEqual(colony['conditional_model']['status'],
                             'NO_GO_Q_OR_COST_CALIBRATION_UNAVAILABLE')

    def test_animal_ethics_metadata_not_proof_of_origin(self):
        src=invented_source(source_kind='declared_original_unverified')
        del src['manifest']['ethics_reference']
        with self.assertRaisesRegex(ValueError,'BAD_ETHICS_REFERENCE'):
            audit(src)


if __name__=='__main__':
    unittest.main()
