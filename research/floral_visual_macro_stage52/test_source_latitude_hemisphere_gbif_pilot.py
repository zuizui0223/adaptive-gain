"""Source-free fake spatial and original lat tercile controls."""
import unittest
from unittest.mock import patch
from source_latitude_hemisphere_gbif_pilot import (
 select_source_2016,_request_hemisphere,_accumulate,report
)

def source_rows():
    rows=[]
    for p,n in ((0,81),(1,78)):
        for i in range(n):
            rows.append({
               "gbif_accepted_species_key":str(p*1000+i+1),
               "source_2016_UV_pattern":str(p),
               "published_latitude_mean":str(20+(i+1)*.61),
               "original_2016_source_genus_or_unknown":"Potentilla",
               "published_uvb_mean":"2750",
               "published_annual_temp_mean":"5"
            })
    return rows

class LatitudeHemispheresNotNativeRange(unittest.TestCase):
    def test_immutable_60_species_sample_balanced_across_UV_and_lat_tercile(self):
        original=source_rows()
        a=select_source_2016(original)
        b=select_source_2016(list(reversed(original)))
        self.assertEqual(a,b)
        self.assertEqual(len(a),60)
        self.assertEqual(len({r["gbif_accepted_species_key"] for r in a}),60)
        for p in (0,1):
            for tercile in (1,2,3):
                self.assertEqual(sum(
                   r["original_source_UV_pattern_binary"]==p and
                   r["original_latitude_tercile_within_pattern"]==tercile for r in a),10)

    def test_signed_latitude_not_assumed_and_two_absolute_mirrored_windows(self):
        species={"gbif_accepted_species_key":11,
                 "original_mean_published_latitude_positive_deg":44}
        args=[]
        def fake(q):
            args.append(q)
            return {"count":45,"results":[]}
        with patch("source_latitude_hemisphere_gbif_pilot._request_json",side_effect=fake):
            n=_request_hemisphere(species,"N")
            s=_request_hemisphere(species,"S")
        self.assertEqual(args[0]["decimalLatitude"],"40.0000,48.0000")
        self.assertEqual(args[1]["decimalLatitude"],"-48.0000,-40.0000")
        self.assertEqual(n["count"],45)
        self.assertEqual(s["count"],45)

    def test_source_ineligible_hex_is_unknown_not_zero_or_bee_absence(self):
        species={"gbif_accepted_species_key":11}
        observed=[
            {"key":1,"speciesKey":11,"decimalLongitude":-8.,"decimalLatitude":42.,
             "coordinateUncertaintyInMeters":1500},
            {"key":2,"speciesKey":11,"decimalLongitude":-7.,"decimalLatitude":42.,
             "coordinateUncertaintyInMeters":1500},
            {"key":3,"speciesKey":11,"decimalLongitude":-8.,"decimalLatitude":42.,
             "coordinateUncertaintyInMeters":None},
            {"key":4,"speciesKey":11,"decimalLongitude":-8.,"decimalLatitude":42.,
             "coordinateUncertaintyInMeters":1000,"establishmentMeans":"INTRODUCED"}
        ]
        res={"status":"GBIF_ORIGINAL_LATITUDE_WINDOW_ONE_PAGE","count":4,
             "records":observed,"search_latitude_bounds":(40,48)}
        model={"A":{"eligible":True,"bombus":3,"allbee":41},
               "B":{"eligible":False,"bombus":None,"allbee":None}}
        def cell(lon,*other):return ["A"] if lon==-8 else ["B"]
        with patch("source_latitude_hemisphere_gbif_pilot.matching_original_hex",
                   side_effect=cell):
            r=_accumulate(species,"N",res,[],None,None,model)
        self.assertEqual(r["n_qualified_original_source_bee_HEX_records"],1)
        self.assertEqual(r["n_distinct_visited_eligible_bee_hex_cells"],1)
        self.assertEqual(r["modelled_Bombus_names_per_visited_bee_hex_equal_cell_mean_or_null"],3)
        self.assertEqual(r["geospatial_quality_exclusions"]["unknown_Bee_model_hex_NOT_ZERO"],1)
        self.assertEqual(r["geospatial_quality_exclusions"]["unknown_uncertainty"],1)
        self.assertEqual(r["geospatial_quality_exclusions"]["explicit_non_native_or_cultivated"],1)
        self.assertTrue(r["not_source_native_range_or_actual_UV_measurement_sites"])

    def test_insufficient_samples_do_not_create_biological_effect(self):
        rows=[]
        for p in (0,1):
            for t in (1,2,3):
                for n in range(10):
                    x={"GBIF_query_status":"GBIF_ORIGINAL_LATITUDE_WINDOW_ONE_PAGE",
                       "n_qualified_original_source_bee_HEX_records":0,
                       "n_distinct_visited_eligible_bee_hex_cells":0,
                       "modelled_Bombus_names_per_visited_bee_hex_equal_cell_mean_or_null":None,
                       "modelled_all_bee_names_per_visited_bee_hex_equal_cell_mean_or_null":None}
                    rows.append({
                        "original_source_UV_pattern_binary":p,
                        "original_latitude_tercile_within_pattern":t,
                        "comparison_original_published_latitude_signedness":
                          "NEITHER_HAS_5_QUALIFIED_SOURCE_OCCURRENCES",
                        "n_source_hemispheres_meeting_minimum_5_quality_points":0,
                        "source_hemisphere_N_GBIF":x,
                        "source_hemisphere_S_GBIF":x
                    })
        out=report(rows)
        self.assertEqual(out["n_pilot_2016_UV_species"],60)
        self.assertEqual(out["n_species_any_hemisphere_at_least_5_quality_points"],0)
        self.assertTrue(out["no_global_UV_pattern_by_Bombus_regression_or_significance"])


if __name__=="__main__":
    unittest.main()
