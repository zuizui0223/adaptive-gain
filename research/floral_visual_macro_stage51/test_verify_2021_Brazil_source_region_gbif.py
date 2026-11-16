"""Only invented occurrence rows, never source biology or botanical phenotypes."""
import unittest
from unittest.mock import patch
from verify_2021_Brazil_source_region_gbif import (
  _page,evaluate_taxon,summary,original_site_hexes,
  SOURCE_DOI,SITE_HEX_BOMBUS_MODEL
)

def plant(key,pattern):
    return {"gbif_species_key":key,"UV_binary":pattern}

def rec(key,lon=-48.5036,lat=-22.9125,uncertainty=1000):
    return {"key":key,"speciesKey":42,"country":"BR",
            "decimalLongitude":lon,"decimalLatitude":lat,
            "coordinateUncertaintyInMeters":uncertainty}

class BrazilStudySourceFeasibility(unittest.TestCase):
    def test_explicit_brazil_study_region_query(self):
        with patch("verify_2021_Brazil_source_region_gbif._request_json",
                   return_value={"count":43,"results":[rec(1)]}) as q:
            r=_page(plant(42,1))
        params=q.call_args[0][0]
        self.assertEqual(params["country"],"BR")
        self.assertEqual(params["year"],"2010,2026")
        self.assertEqual(params["decimalLatitude"],"-23.5,-19.5")
        self.assertEqual(params["decimalLongitude"],"-50.0,-45.5")
        self.assertEqual(params["offset"],0)
        self.assertEqual(r["index_count"],43)

    def test_exact_original_study_hex_and_missing_uncertainty(self):
        specimen=[rec(1),rec(2,uncertainty=None),rec(3,uncertainty=20000),
                  rec(4,lon=-46.44,lat=-20.23)]
        data={"status":"GBIF_BRAZIL_STUDY_REGION_ONE_INDEX_PAGE",
              "index_count":75,"records":specimen}
        def match(lon,lat,names,tree,transform):
            return ["HEX8285"] if lon < -47 else ["HEX8252"]
        with patch("verify_2021_Brazil_source_region_gbif.matching_original_hex",
                   side_effect=match):
            r=evaluate_taxon(plant(42,1),data,[],None,None)
        self.assertEqual(r["n_qualified_in_predeclared_region_and_original_bee_hex"],2)
        self.assertEqual(r["n_qualified_points_in_original_study_site_candidate_HEX"],2)
        self.assertEqual(r["original_study_site_candidate_HEX"],["HEX8252","HEX8285"])
        self.assertEqual(r["quality_diagnostic_counts"]["uncertainty_missing_not_accepted"],1)
        self.assertEqual(r["quality_diagnostic_counts"]["coordinate_uncertainty_above_10km"],1)
        self.assertTrue(r["GBIF_record_no_proof_source_plant_UV_phenotype_measured_here"])

    def test_published_original_sites_three_model_hexes_locked(self):
        def fake(lon,lat,names,tree,transform):
            if lon < -49.2:return ["HEX8318"]
            if lon < -47:return ["HEX8285"]
            return ["HEX8252"]
        with patch("verify_2021_Brazil_source_region_gbif.matching_original_hex",
                   side_effect=fake):
            # This mock's original Santa corners cross two cells as published.
            all_ids=original_site_hexes([],None,None)
        self.assertEqual(all_ids,set(SITE_HEX_BOMBUS_MODEL))

    def test_source_region_GBIF_index_zero_is_not_plants_absent(self):
        row={
          "UV_pattern_source_category_binary":0,
          "source_gbif_region_index_count_or_unknown":0,
          "source_api_status":"GBIF_BRAZIL_STUDY_REGION_ONE_INDEX_PAGE",
          "n_GBIF_source_region_first_page_records":0,
          "n_qualified_in_predeclared_region_and_original_bee_hex":0,
          "n_qualified_points_in_original_study_site_candidate_HEX":0,
          "original_study_site_candidate_HEX":[]
        }
        rows=[dict(row,UV_pattern_source_category_binary=i%2) for i in range(71)]
        x=summary(rows)
        self.assertEqual(x["n_species_with_positive_filtered_Brazil_region_GBIF_index"],0)
        self.assertTrue(x["source_species_original_sample_sites_unknown"])
        self.assertTrue(x["not_a_valid_source_site_trait_SDM_regression"])

    def test_query_failure_is_unknown_not_absence(self):
        from urllib.error import URLError
        with patch("verify_2021_Brazil_source_region_gbif._request_json",
                   side_effect=URLError("slow original API")):
            x=_page(plant(42,0))
        self.assertIsNone(x["index_count"])
        self.assertEqual(x["status"],"GBIF_SOURCE_API_UNAVAILABLE_UNKNOWN_NOT_ZERO")


if __name__=="__main__":
    unittest.main()
