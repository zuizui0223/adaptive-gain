"""Independent normalized posterior oracle for distinct true-bit errors of U/V.

RED first, no original animals. Source bits R,U,V are iid *across trials*
and mutually independent within each eight-world trial, with root R fair,
U minority prior q, and V fair. Z root errors separately by true root;
Uobs/Vobs separately by true paid-leaf bit. Cost incurred for each requested
leaf once. Test's oracle does NOT import production dynamic helpers.
"""
from fractions import Fraction as F
from itertools import product
import unittest
from leaf_bit_confusion import exact_values, sharp_example, source_free_grid

WORLDS=tuple(product((0,1),repeat=3))
ACTIONS=("SKIP","U","V")

def reference(q,c,s0,s1,u0,u1,v0,v1):
    q,c,s0,s1,u0,u1,v0,v1=[F(str(x)) for x in (q,c,s0,s1,u0,u1,v0,v1)]
    prior={(r,u,v):F(1,4)*(q if u else 1-q) for r,u,v in WORLDS}
    def target(w):
        r,u,v=w;return u if r==0 else v
    def guess(p):
        return max(sum((wt for world,wt in p.items() if target(world)==t),F(0))
                   for t in (0,1))
    def reveal(p,leaf):
        pos=1 if leaf=="U" else 2
        correct0,correct1=(u0,u1) if leaf=="U" else (v0,v1)
        for obs in (0,1):
            w={state:wt*((correct0 if obs==0 else 1-correct0)
                         if state[pos]==0 else (1-correct1 if obs==0 else correct1))
               for state,wt in p.items()}
            mass=sum(w.values(),F(0))
            if mass:
                yield mass,{state:wt/mass for state,wt in w.items() if wt}
    def buy(p,leaf,next_decision):
        return -c+sum((mass*next_decision(posterior)
                      for mass,posterior in reveal(p,leaf)),F(0))
    def first(p,leaf):
        other="U" if leaf=="V" else "V"
        return buy(p,leaf,lambda po:max(guess(po),buy(po,other,guess)))
    prob={};branches={}
    for z in (0,1):
        joint={world:wt*((s0 if z==0 else 1-s0) if world[0]==0
                         else (1-s1 if z==0 else s1))
               for world,wt in prior.items()}
        prob[z]=sum(joint.values(),F(0))
        post={world:wt/prob[z] for world,wt in joint.items() if wt}
        branches[z]={"SKIP":guess(post),"U":first(post,"U"),"V":first(post,"V")}
    active=sum((prob[z]*max(branches[z].values()) for z in (0,1)),F(0))
    committed=max(sum((prob[z]*branches[z][a] for z in (0,1)),F(0))
                  for a in ACTIONS)
    return active,committed,prob,branches

