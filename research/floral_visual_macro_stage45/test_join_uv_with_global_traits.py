"""Source-free original 80 UV × 59k trait exact-name join tests."""
import unittest
from join_uv_with_global_traits import canonical_candidate,join_sources

class ExactBotanicalNameJoin(unittest.TestCase):
    def test_authors_trailing_and_uncertain_names(self):
        self.assertEqual(canonical_candidate("Salvia minarum Briq."),"Salvia minarum")
        self.assertEqual(canonical_candidate("Crotalaria micans Link"),"Crotalaria micans")
        self.assertIsNone(canonical_candidate("Eugenia sp."))
        self.assertIsNone(canonical_candidate("Sida cf. urens"))
        self.assertIsNone(canonical_candidate(""))

    def test_exact_join_only_cannot_infer_an_absence_or_bee_distribution(self):
        uu=[
          {"taxon_as_published":"Salvia minarum Briq.","uv_category":"CM",
           "uv_pattern_present":1,"non_uv_pattern_present":1,
           "pollination_system_reported":"Melittophilous"},
          {"taxon_as_published":"Sida cf. urens","uv_category":"BE",
           "uv_pattern_present":1,"non_uv_pattern_present":0,
           "pollination_system_reported":"Generalist"},
          {"taxon_as_published":"Mockus excluded","uv_category":"A",
           "uv_pattern_present":0,"non_uv_pattern_present":0,
           "pollination_system_reported":""}
        ]
        plants=[{"taxon":"Salvia minarum","wfo":"wfo-123",
                 "floral_colour_reported":1,"flower_colour":"blue",
                 "corolla_colour":"","flower_symmetry":""}]
        rows,counts=join_sources(uu,plants)
        self.assertEqual(len(rows),3)
        self.assertEqual(rows[0]["nhm_join_status"],
                         "EXACT_NAME_STRING_ONLY_NOT_TAXONOMIC_RECONCILIATION")
        self.assertEqual(rows[0]["uv_category_source_pdf"],"CM")
        self.assertEqual(rows[1]["nhm_join_status"],"NO_CANONICAL_BINOMIAL")
        self.assertEqual(rows[2]["nhm_join_status"],"NO_EXACT_TAXON_STRING_MATCH")
        self.assertTrue(all(r["gbif_taxonomic_acceptance"]=="not_checked" for r in rows))
        self.assertTrue(all(r["bombus_overlap_or_habitat_suitability"]=="not_estimated" for r in rows))

    def test_ambiguous_duplicate_name_not_overwritten(self):
        uu=[{"taxon_as_published":"Salvia minarum Briq.","uv_category":"CM",
             "uv_pattern_present":1,"non_uv_pattern_present":1,
             "pollination_system_reported":"Melittophilous"}]
        p=[{"taxon":"Salvia minarum","wfo":"a"},
           {"taxon":"Salvia minarum","wfo":"b"}]
        x,counts=join_sources(uu,p)
        self.assertEqual(x[0]["nhm_join_status"],"AMBIGUOUS_EXACT_TAXON_STRING")
        self.assertEqual(x[0]["nhm_taxon"],"")

if __name__=="__main__":
    unittest.main()
