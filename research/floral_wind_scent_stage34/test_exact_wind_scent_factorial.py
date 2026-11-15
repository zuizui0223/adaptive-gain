"""Stage34 source-free test cases, no newly measured floral outcomes."""
import unittest
from fractions import Fraction as F

from exact_wind_scent_factorial import (
    full_factorial, constructed_counterexample, preexisting_source_design_gate
)


class ScentByWindStageTest(unittest.TestCase):
    def test_positive_detection_interaction_can_coexist_with_negative_net_wind(self):
        z=constructed_counterexample()
        self.assertEqual(z['wind_x_scent_detection_interaction'],F(1,5))
        self.assertEqual(z['wind_x_scent_pollen_interaction'],F(21,400))
        self.assertEqual(z['wind_effect_on_pollen_transfer_if_scent_on'],-F(3,200))
        self.assertEqual(z['wind_effect_on_pollen_transfer_if_scent_off'],-F(27,400))
        self.assertFalse(z['wind_on_scented_flower_absolute_benefit'])
        self.assertTrue(z['positive_relative_scent_wind_detection_advantage'])
        self.assertTrue(z['no_original_four_arm_data_supplied'])

    def test_no_wind_response_in_any_cell_has_zero_interaction(self):
        s={'discovery':F(1,2),'landing_given_discovery':F(1,2),
           'pollen_given_landing':F(4,5)}
        z=full_factorial({
            'calm_scent_off':s,'wind_scent_off':s,
            'calm_scent_on':s,'wind_scent_on':s})
        self.assertEqual(z['wind_x_scent_detection_interaction'],F(0))
        self.assertEqual(z['wind_x_scent_pollen_interaction'],F(0))

    def test_positive_discovery_interaction_does_not_force_positive_pollen_interaction(self):
        # A theoretically possible scent-dependent landing penalty can reverse
        # the sign of the full pollination interaction.
        off0={'discovery':F(1,2),'landing_given_discovery':F(4,5),
              'pollen_given_landing':F(1)}
        off1={'discovery':F(1,2),'landing_given_discovery':F(3,5),
              'pollen_given_landing':F(1)}
        on0={'discovery':F(1,2),'landing_given_discovery':F(4,5),
             'pollen_given_landing':F(1)}
        on1={'discovery':F(4,5),'landing_given_discovery':F(1,10),
             'pollen_given_landing':F(1)}
        z=full_factorial(dict(zip(
            ('calm_scent_off','wind_scent_off','calm_scent_on','wind_scent_on'),
            (off0,off1,on0,on1)
        )))
        self.assertGreater(z['wind_x_scent_detection_interaction'],0)
        self.assertLess(z['wind_x_scent_pollen_interaction'],0)

    def test_odor_plume_could_be_disrupted_in_strong_wind(self):
        base={'landing_given_discovery':F(1,2),'pollen_given_landing':F(1)}
        off={**base,'discovery':F(2,5)}
        calm_on={**base,'discovery':F(3,5)}
        wind_on={**base,'discovery':F(1,5)}
        z=full_factorial({
            'calm_scent_off':off,'wind_scent_off':off,
            'calm_scent_on':calm_on,'wind_scent_on':wind_on})
        self.assertEqual(z['wind_x_scent_detection_interaction'],-F(2,5))
        self.assertLess(z['wind_x_scent_pollen_interaction'],0)

    def test_invalid_probability_or_missing_arm_fails(self):
        s={'discovery':F(1,2),'landing_given_discovery':F(1,2),
           'pollen_given_landing':F(1,2)}
        all4={k:s for k in (
            'calm_scent_off','wind_scent_off',
            'calm_scent_on','wind_scent_on')}
        with self.assertRaisesRegex(ValueError,'MISSING_WIND_OR_SCENT_CELL'):
            full_factorial({k:v for k,v in all4.items() if k!='calm_scent_off'})
        with self.assertRaisesRegex(ValueError,'OUT_OF_RANGE'):
            full_factorial(dict(all4,wind_scent_on=dict(s,discovery=F(5,4))))
        with self.assertRaisesRegex(ValueError,'NON_EXACT'):
            full_factorial(dict(all4,wind_scent_on=dict(s,discovery=.5)))

    def test_prior_studies_are_not_joined_into_fictitious_factorial(self):
        evidence=preexisting_source_design_gate()
        self.assertEqual(evidence['status'],
                         'NO_GO_NO_ORIGINAL_2X2_WIND_BY_SCENT_EXPERIMENT_EXTRACTED')
        self.assertTrue(evidence['no_valid_pooled_cross_paper_interaction'])
        self.assertEqual(evidence['zero_empirical_2x2_effects_extracted'],True)
        self.assertTrue(evidence['not_a_meta_analytical_result'])


if __name__=='__main__':
    unittest.main()