class BitAsymmetricTests(unittest.TestCase):
    def test_exact_independent_bayes_oracle_across_source_posterior_cases(self):
        for q in (0,.2,.5):
            for c in (0,.10,.25,.4):
                for s0,s1 in ((.5,.5),(.8,.6),(.6,.8),(1.,1.)):
                    for u0,u1,v0,v1 in ((.5,.5,.5,.5),(.8,.7,.9,1.),
                                        (1.,.9,1.,.9),(.7,1.,.6,.9),
                                        (1.,1.,1.,1.)):
                        with self.subTest(q=q,c=c,s0=s0,s1=s1,u=(u0,u1),v=(v0,v1)):
                            expected=reference(q,c,s0,s1,u0,u1,v0,v1)
                            found=exact_values(q,c,s0,s1,u0,u1,v0,v1)
                            self.assertAlmostEqual(found["contingent_optimum"],expected[0],places=11)
                            self.assertAlmostEqual(found["precommit_optimum"],expected[1],places=11)
                            self.assertAlmostEqual(found["gain"],expected[0]-expected[1],places=11)
                            for z in (0,1):
                                self.assertAlmostEqual(found["observed_z_probability"][str(z)],expected[2][z],places=11)
    def test_reduces_exactly_to_stage21_when_both_leaf_bit_errors_symmetric(self):
        from leaf_channel import optimal_values as stage21
        for s0,s1 in ((.5,.5),(.8,.6),(1.,1.)):
            for au,av in ((.5,.5),(.6,.9),(.9,.6),(1.,1.)):
                old=stage21(.2,.25,s0,s1,au,av)
                new=exact_values(.2,.25,s0,s1,au,au,av,av)
                self.assertAlmostEqual(new["gain"],old["value_of_contingency"],places=12)
                self.assertAlmostEqual(new["contingent_optimum"],old["contingent_optimum"],places=12)
    def test_sharp_q20_quarter_cost_full_reliability_domain(self):
        for s0 in (.5,.6,.8,1.):
            for s1 in (.5,.6,.8,1.):
                for u0,u1 in ((.5,.5),(.8,1.),(1.,.5)):
                    for v0,v1 in ((.5,.5),(.8,1.),(.9,.95),(1.,.9),(1.,1.)):
                        actual=exact_values(.2,.25,s0,s1,u0,u1,v0,v1)
                        expected=max(0, s1*(v0+v1-1.5)/4 +
                                     (1-s0)*(.15*v0-.15*v1-.275))
                        self.assertAlmostEqual(actual["gain"],expected,places=11)
                        self.assertAlmostEqual(actual["precommit_optimum"],.65,places=11)
                        self.assertEqual(actual["first_action_after_z"]["0"],"SKIP")
                        self.assertEqual(actual["first_action_after_z"]["1"],
                                         "V" if expected>1e-12 else "SKIP")
                        self.assertEqual(actual["first_action_precommit"],"SKIP")
    def test_same_v_balanced_accuracy_but_different_direction_of_error(self):
        a=exact_values(.2,.25,.8,.6,.5,1.,1.,.9)
        b=exact_values(.2,.25,.8,.6,1.,.5,.9,1.)
        self.assertAlmostEqual(a["v_balanced_bit_accuracy"],.95)
        self.assertAlmostEqual(b["v_balanced_bit_accuracy"],.95)
        self.assertAlmostEqual(a["gain"],.008)
        self.assertAlmostEqual(b["gain"],.002)
        self.assertGreater(a["gain"],b["gain"])
    def test_unrequested_u_accuracy_irrelevant_only_for_frozen_example(self):
        baseline=exact_values(.2,.25,.8,.6,.5,.5,1.,.9)
        other=exact_values(.2,.25,.8,.6,1.,1.,1.,.9)
        self.assertAlmostEqual(baseline["gain"],other["gain"],places=12)
        self.assertAlmostEqual(other["gain"],.008)
    def test_v_readout_uninformative_has_no_gain(self):
        for u0,u1 in ((.5,.5),(1.,1.)):
            x=exact_values(.2,.25,.8,.6,u0,u1,.5,.5)
            self.assertEqual(x["first_action_after_z"]["1"],"SKIP")
            self.assertAlmostEqual(x["gain"],0.,places=12)
    def test_source_free_metadata_is_never_bee_evidence(self):
        out=source_free_grid()
        self.assertEqual(out["status"],"STAGE22_FOUR_LEAF_BIT_ERRORS_EXACT_BAYES")
        self.assertTrue(out["no_real_bee_data"])
        self.assertTrue(out["all_payoff_costs_hypothetical"])
        self.assertGreaterEqual(len(out["grid"]),100)
    def test_original_source_values_outside_orientation_domain_fail_closed(self):
        for args in ((-.1,.25,.8,.6,.8,.9,.9,1),
                     (.2,.25,.8,.6,.4,.9,.9,1),
                     (.2,.25,.8,.6,.8,.9,.9,1.1),
                     (.2,-1,.8,.6,.8,.9,.9,1),
                     (.2,.25,float("nan"),.6,.8,.9,.9,1)):
            with self.subTest(args=args):
                with self.assertRaises(ValueError):exact_values(*args)

if __name__=="__main__":unittest.main()
