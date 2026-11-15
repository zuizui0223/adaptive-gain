"""Stage33 focused regression of exact source-free models and evidence firewall."""
from fractions import Fraction as F
from pathlib import Path
import unittest

from receiver_cognition_route_value import (
  receiver_cue_value,whole_route_decomposition,source_species_atlas,
  compare_joint_evidence,source_free_counterexamples,original_design_context_audit
)

HERE=Path(__file__).resolve().parent


class ReceiverCognitionVsPollinationTest(unittest.TestCase):
    def test_eight_species_all_learn_no_invented_scores(self):
        x=source_species_atlas(HERE/'KANDORI_2021_EIGHT_TAXA_TASK_ATLAS.csv')
        self.assertEqual(x['eight_species'],8)
        self.assertTrue(x['reported_learning_present_for_all_eight'])
        self.assertTrue(x['higher_rate_Bombus_ignitus_in_this_task'])
        self.assertTrue(x['slow_learning_is_not_random_behavior'])
        self.assertEqual(x['numeric_learning_rate_effects_extracted'],0)
        self.assertFalse(x['cross_task_efficiency_or_fitness_measured'])
        self.assertTrue(x['not_a_global_cognitive_ranking'])

    def test_original_published_8_species_odor_reward_arena_confounding(self):
        x=original_design_context_audit(HERE/'KANDORI_2021_PUBLISHED_DESIGN_CONTEXT_TABLE1.csv')
        self.assertEqual(x['status'],'PUBLISHED_ORIGINAL_TABLE1_CONFONDERS_DOCUMENTED')
        self.assertEqual(x['taxa_checked'],8)
        self.assertEqual(x['sucrose_bees_and_hoverflies_percent'],40)
        self.assertEqual(x['sucrose_butterflies_percent'],10)
        self.assertTrue(x['honey_odor_added_to_bees_and_hoverflies_only'])
        self.assertTrue(x['different_training_color_pairs_across_species'])
        self.assertTrue(x['different_flower_sizes_and_arenas_across_species'])
        self.assertTrue(x['Bombus_ignitus_one_colony_reported'])
        self.assertTrue(x['cannot_identify_order_or_sociality_effect_separately_from_these_design_factors_in_one_study'])

    def test_higher_cue_use_is_not_necessarily_higher_pollen_gain(self):
        x=source_free_counterexamples()
        self.assertEqual(x['high_cue_use_low_transfer_plant_gain'],F(9,100))
        self.assertEqual(x['lower_cue_use_high_transfer_plant_gain'],F(27,250))
        self.assertGreater(x['lower_cue_use_high_transfer_plant_gain'],
                           x['high_cue_use_low_transfer_plant_gain'])
        self.assertTrue(x['all_parameters_assumed_source_free'])

    def test_no_cue_usage_has_zero_signal_specific_gain(self):
        x=receiver_cue_value(
            encounter=F(1),cue_use=F(0),
            baseline_correct_route=F(1,2),
            cued_correct_route=F(1),
            pollen_delivery_if_correct_route=F(1),
            processing_cost=F(1))
        self.assertEqual(x['plant_per_opportunity_transfer_delta'],F(0))
        self.assertEqual(x['receiver_per_opportunity_net_delta'],F(0))

    def test_attraction_cue_value_hits_ceiling_when_baseline_perfect(self):
        x=receiver_cue_value(
            encounter=F(1),cue_use=F(1),
            baseline_correct_route=F(1),
            cued_correct_route=F(1),
            pollen_delivery_if_correct_route=F(1))
        self.assertEqual(x['plant_per_opportunity_transfer_delta'],F(0))

    def test_motor_morphology_can_nullify_visual_signal_transfer(self):
        x=receiver_cue_value(
            encounter=F(1),cue_use=F(1),
            baseline_correct_route=F(1,2),
            cued_correct_route=F(1),
            pollen_delivery_if_correct_route=F(1,4),
            pollen_delivery_if_wrong_route=F(1,4))
        self.assertEqual(x['plant_per_opportunity_transfer_delta'],F(0))

    def test_plant_positive_receiver_negative_requires_fixed_cue_use(self):
        x=receiver_cue_value(
            encounter=F(1),cue_use=F(4,5),
            baseline_correct_route=F(1,2),
            cued_correct_route=F(4,5),
            pollen_delivery_if_correct_route=F(4,5),
            processing_cost=F(2,5))
        self.assertEqual(x['plant_per_opportunity_transfer_delta'],F(24,125))
        self.assertEqual(x['receiver_per_opportunity_net_delta'],-F(2,25))
        self.assertTrue(x['not_a_real_ecological_estimate'])

    def test_remote_display_and_local_guide_exact_decomposition(self):
        z=whole_route_decomposition(
            original_detection=F(2,5),signal_detection=F(3,5),
            cue_use=F(1,2),baseline_correct_route=F(2,5),
            cued_correct_route=F(4,5),
            pollen_delivery_if_correct_route=F(3,4))
        self.assertEqual(z['remote_detection_component'],F(3,50))
        self.assertEqual(z['post_detection_local_route_component'],F(9,100))
        self.assertEqual(z['plant_transfer_total_change'],F(3,20))
        self.assertTrue(z['decomposition_is_order_specific'])

    def test_wind_influence_requires_measured_perception_not_taxon_proxy(self):
        # Example where a noisy cue is counterproductive when relied on
        z=receiver_cue_value(
           encounter=F(1),cue_use=F(1),
           baseline_correct_route=F(3,4),
           cued_correct_route=F(1,2),
           pollen_delivery_if_correct_route=F(1))
        self.assertEqual(z['plant_per_opportunity_transfer_delta'],-F(1,4))

    def test_cross_study_taxonomic_matching_is_not_same_subject_mediation(self):
        evidence={
           'learning_trial_source':'Kandori2021',
           'cue_response_source':'guide2023',
           'pollen_transfer_source':'Page2021',
           'original_animal_id_present':False,
           'original_plant_id_present':False,
           'same_experiment_join_keys_verified':False,
           'repeated_measure_covariance_known':False,
           'independent_colony_or_plant_replication_verified':False
        }
        x=compare_joint_evidence(evidence)
        self.assertEqual(x['status'],'NO_GO_CROSS_STUDY_COGNITION_TO_FITNESS_MEDIATION')
        self.assertFalse(x['causal_mediation_allowed'])
        self.assertTrue(x['source_matching_by_taxon_or_guild_insufficient'])

    def test_same_experiment_join_requires_causal_design_beyond_id_match(self):
        evidence={
           'learning_trial_source':'FAKE_A',
           'cue_response_source':'FAKE_A',
           'pollen_transfer_source':'FAKE_A',
           'original_animal_id_present':True,
           'original_plant_id_present':True,
           'same_experiment_join_keys_verified':True,
           'repeated_measure_covariance_known':True,
           'independent_colony_or_plant_replication_verified':True
        }
        x=compare_joint_evidence(evidence)
        self.assertEqual(x['status'],'STRUCTURAL_ORIGINAL_JOIN_ELIGIBLE_FOR_MODELING_ONLY')
        self.assertFalse(x['causal_mediation_allowed'])

    def test_invalid_or_imputed_parameters_fail_closed(self):
        kw=dict(encounter=F(1),cue_use=F(1,2),
                baseline_correct_route=F(1,2),cued_correct_route=F(3,4),
                pollen_delivery_if_correct_route=F(1))
        for key,val in [('cue_use',1.5),('cue_use',F(11,10)),
                        ('baseline_correct_route',F(-1,4)),
                        ('pollen_delivery_if_correct_route',0.7)]:
            copy=kw.copy()
            copy[key]=val
            with self.assertRaises(ValueError):
                receiver_cue_value(**copy)
        with self.assertRaises(ValueError):
            receiver_cue_value(**kw,processing_cost=-1)


if __name__=='__main__':
    unittest.main()
