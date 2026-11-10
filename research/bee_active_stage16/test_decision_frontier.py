"""Stage16 test-first exact two-mode query value, independent eight-world Bayesian oracle.

Synthetic/math only: no animal behavior or empirical cue learning outcomes.
"""
import itertools
import unittest
from decision_frontier import best_values, mandatory_first_leaf_values, theoretical_ceiling, decision_grid

STATES=list(itertools.product((0,1), repeat=3))

def posterior(signal,root_reliability,known=None):
    known=known or {}
    weights=[]
    for R,U,V in STATES:
        world={'U':U,'V':V}
        if any(world[k]!=v for k,v in known.items()):
            weights.append(0.)
            continue
        weights.append((root_reliability if signal==R else 1-root_reliability)/8)
    z=sum(weights)
    if z<=0:raise ValueError("ZERO_POSTERIOR")
    return [w/z for w in weights]

def guess_payoff(weights):
    successes=[]
    for target in (0,1):
        successes.append(sum(w for w,(r,u,v) in zip(weights,STATES)
            if (u if r==0 else v)==target))
    return max(successes)

def cue_value(weights,key,continuation):
    values=[]
    for bit in (0,1):
        post=[weight if ((U if key=="U" else V)==bit) else 0.
              for weight,(R,U,V) in zip(weights,STATES)]
        prob=sum(post)
        if prob>0:values.append(prob*continuation([x/prob for x in post]))
    return sum(values)

def oracle(root_reliability,cost):
    """Independent brute Bayesian optimization: guess, first U/V, optional second."""
    def after_one(weights,seen):
        other='V' if seen=='U' else 'U'
        return max(guess_payoff(weights),
                   -cost+cue_value(weights,other,guess_payoff))
    def after_signal(weights):
        return max([guess_payoff(weights)]+[
            -cost+cue_value(weights,key,lambda posterior, key=key:after_one(posterior,key))
            for key in ('U','V')])
    signal_post=[posterior(signal,root_reliability) for signal in (0,1)]
    contingent=sum(after_signal(p) for p in signal_post)/2
    precommit=max([sum(guess_payoff(p) for p in signal_post)/2]+[
        -cost+sum(cue_value(p,key,lambda post,key=key:after_one(post,key))
                  for p in signal_post)/2
        for key in ('U','V')])
    return contingent,precommit

class DecisionFrontierTests(unittest.TestCase):
    def test_old_full_information_low_cost_benchmark_is_not_a_general_law(self):
        r=best_values(root_reliability=1.,leaf_cost=.10)
        self.assertAlmostEqual(r["contingent_net"],.9)
        self.assertAlmostEqual(r["precommit_net"],.85)
        self.assertAlmostEqual(r["value_of_contingency"],.05)
        self.assertFalse(r["empirical"])
    def test_closed_form_matches_independent_eight_world_bayes_oracle(self):
        for reliability in (.5,.55,.6,.7,.75,.9,1.):
            for cost in (0.,.01,.07,.1,.2,.25,.3,1/3,.4,.5,.7):
                with self.subTest(s=reliability,c=cost):
                    a,b=oracle(reliability,cost)
                    z=best_values(root_reliability=reliability,leaf_cost=cost)
                    self.assertAlmostEqual(z["contingent_net"],a,places=11)
                    self.assertAlmostEqual(z["precommit_net"],b,places=11)
                    self.assertAlmostEqual(z["value_of_contingency"],a-b,places=11)
    def test_absence_of_usable_root_information_removes_adaptive_value(self):
        for cost in (.0,.01,.1,.25,.4,.8):
            self.assertAlmostEqual(best_values(.5,cost)["value_of_contingency"],0.,places=12)
    def test_free_queries_have_no_payoff_value_despite_saving_query_count(self):
        for reliability in (.5,.6,.8,1.):
            self.assertAlmostEqual(best_values(reliability,0.)["value_of_contingency"],0.,places=12)
    def test_extreme_query_costs_make_both_arms_guess(self):
        for reliability in (.5,.6,.8,1.):
            z=best_values(reliability,reliability/2+.01)
            self.assertAlmostEqual(z["contingent_net"],.5,places=12)
            self.assertAlmostEqual(z["precommit_net"],.5,places=12)
    def test_nonmonotonic_rational_gain_and_exact_ceiling(self):
        z=theoretical_ceiling(1.)
        self.assertAlmostEqual(z["max_value_of_contingency"],1/6)
        self.assertAlmostEqual(z["attaining_leaf_cost"],1/3)
        y=theoretical_ceiling(.6)
        self.assertAlmostEqual(y["max_value_of_contingency"],.05)
        self.assertAlmostEqual(best_values(.6,.15)["value_of_contingency"],.05)
        self.assertAlmostEqual(theoretical_ceiling(.5)["max_value_of_contingency"],0.)
    def test_grid_labels_are_math_not_animals(self):
        g=decision_grid()
        self.assertEqual(g["status"],"EXACT_ANALYTICAL_BAYES_DECISION_FRONTIER")
        self.assertTrue(g["no_real_animals"])
        self.assertTrue(g["no_behavioral_effect_estimated"])
        self.assertGreater(len(g["rows"]),30)
        self.assertTrue(all(z["value_of_contingency"]>=-1e-12 for z in g["rows"]))
    def test_stage15_mandatory_first_request_differs_from_optional_skip_game(self):
        forced=mandatory_first_leaf_values(1.,.8)
        option=best_values(1.,.8)
        self.assertAlmostEqual(forced["contingent_net"],.2)
        self.assertAlmostEqual(forced["precommit_net"],-.05)
        self.assertAlmostEqual(forced["value_of_contingency"],.25)
        self.assertAlmostEqual(option["contingent_net"],.5)
        self.assertAlmostEqual(option["precommit_net"],.5)
        self.assertAlmostEqual(option["value_of_contingency"],0.)
        self.assertFalse(forced["may_skip_first_leaf"])
        self.assertTrue(option["may_skip_first_leaf"])
    def test_forced_first_leaf_gain_is_min_of_root_advantage_and_second_query_cost(self):
        for reliability in (.5,.6,.75,1.):
            for cost in (0,.05,.1,.2,.4,.6,1.):
                with self.subTest(s=reliability,c=cost):
                    r=mandatory_first_leaf_values(reliability,cost)
                    self.assertAlmostEqual(r["value_of_contingency"],
                         min((reliability-.5)/2,cost/2),places=11)
    def test_optional_first_policy_dominates_forced_first_policy(self):
        for reliability in (.5,.6,.8,1.):
            for cost in (0,.1,.3,.6,1.):
                a=best_values(reliability,cost)
                b=mandatory_first_leaf_values(reliability,cost)
                self.assertGreaterEqual(a["contingent_net"]+1e-10,b["contingent_net"])
                self.assertGreaterEqual(a["precommit_net"]+1e-10,b["precommit_net"])
    def test_invalid_root_reliability_or_cost_fails_closed(self):
        for args in [(.49,.1),(1.01,.1),(.9,-.1),(.9,float("nan")),("0.9",.1)]:
            with self.subTest(args=args):
                with self.assertRaises(ValueError):best_values(*args)

if __name__=="__main__": unittest.main()
