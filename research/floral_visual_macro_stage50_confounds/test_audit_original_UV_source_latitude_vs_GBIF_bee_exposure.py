"""Only artificial paper and GBIF input rows. No invented real ecology."""
import unittest
from audit_original_UV_source_latitude_vs_GBIF_bee_exposure import (
    prepare,strict_latitude_and_genus_pairs,_json_list,
)

def pilot(study,pat,key,latjson="[20,40]",countries='["US"]',records="20",cells="4",bee="5"):
    return {
      "gbif_accepted_species_key":str(key),
      "primary_original_UV_study":study,
      "UV_pattern_direct_source_binary":str(pat),
      "sampled_GBIF_latitude_min_max":latjson,
      "source_record_country_codes":countries,
      "n_eligible_model_source_occurrence_records":records,
      "n_eligible_source_model_cells_with_GBIF_plant_points":cells,
      "modelled_Bombus_taxa_equal_visited_HEX_cell_mean_or_null":bee,
      "modelled_all_bee_taxa_equal_visited_HEX_cell_mean_or_null":"100" if bee else "",
    }

def nph(key,state,lat,genus="Potentilla"):
    return {
      "accepted_GBIF_species_match_status":"EXACT_CONFIDENT_SPECIES_MAPPED",
      "accepted_GBIF_taxon_key_or_empty":str(key),
      "source_measured_UV_pattern_present":str(state),
      "source_mean_latitude_deg":str(lat),
      "source_mean_UVB_J_per_m2_per_day":"2500",
      "source_mean_annual_temp_C":"9",
      "source_mean_annual_precip_mm":"900",
      "original_S1_author_full_binomial_candidate":genus+" invented"
    }


class OriginalPublishedLatitudeUVBSensitivityContracts(unittest.TestCase):
    def test_source_latitude_climate_and_2021_brazil_sampling_kept_distinct(self):
        p=[pilot("2016",1,10),pilot("2021",0,20,
                                  latjson="",countries='["BR","US"]',
                                  records="0",cells="0",bee="")]
        out=prepare(p,[nph(10,1,31)],expected_pilot=2,expected_nph=1)
        self.assertEqual(out[0]["original_2016_mean_source_latitude_or_null"],31)
        self.assertEqual(out[0]["original_2016_source_mean_UVB_or_null"],2500)
        self.assertTrue(out[0]["original_2016_source_mean_latitude_within_bounded_GBIF_index_page_range_or_unknown"])
        self.assertEqual(out[1]["original_2016_source_S2_record_count"],0)
        self.assertTrue(out[1]["original_2021_Cerrado_study_Brazil_in_sampled_eligible_GBIF_country_codes_or_unknown"])
        self.assertIsNone(out[1]["original_2016_mean_source_latitude_or_null"])
        self.assertTrue(out[1]["source_GBIF_plant_sample_not_species_native_range"])

    def test_missing_latitude_span_unknown_not_a_biological_absence(self):
        self.assertEqual(_json_list({"sampled_GBIF_latitude_min_max":""},
                                    "sampled_GBIF_latitude_min_max"),[])

    def test_wrong_source_UV_label_rejected(self):
        with self.assertRaisesRegex(ValueError,"NO_GO_PUBLISHED_SOURCE_UV"):
            prepare([pilot("2016",0,10)],[nph(10,1,30)],
                    expected_pilot=1,expected_nph=1)

    def test_nonmapped_2016_species_not_silently_assigned_a_study_site(self):
        with self.assertRaisesRegex(ValueError,"NO_GO_2016_PILOT_GBIF_KEY"):
            prepare([pilot("2016",0,10)],[nph(11,0,30)],
                    expected_pilot=1,expected_nph=1)

    def test_source_model_unknown_cells_cannot_have_numeric_bee_value(self):
        with self.assertRaisesRegex(ValueError,"NO_GO_OUTSIDE_MODELLED_BEE_SUPPORT_TREATED_AS_ZERO"):
            prepare([pilot("2016",1,10,records="0",cells="0",bee="5")],
                    [nph(10,1,30)],expected_pilot=1,expected_nph=1)

    def test_greedy_within_genus_latitude_pair_is_only_descriptive(self):
        q={
           "original_study":"2016",
           "meets_pilot_exposure_minimum":True,
           "original_2016_Genus_or_unknown":"Potentilla",
        }
        a={**q,"gbif_accepted_species_key":"10",
           "source_direct_UV_pattern_binary":1,
           "original_2016_mean_source_latitude_or_null":40,
           "mean_modelled_source_Bombus_taxa_or_null":4}
        b={**q,"gbif_accepted_species_key":"20",
           "source_direct_UV_pattern_binary":0,
           "original_2016_mean_source_latitude_or_null":42,
           "mean_modelled_source_Bombus_taxa_or_null":6}
        z=strict_latitude_and_genus_pairs([a,b])
        self.assertEqual(z["n_disjoint_within_Genus_and_5degree_original_source_latitude_pairs"],1)
        self.assertEqual(z["matched_pair_pattern_minus_uniform_mean_modelled_Bombus_source_names"],-2)
        self.assertTrue(z["insufficient_pairs_for_population_inference"])
        self.assertTrue(z["not_a_causal_climate_or_phylogenetic_control"])


if __name__=="__main__":
    unittest.main()
