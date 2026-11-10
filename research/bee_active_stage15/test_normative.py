import unittest
from normative import worlds, target, contingent_first_leaf, precommit_leaf_queries, benchmark

class NormativeTests(unittest.TestCase):
    def test_exact_eight_worlds_and_target_values(self):
        w = worlds()
        self.assertEqual(len(w),8)
        self.assertEqual(len(set(w)),8)
        for r,u,v in w:
            self.assertEqual(target(r,u,v),u if r==0 else v)
    def test_conditional_first_leaf_is_exactly_relevant(self):
        for r,u,v in worlds():
            self.assertEqual(contingent_first_leaf(r), 'U' if r==0 else 'V')
    def test_any_fixed_precommit_requires_one_point_five_leaf_cues(self):
        for first in ('U','V'):
            self.assertEqual(sum(precommit_leaf_queries(r,first) for r,u,v in worlds())/8,1.5)
    def test_informational_saving_is_exact_with_full_accuracy(self):
        b=benchmark(cost=0.1)
        self.assertEqual(b['n_worlds'],8)
        self.assertEqual(b['contingent_leaf_queries'],1)
        self.assertEqual(b['precommit_leaf_queries'],1.5)
        self.assertEqual(b['query_saving'],0.5)
        self.assertAlmostEqual(b['full_accuracy_toy_payoff_difference'],0.05)
        self.assertFalse(b['observed_animal_result'])
    def test_guesses_not_conflated_with_full_certainty(self):
        with self.assertRaises(ValueError):benchmark(cost=-0.1)

if __name__ == '__main__':unittest.main()
