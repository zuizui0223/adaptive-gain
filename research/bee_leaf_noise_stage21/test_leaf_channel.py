"""Stage21: independent normalized Bayesian oracle with noisy U and V reveals.

All states are purely mathematical. No bee signal accuracy, motor cost, or
fitness has been observed. Every original signal can be displayed at most once.
"""
from fractions import Fraction as F
from itertools import product
import unittest

from leaf_channel import optimal_values, sharp_v_threshold, decision_grid
from asymmetric_root import exact_values as perfect_leaves_stage20

WORLDS=tuple(product((0,1),repeat=3))
ACTIONS=("SKIP","U","V")

def independent_posterior_oracle(q,c,s0,s1,a_u,a_v):
    q,c,s0,s1,a_u,a_v=[F(str(v)) for v in (q,c,s0,s1,a_u,a_v)]
    prior={(r,u,v):F(1,4)*(q if u else 1-q) for r,u,v in WORLDS}
    def guess(post):
        return max(sum((wt for (r,u,v),wt in post.items()
                        if (u if r==0 else v)==t),F(0)) for t in (0,1))
    def observe(post,leaf):
        idx=1 if leaf=="U" else 2
        reliability=a_u if leaf=="U" else a_v
        for reading in (0,1):
            joint={w:wt*(reliability if w[idx]==reading else 1-reliability)
                   for w,wt in post.items()}
            mass=sum(joint.values(),F(0))
            if mass:
                yield mass,{w:wt/mass for w,wt in joint.items() if wt}
    def request(post,leaf,continuation):
        return -c+sum((p*continuation(next_post)
                       for p,next_post in observe(post,leaf)),F(0))
    def first(post,leaf):
        other="V" if leaf=="U" else "U"
        return request(post,leaf,lambda after_first:max(
            guess(after_first),request(after_first,other,guess)))
    arms={}
    probs={}
    for z in (0,1):
        joint={w:p*((s0 if z==0 else 1-s0) if w[0]==0
                    else (1-s1 if z==0 else s1)) for w,p in prior.items()}
        pz=sum(joint.values(),F(0))
        probs[z]=pz
        post={w:wt/pz for w,wt in joint.items() if wt}
        arms[z]={"SKIP":guess(post),"U":first(post,"U"),"V":first(post,"V")}
    active=sum((probs[z]*max(arms[z].values()) for z in (0,1)),F(0))
    fixed=max(sum((probs[z]*arms[z][a] for z in (0,1)),F(0)) for a in ACTIONS)
    return active,fixed,probs,arms

