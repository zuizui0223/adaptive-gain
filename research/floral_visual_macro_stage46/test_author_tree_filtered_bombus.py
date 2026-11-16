"""Source-free tests of author phylogenetic/species/cell filtering and missingness."""
import unittest
from author_tree_filtered_bombus import (
    source_parameter_and_taxa,trim_original_bee_matrix,materialize_join
)


class OriginalAuthorSelectionTests(unittest.TestCase):
    def test_exact_author_filter_semantics_synthetic(self):
        script=b"""pa_cutoff <- 2
shared_species <- intersect(pa_all$species, bee_phylo_consensus$tip.label)
filter(n_distinct(species) >= pa_cutoff)
"""
        tips=b"(Bombus_terrestris_n4m3_Apidae:0.2,(Apis_mellifera_n5m2_Apidae:0.4,Andrena_bicolor_n1m0_Andrenidae:0.3):0.5);"
        # This helper explicitly requires >3000 authentic taxa; test failure
        with self.assertRaisesRegex(ValueError,"NO_GO_SOURCE_TREE_TOO_FEW_TIPS"):
            source_parameter_and_taxa(script,tips)

    def test_intersection_and_cell_cutoff_must_be_applied_before_bombus(self):
        rows=b"""siteid,species
HEX10,Bombus terrestris
HEX10,Apis mellifera
HEX10,Fakeus fictus
HEX11,Bombus terrestris
HEX12,Andrena bicolor
HEX12,Apis mellifera
"""
        p,eligible,shared=trim_original_bee_matrix(
            rows,{"Bombus terrestris","Apis mellifera","Andrena bicolor"},2)
        self.assertEqual(p["raw_model_taxon_strings"],4)
        self.assertEqual(p["n_shared_phylogeny_original_model_taxa"],3)
        self.assertEqual(p["source_cells_after_original_pa_cutoff"],2)
        self.assertEqual(p["source_Bombus_species_after_tree_cell_cutoff"],1)
        self.assertEqual(p["n_hex_with_Bombus_after_paper_filter"],1)
        self.assertNotIn("HEX11",eligible)
        self.assertEqual(len(eligible["HEX10"]),2)

    def test_geographic_unknown_not_zero(self):
        rows=materialize_join({"HEX1":{"Bombus terrestris","Apis mellifera"}},
                              {"HEX1":(12.,42.),"HEX2":(13.,43.)})
        self.assertEqual(len(rows),2)
        self.assertEqual(rows[0]["n_source_tree_and_pa_cutoff_Bombus_taxa"],1)
        self.assertIsNone(rows[1]["n_source_tree_and_pa_cutoff_Bombus_taxa"])
        self.assertTrue("NO_ABSENCE" in rows[1]["eligibility"])

    def test_unregistered_grid_cell_error(self):
        with self.assertRaisesRegex(ValueError,"NO_GO_PAPER_FILTERED_HEX"):
            materialize_join({"HEX99":{"Apis mellifera"}},
                             {"HEX1":(0.,0.)})

    def test_wrong_original_matrix_schema_error(self):
        with self.assertRaisesRegex(ValueError,"NO_GO_SOURCE_BEE_MATRIX_GRAIN"):
            trim_original_bee_matrix(b"species,siteid\nBombus terrestris,HEX1\n",
                                     {"Bombus terrestris"},1)


if __name__=="__main__":
    unittest.main()
