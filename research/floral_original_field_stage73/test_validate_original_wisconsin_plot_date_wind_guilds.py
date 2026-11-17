"""Mock-only Wisconsin original plot/site/date/trait access and date mismatch gates."""
import importlib.util
import unittest
import io,zipfile
from pathlib import Path
from unittest.mock import patch
p=Path(__file__).with_name("validate_original_wisconsin_plot_date_wind_guilds.py")
spec=importlib.util.spec_from_file_location("sourceWisconsinDates",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class WisconsinFieldJoinTests(unittest.TestCase):
    def test_original_workbook_epoch_is_read_not_assumed(self):
        for value,expected in (("0","EXCEL_1900"),("1","EXCEL_1904")):
            buff=io.BytesIO()
            with zipfile.ZipFile(buff,"w") as z:
                z.writestr("xl/workbook.xml",
                    '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
                    + '<workbookPr date1904="' + value + '"/></workbook>')
            self.assertEqual(m.workbook_original_date_system(buff.getvalue()),expected)

    def test_original_excel_serial_is_2021_not_2022(self):
        self.assertEqual(m.excel_date_1900("44383"),"2021-07-06")
        self.assertEqual(m.excel_date_1900("44408"),"2021-07-31")
        self.assertEqual(m.excel_date_1900("44749"),"2022-07-07")
    def test_no_imputation_for_arbitrary_date(self):
        self.assertIsNone(m.excel_date_1900("UNKNOWN"))
        self.assertIsNone(m.excel_date_1900("0"))
        self.assertIsNone(m.excel_date_1900("2021-07-06"))
    def test_source_field_join_key_includes_site_date_plot(self):
        a=m.join_key({"site":"A","date":"44383","plot":"1"})
        b=m.join_key({"site":"B","date":"44383","plot":"1"})
        c=m.join_key({"site":"A","date":"44386","plot":"1"})
        self.assertNotEqual(a,b)
        self.assertNotEqual(a,c)
    def test_missing_numeric_visitors_not_zero(self):
        self.assertIsNone(m.strict_nonnegative_number(""))
        self.assertIsNone(m.strict_nonnegative_number("NA"))
        self.assertIsNone(m.strict_nonnegative_number("-1"))
        self.assertEqual(m.strict_nonnegative_number("0"),0)
        self.assertEqual(m.strict_nonnegative_number("3.0"),3.)
    def test_2021_2022_conflict_fails_field_year_alignment(self):
        # Fixture is only source-grain, not a model; visitor is explicitly
        # present and can be joined to plot only with all three keys.
        books={
          "plots":{1:{0:"site",1:"date",2:"plot",3:"wind"},
                   2:{0:"A",1:"44383",2:"1",3:"1"}},
          "plants":{1:{0:"site",1:"date",2:"plot",3:"flower_sp"},
                    2:{0:"A",1:"44383",2:"1",3:"Monarda fistulosa"}},
          "visitors":{1:{0:"site",1:"date",2:"plot",3:"visitor_sp",4:"flower_sp",5:"flower_visits",6:"visitor_no"},
                      2:{0:"A",1:"44383",2:"1",3:"Bombus vagans",4:"Monarda fistulosa",5:"2",6:"1"}},
          "plant_spp_traits":{1:{0:"flower_sp",1:"petal_color"},
                              2:{0:"Monarda fistulosa",1:"purple"}},
          "visitor_spp_traits":{1:{0:"visitor_sp",1:"visitor_order"},
                              2:{0:"Bombus vagans",1:"Hymenoptera"}}
        }
        with (patch.object(m,"download_original_excel",return_value=b"mock"),
              patch.object(m,"workbook_original_date_system",return_value="EXCEL_1900"),
              patch.object(m,"read_xlsx_sparse",return_value=books)):
            r=m.summarize_field()
        self.assertTrue(r["author_README_vs_original_Excel_date_conflict_UNRESOLVED"])
        self.assertFalse(r["source_weather_year_alignment_allowed"])
        self.assertEqual(r["original_unique_complete_site_date_plot_keys"],1)
        self.assertEqual(r["field_plots_by_original_Beaufort_category"],{"1":1})
        self.assertFalse(r["source_flower_wind_guild_model_fitted"])
        self.assertEqual(r["source_wind_class_recorded_visitation_counts"]["1"]["source_literal_Bombus_genus_individuals"],1)
    def test_same_plot_id_different_sites_not_globally_collapsed(self):
        self.assertNotEqual(m.join_key({"site":"BEN","date":"44383","plot":"1"}),
                            m.join_key({"site":"UWM","date":"44383","plot":"1"}))

if __name__=="__main__":unittest.main()
