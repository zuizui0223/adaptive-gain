"""Stage22 parameter-interval robustness; hypothetical bounds, not animal CIs."""
from fractions import Fraction as F
from itertools import product
import unittest
from interval_robustness import bound_value
from leaf_bit_confusion import exact_values

class RobustnessTests(unittest.TestCase):
    def test_point_rectangle_recovers_exact_gain(self):
        box={'s0':(.8,.8),'s1':(.6,.6),'v0':(1.,1.),'v1':(.9,.9)}
        x=bound_value(box)
        self.assertAlmostEqual(x['smallest_possible_gain'],.008,places=12)
        self.assertAlmostEqual(x['largest_possible_gain'],.008,places=12)
        self.assertEqual(x['status'],'POSITIVE_FOR_ALL_ASSUMED_PARAMETERS')
    def test_point_positive_cannot_be_promoted_if_uncertainty_crosses_zero(self):
        box={'s0':(.79,.81),'s1':(.59,.61),'v0':(.92,1.),'v1':(.85,.95)}
        x=bound_value(box)
        self.assertEqual(x['smallest_possible_gain'],0.)
        self.assertGreater(x['largest_possible_gain'],0.)
        self.assertEqual(x['status'],'INCONCLUSIVE_FOR_SOME_ASSUMED_PARAMETERS')
        self.assertTrue(x['not_a_confidence_interval_without_source_coverage'])
    def test_narrow_intervals_can_robustly_prove_positive_within_the_model(self):
        x=bound_value({'s0':(.8,.8),'s1':(.6,.6),
                       'v0':(.99,1.),'v1':(.96,1.)})
        self.assertAlmostEqual(x['smallest_possible_gain'],.0134,places=12)
        self.assertGreater(x['smallest_possible_gain'],0.)
    def test_exact_corner_enumeration_bounds_inside_parameter_rectangle(self):
        box={'s0':(.7,.85),'s1':(.6,.9),'v0':(.7,1.),'v1':(.8,1.)}
        out=bound_value(box)
        for s0 in (.7,.72,.81,.85):
            for s1 in (.6,.7,.9):
                for v0 in (.7,.85,1.):
                    for v1 in (.8,.9,1.):
                        val=exact_values(.2,.25,s0,s1,.5,.5,v0,v1)['gain']
                        self.assertGreaterEqual(val+1e-10,out['smallest_possible_gain'])
                        self.assertLessEqual(val-1e-10,out['largest_possible_gain'])
    def test_invalid_or_nonphysical_parameter_intervals_fail_closed(self):
        for box in [
            {'s0':(.8,.7),'s1':(.6,.6),'v0':(.9,1.),'v1':(.9,1.)},
            {'s0':(.8,.8),'s1':(.49,.6),'v0':(.9,1.),'v1':(.9,1.)},
            {'s0':(.8,.8),'s1':(.6,.6),'v0':(.9,1.1),'v1':(.9,1.)},
            {'s0':(.8,.8),'s1':(.6,.6),'v0':(.9,1.)}
        ]:
            with self.subTest(box=box):
                with self.assertRaises(ValueError):bound_value(box)
if __name__=="__main__": unittest.main()
