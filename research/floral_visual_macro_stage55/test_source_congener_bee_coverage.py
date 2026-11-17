"""Offline QA only: never synthesize plant occurrences or bee presences."""
import unittest
from source_congener_bee_coverage import (
    original_taxon_task,normalise_exposure,paired_contrasts,summarize,TIERS
)

def source_row(key,status,lat=43.2):
    return {"GBIF_accepted_species_key":str(key),
            "UV_2016_original_measured_pattern":status,
            "2016_original_latitude_N":lat}

def outcome(n,h,b,a,status="GBIF_ORIGINAL_LATITUDE_WINDOW_ONE_PAGE"):
    return normalise_exposure({
       "n_qualified_original_source_bee_HEX_records":n,
       "n_distinct_visited_eligible_bee_hex_cells":h,
       "GBIF_query_status":status,
       "modelled_Bombus_names_per_visited_bee_hex_equal_cell_mean_or_null":b,
       "modelled_all_bee_names_per_visited_bee_hex_equal_cell_mean_or_null":a
    })

def pair(k1=1,k0=2,tier=None):
    return {"comparison_tier":tier or TIERS[-1],
            "UV_patterned_GBIF_key":str(k1),
            "UV_uniform_GBIF_key":str(k0),
            "same_original_study_genus":"Potentilla",
            "n_shared_Kew_verified_native_WGSRPD_L3":1}

class Source159PairedGuildCoverageContract(unittest.TestCase):
    def test_source_1_is_patterned_zero_is_uniform_congener_codes(self):
        self.assertEqual(original_taxon_task(source_row(1,1))
                         ["original_source_UV_pattern_binary"],1)
        self.assertEqual(original_taxon_task(source_row(2,0))
                         ["original_source_UV_pattern_binary"],0)
        with self.assertRaisesRegex(ValueError,"NO_GO_SOURCE_2016"):
            original_taxon_task(source_row(4,1,-43))

    def test_paired_Bombus_fraction_direction_uses_pattern_minus_uniform(self):
        obs={"1":outcome(20,4,9,100),"2":outcome(20,4,3,100)}
        rows=paired_contrasts([pair()],obs,{"1":1,"2":0})
        self.assertTrue(rows[0]["minimum15_records_3_hex_paired_coverage_ok"])
        self.assertAlmostEqual(rows[0][
          "minimum15_records_3_hex_source_modelled_Bombus_fraction_pattern_minus_uniform"
        ],0.06)
        self.assertEqual(rows[0][
          "minimum15_records_3_hex_source_modelled_Bombus_names_pattern_minus_uniform"
        ],6.0)

    def test_missing_model_api_or_zero_all_bee_is_not_true_guild_absence(self):
        obs={"1":outcome(0,0,None,None,
            "GBIF_API_UNAVAILABLE_UNKNOWN_NOT_ABSENCE"),
             "2":outcome(20,3,0,0)}
        rows=paired_contrasts([pair()],obs,{"1":1,"2":0})
        self.assertFalse(rows[0]["minimum5_records_2_hex_paired_coverage_ok"])
        self.assertIsNone(rows[0][
            "minimum5_records_2_hex_source_modelled_Bombus_fraction_pattern_minus_uniform"])
        self.assertIn("UNKNOWN",rows[0][
            "minimum5_records_2_hex_reason_if_unavailable"])

    def test_no_invented_independent_sister_pairs_or_repeated_taxon(self):
        obs={"1":outcome(20,4,9,100),"2":outcome(20,4,3,100)}
        with self.assertRaisesRegex(ValueError,"LABEL_MISMATCH"):
            paired_contrasts([pair()],obs,{"1":0,"2":1})
        with self.assertRaisesRegex(ValueError,"NONINDEPENDENCE"):
            paired_contrasts([pair(),pair()],obs,{"1":1,"2":0})

    def test_guard_nonfinite_richness_and_one_sided_missing(self):
        with self.assertRaisesRegex(ValueError,"ONE_RICHNESS_MISSING"):
            outcome(10,2,2,None)
        with self.assertRaisesRegex(ValueError,"OUTSIDE_SOURCE_BOUNDS"):
            outcome(10,2,8,3)
        with self.assertRaisesRegex(ValueError,"OUTSIDE_SOURCE_BOUNDS"):
            outcome(10,2,float("nan"),50)

    def test_summary_retains_all_three_caliper_tiers_and_coverage_floor(self):
        obs={"1":outcome(20,4,9,100),"2":outcome(20,4,3,100)}
        pairs=paired_contrasts([pair(1,2,t) for t in TIERS],obs,{"1":1,"2":0})
        report=summarize(obs,pairs)
        self.assertEqual(report["n_2016_source_measured_unique_GBIF_accepted_species"],2)
        for t in TIERS:
            self.assertEqual(report["comparison_tiers"][t]["coverage_tiers"]
                             ["minimum5_records_2_hex"]["n_pairs_with_both_modelled_exposures"],1)
            self.assertTrue(report["no_p_values_due_to_source_genera_and_nonrandom_data"])

if __name__=="__main__":
    unittest.main()
