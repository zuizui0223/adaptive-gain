"""Independent Bayes-posterior oracle for asymmetric root-cue confusion.

Tests are EXACT MATHEMATICS with synthetic binary worlds, not bees.
A root 0 is recognized with sensitivity s0=P(Z=0|R=0), root 1 with
s1=P(Z=1|R=1). Both are constrained to >=.5 for this sharp theorem.
"""
from fractions import Fraction as F
from itertools import product
import unittest
from asymmetric_root import exact_values, threshold_boundary, matched_average_accuracy, decision_grid
from root_noisy import optimal_values as symmetric_stage19

WORLDS=tuple(product((0,1),repeat=3))
ACTIONS=("SKIP","U","V")

def posterior_oracle(q,c,s0,s1):
    """Independent normalized posterior dynamic optimization for 8 worlds."""
    q,c,s0,s1=(F(str(x)) for x in (q,c,s0,s1))
    prior={(r,u,v):F(1,4)*(q if u else 1-q) for r,u,v in WORLDS}
    def target(world):
        r,u,v=world
        return u if r==0 else v
    def accuracy(p):
        return max(sum((v for w,v in p.items() if target(w)==k),F(0)) for k in (0,1))
    def condition(p,leaf,bit):
        idx=1 if leaf=="U" else 2
        joint={w:wt for w,wt in p.items() if w[idx]==bit}
        prob=sum(joint.values(),F(0))
        return prob,({w:wt/prob for w,wt in joint.items()} if prob else {})
    def query(p,leaf,next_step):
        total=-c
        for bit in (0,1):
            prob,new=condition(p,leaf,bit)
            if prob:
                total+=prob*next_step(new)
        return total
    def first(p,leaf):
        second="V" if leaf=="U" else "U"
        return query(p,leaf,lambda post:max(accuracy(post),query(post,second,accuracy)))
    branches={}
    marginal={}
    for z in (0,1):
        joint={w:pr*((s0 if z==0 else 1-s0) if w[0]==0 else ((1-s1) if z==0 else s1))
               for w,pr in prior.items()}
        pz=sum(joint.values(),F(0))
        marginal[z]=pz
        posterior={w:wt/pz for w,wt in joint.items() if wt}
        branches[z]={"SKIP":accuracy(posterior),"U":first(posterior,"U"),
                     "V":first(posterior,"V")}
    contingent=sum((marginal[z]*max(branches[z].values()) for z in (0,1)),F(0))
    pre=max(sum((marginal[z]*branches[z][action] for z in (0,1)),F(0))
            for action in ACTIONS)
    return contingent,pre,marginal,branches

