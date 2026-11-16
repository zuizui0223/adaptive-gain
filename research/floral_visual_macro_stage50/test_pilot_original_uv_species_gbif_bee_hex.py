"""Stage50 source-free, invented data only. Real bee/plant source CI is separate."""
import unittest
from unittest.mock import patch

from pilot_original_uv_species_gbif_bee_hex import (
    balanced_preoccurrence_sample,
    fixed_page_offsets,
    aggregate_plant_bee_exposure,
    retrieve_plant_occurrence_pilot,
    summary,
    PILOT_TOTAL,
)

def trait(key,source,pattern):
    return {
        "gbif_accepted_species_key":str(key),
        "source_study_DOIs":"10.1111/nph.13921" if source=="2016" else "10.3389/fpls.2021.618028",
        "source_measured_UV_spatial_pattern_or_missing":str(pattern),
        "source_taxon_aliases":"Mockus invented"+str(key)
    }

def bee_model():
    return {
        "HEX_A":{
            "eligibility":"AUTHOR_TREE_AND_PA_CELL_CUTOFF",
            "n_source_tree_and_pa_cutoff_Bombus_taxa":3,
            "n_source_tree_and_pa_cutoff_all_bee_taxa":40
        },
        "HEX_B":{
            "eligibility":"AUTHOR_TREE_AND_PA_CELL_CUTOFF",
            "n_source_tree_and_pa_cutoff_Bombus_taxa":7,
            "n_source_tree_and_pa_cutoff_all_bee_taxa":60
        },
        "HEX_UNKNOWN":{
            "eligibility":"OUTSIDE_AUTHOR_FILTERED_MODEL_NO_ABSENCE_INFERENCE",
            "n_source_tree_and_pa_cutoff_Bombus_taxa":None,
            "n_source_tree_and_pa_cutoff_all_bee_taxa":None
        },
    }


class GBIFCellSamplingQA(unittest.TestCase):
    def test_source_balanced_pilots_locked_before_occurrence(self):
        pool=[trait(i*1000+j,s,p) for i,s in enumerate(("2016","2021"))
              for p in (0,1) for j in range(1+p*100,21+p*100)]
        a=balanced_preoccurrence_sample(pool,n=15)
        b=balanced_preoccurrence_sample(list(reversed(pool)),n=15)
        self.assertEqual(a,b)
        self.assertEqual(len(a),60)
        self.assertEqual(len({x["taxon_key"] for x in a}),60)
        self.assertEqual(sum(x["source_primary_study"]=="2016" for x in a),30)
        self.assertEqual(sum(x["UV_pattern_source_binary"]==1 for x in a),30)

    def test_gbif_100k_index_and_nonoverlapping_fixed_pages(self):
        self.assertEqual(fixed_page_offsets(0),[])
        self.assertEqual(fixed_page_offsets(90),[0])
        self.assertEqual(fixed_page_offsets(150),[0])
        self.assertEqual(fixed_page_offsets(250),[0,150])
        self.assertEqual(fixed_page_offsets(470),[0,320])
        self.assertEqual(fixed_page_offsets(900000),[0,99850])
        with self.assertRaisesRegex(ValueError,"NO_GO_GBIF_TOTAL_COUNT"):
            fixed_page_offsets(-1)

    def test_two_pages_reject_duplicate_record_ids(self):
        selected={"taxon_key":88}
        def mock_request(x):
            off=x.get("offset")
            if off==0:return {"count":400,"results":[{"key":9},{"key":10}]}
            if off==250:return {"count":400,"results":[{"key":10},{"key":11}]}
            self.fail("unexpected fixed GBIF offset "+str(off))
        with patch("pilot_original_uv_species_gbif_bee_hex._request_json",
                   side_effect=mock_request):
            a=retrieve_plant_occurrence_pilot(selected)
        self.assertEqual(a["n_source_records_fetched_deduplicated"],3)
        self.assertEqual(a["gbif_requested_offsets"],[0,250])
        self.assertEqual(a["fetch_duplicate_or_id_issues"]["duplicate_page_record_ids"],1)
        self.assertTrue(a["not_random_sample_or_complete_native_range"])

    def test_same_species_true_polygon_quality_and_unknown_zero_differ(self):
        selected={"taxon_key":50,"source_primary_study":"2016",
                  "UV_pattern_source_binary":1,"source_taxon_name":"Mockus alpha",
                  "selection_rank_in_study_pattern":1}
        def point(key,lon,uncertainty=None,means=None):
            return {"key":key,"speciesKey":50,"decimalLatitude":20.,
                    "decimalLongitude":lon,"country":"MX",
                    "coordinateUncertaintyInMeters":uncertainty,
                    "establishmentMeans":means}
        raw={"records":[point(1,-10,1000),point(2,10,1000),
                        point(3,20,1000),point(4,10,None),
                        point(5,-10,20000),point(6,20,1000,"INTRODUCED")],
             "source_gbif_index_count_after_query_filters":9000,
             "gbif_requested_offsets":[0,8850],
             "source_search_100000_cap_truncated":False}
        def match(lon,lat,names,tree,transform):
            if lon<0:return ["HEX_A"]
            if lon==10:return ["HEX_B"]
            return ["HEX_UNKNOWN"]
        with patch("pilot_original_uv_species_gbif_bee_hex.matching_original_hex",
                   side_effect=match):
            v=aggregate_plant_bee_exposure(selected,raw,[],None,None,bee_model())
        self.assertEqual(v["n_eligible_model_source_occurrence_records"],2)
        self.assertEqual(v["n_eligible_source_model_cells_with_GBIF_plant_points"],2)
        self.assertAlmostEqual(v["modelled_Bombus_taxa_equal_visited_HEX_cell_mean_or_null"],5)
        self.assertEqual(v["source_record_quality_counts"]["outside_original_bee_model_eligibility_UNKNOWN"],1)
        self.assertEqual(v["source_record_quality_counts"]["explicitly_introduced_or_managed"],1)
        self.assertEqual(v["source_record_quality_counts"]["missing_uncertainty_not_quality_verified"],1)
        self.assertEqual(v["source_record_quality_counts"]["uncertainty_outside_10km"],1)
        self.assertTrue(v["not_a_Bombus_versus_UV_inferential_model"])

    def test_sampling_summary_does_not_claim_plant_distribution_estimation(self):
        rows=[]
        for s in ("2016","2021"):
            for p in (0,1):
                rows.extend({
                    "primary_original_UV_study":s,
                    "UV_pattern_direct_source_binary":p,
                    "n_eligible_model_source_occurrence_records":0,
                    "n_eligible_source_model_cells_with_GBIF_plant_points":0,
                    "original_gbif_filtered_index_count":1,
                    "source_records_retrieved_unique":1,
                    "source_search_100k_limit_truncated":False
                } for _ in range(15))
        self.assertEqual(len(rows),PILOT_TOTAL)
        res=summary(rows)
        self.assertEqual(res["n_pilot_species_with_any_source_model_eligible_records"],0)
        self.assertEqual(res["n_pilot_species_with_at_least_3_covered_cells_and_15_records"],0)
        self.assertTrue(res["no_globally_valid_UV_Bombus_statistical_significance_claim"])
        self.assertTrue(all(r["pilot_species_equal_mean_source_modelled_Bombus_taxa"] is None
                            for r in res["descriptive_study_by_source_pattern"]))


if __name__=="__main__":
    unittest.main()
