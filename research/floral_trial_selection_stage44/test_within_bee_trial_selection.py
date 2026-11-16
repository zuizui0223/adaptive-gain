"""Only constructed numeric rows; no fake rows attributed to original bees."""
import itertools
import math
import statistics
import unittest

from within_bee_trial_selection import (
    CUTOFFS,SPEED_METHODS,finite_cells,selection_envelope
)
KEY=(100,'three_tag_mean')


def row(bee,stem,position,wind,value):
    return dict(B=bee,S=stem,P=position,W=wind,values={KEY:(.5,value,value-.5)})


def synthetic():
    return [
      row('01','0','0','W0',.1),
      row('01','0','0','W0',.4),
      row('01','0','0','W1',.5),
      row('01','0','0','W1',.7),
      row('01','0','1','W0',.2),
      row('01','0','1','W1',.1),
      row('01','0','1','W1',.2),
      row('02','0','0','W0',.25),
      row('02','0','0','W1',.3),
      row('03','1','1','W0',100.), # intentionally unpaired
    ]


class SourceFreeSelectionContracts(unittest.TestCase):
    def test_fixed_all_cells_analytical_exact_bounds(self):
        z=selection_envelope(synthetic())
        self.assertEqual(z['status'],
                         'EXACT_ARCHIVED_TRIAL_SELECTION_ENVELOPES_FIXED_OR_ONE_CELL_PER_B')
        self.assertEqual(z['n_original_B_identifiers'],2)
        self.assertEqual(z['n_original_matched_B_S_P_cells'],3)
        self.assertEqual(z['n_cells_with_multiple_eligible_original_trajectories_in_either_wind_arm'],2)
        self.assertEqual(z['n_source_B_with_at_least_one_optional_cell_or_trial'],1)
        self.assertEqual(z['n_eligible_source_file_appearances_in_matched_cells'],9)
        self.assertAlmostEqual(z['original_within_B_S_P_all_trial_mean_m_s'],.1)
        self.assertAlmostEqual(z['fixed_matched_cells_one_original_trial_per_arm_exact_lower_m_s'],.025)
        self.assertAlmostEqual(z['fixed_matched_cells_one_original_trial_per_arm_exact_upper_m_s'],.175)
        self.assertAlmostEqual(z['any_one_matched_cell_per_B_one_original_trial_per_arm_exact_lower_m_s'],-.025)
        self.assertAlmostEqual(z['any_one_matched_cell_per_B_one_original_trial_per_arm_exact_upper_m_s'],.325)

    def test_brute_enumeration_independent_oracle(self):
        # B1: P0 W0(2) × W1(2), P1 W0(1) × W1(2).
        contrasts=[]
        onecell=[]
        for c0,w0,c1 in itertools.product((.1,.4),(.5,.7),(.1,.2)):
            cell0=w0-c0
            cell1=c1-.2
            fixed_B1=(cell0+cell1)/2
            fixed_B2=.3-.25
            contrasts.append((fixed_B1+fixed_B2)/2)
            onecell.extend([(cell0+fixed_B2)/2,(cell1+fixed_B2)/2])
        z=selection_envelope(synthetic())
        self.assertAlmostEqual(min(contrasts),
            z['fixed_matched_cells_one_original_trial_per_arm_exact_lower_m_s'])
        self.assertAlmostEqual(max(contrasts),
            z['fixed_matched_cells_one_original_trial_per_arm_exact_upper_m_s'])
        self.assertAlmostEqual(min(onecell),
            z['any_one_matched_cell_per_B_one_original_trial_per_arm_exact_lower_m_s'])
        self.assertAlmostEqual(max(onecell),
            z['any_one_matched_cell_per_B_one_original_trial_per_arm_exact_upper_m_s'])

    def test_unmatched_original_files_do_not_create_extra_B(self):
        x=finite_cells(synthetic(),KEY,1,{})
        self.assertEqual(len(x),3)
        self.assertNotIn(('03','1','1'),x)

    def test_exact_W0_W1_same_cell_matching_required(self):
        data=[row('01','0','0','W0',.1),
              row('01','0','1','W1',.9)]
        self.assertEqual(selection_envelope(data)['status'],
                         'NO_GO_NO_MATCHED_ORIGINAL_B_IDENTIFIERS')

    def test_single_source_pair_has_zero_selection_width(self):
        z=selection_envelope([row('01','0','0','W0',.1),
                              row('01','0','0','W1',.3)])
        for k in ('fixed_matched_cells_one_original_trial_per_arm_exact_lower_m_s',
                  'fixed_matched_cells_one_original_trial_per_arm_exact_upper_m_s',
                  'any_one_matched_cell_per_B_one_original_trial_per_arm_exact_lower_m_s',
                  'any_one_matched_cell_per_B_one_original_trial_per_arm_exact_upper_m_s'):
            self.assertAlmostEqual(z[k],.2)

    def test_speed_method_and_endpoints_same_contract(self):
        z=selection_envelope(synthetic(),KEY,2)
        self.assertAlmostEqual(z['original_within_B_S_P_all_trial_mean_m_s'],.1)

    def test_wrong_key_must_fail_closed(self):
        with self.assertRaisesRegex(ValueError,'NO_GO_UNREGISTERED'):
            selection_envelope(synthetic(),(170,'three_tag_mean'))
        with self.assertRaisesRegex(ValueError,'NO_GO_UNREGISTERED'):
            selection_envelope(synthetic(),KEY,3)

    def test_unknown_subset_dimension_blocked(self):
        with self.assertRaisesRegex(ValueError,'NO_GO_UNKNOWN_SUBSET'):
            selection_envelope(synthetic(),KEY,1,{'wind':'1'})

    def test_invalid_speed_and_wind_fail_closed(self):
        bad=[row('01','0','0','W0',.1),
             row('01','0','0','W1',float('nan'))]
        with self.assertRaisesRegex(ValueError,'NO_GO_NAN'):
            selection_envelope(bad)
        bad=[row('01','0','0','W2',.3)]
        with self.assertRaisesRegex(ValueError,'NO_GO_NONBINARY_SOURCE_WIND'):
            selection_envelope(bad)

    def test_exact_method_grid(self):
        self.assertEqual(CUTOFFS,(50,100,150))
        self.assertEqual(SPEED_METHODS,('three_tag_mean','point2_only'))


if __name__=='__main__':
    unittest.main()