class Stage20IndependentOracleTests(unittest.TestCase):
    def test_extends_symmetric_stage19_without_rewriting_it(self):
        for s in (.5,.65,.6875,.7,.8,.9,1.):
            x=exact_values(.2,.25,s,s)
            y=symmetric_stage19(.2,.25,s)
            self.assertAlmostEqual(x["contingent_optimum"],y["contingent_optimum"],places=12)
            self.assertAlmostEqual(x["precommit_optimum"],y["precommit_optimum"],places=12)
            self.assertAlmostEqual(x["value_of_contingency"],y["contingent_minus_precommit"],places=12)
    def test_full_bayes_oracle_on_asymmetric_error_grid_and_varied_costs(self):
        for q in (0.,.2,.4):
            for cost in (0.,.10,.25,.4):
                for s0 in (.5,.65,.8,1.):
                    for s1 in (.5,.7,.9,1.):
                        with self.subTest(q=q,cost=cost,s0=s0,s1=s1):
                            t=exact_values(q,cost,s0,s1)
                            cont,pre,pz,branches=posterior_oracle(q,cost,s0,s1)
                            self.assertAlmostEqual(t["contingent_optimum"],cont,places=11)
                            self.assertAlmostEqual(t["precommit_optimum"],pre,places=11)
                            self.assertAlmostEqual(t["value_of_contingency"],cont-pre,places=11)
                            self.assertAlmostEqual(t["observed_z_probability"]["0"],pz[0],places=11)
                            self.assertAlmostEqual(t["observed_z_probability"]["1"],pz[1],places=11)
    def test_fixed_q20_cquarter_exact_sharp_plane(self):
        for s0 in (.5,.6,.7,.8,.9,1.):
            for s1 in (.5,.6,.7,.8,.9,1.):
                x=exact_values(.2,.25,s0,s1)
                expected=max(0,(11*s0+5*s1-11)/40)
                self.assertAlmostEqual(x["value_of_contingency"],expected,places=12)
                self.assertAlmostEqual(x["precommit_optimum"],.65,places=12)
                self.assertEqual(x["first_action_after_z"]["0"],"SKIP")
                self.assertEqual(x["first_action_after_z"]["1"],
                                 "V" if 11*s0+5*s1>11+1e-12 else "SKIP")
    def test_balanced_accuracy_is_insufficient_to_predict_gain(self):
        a=matched_average_accuracy(.8,.6,.6,.8)
        self.assertAlmostEqual(a["same_balanced_accuracy"],.7)
        self.assertAlmostEqual(a["first_gain"],.02)
        self.assertAlmostEqual(a["second_gain"],0.)
        self.assertGreater(a["first_gain"],a["second_gain"])
        b=matched_average_accuracy(.9,.7,.7,.9)
        self.assertAlmostEqual(b["same_balanced_accuracy"],.8)
        self.assertAlmostEqual(b["first_gain"],.06)
        self.assertAlmostEqual(b["second_gain"],.03)
    def test_boundary_is_observed_class_specific_not_pooled(self):
        b=threshold_boundary(.6)
        self.assertAlmostEqual(b["s1_threshold_for_positive_value"],.88)
        self.assertFalse(b["above_threshold_at_s1_equal_half"])
        a=threshold_boundary(.8)
        self.assertAlmostEqual(a["s1_threshold_for_positive_value"],.44)
        self.assertTrue(a["above_threshold_at_s1_equal_half"])
        c=threshold_boundary(.5)
        self.assertGreater(c["s1_threshold_for_positive_value"],1.)
        self.assertFalse(c["positive_possible_in_theorem_accuracy_domain"])
    def test_overconfident_forced_policy_can_have_negative_gain(self):
        x=exact_values(.2,.25,.6,.8)
        self.assertAlmostEqual(x["value_of_contingency"],0.)
        self.assertAlmostEqual(x["fixed_skip0_v1_minus_precommit"],-.01)
        y=exact_values(.2,.25,.8,.6)
        self.assertAlmostEqual(y["value_of_contingency"],.02)
    def test_average_individual_gains_not_equal_gain_at_average_confusion(self):
        a=exact_values(.2,.25,.9,.9)
        b=exact_values(.2,.25,.5,.5)
        mean_gain=(a["value_of_contingency"]+b["value_of_contingency"])/2
        pooled=exact_values(.2,.25,.7,.7)["value_of_contingency"]
        self.assertAlmostEqual(mean_gain,.0425)
        self.assertAlmostEqual(pooled,.005)
        self.assertGreater(mean_gain,pooled)
    def test_invalid_precision_and_scope_fail_closed(self):
        for args in [(.2,.25,.49,.7),(.2,.25,.7,1.01),(.2,-.1,.8,.8),
                     (.51,.25,.8,.8),(.2,.25,float("nan"),.8)]:
            with self.assertRaises(ValueError):
                exact_values(*args)
    def test_grid_no_animals_or_measured_sensitivity_claimed(self):
        g=decision_grid()
        self.assertEqual(g["status"],"STAGE20_ASYMMETRIC_CONFUSION_EXACT_BAYES_GRID")
        self.assertTrue(g["no_real_bees_observed"])
        self.assertTrue(g["per_root_class_accuracy_unmeasured"])
        self.assertGreaterEqual(len(g["grid"]),70)

if __name__=="__main__":
    unittest.main()
