"""Synthetic GBIF protocol tests; only real API run can declare original taxa."""
import unittest
from unittest.mock import patch
from gbif_taxon_occurrence_seed import validate_taxon_match,resolve_original_taxon,summarize,_get_json

class GbifSeedContract(unittest.TestCase):
    def test_high_confidence_exact_accepted_species_only(self):
        m=validate_taxon_match("Salvia minarum",{
            "canonicalName":"Salvia minarum","rank":"SPECIES",
            "confidence":100,"matchType":"EXACT","status":"ACCEPTED",
            "usageKey":123,"kingdom":"Plantae"})
        self.assertEqual(m["gbif_accepted_species_key"],123)
        self.assertEqual(m["status"],"EXACT_HIGH_CONFIDENCE_SPECIES_MAPPED")

    def test_reject_fuzzy_genus_only_or_wrong_canonical(self):
        base={"canonicalName":"Salvia minarum","rank":"SPECIES",
              "confidence":100,"matchType":"EXACT","status":"ACCEPTED",
              "usageKey":123,"kingdom":"Plantae"}
        for key,value in (("confidence",80),("rank","GENUS"),
                          ("matchType","FUZZY"),("canonicalName","Salvia other")):
            d=dict(base);d[key]=value
            self.assertEqual(validate_taxon_match("Salvia minarum",d)["status"],
                             "NOT_EXACT_HIGH_CONFIDENCE_SPECIES")

    def test_synonym_acceptance_requires_valid_accepted_usage_key(self):
        m=validate_taxon_match("Salvia minarum",{
            "canonicalName":"Salvia minarum","rank":"SPECIES",
            "confidence":100,"matchType":"EXACT","status":"SYNONYM",
            "usageKey":1,"acceptedUsageKey":234,"kingdom":"Plantae"})
        self.assertEqual(m["gbif_accepted_species_key"],234)
        bad=validate_taxon_match("Salvia minarum",{
            "canonicalName":"Salvia minarum","rank":"SPECIES",
            "confidence":100,"matchType":"EXACT","status":"SYNONYM",
            "usageKey":1,"kingdom":"Plantae"})
        self.assertEqual(bad["status"],"NO_ACCEPTED_SPECIES_KEY")

    def test_occurrence_counts_not_absence_or_suitability(self):
        src={"taxon_as_published":"Salvia minarum Briq.","uv_category":"CM",
             "uv_pattern_present":1,"pollination_system_reported":"Melittophilous"}
        def fake(endpoint,params):
            if endpoint=="species/match":
                return {"canonicalName":"Salvia minarum","rank":"SPECIES",
                        "confidence":100,"matchType":"EXACT","status":"ACCEPTED",
                        "usageKey":123,"kingdom":"Plantae"}
            return {"count":0}
        with patch("gbif_taxon_occurrence_seed._get_json",side_effect=fake):
            x=resolve_original_taxon(src)
        self.assertEqual(x["gbif_accepted_taxon_key"],123)
        self.assertEqual(x["georeferenced_occurrence_count"],0)
        self.assertTrue(x["not_native_distribution_or_predicted_suitability"])

    def test_genus_only_uncertain_source_not_queried(self):
        src={"taxon_as_published":"Eugenia sp.","uv_category":"A",
             "uv_pattern_present":0,"pollination_system_reported":"Generalist"}
        with patch("gbif_taxon_occurrence_seed._get_json",
                   side_effect=AssertionError("must not call GBIF")):
            x=resolve_original_taxon(src)
        self.assertEqual(x["gbif_taxonomy_status"],"UNRESOLVED_SOURCE_NAME")
        self.assertEqual(x["georeferenced_occurrence_count"],"")

    def test_summary_does_not_infer_species_richness_from_counts(self):
        row={"gbif_taxonomy_status":"UNRESOLVED_SOURCE_NAME",
             "georeferenced_occurrence_count":"","uv_pattern_measured":0}
        x=summarize([dict(row) for _ in range(80)])
        self.assertEqual(x["matched_exact_species"],0)
        self.assertTrue(x["GBIF_counts_not_species_distribution_predictions"])

    def test_no_unregistered_GBIF_endpoint(self):
        with self.assertRaisesRegex(ValueError,"NO_GO_UNREGISTERED"):
            _get_json("occurrence/download",{})

if __name__=="__main__":
    unittest.main()
