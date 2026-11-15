"""Stage29 SOURCE-FREE tests: exact probability arithmetic and no-go conditions.

No mock bee rows are attributed to real animals. Real author-data verification
is a separate pinned GitHub Actions run, never embedded in this test file.
"""
import json
import math
import tempfile
import unittest
from pathlib import Path

from conditional_chance_source_audit import (
    exact_binom_lower_tail,
    fixed_lambda_martingale,
    source_schema_audit,
    source_identification_receipt,
    source_no_cue_outcomes,
    main,
)


class ConditionalChanceSourceTests(unittest.TestCase):
    def test_small_exact_binomial_tail(self):
        x=exact_binom_lower_tail(4,1)
        self.assertEqual(int(x['exact_integer_numerator']),5)
        self.assertEqual(int(x['exact_integer_denominator']),16)
        self.assertEqual(x['lower_tail_probability'],5/16)
        self.assertTrue(x['not_a_confirmatory_inference'])

    def test_independently_known_fair_probability(self):
        x=exact_binom_lower_tail(883,183)
        self.assertEqual(x['n'],883)
        self.assertEqual(x['correct_at_most'],183)
        self.assertAlmostEqual(x['lower_tail_probability']/3.36948282844465e-72,1,places=10)

    def test_binomial_boundary_probability(self):
        self.assertEqual(exact_binom_lower_tail(6,0)['lower_tail_probability'],1/64)
        self.assertEqual(exact_binom_lower_tail(6,6)['lower_tail_probability'],1.)
        for n,k in [(4,1), (12,4), (20,3)]:
            left=exact_binom_lower_tail(n,k)['lower_tail_probability']
            right=1-exact_binom_lower_tail(n,n-k-1)['lower_tail_probability']
            self.assertAlmostEqual(left,right)

    def test_randomization_compatible_martingale_factor(self):
        lam=1.0
        score_right=math.exp(-lam/2)/math.cosh(lam/2)
        score_wrong=math.exp(lam/2)/math.cosh(lam/2)
        self.assertAlmostEqual(.5*(score_right+score_wrong),1.,places=14)
        x=fixed_lambda_martingale(883,183,lam)
        self.assertTrue(150<x['log_e_value']<155)
        self.assertTrue(1e-67<x['ville_inverse_bound_if_lambda_fixed_a_priori']<1e-66)
        self.assertTrue(x['RETROSPECTIVE_CALCULATION_NOT_PREREGISTERED'])
        self.assertTrue(x['SOURCE_RANDOMIZATION_NOT_VERIFIED'])
        self.assertTrue(x['NOT_EMPIRICAL_ANIMAL_P_VALUE'])

    def test_poor_accuracy_only_requires_huge_bias_under_independence(self):
        expected=.5-183/883
        self.assertGreater(expected,.29)
        self.assertAlmostEqual(1-183/883,.7927519818799547)
        self.assertTrue(expected>0)

    def test_invalid_counts_fail_closed(self):
        for n,k in ((0,0), (4,-1), (4,5), (1,2)):
            with self.assertRaises(ValueError):
                exact_binom_lower_tail(n,k)
            with self.assertRaises(ValueError):
                fixed_lambda_martingale(n,k)

    def test_invalid_lambda_fails_closed(self):
        for x in (0,-1,float('nan'),float('inf'),None,[]):
            with self.assertRaises(ValueError):
                fixed_lambda_martingale(10,2,x)

    def test_mismatched_author_source_raises(self):
        content=b'Trial_ID,Bee_ID,Trial_Number,Difficulty,Trial_Type,Info_Requested\n1,FAKE,1,Impossible,Regular,0\n'
        with self.assertRaisesRegex(ValueError,'AUTHOR_SOURCE_BLOB_SHA_MISMATCH'):
            source_schema_audit(content)
        with self.assertRaisesRegex(ValueError,'AUTHOR_SOURCE_BLOB_SHA_MISMATCH'):
            source_no_cue_outcomes(content)
        with self.assertRaisesRegex(ValueError,'AUTHOR_SOURCE_BLOB_SHA_MISMATCH'):
            source_identification_receipt(content)

    def test_absent_input_fails_source_gate_without_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            main(['--out',tmp])
            x=json.loads(Path(tmp,'stage29_conditional_chance_source_no_go.json').read_text())
            self.assertEqual(x['status'],'NO_GO_ORIGINAL_AUTHOR_TRIAL_FILE_UNAVAILABLE')
            self.assertEqual(x['original_source_animals_verified'],0)
            self.assertTrue(x['no_empirical_adaptation_claim'])

    def test_independence_not_assumed_from_a_numerical_p_value(self):
        x=exact_binom_lower_tail(883,183)
        m=fixed_lambda_martingale(883,183)
        self.assertIn('independent',x['ASSUMPTION'].lower())
        self.assertIn('predictable',m['ASSUMPTION'].lower())
        self.assertTrue(x['not_a_confirmatory_inference'])
        self.assertTrue(m['RETROSPECTIVE_CALCULATION_NOT_PREREGISTERED'])


if __name__ == '__main__':
    unittest.main()
