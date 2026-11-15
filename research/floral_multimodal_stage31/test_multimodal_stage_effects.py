"""Stage31: independently verify only the SUPPORTED computation contracts.

All numerical fixtures are synthetic, and no fitted floral trait effect or
meta-analytic estimate is fabricated from these tests. The single FReD real
spectral record is independently audited by a pinned source-specific CI job.
"""
from __future__ import annotations

import math
import tempfile
import unittest
from pathlib import Path

from multimodal_stage_effects import (
    STAGES, MODALITIES,
    validate_source_ledger, log_odds_ratio, independent_time_log_ratio,
    binary_factorial_interaction, nested_stage_decomposition,
    validate_macro_trait_state, empty_meta_evidence_gate
)
from fred_spectral_pilot import audit_spectrum,main as fred_main

ROOT=Path(__file__).resolve().parent


class Stage31HierarchicalFloralSignalTests(unittest.TestCase):
    def test_seed_source_type_qa_not_a_meta_analysis(self):
        a=validate_source_ledger(ROOT/'VERIFIED_SOURCE_GRANULARITY_LEDGER.csv')
        self.assertGreaterEqual(a['total_source_rows'],20)
        self.assertGreaterEqual(a['experimental_rows'],7)
        self.assertGreaterEqual(a['existing_meta_rows'],2)
        self.assertEqual(a['independent_quantitative_effects_extracted'],0)
        self.assertTrue(a['not_a_systematic_search'])

    def test_signal_and_stages_are_not_forced_into_one_to_one_map(self):
        self.assertEqual(len(STAGES),8)
        for x in ('patch_detection','plant_approach','landing',
                  'within_flower_search','pollen_transfer','plant_fitness'):
            self.assertIn(x,STAGES)
        for x in ('display_size','display_density','scent_bouquet',
                  'scent_spatial_pattern','visible_color','nectar_guide_uv',
                  'age_color_change'):
            self.assertIn(x,MODALITIES)

    def test_binomial_log_odds_with_independent_arms(self):
        r=log_odds_ratio(30,100,20,100)
        self.assertAlmostEqual(r['estimate'],math.log((30*80)/(70*20)))
        self.assertAlmostEqual(r['sampling_variance'],
                               sum(1/x for x in (30,70,20,80)))
        self.assertFalse(r['continuity_correction_applied'])
        self.assertTrue(r['not_valid_as_independent_if_same_bees_repeated'])

    def test_zero_cell_guard_and_invalid_binary_data(self):
        x=log_odds_ratio(0,20,1,20)
        self.assertTrue(x['continuity_correction_applied'])
        self.assertTrue(math.isfinite(x['estimate']))
        for bad in ((-1,10,3,10),(20,10,3,10),(1,0,3,10),(True,10,3,10)):
            with self.assertRaises(ValueError):log_odds_ratio(*bad)

    def test_distinct_time_estimand_and_variance(self):
        a=independent_time_log_ratio(20,7.,2.,20,10.,3.)
        self.assertEqual(a['effect_family'],'log_time_saved')
        self.assertAlmostEqual(a['estimate'],math.log(10/7))
        self.assertAlmostEqual(a['sampling_variance'],
                               (4/(20*49))+(9/(20*100)))
        self.assertTrue(a['same_pollinators_need_paired_covariance'])
        for bad in ((1,7,2,20,10,3),(20,0,2,20,10,3),(20,7,-2,20,10,3)):
            with self.assertRaises(ValueError):independent_time_log_ratio(*bad)

    def test_scent_by_vision_interaction_is_not_simple_addition(self):
        z=binary_factorial_interaction(
            {'00':(40,100),'10':(60,100),
             '01':(50,100),'11':(80,100)})
        self.assertAlmostEqual(z['estimate'],.1)
        self.assertEqual(z['effect_family'],'additive_interaction_risk_difference')
        self.assertTrue(z['requires_independent_arm_units'])
        self.assertTrue(z['NOT_meta_result'])
        with self.assertRaises(ValueError):
            binary_factorial_interaction({'00':(10,20),'11':(15,20)})

    def test_nested_stage_probability_chain_exact_identity(self):
        treated=[100,90,65,55,45,35,25,18,12]
        control=[100,85,70,55,50,35,25,12,9]
        z=nested_stage_decomposition(treated,control)
        self.assertAlmostEqual(z['overall_log_success_ratio'],math.log(12/9))
        self.assertLess(z['stage_conditional_rates'][1]['log_ratio'],0)
        self.assertTrue(z['sampling_covariance_NOT_estimable_by_independent_stage_SE_sums'])
        for invalid in ([100,200,60,30,20,10,5,4,3],
                        [100,90,60,30,20,10,5,4],
                        [0,0,0,0,0,0,0,0,0]):
            with self.assertRaises(ValueError):
                nested_stage_decomposition(invalid,control)

    def test_macro_rgb_never_implies_uv_or_voc(self):
        base={
          'taxon_id':'EXAMPLE_001','source_id':'FAKE_TEST_ONLY',
          'source_url':'https://example.org/mock',
          'population_id':'MOCK_POP', 'rgb_observed':True,
          'uv_spectral_measured':False,'voc_measured':False,
          'age_or_pollination_state_measured':False,
          'guide_type':'unknown'
        }
        a=validate_macro_trait_state(base)
        self.assertTrue(a['uv_unknown'])
        self.assertTrue(a['voc_unknown'])
        self.assertTrue(a['age_change_unknown'])
        self.assertTrue(a['do_not_require_complete_traits'])
        bad=dict(base,guide_type='uv_measured')
        with self.assertRaisesRegex(ValueError,'RGB_INFERRED_FAKE_UV_GUIDE'):
            validate_macro_trait_state(bad)

    def test_fred_pilot_non_source_data_and_uv_guard(self):
        synthetic=b'157,300,0.1\n157,301,0.2\n157,400,0.4\n157,700,0.6\n'
        z=audit_spectrum(synthetic,verify_source=False)
        self.assertEqual(z['spectral_rows'],4)
        self.assertAlmostEqual(z['UV_300_399_arithmetic_mean_reflectance'],.15)
        self.assertAlmostEqual(z['visible_400_700_arithmetic_mean_reflectance'],.5)
        self.assertFalse(z['UV_guide_presence_inferred'])
        with self.assertRaisesRegex(ValueError,'SOURCE_HASH_CHANGED'):
            audit_spectrum(synthetic,verify_source=True)
        with self.assertRaisesRegex(ValueError,'DUPLICATED_WAVELENGTH'):
            audit_spectrum(synthetic+b'157,300,0.2\n',verify_source=False)

    def test_no_input_fred_has_hard_no_go(self):
        with tempfile.TemporaryDirectory() as tmp:
            fred_main(['--out',tmp])
            payload=Path(tmp,'stage31_one_FReD_spectrum_QA.json').read_text()
            self.assertIn('NO_GO_NO_PINNED_FRED_ORIGINAL_EXAMPLE',payload)

    def test_no_new_meta_effects_in_authoring_phase(self):
        g=empty_meta_evidence_gate()
        self.assertEqual(g['status'],'NO_GO_NO_SOURCE_EXTRACTED_TREATMENT_EFFECTS')
        self.assertEqual(g['numbers_of_original_experimental_effects'],0)
        self.assertTrue(g['floral_display_and_scent_are_not_locked_to_one_distance_class'])
        self.assertTrue(g['no_new_animal_or_plant_measurements'])


if __name__=='__main__':
    unittest.main()
