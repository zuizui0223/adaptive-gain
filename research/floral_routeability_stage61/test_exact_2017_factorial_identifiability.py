"""Mock exact fractions only: not Lawson bee outcome observations."""
import unittest,itertools
from fractions import Fraction as F
from exact_2017_factorial_identifiability import (
    ORIGINAL_2017_WIND_ARM_KEYS,EXAMPLE,ALL_CELLS,
    exact_bounds,observed_cells,three_factor_additive_interaction,
    wind_vision_at_odor_one
)

class FourArmMissingWindScentVisualExperimentContract(unittest.TestCase):
    def test_published_four_arms_and_missing_cells_exact(self):
        x=exact_bounds(EXAMPLE)
        self.assertEqual(len(ORIGINAL_2017_WIND_ARM_KEYS),4)
        self.assertEqual(len(ALL_CELLS),8)
        self.assertEqual(len(x["missing_factorial_wind_odor_visible_cells"]),4)
        self.assertEqual(x["published_original_bees_per_arm"],18)
        self.assertTrue(x["order_contingent_route_policy_unobserved"])

    def test_two_opposite_interaction_signs_with_IDENTICAL_observed_four_rates(self):
        k=observed_cells(EXAMPLE)
        low={**k,(0,0,0):F(1),(0,1,1):F(1),(0,0,1):F(0),(1,0,0):F(0)}
        high={**k,(0,0,0):F(0),(0,1,1):F(0),(0,0,1):F(1),(1,0,0):F(1)}
        for cell in ORIGINAL_2017_WIND_ARM_KEYS.values():
            self.assertEqual(low[cell],high[cell])
        self.assertEqual(three_factor_additive_interaction(low),F(-7,4))
        self.assertEqual(three_factor_additive_interaction(high),F(9,4))
        self.assertLess(wind_vision_at_odor_one(low),0)
        self.assertGreater(wind_vision_at_odor_one(high),0)

    def test_exact_bounds_from_independent_non_symbolic_linear_program_corner_oracle(self):
        r=exact_bounds(EXAMPLE)
        self.assertEqual(r["hypothetical_sharp_wind_by_visual_at_odor_one_bounds"],["-1/10","9/10"])
        self.assertEqual(r["hypothetical_sharp_wind_by_odor_by_visual_bounds"],["-7/4","9/4"])
        self.assertTrue(r["both_interactions_can_switch_sign_under_unmeasured_cells"])
        self.assertTrue(r["no_pollen_or_original_bee_rate_used_in_example"])

    def test_contingent_cue_order_requires_additional_randomization(self):
        p=observed_cells(EXAMPLE)
        with self.assertRaisesRegex(ValueError,"MISSING_NO_WIND"):
            wind_vision_at_odor_one(p)
        with self.assertRaisesRegex(ValueError,"ALL_EIGHT"):
            three_factor_additive_interaction(p)
        self.assertTrue(exact_bounds(EXAMPLE)["full_factorial_is_necessary_not_sufficient_for_cue_order_causal_claim"])

    def test_malformed_probabilities_or_non_2017_arm_gate(self):
        with self.assertRaisesRegex(ValueError,"FOUR_ARM"):
            exact_bounds({"odor":F(1,2)})
        with self.assertRaisesRegex(ValueError,"OUT_OF_RANGE"):
            exact_bounds({**EXAMPLE,"A_no_wind_odor_only":F(3,2)})
        with self.assertRaisesRegex(ValueError,"NOT_EXACT"):
            exact_bounds({**EXAMPLE,"A_no_wind_odor_only":0.5})
if __name__=="__main__":unittest.main()
