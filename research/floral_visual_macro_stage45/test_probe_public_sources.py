"""All Stage45 source probing unit tests are mock-only and offline."""
import unittest
from unittest.mock import patch
from probe_public_sources import _safe_url,_resource_schema,_gbif_registry,NHM_RESOURCE


class ProbeContracts(unittest.TestCase):
    def test_public_api_hosts_only(self):
        self.assertEqual(_safe_url("https://api.gbif.org/v1/species/match"),
                         "https://api.gbif.org/v1/species/match")
        self.assertEqual(_safe_url("https://data.nhm.ac.uk/api/3/action/resource_show"),
                         "https://data.nhm.ac.uk/api/3/action/resource_show")
        for u in ("http://data.nhm.ac.uk", "https://evil.example.org/data",
                  "https://api.gbif.org.evil.example.org/data"):
            with self.assertRaisesRegex(ValueError,"NO_GO_UNTRUSTED_SOURCE_HOST"):
                _safe_url(u)

    def test_nhm_schema_evidence_not_a_guide_presence_label(self):
        def fake(action,params):
            if action=="resource_show":
                return {"id":NHM_RESOURCE,"name":"combined.csv",
                        "size":17279412,"url":"https://data.nhm.ac.uk/media/xxx"}
            self.assertEqual(action,"datastore_search")
            return {"total":59369,"fields":[
                {"id":"scientificName"},{"id":"flower_colour"},
                {"id":"floral_pattern"},{"id":"leaf_length"}],
                "records":[{"scientificName":"Mockus example",
                            "flower_colour":"blue",
                            "floral_pattern":None,"leaf_length":10}]}
        with patch("probe_public_sources._ckan",side_effect=fake):
            x=_resource_schema()
        self.assertEqual(x["datastore_total"],59369)
        self.assertEqual(x["potential_floral_columns_not_confirmed_trait_status"],
                         ["flower_colour","floral_pattern"])
        self.assertTrue(x["only_source_schema_not_any_species_claim"])
        self.assertEqual(x["first_record_field_types"]["floral_pattern"]["type"],
                         "NoneType")

    def test_unconfirmed_genus_match_is_no_go(self):
        with patch("probe_public_sources._get_json",
                   return_value={"rank":"GENUS","canonicalName":"Bombus"}):
            with self.assertRaisesRegex(ValueError,"NO_GO_GBIF_BOMBUS"):
                _gbif_registry()

    def test_valid_bombus_counts_not_suitability(self):
        def fake(url):
            if "/species/match" in url:
                return {"usageKey":1340278,"rank":"GENUS","canonicalName":"Bombus",
                        "matchType":"EXACT","status":"ACCEPTED"}
            if "/occurrence/search" in url:
                return {"count":40000,"results":[]}
            return {"count":270,"results":[
                {"rank":"SPECIES","status":"ACCEPTED",
                 "canonicalName":"Bombus example"}]}
        with patch("probe_public_sources._get_json",side_effect=fake):
            x=_gbif_registry()
        self.assertEqual(x["genus_taxon_key"],1340278)
        self.assertEqual(x["taxon_index_species_query_total_raw"],270)
        self.assertTrue(x["not_native_distribution_not_habitat_suitability_or_realized_visit"])


if __name__=="__main__":
    unittest.main()
