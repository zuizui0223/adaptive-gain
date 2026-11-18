"""Mock source tests: 392 width-first cohort and ERA5 no-bee selection."""
import importlib.util,unittest
from pathlib import Path
s=importlib.util.spec_from_file_location("source79i",Path(__file__).with_name("source_sizefirst_392_network_ERA5_gust_Bombus.py"))
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)

class OriginalSizeFirstSelection(unittest.TestCase):
    def test_selects_year_location_month_without_Bombus_or_gust(self):
        traits=[];sites=[]
        for i in range(392):
            study="Study"+str(i%40)
            net="Network"+str(i)
            for species,width in (("caltha palustris","2"),("linum perenne","1")):
                traits.append({"Study_id":study,"Network_id":net,"Year":"2018",
                  "original_plant_literal_accepted_name":species,
                  "source_petal_max_width_cm":width})
            sites.append({"Study_id":study,"Network_id":net,"Year":"2018",
                 "Latitude_original":str(52+(i%5)*.15),"Longitude_original":str(4+(i%4)*.3),
                 "source_observed_visit_months":"5,6"})
        selected,report=m.build_size_first_frame(traits,sites)
        self.assertEqual(report["original_all_networks_with_two_distinct_botanical_petal_widths"],392)
        self.assertEqual(report["frozen_source_studies"],40)
        self.assertGreaterEqual(report["frozen_source_site_networks"],90)
        self.assertTrue(report["source_visiting_bee_outcome_not_used_in_selection"])
        self.assertTrue(all(r["pre_selected_without_original_Bombus_or_ERA5_gust_outcome"] for r in selected))
    def test_duplicate_source_width_comparison_not_qualified(self):
        rows=[{"Study_id":"S","Network_id":"1","Year":"2020",
             "original_plant_literal_accepted_name":sp,"source_petal_max_width_cm":"1.0"}
            for sp in ("x alba","y alba")]
        self.assertEqual(len({r["source_petal_max_width_cm"] for r in rows}),1)
    def test_all_months_january_are_not_justified_as_actual_flowering_survey(self):
        self.assertTrue(m.EXCLUDE_UNRESOLVED_JANUARY)
        self.assertEqual(m.MAX_PER_STUDY,5)
    def test_original_strong_gust_source_not_mean_worldclim_wind(self):
        self.assertEqual(m.MIN_PRE_SOURCE_STUDIES,30)
        self.assertIn("petal",m.__doc__)
if __name__=="__main__":unittest.main()
