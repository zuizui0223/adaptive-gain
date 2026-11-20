"""Stage114 original-source 72 mainland ERA5 gust vs lexical florist reporting diagnostic guards."""
import tempfile,unittest,zipfile
from pathlib import Path
from source72_real_ERA5point_flora3cue_reporting_analysis import (
  TARGETS,SOURCE_EXPOSURES,rank_partial,
  _partial_rank_with_source_blocks,true_source_association_sensitivity,
  verified_zip_member,join_source_frame,stage105_prior33_source)

def generate_data():
    rows=[]
    for i in range(72):
        wind=(i%13)/80+i/10000.
        doc=((i*7)%47+3)/65
        wfo=((i*17)%53+4)/65
        x={"TDWG_L3":"R%03d"%i,
           "source_geographic_block":"block%02d"%(i%17),
           "gust15_ERA5model_1991_2020_point":wind,
           "gust10_secondary":min(.9,wind*3),
           "gust20_secondary":wind/4,
           "NHM_colour_field_description_coverage":doc,
           "WFO_original_flora_description_coverage":wfo,
           "source_ERA5_point_latitude":float(i%30),
           "source_ERA5_1991_2020_mean_temperature_C":float(25-i%12),
           "WorldClim_1970_2000_precip_mm_month":float((i*11)%70),
           "n_AusTraits_original_measured_size_species":11 if i%3!=0 else 3,
           "near_visual_NHM_word_positive_per_native":doc*0.07+wind*.1,
           "near_visual_NHM_word_positive_per_colour_described":doc*.05+wind*.2,
           "chemical_WFO_positive_fragrance_per_description":wfo*.05+wind*.07,
           "chemical_WFO_positive_among_explicit_posneg":(i%4+1)/5.,
           "far_visual_AusTraits_measured_labelled_median_mm_ge3":float(8+i%9),
           "far_visual_AusTraits_measured_labelled_median_mm_ge10":float(8+i%9),
           "SOURCE_NHM_colour_reported_fraction":doc,
           "SOURCE_WFO_full_flora_prose_reporting_fraction":wfo}
        rows.append(x)
    return rows

class SourceReportingGuard(unittest.TestCase):
    def test_point_gust_variable_not_unverified_era5_CDS_hourly(self):
        self.assertEqual(SOURCE_EXPOSURES["gust15_ERA5model_1991_2020_point"],
                         "source_primary_fraction_days_daily_gust_strict_above_15_ms")
        self.assertEqual(len(SOURCE_EXPOSURES),3)
    def test_source_variables_are_lexical_reports_not_verified_traits(self):
        self.assertEqual(len(TARGETS),8)
        self.assertTrue("near_visual_NHM_word_positive_per_colour_described" in TARGETS)
        self.assertTrue("chemical_WFO_positive_among_explicit_posneg" in TARGETS)
        self.assertTrue("far_visual_AusTraits_measured_labelled_median_mm_ge10" in TARGETS)
    def test_output_all_source_results_are_descriptive_without_IID_p(self):
        result=true_source_association_sensitivity(generate_data())
        self.assertEqual(set(result),set(SOURCE_EXPOSURES))
        for expo,metrics in result.items():
            self.assertEqual(set(metrics),set(TARGETS))
            self.assertTrue(all(r["NO_source_region_IID_pvalue_or_causal_effect"] for r in metrics.values()))
    def test_doc_adjusted_and_full_block_rank_correlation_different_from_raw(self):
        result=true_source_association_sensitivity(generate_data())
        a=result["gust15_ERA5model_1991_2020_point"]["near_visual_NHM_word_positive_per_native"]
        self.assertEqual(a["n_original_exploratory_mainland_regions"],72)
        self.assertEqual(a["n_original_geographic_blocks"],17)
        self.assertIsNotNone(a["source_raw_Spearman_rho"])
        self.assertIsNotNone(a["source_partial_rank_after_NHM_WFO_documentation"])
        self.assertIsNotNone(a["source_partial_rank_after_doc_climate_geoBLOCK_fixed_effects"])
    def test_rare_true_measured_size_atleast10_must_reduce_region_n(self):
        x=true_source_association_sensitivity(generate_data())["gust15_ERA5model_1991_2020_point"]
        self.assertEqual(x["far_visual_AusTraits_measured_labelled_median_mm_ge3"]["n_original_exploratory_mainland_regions"],72)
        self.assertEqual(x["far_visual_AusTraits_measured_labelled_median_mm_ge10"]["n_original_exploratory_mainland_regions"],48)
    def test_source_geo_block_controls_not_labeled_phylogenetic(self):
        rows=generate_data()
        p=_partial_rank_with_source_blocks(rows,
            "gust15_ERA5model_1991_2020_point",
            "near_visual_NHM_word_positive_per_native",
            ("NHM_colour_field_description_coverage","WFO_original_flora_description_coverage"))
        self.assertTrue(p is None or -1<=p<=1)
    def test_fake_source_zip_and_fake_SHA_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"fake.zip"
            with zipfile.ZipFile(p,"w") as z:z.writestr("fake.csv","fake")
            with self.assertRaisesRegex(ValueError,"SHA_NOT_PINNED"):
                verified_zip_member(p,"NOT_A_FROZEN_SHA","fake.csv")
            with self.assertRaisesRegex(ValueError,"SOURCE_ZIP_SHA_DRIFT"):
                verified_zip_member(p,"0"*64,"fake.csv")
    def test_frozen_72_source_geo_identity_rejects_partial_or_unknown_region(self):
        climate={"AAA":{"spatial_block_id":"A","lat":4,"lon":3,
           "source_monthly_30yr_mean_T2m_C":{str(m):20 for m in range(1,13)},
           **{f:0 for f in SOURCE_EXPOSURES.values()}}}
        with self.assertRaisesRegex(ValueError,"GEO_IDENTITY_NOT_MATCHED"):
            join_source_frame(climate,{})
    def test_stage105_33_overlap_rejects_changed_weather_vs_source(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"fake.zip"
            with zipfile.ZipFile(p,"w") as z:z.writestr("no","source")
            with self.assertRaisesRegex(ValueError,"SOURCE_ZIP_SHA_DRIFT"):
                stage105_prior33_source(p,{},{})

if __name__=="__main__":unittest.main()
