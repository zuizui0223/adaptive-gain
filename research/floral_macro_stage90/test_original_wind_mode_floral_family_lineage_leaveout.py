"""Stage90C source-free checks of true lineage leaveout without imputations."""
from __future__ import annotations
import unittest
from original_wind_mode_floral_family_lineage_leaveout import CONDITIONS

class OriginalWindPollenFamilyLeaveout(unittest.TestCase):
    def test_source_predeclared_three_families_not_fitted_from_hue_sign(self):
        self.assertEqual(CONDITIONS["exclude_all_three_graminoid_families"],
                         {"Poaceae","Cyperaceae","Juncaceae"})
        self.assertTrue(CONDITIONS["exclude_all_three_graminoid_families"]<
          CONDITIONS["exclude_graminoid_and_nine_wind_enriched_families"])
    def test_fixed_prespecified_family_leave_one_outs(self):
        for family in ("Poaceae","Cyperaceae","Juncaceae"):
            self.assertEqual(CONDITIONS["exclude_"+family],{family})
        self.assertEqual(CONDITIONS["all_source_wind_mode"],set())
        self.assertEqual(len(CONDITIONS),6)
if __name__=="__main__":unittest.main()
