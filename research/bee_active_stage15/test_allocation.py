import unittest
from collections import Counter, defaultdict
from allocation import generate, audit, audit_world_balance

class AllocationTests(unittest.TestCase):
    def test_four_colony_balance_of_mode_and_concealed_eight_worlds(self):
        rows=generate(n_colonies=4,bees_per_colony=4,seed=17)
        report=audit(rows)
        self.assertEqual(report['n_trials'],4*4*64)
        self.assertEqual(report['n_bees'],16)
        self.assertEqual(report['n_independent_colonies'],4)
        self.assertEqual(set(report['cell_counts'].values()),{256})
        bybee=defaultdict(list)
        for r in rows:bybee[(r['colony_id'],r['bee_id'])].append(r)
        for bee,sub in bybee.items():
            for block in range(1,5):
                b=[r for r in sub if r['block']==block]
                self.assertEqual(len(b),16)
                for mode in ('contingent','precommit'):
                    assert set((x['r'],x['u'],x['v']) for x in b if x['access_mode']==mode)==set((r,u,v) for r in (0,1) for u in (0,1) for v in (0,1))
    def test_wrong_world_balance_fails(self):
        rows=generate(2,2,seed=17)
        rows[0]['u']=1-rows[0]['u']
        with self.assertRaisesRegex(ValueError,'WORLD'):audit(rows)
    def test_world_target_is_not_a_predictive_visual_leak(self):
        r=generate(2,2,seed=17)
        self.assertTrue(all(x['world_concealed_from_subject'] for x in r))
        self.assertTrue(all(x['study_design_is_synthetic_QA_only'] for x in r))
    def test_duplicate_trial_rejected(self):
        r=generate(2,2,seed=17)
        r[1]=dict(r[0])
        with self.assertRaisesRegex(ValueError,'DUPLICATE'):audit(r)

if __name__=='__main__':unittest.main()
