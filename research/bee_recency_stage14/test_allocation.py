import unittest
from collections import Counter,defaultdict
from allocation import generate,audit,TIMING,WIND_SEQUENCES

class AllocationTests(unittest.TestCase):
    def test_2x2x2_with_64_per_bee(self):
        rows=generate(4,4);q=audit(rows,4,4)
        self.assertEqual(q['trials'],1024)
        self.assertEqual(q['source_arms'],8)
        self.assertEqual(set(q['arm_totals'].values()),{128})
        bybee=defaultdict(list)
        for r in rows:bybee[(r['colony_id'],r['bee_id'])].append(r)
        for subset in bybee.values():
            self.assertEqual(len(subset),64)
            self.assertEqual(set(Counter((r['wind'],r['order'],r['refresh']) for r in subset).values()),{8})
            for k in range(1,5):
                block=[r for r in subset if r['block']==k]
                self.assertEqual(len(block),16)
                self.assertEqual(set(Counter((r['order'],r['refresh'],r['reward_side']) for r in block).values()),{2})
    def test_latest_exposure_equalized_and_no_cues_at_gate(self):
        self.assertEqual(TIMING['first_off']-TIMING['first_on'],.75)
        self.assertEqual(TIMING['second_off']-TIMING['second_on'],.75)
        self.assertEqual(TIMING['refresh_off']-TIMING['refresh_on'],.75)
        self.assertLess(TIMING['refresh_off'],TIMING['gate'])
        rows=generate(2,2)
        self.assertTrue(all(not r['predictive_cues_visible_at_gate'] for r in rows))
        self.assertTrue(all(r['refresh_payload']=='reward_and_handling_simultaneous' for r in rows if r['refresh']=='informative'))
    def test_unsafe_gate_and_refresh_payload_fail_closed(self):
        a=generate(2,2);a[0]['both_feeders_open_at_s']=4
        with self.assertRaisesRegex(ValueError,'GATE'):audit(a)
        a=generate(2,2)
        a[0]['refresh']='informative' if a[0]['refresh']=='sham' else 'sham'
        with self.assertRaisesRegex(ValueError,'REFRESH'):audit(a)
    def test_allocation_is_explicitly_mock_and_public_only(self):
        q=audit(generate(2,2))
        self.assertTrue(q['synthetic_QA_only'])
        self.assertTrue(q['actual_animal_assignments_must_be_private_and_new'])
        self.assertNotIn('per_animal_schedule',q)
if __name__=='__main__':unittest.main()