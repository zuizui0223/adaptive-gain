"""Source-free exact VOC and original botanical prose equivalence guards."""
import tempfile,unittest,zipfile
from pathlib import Path
from original_WFO_scent_VOC305_exact_source_overlap import get,overlap,describe

def fixture():
    flora=[{"accepted_species":f"genus taxon{i:05d}",
        "source_flora_lexical_fragrance_state":"unmentioned_or_uncertain",
        "original_flora_provider":"Flora_of_China",
        "botanical_description_length_characters_median":"500"} for i in range(27899)]
    flora[0]["source_flora_lexical_fragrance_state"]="positive_candidate"
    flora[1]["source_flora_lexical_fragrance_state"]="explicit_negative_candidate"
    v=[{"GBIF_strict_taxonomy_status":"NOT_EXACT_95_CONFIDENCE_PLANT_SPECIES",
        "source_species_canonical_binomial_if_valid":f"genus other{i:05d}",
        "source_VOC_positive_presence_columns_in_original_full_bouquet":"13",
        "source_article_abbrev":"SOURCE1"} for i in range(305)]
    v[0].update({"GBIF_strict_taxonomy_status":"EXACT_CONFIDENT_SPECIES_MAPPED",
          "source_species_canonical_binomial_if_valid":"Genus taxon00000",
          "source_VOC_positive_presence_columns_in_original_full_bouquet":"27"})
    v[1].update({"GBIF_strict_taxonomy_status":"EXACT_CONFIDENT_SPECIES_MAPPED",
          "source_species_canonical_binomial_if_valid":"Genus taxon00001",
          "source_VOC_positive_presence_columns_in_original_full_bouquet":"4"})
    return flora,v

class VOCOriginalSource(unittest.TestCase):
    def test_exact_native_species_and_positive_negative_separate(self):
        f,v=fixture();rows=overlap(f,v);r=describe(rows)
        self.assertEqual(len(rows),2)
        self.assertEqual(r["source_WFO_lexical_state_counts"]["positive_candidate"],1)
        self.assertEqual(r["source_WFO_lexical_state_counts"]["explicit_negative_candidate"],1)
        self.assertFalse(r["fragrance_absence_proxy_validation_identifiable"])
        self.assertTrue(r["cannot_compare_orig_emission_units_from_this_presence_workbook"])
    def test_not_exact_taxonomy_cannot_match_by_lexical_heuristic(self):
        f,v=fixture();v[1]["GBIF_strict_taxonomy_status"]="NOT_EXACT_95_CONFIDENCE_PLANT_SPECIES"
        self.assertEqual(len(overlap(f,v)),1)
    def test_missing_original_WFO_fragrance_not_negative(self):
        f,v=fixture();f[0]["source_flora_lexical_fragrance_state"]="unmentioned_or_uncertain"
        r=describe(overlap(f,v))
        self.assertEqual(r["source_WFO_lexical_state_counts"].get("explicit_negative_candidate"),1)
        self.assertEqual(r["source_WFO_lexical_state_counts"].get("unmentioned_or_uncertain"),1)
    def test_original_wrong_source_digest_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"fake.zip"
            with zipfile.ZipFile(p,"w") as z:z.writestr("fake.csv","plant\\n")
            with self.assertRaises(ValueError):get(p,"f"*64,"fake.csv")
    def test_compound_presence_not_direct_emission(self):
        f,v=fixture();rows=overlap(f,v)
        self.assertIn("original_VOC_positive_presence_compound_columns_not_emission_flux",rows[0])
        self.assertTrue(rows[0]["original_VOC_compound_detected_not_human_fragrance_perception"])

if __name__=="__main__":unittest.main()
