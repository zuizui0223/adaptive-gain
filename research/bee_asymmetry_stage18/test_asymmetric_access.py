"""Independent full-world posterior oracle for root-conditioned stopping.

TEST-FIRST. All data in this file are imagined binary decision worlds, not
actual observations from bees. The oracle must not call implementation
helpers beyond the public result functions under test.
"""
import itertools
import unittest
from math import isclose
from asymmetric_access import values, maximum_value, condition_grid, sample_hidden_worlds

WORLD=list(itertools.product((0,1),repeat=3))

def probabilities(q):
    return {(r,u,v):.25*(q if u else 1-q) for r,u,v in WORLD}

def guess(post):
    return max(sum(p for (r,u,v),p in post.items() if (u if r==0 else v)==target)
               for target in (0,1))

def query(post,leaf,c,next_action):
    result=-c
    for bit in (0,1):
        subset={state:p for state,p in post.items()
                if state[1 if leaf=="U" else 2]==bit}
        prob=sum(subset.values())
        if prob>0:
            result+=prob*next_action({world:p/prob for world,p in subset.items()})
    return result

def after_first(post,first,c):
    other="V" if first=="U" else "U"
    return max(guess(post),query(post,other,c,guess))

def oracle(q,c):
    prior=probabilities(q)
    root_posterior={}
    for r in (0,1):
        subset={state:p for state,p in prior.items() if state[0]==r}
        root_posterior[r]={state:p/.5 for state,p in subset.items()}
    cont=0.
    for r in (0,1):
        post=root_posterior[r]
        actions=[guess(post)]
        for leaf in ("U","V"):
            actions.append(query(post,leaf,c,lambda po,leaf=leaf:after_first(po,leaf,c)))
        cont+=.5*max(actions)
    pre=[]
    pre.append(.5*sum(guess(root_posterior[r]) for r in (0,1)))
    for leaf in ("U","V"):
        pre.append(.5*sum(query(root_posterior[r],leaf,c,
                         lambda po,leaf=leaf:after_first(po,leaf,c)) for r in (0,1)))
    return cont,max(pre)

class AsymmetricSourceTests(unittest.TestCase):
    def test_state_dependent_skip_is_optimal_only_for_reliability_asymmetry(self):
        x=values(q=.2,c=.25)
        self.assertEqual(x["root0_best"],"SKIP")
        self.assertEqual(x["root1_best"],"V")
        self.assertAlmostEqual(x["contingent_value"],.775)
        self.assertAlmostEqual(x["precommit_value"],.65)
        self.assertAlmostEqual(x["access_value_gain"],.125)
        self.assertTrue(x["root_state_changes_whether_to_query"])
        self.assertFalse(x["empirical"])
        y=values(q=.5,c=.25)
        self.assertEqual(y["root0_best"],"U")
        self.assertEqual(y["root1_best"],"V")
        self.assertFalse(y["root_state_changes_whether_to_query"])
    def test_closed_form_exactly_matches_independent_8_world_dp(self):
        for q in (0.,.05,.10,.20,.25,.30,.40,.50):
            for c in (0.,.01,.07,.10,.15,.2,.25,.28,.3,.35,.4,.5,.6,1.):
                with self.subTest(q=q,c=c):
                    actual=values(q,c)
                    benchmark=oracle(q,c)
                    self.assertAlmostEqual(actual["contingent_value"],benchmark[0],places=11)
                    self.assertAlmostEqual(actual["precommit_value"],benchmark[1],places=11)
    def test_global_cost_optimum_as_function_of_branch_uncertainty(self):
        known={0:(.25,.125),.05:(.25,.125),.20:(.25,.125),
               .25:(.25,.125),.30:(.8/3,.8/6),.40:(.30,.15),
               .50:(1/3,1/6)}
        for q,(cost,gain) in known.items():
            x=maximum_value(q)
            self.assertAlmostEqual(x["attaining_cost"],cost,places=11)
            self.assertAlmostEqual(x["max_access_value"],gain,places=11)
            self.assertAlmostEqual(values(q,cost)["access_value_gain"],gain,places=11)
            for i in range(101):
                self.assertGreaterEqual(gain+1e-9,values(q,i/100)["access_value_gain"])
    def test_source_switching_and_optional_skipping_have_distinct_contributions(self):
        z=values(.2,.25)
        self.assertAlmostEqual(z["mandatory_contingent_value"],.75)
        self.assertAlmostEqual(z["mandatory_precommit_value"],.65)
        self.assertAlmostEqual(z["mandatory_access_gain"],.10)
        self.assertAlmostEqual(z["optional_minus_mandatory_access_gain"],.025)
        self.assertGreater(z["optional_minus_mandatory_access_gain"],0.)
        high=values(.2,.50)
        self.assertAlmostEqual(high["access_value_gain"],0.)
        self.assertGreater(high["mandatory_access_gain"],0.)
        self.assertLess(high["optional_minus_mandatory_access_gain"],0.)
    def test_free_and_unaffordable_queries_both_erase_value(self):
        for q in (0,.05,.20,.3,.5):
            self.assertAlmostEqual(values(q,0)["access_value_gain"],0)
            self.assertAlmostEqual(values(q,.5)["access_value_gain"],0)
            self.assertAlmostEqual(values(q,1)["access_value_gain"],0)
    def test_conditional_stopping_window_is_q_less_than_c_less_than_half(self):
        for q in (0,.05,.2,.4):
            mid=(q+.5)/2
            a=values(q,mid)
            self.assertTrue(a["root_state_changes_whether_to_query"])
            self.assertEqual(a["root0_best"],"SKIP")
            self.assertEqual(a["root1_best"],"V")
    def test_independent_with_replacement_q20_worlds_are_not_depleted(self):
        rows=sample_hidden_worlds(10000,q=.2,seed=20261111)
        self.assertEqual(len(rows),10000)
        self.assertGreater(len(set(rows)),1)
        self.assertTrue(any(rows[i]==rows[i+1] for i in range(len(rows)-1)))
        p0=sum(r==0 for r,u,v in rows)/len(rows)
        p_rare=sum(u for r,u,v in rows)/len(rows)
        p_v=sum(v for r,u,v in rows)/len(rows)
        self.assertAlmostEqual(p0,.5,delta=.02)
        self.assertAlmostEqual(p_rare,.2,delta=.02)
        self.assertAlmostEqual(p_v,.5,delta=.02)
    def test_invalid_q_or_cost_is_rejected(self):
        for q,c in ((-.1,.2),(.6,.2),(.2,-.1),(.2,float('nan'))):
            with self.subTest(q=q,c=c):
                with self.assertRaises(ValueError):values(q,c)
    def test_grid_contains_no_claims_about_real_animals(self):
        z=condition_grid()
        self.assertEqual(z["status"],"EXACT_STATE_DEPENDENT_STOP_DECISION_TOPOLOGY")
        self.assertTrue(z["zero_original_bee_measurements"])
        self.assertGreater(len(z["cases"]),50)

if __name__=="__main__":unittest.main()
