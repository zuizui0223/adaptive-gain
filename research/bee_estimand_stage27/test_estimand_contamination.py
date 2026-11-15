"""Stage27: source-free tests with invented records, not republished author CSV."""
import csv
import io
import json
import tempfile
import unittest
from pathlib import Path

from estimand_contamination import XorShift32, summarize, main
from audit_author_request_semantics import COLUMNS


def invented_csv():
    output=io.StringIO()
    wr=csv.DictWriter(output,fieldnames=COLUMNS,lineterminator='\n')
    wr.writeheader()
    tid=0
    for bee in ('MOCK_B1','MOCK_B2','MOCK_B3'):
        index=0
        for block in (0,50):
            for difficulty in ('Easy','Hard','Impossible'):
                for typ in ('Regular','Random_Free_Cue'):
                    index+=1
                    tid+=1
                    request=int(typ=='Random_Free_Cue' or difficulty!='Easy')
                    landed=int(typ=='Regular' and request==1)
                    row={k:'' for k in COLUMNS}
                    row.update({
                      'Trial_ID':str(tid),
                      'Bee_ID':bee,
                      'Trial_Number':str(block+index),
                      'Difficulty':difficulty,
                      'Trial_Type':typ,
                      'Info_Requested':str(request),
                      'Actually_Landed_On_Platform':str(landed),
                      'Post_Request_Accuracy':'1.0' if request else '',
                      'Is_Post_Request_Correct':'1.0' if request else '',
                      'Non_Request_Accuracy':'0.0' if not request else '',
                      'Is_Post_Non_Request_Correct':'0.0' if not request else ''
                    })
                    wr.writerow(row)
        # Each bee has the same scripted responses. This is a fake QA fixture.
    return output.getvalue().encode('utf-8')


class Stage27ContaminationTests(unittest.TestCase):
    def test_mock_paid_vs_free_information_flag_not_interchangeable(self):
        x=summarize(invented_csv(),verify_source=False,reps=50)
        self.assertEqual(x['status'],'SOURCE_FREE_SYNTHETIC_QA_ONLY')
        self.assertEqual(x['n_trials'],36)
        self.assertEqual(x['n_bee_ids'],3)
        self.assertEqual(x['naively_counted_information_flags'],30)
        self.assertEqual(x['actual_paid_voluntary_request_landings_regular_only'],12)
        self.assertEqual(x['automatic_free_cue_trials_in_naive_flag'],18)
        self.assertAlmostEqual(x['contaminated_fraction_of_naive_flags'],.6)
        self.assertTrue(x['pooled_flag_is_not_paid_request'])
        self.assertEqual(x['scientific_limits']['original_animals_newly_collected'],0)

    def test_mock_gradient_and_per_bee_aggregation(self):
        x=summarize(invented_csv(),verify_source=False,reps=50)
        y=x['trial_weighted']
        self.assertAlmostEqual(y['regular_paid_easy_to_impossible_gradient'],1.)
        self.assertAlmostEqual(y['naive_pooled_flag_easy_to_impossible_gradient'],.5)
        self.assertAlmostEqual(y['gradient_difference'],.5)
        self.assertAlmostEqual(y['gradient_relative_attenuation'],.5)
        per=x['equal_bee_level']['contamination_difference']
        self.assertEqual(per['n_positive'],3)
        self.assertAlmostEqual(per['equal_bee_mean'],.5)

    def test_trial_order_sensitivity(self):
        x=summarize(invented_csv(),verify_source=False,reps=50)
        for period in ('Early','Late'):
            v=x['early_late_trial_number_robustness'][period]
            self.assertAlmostEqual(v['regular_gradient'],1)
            self.assertAlmostEqual(v['naive_pooled_flag_gradient'],.5)
            self.assertAlmostEqual(v['contamination_difference'],.5)

    def test_deterministic_bee_resampling(self):
        a=summarize(invented_csv(),verify_source=False,reps=50,seed=20261115)
        b=summarize(invented_csv(),verify_source=False,reps=50,seed=20261115)
        self.assertEqual(a['individual_bee_cluster_bootstrap'],
                         b['individual_bee_cluster_bootstrap'])
        self.assertEqual(a['individual_bee_cluster_bootstrap']['unit'],
                         'Bee_ID not trial')
        self.assertTrue(a['individual_bee_cluster_bootstrap']
                       ['not_colony_robust_confidence_intervals'])

    def test_real_source_sha_is_required(self):
        with self.assertRaisesRegex(ValueError,'AUTHOR_SOURCE_BLOB_SHA_MISMATCH'):
            summarize(invented_csv(),verify_source=True,reps=20)

    def test_missing_bee_treatment_stratum_fails_closed(self):
        raw=invented_csv().decode().splitlines()
        head=raw[:1]
        from itertools import filterfalse
        # One subject receives no free-cue Impossible trial in the fixture.
        remaining=[v for v in raw[1:] if not (
            ',MOCK_B1,' in v and ',Impossible,Random_Free_Cue,' in v)]
        with self.assertRaisesRegex(ValueError,'MISSING_PER_BEE_DIFFICULTY'):
            summarize(('\n'.join(head+remaining)+'\n').encode(),
                      verify_source=False,reps=20)

    def test_bootstrap_replication_limits(self):
        for bad in (0,-1,100001,1.5):
            with self.assertRaises(ValueError):
                summarize(invented_csv(),verify_source=False,reps=bad)

    def test_rng_is_repeatable_and_bounded(self):
        a=XorShift32(20261115)
        b=XorShift32(20261115)
        seq1=[a.index(192) for _ in range(1000)]
        seq2=[b.index(192) for _ in range(1000)]
        self.assertEqual(seq1,seq2)
        self.assertTrue(all(0<=k<192 for k in seq1))
        self.assertGreater(len(set(seq1)),150)

    def test_no_source_is_hard_no_go(self):
        with tempfile.TemporaryDirectory() as t:
            main(['--out',t])
            doc=json.loads(Path(t,'stage27_estimand_contamination.json').read_text())
            self.assertEqual(doc['status'],'NO_GO_NO_PINNED_AUTHOR_SOURCE')
            self.assertTrue(doc['no_new_animals'])

    def test_source_row_order_invariance(self):
        rows=invented_csv().decode().splitlines()
        shuffled=('\n'.join(rows[:1]+list(reversed(rows[1:])))+'\n').encode()
        a=summarize(invented_csv(),verify_source=False,reps=30)
        b=summarize(shuffled,verify_source=False,reps=30)
        self.assertEqual(a['trial_weighted'],b['trial_weighted'])
        self.assertEqual(a['equal_bee_level'],b['equal_bee_level'])
        self.assertEqual(a['individual_bee_cluster_bootstrap'],
                         b['individual_bee_cluster_bootstrap'])


if __name__=='__main__':
    unittest.main()
