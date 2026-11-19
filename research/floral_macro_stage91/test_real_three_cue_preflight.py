"""Stage91A: test source triage and non-fabricated denominators."""
import tempfile
import unittest
from pathlib import Path
from real_three_cue_preflight import mark_state, petal_width, source_region_counts, source_rows

def row(text="", **kwargs):
    return {"flower colour":text,"petal colour":"","corolla colour":"",**kwargs}

class TestSourceTriage(unittest.TestCase):
    def test_positive_spotted(self):
        self.assertEqual(mark_state(row("white with red spots")),"positive_lexical")
    def test_positive_striped(self):
        self.assertEqual(mark_state(row("purple flowers, striped")),"positive_lexical")
    def test_plain_recorded(self):
        self.assertEqual(mark_state(row("plain yellow flowers")),"explicit_plain_lexical")
    def test_absent_colour_is_unknown(self):
        self.assertEqual(mark_state(row()),"source_colour_missing")
    def test_unmentioned_pattern_not_negative(self):
        self.assertEqual(mark_state(row("red flowers")),"unmentioned")
    def test_negation_is_not_positive(self):
        self.assertEqual(mark_state(row("without spots")),"explicit_plain_lexical")
    def test_positive_and_negative_conflict(self):
        self.assertEqual(mark_state(row("spotted, but elsewhere plain")),"ambiguous")
    def test_width_is_not_diameter(self):
        self.assertEqual(petal_width("2.5 cm"),2.5)
        self.assertIsNone(petal_width("2 to 3 cm"))
        self.assertIsNone(petal_width("unknown"))
        self.assertIsNone(petal_width("-2 cm"))
    def test_region_source_denominators(self):
        traits={
         "flora alba":("positive_lexical",1.4),
         "flora rubra":("unmentioned",None),
         "sylva alba":("explicit_plain_lexical",2.0)}
        d=source_region_counts(set(traits),traits,{"flora alba":"animal","sylva alba":"wind"},
             {"flora alba":"Testaceae","flora rubra":"Testaceae","sylva alba":"Otheraceae"})
        self.assertEqual(d["n_native"],3)
        self.assertEqual(d["n_mark_positive_source_only"],1)
        self.assertEqual(d["n_mark_positive_animal_source_only"],1)
        self.assertEqual(d["n_mark_positive_wind_source_only"],0)
        self.assertEqual(d["n_mark_positive_unknown_source_only"],0)
        self.assertEqual(sum(d[k] for k in ("n_mark_positive_animal_source_only","n_mark_positive_wind_source_only","n_mark_positive_unknown_source_only")),d["n_mark_positive_source_only"])
        self.assertEqual(d["n_mark_unmentioned_not_negative"],1)
        self.assertEqual(d["n_numeric_PETAL_width_not_flower_diameter"],2)
        self.assertEqual(d["n_verified_open_flower_diameter"],0)
        self.assertEqual(d["n_verified_floral_fragrance"],0)
        self.assertEqual(d["pollen_unknown"],1)
        self.assertEqual(d["trait_wind_regression_admissible"],"NO")
    def test_missing_authenticated_source_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"fake.csv"
            path.write_text("taxon,flower colour,petal colour,corolla colour,petal max. width [cm]\n"
                            "Flora alba,red,,,1.2\n",encoding="utf-8")
            with self.assertRaises(ValueError):
                source_rows(path,{"flora alba","other alba"})

if __name__ == "__main__":
    unittest.main()
