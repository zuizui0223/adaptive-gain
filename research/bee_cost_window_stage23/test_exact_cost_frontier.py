"""Stage23 source-free tests; independent normalized Bayes oracle below."""
import unittest
from fractions import Fraction as F
from itertools import product

from exact_cost_frontier import cost_window_certificate, policy_frontiers, _value

WORLDS=tuple(product((0,1),repeat=3))
RATES={'Z':(0,F(4,5),F(3,5)), 'U':(1,F(1),F(1)), 'V':(2,F(1),F(9,10))}


def independent_oracle(cost):
    # Probabilities are normalized afresh after every observation. This does
    # NOT call Stage23's unnormalized joint-mass policy frontier implementation.
    p={w:F(1,4)*(F(1,5) if w[1] else F(4,5)) for w in WORLDS}
    def update(distribution, kind, report):
        index,a0,a1=RATES[kind]
        weighted={w:v*((a0 if report==0 else 1-a0) if w[index]==0
                      else ((1-a1) if report==0 else a1))
                  for w,v in distribution.items()}
        total=sum(weighted.values(),F(0))
        if total==0:
            return F(0),None
        return total,{w:v/total for w,v in weighted.items()}
    def guess(d):
        return max(sum((prob for w,prob in d.items()
                        if (w[1] if w[0]==0 else w[2])==answer),F(0))
                   for answer in (0,1))
    def first(d,name):
        if name=='SKIP':
            return guess(d)
        other='V' if name=='U' else 'U'
        val=-cost
        for observed in (0,1):
            pobs,post=update(d,name,observed)
            if pobs==0:continue
            after_second=sum((pr*guess(post2) for report in (0,1)
                              for pr,post2 in [update(post,other,report)]
                              if pr>0),F(0))-cost
            val+=pobs*max(guess(post),after_second)
        return val
    expected={x:F(0) for x in ('SKIP','U','V')}
    contingent=F(0)
    for z in (0,1):
        prob,posterior=update(p,'Z',z)
        scores={name:first(posterior,name) for name in expected}
        contingent+=prob*max(scores.values())
        for name in expected:expected[name]+=prob*scores[name]
    return contingent,max(expected.values())


class ExactCostWindowTest(unittest.TestCase):
    def test_complete_cost_envelopes(self):
        c=cost_window_certificate()
        self.assertEqual(c['contingent_envelope'],[
            {'start':'0','end':'2/15','gross_correct':'419/500','expected_queries':'1'},
            {'start':'2/15','end':'27/100','gross_correct':'379/500','expected_queries':'2/5'},
            {'start':'27/100','end':None,'gross_correct':'13/20','expected_queries':'0'}])
        self.assertEqual(c['precommit_envelope'],[
            {'start':'0','end':'47/350','gross_correct':'419/500','expected_queries':'7/5'},
            {'start':'47/350','end':None,'gross_correct':'13/20','expected_queries':'0'}])

    def test_exact_boundary_values_and_peak(self):
        contingent,pre=policy_frontiers()
        samples={
            F(0):F(0), F(1,10):F(1,25), F(2,15):F(4,75),
            F(47,350):F(19,350), F(1,4):F(1,125),
            F(27,100):F(0), F(1,1):F(0)}
        for cost,delta in samples.items():
            with self.subTest(cost=cost):
                self.assertEqual(_value(contingent,cost)-_value(pre,cost),delta)

    def test_piecewise_formula_on_dense_rational_grid(self):
        contingent,pre=policy_frontiers()
        for i in range(0,401):
            c=F(i,1000)
            expected=(F(2,5)*c if c<=F(2,15) else
                      c-F(2,25) if c<=F(47,350) else
                      F(27,250)-F(2,5)*c if c<=F(27,100) else F(0))
            with self.subTest(cost=c):
                self.assertEqual(_value(contingent,c)-_value(pre,c),expected)

    def test_independent_normalized_bayes_oracle(self):
        contingent,pre=policy_frontiers()
        cases={F(i,200) for i in range(0,81)} | {
            F(2,15),F(47,350),F(27,100),F(1,4),F(1),F(5,4)}
        for c in sorted(cases):
            with self.subTest(cost=c):
                actual=independent_oracle(c)
                expected=(_value(contingent,c),_value(pre,c))
                self.assertEqual(actual,expected)

    def test_no_real_animal_claims(self):
        c=cost_window_certificate()
        self.assertTrue(c['no_real_animals'])
        self.assertTrue(c['no_empirical_cost_estimate'])
        self.assertTrue(c['not_ecological_fitness'])
        self.assertEqual(c['gain_at_stage22_cost_quarter'],'1/125')
        self.assertEqual(c['peak_gain'],'19/350')

if __name__=='__main__':
    unittest.main()
