"""Stage77D original source VOC workbook authenticity, taxonomy and unknownness tests."""
from __future__ import annotations
import importlib.util
import io
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

p=Path(__file__).with_name("reconstruct_original_multispecies_VOC_XLSX_species_overlap.py")
spec=importlib.util.spec_from_file_location("st77d_voc_source",p)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def fixture_xlsx(header="Species",taxon="Gentiana lutea"):
    wb=b'''<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
      xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
      <sheets><sheet name="VOC_Species" sheetId="1" r:id="rId1"/></sheets></workbook>'''
    rel=b'''<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
      <Relationship Id="rId1"
       Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet"
       Target="worksheets/sheet1.xml"/></Relationships>'''
    sheet=(
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>'
        '<row r="1"><c r="A1" t="inlineStr"><is><t>'+header+'</t></is></c>'
        '<c r="B1" t="inlineStr"><is><t>VOCs</t></is></c></row>'
        '<row r="2"><c r="A2" t="inlineStr"><is><t>'+taxon+'</t></is></c>'
        '<c r="B2"><v>0.45</v></c></row>'
        '<row r="3"><c r="A3" t="inlineStr"><is><t>Undetermined</t></is></c>'
        '<c r="B3"><v>0.00</v></c></row>'
        '</sheetData></worksheet>'
    ).encode()
    b=io.BytesIO()
    with zipfile.ZipFile(b,"w",zipfile.ZIP_DEFLATED) as z:
        z.writestr("xl/workbook.xml",wb)
        z.writestr("xl/_rels/workbook.xml.rels",rel)
        z.writestr("xl/worksheets/sheet1.xml",sheet)
    return b.getvalue()

class OriginalFloralVOCSpeciesGuards(unittest.TestCase):
    def test_original_published_not_automatically_305(self):
        self.assertEqual(m.SOURCE_ARTICLE,"10.3389/fpls.2020.01154")
        self.assertEqual(m.ZIP_SIZE,8428937)
        self.assertEqual(len(m.ZIP_SHA),64)
        self.assertEqual(len(m.XLSX),3)

    def test_genuine_author_excel_text_plant_name_found_only_in_species_column(self):
        sheets,taxa=m.original_workbook(fixture_xlsx(),"mock_source.xlsx")
        self.assertEqual(len(sheets),1)
        self.assertEqual(taxa,{"gentiana lutea"})
        self.assertEqual(sheets[0]["source_sheet"],"VOC_Species")
        self.assertEqual(sheets[0]["source_nonempty_rows"],3)
        self.assertEqual(len(sheets[0]["semantic_exact_plant_species_header_evidence"]),1)

    def test_VOC_molecule_name_in_unlabelled_column_not_a_plant(self):
        sheets,taxa=m.original_workbook(fixture_xlsx(header="Compound",taxon="Linalool oxide"),"mock_source.xlsx")
        self.assertEqual(taxa,set())
        self.assertEqual(sheets[0]["semantic_exact_plant_species_header_evidence"],[])

    def test_missing_original_taxon_cannot_become_zero_VOC(self):
        sheets,taxa=m.original_workbook(fixture_xlsx(taxon="Species unidentified"),"mock_source.xlsx")
        self.assertEqual(taxa,set())
        self.assertTrue(sheets[0]["no_taxa_guessed_from_compound_or_pollinator_names"])

    def test_not_an_XLSX_is_never_extracted(self):
        with self.assertRaisesRegex(ValueError,"NOT_XLSX"):
            m.original_workbook(b"<html>Access denied</html>","no.xlsx")

    def test_cell_references_consistent_with_original_columns(self):
        self.assertEqual(m.col_idx("A1"),0)
        self.assertEqual(m.col_idx("AA202"),26)
        self.assertEqual(m.col_idx("BZ11"),77)
        with self.assertRaisesRegex(ValueError,"INVALID_REAL_XLSX_CELL_REF"):
            m.col_idx("../external")

    def test_non_original_source_host_is_never_used(self):
        self.assertTrue(m.OA_SUPP.startswith("https://www.ebi.ac.uk/"))
        self.assertFalse("photos" in m.OA_SUPP)
        self.assertNotIn("wind",m.SOURCE_ARTICLE)

if __name__=="__main__":
    unittest.main()
