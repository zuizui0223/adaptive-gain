"""ZIP central index scientific fidelity tests; 219 is screened not positive."""
import importlib.util,unittest,struct
from pathlib import Path
p=Path(__file__).with_name("ohashi_2015_zip_central_directory_species_coverage.py")
s=importlib.util.spec_from_file_location("stage79d",p)
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class OriginalOhashiIndexTests(unittest.TestCase):
    def test_true_full_zip_285mb_never_mislabel_partial_MD5(self):
        self.assertEqual(m.SOURCE_ORIGINAL_SIZE,285933377)
        self.assertEqual(m.AUTHOR_MD5_NOT_FULLY_RECHECKED,
                         "d98ddd3b93fb79fdbaaa5eec5818c187")
    def test_real_folder_taxon_names_and_infraspecific_unresolved(self):
        f,e,unresolved=m.original_folder_species([
          "archive/Reflectance/Abelia_spathulata/Abelia-e1.xls",
          "archive/Reflectance/Rosa_rugosa/Rosa-e2.xls",
          "archive/Reflectance/Abelia_spathulata_var_sanguinea/a.xls",
        ])
        self.assertEqual(len(f),3)
        self.assertEqual(set(e),{"abelia spathulata","rosa rugosa"})
        self.assertEqual(unresolved,["Abelia_spathulata_var_sanguinea"])
    def test_original_219_archived_measurements_not_true_positive(self):
        self.assertTrue(m.ZIP_URL.startswith("https://zenodo.org/api/records/4942515/"))
    def test_source_partial_cannot_overread_archive_budget(self):
        with self.assertRaisesRegex(ValueError,"OUT_OF_BOUNDS"):
            m.partial(-1,500,None)
        with self.assertRaisesRegex(ValueError,"OUT_OF_BOUNDS"):
            m.partial(0,50000000,None)
if __name__=="__main__":unittest.main()
