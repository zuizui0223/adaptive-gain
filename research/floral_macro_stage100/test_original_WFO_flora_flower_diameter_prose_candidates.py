"""Stage100 floral diameter lexical positives with conservative exclusions."""
import unittest,tempfile,zipfile
from pathlib import Path
from original_WFO_flora_flower_diameter_prose_candidates import (
    width_candidates,per_species_source_cue,scan_source
)

class OriginalWFOFlowerSizeTests(unittest.TestCase):
    def test_direct_whole_flower_mm(self):
        found,q=width_candidates("Flowers white, 6 mm in diameter, fragrant.")
        self.assertIn(("flower_diameter_TEXT_CANDIDATE",6),found)
    def test_direct_cm_conversion(self):
        found,q=width_candidates("Flowers solitary, 1.5 cm across.")
        self.assertIn(("flower_diameter_TEXT_CANDIDATE",15),found)
    def test_flower_diameter_before_value(self):
        found,q=width_candidates("Flower diameter 2 cm. Leaves narrow.")
        self.assertIn(("flower_diameter_TEXT_CANDIDATE",20),found)
    def test_corolla_only_not_whole_flower(self):
        found,q=width_candidates("Corolla 9 mm wide.")
        self.assertTrue(any(k=="corolla_width_TEXT_NOT_WHOLE_FLOWER" for k,v in found))
        state,value=per_species_source_cue(found)
        self.assertEqual(state,"candidate_corolla_width_only_NOT_whole_flower")
    def test_leaf_width_not_flower_diameter(self):
        found,q=width_candidates("Leaves 5 mm broad. Flowers white.")
        self.assertEqual(found,[])
    def test_inflorescence_head_diameter_not_flower(self):
        found,q=width_candidates("Flowers grouped in heads 2 cm across.")
        self.assertEqual(found,[])
        self.assertTrue(q.get("discard_intervening_other_organ",0)>=1)
    def test_peduncle_diameter_not_flower(self):
        found,q=width_candidates("Flowers terminal on peduncles 3 mm in diameter.")
        self.assertEqual(found,[])
    def test_numeric_range_not_fake_single_value(self):
        found,q=width_candidates("Flowers 3–5 mm across.")
        self.assertEqual(found,[])
        self.assertGreater(q.get("discard_numeric_range",0),0)
    def test_unmentioned_not_zero_mm(self):
        found,q=width_candidates("Flowers blue. Leaves lanceolate.")
        self.assertEqual(found,[])
        self.assertEqual(per_species_source_cue(found),("no_unambiguous_diameter_phrase",None))
    def test_invalid_extreme_size_rejected(self):
        found,q=width_candidates("Flowers 300 mm across.")
        self.assertEqual(found,[])
    def test_conflicting_direct_values_are_not_promoted(self):
        self.assertEqual(per_species_source_cue([
            ("flower_diameter_TEXT_CANDIDATE",5),
            ("flower_diameter_TEXT_CANDIDATE",25)]),
            ("multiple_conflicting_flower_diameter_prose",None))
    def test_flower_precedence_over_corolla_width(self):
        state,value=per_species_source_cue([
            ("corolla_width_TEXT_NOT_WHOLE_FLOWER",12),
            ("flower_diameter_TEXT_CANDIDATE",20)])
        self.assertEqual((state,value),("candidate_flower_diameter_from_prose",20))
    def test_fake_original_source_checksum_rejected_before_parsing(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"fake.zip"
            with zipfile.ZipFile(p,"w") as z:z.writestr("meta.xml","false")
            with self.assertRaisesRegex(ValueError,"AUTHOR_ORIGINAL_WFO_SOURCE_SHA_DRIFT"):
                scan_source(p,"Flora_of_China",{"campanula punctata"},{})

if __name__=="__main__":unittest.main()
