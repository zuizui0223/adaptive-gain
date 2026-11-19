"""Source-free test of strict same-name independent data-label concordance."""
import unittest
from crosscheck_GIFT_AusTraits_original_pollination_modes import source_cross,safe_kappa

class CrossDBLabelControls(unittest.TestCase):
    def test_category_swap_must_lower_concordance(self):
        g={"planta alba":"animal","planta rosea":"animal",
           "gloria viridis":"wind","gloria rubra":"wind"}
        a={"planta alba":"animal","planta rosea":"wind",
           "gloria viridis":"wind","gloria rubra":"animal"}
        z=source_cross(g,a,{},bootstrap=100)
        self.assertEqual(z["source_exact_name_overlap"],4)
        self.assertEqual(z["source_disagreement_species_count"],2)
        self.assertEqual(z["source_agreement_fraction"],.5)
        self.assertTrue(z["source_GIFT_vs_AusTraits_may_share_original_literature"])
        self.assertTrue(z["source_phylogenetic_ancestry_not_adjusted"])
    def test_no_species_only_in_one_source_misclassified(self):
        g={"planta alba":"animal"}
        a={"gloria rubra":"wind"}
        z=source_cross(g,a,{},bootstrap=10)
        self.assertEqual(z["source_exact_name_overlap"],0)
        self.assertIsNone(z["source_agreement_fraction"])
        self.assertEqual(z["source_disagreement_species_count"],0)
        self.assertIsNone(safe_kappa(g,a,[]))
if __name__=="__main__":unittest.main()
