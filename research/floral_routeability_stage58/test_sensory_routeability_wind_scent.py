"""Stage58 tests use only constructed four-world states and verified source labels."""
from fractions import Fraction as F
import unittest

from sensory_routeability_wind_scent import (
   ROUTER,VISUAL,SCENT,SOURCE_SYSTEMS,
   routing_task,exact_route_context,exact_opportunity_chain,
   break_even_landing,hypothetical_wind_stage_contrast,
   study_integration_receipt,
)
from adaptive_gain.core import (
   adaptive_minimum_resolution,fixed_minimum_resolution,bundle_resolves)

class ExactCueRouteabilityWindScentContracts(unittest.TestCase):
    def test_weighted_existing_k2_theorem_matches_independent_solver(self):
        for r in (1,2,3,5):
            for v in (1,2,4,7):
                for s in (1,2,3,6):
                    with self.subTest(r=r,v=v,s=s):
                        task=routing_task(coarse_cost=r,visible_cost=v,chemical_cost=s)
                        aa=adaptive_minimum_resolution(task)
                        ff=fixed_minimum_resolution(task)
                        self.assertEqual(aa.minimum_worst_path_cost,r+max(v,s))
                        self.assertEqual(ff.minimum_cost,r+v+s)
                        self.assertEqual(ff.optimal_bundles,((ROUTER,VISUAL,SCENT),))
                        self.assertFalse(bundle_resolves(task,(VISUAL,SCENT)))
                        self.assertTrue(bundle_resolves(task,(ROUTER,VISUAL,SCENT)))

    def test_nondiagnostic_router_has_no_direct_target_information_under_uniform_prior(self):
        task=routing_task(coarse_cost=1,visible_cost=2,chemical_cost=2)
        # Uniform over four canonical worlds; each router outcome has
        # one target-0 and one target-1 world, exactly preserving 50:50.
        root=task.queries[0]
        for o in set(root.outcomes):
            targets=[w.target for w,s in zip(task.worlds,root.outcomes) if s==o]
            self.assertEqual(sorted(targets),[0,1])
        self.assertEqual([w.target for w in task.worlds],[0,1,0,1])

    def test_cue_loss_changes_identifiability_not_merely_cost(self):
        for name in ("coarse","visible","chemical"):
            task=routing_task(coarse_cost=1,visible_cost=1,chemical_cost=1,removed=name)
            self.assertIsNone(adaptive_minimum_resolution(task).minimum_worst_path_cost)
            self.assertIsNone(fixed_minimum_resolution(task).minimum_cost)
            self.assertFalse(exact_route_context(1,1,1,budget=12,removed=name)[
                "adaptive_resolves_under_budget"])

    def test_phase_gate_supports_nonmonotonic_accessibility_assumptions(self):
        d=study_integration_receipt()
        r=d["exact_source_free_routeability_scenarios"]
        self.assertEqual((r["reference_calm_assumed"]["exact_adaptive_minimum_worst_case_cost_or_unresolvable"],
                          r["reference_calm_assumed"]["exact_fixed_minimum_bundle_cost_or_unresolvable"]),
                         (3,5))
        self.assertEqual((r["facilitated_chemical_cue_but_harder_visual_assumed"]["exact_adaptive_minimum_worst_case_cost_or_unresolvable"],
                          r["facilitated_chemical_cue_but_harder_visual_assumed"]["exact_fixed_minimum_bundle_cost_or_unresolvable"]),
                         (4,5))
        self.assertEqual((r["visual_access_bottleneck_assumed"]["exact_adaptive_minimum_worst_case_cost_or_unresolvable"],
                          r["visual_access_bottleneck_assumed"]["exact_fixed_minimum_bundle_cost_or_unresolvable"]),
                         (6,7))
        self.assertIsNone(r["early_router_disrupted_assumed"]["exact_fixed_minimum_bundle_cost_or_unresolvable"])
        self.assertFalse(r["visual_access_bottleneck_assumed"]["adaptive_only_within_budget"])

    def test_weak_wind_odor_advantage_does_not_imply_positive_pollen_transfer(self):
        x=hypothetical_wind_stage_contrast()
        self.assertEqual(x["calm_per_opportunity_transfer_fraction"],"6/25")
        self.assertEqual(x["wind_per_opportunity_transfer_fraction"],"9/40")
        self.assertEqual(x["wind_minus_calm_transfer_fraction"],"-3/200")
        self.assertEqual(x["break_even_windy_landing_given_discovery_if_same_pollen_fraction"],"8/15")
        self.assertEqual(break_even_landing(calm_detection=F(2,5),
                            calm_landing=F(4,5),wind_detection=F(3,5)),F(8,15))
        self.assertGreater(exact_opportunity_chain(detection=F(3,5),
             landing_given_detection=F(3,4),pollen_given_landing=F(3,4)),
             exact_opportunity_chain(detection=F(2,5),
             landing_given_detection=F(4,5),pollen_given_landing=F(3,4)))

    def test_invalid_probability_cost_unknown_cue_blocked(self):
        with self.assertRaisesRegex(ValueError,"POSITIVE_INTEGER"):
            routing_task(coarse_cost=0,visible_cost=2,chemical_cost=2)
        with self.assertRaisesRegex(ValueError,"POSITIVE_INTEGER"):
            routing_task(coarse_cost=1.0,visible_cost=2,chemical_cost=2)
        with self.assertRaisesRegex(ValueError,"UNKNOWN_CUE"):
            routing_task(coarse_cost=1,visible_cost=2,chemical_cost=2,removed="wind")
        with self.assertRaisesRegex(ValueError,"UNVERIFIED_FLOAT"):
            exact_opportunity_chain(detection=0.5,landing_given_detection=F(1,2),
                                    pollen_given_landing=F(1,2))
        with self.assertRaisesRegex(ValueError,"OUTSIDE_UNIT"):
            exact_opportunity_chain(detection=F(3,2),landing_given_detection=F(1,2),
                                    pollen_given_landing=F(1,2))

    def test_sources_are_independent_endpoints_not_a_faked_factorial(self):
        self.assertEqual(len(SOURCE_SYSTEMS),4)
        self.assertEqual(SOURCE_SYSTEMS["Crall2020"]["doi"],"10.1098/rsbl.2020.0103")
        self.assertIn("odor-off wind factorial",SOURCE_SYSTEMS["Crall2020"]["missing"])
        self.assertIn("failed approach denominator",SOURCE_SYSTEMS["Chang2016"]["missing"])
        x=study_integration_receipt()
        self.assertTrue(x["source_studies_not_same_insects_or_source_flower_system"])
        self.assertTrue(x["no_causal_visual_x_scent_x_wind_factorial_available"])
        self.assertTrue(x["existing_mathematical_result_only"])
        self.assertTrue(x["no_automatic_pollinator_derived_evolutionary_selection_or_feedback_oscillation"])
if __name__=="__main__":
    unittest.main()
