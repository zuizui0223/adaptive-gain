"""Exact stochastic wind/weather and delayed other-species cue routing tests."""
import unittest
from fractions import Fraction as F
from adaptive_gain.stochastic_weather import optimal_accuracy, fixed_accuracy, four_contexts
from adaptive_gain.deadline_mixture import (
    hidden_deadline_accuracy, announced_deadline_accuracy, mixed_contexts
)

class StochasticWeatherTests(unittest.TestCase):
    def test_static_limit_agrees_with_prior_exact_budget(self):
        x=optimal_accuracy(4,5,(0,1),F(1,10),source_costs=((1,1),(1,1)),
                           survival=(F(1),F(1)))
        self.assertEqual(x,F(643,800))
        self.assertEqual(fixed_accuracy(4,5,survival=(F(1),F(1))),F(21,32))

    def test_exact_32_world_p05_guaranteed_5(self):
        r=four_contexts(4,5,F(1,2))
        self.assertEqual(r['AB'],F(798184801,1280000000))
        self.assertEqual(r['interaction'],F(371849,320000000))
        self.assertEqual(r['fixed'],F(14601,25000))

    def test_hard_cap_mixture_without_announcement(self):
        r=mixed_contexts(4,((3,F(1,2)),(7,F(1,2))),stay=F(1,2))
        self.assertEqual(r['hidden']['AB'],F(77375740429,128000000000))
        self.assertEqual(r['announced']['AB'],F(499142757493,819200000000))
        self.assertEqual(r['hidden']['interaction'],F(-250610779,32000000000))
        self.assertEqual(r['hidden']['fixed'],F(362433,625000))
        self.assertEqual(r['announced']['none'],r['hidden']['none'])
        self.assertGreater(r['announced']['AB'],r['hidden']['AB'])

    def test_non_announcement_never_improves_any_of_four_cases(self):
        for p in [F(1,10),F(1,2),F(9,10)]:
            r=mixed_contexts(4,((3,F(1,2)),(7,F(1,2))),stay=p)
            for x in ('none','A','B','AB'):
                self.assertGreaterEqual(r['announced'][x],r['hidden'][x])
                self.assertGreaterEqual(r['hidden'][x],r['hidden']['fixed'])
            self.assertGreaterEqual(r['hidden']['AB'],r['hidden']['A'])

    def test_single_known_budget_recovers_same_model(self):
        for p in [F(1,10),F(1,2),F(9,10)]:
            params=dict(d=4,bits=(0,1),error=F(1,10),
                source_costs=((1,1),(1,2)),stay=p)
            self.assertEqual(hidden_deadline_accuracy(((5,F(1)),),**params),
                optimal_accuracy(budget=5,**params))

    def test_equal_wind_survival_and_cue_costs_remove_persistence_effect(self):
        values=[optimal_accuracy(4,5,(0,1),F(1,10),
                source_costs=((1,1),(1,1)),
                survival=(F(4,5),F(4,5)),stay=p,
                initial=(F(1),F(0))) for p in (F(1,10),F(1,2),F(9,10))]
        self.assertEqual(len(set(values)),1)

    def test_invalid_deadline_distribution_rejected(self):
        with self.assertRaises(ValueError):
            hidden_deadline_accuracy(((3,F(1,3)),(7,F(1,3))))

if __name__=='__main__':unittest.main()
