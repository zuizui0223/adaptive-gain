"""Stage107 WorldClim mean wind is not ERA5 gust, original holdout remains closed."""
import csv,io,tempfile,unittest,zipfile
from pathlib import Path
from source_WorldClim72_mainland_cue_report_sensitivity import (
    safe_original_stage_train,common_train_regions,
    rank_summary,source_wind_proxy_overlap
)

class Stage107SourceGuards(unittest.TestCase):
    def test_367_source_rows_filter_only_original_source_train(self):
        names=[f"R{i:03d}" for i in range(367)]
        header="TDWG_L3,value\n"
        raw=header+"".join(f"{n},1\n" for n in names)
        tr={k:{"TDWG_L3":k} for k in names[:72]}
        d=safe_original_stage_train(raw.encode(),tr)
        self.assertEqual(len(d),72)
        self.assertNotIn("R090",d)
    def test_missing_true_367_source_fails(self):
        x=b"TDWG_L3,value\nA,1\n"
        with self.assertRaises(ValueError):
            safe_original_stage_train(x,{"A":{}})
    def test_size_missing_not_zero(self):
        n=100
        tr={"A":{"spatial_block_id":"BLOCK"}}
        wind={"A":{"source_all_5climate_variables_at_12_or_more_points":"1",
           "worldclim_baseline_wind_m_s":"3.1",
           "region_sampling_latitude_mean":"24",
           "worldclim_baseline_mean_temperature_C":"8",
           "worldclim_baseline_precip_mm_month":"56",
           "worldclim_baseline_wind_m_s_valid_points":"48"}}
        trait={"A":{"n_native_source_species":"100",
            "n_original_WFO_full_flora_description_species":"60",
            "n_positive_marking_TEXT_SOURCE_CANDIDATES":"3",
            "n_source_floral_fragrance_lexical_positive":"1",
            "n_source_floral_fragrance_lexical_explicit_negative":"1"}}
        colour={"A":{"n_native":"100","n_source_colour_missing":"50"}}
        size={"A":{"n_original_WCVP_native_species_in_region":"100",
             "n_original_AusTraits_flower_diameter_species":"0",
             "diameter_median_mm_of_source_species":""}}
        with self.assertRaisesRegex(ValueError,"NOT_EXACT_72"):
            common_train_regions(wind,trait,colour,size,tr)
    def test_rank_summary_does_not_report_significance(self):
        rows=[]
        for i in range(15):
            rows.append({
               "TDWG_L3":f"R{i:03d}","source_geographic_block":f"B{i//3:02d}",
               "WorldClim2_1_1970_2000_mean_wind_m_s_NOT_ERA5_gust":i/2,
               "NHM_colour_field_description_coverage":i/20+.2,
               "WFO_original_flora_description_coverage":i/20+.1,
               "source_region_sampling_latitude":i+5,
               "WorldClim_1970_2000_mean_temperature_C":i,
               "WorldClim_1970_2000_precip_mm_month":i*7,
               "floral_marking_lexical_report_per_native":i/20,
               "floral_marking_lexical_report_per_colour_field_species":.1,
               "fragrance_positive_source_mention_per_flora_description":i/50,
               "fragrance_positive_among_explicit_pos_and_neg":.5,
               "AusTraits_original_measured_grade_median_mm":i+3.,
               "n_AusTraits_original_measured_size_species":5})
        d=rank_summary(rows)
        self.assertTrue(all(x["no_IID_pvalue_or_causal_inference"] for x in d.values()))
        self.assertIsNone(d["near_visual_pattern_lexical_per_colour_described"]["unadjusted_WorldClim_mean_wind_Spearman_rho"])
        self.assertEqual(d["near_visual_pattern_lexical_per_original_native"]["n_source_regions"],15)
    def test_same_33_source_code_names_required_for_proxy_check(self):
        d=[{"TDWG_L3":f"R{i:03d}","WorldClim2_1_1970_2000_mean_wind_m_s_NOT_ERA5_gust":i}
           for i in range(33)]
        raw="TDWG_L3,one_region_representative_point_ERA5_derived_daily_gust15_fraction\n"
        raw+="".join(f"R{i:03d},{i/100}\n" for i in range(33))
        a=source_wind_proxy_overlap(d,raw.encode())
        self.assertEqual(a["n_source_identical_TDWG_region_codes"],33)
        self.assertAlmostEqual(a["SOURCE_WorldClim_average_vs_ERA5_point_30yr_gust_Spearman_rho"],1.)
        with self.assertRaises(ValueError):
            source_wind_proxy_overlap(d,raw.replace("R003","MISSING").encode())
    def test_source_ZIP_is_required_SHA_checked_not_any_367_csv(self):
        from source_50point_wind_vs_flora_report_bias import archive_member
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"fake.zip"
            with zipfile.ZipFile(p,"w") as z:z.writestr("fake.csv","not audited")
            with self.assertRaisesRegex(ValueError,"ORIGINAL_SOURCE_SHA_DRIFT"):
                archive_member(p,"f"*64,"fake.csv")

if __name__=="__main__":unittest.main()
