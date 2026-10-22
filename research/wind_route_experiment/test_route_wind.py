import unittest
import pandas as pd
import numpy as np
from route_wind import matched_bee_deltas, route_differences, bootstrap_ci, sign_flip_p, load_original


def synthetic():
    return pd.DataFrame([
      {'Bee ID':1,'Canopy height (mm)':98,'Wind Presence':'No','Flight Direction Label':'Up-tunnel','Median altitude (mm)':80,'Median ground speed (m/s)':.3,'Lateral excursion (mm)':10},
      {'Bee ID':1,'Canopy height (mm)':98,'Wind Presence':'Yes','Flight Direction Label':'Up-tunnel','Median altitude (mm)':130,'Median ground speed (m/s)':.4,'Lateral excursion (mm)':15},
      {'Bee ID':1,'Canopy height (mm)':98,'Wind Presence':'No','Flight Direction Label':'Down-tunnel','Median altitude (mm)':90,'Median ground speed (m/s)':.2,'Lateral excursion (mm)':12},
      {'Bee ID':1,'Canopy height (mm)':98,'Wind Presence':'Yes','Flight Direction Label':'Down-tunnel','Median altitude (mm)':140,'Median ground speed (m/s)':.6,'Lateral excursion (mm)':17},
      {'Bee ID':2,'Canopy height (mm)':11,'Wind Presence':'No','Flight Direction Label':'Up-tunnel','Median altitude (mm)':80,'Median ground speed (m/s)':.5,'Lateral excursion (mm)':13},
      {'Bee ID':2,'Canopy height (mm)':11,'Wind Presence':'Yes','Flight Direction Label':'Up-tunnel','Median altitude (mm)':90,'Median ground speed (m/s)':.5,'Lateral excursion (mm)':13},
    ])

class WindRouteTests(unittest.TestCase):
    def test_pair_by_individual_and_direction_not_by_flights(self):
        got=matched_bee_deltas(synthetic(),'Median ground speed (m/s)',min_canopy=None)
        self.assertEqual(len(got),2)
        self.assertAlmostEqual(float(got.loc[got.bee_id==1,'delta'].iloc[0]),.25)
        self.assertAlmostEqual(float(got.loc[got.bee_id==2,'delta'].iloc[0]),0.)

    def test_route_excludes_structural_11mm(self):
        got=route_differences(synthetic(),min_canopy=69)
        self.assertEqual(len(got),1)
        self.assertEqual(got.bee_id.iloc[0],1)
        self.assertAlmostEqual(got.delta.iloc[0],1.)

    def test_missing_matched_wind_is_not_imputed(self):
        a=synthetic().query('`Wind Presence` == "Yes"')
        self.assertTrue(matched_bee_deltas(a,'Median ground speed (m/s)').empty)

    def test_bootstrap_zero_values(self):
        self.assertEqual(bootstrap_ci(np.zeros(10),reps=200),[0.,0.])

    def test_signflip_zero_values_no_false_significance(self):
        self.assertEqual(sign_flip_p(np.zeros(10),reps=999),1.)

    def test_original_hash_lock(self):
        d,receipt=load_original('Bee_route_choice_in_wind.csv',enforce_size=False)
        self.assertTrue(receipt['sha256_verified'])
        self.assertEqual(len(d),548)
        self.assertEqual(d['Bee ID'].nunique(),58)

if __name__=='__main__': unittest.main()