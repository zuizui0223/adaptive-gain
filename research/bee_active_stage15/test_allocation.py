import unittest
from collections import Counter, defaultdict
from allocation import generate, audit, audit_mode_balance

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
                self.assertEqual(sum(x['access_mode']=='contingent' for x in b),8)
                self.assertEqual(sum(x['access_mode']=='precommit' for x in b),8)
    def test_independent_with_replacement_worlds_have_repeated_states(self):
        rows=generate(2,2,seed=17)
        groups=defaultdict(list)
        for x in rows:
            groups[x['colony_id'],x['bee_id'],x['block'],x['access_mode']].append((x['r'],x['u'],x['v']))
        repeated=sum(len(set(v))<len(v) for v in groups.values())
        self.assertGreater(repeated,0)
        self.assertEqual(audit(rows)['world_sampling'],'iid_with_replacement_per_trial')
    def test_wrong_mode_balance_fails(self):
        rows=generate(2,2,seed=17)
        rows[0]['access_mode']='precommit' if rows[0]['access_mode']=='contingent' else 'contingent'
        with self.assertRaisesRegex(ValueError,'MODE'):audit(rows)
    def test_world_target_is_not_a_predictive_visual_leak(self):
        r=generate(2,2,seed=17)
        self.assertTrue(all(x['world_concealed_from_subject'] for x in r))
        self.assertTrue(all(x['study_design_is_synthetic_QA_only'] for x in r))
    def test_duplicate_trial_rejected(self):
        r=generate(2,2,seed=17)
        r[1]=dict(r[0])
        with self.assertRaisesRegex(ValueError,'DUPLICATE'):audit(r)

if __name__=='__main__':unittest.main()
