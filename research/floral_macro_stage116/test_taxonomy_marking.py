import unittest
import pandas as pd
from taxonomy_marking import taxonomic_components
from regional_marking_bombus import fit,frame

class Tests(unittest.TestCase):
    def test_disjoint_reference(self):
        mark={"a":1,"b":0,"c":0,"d":1,"e":0}
        tax={s:"genus" for s in mark}
        r=taxonomic_components({"a","b"},set(mark),mark,tax)
        self.assertAlmostEqual(r["residual"],.1)
        self.assertAlmostEqual(r["disjoint_residual"],1/6)
        self.assertEqual(r["disjoint_support_fraction"],1)
    def test_no_other_species_support(self):
        r=taxonomic_components({"a"},{"a"},{"a":1},{"a":"g"})
        self.assertEqual(r["disjoint_support_fraction"],0)
        self.assertIsNone(r["disjoint_residual"])
    def test_missing_taxonomy_not_zero_mark(self):
        r=taxonomic_components({"a","b"},{"a","b"},{"a":1,"b":0},{"a":"g"})
        self.assertEqual(r["classified_fraction"],.5)
        self.assertEqual(r["observed"],1)

if __name__=="__main__":unittest.main()
