import unittest
from reward_source_admission import canon,inspect
class TestSource(unittest.TestCase):
    def test_explicit_name_header(self):
        names=["Acer rubrum","Acer negundo","Acer saccharum","Acer platanoides","Acer campestre"]
        d,s=inspect([["Species","Sugar (mg/flower/day)"]]+[[n,1] for n in names])
        self.assertEqual(len(s),5);self.assertEqual(d["selected_explicit_species_header"]["column"],1)
    def test_unlabelled_binomial_column_not_admitted(self):
        d,s=inspect([["unknown column"]]+[[f"Acer {n}"] for n in ["rubrum","negundo","saccharum","platanoides","campestre"]])
        self.assertIsNone(s)
    def test_nontaxon(self):
        self.assertIsNone(canon("Acer sp"));self.assertIsNone(canon("Acer rubrum L."));self.assertIsNone(canon("Unknown plant"))
if __name__=="__main__":unittest.main()
