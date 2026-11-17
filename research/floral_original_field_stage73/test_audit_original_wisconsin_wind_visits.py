"""Mock-only Wisconsin original author workbook source-grain guards."""
import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch
p=Path(__file__).with_name("audit_original_wisconsin_wind_visits.py")
spec=importlib.util.spec_from_file_location("s73b_wisconsin",p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class WisconsinOriginalAuthorWorkbookTests(unittest.TestCase):
    def test_original_git_blob_source_identity(self):
        self.assertEqual(m.SOURCE_BYTES,69522)
        self.assertEqual(m.SOURCE_GIT_BLOB_SHA1,"d456ddae4b5a737fc3351a5df612bd6a4b2c6244")
        self.assertEqual(len(m.gitblob_sha(b"HELLO")),40)

    def test_original_category_not_spectrometric_wavelength(self):
        self.assertEqual(m.EXPECTED_SHEETS,
                         ("plots","plants","visitors","plant_spp_traits","visitor_spp_traits"))
        self.assertIn("Pollination_neighborhood_data21.xlsx",m.SOURCE_URL)

    def test_source_excel_header_no_imputation(self):
        original={1:{0:"plot",1:"wind",2:"temp"},
                  2:{0:"2",1:"3",2:"78"},
                  3:{0:"3",1:"0"}}
        headings,rows=m.table_from_sheet(original)
        self.assertEqual(headings,["plot","wind","temp"])
        self.assertEqual(len(rows),2)
        self.assertNotIn("temp",rows[1])
        report=m.summarize_sheet("plots",original)
        self.assertEqual(report["original_wind_distinct_value_sample"],["0","3"])
        self.assertEqual(report["original_wind_raw_nonempty_count"],2)
        self.assertEqual(report["source_data_rows_nonempty_after_header"],2)

    def test_native_wind_absence_not_fake_zero(self):
        original={1:{0:"plot",1:"wind"},2:{0:"1"}}
        report=m.summarize_sheet("plots",original)
        self.assertNotIn("original_wind_raw_nonempty_count",report)

    def test_missing_five_required_sheets_fails(self):
        with (patch.object(m,"download_original_excel",return_value=b"not_real"),
              patch.object(m,"read_xlsx_sparse",return_value={"plots":{1:{0:"plot"}}})):
            with self.assertRaisesRegex(ValueError,"FIVE_REQUIRED_SHEETS"):
                m.run()

    def test_original_source_sheet_result_has_no_fitted_model(self):
        books={n:{1:{0:"plot",1:"wind"},2:{0:"1",1:"2"}}
               for n in m.EXPECTED_SHEETS}
        with (patch.object(m,"download_original_excel",return_value=b"fake_bytes"),
              patch.object(m,"read_xlsx_sparse",return_value=books)):
            result=m.run()
        self.assertFalse(result["original_source_wind_and_visits_association_fitted"])
        self.assertTrue(result["petal_wvl_is_ordinal_literature_color_NOT_spectrometric_nm"])
        self.assertTrue(result["visitor_zeros_are_not_inferred_from_absent_rows"])
        self.assertEqual(result["source_sheet_count"],5)

if __name__=="__main__":
    unittest.main()