class NoisyLeafTests(unittest.TestCase):
    def test_perfect_leafs_exactly_recover_stage20_for_all_root_classes(self):
        for q in (0,.2,.4,.5):
            for c in (0,.08,.25,.4):
                for s0,s1 in ((.5,.5),(.6,.8),(.8,.6),(1.,1.)):
                    with self.subTest(q=q,c=c,s0=s0,s1=s1):
                        observed=optimal_values(q,c,s0,s1,1.,1.)
                        old=perfect_leaves_stage20(q,c,s0,s1)
                        self.assertAlmostEqual(observed["contingent_optimum"],old["contingent_optimum"],places=12)
                        self.assertAlmostEqual(observed["precommit_optimum"],old["precommit_optimum"],places=12)
    def test_8world_posterior_with_separate_leaf_accuracies_and_optional_second_leaf(self):
        for q in (0,.2,.5):
            for c in (0,.12,.25,.4):
                for s0,s1 in ((.5,.5),(.6,.8),(.8,.6),(.9,.9)):
                    for accuracy_u,accuracy_v in ((.5,.5),(.6,.9),(.9,.6),(1.,1.)):
                        with self.subTest(q=q,c=c,s0=s0,s1=s1,au=accuracy_u,av=accuracy_v):
                            ref=independent_posterior_oracle(q,c,s0,s1,accuracy_u,accuracy_v)
                            result=optimal_values(q,c,s0,s1,accuracy_u,accuracy_v)
                            self.assertAlmostEqual(result["contingent_optimum"],ref[0],places=11)
                            self.assertAlmostEqual(result["precommit_optimum"],ref[1],places=11)
                            self.assertAlmostEqual(result["value_of_contingency"],ref[0]-ref[1],places=11)
                            self.assertAlmostEqual(result["observed_z_probability"]["0"],ref[2][0],places=11)
    def test_sharp_leaf_reliability_threshold_with_unequal_root_errors(self):
        boundary=sharp_v_threshold(.8,.6)
        self.assertEqual(boundary["threshold_fraction"],"14/15")
        self.assertAlmostEqual(boundary["minimum_v_accuracy_for_strict_positive_gain"],14/15,places=12)
        for v in (.5,.65,.8,.9,14/15,.94,.95,1.):
            with self.subTest(v=v):
                out=optimal_values(.2,.25,.8,.6,1,v)
                self.assertAlmostEqual(out["value_of_contingency"],max(0,.3*v-.28),places=12)
                self.assertEqual(out["first_action_after_z"]["0"],"SKIP")
                self.assertEqual(out["first_action_after_z"]["1"],"V" if v>14/15+1e-12 else "SKIP")
    def test_sharp_fixed_q_and_c_surface_unaffected_by_accuracy_of_irrelevant_u(self):
        for s0 in (.5,.6,.8,1.):
            for s1 in (.5,.7,.9,1.):
                for au in (.5,.7,1.):
                    for av in (.5,.75,.9,.95,1.):
                        with self.subTest(s0=s0,s1=s1,au=au,av=av):
                            out=optimal_values(.2,.25,s0,s1,au,av)
                            expected=max(0,(s1*(av-.75)-.55*(1-s0))/2)
                            self.assertAlmostEqual(out["value_of_contingency"],expected,places=11)
                            self.assertEqual(out["precommit_first_action"],"SKIP")
    def test_same_mean_leaf_accuracy_can_have_positive_or_zero_gain(self):
        a=optimal_values(.2,.25,.8,.6,.8,1.)
        b=optimal_values(.2,.25,.8,.6,1.,.8)
        self.assertAlmostEqual(a["balanced_leaf_accuracy"],.9)
        self.assertAlmostEqual(b["balanced_leaf_accuracy"],.9)
        self.assertAlmostEqual(a["value_of_contingency"],.02)
        self.assertAlmostEqual(b["value_of_contingency"],0)
    def test_when_both_leafs_are_uninformative_queries_have_no_value(self):
        for s0,s1 in ((.5,.5),(.8,.6),(1.,1.)):
            for cost in (0,.01,.25,.5):
                val=optimal_values(.2,cost,s0,s1,.5,.5)
                self.assertAlmostEqual(val["value_of_contingency"],0,places=12)
    def test_root_no_information_erases_access_gain_despite_leaf_quality(self):
        for accuracy_u,accuracy_v in ((.5,.9),(.9,.5),(1.,1.)):
            x=optimal_values(.2,.25,.5,.5,accuracy_u,accuracy_v)
            self.assertAlmostEqual(x["value_of_contingency"],0,places=12)
    def test_sharp_threshold_can_be_unattainable_even_with_perfect_v(self):
        x=sharp_v_threshold(.5,.5)
        self.assertFalse(x["strict_positive_gain_possible_with_v_accuracy_at_most_one"])
        self.assertGreater(x["minimum_v_accuracy_for_strict_positive_gain"],1.)
        y=sharp_v_threshold(.8,.6)
        self.assertTrue(y["strict_positive_gain_possible_with_v_accuracy_at_most_one"])
    def test_grid_provenance_excludes_living_bees_or_colony_inference(self):
        g=decision_grid()
        self.assertEqual(g["status"],"STAGE21_SOURCE_FREE_NOISY_LEAF_EXACT_DECISION")
        self.assertTrue(g["no_real_bees"])
        self.assertTrue(g["no_measured_root_or_leaf_confusion"])
        self.assertGreaterEqual(len(g["grid"]),100)
    def test_invalid_cost_q_or_leaf_signal_accuracy_rejected(self):
        for vals in ((-.1,.25,.8,.6,.8,1),(.6,.25,.8,.6,.8,1),
                     (.2,-1,.8,.6,.8,1),(.2,.25,.49,.6,.8,1),
                     (.2,.25,.8,.6,.49,1),(.2,.25,.8,.6,.8,1.01),
                     (.2,.25,.8,.6,.8,float('nan'))):
            with self.subTest(vals=vals):
                with self.assertRaises(ValueError):optimal_values(*vals)

if __name__=="__main__":unittest.main()
