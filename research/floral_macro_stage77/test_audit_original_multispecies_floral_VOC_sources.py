"""Source-free controls for prospective 305-species floral scent meta source."""
import importlib.util,unittest,zipfile,io
from pathlib import Path

p=Path(__file__).with_name("audit_original_multispecies_floral_VOC_sources.py")
sp=importlib.util.spec_from_file_location("stage77c_VOC",p)
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)

class FloralScentSourceGuards(unittest.TestCase):
    def test_source_305_is_published_meta_not_own_extracted_data(self):
        self.assertEqual(m.SOURCE_PUBLISHED_NOT_RECALCULATED["plants"],305)
        self.assertEqual(m.SOURCE_PUBLISHED_NOT_RECALCULATED["VOC_compounds"],851)
        self.assertEqual(m.SOURCE_PUBLISHED_NOT_RECALCULATED["source_studies"],58)
        self.assertEqual(m.PMCID,"PMC7412988")
    def test_only_actual_author_HTML_links_are_considered(self):
        sample=(b'<a href="https://www.frontiersin.org/files/Articles/2020/s1.xlsx">supp</a>'
                b'<a href="https://attacker.invalid/x.xlsx">NO</a>'
                b'<a href="/files/Articles/2020/s2.zip">supp</a>')
        links=m.original_supp_links(sample)
        self.assertEqual(len(links),2)
        self.assertTrue(all("frontiersin.org" in x for x in links))
    def test_no_unapproved_private_host_scent_path(self):
        for url in ("file:///etc/passwd","https://github.com/other/","http://www.ebi.ac.uk/a"):
            with self.assertRaisesRegex(ValueError,"NON_AUTHORITATIVE"):
                m.source_get(url)
    def test_original_zip_members_are_source_only_not_co_measured_Bombus(self):
        mem=io.BytesIO()
        with zipfile.ZipFile(mem,"w") as z:
            z.writestr("original_table_s1.csv","plant,VOC\nSpecies 1,0.4\n")
        d=m.archive_inventory(mem.getvalue(),"s1.zip")
        self.assertEqual(d["source_archive_format"],"ZIP")
        self.assertEqual(d["n_actual_original_spreadsheets"],1)
        self.assertEqual(d["n_original_archive_files"],1)
    def test_invalid_original_material_not_counted_as_VOC(self):
        d=m.archive_inventory(b"<html>Cookie</html>","file.zip")
        self.assertFalse(d["source_original_biological_numeric_data_admitted"])
        self.assertEqual(d["source_archive_format"],"HTTP200_HTML_NOT_SOURCE_BINARY")
    def test_original_2020_source_data_cannot_be_made_up(self):
        self.assertEqual(len(m.HUED_NHM_SHA),64)
        self.assertEqual(len(m.EUPP_SHA),64)
        self.assertEqual(m.ARTICLE,"10.3389/fpls.2020.01154")
if __name__=="__main__":
    unittest.main()
