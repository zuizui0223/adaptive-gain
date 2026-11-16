"""Stage53 mock-only GBIF checklist-native evidence safety and pagination."""
import unittest
from unittest.mock import patch
from urllib.error import URLError
from check_original_UV_species_native_distribution import (
    harmonize_country_claims,fetch_checklist_distribution,one_species,summary
)

class OriginalSpeciesCountryEvidenceQA(unittest.TestCase):
    def test_native_and_introduced_conflict_never_becomes_native(self):
        records=[
            {"country":"JP","establishmentMeans":"NATIVE","source":"checklist A"},
            {"country":"JP","establishmentMeans":"INTRODUCED","source":"checklist B"},
            {"country":"GB","establishmentMeans":"NATIVE","source":"checklist A"},
            {"country":"DE","establishmentMeans":"UNSPECIFIED","source":"checklist A"},
            {"country":"FR","establishmentMeans":None,"source":"checklist B"},
            {"country":"CH","establishmentMeans":"NATURALISED","source":"checklist B"},
            {"country":None,"establishmentMeans":"NATIVE","source":"checklist A"}
        ]
        r=harmonize_country_claims(records)
        self.assertEqual(r["explicit_native_nonconflicting_ISO_countries"],["GB"])
        self.assertEqual(r["conflicting_native_vs_introduced_ISO_countries"],["JP"])
        self.assertEqual(r["explicit_introduced_nonconflicting_ISO_countries"],["CH"])
        self.assertEqual(r["unresolved_ISO_countries"],["DE","FR"])
        self.assertEqual(r["n_distinct_checklist_sources_reported"],2)
        self.assertTrue(r["no_checklist_country_listing_is_NOT_a_nativity_absence"])

    def test_empty_distribution_is_not_true_native_absence(self):
        r=harmonize_country_claims([])
        self.assertEqual(r["n_checklist_items"],0)
        self.assertEqual(r["explicit_native_nonconflicting_ISO_countries"],[])
        self.assertTrue(r["native_status_only_if_explicit_and_not_conflicted"])

    def test_paging_advances_raw_count_instead_of_distinct_records(self):
        seen=[]
        one={"country":"US","establishmentMeans":"NATIVE"}
        def fake(url):
            seen.append(url)
            if "offset=0" in url:
                return {"results":[one,one],"endOfRecords":False}
            if "offset=2" in url:
                return {"results":[{"country":"CA","establishmentMeans":"NATIVE"}],
                        "endOfRecords":True}
            self.fail("unexpected page="+url)
        with patch("check_original_UV_species_native_distribution.fetch_json",side_effect=fake):
            x=fetch_checklist_distribution(42)
        self.assertEqual(len(x["items"]),2)
        self.assertEqual(x["pages"],2)
        self.assertFalse(x["truncated"])
        self.assertTrue("offset=2" in seen[1])

    def test_api_failure_is_unknown_never_zero_native(self):
        with patch("check_original_UV_species_native_distribution.fetch_json",
                   side_effect=URLError("temporary unavailable")):
            r=fetch_checklist_distribution(42)
        self.assertEqual(r["status"],"SOURCE_API_UNAVAILABLE_CHECKLIST_UNKNOWN")
        self.assertEqual(r["items"],[])
        self.assertTrue(r["truncated"])
        row={"gbif_accepted_species_key":"42","source_2016_UV_pattern":"1",
             "published_latitude_mean":"46","published_uvb_mean":"2200"}
        with patch("check_original_UV_species_native_distribution.fetch_checklist_distribution",
                   return_value=r):
            x=one_species(row)
        self.assertEqual(x["GBIF_checklist_api_status"],
                         "SOURCE_API_UNAVAILABLE_CHECKLIST_UNKNOWN")
        self.assertTrue(x["no_proven_current_native_species_range_polygon"])

    def test_159_original_taxon_denominator_and_group_audit(self):
        rows=[]
        for p,n in [(0,81),(1,78)]:
            for i in range(n):
                rows.append({
                    "original_source_2016_UV_pattern":p,
                    "n_checklist_items":2,
                    "explicit_native_nonconflicting_ISO_countries":["US"] if i%2==0 else [],
                    "conflicting_native_vs_introduced_ISO_countries":[],
                    "GBIF_checklist_source_record_truncated":False,
                    "GBIF_checklist_api_status":"GBIF_CHECKLIST_DISTRIBUTIONS_RETURNED"
                })
        r=summary(rows)
        self.assertEqual(r["original_source_accepted_species"],159)
        self.assertEqual(r["source_UV_pattern_state_counts"],{0:81,1:78})
        self.assertEqual(r["n_species_with_checklist_records"],159)
        self.assertTrue(r["GBIF_checklist_country_claim_not_native_range_polygon"])

if __name__=="__main__":
    unittest.main()
