"""Mock only. An example XLSX workbook does not become published bee data."""
import io,zipfile,unittest
from probe_2017_wind_visual_odor_original_data import workbook_schema,inspect_archive

def zblob(files):
    b=io.BytesIO()
    with zipfile.ZipFile(b,"w",compression=zipfile.ZIP_DEFLATED) as z:
        for k,v in files.items():z.writestr(k,v)
    return b.getvalue()

def fake_xlsx():
    ns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    return zblob({
      "xl/workbook.xml":f'<workbook xmlns="{ns}"><sheets><sheet name="Wind" sheetId="1"/></sheets></workbook>',
      "xl/sharedStrings.xml":f'<sst xmlns="{ns}"><si><t>treatment</t></si><si><t>bee</t></si></sst>',
      "xl/worksheets/sheet1.xml":f'<worksheet xmlns="{ns}"><dimension ref="A1:B2"/>'
        '<sheetData><row r="1"><c r="A1" t="s"><v>0</v></c>'
        '<c r="B1" t="s"><v>1</v></c></row>'
        '<row r="2"><c r="A2" t="inlineStr"><is><t>wind_and_odour</t></is></c>'
        '<c r="B2"><v>42</v></c></row></sheetData></worksheet>'
    })

class OriginalPriorWorkWindVisionOdorContracts(unittest.TestCase):
    def test_source_schema_preserves_names_and_not_fake_route_policy(self):
        r=workbook_schema(fake_xlsx())
        self.assertEqual(r["source_workbook_sheet_names"],["Wind"])
        self.assertEqual(r["source_worksheets"][0]["first_10_source_row_schema_only"][0],
                          ["treatment","bee"])
        self.assertTrue(r["original_2017_individual_trial_rows_not_yet_reconstructed"])
    def test_archive_reports_four_arms_not_full_three_way_causal_interaction(self):
        a=inspect_archive(zblob({"supplement/rsos170996supp2.xlsx":fake_xlsx(),
                                 "supplement/rsos170996supp1.pdf":b"%PDF-1.4"}))
        self.assertEqual(a["number_detected_xlsx_members"],1)
        self.assertTrue(a["2017_wind_four_arms_n18_each_not_complete_three_way_factorial"])
        self.assertTrue(a["no_conditional_first_cue_policy_or_pollen_deposition_label_inferred"])
        self.assertTrue(a["existing_visual_backup_wind_result_NOT_NEW_FLORAL_FINDING"])
    def test_not_excel_or_no_source_rejected(self):
        with self.assertRaisesRegex(ValueError,"NOT_XLSX"):
            workbook_schema(zblob({"fake.txt":b"data"}))
        with self.assertRaisesRegex(ValueError,"NOT_AUTHOR"):
            inspect_archive(b"not a zip")
if __name__=="__main__":unittest.main()
