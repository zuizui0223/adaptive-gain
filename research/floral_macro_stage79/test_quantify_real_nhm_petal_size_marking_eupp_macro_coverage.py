"""Source-only tests: floral petal size far-stage versus markings near-stage."""
import importlib.util,unittest
from pathlib import Path
p=Path(__file__).with_name("quantify_real_nhm_petal_size_marking_eupp_macro_coverage.py")
spec=importlib.util.spec_from_file_location("s79b",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def blank(width=None,mark=0):
    return {"petal max. width [cm]":width,
       "petal min. width [cm]":width,
       "corolla tube max. length [cm]":None,
       "source_orientation_text":"","source_symmetry_text":"",
       "source_shape_text":"",
       "source_reported_positive_marking_text":mark}

class OriginalNearFarAuditTests(unittest.TestCase):
    def test_empty_width_is_missing_not_same_as_zero(self):
        self.assertIsNone(m.parsed_size(""))
        self.assertIsNone(m.parsed_size("NA"))
        self.assertIsNone(m.parsed_size("two"))
        self.assertIsNone(m.parsed_size("0"))
        self.assertEqual(m.parsed_size("2.4"),2.4)
        self.assertIsNone(m.parsed_size("10000"))
    def test_original_marking_word_positive_only(self):
        self.assertIsNotNone(m.POTENTIAL_MARK.search("petal with spotted centre"))
        self.assertIsNotNone(m.POTENTIAL_MARK.search("nectar guide on petals"))
        self.assertIsNone(m.POTENTIAL_MARK.search("red flower"))
        self.assertIsNone(m.POTENTIAL_MARK.search(""))
    def test_real_NHM_size_and_lookedup_plant_field_requires_same_network(self):
        taxa={"gentiana lutea","linum perenne","teucrium chamaedrys"}
        nhm={"gentiana lutea":blank(3.1,0),
             "linum perenne":blank(1.2,1),
             "teucrium chamaedrys":blank(2.4,0)}
        row=lambda n,sp:{"Study_id":"S1","Network_id":n,
             "Year_from_original_date":"2021",
             "Original_plant_accepted_name_literal":sp}
        roster=[row("A","gentiana lutea"),row("A","linum perenne"),
                row("B","teucrium chamaedrys")]
        nets={("S1","A","2021"),("S1","B","2021")}
        r,site,plants=m.coverage(nhm,roster,taxa,nets)
        self.assertEqual(r["original_source_species_with_positive_pattern_text"],1)
        self.assertEqual(
            r["network_design_coverage_selected_BEFORE_any_visiting_bee_outcome"][
                "source_network_has_2_size_species_and_close_pattern"],1)
        self.assertEqual(site[1]["source_network_has_at_least_2_distinct_plant_species_with_petal_max_width"],0)
        self.assertEqual(len(plants),3)
        self.assertTrue(r["source_unknown_marking_is_NEVER_zero"])
    def test_network_with_all_unknown_markings_is_not_negative_control(self):
        taxa={"gentiana lutea"}
        nhm={"gentiana lutea":blank(4.0,0)}
        roster=[{"Study_id":"S1","Network_id":"A",
            "Year_from_original_date":"2021",
            "Original_plant_accepted_name_literal":"gentiana lutea"}]
        r,site,_=m.coverage(nhm,roster,taxa,{("S1","A","2021")})
        self.assertEqual(site[0]["source_positive_pattern_documented_species"],0)
        self.assertEqual(site[0]["source_unreported_visual_pattern_remains_UNKNOWN"],1)
    def test_source_pin_is_NHM_botanical_prose_not_photo(self):
        self.assertEqual(m.ORIGINAL_SOURCE_GITBLOB,
                         "e1cfd2d5c518c2061ec91d1a9e8b64fc7ca69389")
        self.assertEqual(m.EXPECTED_SOURCE_EUPP_PLANTS,1408)
        self.assertTrue(m.ORIGINAL_SOURCE_URL.endswith("/ocr-traits/combined.csv"))
if __name__=="__main__":unittest.main()
