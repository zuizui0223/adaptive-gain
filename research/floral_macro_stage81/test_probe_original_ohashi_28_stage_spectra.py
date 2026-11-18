import io,unittest,zipfile
from unittest.mock import patch
import probe_original_ohashi_28_stage_spectra as m

class SourceStructureTests(unittest.TestCase):
    @staticmethod
    def make_source(paths):
        memory=io.BytesIO()
        with zipfile.ZipFile(memory,"w") as z:
            for path in paths:z.writestr(path,b'not actual XLS')
        memory.seek(0)
        return zipfile.ZipFile(memory)
    def test_exact_match_does_not_collapse_infraspecific_taxa(self):
        z=self.make_source(["Reflectance/Test_alpha/1a.xls",
                            "Reflectance/Test_beta/2a.xls"])
        with patch.object(m,"PINNED_PUBLISHED_SPECIES",2),patch.object(m,"PINNED_CROSSWALK_COUNT",1):
            t,match,files=m.source_archive_crosswalk(z,["test alpha"])
            self.assertEqual(len(t),1)
            self.assertEqual(t[0]["n_original_spectral_workbooks"],1)
            self.assertEqual(t[0]["sample_first_12_original_filenames"],["1a.xls"])
    def test_unsupported_species_names_are_not_fuzzily_matched(self):
        z=self.make_source(["Reflectance/Test_alpha/1a.xls",
                            "Reflectance/Test_beta/2a.xls"])
        with patch.object(m,"PINNED_PUBLISHED_SPECIES",2),patch.object(m,"PINNED_CROSSWALK_COUNT",1):
            with self.assertRaisesRegex(ValueError,"28_ORIGINAL_ACCEPTED"):
                m.source_archive_crosswalk(z,["test gamma"])
    def test_no_workbooks_is_not_a_negative_flower_trait(self):
        z=self.make_source(["Reflectance/Test_alpha/README.txt"])
        with patch.object(m,"PINNED_PUBLISHED_SPECIES",1),patch.object(m,"PINNED_CROSSWALK_COUNT",1):
            with self.assertRaisesRegex(ValueError,"WITHOUT_SPECTRAL_SHEETS"):
                m.source_archive_crosswalk(z,["test alpha"])

if __name__=="__main__":unittest.main()
