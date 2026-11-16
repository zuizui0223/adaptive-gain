"""Offline mock tests for deduplicated modeled taxon × original HEX cells."""
from unittest.mock import patch
import unittest
from derive_bombus_hex_prediction import (
   modelled_bombus_coverage,SOURCE_INNER_SHA256
)

EXPECTED={"source_matrix_member_SHA256":SOURCE_INNER_SHA256,
          "n_data_rows":396703,
          "first_30_columns":["siteid","species"]}

class BombusModeledCellAudit(unittest.TestCase):
    def test_deduplicate_same_source_model_taxon_in_cell(self):
        source=(b"siteid,species\nHEX12,Bombus terrestris\n"
                b"HEX12,Bombus terrestris\nHEX12,Bombus cryptarum\n"
                b"HEX13,Apis mellifera\nHEX13,Bombus terrestris\n"
                b"HEX14,Apis mellifera\n")
        with patch("derive_bombus_hex_prediction.source_matrix_schema",return_value=EXPECTED):
            report,grid,taxa=modelled_bombus_coverage(source)
        self.assertEqual(report["duplicate_source_species_cell_pairs"],1)
        self.assertEqual(report["n_distinct_modelled_Bombus_taxon_strings"],2)
        self.assertEqual(report["n_grid_cells_with_Bombus_modelled_presence"],2)
        self.assertEqual(report["n_grid_cells_zero_Bombus_in_covered_source_grid"],1)
        self.assertIn(("HEX12",2,2),grid)
        self.assertIn(("HEX13",1,2),grid)
        self.assertTrue(report["zero_is_no_modelled_genus_in_supplied_grid_not_true_biological_absence"])

    def test_bad_original_model_cell_not_accepted(self):
        with patch("derive_bombus_hex_prediction.source_matrix_schema",return_value=EXPECTED):
            with self.assertRaisesRegex(ValueError,"NO_GO_BAD_MODELED_BEE"):
                modelled_bombus_coverage(b"siteid,species\nA,Bombus terrestris\n")

    def test_unauthenticated_source_does_not_run(self):
        wrong={**EXPECTED,"source_matrix_member_SHA256":"bad"}
        with patch("derive_bombus_hex_prediction.source_matrix_schema",return_value=wrong):
            with self.assertRaisesRegex(ValueError,"NO_GO_BEE_SPECIES_GRID_SOURCE_BYTES_CHANGED"):
                modelled_bombus_coverage(b"siteid,species\nHEX12,Bombus test\n")

if __name__=="__main__":
    unittest.main()
