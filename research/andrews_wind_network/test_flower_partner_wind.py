"""Tests written before implementation; synthetic watch/plant opportunities only."""
import unittest
import numpy as np
from flower_partner_wind import admissible_masks, day_stats, holm, evaluate_panel


class BloomConditionedWindTests(unittest.TestCase):
    def test_flowering_in_both_winds_is_required_for_every_plant(self):
        bloom=np.array([[1,1],[1,0],[0,1],[1,1]],bool)
        masks=admissible_masks(bloom,2)
        self.assertTrue(len(masks)>0)
        for m in masks:
            self.assertTrue(np.all(bloom[m].sum(0)>=1))
            self.assertTrue(np.all(bloom[~m].sum(0)>=1))
            self.assertEqual(int(m.sum()),2)

    def test_missing_flower_opportunity_is_not_an_observed_zero(self):
        bloom=np.array([[1,0],[1,1],[0,1],[1,1]],bool)
        visits=np.array([[1,0],[0,1],[0,0],[0,0]],bool)
        wind=np.array([0,0,1,1],bool)
        stats=day_stats(bloom,visits,visits,wind)
        # A: ST 1/2; BR 0/1  => -0.5
        # B: ST 1/1; BR 0/2  => -1.0
        self.assertAlmostEqual(stats[2],-.75)
        self.assertAlmostEqual(stats[0],.0625)

    def test_uniform_response_across_plants_has_zero_heterogeneity(self):
        b=np.ones((4,2),bool)
        z=np.array([[1,1],[0,0],[1,1],[0,0]],bool)
        r=day_stats(b,z,z,np.array([1,1,0,0],bool))
        self.assertEqual(r[0],0.)
        self.assertEqual(r[1],0.)

    def test_wind_label_inversion_has_equal_H_opposite_signed_effect(self):
        b=np.ones((4,2),bool)
        z=np.array([[1,0],[1,1],[0,0],[0,1]],bool)
        m=np.array([1,0,1,0],bool)
        x=day_stats(b,z,z,m)
        y=day_stats(b,z,z,~m)
        np.testing.assert_allclose(x[:2],y[:2])
        np.testing.assert_allclose(x[2:],-y[2:])

    def test_labeled_plant_has_no_admissible_assignment_when_one_occurrence(self):
        b=np.array([[1,1],[1,0],[1,0]],bool)
        self.assertEqual(len(admissible_masks(b,1)),0)

    def test_cluster_weight_equalizes_many_day_meadow(self):
        # The second meadow has a single day but must have the same weight
        # as the first meadow with 3 days, not one quarter of its weight.
        days=[{"meadow":"X","wind":np.array([0,1,0,1],bool),
              "bloom":np.ones((4,2),bool),"all":np.array([[1,0],[1,0],[0,1],[0,1]],bool),
              "bee":np.array([[1,0],[1,0],[0,1],[0,1]],bool)}]*3
        days.append({"meadow":"Y","wind":np.array([0,1,0,1],bool),
              "bloom":np.ones((4,2),bool),"all":np.array([[0,1],[1,0],[0,1],[1,0]],bool),
              "bee":np.array([[0,1],[1,0],[0,1],[1,0]],bool)})
        r=evaluate_panel(days,reps=199,seed=7,boot_reps=199)
        self.assertEqual(r['n_meadows'],2)
        self.assertEqual(r['n_days'],4)
        self.assertEqual(r['n_plant_day_pairs'],8)
        self.assertEqual(len(r['metrics']),4)

    def test_holm_two_avoids_cherry_picking(self):
        np.testing.assert_allclose(holm([.04,.03]),[.06,.06])

if __name__=='__main__':unittest.main()