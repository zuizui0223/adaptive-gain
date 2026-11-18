"""Original 219 source spectrometer taxon folders are not change negatives."""
import importlib.util,unittest
from pathlib import Path
s=importlib.util.spec_from_file_location("ohashi79",Path(__file__).with_name("ohashi_2015_zip_central_directory_species_coverage.py"))
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class OriginalOhashiArchiveTests(unittest.TestCase):
    def test_original_author_286mb_MD5_and_219_source_species_pin(self):
        self.assertEqual(m.SOURCE_BYTES,285933377)
        self.assertEqual(m.SOURCE_MD5,"d98ddd3b93fb79fdbaaa5eec5818c187")
        self.assertEqual(m.EXPECTED_SCREENED,219)
    def test_original_taxa_in_two_word_folder_not_infraspecific(self):
        paths=["Ohashi_etal/Reflectance/Rosa_rugosa/e1.xls",
               "Ohashi_etal/Reflectance/Abelia_spathulata_var_sanguinea/e1.xls",
               "Ohashi_etal/Reflectance/Genus_sp/e1.xls",
               "__MACOSX/._junk"]
        f,exact,infra,unknown=m.original_folders(paths)
        self.assertEqual(len(f),3)
        self.assertIn("rosa rugosa",exact)
        self.assertEqual(len(infra),1)
        self.assertIn("Genus_sp",unknown)
    def test_only_exact_source_species_name_matched(self):
        _,exact,_,_=m.original_folders(["Reflectance/Pulmonaria_officinalis/e1.xls"])
        self.assertIn("pulmonaria officinalis",exact)
        self.assertNotIn("pulmonaria",exact)
    def test_source_historical_MD5_cannot_be_claimed_on_partial_file(self):
        self.assertIn("zip/content",m.ORIGINAL_URL)
        self.assertEqual(len(m.SOURCE_STAGE69_SHA),64)
if __name__=="__main__":unittest.main()
