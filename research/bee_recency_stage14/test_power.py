import unittest
from power import comparison

class PowerTests(unittest.TestCase):
    def test_refresh_halves_cell_replicates_not_colony_count(self):
        p=comparison(24,true_delta=.02,sigma_colony=.025)
        self.assertEqual(p['bees_per_colony'],12)
        self.assertEqual(p['refreshed_arm_trials_per_order_wind_cell_per_bee'],8)
        self.assertEqual(p['no_refresh_arm_trials_per_order_wind_cell_per_bee'],8)
        self.assertEqual(p['total_qa_trials'],24*12*64)
        self.assertLess(p['new_power_if_assumptions_true'],
                        p['original_stage9_power_if_assumptions_true'])
        self.assertTrue(p['all_sds_are_assumptions_not_data'])
if __name__=='__main__':unittest.main()