"""Stage19 source-free exact-Bayes test: root-cue recognition error.

Independent posterior-normalized reference calculation, distinct from
production's joint-mass dynamic program. No real bee data or inference.
"""
from fractions import Fraction as F
from itertools import product
import unittest

from root_noisy import optimal_values, threshold_witness, threshold_family, decision_grid

WORLDS=list(product((0,1),repeat=3))
ACTIONS=("SKIP","U","V")

def post_opt(q,c,s):
    """Independent normalized posterior recursion, not production machinery."""
    q,c,s=map(lambda x:F(str(x)),(q,c,s))
    prior={(r,u,v):F(1,4)*(q if u else 1-q) for r,u,v in WORLDS}
    def target(world):
        r,u,v=world
        return u if r==0 else v
    def choice_accuracy(p):
        return max(sum(x for world,x in p.items() if target(world)==t) for t in (0,1))
    def condition(p,leaf,bit):
        idx=1 if leaf=="U" else 2
        mass=sum(wt for world,wt in p.items() if world[idx]==bit)
        return mass,({world:wt/mass for world,wt in p.items()
                     if world[idx]==bit} if mass else {})
    def observation_value(p,leaf,continuation):
        return -c+sum(prob*continuation(new)
             for bit in (0,1)
             for prob,new in (condition(p,leaf,bit),) if prob)
    def one_leaf(p,leaf):
        other="V" if leaf=="U" else "U"
        return observation_value(p,leaf,lambda posterior:max(
            choice_accuracy(posterior),
            observation_value(posterior,other,choice_accuracy)))
    arms={}
    for z in (0,1):
        w={world:wt*(s if world[0]==z else 1-s) for world,wt in prior.items()}
        denom=sum(w.values())
        posterior={world:wt/denom for world,wt in w.items() if wt}
        arms[z]={"SKIP":choice_accuracy(posterior),
                 "U":one_leaf(posterior,"U"),"V":one_leaf(posterior,"V")}
    contingent=sum(max(v.values()) for v in arms.values())/2
    precommit=max(sum(v[act] for v in arms.values())/2 for act in ACTIONS)
    return contingent,precommit,arms

