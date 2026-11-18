"""No artificial original macro data in tests: source-free key and method guards."""
import unittest
from audit_real_dopi_v2_ohashi_eupp_power import (
    normalized_name, normalized_doi, guild, source_site_key, publication_id
)

class Stage84SourceSemantics(unittest.TestCase):
    def test_only_strict_two_part_names(self):
        self.assertEqual(normalized_name("Trifolium_pratense"),"trifolium pratense")
        self.assertEqual(normalized_name("TARAXACUM OFFICINALE"),"taraxacum officinale")
        for s in ("Trifolium sp.","Trifolium cf. pratense","Trifolium",
                  "Trifolium repens subsp typicum","Bombus spp."):
            self.assertIsNone(normalized_name(s),s)
    def test_only_true_source_DOl(self):
        self.assertEqual(normalized_doi("https://doi.org/10.1111/geb.70000"),
                         "10.1111/geb.70000")
        self.assertEqual(normalized_doi("DOI:10.1002/ecy.3801"),"10.1002/ecy.3801")
        self.assertIsNone(normalized_doi("Unpublished data"))
        self.assertIsNone(normalized_doi(""))
    def test_study_label_not_publication(self):
        self.assertEqual(publication_id("23_Holzschuh"),publication_id("25_Holzschuh"))
        self.assertNotEqual(publication_id("4_Marini"),publication_id("5_Marini"))
    def test_bee_versus_visitor_recognition_conservative(self):
        self.assertEqual(guild({"pollinator_species":"Bombus terrestris",
          "pollinator_order":"Hymenoptera","pollinator_family":"Apidae"}),"BOMBUS")
        self.assertEqual(guild({"pollinator_species":"Apis mellifera",
          "pollinator_order":"Hymenoptera","pollinator_family":"Apidae"}),"OTHER_BEE")
        self.assertEqual(guild({"pollinator_species":"Eristalis tenax",
          "pollinator_order":"Diptera","pollinator_family":"Syrphidae"}),"NON_BEE_OR_UNRESOLVED")
        self.assertEqual(guild({"pollinator_species":"Bombus sp.",
          "pollinator_order":"Hymenoptera","pollinator_family":"Apidae"}),"UNRESOLVED_POLLINATOR")
    def test_no_publication_or_location_no_fabricated_site(self):
        source={"country":"France","year":"2019","month":"6","latitude":"47.00",
                "longitude":"4.0","habitat":"Grassland"}
        self.assertIsNone(source_site_key(source,None))
        self.assertEqual(source_site_key(source,"10.1111/geb.70000")[:4],
                         ("10.1111/geb.70000","France","2019","6"))
        source.pop("latitude")
        self.assertIsNone(source_site_key(source,"10.1111/geb.70000"))

if __name__=="__main__":unittest.main()
