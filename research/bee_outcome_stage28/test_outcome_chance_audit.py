"""Stage28 tests use invented mock entries ONLY. No copyrighted trial source."""
import csv
import io
import json
import tempfile
import unittest
from pathlib import Path

from outcome_chance_audit import analyze_csv,main
from audit_author_request_semantics import COLUMNS


def mocked_csv():
    s=io.StringIO()
    w=csv.DictWriter(s,fieldnames=COLUMNS,lineterminator='\n')
    w.writeheader()
    tid=0
    for j in range(3):
        bee=f'MOCK_B{j}'
        for start in (1,51):
            n=0
            for difficulty in ('Easy','Hard','Impossible'):
                for typ,landing in (
                    ('Regular',0),('Regular',1),
                    ('Random_Free_Cue',0),('Random_Free_Cue',1)):
                    n+=1;tid+=1
                    request=int(typ=='Random_Free_Cue' or landing)
                    correct=(int(j==2) if difficulty=='Impossible' and
                              typ=='Regular' and landing==0 else 1)
                    row=dict.fromkeys(COLUMNS,'')
                    row.update({
                        'Trial_ID':str(tid),'Bee_ID':bee,
                        'Trial_Number':str(start+n-1),
                        'Difficulty':difficulty,'Trial_Type':typ,
                        'Info_Requested':str(request),
                        'Actually_Landed_On_Platform':str(landing),
                        'Is_Post_Request_Correct':f'{correct}.0' if request else '',
                        'Post_Request_Accuracy':f'{correct}.0' if request else '',
                        'Is_Post_Non_Request_Correct':f'{correct}.0' if not request else '',
                        'Non_Request_Accuracy':f'{correct}.0' if not request else ''
                    })
                    w.writerow(row)
    return s.getvalue().encode('utf-8')


class OutcomeSourceQATests(unittest.TestCase):
    def test_invented_source_exact_four_way_stratification(self):
        x=analyze_csv(mocked_csv(),verify_source=False,reps=200)
        self.assertEqual(x['status'],'FAKE_SOURCE_FREE_TEST_ONLY')
        self.assertEqual(x['n_author_trial_rows'],72)
        self.assertEqual(x['n_unique_bee_ids'],3)
        for d in ('Easy','Hard','Impossible'):
            for k in ('Regular_No_Cue','Regular_Paid_Cue',
                      'Free_Cue_No_Landing','Free_Cue_Landing'):
                self.assertEqual(x['source_specific_accuracy'][d][k]['trials'],6)
        self.assertEqual(x['impossible_no_cue_negative_control']['trials'],6)
        self.assertEqual(x['impossible_no_cue_negative_control']['correct'],2)
        self.assertAlmostEqual(x['impossible_no_cue_negative_control']['accuracy'],1/3)
        self.assertTrue(x['anomalous_rate_reason_unidentified'])

    def test_per_bee_not_trial_pseudoreplication(self):
        x=analyze_csv(mocked_csv(),verify_source=False,reps=100)
        v=x['per_bee_negative_control']
        self.assertEqual(v['n_bees'],3)
        self.assertEqual(v['n_below_50pct'],2)
        self.assertEqual(v['n_above_50pct'],1)
        self.assertEqual(v['n_equal_50pct'],0)
        self.assertAlmostEqual(v['equal_bee_mean_accuracy'],1/3)
        self.assertEqual(x['bee_unit_bootstrap']['sampling_unit'],
                         'Bee_ID (not independent colony)')
        self.assertTrue(x['bee_unit_bootstrap']['independent_colony_variance_unavailable'])

    def test_early_and_late_both_present(self):
        x=analyze_csv(mocked_csv(),verify_source=False,reps=50)
        for period in ('Early','Late'):
            z=x['early_late_source_check'][period]
            self.assertEqual(z['Impossible|Regular_No_Cue']['trials'],3)
            self.assertEqual(z['Impossible|Free_Cue_No_Landing']['trials'],3)
            self.assertAlmostEqual(z['Impossible|Regular_No_Cue']['accuracy'],1/3)

    def test_reward_proxy_keeps_unknown_punishment_and_self_selection(self):
        x=analyze_csv(mocked_csv(),verify_source=False,reps=50)
        d=x['hypothetical_reward_proxy_not_fitness']['Impossible']
        self.assertAlmostEqual(d['paid_correct_probability'],1.)
        self.assertAlmostEqual(d['no_cue_correct_probability'],1/3)
        self.assertAlmostEqual(d['paid_minus_no_cue_correct_reward_proxy_at_K0'],1/6)
        self.assertAlmostEqual(d['conditional_break_even_K'],-.25)
        self.assertIn('not causal',d['CAUTION'].lower())
        hypot=x['hypothetical_reward_proxy_not_fitness'][
          'Impossible_if_unobserved_no_cue_chance_is_0point5']
        self.assertTrue(hypot['NOT_OBSERVED_COUNTERFACTUAL'])

    def test_byte_identity_mismatch_fails_closed(self):
        with self.assertRaisesRegex(ValueError,'AUTHOR_SOURCE_BLOB_SHA_MISMATCH'):
            analyze_csv(mocked_csv(),verify_source=True,reps=30)

    def test_missing_category_fails_closed(self):
        lines=mocked_csv().decode().splitlines()
        rest=[row for row in lines[1:] if not ',Random_Free_Cue,' in row]
        with self.assertRaisesRegex(ValueError,'MISSING_PUBLIC_OUTCOME_CLASS'):
            analyze_csv(('\n'.join(lines[:1]+rest)+'\n').encode(),
                        verify_source=False,reps=30)

    def test_wrong_outcome_branch_fails_source_gate(self):
        src=mocked_csv().decode().splitlines()
        ix=next(i for i,row in enumerate(src) if ',Regular,0,0,' in row)
        a=src[ix].split(',')
        a[-1]=''
        src[ix]=','.join(a)
        with self.assertRaisesRegex(ValueError,'NONBINARY'):
            analyze_csv(('\n'.join(src)+'\n').encode(),verify_source=False,reps=30)

    def test_deterministic_cluster_bootstrap(self):
        a=analyze_csv(mocked_csv(),verify_source=False,reps=200,seed=20261115)
        b=analyze_csv(mocked_csv(),verify_source=False,reps=200,seed=20261115)
        self.assertEqual(a['bee_unit_bootstrap'],b['bee_unit_bootstrap'])

    def test_bootstrap_limits(self):
        for reps in (0,-1,100001,1.5):
            with self.assertRaises(ValueError):
                analyze_csv(mocked_csv(),verify_source=False,reps=reps)

    def test_no_source_is_no_go(self):
        with tempfile.TemporaryDirectory() as d:
            main(['--out',d])
            receipt=json.loads(Path(d,'stage28_chance_baseline_outcomes.json').read_text())
            self.assertEqual(receipt['status'],'NO_GO_NO_PINNED_AUTHOR_SOURCE')
            self.assertEqual(receipt['new_bees'],0)

    def test_no_biological_or_stage24_payoff_claim(self):
        x=analyze_csv(mocked_csv(),verify_source=False,reps=30)
        self.assertEqual(x['real_animal_new_collection'],0)
        self.assertFalse(x['stage24_8world_model_empirically_validated'])
        self.assertTrue(x['no_causal_paid_query_reward_gain_claim'])
        self.assertTrue(x['raw_author_trial_data_not_redistributed'])


if __name__=='__main__':
    unittest.main()