class Stage19Tests(unittest.TestCase):
    def test_exact_strict_threshold_is_eleven_sixteenths(self):
        w=threshold_witness()
        self.assertEqual(w["threshold_fraction"],"11/16")
        self.assertEqual(w["threshold_percent"],68.75)
        self.assertEqual(w["expected_gain_formula"],"max(0,2*s/5-11/40)")
        for s,gain in [(.5,0),(.6,0),(.6875,0),(.7,.005),(.75,.025),
                       (.9,.085),(1.,.125)]:
            x=optimal_values(.2,.25,s)
            self.assertAlmostEqual(x["contingent_minus_precommit"],gain,places=12)
            self.assertAlmostEqual(x["contingent_minus_precommit"],
                                   max(0,.4*s-.275),places=12)
    def test_threshold_changes_whether_to_query_not_just_which(self):
        a=optimal_values(.2,.25,.8)
        self.assertEqual(a["optimal_first_after_root"]["0"],"SKIP")
        self.assertEqual(a["optimal_first_after_root"]["1"],"V")
        self.assertEqual(a["optimal_first_precommit"],"SKIP")
        b=optimal_values(.2,.25,.6)
        self.assertEqual(b["optimal_first_after_root"]["0"],"SKIP")
        self.assertEqual(b["optimal_first_after_root"]["1"],"SKIP")
    def test_noisy_root_reduces_expected_value_in_exact_eight_world_oracle(self):
        for q in (0,.1,.2,.35,.5):
            for c in (0,.04,.1,.2,.25,.4,.6):
                for s in (.5,.65,.75,.9,1.):
                    with self.subTest(q=q,c=c,s=s):
                        expected=post_opt(q,c,s)
                        actual=optimal_values(q,c,s)
                        self.assertAlmostEqual(actual["contingent_optimum"],expected[0],places=11)
                        self.assertAlmostEqual(actual["precommit_optimum"],expected[1],places=11)
                        self.assertAlmostEqual(actual["contingent_minus_precommit"],expected[0]-expected[1],places=11)
    def test_no_information_on_root_has_no_adaptive_access_value(self):
        for q in (0,.1,.2,.5):
            for cost in (0,.01,.12,.25,.4,1.):
                v=optimal_values(q,cost,.5)
                self.assertAlmostEqual(v["contingent_minus_precommit"],0,places=12)
    def test_perfect_root_recovers_stage18_exact_case(self):
        x=optimal_values(.2,.25,1.)
        self.assertAlmostEqual(x["contingent_optimum"],.775)
        self.assertAlmostEqual(x["precommit_optimum"],.65)
        self.assertAlmostEqual(x["contingent_minus_precommit"],.125)
    def test_unverified_strong_root_strategy_can_lower_utility(self):
        x=optimal_values(.2,.25,.6)
        self.assertAlmostEqual(x["fixed_root0_skip_root1_v_minus_optimal_precommit"],-.035,places=12)
        self.assertAlmostEqual(x["contingent_minus_precommit"],0,places=12)
        y=optimal_values(.2,.25,.9)
        self.assertAlmostEqual(y["fixed_root0_skip_root1_v_minus_optimal_precommit"],.085,places=12)
    def test_unobserved_cost_and_signal_accuracy_never_claimed_as_measurements(self):
        grid=decision_grid()
        self.assertEqual(grid["status"],"STAGE19_EXACT_NOISY_ROOT_DECISION_SURFACE")
        self.assertTrue(grid["no_original_animal_data"])
        self.assertTrue(grid["no_root_cue_confusion_matrix_measured"])
        self.assertTrue(grid["not_an_actual_recruitment_or_fitness_estimate"])
        self.assertGreaterEqual(len(grid["grid"]),150)
    def test_sharp_threshold_curve_for_easy_branch_family_at_quarter_cost(self):
        # For R0 target U~Bern(q) with q<=1/4 and cost c=1/4,
        # sharp root-recognition threshold is (3/4-q)/(1-q).
        for q in (0,.05,.10,.15,.20,.24,.25):
            with self.subTest(q=q):
                record=threshold_family(q)
                threshold=(.75-q)/(1-q)
                self.assertAlmostEqual(record["minimum_s_for_strict_positive_gain"],threshold,places=11)
                self.assertAlmostEqual(record["max_gain_at_perfect_root"],.125,places=12)
                for s in (.5,.6,.65,.6875,.7,.75,.8,.9,1.):
                    result=optimal_values(q,.25,s)
                    predicted=max(0,((1-q)*s+q-.75)/2)
                    self.assertAlmostEqual(result["contingent_minus_precommit"],predicted,places=11)
                s_below=(.5+threshold)/2
                s_above=(threshold+1.)/2
                self.assertAlmostEqual(optimal_values(q,.25,s_below)["contingent_minus_precommit"],0,places=12)
                self.assertGreater(optimal_values(q,.25,s_above)["contingent_minus_precommit"],0)
    def test_more_predictable_easy_branch_requires_more_reliable_root_at_fixed_cost(self):
        q0=threshold_family(0)
        q20=threshold_family(.2)
        q25=threshold_family(.25)
        self.assertAlmostEqual(q0["minimum_s_for_strict_positive_gain"],.75)
        self.assertAlmostEqual(q20["minimum_s_for_strict_positive_gain"],.6875)
        self.assertAlmostEqual(q25["minimum_s_for_strict_positive_gain"],2/3)
        self.assertGreater(q0["minimum_s_for_strict_positive_gain"],
                           q20["minimum_s_for_strict_positive_gain"])
        self.assertGreater(q20["minimum_s_for_strict_positive_gain"],
                           q25["minimum_s_for_strict_positive_gain"])
    def test_invalid_parameter_or_root_signal_fails(self):
        for q,c,s in ((-.1,.25,1),(.51,.25,1),(.2,-.1,1),(.2,.25,.49),(.2,.25,1.01),
                      (.2,.25,float('nan'))):
            with self.assertRaises(ValueError):optimal_values(q,c,s)

if __name__=="__main__":
    unittest.main()
