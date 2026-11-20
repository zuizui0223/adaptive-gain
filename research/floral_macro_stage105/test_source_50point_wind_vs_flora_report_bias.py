"""Stage105: original source-only 33/50 no-holdout/floral reporting-bias guards."""
import unittest,tempfile,zipfile
from pathlib import Path
from source_50point_wind_vs_flora_report_bias import (
  archive_member,train_source_split,rank_partial,spearman_safe,analyse,weather_sources,
  qualified_training_data
)

def rank_source_rows():
    # A spurious raw wind-marking correlation solely driven by measurement
    # coverage should be attenuated in the rank residual diagnostic.
    rows=[]
    for i in range(16):
        wind=(i+1)/20.
        coverage=(i+1)/18.
        rows.append({
          "TDWG_L3":f"R{i:03d}","source_geographic_block":f"B{i//3:02d}",
          "one_region_representative_point_ERA5_derived_daily_gust15_fraction":wind,
          "NHM_flower_colour_documentation_coverage":coverage,
          "WFO_flora_description_coverage":coverage,
          "latitude":10+i,"mean_annual_T2m_C":5+i,
          "marking_lexical_positive_per_native":coverage,
          "marking_lexical_positive_per_colour_described":.05,
          "fragrance_positive_reports_per_WFO_description":coverage,
          "fragrance_positive_fraction_among_explicit_pos_and_neg":.25,
          "AusTraits_source_median_flower_diameter_mm":1+i,
          "n_original_AusTraits_measured_source_flower_diameter_species":5})
    return rows

class SourceGuards(unittest.TestCase):
    def test_partial_rank_all_variables_ranked(self):
        x=[.1,.2,.3,.4,.5,.6,.7,.8,.9,1.0]
        y=[1,2,4,3,5,8,6,7,10,9]
        c=[2,1,3,5,4,6,8,7,9,10]
        a=rank_partial(x,y,[c])
        self.assertIsNotNone(a)
        self.assertTrue(-1<=a<=1)
    def test_perfect_confounding_yields_unidentifiable_partial(self):
        x=[i for i in range(10)]
        y=[i for i in range(10)]
        self.assertIsNone(rank_partial(x,y,[x]))
    def test_raw_spearman_ties(self):
        self.assertAlmostEqual(spearman_safe([0,0,1,1,2],[1,1,2,2,3]),1.)
    def test_no_false_pvalues_or_confident_causal_output(self):
        rows=rank_source_rows()
        results=analyse(rows)
        self.assertIn("near_visual_source_positive_marking_per_native",results)
        self.assertIn("SOURCE_ascertainment_NHM_colour_coverage",results)
        self.assertIsNone(results["near_visual_source_positive_marking_per_colour_described"]["unadjusted_region_Spearman_rho"])
        self.assertTrue(all(x["NO_p_value_or_evolutionary_hypothesis_test"] for x in results.values()))
    def test_original_50_source_temporal_completeness(self):
        def s(i):
            return {"TDWG_L3":f"R{i:03d}","source_ERA5_observed_30yr_days":10958,
                 "source_primary_fraction_days_daily_gust_strict_above_15_ms":i/100}
        first={"source_completed_region_count":25,"sites":[s(i) for i in range(25)],
                "no_source_regional_area_weighting":True}
        second={"source_returned_distinct_region_count":25,
            "regions":[s(i) for i in range(25,50)],
            "source_prior25_exact_region_codes":[s(i)["TDWG_L3"] for i in range(25)],
            "region_area_weighting_performed":False}
        import json
        result=weather_sources(json.dumps(first),json.dumps(second))
        self.assertEqual(len(result),50)
        second["regions"][0]["source_ERA5_observed_30yr_days"]=365
        with self.assertRaises(ValueError):
            weather_sources(json.dumps(first),json.dumps(second))
    def test_geo_holdout_or_island_never_in_training(self):
        import csv,io
        hdr="TDWG_L3,land_scope,shared_split,spatial_block_id"
        rows=["R%03d,mainland,exploration,B%02d"%(i,i//5) for i in range(72)]
        d=train_source_split((hdr+"\n"+"\n".join(rows)+"\n").encode())
        self.assertEqual(len(d),72)
        rows[3]=rows[3].replace("mainland","island")
        with self.assertRaises(ValueError):train_source_split((hdr+"\n"+"\n".join(rows)+"\n").encode())
    def test_any_source_file_without_immutable_SHA_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"bad.zip"
            with zipfile.ZipFile(p,"w") as z:z.writestr("a.csv","something")
            with self.assertRaisesRegex(ValueError,"ORIGINAL_SOURCE_SHA_DRIFT"):
                archive_member(p,"a"*64,"a.csv")

if __name__=="__main__":unittest.main()
