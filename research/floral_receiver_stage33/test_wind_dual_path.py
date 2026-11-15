"""Stage33: wind-scoped EXACT artificial-world tests. No real experiments."""
import unittest
from fractions import Fraction as F
from pathlib import Path
from wind_dual_path import (
    dual_wind_decomposition,wind_scenarios_source_free,
    inspect_wind_source_ledger,measurement_contract
)

ROOT=Path(__file__).resolve().parent


class WindTwoPathTests(unittest.TestCase):
    def test_moderate_wind_can_raise_arrival_but_harm_landing(self):
        r=wind_scenarios_source_free()['moderate_wind']['decomposition']
        self.assertEqual(r['original_per_opportunity_transfer'],F(9,50))
        self.assertEqual(r['windy_per_opportunity_transfer'],F(9,40))
        self.assertEqual(r['odour_or_other_detection_component'],F(9,50))
        self.assertEqual(r['mechanical_landing_component'],-F(27,200))
        self.assertEqual(r['per_landing_pollen_transfer_component'],F(0))
        self.assertEqual(r['wind_minus_calm'],F(9,200))
        self.assertEqual(r['break_even_windy_landing_probability_if_transfer_unchanged'],F(2,5))
        self.assertTrue(r['ordered_decomposition_is_not_a_statistical_mediation_test'])

    def test_strong_wind_reverses_net_sign_despite_larger_plume_reach(self):
        r=wind_scenarios_source_free()['strong_wind']['decomposition']
        self.assertGreater(r['odour_or_other_detection_component'],0)
        self.assertLess(r['mechanical_landing_component'],0)
        self.assertLess(r['wind_minus_calm'],0)
        self.assertEqual(r['wind_minus_calm'],-F(3,40))

    def test_compensatory_sensory_motor_skill_can_reverse_again(self):
        source=wind_scenarios_source_free()
        comp=source['strong_wind_with_visual_motor_compensation']['decomposition']
        uncomp=source['strong_wind']['decomposition']
        self.assertEqual(comp['wind_minus_calm'],F(3,16))
        self.assertLess(uncomp['wind_minus_calm'],0)
        self.assertTrue(source['no_wind_speed_threshold_unless_measured'])

    def test_wind_can_increase_pollen_transfer_even_when_less_visitation(self):
        calm={'discovery':F(1,2),'landing_given_discovery':F(4,5),
              'transfer_given_landing':F(3,10)}
        wind={'discovery':F(2,5),'landing_given_discovery':F(3,5),
              'transfer_given_landing':F(4,5)}
        r=dual_wind_decomposition(calm,wind)
        self.assertLess(r['odour_or_other_detection_component'],0)
        self.assertLess(r['mechanical_landing_component'],0)
        self.assertGreater(r['per_landing_pollen_transfer_component'],0)
        self.assertEqual(r['original_per_opportunity_transfer'],F(3,25))
        self.assertEqual(r['windy_per_opportunity_transfer'],F(24,125))
        self.assertEqual(r['wind_minus_calm'],F(9,125))

    def test_zero_detection_or_transfer_has_no_division_by_zero(self):
        calm={'discovery':F(0),'landing_given_discovery':F(1),
              'transfer_given_landing':F(0)}
        windy={'discovery':F(1),'landing_given_discovery':F(1),
               'transfer_given_landing':F(0)}
        out=dual_wind_decomposition(calm,windy)
        self.assertEqual(out['wind_minus_calm'],F(0))
        self.assertIsNone(out['break_even_windy_landing_probability_if_transfer_unchanged'])

    def test_input_must_be_real_probabilities_not_proxy_guild_scores(self):
        good={'discovery':F(1,2),'landing_given_discovery':F(1,2),
              'transfer_given_landing':F(1,2)}
        for corrupt in (
          dict(good,landing_given_discovery=F(4,3)),
          dict(good,discovery=-1),
          dict(good,transfer_given_landing=0.5),
          dict(good,incorrect_outcome=F(0))
        ):
            with self.assertRaises(ValueError):
                dual_wind_decomposition(good,corrupt)

    def test_pinned_prior_art_provenance_separate_positive_negative_and_guild(self):
        x=inspect_wind_source_ledger(ROOT/'WIND_DUAL_PATH_EVIDENCE_LEDGER.csv')
        self.assertGreaterEqual(x['distinct_reference_rows'],9)
        self.assertFalse(x['all_effect_sizes_from_original_raw_studies_extracted'])
        self.assertTrue(x['no_claim_of_same_cohort_between_scent_and_landing_studies'])
        self.assertIn('10.5061/dryad.4qrfj6qpf',x['original_dataset_candidates'])

    def test_original_observation_contract_explicit_missingness(self):
        base={
            'original_session_id':'MOCK_SESSION',
            'plant_individual_id':'MOCK_PLANT',
            'receiver_id':'MOCK_POLLINATOR',
            'original_source_url':'https://example.org/mock',
            'mean_wind_m_s':1.5,
            'wind_direction_deg':90,
            'gust_sd_m_s':0.3,
            'flower_sway_displacement_cm':None,
            'plume_encounter_observed':None,
            'discovery_observed':False,
            'landing_observed':None,
            'pollen_transfer_observed':None,
        }
        x=measurement_contract(base)
        self.assertEqual(x['status'],'OBSERVATION_CONTRACT_VALID_NOT_CAUSAL')
        self.assertFalse(x['plume_measured'])
        self.assertFalse(x['flower_sway_measured'])
        self.assertFalse(x['all_events_directly_observed'])
        with self.assertRaises(ValueError):
            measurement_contract(dict(base,landing_observed=False))
        with self.assertRaises(ValueError):
            measurement_contract(dict(base,mean_wind_m_s=-2))
        with self.assertRaises(ValueError):
            measurement_contract(dict(base,plume_encounter_observed=0))

    def test_source_identity_cannot_be_assumed_from_wind_speed_alone(self):
        # same wind does not identify odour intermittency or flower motion
        base={
            'original_session_id':'MOCK',
            'plant_individual_id':'MOCK_P',
            'receiver_id':'MOCK_B',
            'original_source_url':'https://example.org/a',
            'mean_wind_m_s':2.5,
            'wind_direction_deg':None,
            'gust_sd_m_s':None,
            'flower_sway_displacement_cm':None,
            'plume_encounter_observed':None,
            'discovery_observed':None,
            'landing_observed':None,
            'pollen_transfer_observed':None,
        }
        z=measurement_contract(base)
        self.assertFalse(z['all_events_directly_observed'])
        self.assertFalse(z['plume_measured'])


if __name__=='__main__':
    unittest.main()
