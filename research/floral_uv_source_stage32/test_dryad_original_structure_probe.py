"""Stage32 SOURCE-FREE fixture tests. No original workbook content republished."""
from __future__ import annotations
import io
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

from dryad_original_structure_probe import inspect_archive,run,EXPECTED_ORIGINAL


def invented_archived_xlsx(sheet_names=('Array_UV','Array_Bullseye','Array_Inverse')):
    main='http://schemas.openxmlformats.org/spreadsheetml/2006/main'
    workbook='<workbook xmlns="%s"><sheets>%s</sheets></workbook>'%(
        main,''.join(
            '<sheet name="%s" sheetId="%d"/>'%(name,j+1)
            for j,name in enumerate(sheet_names)))
    stream=io.BytesIO()
    with zipfile.ZipFile(stream,'w',zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr('xl/workbook.xml',workbook)
    book=stream.getvalue()
    stream=io.BytesIO()
    with zipfile.ZipFile(stream,'w',zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr('data/'+EXPECTED_ORIGINAL,book)
    return stream.getvalue()


class Stage32DryadSourceShellTests(unittest.TestCase):
    def test_three_arrangement_tabs_no_independence_inference(self):
        r=inspect_archive(invented_archived_xlsx())
        self.assertEqual(r['status'],'ORIGINAL_DRYAD_ARCHIVE_AND_WORKBOOK_STRUCTURALLY_PRESENT')
        self.assertEqual(r['original_workbook_name'],EXPECTED_ORIGINAL)
        names=r['original_workbook_structure']['sheet_names']
        self.assertEqual(names,['Array_UV','Array_Bullseye','Array_Inverse'])
        self.assertEqual(r['original_workbook_structure']['sheet_count'],3)
        self.assertFalse(r['original_workbook_structure']['cell_values_or_headers_examined'])
        self.assertFalse(r['independent_array_count_inferred_from_sheet_rows'])
        self.assertEqual(r['experimental_effects_extracted'],0)
        self.assertFalse(r['original_excel_redistributed'])

    def test_unknown_workbook_name_does_not_guess_source(self):
        raw=invented_archived_xlsx().replace(b'FEKoskiSF2.xlsx',b'OtherBook01.xlsx')
        with self.assertRaises(ValueError):
            inspect_archive(raw)

    def test_unparseable_payload_rejected(self):
        with self.assertRaisesRegex(ValueError,'NOT_DRYAD_ZIP'):
            inspect_archive(b'not a zip archive')

    def test_duplicate_original_file_rejected(self):
        stream=io.BytesIO()
        orig=invented_archived_xlsx()
        with zipfile.ZipFile(io.BytesIO(orig)) as source:
            original=source.read('data/'+EXPECTED_ORIGINAL)
        with zipfile.ZipFile(stream,'w') as z:
            z.writestr('one/'+EXPECTED_ORIGINAL,original)
            z.writestr('two/'+EXPECTED_ORIGINAL,original)
        with self.assertRaisesRegex(ValueError,'ORIGINAL_WORKBOOK_MISSING_OR_DUPLICATE'):
            inspect_archive(stream.getvalue())

    def test_wrong_xlsx_worksheet_container_rejected(self):
        stream=io.BytesIO()
        with zipfile.ZipFile(stream,'w') as z:
            z.writestr(EXPECTED_ORIGINAL,b'PKnotreal')
        with self.assertRaises(ValueError):
            inspect_archive(stream.getvalue())

    def test_no_meta_effect_from_successful_source_archive(self):
        z=run(invented_archived_xlsx())
        self.assertTrue(z['not_biological_meta_result'])
        self.assertFalse(z['source_variances_extracted'])
        self.assertEqual(z['experimental_effects_extracted'],0)


if __name__=='__main__':
    unittest.main()
