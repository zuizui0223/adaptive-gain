import unittest
from audit_bee_model_phylogeny_selection import tree_tips

class TreeSourceContracts(unittest.TestCase):
    def test_simple_original_style_tree(self):
        x=tree_tips("(Bombus_terrestris:0.1,Apis_mellifera:0.2);")
        self.assertEqual(x,["Bombus_terrestris","Apis_mellifera"])
    def test_unterminated_newick_rejected(self):
        with self.assertRaisesRegex(ValueError,"NO_GO_INVALID_ORIGINAL_NEWICK"):
            tree_tips("(Bombus_terrestris:0.1)")
if __name__=="__main__":
    unittest.main()
